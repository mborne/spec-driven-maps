#!/usr/bin/env bash
# Simplifie les communes du Doubs avec mapshaper pour l'affichage web.
# Voir https://mborne.github.io/outils/mapshaper/
#
# Usage : bash scripts/simplify.sh (après python3 scripts/fetch_data.py)
# Entrée : data/communes-doubs-brut.geojson
# Sortie : data/communes-doubs.geojson
set -euo pipefail

DATA_DIR="$(cd "$(dirname "$0")/../data" && pwd)"

# -clean : répare la topologie
# -simplify 10% keep-shapes : Visvalingam, conserve 10 % des sommets
#   sans faire disparaître de commune ; les limites partagées restent jointives
# precision=0.00001 : coordonnées à 5 décimales (~1 m)
npx -y mapshaper@0.7 "$DATA_DIR/communes-doubs-brut.geojson" \
  -clean \
  -simplify 10% keep-shapes \
  -o precision=0.00001 format=geojson "$DATA_DIR/communes-doubs.geojson"
