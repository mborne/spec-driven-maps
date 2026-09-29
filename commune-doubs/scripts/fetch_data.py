#!/usr/bin/env python3
"""Télécharge les communes du Doubs (BD TOPO V3) depuis le WFS de la Géoplateforme
et calcule la densité de population (hab/km²).

Usage : python3 scripts/fetch_data.py
Sortie : data/communes-doubs-brut.geojson (à simplifier avec scripts/simplify.sh)
"""
import json
import urllib.parse
import urllib.request
from pathlib import Path

WFS_URL = "https://data.geopf.fr/wfs"
PARAMS = {
    "service": "WFS",
    "version": "2.0.0",
    "request": "GetFeature",
    "typeNames": "BDTOPO_V3:commune",
    "outputFormat": "application/json",
    "count": "1000",
    "propertyName": "code_insee,nom_officiel,population,superficie_cadastrale,date_du_recensement,geometrie",
    "cql_filter": "code_insee_du_departement = '25'",
}
EXPECTED_COUNT = 563
PRECISION = 5  # décimales conservées (~1 m)
OUTPUT = Path(__file__).resolve().parent.parent / "data" / "communes-doubs-brut.geojson"


def round_coords(coords):
    if isinstance(coords[0], (int, float)):
        return [round(c, PRECISION) for c in coords]
    return [round_coords(c) for c in coords]


def main():
    url = WFS_URL + "?" + urllib.parse.urlencode(PARAMS)
    with urllib.request.urlopen(url, timeout=120) as response:
        collection = json.load(response)

    features = collection["features"]
    matched = collection.get("numberMatched", len(features))
    if len(features) != matched:
        raise SystemExit(f"Résultat incomplet : {len(features)} / {matched} communes")
    if matched != EXPECTED_COUNT:
        print(f"Attention : {matched} communes (attendu {EXPECTED_COUNT})")

    for feature in features:
        props = feature["properties"]
        superficie_km2 = props["superficie_cadastrale"] / 100
        props["densite"] = round(props["population"] / superficie_km2, 1)
        feature["geometry"]["coordinates"] = round_coords(feature["geometry"]["coordinates"])
        feature.pop("geometry_name", None)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as f:
        json.dump(
            {"type": "FeatureCollection", "features": features},
            f,
            ensure_ascii=False,
            separators=(",", ":"),
        )
    print(f"{len(features)} communes écrites dans {OUTPUT} ({OUTPUT.stat().st_size / 1e6:.1f} Mo)")


if __name__ == "__main__":
    main()
