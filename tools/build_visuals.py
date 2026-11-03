# Usage: python3 tools/build_visuals.py asins/<ASIN>_<Produit>  (lit spec.json, écrit aplus/02..09 + preview.jpg)
import sys,json,os,shutil
sys.path.insert(0,os.path.dirname(__file__)); from aplus import *
D=sys.argv[1]; S=json.load(open(f'{D}/spec.json')); A=S['asin']; OUTD=f'{D}/aplus'; os.makedirs(OUTD,exist_ok=True)
def src(k): return Image.open(os.path.join(S['drive_dir'],S['files'][k])).convert('RGB')
def crop(k,c): im=src(k); return im.crop(tuple(c)) if c else im
def out(n): return f'{OUTD}/{A}_{n}.jpg'
for i,z in enumerate(S['zooms']):  # 4 zooms photo + bandeau bas
    save(band(cover(crop(z['src'],z.get('crop')),O,O,*z.get('c',(0.5,0.5))),z['text']),out(f"0{i+2}_Zoom{i+1}"))
im=canvas(); p=fit(src(S['packshot']),580,580); im.paste(p,((O-p.width)//2,(O-p.height)//2)); save(im,out('06_Reassurance'))
for n,key in (('07_Dimensions','dims'),('08_'+S['feature'].get('name','Feature'),'feature'),('09_ContenuPack','contents')):
    z=S[key]; im=canvas(); c=crop(z['src'],z.get('crop'))
    p=cover(c,O,504,*z.get('c',(0.5,0.5))) if z.get('fill') else fit(c,592,496)
    im.paste(p,((O-p.width)//2,96+(504-p.height)//2)); save(band(im,z['text'],True),out(n))
if os.path.exists(f'{D}/hero.jpg'): shutil.copy(f'{D}/hero.jpg',out('01_Hero'))
sheet(sorted(f'{OUTD}/{f}' for f in os.listdir(OUTD) if 'Hero' not in f),f'{D}/preview.jpg')
