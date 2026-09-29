# Tâches – commune-doubs

- [x] Identifier le type WFS et ses propriétés avec le MCP geocontext
- [x] Écrire `scripts/fetch_data.py` (téléchargement, contrôle, densité, arrondi)
- [x] Générer les données brutes `data/communes-doubs-brut.geojson` (563 communes, ~3 Mo)
- [x] Simplifier avec mapshaper (`scripts/simplify.sh`) → `data/communes-doubs.geojson` (~0,5 Mo)
- [x] Écrire `index.html` (fond Plan IGN, choroplèthe, légende, popup, attribution)
- [x] Passer le fond Plan IGN en niveaux de gris
- [x] Afficher un message pendant le chargement des communes (et en cas d'échec)
- [x] Ajouter le lien vers les mentions légales en bas de carte
- [x] Centrer les mentions légales en bas de carte, séparées des attributions
- [x] Tester localement : `python3 -m http.server -d commune-doubs 8000`
- [x] Vérifier les critères d'acceptation de `spec.md`
- [ ] Publier sur GitHub Pages
