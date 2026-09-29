# Spécification – Carte d'accès au Printemps des Cartes 2026

## Demande initiale

> Nous allons créer la "Carte d'accès au Printemps des Cartes 2026" avec une approche specs as code (ancienne version ici : https://mborne.github.io/montmorillon/printemps-des-cartes-montmorillon/index.html). Voici l'adresse :
>
> Festival Printemps des Cartes
> 16 rue des Récollets
> 86500 Montmorillon, France
>
> Tu procéderas au géocodage, à la recherche des informations utiles (gare et parking à proximité). Tu prévoieras une fiche avec un bouton pour ouvrir la carte sur un smartphone afin de pouvoir lancer un calcul d'itinéraire.

## Objectif

Permettre à un visiteur du festival [Printemps des Cartes](https://www.printempsdescartes.fr/) (7e édition, du 28 au 31 mai 2026) de **trouver le lieu, se garer ou venir en train**, puis de **lancer le guidage** depuis son smartphone.

## Public

Visiteurs du festival (grand public, scolaires, professionnels de la géographie), consultant la carte :

- sur **smartphone**, en mobilité (usage principal) ;
- sur ordinateur, avant de partir.

## Contenu

- **Lieu du festival** : Festival Printemps des Cartes, 16 rue des Récollets, 86500 Montmorillon, positionné par géocodage.
- **Gare** de Montmorillon (130 avenue du Général de Gaulle), avec la distance et le temps de trajet **à pied** jusqu'au lieu.
- **Parkings** dans un rayon de 1,5 km autour du lieu, avec leur distance à pied.
- **Itinéraire piéton** gare → lieu tracé sur la carte.
- Une **fiche** du lieu (nom, adresse, dates) avec un bouton **« Itinéraire »** qui ouvre l'application de navigation du smartphone avec le lieu en destination.
- Un fond de carte de référence (Plan IGN).

## Critères d'acceptation

- [x] Le lieu du festival est placé à l'adresse géocodée (16 rue des Récollets, Montmorillon) avec un marqueur distinct.
- [x] La gare de Montmorillon est affichée, avec la distance et la durée à pied jusqu'au lieu, calculées sur le réseau et non à vol d'oiseau.
- [x] Les parkings BD TOPO situés à moins de 1,5 km du lieu sont affichés, avec leur distance à pied.
- [x] L'itinéraire piéton gare → lieu est tracé sur la carte.
- [x] Une fiche présente le nom du festival, l'adresse et les dates (28 – 31 mai 2026).
- [ ] Le bouton « Itinéraire » de la fiche ouvre l'application de navigation du smartphone (Android et iOS) avec le lieu en destination ; sur ordinateur, il ouvre un calculateur d'itinéraire web.
- [x] Chaque gare ou parking propose aussi un bouton « Itinéraire ».
- [x] Une seule popup est ouverte à la fois : ouvrir le détail d'un parking, de la gare ou du lieu (sur la carte ou depuis la fiche) ferme la popup précédente.
- [x] Une légende distingue le lieu, la gare, les parkings et l'itinéraire piéton.
- [x] La vue initiale montre à la fois le lieu, les parkings et la gare.
- [x] La présentation est sobre : carte plein écran et fiche claire, dans la lignée de `commune-doubs`.
- [x] La carte est utilisable sur smartphone : fiche lisible, boutons assez grands pour le doigt, carte non masquée par la fiche.
- [x] Les sources sont attribuées (IGN, BD TOPO®, Géoplateforme).
- [x] Un lien vers les [mentions légales](https://mborne.github.io/mentions-legales/) est centré en bas de carte, séparé des attributions des sources ; sur mobile, il reste visible au-dessus de la fiche.
- [x] Un lien « GitHub » vers le [README de la carte](https://github.com/mborne/spec-driven-maps/tree/main/montmorillon-acces#readme) dans le dépôt figure à côté des mentions légales (« GitHub / Mentions légales »).
- [x] La carte est un site statique publiable sur GitHub Pages (aucun serveur applicatif).

## Hors périmètre

- Programme détaillé du festival et plan des différentes salles.
- Horaires de train, lignes de bus.
- Gratuité, tarifs et capacité des parkings.
- Tracé des itinéraires piétons depuis les parkings.
- QR code et choix explicite de l'application de navigation.
- Calcul d'itinéraire intégré à la page : le calcul est confié à l'application de navigation du smartphone.
