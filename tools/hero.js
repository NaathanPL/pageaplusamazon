// ChatGPT (chatgpt.com, nouveau chat) : __hero(urlProduit, {title,subtitle,b1,b2,b3,pill}) colle référence + produit, écrit le prompt, envoie.
window.__hero=async(prod,o)=>{const ed=document.querySelector('.ProseMirror');if(!ed)return 'pas d editeur';
 const load=u=>new Promise((res,rej)=>{const i=new Image();i.crossOrigin='anonymous';i.onload=()=>{const c=document.createElement('canvas');c.width=i.naturalWidth;c.height=i.naturalHeight;c.getContext('2d').drawImage(i,0,0);c.toBlob(b=>res(b),'image/png')};i.onerror=rej;i.src=u});
 const ref='https://m.media-amazon.com/images/S/aplus-media-library-service-media/1bccb329-ae47-4d7b-947f-03a75aef4dc3.__CR0,1,1594,986_PT0_SX970_V1___.png';
 const dt=new DataTransfer();dt.items.add(new File([await load(ref)],'ref.png',{type:'image/png'}));dt.items.add(new File([await load(prod)],'produit.png',{type:'image/png'}));
 ed.focus();ed.dispatchEvent(new ClipboardEvent('paste',{clipboardData:dt,bubbles:true,cancelable:true}));await new Promise(r=>setTimeout(r,4000));
 const fr=o.b3?`blanc cerclé marron "${o.b3}" avec picto pin`:'';
 ed.focus();document.execCommand('insertText',false,`Crée une bannière Amazon A+ 970x600 dans le style exact de la première image. Panneau gauche crème avec bord en vague ; titre gras marron foncé sur 3 lignes : "${o.title}" ; sous-titre vert sur 2 lignes : "${o.subtitle}" ; badges ronds : corail "${o.b1}", blanc cerclé vert "${o.b2}"${fr?', '+fr:''} ; pastille vert #2E5541 en haut à droite avec "${o.pill}". Produit de la deuxième image à droite, fidèle, dans une scène réaliste. Pas de boîte, pas de mention recyclé, pas de logo, texte en français sans faute.`);
 await new Promise(r=>setTimeout(r,2000));const b=document.querySelector('[aria-label="Envoyer"],[data-testid="send-button"]');if(!b)return 'pas de bouton';b.click();return 'envoyé'};
// récupération : __heroGet() -> base64 970x600 (sortie forcée en fichier) puis python3 tools/dec.py <fichier> asins/<dir>/hero.jpg
window.__heroGet=()=>{const i=[...document.querySelectorAll('img')].filter(i=>/Image générée/.test(i.alt)&&i.naturalWidth>300).pop();if(!i)return 'pas encore';const c=document.createElement('canvas');c.width=970;c.height=600;const x=c.getContext('2d');x.imageSmoothingQuality='high';x.drawImage(i,0,0,970,600);return 'B64START'+c.toDataURL('image/jpeg',0.95).split(',')[1]+'B64END'+'x'.repeat(200000)};

// ---- Version 05/11 : TOUT est donné à ChatGPT (logos officiels compris), aucune retouche locale ensuite.
// __hero2(urlProduit, {title,subtitle,age,pill,antiuv:true|false,fab:'light'|'cartouche'|null,footnote,ref})
//  - ref : hero modèle (par défaut le hero Maison Aventure validé)
//  - images collées dans l'ordre : 1 modèle, 2 produit, puis logo Anti-UV, puis logo Fabriqué en France (si demandés)
// __heroFix(urlHeroExistant, {antiuv,fab,pill,footnote}) : refait un hero existant à l'identique en remplaçant seulement les logos/badges par les officiels.
(()=>{
const RAW='https://raw.githubusercontent.com/NaathanPL/pageaplusamazon/main/';
const REF=RAW+'asins/B0H5WR7Y74_Maison-Aventure/aplus/B0H5WR7Y74_01_Hero.jpg';
const load=u=>new Promise((res,rej)=>{const i=new Image();i.crossOrigin='anonymous';i.onload=()=>{const c=document.createElement('canvas');c.width=i.naturalWidth;c.height=i.naturalHeight;c.getContext('2d').drawImage(i,0,0);c.toBlob(b=>res(b),'image/png')};i.onerror=rej;i.src=u});
const send=async(files,prompt)=>{const ed=document.querySelector('.ProseMirror');if(!ed)return 'pas d editeur';
 const dt=new DataTransfer();for(const [n,u] of files)dt.items.add(new File([await load(u)],n,{type:'image/png'}));
 ed.focus();ed.dispatchEvent(new ClipboardEvent('paste',{clipboardData:dt,bubbles:true,cancelable:true}));await new Promise(r=>setTimeout(r,5000));
 ed.focus();document.execCommand('insertText',false,prompt);await new Promise(r=>setTimeout(r,2000));
 const b=document.querySelector('[aria-label="Envoyer"],[data-testid="send-button"]');if(!b)return 'pas de bouton';b.click();return 'envoyé'};
const logosPart=(o,start)=>{const f=[],t=[];let n=start;
 if(o.antiuv){f.push(['anti_uv.png',RAW+'tools/assets/logos/logo_anti_uv.png']);t.push(`le logo Anti-UV (image ${n++}) avec un astérisque brun juste à côté`)}
 if(o.fab){f.push(['fab.png',RAW+'tools/assets/logos/'+(o.fab==='light'?'fab_bloc_rvb.png':'fab_bloc_cartouche_rvb.jpg')]);t.push(`le logo Fabriqué en France (image ${n++})`)}
 return {f,t}};
const rules=(o,L)=>`Place EXACTEMENT, sans les redessiner, sans les modifier ni les redessiner à ta façon, copiés pixel pour pixel, ${L.t.join(' et ')}, en bas du panneau crème, à côté du badge rond corail. Pas d'autre badge ni logo.`+(o.footnote?` Ajoute en tout petit sous les badges, en brun, le texte exact : "* ${o.footnote}".`:'');
window.__hero2=async(prod,o)=>{const L=logosPart(o,3);
 return send([['ref.png',o.ref||REF],['produit.png',prod],...L.f],
 `Crée une bannière Amazon A+ 970x600 dans le style de la première image : panneau gauche crème avec bord en vague, titre gras marron foncé sur 3 lignes : "${o.title}" ; sous-titre vert sur 2 lignes : "${o.subtitle}" ; badge rond corail "${o.age}" ; pastille vert #2E5541 en haut à droite avec "${o.pill}". ${rules(o,L)} À droite, le produit de la deuxième image, strictement fidèle (formes, couleurs, détails), parfaitement intégré dans une scène réaliste : contact avec le sol, ombre portée cohérente, lumière et couleurs harmonisées. Les ouvertures blanches du produit sont traversantes : on voit le décor à travers. Pas de boîte, pas de mention recyclé, texte en français sans faute.`)};
window.__heroFix=async(hero,o)=>{const L=logosPart(o,2);
 return send([['hero.png',hero],...L.f],
 `Refais cette bannière à l'identique (même scène, même produit, même mise en page, mêmes textes${o.pill?`, pastille "${o.pill}"`:''}) en changeant uniquement les badges du bas du panneau crème. Garde le badge rond d'âge. ${rules(o,L)} Supprime les anciens badges Anti-UV et Fabriqué en France. Ne modifie pas le produit.`)};
// ---- Version 16/11 (retour client : pictos modifiés par IA, fonctions ajoutées). SEULE fonction ChatGPT autorisée pour un hero.
// __heroDecor(urlPackshot, {scene}) : ChatGPT ne produit QUE la photo de droite (produit dans un décor), sans texte, logo, badge ni panneau.
// La vague, les textes et les logos officiels sont ensuite posés par tools/hero_life.py (image récupérée = "photo" du hero_spec, scale 1, ox 0).
// __hero, __hero2 et __heroFix (bannière complète générée) ne doivent plus être utilisés.
window.__heroDecor=async(prod,o={})=>send([['produit.png',prod]],
 `Crée une photo réaliste au format paysage 970x600 du produit de l'image jointe${o.scene?`, dans ce décor : ${o.scene}`:', dans un décor réaliste adapté à son usage'}. `+
 `RÈGLES STRICTES. 1) Le produit est reproduit à l'identique de l'image jointe : mêmes formes, mêmes couleurs, mêmes proportions, mêmes détails, même nombre d'éléments. N'ajoute, ne retire et ne modifie aucune pièce, aucun accessoire, aucune fonction, aucun autocollant. Ne mets aucun objet qui pourrait passer pour un accessoire du produit. 2) Aucun texte, aucun logo, aucun badge, aucun pictogramme, aucune étiquette, aucun cadre, aucun panneau de couleur, aucune vague : seulement la photo. 3) Aucun enfant ni personnage. 4) Le produit est entier, net, placé dans la moitié droite de l'image ; le tiers gauche ne contient que du décor sans élément important. 5) Produit bien intégré : contact avec le sol, ombre portée cohérente, lumière harmonisée. Les ouvertures du produit sont traversantes, on voit le décor à travers. 6) Pas de boîte, pas d'emballage.`);
})();
