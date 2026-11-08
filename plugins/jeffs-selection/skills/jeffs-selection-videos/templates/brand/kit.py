# 姐夫嚴選 brand video kit — shared opening/cover frame for 3 series (開箱 / 團購 / 探店)
import sys;sys.path.insert(0,"__ROOT__/goose")
from sty import *
import sty
def SANS(w,size):return sty._f(FX+f"{w}/NotoSansTC_{w}.ttf",size)     # 500Medium 700Bold 900Black
CREAM=(250,246,240);INK=(46,34,26);MUTE=(120,104,92)
SERIES={"開箱":dict(name="姐夫開箱",col=(166,110,66),icon="box"),
        "團購":dict(name="姐夫團購",col=(190,58,42),icon="tag"),
        "探店":dict(name="姐夫探店",col=(52,94,72),icon="pin")}
BX0,BX1,BY0,BY1=56,944,1080,1480        # title card (inside IG/TikTok 3:4 grid crop y240-1680 and clear of side buttons)
def icon(kind,s,col):
    k=4;S=s*k;im=blank(S,S);d=ImageDraw.Draw(im);w=int(S*0.09)
    if kind=="pin":
        d.ellipse((S*.2,S*.06,S*.8,S*.66),outline=col,width=w);d.polygon([(S*.28,S*.52),(S*.72,S*.52),(S*.5,S*.95)],fill=col);d.ellipse((S*.2+w,S*.06+w,S*.8-w,S*.66-w),fill=(0,0,0,0))
        d.ellipse((S*.4,S*.26,S*.6,S*.46),fill=col)
    elif kind=="box":
        d.polygon([(S*.5,S*.1),(S*.92,S*.3),(S*.5,S*.5),(S*.08,S*.3)],outline=col,width=w);d.line([(S*.08,S*.3),(S*.08,S*.74),(S*.5,S*.94),(S*.92,S*.74),(S*.92,S*.3)],fill=col,width=w,joint="curve");d.line([(S*.5,S*.5),(S*.5,S*.94)],fill=col,width=w)
    elif kind=="tag":
        d.polygon([(S*.1,S*.12),(S*.56,S*.12),(S*.92,S*.5),(S*.56,S*.88),(S*.1,S*.88)],outline=col,width=w);d.ellipse((S*.24,S*.4,S*.4,S*.56),fill=col)
    return im.resize((s,s),Image.LANCZOS)
def tag(series,size=42):
    c=SERIES[series];f=SANS("900Black",size);tw=f.getlength(c["name"]);h=int(size*1.8);ic=icon(c["icon"],int(size*0.95),CREAM+(255,))
    w=int(size*0.7+ic.size[0]+size*0.35+tw+size*0.8);im=blank(w+24,h+24);d=ImageDraw.Draw(im)
    d.rounded_rectangle((12,12,w+12,h+12),radius=h//2,fill=c["col"]+(255,));im.alpha_composite(ic,(12+int(size*0.7),12+(h-ic.size[1])//2))
    d.text((12+size*0.7+ic.size[0]+size*0.35,12+h/2+1),c["name"],font=f,fill=CREAM+(255,),anchor="lm");return shadow(im,8,(0,4),0.3)
def sticker(l1,l2,col,d=250,rot=10):
    k=3;D=d*k;im=blank(D,D);dr=ImageDraw.Draw(im);dr.ellipse((0,0,D-1,D-1),fill=col+(255,));m=int(D*.06);dr.ellipse((m,m,D-m,D-m),outline=CREAM+(255,),width=3*k)
    dr.text((D/2,D*.38),l1,font=SANS("900Black",int(D*.2)),fill=CREAM+(255,),anchor="mm");dr.text((D/2,D*.64),l2,font=SANS("900Black",int(D*.2)),fill=(255,226,140,255),anchor="mm")
    im=im.resize((d,d),Image.LANCZOS).rotate(rot,resample=Image.BICUBIC,expand=True);return shadow(im,10,(0,8),0.4)
BUG=logo_card(150)
BADGE_S=badge(160,-8)
def grade(img):
    a=np.asarray(img.convert("RGB")).astype(np.float32);a=a*np.array([1.03,1.0,0.95])+np.array([4,2,-2]);return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
def card(series,title,sub,k=2):
    """the shared title card (cream panel + series tag + serif title + sub + brand badge)"""
    c=SERIES[series];W,H=BX1-BX0,BY1-BY0;im=blank((W+80)*k,(H+120)*k);d=ImageDraw.Draw(im);o=40*k;t=60*k
    d.rounded_rectangle((o,t,o+W*k,t+H*k),radius=30*k,fill=CREAM+(250,));d.rounded_rectangle((o+12*k,t+12*k,o+(W-12)*k,t+(H-12)*k),radius=22*k,outline=c["col"]+(255,),width=2*k)
    lines=title.split("\n");fs=120 if len(lines)==1 else 100;f=SERIF("900Black",fs*k)
    while max(f.getlength(L) for L in lines)>(W-90)*k:fs-=4;f=SERIF("900Black",fs*k)
    ys=[0.43] if len(lines)==1 else [0.30,0.58]
    for L,yy in zip(lines,ys):d.text((o+44*k,t+H*yy*k),L,font=f,fill=INK+(255,),anchor="lm")
    fs2=SANS("700Bold",40*k);x=o+46*k;yy=t+H*0.82*k
    if c["icon"]=="pin":ic=icon("pin",int(40*k),c["col"]+(255,));im.alpha_composite(ic,(int(x),int(yy-ic.size[1]/2)));x+=ic.size[0]+8*k
    d.text((x,yy),sub,font=fs2,fill=c["col"]+(255,),anchor="lm")
    im=im.resize((im.size[0]//k,im.size[1]//k),Image.LANCZOS);return shadow(im,16,(0,10),0.35)
def cover(series,hero,title,sub,extra=None,u=None):
    """full 1080x1920 opening frame / platform cover. u=None → static cover"""
    base=grade(hero).convert("RGBA")
    g=np.clip((np.arange(OH)-900)/1020,0,1)[:,None]*np.ones((1,OW));sh=Image.new("RGBA",(OW,OH),(30,18,10,0));sh.putalpha(Image.fromarray((g*150).astype(np.uint8)));base.alpha_composite(sh)
    paste(base,BUG,20,18)
    if extra:put(base,extra[0],extra[1],extra[2])
    cd=card(series,title,sub);paste(base,cd,BX0-40-16,BY0-60-16)
    tg=tag(series);paste(base,tg,BX0+18,BY0-tg.size[1]/2)
    put(base,BADGE_S,BX1-74,BY0+6)
    return base
def herofrom(path,t=None,cx=0.5,cy=0.5,zoom=1.0):
    if t is None:img=Image.open(path).convert("RGB")
    else:
        raw=subprocess.run(["ffmpeg","-v","error","-ss",str(t),"-i",path,"-frames:v","1","-f","image2pipe","-vcodec","png","-"],capture_output=True).stdout
        import io;img=Image.open(io.BytesIO(raw)).convert("RGB")
    s=max(OW/img.size[0],OH/img.size[1])*zoom;w,h=OW/s,OH/s;x0=(img.size[0]-w)*cx;y0=(img.size[1]-h)*cy
    return img.resize((OW,OH),Image.LANCZOS,box=(x0,y0,x0+w,y0+h))
