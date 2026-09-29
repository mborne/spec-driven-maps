# vignobles

> 🚧 **En construction** : cette carte est une première version (V0), susceptible d'évoluer.

Carte web de la **vigne en France métropolitaine**, du pays à la parcelle, pour répondre à la question « Où sont les vignobles ? » posée lors d'un atelier « Les cartes qu'il nous faut » de [La République des Cartes](https://www.republiquedescartes.fr/).

## La carte

- **Petites et moyennes échelles** : densité de vignoble par commune, c'est-à-dire la part de la superficie communale plantée en vigne. Elle couvre 5 603 communes ayant au moins 1 ha de vigne ; le fichier pèse 2,7 Mo, soit environ 620 Ko compressés.
- **Grandes échelles** (à partir du zoom 12) : les surfaces de vigne de la BD TOPO, issues des tuiles du Plan IGN recolorées.
- **Bassins viticoles AOP** en repère ; accès rapide à la Champagne, l'Alsace, la Bourgogne, le Bordelais, le Languedoc et Saint-Dié-des-Vosges (vignoble presque disparu).
- Sources : © IGN – BD TOPO® (`BDTOPO_V3:zone_de_vegetation`, `nature = 'Vigne'` : 379 335 zones, 757 317 ha), ADMIN EXPRESS COG CARTO (`ADMINEXPRESS-COG-CARTO.LATEST:commune`), Plan IGN ; bassins AOP (data.gouv.fr, CC-BY). Extraction du 2026-09-29.
- « [GitHub](https://github.com/mborne/spec-driven-maps/tree/main/vignobles#readme) / [Mentions légales](https://mborne.github.io/mentions-legales/) » centré en bas de carte, séparé des attributions.

Limites :

- La vigne de la BD TOPO est en partie détectée par IA (« Processus IA non métrique ») : des confusions avec les vergers sont possibles. Un contrôle avec le RPG est prévu hors V0.
- Les bassins AOP sont un regroupement indicatif ; une aire d'appellation est une zone *autorisée*, pas une surface plantée.

## Méthode

1. **Demande** : voir [specs/spec.md](specs/spec.md) (objectif, contenu, critères d'acceptation).
2. **Plan** : voir [specs/plan.md](specs/plan.md) (choix des données avec le MCP geocontext, traitements, symbologie, rendu).
3. **Tâches** : voir [specs/tasks.md](specs/tasks.md).
4. **Implémentation** :
   - [scripts/fetch_vignes.py](scripts/fetch_vignes.py) : extraction des vignes par dalles (quadtree en Lambert-93), réduction à leur surface et à leur centroïde, contrôle de complétude ([data/fetch_vignes.log.json](data/fetch_vignes.log.json)) ;
   - [scripts/fetch_communes.py](scripts/fetch_communes.py) : communes ADMIN EXPRESS COG CARTO, département par département ;
   - [scripts/build_communes.sh](scripts/build_communes.sh) : jointure spatiale SpatiaLite (99,99 % des vignes rattachées), agrégats [data/vignes-communes.csv](data/vignes-communes.csv), simplification mapshaper et [data/communes-vigne.geojson](data/communes-vigne.geojson) ;
   - [scripts/fetch_bassins.sh](scripts/fetch_bassins.sh) : bassins AOP simplifiés et points d'étiquette ;
   - [index.html](index.html) affiche la carte.

## Régénérer les données

```bash
python3 scripts/fetch_vignes.py      # ~20 min ; cache par dalle dans data/cache-vignes/
python3 scripts/fetch_communes.py    # ~10 min
bash scripts/build_communes.sh       # ~1 min ; GDAL avec SpatiaLite, Node.js (mapshaper)
bash scripts/fetch_bassins.sh
```

## Tester en local

```bash
python3 -m http.server 8000
# puis ouvrir http://localhost:8000/
```
