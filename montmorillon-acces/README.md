# montmorillon-acces

Carte d'**accès au festival Printemps des Cartes 2026** (28 – 31 mai 2026), 16 rue des Récollets à Montmorillon (86).

Nouvelle version, conçue selon la méthode [spec-driven-maps](../README.md), de l'[ancienne carte d'accès](https://mborne.github.io/montmorillon/printemps-des-cartes-montmorillon/index.html).

## La carte

- Le lieu du festival, placé par géocodage de l'adresse (au numéro).
- La gare de Montmorillon et l'itinéraire piéton gare → festival : **1,2 km, 22 min à pied**.
- Les 10 parkings de la BD TOPO à moins de 1,5 km, avec leur emprise et leur distance à pied (de 80 m à 1,4 km).
- Une fiche avec le nom du festival, les dates, l'adresse et un bouton **« Itinéraire vers le festival »** qui ouvre l'application de navigation du smartphone :
  - iPhone / iPad : Plans (`maps.apple.com`) ;
  - Android : lien `geo:`, qui laisse choisir l'application (Google Maps, OsmAnd, Organic Maps…) ;
  - ordinateur : Google Maps dans le navigateur.
- Un bouton « Itinéraire » pour la gare et chaque parking, dans la fiche et dans les popups.
- Sur mobile, la fiche est en bas de l'écran et repliée par défaut (titre, dates, adresse, bouton) ; sur ordinateur, elle est affichée à gauche.
- Fond Plan IGN vecteur (style standard), rendu MapLibre GL JS.
- Sources : © IGN – BD TOPO® (`BDTOPO_V3:equipement_de_transport`), Géoplateforme (géocodage, itinéraire).
- Une seule popup ouverte à la fois.
- Lien vers les [mentions légales](https://mborne.github.io/mentions-legales/) centré en bas de carte, séparé des attributions.

## Méthode

1. **Demande** : voir [specs/spec.md](specs/spec.md) (demande initiale et critères d'acceptation).
2. **Plan** : voir [specs/plan.md](specs/plan.md) (géocodage, choix des données avec le MCP geocontext, distances à pied, rendu, décisions).
3. **Tâches** : voir [specs/tasks.md](specs/tasks.md).
4. **Implémentation** :
   - [scripts/fetch_data.py](scripts/fetch_data.py) géocode le lieu, télécharge la gare et les parkings, les nomme par géocodage inverse, calcule les distances à pied et produit [data/acces.geojson](data/acces.geojson) ;
   - [index.html](index.html) affiche la carte.

## Prompt équivalent

Pour commander directement une carte équivalente à un assistant disposant du connecteur [MCP geocontext](https://github.com/ignfab/geocontext) :

```text
À l'aide du MCP geocontext, génère une carte web d'accès au festival Printemps des Cartes 2026
(du 28 au 31 mai 2026), 16 rue des Récollets, 86500 Montmorillon.

Données :
- Géocode l'adresse au numéro (géocodage de la Géoplateforme).
- Récupère la gare et les parkings dans un rayon de 1,5 km avec le type WFS
  BDTOPO_V3:equipement_de_transport (nature 'Parking', 'Gare voyageurs et fret',
  'Gare voyageurs uniquement').
- Nomme les parkings sans toponyme par la voie la plus proche (géocodage inverse).
- Calcule la distance et la durée à pied de la gare et de chaque parking jusqu'au lieu avec
  le service d'itinéraire de la Géoplateforme (resource bdtopo-osrm, profile pedestrian),
  et conserve le tracé gare → lieu.
- N'affiche ni gratuité ni capacité des parkings (non renseignées dans la BD TOPO).
- Fige les données dans un GeoJSON versionné.

Rendu :
- Un site statique (index.html + GeoJSON) publiable sur GitHub Pages, avec MapLibre GL JS v5
  et le fond Plan IGN vecteur standard :
  https://data.geopf.fr/annexes/ressources/vectorTiles/styles/PLAN.IGN/standard.json
- Présentation sobre : carte plein écran ; marqueur rouge pour le lieu, pictogrammes pour la gare
  et les parkings, emprise des parkings en aplat léger, itinéraire gare → lieu en pointillés
  avec sa distance et sa durée.
- Une fiche (nom, dates, adresse) avec un bouton « Itinéraire » qui ouvre l'application de
  navigation du smartphone (Apple Plans sur iOS, lien geo: sur Android, Google Maps sur ordinateur),
  la liste de la gare et des parkings avec leur distance à pied et leur propre bouton « Itinéraire »,
  et une légende.
- Sur mobile, fiche en bas de l'écran, repliable, sans masquer la carte ; boutons assez grands
  pour le doigt.
- Une seule popup ouverte à la fois (ouvrir un détail ferme le précédent).
- Attribution des sources (© IGN – BD TOPO®, Géoplateforme) et, centré en bas de carte et séparé
  des attributions, un lien vers les mentions légales : https://mborne.github.io/mentions-legales/
```

## Régénérer les données

```bash
python3 scripts/fetch_data.py
```

Le script n'utilise que la bibliothèque standard Python.

## Tester en local

```bash
python3 -m http.server 8000
# puis ouvrir http://localhost:8000/
```
