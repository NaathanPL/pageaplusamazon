// Conversion des puces tapées "•" en vraie liste à puces (éditeur A+ Vendor Central, Draft.js)
// Usage : __bulInfo() -> [{i, n}] éditeurs avec lignes "•" ; __bsel(i) sélectionne les blocs "•" et renvoie
// les coordonnées (repère capture 800 px) du bouton liste à puces à cliquer ; __car(i) place le curseur
// avant le premier "•" restant ; puis touches "Delete Delete" + (n-1) x "Down Home Delete Delete".
(() => {
  const eds = () => [...document.querySelectorAll('[contenteditable=true]')];
  const first = n => document.createTreeWalker(n, NodeFilter.SHOW_TEXT).nextNode();
  const last = n => { const w = document.createTreeWalker(n, NodeFilter.SHOW_TEXT); let t, l; while (t = w.nextNode()) l = t; return l; };
  const sel = r => { const s = getSelection(); s.removeAllRanges(); s.addRange(r); };
  const isB = b => b.innerText.trim().startsWith('•');
  window.__bulInfo = () => eds().map((e, i) => ({ i, n: [...e.querySelectorAll('[data-block]')].filter(isB).length })).filter(x => x.n);
  window.__bsel = i => {
    const e = eds()[i], bl = [...e.querySelectorAll('[data-block]')], b0 = bl.findIndex(isB);
    let b1 = b0; while (b1 + 1 < bl.length && isB(bl[b1 + 1])) b1++;
    e.scrollIntoView({ block: 'center' }); e.focus();
    const r = document.createRange(); r.setStart(first(bl[b0]), 0); const L = last(bl[b1]); r.setEnd(L, L.length); sel(r);
    let p = e, b; while (p && (b = [...p.querySelectorAll('div.css-7qjrqi')].filter(x => !e.contains(x))).length < 6) p = p.parentElement;
    const q = b[4].getBoundingClientRect(), k = 800 / innerWidth;
    return { x: Math.round((q.x + q.width / 2) * k), y: Math.round((q.y + q.height / 2) * k), n: b1 - b0 + 1 };
  };
  window.__car = i => {
    const e = eds()[i], li = [...e.querySelectorAll('li')].find(isB); if (!li) return 'fini';
    const t = first(li); e.focus(); const r = document.createRange(); r.setStart(t, t.data.indexOf('•')); r.collapse(true); sel(r);
    return [...e.querySelectorAll('li')].filter(isB).length;
  };
})();
