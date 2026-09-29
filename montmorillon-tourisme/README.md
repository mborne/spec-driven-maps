# montmorillon-tourisme

Carte touristique du **centre-ville de Montmorillon** (Vienne), « Cité de l'Écrit » et Ville d'art et d'histoire, avec des données ouvertes et traçables.

Nouvelle version, conçue selon la méthode [spec-driven-maps](../README.md), de l'[ancienne carte touristique](https://github.com/mborne/montmorillon/blob/main/montmorillon_carte_touristique/index.html). Suivi : [issue #15](https://github.com/mborne/spec-driven-maps/issues/15).

## La carte

- **18 lieux** du centre-ville (1 km autour de l'office de tourisme), en six catégories :
  - musées ;
  - patrimoine religieux ;
  - monuments civils ;
  - Cité de l'Écrit ;
  - espaces et promenades ;
  - office de tourisme.
- Les **7 monuments historiques** du centre-ville recensés dans la base Mérimée, avec un badge « MH », leur protection (classé / inscrit) et un lien vers la notice. L'Octogone et la chapelle Saint-Laurent sont rattachés à la notice de l'ancien Hôtel-Dieu.
- Chaque fiche indique la **source** de la donnée : objet BD TOPO, notice Mérimée ou adresse géocodée. La mention « et recherche web » signale les fiches qui contiennent un lien ou un élément de description trouvé sur le web ; le champ `recherche_web` de `scripts/lieux.json` précise lequel.
- Un lien « Horaires et informations » vers le site officiel des musées et de l'office de tourisme ; aucun horaire n'est recopié dans la carte.
- La **Gartempe**, tracée d'après la BD TOPO.
- Fond Plan IGN vecteur teinté sépia et habillage « parchemin » (polices Cinzel, Playfair Display, Crimson Text), repris de l'ancienne version. Rendu MapLibre GL JS.
- Sur ordinateur, un panneau latéral liste les lieux par catégorie. Sur smartphone, la carte occupe l'écran et la liste est dans une fiche repliable.
- Une seule popup ouverte à la fois.
- « [GitHub](https://github.com/mborne/spec-driven-maps/tree/main/montmorillon-tourisme#readme) / [Mentions légales](https://mborne.github.io/mentions-legales/) » centré en bas de carte, séparé des attributions.

Écarts avec l'ancienne version :

- Le Vieux Pont n'a plus de badge « MH » : il ne figure pas dans Mérimée.
- La Cité de l'Écrit est figurée par un point : la BD TOPO ne fournit pas d'emprise du quartier du Brouard.
- La restauration, l'hébergement, les spécialités, les notes et avis, et les lieux hors de Montmorillon sont retirés.

## Méthode

1. **Demande** : voir [specs/spec.md](specs/spec.md) (objectif, public, critères d'acceptation, décisions).
2. **Plan** : voir [specs/plan.md](specs/plan.md) (emprise, sources identifiées avec le MCP geocontext et Mérimée, appariement, symbologie, rendu).
3. **Tâches** : voir [specs/tasks.md](specs/tasks.md).
4. **Implémentation** :
   - [scripts/lieux.json](scripts/lieux.json) décrit chaque lieu par une **référence à sa source**, sans coordonnées : `cleabs` BD TOPO, référence Mérimée ou adresse ;
   - [scripts/fetch_data.py](scripts/fetch_data.py) résout ces références, contrôle l'emprise et vérifie que tous les monuments Mérimée de l'emprise sont présents, puis produit [data/tourisme.geojson](data/tourisme.geojson) ;
   - [index.html](index.html) affiche la carte.

## Prompt équivalent

Pour commander directement une carte équivalente à un assistant disposant du connecteur [MCP geocontext](https://github.com/ignfab/geocontext) :

```text
À l'aide du MCP geocontext, génère une carte web touristique du centre-ville de Montmorillon (86165),
dans un rayon de 1 km autour de l'office de tourisme.

Lieux, en six catégories : musées, patrimoine religieux, monuments civils, Cité de l'Écrit,
espaces et promenades, office de tourisme.
- Décris chaque lieu dans un fichier de configuration par une référence à sa source, sans coordonnées :
  cleabs BD TOPO (BDTOPO_V3:zone_d_activite_ou_d_interet pour musées, églises, chapelles, espaces
  publics et office de tourisme ; BDTOPO_V3:construction_lineaire pour le Vieux Pont ;
  BDTOPO_V3:zone_d_habitation pour le quartier du Brouard), référence Mérimée, ou adresse à géocoder.
- Monuments historiques : base Mérimée (immeubles protégés, ministère de la Culture) via l'API
  tabulaire de data.gouv.fr ; affiche la protection (classé / inscrit) et un lien vers la notice POP.
  Tous les monuments Mérimée de l'emprise doivent être présents ; le badge « MH » n'est donné qu'aux
  lieux associés à une notice.
- La Gartempe d'après BDTOPO_V3:troncon_hydrographique.
- Pas de restauration, d'hébergement, d'horaires ni d'avis ; un lien vers le site officiel des musées
  et de l'office de tourisme.
- Quand une fiche contient une information issue d'une recherche web (lien, complément de description),
  sa source le précise : « Source : IGN – BD TOPO® et recherche web ».
- Un script Python produit un GeoJSON versionné ; la page ne contient aucune donnée.

Rendu :
- Un site statique (index.html + GeoJSON) publiable sur GitHub Pages, avec MapLibre GL JS v5 et le
  fond Plan IGN vecteur standard teinté sépia (filtre CSS sur le canevas).
- Habillage « parchemin » : polices Cinzel, Playfair Display et Crimson Text ; palette parchemin,
  encre, or et rouge sceau ; popups bordées d'or ; pictogrammes colorés par catégorie ; badge « MH ».
- Sur ordinateur, un en-tête et un panneau latéral listant les lieux par catégorie (un clic centre la
  carte et ouvre la fiche) ; sur smartphone, carte plein écran et fiche repliable en bas de l'écran.
- Une seule popup ouverte à la fois ; chaque fiche indique la source de la donnée.
- Attribution des sources (© IGN – BD TOPO®, ministère de la Culture – Mérimée, Géoplateforme) et,
  centré en bas de carte et séparé des attributions, « GitHub / Mentions légales » avec des liens vers
  https://github.com/mborne/spec-driven-maps/tree/main/montmorillon-tourisme#readme
  et https://mborne.github.io/mentions-legales/
```

## Régénérer les données

```bash
python3 scripts/fetch_data.py
```

Le script n'utilise que la bibliothèque standard Python. Il s'arrête en erreur si un lieu sort de l'emprise ou si un monument historique de l'emprise manque dans `scripts/lieux.json`.

## Tester en local

```bash
python3 -m http.server 8000
# puis ouvrir http://localhost:8000/
```
