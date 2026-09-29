#!/usr/bin/env python3
"""Prépare les données de la carte d'accès au Printemps des Cartes 2026 à partir
des services de la Géoplateforme : géocodage du lieu, gare et parkings (BD TOPO V3),
nommage des parkings par géocodage inverse et distances à pied (service d'itinéraire).

Usage : python3 scripts/fetch_data.py
Sortie : data/acces.geojson
"""
import json
import math
import time
import urllib.parse
import urllib.request
from pathlib import Path

ADRESSE = "16 rue des Récollets 86500 Montmorillon"
NOM_LIEU = "Festival Printemps des Cartes"
RAYON_M = 1500  # rayon de recherche des parkings et de la gare autour du lieu

GEOCODAGE_URL = "https://data.geopf.fr/geocodage"
WFS_URL = "https://data.geopf.fr/wfs"
ITINERAIRE_URL = "https://data.geopf.fr/navigation/itineraire"
NATURES = ["Parking", "Gare voyageurs et fret", "Gare voyageurs uniquement"]

PRECISION = 6  # décimales conservées (~0,1 m)
OUTPUT = Path(__file__).resolve().parent.parent / "data" / "acces.geojson"


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


def round_coords(coords):
    if isinstance(coords[0], (int, float)):
        return [round(c, PRECISION) for c in coords[:2]]
    return [round_coords(c) for c in coords]


def geocode(adresse):
    result = get_json(f"{GEOCODAGE_URL}/search", {"q": adresse, "index": "address", "limit": 1})
    feature = result["features"][0]
    if feature["properties"]["type"] != "housenumber":
        raise SystemExit(f"Géocodage imprécis : {feature['properties']['label']}")
    return feature


def reverse_street(lon, lat):
    result = get_json(f"{GEOCODAGE_URL}/reverse", {"lon": lon, "lat": lat, "index": "address", "limit": 1})
    props = result["features"][0]["properties"]
    return props.get("street") or props["name"]


def fetch_equipements(lon, lat):
    natures = ", ".join(f"'{n}'" for n in NATURES)
    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "typeNames": "BDTOPO_V3:equipement_de_transport",
        "outputFormat": "application/json",
        "count": "100",
        "propertyName": "cleabs,nature,toponyme,adresse_postale,geometrie",
        "cql_filter": f"DWITHIN(geometrie,SRID=4326;POINT({lon} {lat}),{RAYON_M},meters) AND nature IN ({natures})",
    }
    collection = get_json(WFS_URL, params)
    if len(collection["features"]) != collection.get("numberMatched", len(collection["features"])):
        raise SystemExit("Résultat WFS incomplet")
    return collection["features"]


def centroid(geometry):
    """Centroïde surfacique (premier anneau de chaque polygone), en lon/lat."""
    polygons = geometry["coordinates"] if geometry["type"] == "MultiPolygon" else [geometry["coordinates"]]
    area = cx = cy = 0.0
    for polygon in polygons:
        ring = polygon[0]
        for (x1, y1, *_), (x2, y2, *_) in zip(ring, ring[1:]):
            cross = x1 * y2 - x2 * y1
            area += cross / 2
            cx += (x1 + x2) * cross / 6
            cy += (y1 + y2) * cross / 6
    return cx / area, cy / area


def distance_m(lon1, lat1, lon2, lat2):
    kx = 111320 * math.cos(math.radians((lat1 + lat2) / 2))
    return math.hypot((lon2 - lon1) * kx, (lat2 - lat1) * 110574)


def pedestrian_route(start, end):
    return get_json(ITINERAIRE_URL, {
        "resource": "bdtopo-osrm",
        "profile": "pedestrian",
        "optimization": "fastest",
        "start": f"{start[0]},{start[1]}",
        "end": f"{end[0]},{end[1]}",
        "geometryFormat": "geojson",
        "getSteps": "false",
    })


def point(coords, **props):
    return {"type": "Feature", "geometry": {"type": "Point", "coordinates": round_coords(coords)}, "properties": props}


def main():
    lieu = geocode(ADRESSE)
    lon, lat = lieu["geometry"]["coordinates"]
    print(f"Lieu : {lieu['properties']['label']} ({lon}, {lat})")

    features = [point([lon, lat], categorie="lieu", nom=NOM_LIEU, adresse=lieu["properties"]["label"])]
    route_gare = None

    for eq in fetch_equipements(lon, lat):
        p = eq["properties"]
        c = centroid(eq["geometry"])
        route = pedestrian_route(c, (lon, lat))
        props = {
            "cleabs": p["cleabs"],
            "distance_m": round(route["distance"]),
            "duree_min": max(1, round(route["duration"] / 60)),
            "vol_oiseau_m": round(distance_m(c[0], c[1], lon, lat)),
        }
        if p["nature"] == "Parking":
            # Parkings rarement nommés dans la BD TOPO : nommés par la voie la plus proche
            rue = reverse_street(*c)
            voie = rue[0].lower() + rue[1:]
            props["categorie"] = "parking"
            props["nom"] = f"Parking {p['toponyme']} ({voie})" if p["toponyme"] else f"Parking {voie}"
            props["adresse"] = f"{rue}, Montmorillon"
            features.append({
                "type": "Feature",
                "geometry": {"type": eq["geometry"]["type"], "coordinates": round_coords(eq["geometry"]["coordinates"])},
                "properties": {"categorie": "parking-emprise", "cleabs": p["cleabs"]},
            })
        else:
            props["categorie"] = "gare"
            props["nom"] = p["toponyme"] or "Gare"
            # adresse_postale est en majuscules sans accents : numéro BD TOPO + voie BAN
            numero = (p["adresse_postale"] or "").split(" ")[0]
            rue = reverse_street(*c)
            props["adresse"] = f"{numero + ' ' if numero.isdigit() else ''}{rue}, Montmorillon"
            route_gare = route
        features.append(point(c, **props))
        print(f"{props['nom']:32} {props['adresse']:42} {props['distance_m']:5} m {props['duree_min']:3} min")

    if route_gare is None:
        raise SystemExit("Gare introuvable")
    features.append({
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": round_coords(route_gare["geometry"]["coordinates"])},
        "properties": {
            "categorie": "itineraire",
            "distance_m": round(route_gare["distance"]),
            "duree_min": round(route_gare["duration"] / 60),
        },
    })

    # Tri stable : lieu, gare, parkings par distance à pied croissante
    ordre = {"lieu": 0, "gare": 1, "parking": 2}
    features.sort(key=lambda f: (ordre.get(f["properties"]["categorie"], 3), f["properties"].get("distance_m", 0)))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "features": features}, f, ensure_ascii=False, indent=1)
    print(f"{len(features)} objets écrits dans {OUTPUT} ({OUTPUT.stat().st_size / 1e3:.0f} ko)")


if __name__ == "__main__":
    main()
