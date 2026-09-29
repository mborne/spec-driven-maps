# Plan technique – commune-doubs

## Données

| Élément | Choix |
|---|---|
| Source | WFS Géoplateforme `https://data.geopf.fr/wfs` |
| Type | `BDTOPO_V3:commune` |
| Filtre | `code_insee_du_departement = '25'` (563 communes) |
| Propriétés | `code_insee`, `nom_officiel`, `population`, `superficie_cadastrale` (ha), `date_du_recensement`, `geometrie` |

Démarche d'identification avec le MCP geocontext :

1. `gpf_wfs_search_types` (« commune ») → `BDTOPO_V3:commune` retenu car il porte `population` et `superficie_cadastrale`. Les types `ADMINEXPRESS-COG.*` sont millésimés et `CADASTRALPARCELS.PARCELLAIRE_EXPRESS:commune` ne porte pas la population.
2. `gpf_wfs_describe_type` → noms exacts des propriétés.
3. `gpf_wfs_get_features` avec `result_type=hits` → 563 communes.
4. `gpf_wfs_get_features` avec `result_type=request` → URL WFS reprise dans `scripts/fetch_data.py`.

## Traitement (`scripts/fetch_data.py`)

- Téléchargement GeoJSON (EPSG:4326) et contrôle de complétude (`numberMatched`).
- `densite = population / (superficie_cadastrale / 100)` en hab/km², arrondie à 0,1. On utilise la superficie Insee plutôt qu'un calcul géométrique, par cohérence avec les densités publiées par l'Insee.
- Coordonnées arrondies à 5 décimales (~1 m), soit un fichier d'environ 3 Mo sans simplification.
- Sortie : `data/communes-doubs-brut.geojson`, intermédiaire non versionné (`.gitignore`).

## Simplification (`scripts/simplify.sh`)

Avec [mapshaper](https://mborne.github.io/outils/mapshaper/) (`npx mapshaper@0.7`, Node.js requis) :

```bash
mapshaper communes-doubs-brut.geojson -clean -simplify 10% keep-shapes -o precision=0.00001 format=geojson communes-doubs.geojson
```

- `-clean` répare la topologie ; `-simplify 10%` (Visvalingam) conserve 10 % des sommets ; `keep-shapes` évite la disparition des petites communes.
- mapshaper travaille sur la topologie : les limites partagées sont simplifiées une seule fois, sans trou ni chevauchement entre communes.
- Résultat : 563 communes, ~0,5 Mo contre ~3,2 Mo (20 % → 0,8 Mo, 5 % → 0,36 Mo ; 10 % garde un tracé fidèle à l'échelle communale).
- Sortie : `data/communes-doubs.geojson`, versionnée pour la reproductibilité.

Remarque : `date_du_recensement` n'est pas homogène (2022 ou 2023 selon les communes). La date est affichée dans la popup.

## Symbologie

Choroplèthe en classes fixes, adaptées à une distribution très asymétrique (médiane ≈ 39 hab/km², maximum ≈ 1 823 pour Besançon) :

| Classe (hab/km²) | Couleur | Nb communes |
|---|---|---|
| < 25 | `#ffffb2` | 185 |
| 25 – 50 | `#fed976` | 150 |
| 50 – 100 | `#feb24c` | 109 |
| 100 – 250 | `#fd8d3c` | 72 |
| 250 – 500 | `#fc4e2a` | 29 |
| 500 – 1000 | `#e31a1c` | 11 |
| ≥ 1000 | `#b10026` | 7 |

Opacité de remplissage 0,75, contours blancs de 0,5 px. Les couches sont insérées sous les libellés du fond.

## Rendu

- MapLibre GL JS v5 (CDN jsdelivr), un seul fichier `index.html`.
- Fond : Plan IGN vecteur en niveaux de gris (style officiel `gris`), `https://data.geopf.fr/annexes/ressources/vectorTiles/styles/PLAN.IGN/gris.json`. Le fond neutre ne concurrence pas la rampe de couleurs de la choroplèthe.
- Vue initiale : emprise du Doubs `[5.699, 46.554, 7.062, 47.580]`.
- Chargement : message « Chargement des communes… » centré sur la carte (`role="status"`), masqué à l'événement `sourcedata` de la source `communes` lorsque `isSourceLoaded` est vrai ; remplacé par un message d'échec sur l'événement `error` de cette source. Le GeoJSON pèse environ 0,5 Mo après simplification.
- Mentions légales : lien vers `https://mborne.github.io/mentions-legales/` dans un bloc distinct, centré en bas de carte (convention commune, voir le [README](../../README.md)). Les sources restent dans le contrôle d'attribution MapLibre, en bas à droite. Si l'attribution déployée chevauche les mentions (écran étroit), celles-ci sont remontées juste au-dessus.

## Hébergement

GitHub Pages depuis la racine du dépôt. La carte est servie sous `/<depot>/commune-doubs/`. Tous les chemins sont relatifs.
