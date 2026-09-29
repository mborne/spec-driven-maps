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

## Cartes

| Dossier | Description | Statut |
|---|---|---|
| [commune-doubs](commune-doubs/) | Densité de population des communes du Doubs | exemple de départ |
| montmorillon-acces | Carte d'accès au Printemps des Cartes | à venir |
| montmorillon-tourisme | Carte touristique de Montmorillon | à venir |
| montmorillon-bdtopo-3d | Carte des bâtiments de Montmorillon en 3D | à venir |

Référence : <https://mborne.github.io/montmorillon/>
