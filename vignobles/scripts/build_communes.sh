#!/usr/bin/env bash
# Densité de vignoble par commune : rattache les vignes (centroïdes) à leur commune,
# puis produit la couche communale simplifiée pour l'affichage web.
#
# Usage : bash scripts/build_communes.sh
#   (après python3 scripts/fetch_vignes.py et python3 scripts/fetch_communes.py)
# Entrées : data/vignes-centroides.csv, data/communes-cog-carto.geojson (Lambert-93)
# Sorties : data/vignes-communes.csv (agrégats, versionné)
#           data/communes-vigne.geojson (WGS84, communes ayant de la vigne)
# Requiert GDAL/OGR avec SpatiaLite et Node.js (mapshaper via npx).
set -euo pipefail

DATA_DIR="$(cd "$(dirname "$0")/../data" && pwd)"
DB="$DATA_DIR/jointure.sqlite"
rm -f "$DB"

# 1. Base SpatiaLite : communes (polygones) + vignes (points), en Lambert-93, avec index spatial
ogr2ogr -f SQLite -dsco SPATIALITE=YES "$DB" "$DATA_DIR/communes-cog-carto.geojson" \
  -nln communes -a_srs EPSG:2154 -nlt MULTIPOLYGON
ogr2ogr -append "$DB" "$DATA_DIR/vignes-centroides.csv" -nln vignes -a_srs EPSG:2154 \
  -oo X_POSSIBLE_NAMES=x -oo Y_POSSIBLE_NAMES=y -oo KEEP_GEOM_COLUMNS=NO -oo AUTODETECT_TYPE=YES

# 2. Jointure point dans polygone (index spatial SpatiaLite) et agrégation par commune
ogr2ogr -f CSV "$DATA_DIR/vignes-communes.csv" "$DB" -sql "
  SELECT c.code_insee AS code_insee, ROUND(SUM(v.surface_m2)) AS surface_m2, COUNT(*) AS n
  FROM communes c
  JOIN vignes v ON ST_Within(v.GEOMETRY, c.GEOMETRY)
    AND v.ROWID IN (SELECT ROWID FROM SpatialIndex WHERE f_table_name = 'vignes' AND search_frame = c.GEOMETRY)
  GROUP BY c.code_insee
  ORDER BY c.code_insee"

# Contrôle : vignes non rattachées à une commune (centroïde hors contour généralisé, en mer…)
TOTAL=$(($(wc -l < "$DATA_DIR/vignes-centroides.csv") - 1))
RATTACHEES=$(awk -F, 'NR > 1 { s += $3 } END { print s }' "$DATA_DIR/vignes-communes.csv")
echo "Vignes rattachées à une commune : $RATTACHEES / $TOTAL"
rm -f "$DB"

# 3. Couche d'affichage : simplification sur l'ensemble des communes (limites jointives),
#    jointure des agrégats, part de la superficie cadastrale (ha), communes ≥ 1 ha de vigne, WGS84
# Voir https://mborne.github.io/outils/mapshaper/
npx -y mapshaper@0.7 "$DATA_DIR/communes-cog-carto.geojson" \
  -proj init=EPSG:2154 crs=wgs84 \
  -clean \
  -simplify 5% keep-shapes \
  -join "$DATA_DIR/vignes-communes.csv" keys=code_insee,code_insee field-types=code_insee:str,surface_m2:num,n:num \
  -filter 'surface_m2 >= 10000' \
  -each 'surface_ha = Math.round(surface_m2 / 1000) / 10, part = Math.round(1000 * surface_m2 / (superficie_cadastrale * 10000)) / 10, delete surface_m2, delete superficie_cadastrale, delete code_insee_du_departement' \
  -o precision=0.0001 format=geojson "$DATA_DIR/communes-vigne.geojson"
