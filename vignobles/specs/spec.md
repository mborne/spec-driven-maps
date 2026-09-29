# Spécification – Où sont les vignobles ?

## Demande initiale

Carte proposée lors d'un atelier participatif « Les cartes qu'il nous faut » (Jour de la Carte 2026).

> Où sont les vignobles ? C'est notre histoire. Noé est passé par là.

Aucune représentation n'a été proposée par les participants.

## Objectif

Montrer **où est la vigne en France aujourd'hui**, de la vue d'ensemble nationale jusqu'à la parcelle, et situer les grands bassins viticoles. La carte doit aussi faire sentir que la vigne a une histoire : des vignobles ont presque disparu, comme autour de Saint-Dié-des-Vosges.

## Public

Grand public.

## Contenu

- **Vue nationale et régionale** (petites et moyennes échelles) : **densité de vignoble par commune**, c'est-à-dire la part de la superficie communale plantée en vigne. Elle est calculée à partir des zones de végétation de nature « Vigne » de la BD TOPO, rattachées aux communes d'ADMIN EXPRESS COG CARTO (France métropolitaine).
- **Vue détaillée** (grandes échelles) : les surfaces de vigne elles-mêmes (BD TOPO, via les tuiles vectorielles du Plan IGN).
- **Bassins viticoles** : contours et noms des grandes régions productrices de vins AOP, en repère.
- **Accès rapide** à quelques vignobles (Champagne, Alsace, Bourgogne, Bordelais, Languedoc) et à Saint-Dié-des-Vosges.
- Un fond Plan IGN en niveaux de gris.

Hors périmètre de la V0 : les vignobles historiques (carte d'État-major), le contrôle par le RPG, les délimitations parcellaires des AOC et l'outre-mer (voir `tasks.md`, « Au-delà de la V0 »).

## Critères d'acceptation

- [x] À l'ouverture, la France métropolitaine est visible avec la densité de vignoble par commune, en classes lisibles sur une rampe séquentielle lie-de-vin.
- [x] Le chargement initial reste fluide : la couche communale ne contient que les communes ayant de la vigne, simplifiées (quelques Mo au plus).
- [x] En zoomant, la couche communale s'efface au profit des surfaces de vigne de la BD TOPO, sans rupture visuelle brutale.
- [x] Les contours et les noms des bassins viticoles AOP sont affichés aux petites échelles.
- [x] Une légende présente les classes de densité (unité : % de la superficie communale), le symbole des vignes et celui des bassins, et indique à quel niveau de zoom chaque élément est visible.
- [x] Des boutons centrent la carte sur la France, sur les vignobles cités et sur Saint-Dié-des-Vosges.
- [x] Un clic sur une commune affiche son nom, son code INSEE, sa surface de vigne (ha) et la part de sa superficie en vigne (%). Un clic sur un bassin affiche son nom.
- [x] Un message signale le chargement des données, puis disparaît (ou signale un échec).
- [x] Les sources sont attribuées : © IGN – BD TOPO®, ADMIN EXPRESS COG CARTO, Plan IGN ; bassins AOP (data.gouv.fr, CC-BY, d'après l'INAO), avec leur caractère indicatif.
- [x] La légende ou une note rappelle qu'une aire d'appellation n'est pas une surface plantée, et que les vignes de la BD TOPO sont en partie détectées par IA.
- [x] Un lien « GitHub / Mentions légales » ([mentions légales](https://mborne.github.io/mentions-legales/)) figure en bas de carte, séparé des attributions.
- [x] La carte est utilisable sur mobile.
- [x] La carte est un site statique (aucun serveur applicatif), dont les données tiennent en quelques Mo.
- [x] Les données sont reproductibles par des scripts documentés (`scripts/`), avec un contrôle de complétude.
