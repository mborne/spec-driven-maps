#!/usr/bin/env python3
"""Prépare les données de la carte touristique de Montmorillon.

Les lieux sont décrits dans scripts/lieux.json par une référence à leur source
(objet BD TOPO, notice Mérimée ou adresse) ; ce script résout ces références
auprès de la Géoplateforme et de data.gouv.fr, contrôle l'emprise du centre-ville
et vérifie que tous les monuments historiques de l'emprise sont présents.

Usage : python3 scripts/fetch_data.py
Sortie : data/tourisme.geojson
"""
import json
import math
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "scripts" / "lieux.json"
OUTPUT = ROOT / "data" / "tourisme.geojson"

WFS_URL = "https://data.geopf.fr/wfs"
GEOCODAGE_URL = "https://data.geopf.fr/geocodage/search"
# Immeubles protégés au titre des monuments historiques (Mérimée), via l'API tabulaire de data.gouv.fr
MERIMEE_URL = "https://tabular-api.data.gouv.fr/api/resources/3a52af4a-f9da-4dcc-8110-b07774dfb3bc/data/"
MERIMEE_COMMUNE = "Montmorillon"
POP_URL = "https://pop.culture.gouv.fr/notice/merimee/"

PRECISION = 6  # décimales conservées (~0,1 m)


def get_json(url, params):
    full_url = url + "?" + urllib.parse.urlencode(params)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(full_url, timeout=60) as response:
                return json.load(response)
        except OSError:
            if attempt == 2:
                raise
            time.sleep(2)


def wfs(typename, cql, count=100):
    collection = get_json(WFS_URL, {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "typeNames": typename,
        "outputFormat": "application/json",
        "count": str(count),
        "cql_filter": cql,
    })
    if len(collection["features"]) != collection.get("numberMatched", len(collection["features"])):
        raise SystemExit(f"Résultat WFS incomplet pour {typename}")
    return collection["features"]


def round_coords(coords):
    if isinstance(coords[0], (int, float)):
        return [round(c, PRECISION) for c in coords[:2]]
    return [round_coords(c) for c in coords]


def centroid(geometry):
    """Centroïde surfacique d'un (multi)polygone, milieu d'une ligne, ou le point lui-même."""
    if geometry["type"] == "Point":
        return geometry["coordinates"][:2]
    if geometry["type"] in ("LineString", "MultiLineString"):
        lines = geometry["coordinates"] if geometry["type"] == "MultiLineString" else [geometry["coordinates"]]
        points = [p for line in lines for p in line]
        return points[len(points) // 2][:2] if len(points) % 2 else [
            (points[len(points) // 2 - 1][0] + points[len(points) // 2][0]) / 2,
            (points[len(points) // 2 - 1][1] + points[len(points) // 2][1]) / 2,
        ]
    polygons = geometry["coordinates"] if geometry["type"] == "MultiPolygon" else [geometry["coordinates"]]
    area = cx = cy = 0.0
    for polygon in polygons:
        ring = polygon[0]
        for (x1, y1, *_), (x2, y2, *_) in zip(ring, ring[1:]):
            cross = x1 * y2 - x2 * y1
            area += cross / 2
            cx += (x1 + x2) * cross / 6
            cy += (y1 + y2) * cross / 6
    return [cx / area, cy / area]


def distance_m(a, b):
    kx = 111320 * math.cos(math.radians((a[1] + b[1]) / 2))
    return math.hypot((b[0] - a[0]) * kx, (b[1] - a[1]) * 110574)


def bbox_around(center, radius_m):
    dlon = radius_m / (111320 * math.cos(math.radians(center[1])))
    dlat = radius_m / 110574
    return [center[0] - dlon, center[1] - dlat, center[0] + dlon, center[1] + dlat]


def fetch_bdtopo(typename, cleabs):
    features = wfs(typename, f"cleabs = '{cleabs}'")
    if len(features) != 1:
        raise SystemExit(f"{typename} {cleabs} : {len(features)} objet(s) trouvé(s)")
    return features[0]


def fetch_merimee():
    result = get_json(MERIMEE_URL, {"Commune_forme_index__exact": MERIMEE_COMMUNE, "page_size": 50})
    notices = {}
    for row in result["data"]:
        coords = row.get("coordonnees_au_format_WGS84")
        if coords:
            lat, lon = (float(v) for v in coords.split(","))
            row["_lonlat"] = [lon, lat]
        notices[row["Reference"]] = row
    return notices


def protection(notice):
    """« classé », « inscrit » ou « classé et inscrit », avec « (partiellement) » le cas échéant."""
    typologie = notice.get("Typologie_de_la_protection") or ""
    statuts = [s for s in ("classé", "inscrit") if s in typologie]
    label = " et ".join(statuts)
    return label + (" (partiellement)" if "partiellement" in typologie else "")


def geocode(q):
    result = get_json(GEOCODAGE_URL, {"q": q, "index": "address", "limit": 1})
    feature = result["features"][0]
    if feature["properties"]["type"] != "housenumber":
        raise SystemExit(f"Géocodage imprécis pour « {q} » : {feature['properties']['label']}")
    return feature


def merimee_address(value):
    """« Augustins (rue des) 4 » → « 4 rue des Augustins »."""
    match = re.fullmatch(r"(.+?) \((.+?)\)\s*(\S*)", (value or "").strip())
    if not match:
        return value or None
    nom, voie, numero = match.groups()
    return " ".join(part for part in (numero, voie, nom) if part)


def normalize_address(value, commune="86500 Montmorillon"):
    """Graphie de la Base Adresse Nationale (« 5 AV PASTEUR » → « 5 Avenue Pasteur »), si l'adresse y est trouvée."""
    value = (value or "").strip()
    if not value:
        return None
    result = get_json(GEOCODAGE_URL, {"q": f"{value} {commune}", "index": "address", "limit": 1})
    if result["features"]:
        p = result["features"][0]["properties"]
        if p["type"] in ("housenumber", "street") and p["citycode"] == "86165" and p.get("score", 0) > 0.6:
            value = p["name"]
    # « Saint-christophe » → « Saint-Christophe » ; « place … » → « Place … »
    value = re.sub(r"\b(Saint|Sainte)-([a-zà-ÿ])", lambda m: f"{m.group(1)}-{m.group(2).upper()}", value)
    return value[0].upper() + value[1:]


def main():
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    categories = config["categories"]
    merimee = fetch_merimee()
    print(f"Mérimée : {len(merimee)} notices pour {MERIMEE_COMMUNE}")

    centre_ref = config["emprise"]["centre"]
    centre = centroid(fetch_bdtopo(centre_ref["type"], centre_ref["cleabs"])["geometry"])
    rayon = config["emprise"]["rayon_m"]

    features = []
    for lieu in config["lieux"]:
        source = lieu["source"]
        props = {
            "id": lieu["id"],
            "categorie": lieu["categorie"],
            "nom": lieu["nom"],
            "description": lieu["description"],
        }
        if source["type"] == "merimee":
            notice = merimee[source["reference"]]
            coords = notice["_lonlat"]
            adresse = normalize_address(merimee_address(notice.get("Adresse_forme_index")))
            props["source"] = f"Culture – Mérimée ({source['reference']})"
        elif source["type"] == "adresse":
            result = geocode(source["q"])
            coords = result["geometry"]["coordinates"]
            adresse = result["properties"]["name"]
            props["source"] = "Adresse géocodée (Géoplateforme)"
        else:
            feature = fetch_bdtopo(source["type"], source["cleabs"])
            coords = centroid(feature["geometry"])
            adresse = normalize_address(feature["properties"].get("adresse_postale"))
            props["source"] = f"IGN – BD TOPO® ({source['cleabs']})"
        if adresse:
            props["adresse"] = adresse
        if lieu.get("site"):
            props["site"] = lieu["site"]
        if lieu.get("merimee"):
            notice = merimee[lieu["merimee"]]
            props["mh"] = lieu.get("protection") or protection(notice)
            props["mh_reference"] = lieu["merimee"]
            props["mh_url"] = POP_URL + lieu["merimee"]
            props["mh_titre"] = notice["Titre_editorial_de_la_notice"]
            if lieu.get("partie"):
                props["mh_partie"] = lieu["partie"]
            # Siècles de la notice entière : non affichés pour une partie d'ensemble
            siecle = notice.get("Siecle_de_la_campagne_principale_de_construction")
            if siecle and not lieu.get("partie"):
                props["mh_siecle"] = siecle.replace(";", ", ")

        d = distance_m(centre, coords)
        if d > rayon:
            raise SystemExit(f"{lieu['id']} hors de l'emprise ({d:.0f} m > {rayon} m)")
        features.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": round_coords(coords)}, "properties": props})
        print(f"{categories[lieu['categorie']]['libelle']:22} {lieu['nom']:40} {d:5.0f} m  {props.get('mh', '')}")

    # Contrôle : tous les monuments Mérimée de l'emprise sont associés à un lieu
    references = {lieu.get("merimee") for lieu in config["lieux"]}
    for ref, notice in merimee.items():
        if "_lonlat" in notice and distance_m(centre, notice["_lonlat"]) <= rayon and ref not in references:
            raise SystemExit(f"Monument historique absent de lieux.json : {ref} {notice['Titre_editorial_de_la_notice']}")
    hors = [f"{ref} {n['Titre_editorial_de_la_notice']}" for ref, n in merimee.items()
            if "_lonlat" not in n or distance_m(centre, n["_lonlat"]) > rayon]
    print(f"Monuments hors emprise ou sans coordonnées ({len(hors)}) : {'; '.join(hors)}")

    # Gartempe : tronçons BD TOPO dans l'emprise
    west, south, east, north = bbox_around(centre, rayon * 1.5)
    troncons = wfs("BDTOPO_V3:troncon_hydrographique",
                   f"BBOX(geometrie,{west},{south},{east},{north},'EPSG:4326') AND cpx_toponyme_de_cours_d_eau = 'la Gartempe'")
    features.append({
        "type": "Feature",
        "geometry": {"type": "MultiLineString", "coordinates": [round_coords(t["geometry"]["coordinates"]) for t in troncons]},
        "properties": {"categorie": "riviere", "nom": "La Gartempe", "source": "IGN – BD TOPO® (tronçons hydrographiques)"},
    })
    print(f"Gartempe : {len(troncons)} tronçons")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "categories": categories, "features": features},
                  f, ensure_ascii=False, indent=1)
    print(f"{len(features)} objets écrits dans {OUTPUT} ({OUTPUT.stat().st_size / 1e3:.0f} ko)")


if __name__ == "__main__":
    main()
