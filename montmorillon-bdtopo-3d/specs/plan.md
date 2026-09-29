# Plan technique – montmorillon-bdtopo-3d

## Données

### Bâtiments : tuiles vectorielles BD TOPO

| Élément | Choix |
|---|---|
| Source | `https://data.geopf.fr/tms/1.0.0/BDTOPO/{z}/{x}/{y}.pbf` ([métadonnées](https://data.geopf.fr/tms/1.0.0/BDTOPO/metadata.json), édition du 15/06/2026) |
| Couche | `batiment`, disponible **du zoom 15 au zoom 19** |
| Attributs utilisés | `hauteur`, `nombre_d_etages`, `usage_1`, `usage_2`, `nature`, `nombre_de_logements`, `altitude_minimale_sol`, `altitude_maximale_toit`, `methode_d_acquisition_altimetrique`, `date_d_apparition`, `cleabs`, `identifiants_rnb` |

- Aucune donnée n'est copiée dans le dépôt : la page lit les tuiles directement.
- La couche n'existe qu'à partir du zoom 15. En dessous, un message « Zoomez pour afficher les bâtiments » est affiché. L'ancienne version déclarait la couche dès le zoom 13 ; elle y restait vide.

### Contrôle avec le MCP geocontext (WFS `BDTOPO_V3:batiment`)

Sur l'emprise `0.845, 46.405 – 0.895, 46.445` (ville et abords) :

- `gpf_wfs_describe_type` : les 8 valeurs de `usage_1` sont Résidentiel, Annexe, Indifférencié, Commercial et services, Industriel, Agricole, Religieux et Sportif. Aucun bâtiment n'est sans usage.
- `result_type=hits` : **6 995 bâtiments**, répartis ainsi :

  | Usage | Bâtiments |
  |---|---|
  | Résidentiel | 2 906 |
  | Indifférencié | 2 824 |
  | Annexe | 868 |
  | Commercial et services | 343 |
  | Religieux | 20 |
  | Agricole | 16 |
  | Sportif | 14 |
  | Industriel | 4 |

- Hauteurs :
  - 149 bâtiments n'ont pas de `hauteur` ;
  - parmi eux, **128 (1,8 %)** n'ont pas non plus de `nombre_d_etages` : ils reçoivent la valeur par défaut de 3 m.
- Répartition des hauteurs renseignées :

  | Hauteur | Bâtiments |
  |---|---|
  | < 4 m | 3 037 |
  | 4 – 8 m | 3 222 |
  | 8 – 12 m | 517 |
  | 12 – 16 m | 76 |
  | 16 – 20 m | 16 |
  | 20 – 30 m | 3 |
  | ≥ 30 m | 1 |

- Emprise de la commune (`BDTOPO_V3:commune`, `code_insee = '86165'`) : `0.8256, 46.3814 – 0.9622, 46.4769`.

## Hauteur et origine

```text
hauteur > 0            → hauteur                    (origine : « mesurée », BD TOPO)
sinon nombre_d_etages > 0 → nombre_d_etages × 3 m   (origine : « déduite du nombre d'étages »)
sinon                  → 3 m                        (origine : « valeur par défaut »)
```

- La même expression MapLibre sert à l'extrusion et à la coloration par hauteur.
- La fiche affiche l'origine de la hauteur retenue.
- Les volumes « poussent » entre les zooms 15 et 16 (interpolation de la hauteur), comme dans l'ancienne version.

## Symbologie

### Par usage (couleurs de l'ancienne version)

| `usage_1` | Couleur |
|---|---|
| Résidentiel | `#d98c5f` |
| Commercial et services | `#5b8bb5` |
| Industriel | `#7d8a99` |
| Agricole | `#8aa86a` |
| Sportif | `#56a6a0` |
| Religieux | `#9b7bb5` |
| Annexe | `#cab38f` |
| Indifférencié | `#b9b1a4` |

### Par hauteur (classes, expression `step`)

Les classes suivent la répartition observée. L'ancienne rampe continue de 0 à 50 m colorait presque toute la ville avec ses deux premières teintes, et ses libellés (0, 15, 30, 50 m) ne correspondaient pas à ses paliers (0, 5, 12, 25, 50 m).

| Classe | Couleur |
|---|---|
| < 4 m | `#e8d9c0` |
| 4 – 8 m | `#d8b48c` |
| 8 – 12 m | `#c98a5c` |
| 12 – 20 m | `#a85a3c` |
| ≥ 20 m | `#6e3a30` |

La légende est générée à partir des mêmes tableaux que les expressions de couleur : elle ne peut pas diverger de la carte.

## Fond de carte

- **Plan IGN vecteur** : style `standard` (`https://data.geopf.fr/annexes/ressources/vectorTiles/styles/PLAN.IGN/standard.json`).
  - Les couches de source `bati_surf` (bâtiments plats, types `fill` et `line`) sont masquées au chargement.
  - Les zones d'activité (`bati_zai`) et les libellés sont conservés.
- **Orthophoto** : couche raster WMTS `ORTHOIMAGERY.ORTHOPHOTOS` (`https://data.geopf.fr/wmts`, `TILEMATRIXSET=PM`).
  - Elle est ajoutée au-dessus des aplats du fond et sous ses libellés, puis rendue visible ou masquée par le sélecteur.
- Les bâtiments 3D sont ajoutés en dernier, au-dessus de tout.

## Rendu

- **MapLibre GL JS v5** (CDN jsdelivr), un seul `index.html`.
- **Vue initiale** : centre `0.8713, 46.4262`, zoom 15,6, inclinaison 58°, orientation −22° (ancienne version).
  - `hash: true` pour partager la vue par l'URL.
  - `maxBounds` sur l'emprise de la commune, élargie de 2 km.
- **Panneau de réglages** repris de l'ancienne version, repliable :
  - fond (Plan IGN / Orthophoto) ;
  - coloration (Par usage / Par hauteur) ;
  - interrupteur « Relief 3D » ;
  - légende.
  - Sur smartphone, il est replié par défaut.
- **Fiche** au clic : une seule popup MapLibre réutilisée. Contenu :
  - usage principal (titre) et usage secondaire ;
  - nature ;
  - hauteur retenue et son origine ;
  - nombre d'étages et de logements ;
  - altitudes du sol (minimale) et du toit (maximale) ;
  - méthode d'acquisition altimétrique ;
  - date d'apparition si renseignée ;
  - `cleabs` ;
  - identifiant RNB, avec un lien vers la fiche du Référentiel national des bâtiments quand il existe.
- **Chargement** : écran « Chargement de Montmorillon… » jusqu'au premier rendu complet, puis message « Zoomez pour afficher les bâtiments » sous le zoom 15.
- **Pied de carte** : « GitHub / Mentions légales », centré en bas et séparé des attributions (convention commune). Le lien GitHub pointe vers `https://github.com/mborne/spec-driven-maps/tree/main/montmorillon-bdtopo-3d#readme`. Le bandeau « Données BD TOPO®… » de l'ancienne version, qui occupait cette place, est supprimé ; les sources vont dans l'attribution.
- **Attribution** : © IGN – BD TOPO®, Plan IGN, orthophotographie (Géoplateforme).
- **Dépendances** : jsdelivr plutôt qu'unpkg ; pas de `glyphs` inutile (les libellés viennent du style Plan IGN).
- **Accessibilité** : `viewport` sans `maximum-scale` ; boutons du panneau atteignables au clavier.

## Hébergement

GitHub Pages depuis la racine du dépôt, servie sous `/<depot>/montmorillon-bdtopo-3d/`. Chemins relatifs.

## Décisions

Voir [spec.md](spec.md#décisions) et l'[issue #14](https://github.com/mborne/spec-driven-maps/issues/14). Décisions propres au plan :

| Question | Décision |
|---|---|
| Classes de hauteur | < 4, 4 – 8, 8 – 12, 12 – 20, ≥ 20 m (répartition observée) |
| Bâtiments plats du Plan IGN | Couches `bati_surf` masquées |
| Emprise | `maxBounds` sur la commune élargie de 2 km |
| Données | Aucune extraction versionnée ; pas de script |
