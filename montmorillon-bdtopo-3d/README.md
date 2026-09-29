# montmorillon-bdtopo-3d

Les **bâtiments de Montmorillon en 3D** d'après la BD TOPO® de l'IGN : volumes, hauteurs, usages, et d'où vient chaque hauteur.

Nouvelle version, conçue selon la méthode [spec-driven-maps](../README.md), de l'[ancienne carte 3D](https://github.com/mborne/montmorillon/blob/main/montmorillon-bdtopo-3d/index.html). Suivi : [issue #14](https://github.com/mborne/spec-driven-maps/issues/14).

## La carte

- Les bâtiments de la BD TOPO extrudés en 3D, lus directement dans les **tuiles vectorielles BD TOPO** de la Géoplateforme (couche `batiment`, à partir du zoom 15). Aucune donnée n'est copiée dans le dépôt.
- **Hauteur retenue** : la valeur `hauteur`, sinon le nombre d'étages × 3 m, sinon 3 m. À Montmorillon, 1,8 % des bâtiments n'ont ni hauteur ni étages.
- **Deux colorations** :
  - par usage (8 valeurs de `usage_1`) ;
  - par hauteur, en classes adaptées au bâti local (< 4, 4 – 8, 8 – 12, 12 – 20, ≥ 20 m).
  - La légende est générée à partir des mêmes tableaux que les couleurs.
- **Fiche détaillée** au clic, avec les attributs BD TOPO :
  - usages et nature ;
  - hauteur et **son origine** (mesurée, déduite des étages ou valeur par défaut) ;
  - étages et logements ;
  - altitudes du sol et du toit ;
  - méthode d'acquisition ;
  - date d'apparition ;
  - `cleabs` ;
  - identifiant [RNB](https://rnb.beta.gouv.fr/), avec un lien vers sa fiche.
- **Fond** : Plan IGN vecteur, sans ses bâtiments plats (qui doubleraient la 3D), avec un choix orthophoto.
- Interrupteur « Relief 3D » ; vue inclinée partageable par l'URL ; message « Zoomez pour afficher les bâtiments » sous le zoom 15.
- Panneau de réglages repliable (replié par défaut sur smartphone) ; la page peut être agrandie sur mobile.
- « [GitHub](https://github.com/mborne/spec-driven-maps/tree/main/montmorillon-bdtopo-3d#readme) / [Mentions légales](https://mborne.github.io/mentions-legales/) » centré en bas de carte, séparé des attributions.

Corrections par rapport à l'ancienne version :

- La légende de hauteur correspond aux couleurs (les libellés 0 / 15 / 30 / 50 m ne suivaient pas les paliers 0 / 5 / 12 / 25 / 50 m).
- Les classes de hauteur sont adaptées : 97 % des bâtiments font moins de 12 m.
- Les hauteurs estimées sont signalées.
- La couche est déclarée à partir du zoom 15, où les tuiles commencent (et non 13).
- `maximum-scale` est retiré.
- Les dépendances sont chargées depuis jsdelivr.

## Méthode

1. **Demande** : voir [specs/spec.md](specs/spec.md) (objectif, public, critères d'acceptation, décisions).
2. **Plan** : voir [specs/plan.md](specs/plan.md) :
   - contrôle des données avec le MCP geocontext (usages, hauteurs manquantes, répartition des hauteurs) ;
   - métadonnées des tuiles ;
   - symbologie et rendu.
3. **Tâches** : voir [specs/tasks.md](specs/tasks.md).
4. **Implémentation** : [index.html](index.html). Il n'y a pas de script de données : la page lit les tuiles vectorielles BD TOPO.

## Prompt équivalent

Pour commander directement une carte équivalente à un assistant disposant du connecteur [MCP geocontext](https://github.com/ignfab/geocontext) :

```text
À l'aide du MCP geocontext, génère une carte web des bâtiments de Montmorillon (86165) en 3D,
pour montrer ce que contient la BD TOPO sur les bâtiments.

Données :
- Tuiles vectorielles BD TOPO de la Géoplateforme (https://data.geopf.fr/tms/1.0.0/BDTOPO/{z}/{x}/{y}.pbf),
  couche « batiment », disponible à partir du zoom 15 ; pas d'extraction versionnée.
- Contrôle avec BDTOPO_V3:batiment (WFS) : valeurs de usage_1, part des bâtiments sans hauteur,
  répartition des hauteurs pour choisir les classes.
- Hauteur retenue : hauteur, sinon nombre_d_etages × 3 m, sinon 3 m ; la fiche indique l'origine.

Rendu :
- Un site statique (index.html) publiable sur GitHub Pages, avec MapLibre GL JS v5 et fill-extrusion ;
  vue inclinée sur le centre-ville, hash dans l'URL, emprise limitée à la commune.
- Fond Plan IGN vecteur standard sans ses bâtiments plats (couches « bati_surf »), avec un choix
  orthophoto (WMTS ORTHOIMAGERY.ORTHOPHOTOS) sous les libellés.
- Deux colorations : par usage (8 valeurs) et par hauteur en classes (< 4, 4–8, 8–12, 12–20, ≥ 20 m) ;
  légende générée à partir des mêmes tableaux.
- Fiche au clic : usages, nature, hauteur et origine, étages, logements, altitudes sol et toit,
  méthode d'acquisition, date d'apparition, cleabs, identifiant RNB avec lien.
- Interrupteur « Relief 3D », panneau repliable (replié sur smartphone), message « Zoomez » sous le zoom 15.
- Attribution des sources (© IGN – BD TOPO®, orthophotographie) et, centré en bas de carte et séparé
  des attributions, « GitHub / Mentions légales » avec des liens vers
  https://github.com/mborne/spec-driven-maps/tree/main/montmorillon-bdtopo-3d#readme
  et https://mborne.github.io/mentions-legales/
```

## Tester en local

```bash
python3 -m http.server 8000
# puis ouvrir http://localhost:8000/
```
