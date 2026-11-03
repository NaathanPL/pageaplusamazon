# Hero ChatGPT (onglet ChatGPT du navigateur intégré)
Référence (hero Maison Aventure) : https://m.media-amazon.com/images/S/aplus-media-library-service-media/1bccb329-ae47-4d7b-947f-03a75aef4dc3.__CR0,1,1594,986_PT0_SX970_V1___.png
1. Coller la référence + la photo produit (Image crossOrigin -> canvas -> blob -> ClipboardEvent 'paste' sur .ProseMirror).
2. Insérer le prompt (execCommand insertText), cliquer le bouton aria-label "Envoyer".
3. Récupérer l'image générée : canvas 970x600 -> base64 ; renvoyer 'B64START'+b64+'B64END'+'x'.repeat(200000) pour que la sortie parte en fichier tool-result ; puis `python3 tools/dec.py <fichier> asins/<dir>/hero.jpg`.
4. Produit sous licence bloqué (Disney/Winnie) : demander la bannière sans le produit, puis composer le détourage produit (flood-fill du blanc, scipy).

Prompt (remplacer les {…}) :
Crée une bannière Amazon A+ 970x600 dans le style exact de la première image. Panneau gauche crème avec bord en vague ; titre gras marron foncé sur 3 lignes : "{titre}" ; sous-titre vert sur 2 lignes : "{sous-titre}" ; 3 badges ronds : corail "{âge}", blanc cerclé vert "{atout}", blanc cerclé marron "FABRIQUÉ EN FRANCE" avec picto pin (seulement si le pin est sur la boîte) ; pastille vert #2E5541 en haut à droite avec "{nom produit}". Produit de la deuxième image à droite, fidèle, dans une scène réaliste. Pas de boîte, pas de mention recyclé, pas de logo, texte en français sans faute.
