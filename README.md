# spec-driven-maps

**EXPERIMENTATION**

L'idée consiste à expérimenter la méthode [Specification-Driven Development (SDD)](https://github.com/github/spec-kit/blob/main/spec-driven.md) pour produire des cartes à l'aide d'assistant de codage et de connecteurs fournissant un accès aux données tels le [MCP geocontext](https://github.com/ignfab/geocontext) pour l'accès aux données de la géoplateforme.

## Principes

- Chaque carte produite correspond à un dossier (ex : `montmorillon-bdtopo-3d` pour la carte des bâtiments de Montmorillon en 3D).
- Chaque dossier est un site statique hébergé sur GitHub Pages.
- Chaque dossier contient un `README.md` qui décrit la carte et la méthode de création.
- Chaque dossier contient un sous-dossier `specs/` avec les éléments qui spécifient la création :
  - `spec.md` : **quoi et pourquoi** (demande, objectif, public, critères d'acceptation) ;
  - `plan.md` : **comment** (sources de données, traitements, symbologie, rendu) ;
  - `tasks.md` : les tâches de réalisation.

## Conventions communes

Toutes les cartes respectent les règles suivantes :

- **Pied de carte** : « GitHub / Mentions légales » est centré en bas de la carte, séparé des attributions des sources (qui restent dans le contrôle d'attribution MapLibre, en bas à droite) :
  - « GitHub » renvoie vers le README de la carte dans le dépôt : `https://github.com/mborne/spec-driven-maps/tree/main/<dossier>#readme` ;
  - « Mentions légales » renvoie vers <https://mborne.github.io/mentions-legales/>.

## Cartes

| Dossier | Description | Statut |
|---|---|---|
| [commune-doubs](commune-doubs/) | Densité de population des communes du Doubs | exemple de départ |
| [montmorillon-acces](montmorillon-acces/) | Carte d'accès au Printemps des Cartes 2026 | réalisée |
| [montmorillon-tourisme](montmorillon-tourisme/) | Carte touristique de Montmorillon ([#15](https://github.com/mborne/spec-driven-maps/issues/15)) | réalisée |
| [montmorillon-bdtopo-3d](montmorillon-bdtopo-3d/) | Carte des bâtiments de Montmorillon en 3D ([#14](https://github.com/mborne/spec-driven-maps/issues/14)) | réalisée |
| [vignobles](vignobles/) | Où sont les vignobles ? Densité de vignoble par commune et vignes de la BD TOPO | en construction |

Référence : <https://mborne.github.io/montmorillon/>
