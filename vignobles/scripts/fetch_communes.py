#!/usr/bin/env python3
"""Télécharge les communes de France métropolitaine (ADMIN EXPRESS COG CARTO) en Lambert-93.

Type WFS : ADMINEXPRESS-COG-CARTO.LATEST:commune (Géoplateforme). Le téléchargement se
fait département par département pour éviter la pagination profonde du WFS.

Usage : python3 scripts/fetch_communes.py
Sortie : data/communes-cog-carto.geojson (non versionné, entrée de build_communes.sh)
"""
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

WFS_URL = "https://data.geopf.fr/wfs"
TYPENAME = "ADMINEXPRESS-COG-CARTO.LATEST:commune"
PROPERTIES = "code_insee,nom_officiel,code_insee_du_departement,superficie_cadastrale,geometrie"
DEPARTEMENTS = [f"{i:02d}" for i in range(1, 96) if i != 20] + ["2A", "2B"]
RETRIES = 4
OUTPUT = Path(__file__).resolve().parent.parent / "data" / "communes-cog-carto.geojson"


def get(params):
    base = {"service": "WFS", "version": "2.0.0", "request": "GetFeature", "typeNames": TYPENAME}
    url = WFS_URL + "?" + urllib.parse.urlencode({**base, **params})
    for attempt in range(1, RETRIES + 1):
        try:
            with urllib.request.urlopen(url, timeout=180) as response:
                return json.load(response)
        except Exception as error:
            if attempt == RETRIES:
                raise
            print(f"  nouvel essai ({attempt}/{RETRIES}) : {error}")
            time.sleep(5 * attempt)


def main():
    features = []
    for dep in DEPARTEMENTS:
        collection = get({"outputFormat": "application/json", "srsName": "EPSG:2154", "count": "5000",
                          "propertyName": PROPERTIES,
                          "cql_filter": f"code_insee_du_departement = '{dep}'"})
        batch = collection["features"]
        if len(batch) != collection.get("numberMatched", len(batch)) or not batch:
            raise SystemExit(f"Département {dep} incomplet : {len(batch)} / {collection.get('numberMatched')}")
        for feature in batch:
            feature.pop("geometry_name", None)
            feature.pop("id", None)
        features.extend(batch)
        print(f"{dep} : {len(batch)} communes (total {len(features)})")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection",
                   "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::2154"}},
                   "features": features}, f, ensure_ascii=False, separators=(",", ":"))
    print(f"{len(features)} communes métropolitaines -> {OUTPUT} ({OUTPUT.stat().st_size / 1e6:.0f} Mo)")


if __name__ == "__main__":
    main()
