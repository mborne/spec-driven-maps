#!/usr/bin/env python3
"""Réduit les vignes de la BD TOPO (France métropolitaine) à leur surface et leur centroïde.

Les zones de végétation de nature « Vigne » (BDTOPO_V3:zone_de_vegetation) sont
téléchargées depuis le WFS de la Géoplateforme par dalles en Lambert-93. Les dalles
sont subdivisées (quadtree) tant qu'elles contiennent plus de MAX_PER_TILE objets,
ce qui évite la pagination profonde du WFS, trop lente. Les géométries ne sont pas
conservées : chaque polygone est réduit à sa surface planaire (m²) et à son centroïde
en Lambert-93, rattaché ensuite à sa commune par scripts/build_communes.sh.

Chaque dalle terminée est mise en cache (data/cache-vignes/) : une extraction interrompue
reprend là où elle s'est arrêtée. Supprimer ce dossier pour repartir de zéro.

Usage : python3 scripts/fetch_vignes.py
Sorties : data/vignes-centroides.csv (non versionné), data/fetch_vignes.log.json
"""
import csv
import json
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

WFS_URL = "https://data.geopf.fr/wfs"
TYPENAME = "BDTOPO_V3:zone_de_vegetation"
NATURE_FILTER = "nature = 'Vigne'"
# Emprise métropolitaine (Corse comprise) en Lambert-93
EXTENT = (99_000, 6_040_000, 1_250_000, 7_120_000)
START_TILE = 100_000  # taille des dalles initiales (m)
MAX_PER_TILE = 2_000  # au-delà, la dalle est subdivisée (limite WFS : 5 000 par page ; petites réponses plus fiables)
RETRIES = 4

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUTPUT = DATA_DIR / "vignes-centroides.csv"
LOG = DATA_DIR / "fetch_vignes.log.json"
CACHE_DIR = DATA_DIR / "cache-vignes"


def wfs(params):
    base = {"service": "WFS", "version": "2.0.0", "request": "GetFeature", "typeNames": TYPENAME}
    url = WFS_URL + "?" + urllib.parse.urlencode({**base, **params})
    for attempt in range(1, RETRIES + 1):
        try:
            with urllib.request.urlopen(url, timeout=180) as response:
                return response.read()
        except Exception as error:  # réseau ou délai du service
            if attempt == RETRIES:
                raise
            print(f"  nouvel essai ({attempt}/{RETRIES}) : {error}")
            time.sleep(5 * attempt)


def bbox_filter(tile):
    x1, y1, x2, y2 = tile
    return f"{NATURE_FILTER} AND BBOX(geometrie,{x1},{y1},{x2},{y2},'EPSG:2154')"


def count(cql):
    body = wfs({"resultType": "hits", "cql_filter": cql}).decode()
    return int(body.split('numberMatched="')[1].split('"')[0])


def fetch_tile(tile, n):
    """Réduit les vignes d'une dalle à (cleabs, x, y, surface), avec relance si la réponse
    est tronquée ou incomplète."""
    for attempt in range(1, RETRIES + 1):
        body = wfs({"outputFormat": "application/json", "srsName": "EPSG:2154", "count": "5000",
                    "propertyName": "cleabs,geometrie", "cql_filter": bbox_filter(tile)})
        try:
            features = json.loads(body)["features"]
        except (json.JSONDecodeError, KeyError) as error:
            print(f"  réponse illisible ({attempt}/{RETRIES}) : {str(error)[:80]}")
            time.sleep(5 * attempt)
            continue
        if len(features) != n:
            print(f"  dalle incomplète ({attempt}/{RETRIES}) : {len(features)} / {n}")
            time.sleep(5 * attempt)
            continue
        rows = []
        for feature in features:
            area, cx, cy = polygon_area_centroid(feature["geometry"])
            if cx is not None:
                rows.append((feature["properties"]["cleabs"], round(cx, 1), round(cy, 1), round(area, 1)))
        return rows
    raise SystemExit(f"Dalle {tile} : échec après {RETRIES} essais")


def ring_area_centroid(ring):
    """Surface signée et centroïde d'un anneau (formule du lacet)."""
    a = cx = cy = 0.0
    for (x1, y1), (x2, y2) in zip(ring, ring[1:]):
        cross = x1 * y2 - x2 * y1
        a += cross
        cx += (x1 + x2) * cross
        cy += (y1 + y2) * cross
    a /= 2
    if a == 0:
        return 0.0, ring[0][0], ring[0][1]
    return a, cx / (6 * a), cy / (6 * a)


def polygon_area_centroid(geometry):
    polygons = geometry["coordinates"] if geometry["type"] == "MultiPolygon" else [geometry["coordinates"]]
    total = sx = sy = 0.0
    for polygon in polygons:
        for i, ring in enumerate(polygon):
            ring = [p[:2] for p in ring]
            a, cx, cy = ring_area_centroid(ring)
            a = abs(a) if i == 0 else -abs(a)  # anneaux intérieurs soustraits
            total += a
            sx += a * cx
            sy += a * cy
    if total <= 0:
        return 0.0, None, None
    return total, sx / total, sy / total


def tiles(extent, size):
    x1, y1, x2, y2 = extent
    for x in range(x1, x2, size):
        for y in range(y1, y2, size):
            yield (x, y, min(x + size, x2), min(y + size, y2))


def split(tile):
    x1, y1, x2, y2 = tile
    xm, ym = (x1 + x2) // 2, (y1 + y2) // 2
    return [(x1, y1, xm, ym), (xm, y1, x2, ym), (x1, ym, xm, y2), (xm, ym, x2, y2)]


def main():
    started = time.time()
    national = count(NATURE_FILTER)
    print(f"{national} vignes au total dans {TYPENAME} (France entière)")

    seen = set()
    rows = []
    log = {"date": date.today().isoformat(), "typename": TYPENAME, "filter": NATURE_FILTER,
           "national_count": national, "tiles": []}
    stack = list(tiles(EXTENT, START_TILE))
    requests = 0

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    while stack:
        tile = stack.pop()
        cache = CACHE_DIR / ("_".join(map(str, tile)) + ".csv")
        if cache.exists():
            with cache.open(encoding="utf-8") as f:
                tile_rows = [(r[0], float(r[1]), float(r[2]), float(r[3])) for r in csv.reader(f)]
            n = len(tile_rows)
        else:
            n = count(bbox_filter(tile))
            requests += 1
            if n == 0:
                continue
            if n > MAX_PER_TILE:
                stack.extend(split(tile))
                continue
            tile_rows = fetch_tile(tile, n)
            requests += 1
            with cache.open("w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerows(tile_rows)
        new = 0
        for row in tile_rows:
            if row[0] in seen:
                continue
            seen.add(row[0])
            rows.append(row)
            new += 1
        log["tiles"].append({"bbox": tile, "count": n, "new": new})
        print(f"dalle {tile} : {n} objets, {new} nouveaux – total {len(seen)}")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["cleabs", "x", "y", "surface_m2"])
        writer.writerows(rows)

    total_area = sum(r[3] for r in rows)
    log.update({"metropole_count": len(seen), "outside_extent": national - len(seen),
                "surface_ha": round(total_area / 10_000),
                "requests": requests, "duration_s": round(time.time() - started)})
    LOG.write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(seen)} vignes distinctes en métropole ({national - len(seen)} hors emprise), "
          f"{total_area / 10_000:,.0f} ha -> {OUTPUT}")


if __name__ == "__main__":
    main()
