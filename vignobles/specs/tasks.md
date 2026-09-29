# Tâches – vignobles

- [x] Identifier le type WFS et ses propriétés avec le MCP geocontext (`BDTOPO_V3:zone_de_vegetation`, `nature = 'Vigne'`)
- [x] Vérifier le niveau de zoom d'apparition des vignes dans les tuiles du Plan IGN (≈ z 12)
- [x] Vérifier la stratégie de téléchargement (bbox Lambert-93 rapides, pagination profonde trop lente)
- [x] Écrire `scripts/fetch_vignes.py` (quadtree, dédoublonnage, surface et centroïde de chaque vigne, contrôle de complétude)
- [x] Écrire `scripts/fetch_bassins.sh` (téléchargement et simplification des bassins AOP, points d'étiquette)
- [x] Générer `data/bassins-aop.geojson` et `data/bassins-aop-labels.geojson`
- [x] Abandonner la grille de 1 et 5 km : trop lourde pour un chargement fluide à petite échelle. Elle est remplacée par la densité de vignoble par commune
- [x] Identifier le type des communes : `ADMINEXPRESS-COG-CARTO.LATEST:commune` (absent du catalogue du MCP, vérifié par `GetCapabilities`)
- [x] Écrire `scripts/fetch_communes.py` (communes métropolitaines par département, Lambert-93)
- [x] Écrire `scripts/build_communes.sh` (jointure SpatiaLite, agrégats, simplification mapshaper, WGS84)
- [x] Générer `data/vignes-centroides.csv` et `data/communes-cog-carto.geojson`
- [x] Générer `data/vignes-communes.csv` et `data/communes-vigne.geojson` ; vérifier le taux de rattachement (379 280 / 379 335) et le poids du fichier (2,7 Mo après simplification à 5 % et seuil de 1 ha)
- [x] Ajuster les seuils de classes à la distribution observée
- [x] Écrire `index.html` (fond gris, communes, vignes des tuiles, bassins, légende, popups, accès rapides)
- [x] Afficher un message pendant le chargement des données (et en cas d'échec)
- [x] Ajouter le pied de carte « GitHub / Mentions légales »
- [x] Tester localement : `python3 -m http.server 8000` (captures Playwright : France, Champagne z 9 / 12 / 13,5, Saint-Dié, mobile ; aucune erreur console)
- [x] Vérifier les critères d'acceptation de `spec.md`
- [x] Documenter la carte et la méthode dans le `README.md`
- [ ] Publier (GitHub Pages) : intégration dans spec-driven-maps (`vignobles`)

## Au-delà de la V0

- [ ] Contrôler la vigne de la BD TOPO avec le RPG (code culture vigne).
- [ ] Carte « vignobles disparus » en Lorraine et dans les Vosges, à partir de la carte d'État-major.
- [ ] Ajouter les délimitations parcellaires des AOC de l'INAO et une version interactive par appellation.
- [ ] Étendre aux DROM.
