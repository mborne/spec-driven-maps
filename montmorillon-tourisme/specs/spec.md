# Spécification – Carte touristique de Montmorillon

## Demande initiale

> Reprise, selon la démarche specs driven du dépôt, de la carte touristique de Montmorillon :
> [mborne/montmorillon – montmorillon_carte_touristique/index.html](https://github.com/mborne/montmorillon/blob/main/montmorillon_carte_touristique/index.html).

Suivi : [issue #15](https://github.com/mborne/spec-driven-maps/issues/15) (inventaire de l'existant, points à revoir, décisions du 29/09/2026).

## Objectif

Faire découvrir le **patrimoine de Montmorillon** (Vienne), « Cité de l'Écrit » et Ville d'art et d'histoire, avec des données **ouvertes et traçables** : chaque lieu affiché renvoie à sa source (BD TOPO, Mérimée ou adresse géocodée).

La nouvelle version corrige les approximations de l'ancienne carte : rivière tracée à la main, Cité de l'Écrit figurée par un cercle, coordonnées estimées, statut de monument historique saisi à la main et parfois faux (le Vieux Pont, par exemple, ne figure pas dans Mérimée).

## Public

- **Visiteurs sur place**, sur smartphone : repérer les lieux autour de soi, lire une fiche courte.
- **Visiteurs qui préparent leur venue**, sur ordinateur : parcourir la liste des lieux par catégorie et lire les fiches détaillées.

## Contenu

Six catégories de lieux, dans le **centre-ville de Montmorillon** (commune 86165 ; emprise précisée dans `plan.md`) :

| Catégorie | Exemples attendus |
|---|---|
| Musées | Musée d'Art et d'Histoire, Musée de l'Amande et du Macaron |
| Patrimoine religieux | Église Notre-Dame, Église Saint-Martial, Octogone, Chapelle Saint-Laurent |
| Monuments civils | Ancien Hôtel-Dieu (Maison-Dieu), Hôtel de Moussac, Maison dite du Brouard, Vieux Pont |
| Cité de l'Écrit | Quartier du Brouard (librairies, métiers du livre) |
| Espaces et promenades | Prairie du Séminaire, Espace Camille Olivet, squares |
| Office de tourisme | Office de tourisme, place du Maréchal Leclerc |

Pour chaque lieu : nom, catégorie, adresse lorsqu'elle est connue, courte description, **statut de monument historique** (classé / inscrit) avec un lien vers la notice Mérimée, la **source** de la donnée et, quand il existe, un lien **« Horaires et informations »** vers le site officiel du lieu (pas d'horaires recopiés dans la carte).

Éléments de contexte :

- la **Gartempe**, tracée d'après la BD TOPO ;
- l'**emprise de la Cité de l'Écrit** (quartier du Brouard), plutôt qu'un cercle ;
- un fond Plan IGN vecteur (sans orthophoto), avec un habillage « parchemin » repris de l'ancienne version.

## Critères d'acceptation

- [ ] Les lieux des six catégories sont affichés, chacun avec un pictogramme propre à sa catégorie.
- [ ] Chaque lieu est positionné d'après un objet BD TOPO, une notice Mérimée ou le géocodage de son adresse ; aucune coordonnée n'est saisie à la main.
- [ ] Chaque monument historique recensé dans Mérimée dans l'emprise du centre-ville est affiché, avec son statut (classé / inscrit) et un lien vers sa notice.
- [ ] Un lieu n'a le badge « MH » que s'il correspond à une notice Mérimée.
- [ ] Chaque fiche indique la source de la donnée.
- [ ] Aucun horaire n'est affiché ; les fiches des musées et de l'office de tourisme renvoient vers leur site officiel quand il existe.
- [ ] La Gartempe et l'emprise de la Cité de l'Écrit proviennent de données de référence, pas d'un tracé manuel.
- [ ] Une légende présente les catégories et le badge « MH ».
- [ ] Sur ordinateur, un panneau latéral liste les lieux par catégorie ; un clic sur un lieu centre la carte et ouvre sa fiche.
- [ ] Sur smartphone, la carte occupe l'écran et la liste est accessible dans une fiche repliable qui ne masque pas la carte.
- [ ] Une seule popup est ouverte à la fois.
- [ ] L'habillage « parchemin » (polices, couleurs, cadre) est repris de l'ancienne version, sans gêner la lecture sur smartphone.
- [ ] Le fond de carte est le Plan IGN vecteur, rendu avec MapLibre GL JS ; il n'y a pas de choix d'orthophoto.
- [ ] La vue initiale et l'emprise des données couvrent le centre-ville.
- [ ] Les sources sont attribuées (IGN – BD TOPO®, Plan IGN, ministère de la Culture – Mérimée, Géoplateforme pour le géocodage).
- [ ] « GitHub / Mentions légales » est centré en bas de carte, séparé des attributions (convention commune, voir le [README](../../README.md)).
- [ ] Les données sont produites par un script et versionnées dans `data/` (aucune donnée codée en dur dans la page).
- [ ] La carte est un site statique publiable sur GitHub Pages (aucun serveur applicatif).

## Hors périmètre

- Restauration, hébergement, spécialités et terroir (données commerciales vite périmées).
- Notes et nombres d'avis.
- Lieux situés hors de la commune de Montmorillon (Pindray, Saulgé…).
- Monuments de la commune éloignés du centre-ville : église Saint-Martin et lanterne des morts de Moussac (~4 km), dolmen (~8 km), montjoie (sans coordonnées dans Mérimée).
- Horaires d'ouverture recopiés dans la carte.
- Orthophoto et choix du fond de carte.
- Bouton « Itinéraire » vers l'application de navigation (voir `montmorillon-acces`).
- Circuits de visite et itinéraires piétons.

## Décisions

| Question | Décision |
|---|---|
| Public (issue #15) | Visite sur place (smartphone) et préparation de visite (ordinateur) |
| Catégories (issue #15) | Patrimoine + pratique : musées, patrimoine religieux, monuments civils, Cité de l'Écrit, espaces et promenades, office de tourisme |
| Sources (issue #15) | BD TOPO + Mérimée ; lieux absents géocodés depuis leur adresse |
| Style (issue #15) | Parchemin |
| Rendu (issue #15) | MapLibre + Plan IGN vecteur |
| Bouton « Itinéraire » (issue #15) | Non |
| Orthophoto | Non : Plan IGN seul, teintable pour s'accorder au parchemin |
| Horaires | Non affichés ; lien vers le site officiel du lieu quand il existe |
| Emprise | Centre-ville seul ; monuments éloignés exclus |
