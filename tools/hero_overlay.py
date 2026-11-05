# Pose les badges officiels sur un hero généré par ChatGPT (zone badges laissée vide).
# Usage : python3 tools/hero_overlay.py <spec.json>
# spec : {"src":"gpt_hero.jpg","out":"hero.jpg","age":"2+","anti_uv":true,"fab":"light"|"cartouche"|null,"footnote":"...","y":420,"x":22,"d":80,"foot_y":545,"foot_w":36}
import json, os, sys, textwrap
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from aplus import F
SS = 3; W, H = 970, 600
CORAL = (212, 91, 71); BROWN = (84, 54, 38)
LOGOS = os.path.join(os.path.dirname(__file__), 'assets', 'logos')
sp = json.load(open(sys.argv[1])); base = os.path.dirname(os.path.abspath(sys.argv[1]))
p = lambda f: f if os.path.isabs(f) else os.path.join(base, f)
img = Image.open(p(sp['src'])).convert('RGB').resize((W * SS, H * SS), Image.LANCZOS).convert('RGBA')
d = ImageDraw.Draw(img); D = sp.get('d', 80) * SS; x = sp.get('x', 22) * SS; y = sp.get('y', 420) * SS; gap = 10 * SS
d.ellipse((x, y, x + D, y + D), fill=CORAL)
a = sp.get('age', '2+'); f1 = F(int(D * 0.38), 800); f2 = F(int(D * 0.21), 700)
bb = d.textbbox((0, 0), a, font=f1); d.text((x + (D - (bb[2] - bb[0])) / 2 - bb[0], y + D * 0.12), a, font=f1, fill='white')
bb = d.textbbox((0, 0), 'ANS', font=f2); d.text((x + (D - (bb[2] - bb[0])) / 2 - bb[0], y + D * 0.58), 'ANS', font=f2, fill='white')
x += D + gap
if sp.get('anti_uv'):
    uv = Image.open(os.path.join(LOGOS, 'logo_anti_uv.png')).convert('RGBA').resize((D, D), Image.LANCZOS); img.alpha_composite(uv, (x, y))
    d.text((x + D - 2 * SS, y - 8 * SS), '*', font=F(int(D * 0.4), 800), fill=BROWN); x += D + gap
if sp.get('fab'):
    fn = 'fab_bloc_rvb.png' if sp['fab'] == 'light' else 'fab_bloc_cartouche_rvb.jpg'
    fb = Image.open(os.path.join(LOGOS, fn)).convert('RGBA'); fh = int(D * 1.3)
    fb = fb.resize((round(fb.width * fh / fb.height), fh), Image.LANCZOS); img.alpha_composite(fb, (x, y - int(D * 0.15)))
if sp.get('footnote'):
    for k, ln in enumerate(textwrap.wrap('* ' + sp['footnote'], sp.get('foot_w', 36))):
        d.text((sp.get('x', 22) * SS, (sp.get('foot_y', 545) + k * 12) * SS), ln, font=F(9 * SS, 600), fill=BROWN)
img.convert('RGB').resize((W, H), Image.LANCZOS).save(p(sp['out']), quality=95, subsampling=0); print('ok')
