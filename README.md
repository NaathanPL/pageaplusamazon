# Pages A+ Smoby
- `tools/` : aplus.py (lib visuels HQ), build_visuals.py (spec.json -> 9 visuels 600px), vc.js (helpers Vendor Central), hero.md (prompt + méthode ChatGPT), dec.py
- `asins/<ASIN>_<Produit>/` : spec.json, hero.jpg, aplus/ (visuels dans l'ordre d'upload), preview.jpg
- URL brute d'une image : https://raw.githubusercontent.com/NaathanPL/pageaplusamazon/main/asins/<dir>/aplus/<fichier>
- Éditeur VC : URL https://vendorcentral.amazon.fr/hz/vendor/members/aplus/content-manager/workflow/emc-standard/content/<id>/revision/<rev>/edit
- Upload images : `__up(i,url)` dans vc.js (validé). Ne pas recharger une image identique à celle déjà en place.
