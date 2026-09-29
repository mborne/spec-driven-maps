# Tâches – montmorillon-acces

- [x] Géocoder l'adresse du lieu avec le MCP geocontext
- [x] Identifier la gare et les parkings (`BDTOPO_V3:equipement_de_transport`)
- [x] Tester le service d'itinéraire piéton de la Géoplateforme (gare → lieu)
- [x] Rédiger `specs/spec.md` et un brouillon de `specs/plan.md`
- [x] Trancher les questions ouvertes (style sobre, parkings < 1,5 km, bouton seul, dates 2026)
- [x] Écrire `scripts/fetch_data.py` (géocodage, WFS, géocodage inverse, itinéraires) → `data/acces.geojson`
- [x] Écrire `index.html` (fond Plan IGN, marqueurs, itinéraire gare → lieu, fiche, boutons « Itinéraire », légende, attribution)
- [x] Vérifier les liens générés selon l'appareil (émulation Playwright iPhone 13, Pixel 7, ordinateur)
- [ ] Tester les boutons « Itinéraire » sur de vrais smartphones Android et iOS
- [x] Tester localement : `python3 -m http.server -d montmorillon-acces 8000`
- [x] Vérifier les critères d'acceptation de `spec.md` (sauf ouverture réelle des applications de navigation)
- [x] Rédiger `README.md` (carte, méthode, prompt équivalent)
- [ ] Publier sur GitHub Pages
