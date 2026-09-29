#!/usr/bin/env bash
# Télécharge et simplifie les grandes régions productrices de vins AOP.
# Source : https://www.data.gouv.fr/datasets/6126659ca058ff97a694a473 (CC-BY)
# Voir https://mborne.github.io/outils/mapshaper/
#
# Usage : bash scripts/fetch_bassins.sh
# Sortie : data/bassins-aop.geojson
set -euo pipefail

DATA_DIR="$(cd "$(dirname "$0")/../data" && pwd)"
URL="https://static.data.gouv.fr/resources/cartes-des-grandes-regions-productrices-de-vins-aop-en-france/20210826-082459/bassinsviticolesfranceaop.geojson"
RAW="$DATA_DIR/bassins-aop-brut.geojson"

curl -sSfL "$URL" -o "$RAW"

# -clean : répare la topologie ; -simplify 15% keep-shapes : Visvalingam
# precision=0.0001 : coordonnées à 4 décimales (~10 m), suffisant pour des contours de bassins
npx -y mapshaper@0.7 "$RAW" \
  -clean \
  -simplify 15% keep-shapes \
  -rename-fields nom=Bassin \
  -o precision=0.0001 format=geojson "$DATA_DIR/bassins-aop.geojson"

# Un point d'étiquette par bassin, garanti à l'intérieur du contour (-points inner)
npx -y mapshaper@0.7 "$DATA_DIR/bassins-aop.geojson" \
  -points inner \
  -o precision=0.0001 format=geojson "$DATA_DIR/bassins-aop-labels.geojson"

rm -f "$RAW"
