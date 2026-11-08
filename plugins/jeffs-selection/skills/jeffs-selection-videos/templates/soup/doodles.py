# cartoon ingredient doodles (thick ink outline, flat colours — same family as the 牛肉爐 doodles) + the round 姐夫嚴選 mark
import sys,math,random
SP="__ROOT__/"
sys.path.insert(0,SP+"eng");sys.path.insert(0,SP+"brand")
from eng import *
import kit5
K=3
def _cv(D=200):return blank(D*K,D*K)
def _fin(im,S,sh=True):
    im=im.resize((S,S),Image.LANCZOS)
    if not sh:return im
    a=im.getchannel("A");s=Image.new("RGBA",im.size,(20,8,0,0));s.putalpha(a.filter(ImageFilter.GaussianBlur(6)).point(lambda v:int(v*0.45)))
    out=blank(S+20,S+20);out.alpha_composite(s,(10,16));out.alpha_composite(im,(10,10));return out
OL=7  # outline width at 1x
def P(x,y):return (x*K,y*K)
def onion(S=200):
    im=_cv(200);d=ImageDraw.Draw(im);w=OL*K
    d.polygon([P(100,22),P(88,52),P(112,52)],fill=(150,196,92,255),outline=INK+(255,),width=w)      # sprout
    d.ellipse(P(38,48)+P(162,178),fill=(244,222,236,255),outline=INK+(255,),width=w)
    d.polygon([P(70,62),P(100,38),P(130,62)],fill=(244,222,236,255))
    d.line([P(70,64),P(100,38),P(130,64)],fill=INK+(255,),width=w,joint="curve")
    for x0,x1 in ((72,82),(118,128)):d.arc(P(x0-30,62)+P(x1+30,172),100 if x0<100 else 20,160 if x0<100 else 80,fill=(196,140,186,255),width=int(5*K))
    d.arc(P(84,60)+P(116,176),70,110,fill=(196,140,186,255),width=int(5*K))
    for dx in (-12,0,12):d.line([P(100+dx,176),P(100+dx*1.4,192)],fill=INK+(255,),width=int(5*K))
    d.ellipse(P(60,82)+P(78,104),fill=(255,255,255,200));return _fin(im,S)
def cabbage(S=200):
    im=_cv(200);d=ImageDraw.Draw(im);w=OL*K
    d.rounded_rectangle(P(62,70)+P(138,190),radius=30*K,fill=(250,248,228,255),outline=INK+(255,),width=w)
    pts=[P(46,96),P(40,64),P(58,40),P(80,30),P(100,18),P(122,28),P(144,40),P(160,64),P(154,96),P(132,108),P(100,112),P(68,108)]
    d.polygon(pts,fill=(154,204,92,255),outline=INK+(255,),width=w)
    d.line([P(100,30),P(100,104)],fill=(110,160,64,255),width=int(5*K));d.line([P(100,62),P(74,48)],fill=(110,160,64,255),width=int(4*K));d.line([P(100,74),P(128,56)],fill=(110,160,64,255),width=int(4*K))
    d.line([P(86,118),P(86,178)],fill=(222,226,196,255),width=int(5*K));d.line([P(114,118),P(114,178)],fill=(222,226,196,255),width=int(5*K))
    return _fin(im,S)
def drumstick(S=200,rot=-30):
    im=_cv(200);d=ImageDraw.Draw(im);w=OL*K
    d.rounded_rectangle(P(92,96)+P(110,168),radius=8*K,fill=(252,246,232,255),outline=INK+(255,),width=w)
    for cx in (88,114):d.ellipse(P(cx-14,156)+P(cx+14,184),fill=(252,246,232,255),outline=INK+(255,),width=w)
    d.rectangle(P(96,150)+P(106,166),fill=(252,246,232,255))
    d.ellipse(P(44,18)+P(158,122),fill=(214,150,88,255),outline=INK+(255,),width=w)
    d.ellipse(P(66,34)+P(100,58),fill=(240,196,140,255));d.arc(P(60,70)+P(140,116),20,160,fill=(176,108,58,255),width=int(5*K))
    im=im.rotate(rot,resample=Image.BICUBIC);return _fin(im,S)
def apple(S=200):
    im=_cv(200);d=ImageDraw.Draw(im);w=OL*K
    d.line([P(102,58),P(108,26)],fill=(110,72,40,255),width=int(8*K))
    d.ellipse(P(108,22)+P(156,50),fill=(126,190,80,255),outline=INK+(255,),width=int(5*K))
    d.ellipse(P(34,56)+P(110,180),fill=(222,58,52,255),outline=INK+(255,),width=w);d.ellipse(P(90,56)+P(166,180),fill=(222,58,52,255),outline=INK+(255,),width=w)
    d.rectangle(P(80,70)+P(120,170),fill=(222,58,52,255));d.ellipse(P(56,80)+P(76,110),fill=(255,255,255,210))
    return _fin(im,S)
def corn(S=200,rot=-24):
    im=_cv(200);d=ImageDraw.Draw(im);w=OL*K
    d.ellipse(P(66,20)+P(134,176),fill=(255,214,64,255),outline=INK+(255,),width=w)
    for y in range(40,170,16):d.line([P(70,y),P(130,y)],fill=(224,170,30,255),width=int(3*K))
    for x in (84,100,116):d.line([P(x,28),P(x,170)],fill=(224,170,30,255),width=int(3*K))
    d.polygon([P(58,190),P(40,110),P(82,160)],fill=(126,190,80,255),outline=INK+(255,),width=int(5*K))
    d.polygon([P(142,190),P(160,110),P(118,160)],fill=(126,190,80,255),outline=INK+(255,),width=int(5*K))
    im=im.rotate(rot,resample=Image.BICUBIC);return _fin(im,S)
def flame(S=200,level=1.0,t=0.0):
    im=_cv(200);d=ImageDraw.Draw(im);w=OL*K;s=0.55+0.45*level;wob=math.sin(t*14)*4*level
    def tear(cx,cy,h,wd,col):
        top=(cx+wob,cy-h);pts=[top]
        for i in range(25):
            a=math.pi*i/24;pts.append((cx+wd*math.cos(math.pi+a)*-1*(1 if True else 1),cy+wd*0.2*math.sin(a)))
        d.polygon([P(*top)]+[P(cx-wd,cy-h*0.25),P(cx-wd*0.92,cy+wd*0.35),P(cx-wd*0.5,cy+wd*0.8),P(cx,cy+wd*0.92),P(cx+wd*0.5,cy+wd*0.8),P(cx+wd*0.92,cy+wd*0.35),P(cx+wd,cy-h*0.25)],fill=col,outline=INK+(255,),width=w)
    tear(100,140,110*s,58*s,(255,128,36,255));tear(100,150,60*s,30*s,(255,214,64,255))
    return _fin(im,S)
def bowl(S=220):
    im=_cv(220);d=ImageDraw.Draw(im);w=OL*K
    d.chord(P(26,70)+P(194,206),0,180,fill=(250,244,230,255),outline=INK+(255,),width=w)
    d.ellipse(P(26,104)+P(194,144),fill=(232,176,72,255),outline=INK+(255,),width=w)
    d.ellipse(P(96,108)+P(130,126),fill=(255,214,64,255));d.ellipse(P(62,114)+P(84,128),fill=(232,96,72,255))
    d.line([P(70,184),P(150,184)],fill=(214,60,44,255),width=int(6*K))
    return _fin(im,S)
def bubble_dot(r=22):
    S=int(r*2.6);im=blank(S*K,S*K);d=ImageDraw.Draw(im);c=S*K/2;rr=r*K
    d.ellipse((c-rr,c-rr,c+rr,c+rr),fill=(255,255,255,90),outline=(255,255,255,240),width=int(4*K))
    d.ellipse((c-rr*0.5,c-rr*0.55,c-rr*0.15,c-rr*0.2),fill=(255,255,255,230));return im.resize((S,S),Image.LANCZOS)
# ---------- round 姐夫嚴選 mark for the top-left corner (semi-transparent) ----------
def round_mark(d=164,bg_alpha=0.72,ink_alpha=0.92,k=3):
    D=d*k;im=blank(D+24*k,D+24*k);o=12*k
    disc=blank(D+24*k,D+24*k);dd=ImageDraw.Draw(disc);dd.ellipse((o,o,D+o,D+o),fill=(246,242,233,int(255*bg_alpha)))
    m=int(D*0.05);dd.ellipse((o+m,o+m,D+o-m,D+o-m),outline=kit5.COP+(int(255*ink_alpha),),width=max(2*k,int(D*0.014)))
    lg=kit5.logo_h(int(D*0.70));a=lg.getchannel("A").point(lambda v:int(v*ink_alpha));lg.putalpha(a)
    disc.alpha_composite(lg,(o+(D-lg.size[0])//2,o+(D-lg.size[1])//2))
    im=disc.resize((disc.size[0]//k,disc.size[1]//k),Image.LANCZOS)
    a=im.getchannel("A");sh=Image.new("RGBA",im.size,(0,0,0,0));sh.putalpha(a.filter(ImageFilter.GaussianBlur(5)).point(lambda v:int(v*0.25)))
    out=blank(im.size[0]+8,im.size[1]+10);out.alpha_composite(sh,(4,8));out.alpha_composite(im,(4,4));return out
MARK=round_mark()
MARK_XY=(26,26)
def paste_mark(base):base.alpha_composite(MARK,MARK_XY)
# ---------- comic parts ----------
def burst2(r=150,col=YEL,n=18,seed=1):
    S=int(r*2.4);im=blank(S*K,S*K);d=ImageDraw.Draw(im);c=S*K/2;rng=random.Random(seed);pts=[]
    for i in range(n*2):
        a=i/(n*2)*2*math.pi;rr=(r if i%2==0 else r*0.68)*K*rng.uniform(0.92,1.05);pts.append((c+rr*math.cos(a),c+rr*math.sin(a)))
    d.polygon(pts,fill=col+(255,),outline=INK+(255,),width=7*K);return im.resize((S,S),Image.LANCZOS)
def sound(text,size=150,col=YEL,rot=-8,burst_col=None):
    t=punch(text,size,col,0)
    if burst_col:
        b=burst2(max(t.size)*0.42,burst_col);W=max(b.size[0],t.size[0]);H=max(b.size[1],t.size[1]);out=blank(W,H)
        out.alpha_composite(b,((W-b.size[0])//2,(H-b.size[1])//2));out.alpha_composite(t,((W-t.size[0])//2,(H-t.size[1])//2));t=out
    return t.rotate(rot,resample=Image.BICUBIC,expand=True)
def speech(text,size=64,hl=RED,maxw=860):
    segs=parse(text);f=F("k",size)
    lines=wrap(segs,f,maxw)
    lh=int(size*1.32);tw=int(max(sum(f.getlength(c) for c,_ in l) for l in lines));W=tw+90;H=lh*len(lines)+56
    im=blank(W+40,H+80);sh=blank(W+40,H+80);sd=ImageDraw.Draw(sh)
    sd.rounded_rectangle((26,30,W+26,H+30),radius=40,fill=(20,8,0,110));sd.polygon([(90,H+20),(150,H+20),(70,H+70)],fill=(20,8,0,110))
    im=Image.alpha_composite(im,sh.filter(ImageFilter.GaussianBlur(9)));d=ImageDraw.Draw(im)
    d.rounded_rectangle((20,20,W+20,H+20),radius=40,fill=CREAM+(255,),outline=INK+(255,),width=6)
    d.polygon([(92,H+14),(150,H+14),(68,H+66)],fill=CREAM+(255,),outline=INK+(255,),width=6);d.line([(94,H+17),(148,H+17)],fill=CREAM+(255,),width=10)
    y=20+28
    for l in lines:
        x=20+45+(tw-sum(f.getlength(c) for c,_ in l))/2
        for c,h in l:d.text((x,y),c,font=f,fill=(hl if h else INK)+(255,),anchor="lt");x+=f.getlength(c)
        y+=lh
    return im
def confetti_layer(base,t,t0,seed=3,n=26):
    u=t-t0
    if u<0 or u>2.2:return
    rng=random.Random(seed);d=ImageDraw.Draw(base)
    for i in range(n):
        x0=540+rng.uniform(-80,80);vx=rng.uniform(-560,560);vy=rng.uniform(-1150,-650);g=1500
        x=x0+vx*u;y=1180+vy*u+0.5*g*u*u;col=rng.choice([YEL,RED,(90,180,255),(126,190,80),WHITE]);a=int(255*clamp((2.2-u)/0.5))
        r=rng.uniform(9,15);ang=u*rng.uniform(4,10)
        pts=[(x+r*math.cos(ang+k*math.pi/2)*(1 if k%2==0 else 0.45),y+r*math.sin(ang+k*math.pi/2)*(1 if k%2==0 else 0.45)) for k in range(4)]
        d.polygon(pts,fill=col+(a,))
