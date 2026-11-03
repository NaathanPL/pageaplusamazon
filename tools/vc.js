// Helpers Vendor Central A+ : coller le contenu du fichier dans un javascript_exec sur l'onglet VC (éditeur ouvert).
window.deep=(sel,root=document)=>{let o=[];const w=r=>{r.querySelectorAll(sel).forEach(e=>o.push(e));r.querySelectorAll('*').forEach(e=>{if(e.shadowRoot)w(e.shadowRoot)})};w(root);return o};
window.__sleep=ms=>new Promise(r=>setTimeout(r,ms));
window.__click=e=>(e.shadowRoot?.querySelector('button')||e).click();
window.__btn=re=>deep('kat-button,button').find(e=>re.test((e.getAttribute('label')||e.textContent||'').trim()));
window.__mods=()=>deep('*').filter(e=>e.childElementCount==0&&/^(Image standard et superposition|En-tête d'image standard|Quatre images|Image gauche|Trois images|Image de l'en-tête|Plusieurs images|Texte standard|Tableau)/.test((e.textContent||'').trim()));
window.__flds=()=>deep('input[type=text],input:not([type]),[contenteditable=true],textarea').filter(e=>{const r=e.getBoundingClientRect();return (r.width>0||r.height>0)&&!e.closest('header')&&!/search|recherche/i.test(e.placeholder||'')});
// ordre logique des champs, attendu 'IIIDIIDIDIDIDIDIIDIDID' (0 nom,1-2 titres hero,3 corps hero,4 titre M2,5..12 sous-titre/corps,13-14 M3,15 titre M4,16..21)
window.__ord=()=>{const sy=scrollY;const hs=__mods().map(e=>e.getBoundingClientRect().top+sy).sort((a,b)=>a-b);
 return __flds().map(e=>{const r=e.getBoundingClientRect(),y=r.top+sy;return{e,m:hs.filter(h=>h<y).length,x:Math.round(r.left/60),y}}).sort((a,b)=>a.m-b.m||(a.m==2||a.m==4?(a.x-b.x||a.y-b.y):a.y-b.y)).map(o=>o.e)};
window.__layout=()=>__ord().map(e=>e.isContentEditable?'D':'I').join('');
window.__dump=()=>__ord().map((e,i)=>i+':'+(e.value||e.innerText||'').trim().slice(0,60));
// titres (inputs) : __titles({0:'...',1:'...'})
window.__titles=T=>{const set=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set,o=__ord();for(const k in T){const e=o[k];set.call(e,T[k]);['input','change'].forEach(t=>e.dispatchEvent(new Event(t,{bubbles:true,composed:true})))}};
// corps (contenteditable) : __f(i) puis action computer type (clavier) ; __ins(i,txt) = essai execCommand (à valider)
window.__f=i=>{const e=__ord()[i];e.scrollIntoView({block:'center'});e.focus();getSelection().selectAllChildren(e);return i};
// __ins : NE PAS UTILISER (casse le module : "Erreur de rendu de l'éditeur"). Corps = __f(i) puis action clavier type.
window.__ins=(i,t)=>{__f(i);document.execCommand('insertText',false,t);return __ord()[i].innerText.trim()==t.trim()};
// supprimer un module par son nom (confirme "Oui")
window.__del=async name=>{const h=__mods().find(e=>e.textContent.trim().startsWith(name));if(!h)return 'absent';h.scrollIntoView({block:'start'});await __sleep(300);const y=h.getBoundingClientRect().top;
 const x=deep('kat-icon').filter(e=>e.getAttribute('name')=='x').sort((a,b)=>Math.abs(a.getBoundingClientRect().top-y)-Math.abs(b.getBoundingClientRect().top-y))[0];(x.closest('button')||x.parentElement).click();await __sleep(1200);
 const b=deep('kat-button').find(e=>(e.getAttribute('label')||e.textContent||'').trim()=='Oui');if(b)__click(b);await __sleep(1500);return 'ok'};
// ajouter un module en fin de page
window.__add=async n=>{scrollTo(0,document.body.scrollHeight);await __sleep(500);const s=deep('span').find(e=>e.textContent.trim()=='Ajouter un module');s.click();await __sleep(1500);
 let h=deep('h6').find(e=>e.textContent.trim()==n);if(!h){s.parentElement.click();await __sleep(1500);h=deep('h6').find(e=>e.textContent.trim()==n)}h.click();await __sleep(1500);return __mods().map(e=>e.textContent.trim())};
window.__draft=async()=>{__click(__btn(/brouillon/i));await __sleep(5000);return deep('kat-alert,[role=alert]').map(a=>(a.getAttribute('description')||a.textContent||'').trim().slice(0,100))};
// UPLOAD (validé 03/11/2026 sur Safran) : drop synthétique dans la modale, sans retirer l'ancienne image, puis "Ajouter".
// __imgBtns() : boutons "Modifier" des images dans l'ordre (0 hero, 1-4 M2, 5 M3, 6-8 M4). __up(i,url) : remplace l'image i.
window.__imgBtns=()=>{const sy=scrollY;return deep('kat-button').filter(e=>(e.getAttribute('label')||e.textContent||'').trim()=='Modifier').map(e=>({e,y:Math.round(e.getBoundingClientRect().top+sy),x:e.getBoundingClientRect().left})).sort((a,b)=>a.y-b.y||a.x-b.x).map(o=>o.e)};
window.__up=async(i,url)=>{const b=__imgBtns()[i];b.scrollIntoView({block:'center'});await __sleep(300);__click(b);await __sleep(1500);
 const f=new File([await (await fetch(url)).blob()],url.split('/').pop(),{type:'image/jpeg'});
 const p=deep('p').find(e=>/Faites glisser/.test(e.textContent));if(!p)return 'pas de zone de dépôt';
 const dt=new DataTransfer();dt.items.add(f);for(const t of ['dragenter','dragover','drop'])p.dispatchEvent(new DragEvent(t,{bubbles:true,cancelable:true,composed:true,dataTransfer:dt}));
 for(let k=0;k<20&&/Chargement/.test(deep('kat-modal').map(m=>m.innerText).join(''));k++)await __sleep(500);await __sleep(800);
 const ok=deep('kat-button').find(e=>(e.getAttribute('label')||e.textContent||'').trim()=='Ajouter'&&e.getBoundingClientRect().width>0);if(!ok)return 'pas de bouton Ajouter';__click(ok);await __sleep(1500);return 'ok '+i};
// Emplacements vides ("Cliquez pour ajouter une image") dans l'ordre ; __upE(url) remplit le premier vide (attend la fin du chargement puis Ajouter).
window.__slots=()=>{const sy=scrollY;return deep('*').filter(e=>e.childElementCount==0&&/Cliquez pour ajouter une image/.test(e.textContent||'')&&e.getBoundingClientRect().width>0).map(e=>({e,y:Math.round(e.getBoundingClientRect().top+sy),x:e.getBoundingClientRect().left})).sort((a,b)=>a.y-b.y||a.x-b.x).map(o=>o.e)};
window.__drop=async(url)=>{const f=new File([await (await fetch(url)).blob()],url.split('/').pop(),{type:'image/jpeg'});
 const p=deep('p').find(e=>/Faites glisser/.test(e.textContent)&&e.getBoundingClientRect().width>0);if(!p)return false;
 const dt=new DataTransfer();dt.items.add(f);for(const t of ['dragenter','dragover','drop'])p.dispatchEvent(new DragEvent(t,{bubbles:true,cancelable:true,composed:true,dataTransfer:dt}));
 for(let k=0;k<40;k++){await __sleep(500);const m=deep('kat-modal').find(m=>m.hasAttribute('visible'));if(!m)return true;if(/Chargement/.test(m.innerText))continue;
  const ok=deep('kat-button').find(e=>/^Ajouter$/.test((e.getAttribute('label')||e.textContent||'').trim())&&e.getBoundingClientRect().width>0);if(ok&&!ok.hasAttribute('disabled')){__click(ok);await __sleep(1200)}}
 return !deep('kat-modal').some(m=>m.hasAttribute('visible'))};
window.__upE=async(url)=>{const s=__slots()[0];if(!s)return 'aucun vide';s.scrollIntoView({block:'center'});await __sleep(300);s.click();await __sleep(1500);return (await __drop(url))?'ok':'MODALE OUVERTE'};
// remplacer l'image d'un emplacement déjà rempli : __upM(i,url) (i = index __imgBtns)
window.__upM=async(i,url)=>{const b=__imgBtns()[i];b.scrollIntoView({block:'center'});await __sleep(300);__click(b);await __sleep(1500);return (await __drop(url))?'ok':'MODALE OUVERTE'};
