# Spécification – Densité de population des communes du Doubs

## Demande initiale

> A l'aide du MCP geocontext, génère moi une carte web des communes du département du Doubs avec une symbologie présentant la densité de population.

## Objectif

Visualiser le contraste de peuplement entre les communes du Doubs (25), des communes rurales du Haut-Doubs aux pôles urbains de Besançon, Montbéliard et Pontarlier.

## Public

Grand public et agents souhaitant une lecture rapide du peuplement du département.

## Contenu

- Toutes les communes du Doubs (découpage en vigueur dans la BD TOPO).
- Densité de population en habitants par km² (population municipale Insee / superficie).
- Un fond de carte de référence en niveaux de gris pour se repérer sans concurrencer la symbologie.

## Critères d'acceptation

- [x] Les 563 communes du Doubs sont affichées.
- [x] La couleur de chaque commune dépend de sa densité (classes lisibles, rampe séquentielle).
- [x] Une légende présente les classes de densité et leur unité.
- [x] Un message informe du chargement en cours des données communales, puis disparaît une fois les communes affichées (ou signale un échec).
- [x] Un clic sur une commune affiche son nom, son code INSEE, sa population, sa superficie et sa densité.
- [x] Les sources sont attribuées (IGN BD TOPO®, Insee).
- [x] Un lien vers les [mentions légales](https://mborne.github.io/mentions-legales/) couvrant `mborne.github.io` est centré en bas de carte, séparé des attributions des sources.
- [x] La carte est utilisable sur mobile.
- [x] Les contours des communes sont simplifiés pour un affichage web rapide, sans trou ni chevauchement entre communes voisines.
- [x] La carte est un site statique publiable sur GitHub Pages (aucun serveur applicatif).
