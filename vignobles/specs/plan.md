# Plan technique – vignobles

## Données

| Élément | Choix |
|---|---|
| Vignes (source) | WFS Géoplateforme `https://data.geopf.fr/wfs`, type `BDTOPO_V3:zone_de_vegetation`, filtre `nature = 'Vigne'` |
| Vignes (affichage détaillé) | Tuiles vectorielles Plan IGN, couche `ocs_vegetation_surf`, `symbo = 'ZONE_VIGNE'` (dérivée de la BD TOPO) |
| Communes | WFS Géoplateforme, type `ADMINEXPRESS-COG-CARTO.LATEST:commune` (34 877 communes ; `code_insee`, `nom_officiel`, `superficie_cadastrale` en ha) |
| Bassins viticoles | « Cartes des grandes régions productrices de vins AOP en France », data.gouv.fr `6126659ca058ff97a694a473`, CC-BY (regroupement par comité régional de l'INAO, 12 bassins, 2021) |
| Fond | Plan IGN vecteur, style `gris` |

Démarche d'identification avec le MCP geocontext :

1. `gpf_wfs_search_types` (« zone de végétation vigne ») → `BDTOPO_V3:zone_de_vegetation`.
2. `gpf_wfs_describe_type` → l'énumération `nature` contient « Vigne ».
3. `gpf_wfs_get_features` (`hits`) → 348 polygones à Épernay, 385 à Turckheim, 2 autour de Saint-Dié.
4. Comptage national direct (WFS, `resultType=hits`) : **379 353** polygones de vigne.
5. Communes : le type `ADMINEXPRESS-COG-CARTO.LATEST:commune` n'est **pas trouvé par `gpf_wfs_search_types` ni `gpf_wfs_describe_type`** (le catalogue du MCP ne propose que `ADMINEXPRESS-COG.*`). Il est pourtant publié par le WFS : on l'a vérifié par `GetCapabilities` et `DescribeFeatureType`. Épernay compte 347 sommets en COG CARTO, contre 56 en COG CARTO PE (petite échelle).

Constats qui orientent le plan :

- Les tuiles du Plan IGN ne contiennent les vignes qu'à partir du **zoom 12** environ (vérifié : 0 au zoom 10, 3 au zoom 12, 281 au zoom 13 sur une tuile d'Épernay). Il faut donc une donnée agrégée pour les petites échelles.
- Une source GeoJSON est chargée en entier dès l'ouverture, quel que soit le zoom. Une grille nationale fine (1 km) serait trop lourde pour un chargement fluide. On retient donc la **commune** comme maille, en ne gardant que les communes plantées, simplifiées.
- La pagination profonde triée du WFS (`startIndex` = 375 000, `sortBy`) dépasse 60 s. En revanche, une requête filtrée par bbox en Lambert-93 répond en 1 à 2 s.
- Pas de bibliothèque géométrique Python (shapely, pyproj) dans l'environnement. En revanche, GDAL 3.8 avec **SpatiaLite 5.1** (`ogr2ogr`) et Node.js (mapshaper via `npx`) sont disponibles.

## Traitement

### `scripts/fetch_vignes.py` – surfaces et centroïdes des vignes

- **Découpage spatial (quadtree)** de l'emprise métropolitaine en Lambert-93 (`x` 99 000–1 250 000, `y` 6 040 000–7 120 000), en dalles de 100 km au départ.
  - Pour chaque dalle, un comptage `resultType=hits` avec `nature = 'Vigne' AND BBOX(geometrie, …, 'EPSG:2154')` ;
  - on ignore les dalles vides et on subdivise en 4 les dalles de plus de 4 000 objets ;
  - sinon, on télécharge `cleabs` + `geometrie` en `EPSG:2154` (`count=5000`, une seule page).
- **Dédoublonnage** par `cleabs` : un polygone à cheval sur deux dalles est renvoyé deux fois.
- **Réduction au fil de l'eau**, sans conserver les géométries : chaque polygone donne sa surface planaire (formule du lacet, anneaux intérieurs soustraits, en m²) et son centroïde (Lambert-93).
- **Contrôle de complétude** : le nombre de polygones distincts est comparé au comptage national (379 353). L'écart doit s'expliquer par l'outre-mer, hors emprise.
- Sortie : `data/vignes-centroides.csv` (`cleabs`, `x`, `y`, `surface_m2`), intermédiaire non versionné (une vingtaine de Mo).
- Journal : `data/fetch_vignes.log.json` (dalles, comptages, date d'extraction), versionné.

### `scripts/fetch_communes.py` – communes ADMIN EXPRESS COG CARTO

- Téléchargement département par département (96 requêtes, filtre `code_insee_du_departement`), en `EPSG:2154`, avec `code_insee`, `nom_officiel`, `code_insee_du_departement`, `superficie_cadastrale` et `geometrie`.
- Contrôle : pour chaque département, le nombre d'objets reçus est égal à `numberMatched`.
- Sortie : `data/communes-cog-carto.geojson`, intermédiaire non versionné.

### `scripts/build_communes.sh` – densité de vignoble par commune

1. **Base SpatiaLite** temporaire (`ogr2ogr -f SQLite -dsco SPATIALITE=YES`) avec les communes (polygones) et les centroïdes (points), en Lambert-93, avec index spatial.
2. **Jointure point dans polygone** (`ST_Within`, filtrée par l'index `SpatialIndex`) et agrégation par commune (surface en m², nombre de zones). Sortie : `data/vignes-communes.csv`, versionnée. Contrôle affiché : vignes rattachées / vignes totales.
3. **Couche d'affichage** avec mapshaper :
   - reprojection en WGS84 ;
   - `-clean -simplify 5% keep-shapes` appliqué à **toutes** les communes, pour que les limites restent jointives ;
   - jointure des agrégats et calcul de `part = surface / superficie_cadastrale` (%, arrondie à 0,1) et `surface_ha` ;
   - filtrage des communes ayant **au moins 1 ha** de vigne : 5 603 communes sur 7 990 plantées. On écarte ainsi 871 ha (0,1 %) de très petites surfaces, surtout du bruit (jardins, détections douteuses) ;
   - coordonnées à 4 décimales (~10 m).
   - Sortie : `data/communes-vigne.geojson`.

La **superficie cadastrale** (ha, attribut de la commune) sert de dénominateur, par cohérence avec les statistiques communales. Le centroïde de chaque polygone de vigne le rattache à une seule commune : l'erreur est négligeable, car les parcelles de vigne sont petites devant les communes.

### `scripts/fetch_bassins.sh` – bassins AOP

- Télécharge le GeoJSON des bassins (1,4 Mo, CRS84).
- Simplifie avec mapshaper (`-clean -simplify 15% keep-shapes`, précision 0,0001°).
- Sorties : `data/bassins-aop.geojson` et `data/bassins-aop-labels.geojson` (un point d'étiquette par bassin).

## Symbologie

| Élément | Zoom | Rendu |
|---|---|---|
| Communes (densité de vignoble) | < 13,5 | Choroplèthe, opacité 0,85, fondu entre z 11,5 et 13,5 ; limites blanches de 0,5 px à partir de z 8 |
| Vignes BD TOPO (tuiles) | ≥ 12 | Couche `ocs - vegetation - vigne` du style gris recolorée en `#7b1e3c` (opacité 0,85), remontée sous les libellés. Les tuiles du zoom 12 sont incomplètes, d'où le chevauchement avec la couche communale jusqu'au zoom 13,5 |
| Bassins AOP | < 11 | Contour `#5c1a33` en tirets, 1,2 px, fondu entre z 9 et 11 ; nom (z < 9) sur un point intérieur calculé par mapshaper (`-points inner`, `data/bassins-aop-labels.geojson`) |

Classes de la densité de vignoble (en % de la superficie communale, rampe séquentielle lie-de-vin) :

| Classe | Couleur |
|---|---|
| < 1 % | `#f6e3e8` |
| 1 – 5 % | `#e8b4c3` |
| 5 – 10 % | `#d4809b` |
| 10 – 25 % | `#b44d72` |
| 25 – 50 % | `#8c2451` |
| ≥ 50 % | `#5a0f33` |

Seuils confirmés par la distribution observée (5 603 communes, médiane 0,8 %, 90ᵉ centile 24,9 %, maximum 82,6 % à Aloxe-Corton) : 1 756, 1 281, 710, 1 059, 681 et 116 communes par classe.

## Rendu

- MapLibre GL JS v5 (CDN jsdelivr), un seul fichier `index.html`.
- Fond : Plan IGN vecteur gris, `https://data.geopf.fr/annexes/ressources/vectorTiles/styles/PLAN.IGN/gris.json`. Les couches thématiques sont insérées sous le premier calque `toponyme` pour garder les libellés lisibles.
- Vue initiale : France métropolitaine `[-5.3, 41.3, 9.7, 51.2]`.
- Boutons d'accès rapide : France, Champagne (Épernay), Alsace (Colmar), Bourgogne (Beaune), Bordelais, Languedoc, Saint-Dié-des-Vosges. Ils cadrent le vignoble à l'échelle régionale (zooms 8,5 à 10), où la densité par commune est lisible ; c'est l'utilisateur qui zoome ensuite jusqu'aux parcelles.
- Chargement : message « Chargement des vignobles… » (`role="status"`), masqué quand les sources GeoJSON sont chargées, remplacé par un message d'échec sur `error`.
- Légende repliable sur mobile.
- Popups : commune (nom, code INSEE, surface de vigne en ha, part en %), vigne (source), bassin (nom).
- Pied de carte « GitHub / Mentions légales », centré et séparé des attributions (convention de spec-driven-maps).

## Hébergement

Site statique ; tous les chemins sont relatifs. Test local : `python3 -m http.server 8000`.

## Points d'attention

- Les vignes de la BD TOPO sont en partie détectées par IA (« Processus IA non métrique »). Le contrôle par le RPG est prévu hors V0.
- Les bassins AOP sont un **regroupement indicatif** produit par un contributeur de data.gouv.fr à partir des données de l'INAO. Ce ne sont pas les délimitations officielles. Le Bordelais y est inclus dans « Sud-Ouest ».
- Une aire d'appellation est une zone *autorisée*, pas une surface plantée : la légende doit le dire.
- Rattacher les vignes par leur centroïde attribue un polygone à cheval sur deux communes à une seule d'entre elles. Les contours COG CARTO sont généralisés : quelques centroïdes proches des limites (ou de la côte) peuvent tomber dans la commune voisine, ou hors de toute commune. Le nombre de vignes non rattachées est contrôlé.
- La densité est rapportée à la superficie communale. Une petite commune très plantée ressort donc plus qu'une grande commune qui a la même surface de vigne.
