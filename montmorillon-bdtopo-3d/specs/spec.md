# Spécification – Bâtiments de Montmorillon en 3D

## Demande initiale

> Reprise, selon la démarche specs driven du dépôt, de la carte des bâtiments de Montmorillon en 3D :
> [mborne/montmorillon – montmorillon-bdtopo-3d/index.html](https://github.com/mborne/montmorillon/blob/main/montmorillon-bdtopo-3d/index.html).

Suivi : [issue #14](https://github.com/mborne/spec-driven-maps/issues/14) (inventaire de l'existant, points à revoir, décisions du 29/09/2026).

## Objectif

**Montrer ce que contient la BD TOPO® sur les bâtiments**, à partir de l'exemple de Montmorillon : volumes, hauteurs, usages, et d'où vient chaque hauteur. La carte sert de démonstration, par exemple lors de la présentation « République des cartes » du 01/10/2026.

La nouvelle version corrige les défauts de l'ancienne :

- la légende de hauteur ne correspondait pas aux couleurs ;
- les bâtiments sans hauteur étaient extrudés à 3 m sans le signaler ;
- la page ne pouvait pas être agrandie sur mobile ;
- le pied de carte ne suivait pas la convention commune.

## Public

Un public curieux de données géographiques : participants à une présentation, agents, étudiants. La carte est consultée surtout sur ordinateur ou sur un écran projeté, mais elle reste utilisable sur smartphone.

## Contenu

- Les **bâtiments de la BD TOPO** en 3D, sur la commune de Montmorillon, lus directement dans les tuiles vectorielles BD TOPO de la Géoplateforme. Ils sont colorés au choix :
  - **par usage** (`usage_1`, 8 valeurs) ;
  - **par hauteur**, en classes adaptées au bâti de Montmorillon.
- Une **fiche détaillée** au clic sur un bâtiment, qui montre les attributs de la BD TOPO :
  - usages et nature ;
  - hauteur et **origine de la hauteur** (mesurée, déduite du nombre d'étages, ou valeur par défaut) ;
  - nombre d'étages et de logements ;
  - altitudes du sol et du toit ;
  - méthode d'acquisition altimétrique ;
  - identifiants BD TOPO et RNB.
- Un fond **Plan IGN vecteur**, sans ses bâtiments plats (qui doubleraient la 3D), avec un choix **orthophoto**.
- Un interrupteur **Relief 3D** qui remet la carte à plat.

## Critères d'acceptation

- [x] Les bâtiments de Montmorillon sont extrudés en 3D d'après la BD TOPO (tuiles vectorielles de la Géoplateforme).
- [x] La hauteur utilisée est `hauteur` si elle est renseignée, sinon `nombre_d_etages` × 3 m, sinon 3 m. La fiche indique laquelle des trois a été retenue.
- [x] Deux colorations sont proposées : par usage (8 valeurs de `usage_1`) et par hauteur, en classes.
- [x] La légende correspond exactement à la coloration affichée (mêmes classes, mêmes couleurs, mêmes libellés).
- [x] Au clic sur un bâtiment, une fiche présente ses attributs BD TOPO (voir « Contenu ») ; une seule fiche est ouverte à la fois.
- [x] Le fond est le Plan IGN vecteur sans ses bâtiments plats, avec un choix orthophoto.
- [x] Un interrupteur « Relief 3D » masque les volumes et remet la carte à plat, puis les rétablit.
- [x] La vue initiale est inclinée sur le centre-ville et la vue courante est partageable par l'URL.
- [x] Les bâtiments apparaissent dès que les données sont disponibles, et un message invite à zoomer quand elles ne le sont pas encore.
- [x] Sur smartphone, le panneau de réglages est repliable, la carte reste manipulable et la page peut être agrandie (pas de `maximum-scale`).
- [x] Les sources sont attribuées (IGN – BD TOPO®, Plan IGN, orthophotographie).
- [x] « GitHub / Mentions légales » est centré en bas de carte, séparé des attributions (convention commune, voir le [README](../../README.md)).
- [x] La carte est un site statique publiable sur GitHub Pages (aucun serveur applicatif, aucune donnée figée dans le dépôt).

## Hors périmètre

- Relief du terrain (MNT), toits, textures.
- Mise en évidence du bâtiment du festival ou des monuments historiques (voir `montmorillon-acces` et `montmorillon-tourisme`).
- Extraction des bâtiments dans un fichier versionné.
- Statistiques sur le bâti.

## Décisions

| Question | Décision |
|---|---|
| Objectif et public (issue #14) | Démonstration de la BD TOPO : panneau d'exploration, fiche détaillée |
| Fond de carte (issue #14) | Plan IGN vecteur (sans bâtiments plats) + choix orthophoto |
| Coloration (issue #14) | Usage et hauteur, légende de hauteur corrigée |
| Données (issue #14) | Tuiles vectorielles BD TOPO en direct |
| Sujets en plus (issue #14) | Aucun |
| Habillage | Celui de l'ancienne version (panneau translucide, polices Fraunces et Public Sans), mis en conformité avec les conventions communes |
