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
  // Bloc unique "• a • b • c" : passer le bloc en liste (sélection du champ + bouton), puis __sep(i) sélectionne
  // le dernier séparateur " • " ; touche Return ; répéter jusqu'à 0 ; finir par __car(i) + "Delete Delete".
  window.__sep = i => {
    const e = eds()[i], w = document.createTreeWalker(e, NodeFilter.SHOW_TEXT), ts = []; let t; while (t = w.nextNode()) ts.push(t);
    for (let j = ts.length - 1; j >= 0; j--) { const k = ts[j].data.lastIndexOf(' • '); if (k >= 0) { e.focus(); const r = document.createRange(); r.setStart(ts[j], k); r.setEnd(ts[j], k + 3); sel(r); return (e.textContent.match(/ • /g) || []).length; } }
    return 0;
  };
  window.__selAll = i => {
    const e = eds()[i]; e.scrollIntoView({ block: 'center' }); e.focus(); getSelection().selectAllChildren(e);
    let p = e, b; while (p && (b = [...p.querySelectorAll('div.css-7qjrqi')].filter(x => !e.contains(x))).length < 6) p = p.parentElement;
    const q = b[4].getBoundingClientRect(), k = 800 / innerWidth;
    return { x: Math.round((q.x + q.width / 2) * k), y: Math.round((q.y + q.height / 2) * k) };
  };
  window.__show = () => eds().map((e, i) => [i, e]).filter(([, e]) => /•/.test(e.innerText)).map(([i, e]) => i + ': ' + [...e.querySelectorAll('[data-block]')].map(b => (b.closest('li') ? 'LI ' : 'P ') + b.innerText.slice(0, 40) + '…' + b.innerText.length).join(' | '));
  window.__car = i => {
    const e = eds()[i], li = [...e.querySelectorAll('li')].find(isB); if (!li) return 'fini';
    const t = first(li); e.focus(); const r = document.createRange(); r.setStart(t, t.data.indexOf('•')); r.collapse(true); sel(r);
    return [...e.querySelectorAll('li')].filter(isB).length;
  };
})();
