# commune-doubs

Carte web de la **densité de population des communes du Doubs** (25), en habitants par km².

C'est l'exemple de départ, volontairement simple, qui pose le cadre de [spec-driven-maps](../README.md).

## La carte

- 563 communes colorées selon 7 classes de densité (de < 25 à ≥ 1000 hab/km²).
- Un message indique le chargement en cours des communes (~0,5 Mo).
- Un clic sur une commune affiche sa population, sa superficie et sa densité.
- Fond Plan IGN vecteur en niveaux de gris, rendu MapLibre GL JS.
- Sources : © IGN – BD TOPO® (`BDTOPO_V3:commune`), population municipale Insee.
- Lien vers les [mentions légales](https://mborne.github.io/mentions-legales/) centré en bas de carte, séparé des attributions.

## Méthode

1. **Demande** : voir [specs/spec.md](specs/spec.md) (demande initiale et critères d'acceptation).
2. **Plan** : voir [specs/plan.md](specs/plan.md) (choix des données avec le MCP geocontext, traitement, symbologie, rendu).
3. **Tâches** : voir [specs/tasks.md](specs/tasks.md).
4. **Implémentation** :
   - [scripts/fetch_data.py](scripts/fetch_data.py) télécharge les communes et calcule la densité (`data/communes-doubs-brut.geojson`) ;
   - [scripts/simplify.sh](scripts/simplify.sh) simplifie les contours avec [mapshaper](https://mborne.github.io/outils/mapshaper/) et produit [data/communes-doubs.geojson](data/communes-doubs.geojson) ;
   - [index.html](index.html) affiche la carte.

## Prompt équivalent

La demande initiale a été enrichie au fil des itérations (mentions légales, chargement, simplification, fond gris). Pour commander directement une carte équivalente à un assistant en ligne disposant du connecteur [MCP geocontext](https://github.com/ignfab/geocontext) :

```text
À l'aide du MCP geocontext, génère une carte web des communes du département du Doubs (25)
avec une symbologie présentant la densité de population.

Données :
- Utilise le type WFS BDTOPO_V3:commune de la Géoplateforme (https://data.geopf.fr/wfs),
  filtré sur code_insee_du_departement = '25' (563 communes attendues).
- Conserve code_insee, nom_officiel, population, superficie_cadastrale (en ha) et date_du_recensement.
- Calcule densite = population / (superficie_cadastrale / 100), en hab/km², arrondie à 0,1.
- Simplifie les contours avec mapshaper pour l'affichage web
  (-clean -simplify 10% keep-shapes, coordonnées à 5 décimales), sans trou ni chevauchement
  entre communes voisines.

Rendu :
- Un site statique (index.html + GeoJSON) publiable sur GitHub Pages, avec MapLibre GL JS v5.
- Fond Plan IGN vecteur en niveaux de gris :
  https://data.geopf.fr/annexes/ressources/vectorTiles/styles/PLAN.IGN/gris.json
- Choroplèthe en 7 classes (< 25, 25–50, 50–100, 100–250, 250–500, 500–1000, ≥ 1000 hab/km²),
  rampe YlOrRd, opacité 0,75, contours blancs fins, sous les libellés du fond.
- Une légende avec les classes et leur unité.
- Au clic sur une commune : nom, code INSEE, population, superficie, densité et année de recensement.
- Un message « Chargement des communes… » pendant le chargement des données, et un message
  en cas d'échec.
- Attribution des sources (© IGN – BD TOPO® / Insee, population municipale) et, centré en bas
  de carte et séparé des attributions, un lien vers les mentions légales :
  https://mborne.github.io/mentions-legales/
- La carte doit être utilisable sur mobile.
```

## Régénérer les données

```bash
python3 scripts/fetch_data.py
bash scripts/simplify.sh
```

`fetch_data.py` n'utilise que la bibliothèque standard Python ; `simplify.sh` requiert Node.js (mapshaper via `npx`).

## Tester en local

```bash
python3 -m http.server 8000
# puis ouvrir http://localhost:8000/
```
