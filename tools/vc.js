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
window.__ins=(i,t)=>{__f(i);document.execCommand('insertText',false,t);return __ord()[i].innerText.trim()==t.trim()};
// supprimer un module par son nom (confirme "Oui")
window.__del=async name=>{const h=__mods().find(e=>e.textContent.trim().startsWith(name));if(!h)return 'absent';h.scrollIntoView({block:'start'});await __sleep(300);const y=h.getBoundingClientRect().top;
 const x=deep('kat-icon').filter(e=>e.getAttribute('name')=='x').sort((a,b)=>Math.abs(a.getBoundingClientRect().top-y)-Math.abs(b.getBoundingClientRect().top-y))[0];(x.closest('button')||x.parentElement).click();await __sleep(1200);
 const b=deep('kat-button').find(e=>(e.getAttribute('label')||e.textContent||'').trim()=='Oui');if(b)__click(b);await __sleep(1500);return 'ok'};
// ajouter un module en fin de page
window.__add=async n=>{scrollTo(0,document.body.scrollHeight);await __sleep(500);const s=deep('span').find(e=>e.textContent.trim()=='Ajouter un module');s.click();await __sleep(1500);
 let h=deep('h6').find(e=>e.textContent.trim()==n);if(!h){s.parentElement.click();await __sleep(1500);h=deep('h6').find(e=>e.textContent.trim()==n)}h.click();await __sleep(1500);return __mods().map(e=>e.textContent.trim())};
window.__draft=async()=>{__click(__btn(/brouillon/i));await __sleep(5000);return deep('kat-alert,[role=alert]').map(a=>(a.getAttribute('description')||a.textContent||'').trim().slice(0,100))};
// NON TESTÉ : charger une image depuis une URL (repo GitHub raw) dans un input file visible (après ouverture du dialogue d'upload)
window.__upload=async(url,name)=>{const b=await (await fetch(url)).blob();const f=new File([b],name||url.split('/').pop(),{type:b.type||'image/jpeg'});
 const inp=deep('input[type=file]');if(!inp.length)return 'pas d input file';const dt=new DataTransfer();dt.items.add(f);const i=inp[inp.length-1];i.files=dt.files;
 i.dispatchEvent(new Event('change',{bubbles:true,composed:true}));return 'ok '+f.size+' '+inp.length+' inputs'};
