# Hero A+ 970x600 : photo lifestyle Drive INTACTE (recadrage + réduction seulement) à droite, panneau crème ondulé à gauche,
# titre, sous-titre, badges (âge, Anti-UV, pastille libre), logo Fabriqué en France officiel, étiquette produit.
# Usage : python3 tools/hero_life.py <spec.json>
# spec : {"photo":"life.jpg","out":"hero.jpg","scale":0.47,"ox":null,"oy":-5,"title":["l1","l2","l3"],"sub":["l1","l2"],
#         "age":"3+","unit":"ANS","anti_uv":false,"fab":true,"extra":["SONS","RÉALISTES"],"pill":"Cuisine Romarin","tsize":46}
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy.interpolate import PchipInterpolator
sys.path.insert(0, os.path.dirname(__file__))
from aplus import F
SS = 3; W, H = 970, 600
CREAM = (253, 240, 221); BROWN = (58, 22, 14); GREEN = (62, 98, 58); RED = (232, 66, 70); PILL = (46, 85, 65)
LOGOS = os.path.join(os.path.dirname(__file__), 'assets', 'logos')

def main(sp_path):
    sp = json.load(open(sp_path)); base = os.path.dirname(os.path.abspath(sp_path))
    p = lambda f: f if os.path.isabs(f) else os.path.join(base, f)
    # photo à droite, intacte
    ph = Image.open(p(sp['photo'])).convert('RGB'); s = sp.get('scale', 0.47)
    ph = ph.resize((round(ph.width * s), round(ph.height * s)), Image.LANCZOS)
    ox = sp.get('ox'); ox = W - ph.width if ox is None else ox
    canvas = Image.new('RGB', (W, H), CREAM); canvas.paste(ph, (ox, sp.get('oy', 0)))
    # panneau crème ondulé (haute résolution)
    f = PchipInterpolator([0, 150, 300, 420, 490, 560, 600], sp.get('edge', [415, 410, 408, 402, 392, 352, 332]))
    mask = np.zeros((H * SS, W * SS), np.uint8)
    for y in range(H * SS): mask[y, :int(f(y / SS) * SS)] = 255
    mask = Image.fromarray(mask).filter(ImageFilter.GaussianBlur(1.5)).resize((W * SS, H * SS))
    big = canvas.resize((W * SS, H * SS), Image.LANCZOS).convert('RGBA')
    big.paste(Image.new('RGBA', big.size, CREAM + (255,)), (0, 0), mask)
    d = ImageDraw.Draw(big)
    # titre + sous-titre
    ts = sp.get('tsize', 46); x = 24 * SS; y = 70 * SS
    while ts > 28 and max(d.textlength(l, font=F(ts * SS, 700)) for l in sp['title']) > 372 * SS: ts -= 1
    ft = F(ts * SS, 700)
    while ts > 20 and max(d.textlength(l, font=F(int(ts * 0.56) * SS, 600)) for l in sp['sub']) > 372 * SS: ts -= 1
    for ln in sp['title']:
        d.text((x, y), ln, font=ft, fill=BROWN); y += int(ts * 1.2 * SS)
    y += 14 * SS; fs = F(int(ts * 0.56) * SS, 600)
    for ln in sp['sub']:
        d.text((x, y), ln, font=fs, fill=GREEN); y += int(ts * 0.74 * SS)
    # badges
    D = 118 * SS; by = max(y + 22 * SS, 366 * SS); bx = 12 * SS
    if sp.get('age'):
        d.ellipse((bx, by, bx + D, by + D), fill=RED)
        f1 = F(int(D * 0.40), 700); f2 = F(int(D * 0.22), 700)
        bb = d.textbbox((0, 0), sp['age'], font=f1); d.text((bx + (D - bb[2] + bb[0]) / 2 - bb[0], by + D * 0.15), sp['age'], font=f1, fill='white')
        u = sp.get('unit', 'ANS'); bb = d.textbbox((0, 0), u, font=f2); d.text((bx + (D - bb[2] + bb[0]) / 2 - bb[0], by + D * 0.60), u, font=f2, fill='white')
        bx += D + 14 * SS
    if sp.get('anti_uv'):
        uv = Image.open(os.path.join(LOGOS, 'logo_anti_uv.png')).convert('RGBA').resize((D, D), Image.LANCZOS)
        big.alpha_composite(uv, (bx, by)); d.text((bx + D - 6 * SS, by - 10 * SS), '*', font=F(int(D * 0.4), 800), fill=BROWN)
        bx += D + 14 * SS
    if sp.get('extra'):
        d.ellipse((bx, by, bx + D, by + D), fill='white', outline=GREEN, width=3 * SS)
        fe = F(int(D * 0.19), 700); lines = sp['extra']; tot = len(lines) * int(D * 0.24)
        yy = by + (D - tot) / 2
        for ln in lines:
            bb = d.textbbox((0, 0), ln, font=fe); d.text((bx + (D - bb[2] + bb[0]) / 2 - bb[0], yy), ln, font=fe, fill=GREEN); yy += int(D * 0.24)
        bx += D + 14 * SS
    if sp.get('fab'):
        fb = Image.open(os.path.join(LOGOS, 'fab_bloc_rvb.png')).convert('RGBA'); fb = fb.crop(fb.getbbox())
        fh = int(D * 1.0); fb = fb.resize((round(fb.width * fh / fb.height), fh), Image.LANCZOS); big.alpha_composite(fb, (bx, by + int(D * 0.0)))
    # étiquette produit en haut à droite
    pf = F(26 * SS, 700); bb = d.textbbox((0, 0), sp['pill'], font=pf); pw = bb[2] - bb[0] + 36 * SS; ph_ = 46 * SS
    px = (W - 12) * SS - pw; py = 14 * SS
    d.rounded_rectangle((px, py, px + pw, py + ph_), radius=ph_ // 2, fill=PILL, outline='white', width=3 * SS)
    d.text((px + 18 * SS - bb[0], py + (ph_ - (bb[3] - bb[1])) / 2 - bb[1]), sp['pill'], font=pf, fill='white')
    big.convert('RGB').resize((W, H), Image.LANCZOS).save(p(sp['out']), quality=95, subsampling=0); print('ok')

main(sys.argv[1])
