# Plan technique – montmorillon-tourisme

## Principe

La liste des lieux est un **fichier de configuration** versionné, [`scripts/lieux.json`](../scripts/lieux.json). Il fixe pour chaque lieu sa catégorie, son nom, une courte description, le lien vers son site officiel, et surtout **la référence de l'objet source** (identifiant BD TOPO, référence Mérimée ou adresse à géocoder). Il ne contient **aucune coordonnée**.

[`scripts/fetch_data.py`](../scripts/fetch_data.py) résout ces références auprès des services et produit `data/tourisme.geojson`. La page ne fait qu'afficher ce fichier.

## Emprise : le centre-ville

- Disque de **1 km autour de l'office de tourisme** (objet BD TOPO `SURFACTI0000000319021128`, place du Maréchal Leclerc).
- Le script **s'arrête en erreur** si un lieu est hors de l'emprise.
- Il **s'arrête aussi en erreur** si un monument Mérimée de la commune situé dans l'emprise est absent de `lieux.json`. C'est ce contrôle qui garantit le critère « chaque monument historique du centre-ville est affiché ».
- Résultat : 7 des 11 monuments de la commune sont dans l'emprise. Sont exclus l'église Saint-Martin et la lanterne des morts de Moussac (~3,3 km), le dolmen (~7,6 km) et la montjoie (sans coordonnées).

## Sources

### BD TOPO – lieux (`BDTOPO_V3:zone_d_activite_ou_d_interet`)

Démarche avec le MCP geocontext :

1. `gpf_wfs_search_types` (« monument historique », « musée »…) → `zone_d_activite_ou_d_interet`, qui porte musées, lieux de culte, espaces publics et office de tourisme (`nature`, `nature_detaillee`, `toponyme`).
2. `gpf_wfs_describe_type` → propriétés `cleabs`, `categorie`, `nature`, `nature_detaillee`, `toponyme`, `identifiants_sources`, `geometrie` (multipolygone).
3. `gpf_wfs_get_features` sur `insee_commune = '86165'` et `categorie IN ('Culture et loisirs', 'Religieux')` → 25 objets, dont les lieux retenus :

| Lieu | `cleabs` | `identifiants_sources` |
|---|---|---|
| Église Notre-Dame | `SURFACTI0000000090133952` | `BASILIC:MONH_86165_65957` |
| Église Saint-Martial | `SURFACTI0000000090116518` | `BASILIC:MONH_86165_65950` |
| Octogone | `SURFACTI0000000223411829` | – |
| Chapelle Saint-Laurent | `SURFACTI0000000090129986` | – |
| Musée d'Art et d'Histoire | `SURFACTI0000002012620301` | `MUSEO:m0851` |
| Musée de l'Amande et du Macaron | `SURFACTI0000000223411911` | `SIRTAQUI:PCUAQU086V500331` |
| Office de tourisme | `SURFACTI0000000319021128` | `SIRTAQUI:ORGAQU086V50024V` |
| Prairie du Séminaire | `SURFACTI0000000090129984` | – |
| Square Alphonse Boudard | `SURFACTI0000000315532392` | – |
| Square Médina del Campo | `SURFACTI0000000242611947` | – |

Le point affiché est le centroïde surfacique de l'objet. Les places (Pont de Bois, Régine Deforges…), le temple sans nom, le cinéma et la médiathèque ne sont pas retenus.

### BD TOPO – autres objets

| Élément | Type | Objet |
|---|---|---|
| Vieux Pont | `BDTOPO_V3:construction_lineaire` (`nature = 'Pont'`, sans toponyme) | `CONSLINE0000000054298680` : le pont qui traverse la Gartempe au pied de Notre-Dame. Le point affiché est le milieu de la ligne |
| Cité de l'Écrit | `BDTOPO_V3:zone_d_habitation` (`nature = 'Quartier'`) | `PAIHABIT0000002207067543`, quartier « Brouard ». Ce n'est qu'un repère de 9 m × 6 m, pas un périmètre : seul son centroïde est affiché |
| Gartempe | `BDTOPO_V3:troncon_hydrographique` | tronçons où `cpx_toponyme_de_cours_d_eau = 'la Gartempe'` dans l'emprise |

Pour le filtre spatial WFS, la syntaxe qui fonctionne est `BBOX(geometrie, lon_min, lat_min, lon_max, lat_max, 'EPSG:4326')`. Avec les latitudes en premier, ou sans système de coordonnées, la requête ne renvoie rien.

### Mérimée – monuments historiques

- Source : [Immeubles protégés au titre des monuments historiques](https://www.data.gouv.fr/datasets/immeubles-proteges-au-titre-des-monuments-historiques-2) (ministère de la Culture, Licence Ouverte).
- On l'interroge avec l'[API tabulaire de data.gouv.fr](https://tabular-api.data.gouv.fr/api/resources/3a52af4a-f9da-4dcc-8110-b07774dfb3bc/data/?Commune_forme_index__exact=Montmorillon), qui renvoie 11 notices, plutôt que de télécharger le CSV national de 100 Mo.
- Champs utilisés : `Reference`, `Titre_editorial_de_la_notice`, `Typologie_de_la_protection`, `Date_et_typologie_de_la_protection`, `Siecle_de_la_campagne_principale_de_construction`, `Datation_de_l_edifice`, `coordonnees_au_format_WGS84`.
- Lien vers la notice : `https://pop.culture.gouv.fr/notice/merimee/<Reference>`.

Dans `lieux.json`, le champ `merimee` associe un lieu à sa notice, qu'il soit positionné par la BD TOPO ou par Mérimée :

| Lieu | Notice | Protection affichée |
|---|---|---|
| Église Notre-Dame | PA00105545 | classé |
| Église Saint-Martial | PA00105546 | inscrit |
| Maison-Dieu (ancien Hôtel-Dieu) | PA00105548 | classé et inscrit (partiellement) |
| Octogone | PA00105548 (partie) | classé : « chapelle octogonale : classement par liste de 1840 » |
| Chapelle Saint-Laurent | PA00105548 (partie) | inscrit : « chapelle Saint-Laurent (à l'exclusion des parties classées) : inscription par arrêté du 3 décembre 1930 » |
| Hôtel de Moussac | PA00105549 | classé (partiellement) |
| Hôtel, 7 rue Saint-Christophe | PA00105550 | inscrit |
| Maison dite du Brouard | PA00105552 | inscrit |
| Ancien hôpital | PA86000064 | inscrit (2024) |

Les lieux positionnés par Mérimée sont la Maison-Dieu, les hôtels de Moussac et de la rue Saint-Christophe, la maison du Brouard et l'ancien hôpital. Le **Vieux Pont** n'a pas de notice : il n'a donc **pas** de badge MH.

### Géocodage – lieux absents des référentiels

- **Espace Camille Olivet** : absent de la BD TOPO. Il est géocodé depuis l'adresse de l'ancienne carte, « 23 avenue Fernand Tribot, 86500 Montmorillon » (`https://data.geopf.fr/geocodage/search`). Le script exige un résultat au numéro (`type = housenumber`).

## Contenu des fiches

| Champ | Origine |
|---|---|
| Nom | `lieux.json` (nom d'usage), sinon toponyme de la source |
| Catégorie | `lieux.json` |
| Description | `lieux.json` : une à deux phrases factuelles et durables, sans horaires, tarifs ni avis |
| Adresse | `adresse_postale` BD TOPO, adresse Mérimée ou adresse géocodée, si disponible |
| Monument historique | Mérimée : protection et siècle, lien vers la notice POP |
| Horaires et informations | `lieux.json` (`site`) : musées et office de tourisme uniquement, liens vérifiés le 29/09/2026 |
| Source | générée : « IGN – BD TOPO® (cleabs) », « Culture – Mérimée (référence) » ou « Adresse géocodée (Géoplateforme) » |

Sites officiels retenus :

- Musée d'Art et d'Histoire : <https://www.montmorillon.fr/contacts/musee-de-france-dart-et-dhistoire-de-montmorillon-mahm/>
- Musée de l'Amande et du Macaron : <https://www.museedumacaron.com/>
- Office de tourisme Sud Vienne Poitou, bureau de Montmorillon : <https://www.sudviennepoitou.com/toute-l-offre/office-de-tourisme-sud-vienne-poitou-3733478> (fiche du bureau, plutôt que l'accueil du site qui couvre tout le territoire)

## Symbologie

| Catégorie | Couleur | Pictogramme |
|---|---|---|
| Musées | `#8b1a1a` (rouge sceau) | 🏛 |
| Patrimoine religieux | `#6b4c8b` | ⛪ |
| Monuments civils | `#5a3a1a` | 🏰 |
| Cité de l'Écrit | `#2c6b6b` | 📚 |
| Espaces et promenades | `#4a6741` | 🌿 |
| Office de tourisme | `#b8860b` (or) | ℹ️ |
| Gartempe | `#4a6fa5`, 4 px | ligne |

- Les couleurs et pictogrammes sont repris de l'ancienne version.
- Les marqueurs sont des pastilles rondes cerclées de parchemin.
- Le badge « MH » est un petit sceau rouge accolé au marqueur et au nom dans la liste.

## Rendu

- **MapLibre GL JS v5** (CDN jsdelivr), un seul `index.html`.
- **Fond** : Plan IGN vecteur, style `standard` (`https://data.geopf.fr/annexes/ressources/vectorTiles/styles/PLAN.IGN/standard.json`), teinté parchemin par un filtre CSS sur le canevas de la carte (`sepia(0.55) saturate(0.7)`).
  - Les marqueurs HTML ne sont pas touchés par ce filtre ; le trait de la Gartempe dans la légende reçoit le même filtre que la carte.
  - Le style `attenue`, essayé d'abord, devenait trop pâle une fois teinté : les rues ne se lisaient plus.
  - Les couches ajoutées sont insérées au-dessus du dernier aplat du fond, sous ses libellés : le style intercale des symboles tôt dans la pile, qui masqueraient la Gartempe.
  - Pas d'orthophoto.
- **Habillage parchemin** repris de l'ancienne version :
  - polices Cinzel (titres), Playfair Display (sous-titres) et Crimson Text (texte), via Google Fonts ;
  - palette `--parchment #f5edd6`, `--ink #2c1f0f`, `--gold #b8860b`, `--red-seal #8b1a1a` ;
  - filets dorés ; popups sur fond parchemin bordé d'or.
- **Ordinateur** (> 700 px) : en-tête compact (« Montmorillon », sous-titre « Cité de l'Écrit & patrimoine roman ») et panneau latéral à droite (320 px) avec la légende et la liste des lieux par catégorie. Un clic dans la liste centre la carte et ouvre la fiche.
- **Smartphone** (≤ 700 px) : carte plein écran, titre dans la fiche en bas de l'écran. La fiche est repliée par défaut (titre + « Afficher les lieux et la légende ») et se déplie pour montrer la liste, sans masquer la carte (même principe que `montmorillon-acces`).
- **Vue initiale** : emprise des lieux, en tenant compte du panneau.
- **Une seule popup** ouverte à la fois : la page garde une référence à la popup ouverte.
- **Pied de carte** : « GitHub / Mentions légales » centré en bas, séparé des attributions (convention commune). Le lien GitHub pointe vers `https://github.com/mborne/spec-driven-maps/tree/main/montmorillon-tourisme#readme`.
- **Attribution** : © IGN – BD TOPO®, Plan IGN · Ministère de la Culture – Mérimée · Géoplateforme (géocodage).
- Chargement : message pendant le chargement de `data/tourisme.geojson`, et message d'échec.

## Hébergement

GitHub Pages depuis la racine du dépôt, servie sous `/<depot>/montmorillon-tourisme/`. Chemins relatifs.

## Décisions

Voir [spec.md](spec.md#décisions) et l'[issue #15](https://github.com/mborne/spec-driven-maps/issues/15). Décisions propres au plan :

| Question | Décision |
|---|---|
| Emprise du centre-ville | Disque de 1 km autour de l'office de tourisme, contrôlé par le script |
| Liste des lieux | `scripts/lieux.json`, références aux sources sans coordonnées |
| Mérimée | API tabulaire data.gouv.fr (filtre sur la commune) |
| Fond | Plan IGN `standard` teinté par filtre CSS (`attenue` trop pâle une fois teinté) |
| Emprise de la Cité de l'Écrit | Non disponible dans les référentiels : point seul |
| Théâtre de plein air, chauffoir | Non retenus comme lieux distincts : ils sont mentionnés dans les fiches de la Prairie du Séminaire et de la Maison-Dieu |
