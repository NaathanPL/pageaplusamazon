# Hero A+ 970x600, charte figée le 16/11/2026 (validée par Nathan) : photo lifestyle Drive INTACTE (recadrage + réduction seulement) à droite,
# panneau crème à bord net (droit en haut, ondulé ensuite), police Fredoka, titre + sous-titre + badges centrés dans le panneau,
# badges TOUJOURS à la même taille (BADGE), logos officiels collés tels quels, pastille produit en haut à droite.
# Usage : python3 tools/hero_life.py <spec.json>
# spec : {"photo":"life.jpg","out":"hero.jpg","scale":0.47,"ox":null,"oy":-5,"title":["l1","l2"],"sub":["l1","l2"],
#         "age":"3+","unit":"ANS","anti_uv":false,"fab":true,"extra":["SONS","RÉALISTES"],"pill":"Cuisine Romarin"}
# Seuls la photo, son cadrage (scale/ox/oy) et les textes changent d'un produit à l'autre : forme, tailles, couleurs et positions ne se règlent pas par spec.
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy.interpolate import PchipInterpolator
sys.path.insert(0, os.path.dirname(__file__))
from aplus import F
SS = 3; W, H = 970, 600
CREAM = (253, 240, 221); BROWN = (58, 22, 14); GREEN = (46, 85, 65); RED = (232, 66, 70)  # GREEN = vert des bandeaux #2E5541
LOGOS = os.path.join(os.path.dirname(__file__), 'assets', 'logos')
CX = 200; GAP = 14; BADGE = 82; TSIZE = 50; EDGE = [412, 412, 386, 420, 380, 356]

def ctext(d, cx, y, t, f, fill):
    bb = d.textbbox((0, 0), t, font=f); d.text((cx - (bb[2] - bb[0]) / 2 - bb[0], y), t, font=f, fill=fill)
def main(sp_path):
    sp = json.load(open(sp_path)); base = os.path.dirname(os.path.abspath(sp_path)); fade = 0
    p = lambda f: f if os.path.isabs(f) else os.path.join(base, f)
    ph = Image.open(p(sp['photo'])).convert('RGB'); s = sp.get('scale', 0.47)
    ph = ph.resize((round(ph.width * s), round(ph.height * s)), Image.LANCZOS)
    ox = sp.get('ox'); ox = W - ph.width if ox is None else ox
    canvas = Image.new('RGB', (W, H), CREAM); canvas.paste(ph, (ox, sp.get('oy', 0)))
    big = canvas.resize((W * SS, H * SS), Image.LANCZOS).convert('RGBA')
    f = PchipInterpolator([0, 170, 280, 390, 500, 600], EDGE)
    E = f(np.arange(H * SS) / SS); X = np.arange(W * SS)[None, :] / SS
    if fade:
        t = np.clip((X - (E[:, None] - 10)) / fade, 0, 1); a = 1 - t * t * (3 - 2 * t)
        mask = Image.fromarray((a * 255).astype(np.uint8))
    else:
        mask = Image.fromarray(((X < E[:, None]) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5))
    big.paste(Image.new('RGBA', big.size, CREAM + (255,)), (0, 0), mask)
    d = ImageDraw.Draw(big); cx = CX * SS
    ts = TSIZE
    while ts > 28 and max(d.textlength(l, font=F(ts * SS, 700)) for l in sp['title']) > 340 * SS: ts -= 1
    ss_ = round(ts * 0.58)
    while ss_ > 14 and max(d.textlength(l, font=F(ss_ * SS, 600)) for l in sp['sub']) > 320 * SS: ss_ -= 1
    # badges : liste (type, largeur relative)
    items = []
    if sp.get('age'): items.append('age')
    if sp.get('anti_uv'): items.append('uv')
    if sp.get('extra'): items.append('extra')
    fb = None
    if sp.get('fab'):
        fb = Image.open(os.path.join(LOGOS, 'fab_bloc_rvb.png')).convert('RGBA'); fb = fb.crop(fb.getbbox()); items.append('fab')
    rel = lambda k: fb.width / fb.height if k == 'fab' else 1
    Dp = BADGE  # taille fixe, identique quel que soit le nombre de badges
    note = bool(sp.get('anti_uv')); nh = 44 if note else 0
    th = len(sp['title']) * ts * 1.16; sh = len(sp['sub']) * ss_ * 1.32
    free = H - 120 - (th + sh + Dp + nh); g1 = min(44, free * 0.4); g2 = min(64, free * 0.6)
    y = (60 + (free - g1 - g2) / 2) * SS
    for ln in sp['title']: ctext(d, cx, y, ln, F(ts * SS, 700), BROWN); y += ts * 1.16 * SS
    y += g1 * SS
    for ln in sp['sub']: ctext(d, cx, y, ln, F(ss_ * SS, 600), GREEN); y += ss_ * 1.32 * SS
    D = Dp * SS; by = int(y + g2 * SS); tw = sum(rel(k) for k in items) * D + GAP * SS * (len(items) - 1); bx = int(cx - tw / 2)
    for k in items:
        if k == 'age':
            d.ellipse((bx, by, bx + D, by + D), fill=RED)
            f1 = F(D * 0.42, 700); f2 = F(D * 0.19, 700); u = sp.get('unit', 'ANS')
            b1 = d.textbbox((0, 0), sp['age'], font=f1); b2 = d.textbbox((0, 0), u, font=f2); g = D * 0.06
            h = (b1[3] - b1[1]) + g + (b2[3] - b2[1]); y0 = by + (D - h) / 2
            d.text((bx + (D - (b1[2] - b1[0])) / 2 - b1[0], y0 - b1[1]), sp['age'], font=f1, fill='white')
            d.text((bx + (D - (b2[2] - b2[0])) / 2 - b2[0], y0 + (b1[3] - b1[1]) + g - b2[1]), u, font=f2, fill='white')
        elif k == 'uv':
            uv = Image.open(os.path.join(LOGOS, 'logo_anti_uv.png')).convert('RGBA').resize((D, D), Image.LANCZOS)
            big.alpha_composite(uv, (bx, by))
            fa = F(D * 0.2, 700); ab = d.textbbox((0, 0), '*', font=fa)  # astérisque petit, collé en haut à droite du logo
            lb = uv.getchannel('A').point(lambda v: 255 if v > 128 else 0).getbbox()  # cercle visible du logo
            r = (lb[2] - lb[0]) / 2; ccx = bx + (lb[0] + lb[2]) / 2; ccy = by + (lb[1] + lb[3]) / 2; aw = ab[2] - ab[0]; ah = ab[3] - ab[1]
            k = (r + aw * 0.35) * 0.707  # centre de l'astérisque posé contre le bord du cercle, à 45° en haut à droite
            d.text((ccx + k - aw / 2 - ab[0], ccy - k - ah / 2 - ab[1]), '*', font=fa, fill=BROWN)
        elif k == 'extra':
            d.ellipse((bx, by, bx + D, by + D), fill='white', outline=GREEN, width=3 * SS)
            lines = sp['extra']; fsz = int(D * 0.19)
            while fsz > 10 and max(d.textlength(l, font=F(fsz, 700)) for l in lines) > D * 0.80: fsz -= 1
            fe = F(fsz, 700); bbs = [d.textbbox((0, 0), l, font=fe) for l in lines]; lg = D * 0.06
            h = sum(b[3] - b[1] for b in bbs) + lg * (len(lines) - 1); y2 = by + (D - h) / 2
            for ln, b in zip(lines, bbs):
                d.text((bx + (D - (b[2] - b[0])) / 2 - b[0], y2 - b[1]), ln, font=fe, fill=GREEN); y2 += b[3] - b[1] + lg
        elif k == 'fab':
            w_ = round(fb.width * D / fb.height); big.alpha_composite(fb.resize((w_, D), Image.LANCZOS), (bx, by))
        bx += int(rel(k) * D) + GAP * SS
    if note:
        nt = '* ' + sp.get('uv_note', "Résistance équivalente à 3 ans (Dégradation max 3 sur 5 sur l'échelle des gris. Norme D15 1343)")
        fn = F(12 * SS, 600); lines, cur = [], ''
        for w_ in nt.split():
            t_ = (cur + ' ' + w_).strip()
            if d.textlength(t_, font=fn) > 320 * SS and cur: lines.append(cur); cur = w_
            else: cur = t_
        lines.append(cur); y2 = by + D + 10 * SS
        for ln in lines: ctext(d, cx, y2, ln, fn, BROWN); y2 += 16 * SS
    pf = F(26 * SS, 700); bb = d.textbbox((0, 0), sp['pill'], font=pf); pw = bb[2] - bb[0] + 40 * SS; ph_ = 48 * SS
    px = (W - 14) * SS - pw; py = 16 * SS
    d.rounded_rectangle((px, py, px + pw, py + ph_), radius=ph_ // 2, fill=GREEN, outline='white', width=3 * SS)
    d.text((px + 20 * SS - bb[0], py + (ph_ - (bb[3] - bb[1])) / 2 - bb[1]), sp['pill'], font=pf, fill='white')
    big.convert('RGB').resize((W, H), Image.LANCZOS).save(p(sp['out']), quality=95, subsampling=0); print('ok')

main(sys.argv[1])
