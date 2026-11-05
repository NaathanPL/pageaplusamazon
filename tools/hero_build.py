# Hero A+ 970x600 monté localement : décor (sans produit) + vrai packshot détouré + panneau texte + logos officiels.
# Usage : python3 tools/hero_build.py <spec.json>
# spec : {"decor":"decor.jpg","pack":"pack_cut.png","out":"hero.jpg","title":"...","subtitle":"...","age":"2+","pill":"Maison Aventure",
#         "anti_uv":true,"fab":"light"|"cartouche"|null,"footnote":"...","pack_box":[x0,y0,x1,y1]}
import json, os, sys
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from aplus import F, GREEN
SS = 3
W, H = 970, 600
CREAM = (246, 238, 224); BROWN = (84, 54, 38); OLIVE = (96, 128, 52); CORAL = (212, 91, 71)
LOGOS = os.path.join(os.path.dirname(__file__), 'assets', 'logos')

def cover(im, w, h):
    s = max(w / im.width, h / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - w) // 2; y = (im.height - h) // 2; return im.crop((x, y, x + w, y + h))

def trim(im):
    a = im.getchannel('A').point(lambda v: 255 if v > 128 else 0)
    return im.crop(a.getbbox())

def main(spec_path):
    sp = json.load(open(spec_path)); base = os.path.dirname(os.path.abspath(spec_path))
    p = lambda f: f if os.path.isabs(f) else os.path.join(base, f)
    w, h = W * SS, H * SS
    img = cover(Image.open(p(sp['decor'])).convert('RGB'), w, h).convert('RGBA')
    # profondeur : léger flou du décor (le produit reste net)
    img = Image.alpha_composite(img.filter(ImageFilter.GaussianBlur(1.6 * SS)).convert('RGBA'), Image.new('RGBA', img.size, (255, 236, 200, 22)))
    decor_sharp = cover(Image.open(p(sp['decor'])).convert('RGB'), w, h).convert('RGBA')
    # produit réel, proportions d'origine
    pk = trim(Image.open(p(sp['pack'])).convert('RGBA'))
    x0, y0, x1, y1 = [v * SS for v in sp.get('pack_box', [405, 62, 945, 560])]
    s = min((x1 - x0) / pk.width, (y1 - y0) / pk.height)
    pk = pk.resize((round(pk.width * s), round(pk.height * s)), Image.LANCZOS)
    # contour adouci + éclairage chaud, contraste légèrement réduit pour se fondre dans la scène
    al = pk.getchannel('A').filter(ImageFilter.GaussianBlur(0.7 * SS)); pk.putalpha(al)
    import numpy as np
    arr = np.array(pk).astype(float)
    arr[..., :3] = (arr[..., :3] - 128) * 0.93 + 128
    arr[..., 0] *= 1.02; arr[..., 1] *= 0.985; arr[..., 2] *= 0.93
    gy = np.linspace(1.04, 0.90, arr.shape[0])[:, None]  # haut éclairé, bas plus sombre
    arr[..., :3] *= gy[..., None]
    pk = Image.fromarray(np.clip(arr, 0, 255).astype('uint8'), 'RGBA')
    px = x0 + ((x1 - x0) - pk.width) // 2; py = y1 - pk.height
    # ombre portée (soleil en haut à gauche) + ombre de contact
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
    d.polygon([(px + pk.width * 0.05, py + pk.height - 6 * SS), (px + pk.width * 1.02, py + pk.height - 6 * SS),
               (px + pk.width * 1.16, py + pk.height + 16 * SS), (px + pk.width * 0.20, py + pk.height + 22 * SS)], fill=(15, 28, 8, 120))
    sh = sh.filter(ImageFilter.GaussianBlur(9 * SS)); img.alpha_composite(sh)
    sh2 = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(sh2)
    d.ellipse((px + pk.width * 0.03, py + pk.height - 8 * SS, px + pk.width * 1.0, py + pk.height + 9 * SS), fill=(10, 20, 5, 190))
    img.alpha_composite(sh2.filter(ImageFilter.GaussianBlur(3.5 * SS)))
    img.alpha_composite(pk, (px, py))
    # herbe devant la base du produit (touffes tirées du décor net)
    rng = np.random.default_rng(7); band = 20 * SS; yb = py + pk.height
    m = np.zeros((h, w), float)
    cols = rng.random(w); cols = np.convolve(cols, np.ones(5 * SS) / (5 * SS), mode='same')
    for xx in range(px, min(px + pk.width, w)):
        hh = int(band * (0.25 + 1.1 * cols[xx]))
        m[max(yb - hh, 0):yb + 2 * SS, xx] = np.linspace(0.0, 1.0, min(hh, yb) + 2 * SS)[:m[max(yb - hh, 0):yb + 2 * SS, xx].shape[0]]
    m = np.array(Image.fromarray((m * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.8 * SS))) / 255.0
    grass = decor_sharp.copy(); gm = np.array(grass).astype(float)
    gm[..., :3] *= 0.92; grass = Image.fromarray(np.clip(gm, 0, 255).astype('uint8'), 'RGBA')
    grass.putalpha(Image.fromarray((m * 255).astype('uint8'))); img.alpha_composite(grass)
    # panneau crème, bord en vague
    pan = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(pan)
    import math
    edge = 414 * SS; pts = [(0, 0)]
    for yy in range(0, h + 1, 4):
        pts.append((edge + math.sin(yy / (h / 2.0) * math.pi) * 16 * SS - 8 * SS, yy))
    pts.append((0, h)); d.polygon(pts, fill=CREAM + (255,)); img.alpha_composite(pan)
    d = ImageDraw.Draw(img)
    # textes
    ft = F(43 * SS, 800); y = 46 * SS
    for line in sp['title'].split('\n'):
        d.text((26 * SS, y), line, font=ft, fill=BROWN); y += 51 * SS
    fs = F(25 * SS, 700); y += 12 * SS
    for line in sp['subtitle'].split('\n'):
        d.text((26 * SS, y), line, font=fs, fill=OLIVE); y += 33 * SS
    # badges
    by = 392 * SS; bx = 26 * SS; D = 104 * SS
    d.ellipse((bx, by, bx + D, by + D), fill=CORAL)
    f1 = F(40 * SS, 800); f2 = F(22 * SS, 700); a = sp.get('age', '2+')
    bb = d.textbbox((0, 0), a, font=f1); d.text((bx + (D - (bb[2] - bb[0])) / 2 - bb[0], by + 14 * SS), a, font=f1, fill='white')
    bb = d.textbbox((0, 0), 'ANS', font=f2); d.text((bx + (D - (bb[2] - bb[0])) / 2 - bb[0], by + 58 * SS), 'ANS', font=f2, fill='white')
    bx += D + 14 * SS
    if sp.get('anti_uv'):
        uv = Image.open(os.path.join(LOGOS, 'logo_anti_uv.png')).convert('RGBA').resize((D, D), Image.LANCZOS)
        img.alpha_composite(uv, (bx, by))
        d.text((bx + D - 4 * SS, by - 6 * SS), '*', font=F(34 * SS, 800), fill=BROWN)
        bx += D + 14 * SS
    if sp.get('fab'):
        fn = 'fab_bloc_rvb.png' if sp['fab'] == 'light' else 'fab_bloc_cartouche_rvb.jpg'
        fb = Image.open(os.path.join(LOGOS, fn)).convert('RGBA'); fh = 132 * SS
        fb = fb.resize((round(fb.width * fh / fb.height), fh), Image.LANCZOS); img.alpha_composite(fb, (bx, by - 14 * SS))
    if sp.get('footnote'):
        import textwrap
        for k, ln in enumerate(textwrap.wrap('* ' + sp['footnote'], 62)):
            d.text((26 * SS, (552 + k * 12) * SS), ln, font=F(9 * SS, 600), fill=BROWN)
    # pastille nom produit
    fp = F(24 * SS, 700); bb = d.textbbox((0, 0), sp['pill'], font=fp); tw = bb[2] - bb[0]
    pw = tw + 44 * SS; ph = 48 * SS; px0 = w - pw - 16 * SS; py0 = 14 * SS
    d.rounded_rectangle((px0, py0, px0 + pw, py0 + ph), radius=ph // 2, fill=GREEN)
    d.text((px0 + 22 * SS - bb[0], py0 + (ph - (bb[3] - bb[1])) / 2 - bb[1]), sp['pill'], font=fp, fill='white')
    out = img.convert('RGB').resize((W, H), Image.LANCZOS); out.save(p(sp['out']), quality=95, subsampling=0)
    print('ok', p(sp['out']))

if __name__ == '__main__':
    main(sys.argv[1])
