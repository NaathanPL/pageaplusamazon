# Lib visuels A+ Smoby. Texte rendu en 4x puis réduit (espacement régulier), JPEG q95 4:4:4.
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, features
LE=ImageFont.Layout.RAQM if features.check('raqm') else ImageFont.Layout.BASIC
FD=os.path.join(os.path.dirname(__file__),'fonts','poppins-latin-%d-normal.woff')
GREEN=(46,85,65); CORAL=(212,91,71); DARK=(59,50,45); BG=(244,239,231); WHITE=(255,255,255); GREY=(120,112,105)
SS=4; O=600  # taille des visuels carrés
def F(s,w=700): return ImageFont.truetype(FD%w,s,layout_engine=LE)
def cover(im,w,h,cx=0.5,cy=0.5):
    s=max(w/im.width,h/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=int((im.width-w)*cx); y=int((im.height-h)*cy); return im.crop((x,y,x+w,y+h))
def fit(im,w,h): im=im.copy(); im.thumbnail((w,h),Image.LANCZOS); return im
def canvas(c=WHITE): return Image.new('RGB',(O,O),c)
def text_hq(w,h,t,size,bg=GREEN,fg=WHITE,weight=700,spacing=4):
    """Bloc texte centré rendu en SSx puis réduit. size/spacing en px finaux."""
    big=Image.new('RGB',(w*SS,h*SS),bg); d=ImageDraw.Draw(big); f=F(size*SS,weight)
    bb=d.multiline_textbbox((0,0),t,font=f,align='center',spacing=spacing*SS)
    d.multiline_text(((big.width-(bb[2]-bb[0]))/2-bb[0],(big.height-(bb[3]-bb[1]))/2-bb[1]),t,font=f,fill=fg,align='center',spacing=spacing*SS)
    return big.resize((w,h),Image.LANCZOS)
def band(im,t,top=False):
    """Bandeau vert : bas 128px (2 lignes max) ou haut 96px."""
    im=im.copy(); h=96 if top else 128
    im.paste(text_hq(O,h,t,38 if top else 36),(0,0 if top else O-h)); return im
def save(im,path): im.convert('RGB').save(path,quality=95,subsampling=0)
def sheet(paths,out):
    sh=Image.new('RGB',(1240,620),'white')
    for i,p in enumerate(paths): sh.paste(Image.open(p).resize((300,300),Image.LANCZOS),((i%4)*310,(i//4)*310))
    sh.save(out,quality=80)
