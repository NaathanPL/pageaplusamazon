# Hero ChatGPT (onglet ChatGPT du navigateur intégré)
Référence (hero Maison Aventure) : https://m.media-amazon.com/images/S/aplus-media-library-service-media/1bccb329-ae47-4d7b-947f-03a75aef4dc3.__CR0,1,1594,986_PT0_SX970_V1___.png
1. Coller la référence + la photo produit (Image crossOrigin -> canvas -> blob -> ClipboardEvent 'paste' sur .ProseMirror).
2. Insérer le prompt (execCommand insertText), cliquer le bouton aria-label "Envoyer".
3. Récupérer l'image générée : canvas 970x600 -> base64 ; renvoyer 'B64START'+b64+'B64END'+'x'.repeat(200000) pour que la sortie parte en fichier tool-result ; puis `python3 tools/dec.py <fichier> asins/<dir>/hero.jpg`.
4. Produit sous licence bloqué (Disney/Winnie) : demander la bannière sans le produit, puis composer le détourage produit (flood-fill du blanc, scipy).

Prompt (remplacer les {…}) :
Crée une bannière Amazon A+ 970x600 dans le style exact de la première image. Panneau gauche crème avec bord en vague ; titre gras marron foncé sur 3 lignes : "{titre}" ; sous-titre vert sur 2 lignes : "{sous-titre}" ; 3 badges ronds : corail "{âge}", blanc cerclé vert "{atout}", blanc cerclé marron "FABRIQUÉ EN FRANCE" avec picto pin (seulement si le pin est sur la boîte) ; pastille vert #2E5541 en haut à droite avec "{nom produit}". Produit de la deuxième image à droite, fidèle, dans une scène réaliste. Pas de boîte, pas de mention recyclé, pas de logo, texte en français sans faute.

Attente : envoyer le prompt hero puis faire le reste de la page ; première vérification à 1 min 40 après l envoi, puis une par minute.

## Règle du 05/11 (retour client + Nathan)
- ChatGPT reçoit TOUT : modèle, vraie photo produit, logos officiels (tools/assets/logos) et texte de note Anti-UV. Aucune retouche locale ensuite (hero_build.py et hero_overlay.py ne servent plus qu'en secours).
- Nouveau hero : `__hero2(urlProduit,{title,subtitle,age,pill,antiuv,fab,footnote})`. Hero existant à corriger (logos) : `__heroFix(urlHero,{antiuv,fab,pill,footnote})`.
- Le produit doit rester fidèle (jamais redessiné) et intégré à la scène (ombre, herbe/sol, lumière). Ouvertures blanches du packshot = traversantes.
- Contrôle du rendu : logos identiques aux fichiers officiels. Si ChatGPT les déforme, relancer ; ne pas corriger à la main.

## Règle du 16/11 (retour client : pictos modifiés par IA, fonctions ajoutées) : remplace la règle du 05/11
- ChatGPT ne génère plus jamais une bannière complète. `__hero`, `__hero2`, `__heroFix` : ne plus utiliser.
- Seule fonction autorisée, et seulement avec l'accord de Nathan quand aucune photo Drive ne convient : `__heroDecor(urlPackshot,{scene})`. Elle demande uniquement la photo de droite : produit strictement identique au packshot, rien d'ajouté, aucun texte, logo, badge ni panneau.
- Récupération `__heroGet()` puis dec.py vers `asins/<dir>/decor.jpg`, utilisé comme `photo` dans hero_spec.json (scale 1, ox 0). La vague, les textes et les logos officiels sont posés par hero_life.py, comme sur toutes les pages.
- Contrôle : comparer le produit généré au packshot. Une pièce, un accessoire ou une fonction en plus ou en moins : relancer, sinon demander à Nathan.

## Décision du 16/11 (Nathan) : plus de ChatGPT
- Plus aucune génération d image par IA pour les pages A+ Smoby. Le hero est toujours fait par hero_life.py sur une vraie photo Drive.
- Aucune photo utilisable après les deux recherches Drive (SKU complet et 6 derniers chiffres) : demander à Nathan.
- hero.js et les sections ci-dessus sont gardés pour archive, à ne plus utiliser.
