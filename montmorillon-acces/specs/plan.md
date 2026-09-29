# Plan technique – montmorillon-acces

## Données

### Lieu du festival (géocodage)

| Élément | Valeur |
|---|---|
| Requête | `16 rue des Récollets 86500 Montmorillon` |
| Outil | MCP geocontext `geocode` (service d'autocomplétion de la Géoplateforme) |
| Résultat | `16 Rue des Recollets, 86500 Montmorillon`, type `housenumber` |
| Coordonnées | lon `0.869201`, lat `46.424964` |

L'ancienne version utilisait `0.869043, 46.425111`, soit environ 20 m d'écart. On retient le géocodage au numéro.

### Gare et parkings (BD TOPO)

Démarche avec le MCP geocontext :

1. `gpf_wfs_search_types` (« gare ferroviaire », « parking stationnement ») → `BDTOPO_V3:equipement_de_transport`, qui porte les gares et les parkings (`nature`).
2. `gpf_wfs_describe_type` → propriétés `nature`, `nature_detaillee`, `toponyme`, `adresse_postale`, `geometrie` (multipolygone).
3. `gpf_wfs_get_features` avec `dwithin_point` (1 500 m autour du lieu) et `nature IN ('Parking', 'Gare voyageurs et fret', …)` → 1 gare et 10 parkings.
4. `result_type=request` → URL WFS reprise dans `scripts/fetch_data.py`.

Résultats de l'exploration (distance à vol d'oiseau depuis le centroïde ; les distances à pied calculées par le script figurent dans `data/acces.geojson`) :

| Objet BD TOPO | Nature | Nom / adresse la plus proche | Surface | Distance |
|---|---|---|---|---|
| `equipement_de_transport.32859` | Parking | Rue du Four | 655 m² | 74 m |
| `equipement_de_transport.32852` | Parking | Place du Maréchal Leclerc | 925 m² | 124 m |
| `equipement_de_transport.175897` | Parking | Boulevard de Strasbourg (bord de Gartempe) | 596 m² | 161 m |
| `equipement_de_transport.32881` | Parking | « Cité de l'Écrit », rue Léon Dardant | 1 458 m² | 204 m |
| `equipement_de_transport.32870` | Parking | « Cité de l'Écrit », rue Fontaine de l'École | 1 208 m² | 225 m |
| `equipement_de_transport.32882` | Parking | Rue Saint-Martial | 2 154 m² | 230 m |
| `equipement_de_transport.55352` | Parking | Rue Puits Cornet | 260 m² | 252 m |
| `equipement_de_transport.55351` | Parking | Boulevard Gambetta | 1 269 m² | 341 m |
| `equipement_de_transport.32812` | Parking | Rue des Volliboeufs | 724 m² | 987 m |
| `equipement_de_transport.32860` | Parking | Boulevard du Terrier Blanc | 4 500 m² | 1 154 m |
| `equipement_de_transport.11809` | Gare voyageurs et fret | Gare de Montmorillon, 130 av. du Général de Gaulle | – | 896 m |

- Les parkings BD TOPO n'ont généralement pas de `toponyme` : on les nomme par la voie la plus proche, obtenue par géocodage inverse (`https://data.geopf.fr/geocodage/reverse`, index `address`).
- On retient **tous les parkings à moins de 1,5 km** du lieu, soit 10 parkings : 8 dans le centre (< 350 m) et 2 plus grands au nord-est (~1 km), utiles quand le centre est saturé.
- La BD TOPO ne renseigne ni la gratuité ni la capacité. L'ancienne version indiquait « gratuit » sans source : on n'affiche **pas** ces informations (pas de vérification OpenStreetMap pour l'instant).

### Distances et itinéraire piéton (service d'itinéraire Géoplateforme)

`https://data.geopf.fr/navigation/itineraire?resource=bdtopo-osrm&profile=pedestrian&optimization=fastest&start=…&end=…&geometryFormat=geojson`

- Gare → lieu : **1 202 m, ~22 min à pied** (1 315 s). L'ancienne version affichait « ~900 m », la distance à vol d'oiseau.
- Les parkings « Cité de l'Écrit », à ~200 m à vol d'oiseau, sont à 450 – 570 m à pied.
- Le même service donne la distance et la durée à pied de chaque parking retenu (point de départ : centroïde du parking). Seule la géométrie de l'itinéraire gare → lieu est conservée et tracée : les itinéraires depuis les parkings ne sont pas dessinés, y compris pour les 2 parkings éloignés.

## Traitement (`scripts/fetch_data.py`)

Bibliothèque standard Python uniquement, comme pour `commune-doubs` :

1. Géocoder l'adresse du lieu.
2. Télécharger gare et parkings (WFS), les filtrer, calculer leurs centroïdes.
3. Nommer les parkings par géocodage inverse.
4. Calculer l'itinéraire piéton de chaque parking et de la gare vers le lieu (distance, durée, géométrie).
5. Écrire `data/acces.geojson` : points (`categorie` = `lieu` | `gare` | `parking`, `nom`, `adresse`, `distance_m`, `duree_min`), polygones des parkings et ligne de l'itinéraire gare → lieu.

Les données sont figées dans le dépôt : la carte ne dépend pas des services au moment de la consultation, en dehors du fond de carte.

## Symbologie

| Élément | Représentation |
|---|---|
| Lieu du festival | Marqueur rouge, plus grand, libellé « Printemps des Cartes » |
| Gare | Pictogramme train, bleu |
| Parkings | Pictogramme « P » bleu + emprise du parking en aplat léger |
| Itinéraire piéton gare → lieu | Ligne pointillée, avec distance et durée |

## Rendu

- MapLibre GL JS v5 (CDN jsdelivr), un seul `index.html`, dans la continuité de `commune-doubs`.
- Fond : Plan IGN vecteur, style standard en couleur (`https://data.geopf.fr/annexes/ressources/vectorTiles/styles/PLAN.IGN/standard.json`). Pour une carte d'accès, le fond sert à se repérer (rues, bâtiments), d'où la couleur plutôt que les niveaux de gris.
- Vue initiale : emprise englobant le lieu, les parkings retenus et la gare.
- **Présentation sobre** : carte plein écran, fiche claire, pas d'habillage décoratif (choix validé).
- **Fiche** : panneau en bas de l'écran sur mobile (repliable), latéral sur ordinateur. Contenu : « Printemps des Cartes 2026 », adresse, dates (28 – 31 mai 2026), bouton « Itinéraire », liste de la gare et des parkings (clic → centrage sur la carte).
- **Bouton « Itinéraire »** (fiche et popups) :
  - iOS : `https://maps.apple.com/?daddr=<lat>,<lon>` (Plans) ;
  - Android : `geo:<lat>,<lon>?q=<lat>,<lon>(<libellé>)`, qui laisse choisir l'application (Google Maps, OsmAnd, Organic Maps…) ;
  - ordinateur ou repli : `https://www.google.com/maps/dir/?api=1&destination=<lat>,<lon>`.
- **Popups** : une seule popup à la fois. La page garde une référence à la popup ouverte et la ferme avant d'en ouvrir une autre, que l'ouverture vienne d'un marqueur ou de la liste de la fiche.
- Attribution : © IGN – BD TOPO®, Plan IGN, Géoplateforme (géocodage et itinéraire), dans le contrôle d'attribution MapLibre.
- Pied de carte « GitHub / Mentions légales » : liens vers le README de la carte dans le dépôt (`https://github.com/mborne/spec-driven-maps/tree/main/montmorillon-acces#readme`) et vers les mentions légales, dans un bloc distinct, centré en bas de carte (convention commune, voir le [README](../../README.md)). Sur mobile, le bloc est placé juste au-dessus de la fiche ; si l'attribution déployée le chevauche, il est remonté au-dessus d'elle.

## Hébergement

GitHub Pages depuis la racine du dépôt, servie sous `/<depot>/montmorillon-acces/`. Chemins relatifs.

## Décisions

| Question | Décision |
|---|---|
| Ton de la page | Sobre, dans la lignée de `commune-doubs` |
| Parkings | Tous les parkings BD TOPO à moins de 1,5 km (10) |
| Ouverture sur smartphone | Bouton « Itinéraire » seul (pas de QR code) |
| Dates | Affichées : 28 – 31 mai 2026 |
| Gratuité / capacité des parkings | Non affichées (source BD TOPO muette, vérification OSM écartée pour l'instant) |
| Itinéraires tracés | Gare → lieu uniquement ; distances à pied seules pour les parkings |
