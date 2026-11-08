# 姐夫探店｜職人風格 三版（後驛鵝肉）：1 電影黑邊／2 紀錄片字卡／3 老店手寫
import sys,os,math,random,json,subprocess,io
SP="__ROOT__/"
sys.path.insert(0,SP+"soup")
from magv4 import *
from magv4 import _I3
sys.path.insert(0,SP+"goose")
import sty as gs
sfx=gs.sfx
BGM="__ROOT__/music/通用_lose-it.mp3";BGM_OFF=12.419
INFO=3.6;ENDC=2.6;END_ALL=INFO+ENDC
DISH=gs.DISH;CN="壹貳參肆";ORD=["第一道","第二道","第三道","第四道"]
ADDR="台北市大同區長安西路 220 巷 29 號";MRT="捷運台北車站／北門站 步行約 10 分鐘"
SUB={"case":"玻璃櫃裡，掛滿了鵝與鴨。","chop":"現點，現切。","soup":"先來一碗當歸鵝腸湯，暖胃。","blood":"乾鴨血，滑嫩綿密，越吃越涮嘴。",
     "duck":"白切鴨，吃的是原汁原味。","smoke":"煙燻鵝腿，煙燻香撲鼻。","all":"一桌四道，姐夫嚴選。"}
DISHES=["soup","blood","duck","smoke"]
DY={"store":40,"case":-60,"chop":170,"soup":60,"blood":-40,"duck":40,"smoke":0,"all":0}
WMAP={400:"400Regular",500:"500Medium",600:"600SemiBold",700:"700Bold",900:"900Black"}
def SER(w,s):return font("serif",WMAP[w],s)
def KA(s):return gs.KAI("700Bold",s)
_TK={}
def TK(text,f,col=WARM,track=0,sh=True,vertical=False,lead=1.04):
    k=(text,f.path,f.size,col,track,sh,vertical,lead)
    if k not in _TK:
        im=vtx(text,f,col,lead) if vertical else tx(text,f,col,track);_TK[k]=halo(im,f.size) if sh else bare(im)
    return _TK[k]
def cshow(base,im,top,v,a):w,h=vis(im);show_rise(base,im,540-w//2,top,v,a)
def shop_icon(h=90,col=WARM,sw=3.2,k=4):
    S=100;im=blank(S*k,S*k);d=ImageDraw.Draw(im);w=int(sw*k*100/h);c=col+(255,)
    def Q(x,y):return (x*k,y*k)
    d.line([Q(8,34),Q(50,12),Q(92,34)],fill=c,width=w,joint="curve");d.line([Q(14,40),Q(86,40)],fill=c,width=w)
    d.rectangle(Q(22,40)+Q(78,64),outline=c,width=w)
    for x in (40.7,59.3):d.line([Q(x,47),Q(x,64)],fill=c,width=w)
    d.line([Q(22,40),Q(22,92)],fill=c,width=w);d.line([Q(78,40),Q(78,92)],fill=c,width=w);d.line([Q(6,92),Q(94,92)],fill=c,width=w)
    return crop_vis(im.resize((h,h),Image.LANCZOS))
ICON=ink2(shop_icon(92),5,10,0.5,0.6)
# ---------------- looks ----------------
def mk_grade(lift=0.04,sat=0.92,sh=(0,0,0),hi=(0,0,0),con=0.0):
    lut=[]
    for c in range(3):
        for v in range(256):
            x=v/255;y=lift+(1-lift)*x;y+=con*(x-0.5)*(1-abs(2*x-1));y+=sh[c]*(1-x)**2+hi[c]*x**2;lut.append(int(round(min(max(y,0),1)*255)))
    def g(img):
        img=img.point(lut);return ImageEnhance.Color(img).enhance(sat) if abs(sat-1)>0.01 else img
    return g
_rng=np.random.default_rng(5);_GR=[_rng.normal(0,1,(OH//2,OW//2)).astype(np.float32) for _ in range(6)];_GC={}
def add_grain(img,t,sigma):
    k=(sigma,int(t*FPS/3)%6)
    if k not in _GC:_GC[k]=np.repeat(np.repeat((_GR[k[1]]*sigma).astype(np.int16),2,0),2,1)[:,:,None]
    a=np.asarray(img).astype(np.int16)+_GC[k];return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
def vignette(strength):
    yy,xx=np.mgrid[0:OH,0:OW].astype(np.float32);nx=(xx-OW/2)/(OW/2);ny=(yy-OH/2)/(OH/2)
    a=np.clip((np.sqrt(nx**2*0.9+ny**2*0.6)-0.55)/0.75,0,1)**1.6*strength
    im=Image.new("RGBA",(OW,OH),(10,6,4,0));im.putalpha(Image.fromarray((a*255).astype(np.uint8)));return im
# ---------------- ticker (address + transit), runs across store + case ----------------
def ticker_img(fl,ft,cl,ct):
    parts=[("地址",fl,cl),(ADDR,ft,ct),("交通",fl,cl),(MRT,ft,ct)];ims=[tx(p,f,c,2) for p,f,c in parts]
    gaps=[22,96,22];W=sum(i.size[0] for i in ims)+sum(gaps);H=max(i.size[1] for i in ims);can=blank(W,H);x=0
    for j,i in enumerate(ims):
        can.alpha_composite(i,(x,H-i.size[1]-(2 if j%2==0 else 0)));x+=i.size[0]+(gaps[j] if j<3 else 0)
    return halo(can,ft.size)
LOGO460=logo_h(460);ENDLINE=tx("姐夫嚴選為您挑選",SER(600,62),COP,10)
def brand_end(u):
    b=Image.new("RGBA",(OW,OH),CRM+(255,));v=ease(clamp(u/0.6));put(b,LOGO460,540,800-(1-v)*10,v)
    v2=ease(clamp((u-0.35)/0.5));put(b,ENDLINE,540,1238+(1-v2)*12,v2)
    r=ease(clamp((u-0.65)/0.5));hw=ENDLINE.size[0]/2;d=ImageDraw.Draw(b)
    if r>0.02:d.line([(540-hw-40-90*r,1240),(540-hw-40,1240)],fill=COP+(255,),width=2);d.line([(540+hw+40,1240),(540+hw+40+90*r,1240)],fill=COP+(255,),width=2)
    return b
def chop_snd():
    n=int(.25*SR);tt=np.arange(n)/SR;rng=np.random.default_rng(11);nz=rng.standard_normal(n)
    return (np.diff(np.r_[0,nz])*np.exp(-tt*110)*.4+np.sin(2*np.pi*np.cumsum(150*np.exp(-tt*16)+70)/SR)*np.exp(-tt*22)*1.0)*.8
class Craft(gs.SV):
    name="x";bars=False;grain=0;vig=0.0;TY=1430;TW=(40,940)
    def __init__(s):
        wd=SP+f"goose/craft_{s.name}";os.makedirs(wd,exist_ok=True)
        for f in ("video.mp4","cut.json"):
            p=os.path.join(wd,f)
            if not os.path.exists(p):os.symlink(SP+"goose/sP/"+f,p)
        super().__init__(wd,BGM,BGM_OFF,END_ALL,lufs=-17,fade_out=2.0)
        s.held={};s.cuts=[s.vo(n) for n in s.order[1:]];s.last_comp=None;s.last_clean=None;s.info_end=None
        s.VIG=vignette(s.vig) if s.vig>0 else None;s.SHADE=low_shade(900,0.42);s.setup()
        c=s.vo("chop");s.ev=[(c-1.6,sfx.whoosh(1.5,True),.2),(c,sfx.boom(),.34)]+[(h,chop_snd(),.4) for h in s.hits("chop",[6.195,6.589,7.007,7.425])]
        s.ev+=[(s.MAIN+0.02,sfx.whoosh(.8,True)*.6,.10),(s.MAIN+INFO+0.25,sfx.chime(),.16)]
    def setup(s):pass
    def cam(s,raw,n,u,d):
        z=1.0+0.045*clamp(u/d);w,h=OW/z,OH/z;cy=960+DY.get(n,0);y0=min(max(cy-h/2,0),OH-h);x0=(OW-w)/2
        return raw.resize((OW,OH),Image.BICUBIC,box=(x0,y0,x0+w,y0+h))
    def look(s,raw,n,u,d,t):
        img=s.grade(s.cam(raw,n,u,d));return add_grain(img,t,s.grain) if s.grain else img
    def compose(s,raw,t):
        n,u,d=s.seg(t);img=s.look(raw,n,u,d,t);ch=s.vo("chop")
        for c in s.cuts:
            if c-1.5/FPS<=t<c:s.held[c]=img
            elif c<=t<c+0.28 and abs(c-ch)>1e-3:
                h=s.held.get(c)
                if h is None:tp=c-1/FPS;nn,uu,dd=s.seg(tp);h=s.look(s.frame_at(tp),nn,uu,dd,tp);s.held[c]=h
                img=Image.blend(h,img,ease((t-c)/0.28))
        s.last_clean=img;base=img.convert("RGBA")
        if s.VIG:base.alpha_composite(s.VIG)
        if not s.bars:base.alpha_composite(s.SHADE)
        s.text(base,t,n,u,d);s.ticker(base,t)
        if s.bars:d=ImageDraw.Draw(base);d.rectangle((0,0,OW,250),fill=(8,7,6,255));d.rectangle((0,1690,OW,OH),fill=(8,7,6,255))
        paste_mark(base);s.last_comp=base;return base
    def ticker(s,base,t):
        t0=0.7;t1=s.ve("case")-0.12
        if not(t0<=t<t1):return
        uu=clamp((t-t0-0.6)/(t1-t0-1.1));q=0.5-0.5*math.cos(math.pi*uu);a=clamp((t-t0)/0.35)*clamp((t1-t)/0.22)
        w,h=vis(s.TICK);xl0=s.TW[0]+40;xl1=s.TW[1]-40-w;marquee(base,s.TICK,s.TY,xl0+(xl1-xl0)*q,a,s.TW,36);s.tick_extra(base,a)
    def tick_extra(s,base,a):pass
    def endframe(s,u):
        if u<INFO:
            pg=s.info(u);return Image.blend(s.last_comp,pg,ease(u/0.4)) if u<0.4 else pg
        u2=u-INFO;e=brand_end(u2)
        if u2<0.35:
            if s.info_end is None:s.info_end=s.info(INFO-0.01)
            return Image.blend(s.info_end,e,ease(u2/0.35))
        return e
    def still(s,t):
        if t<s.MAIN:return s.compose(s.frame_at(t),t).convert("RGB")
        s.compose(s.frame_at(s.MAIN-0.05),s.MAIN-0.05);return s.endframe(t-s.MAIN).convert("RGB")
# ======================= 1｜電影黑邊 =======================
class Cinema(Craft):
    name="cinema";bars=True;grain=4.5;vig=0.22
    grade=staticmethod(mk_grade(0.045,0.9,(-0.03,0.0,0.03),(0.045,0.015,-0.04),0.05))
    def setup(s):s.TICK=ticker_img(SER(600,46),SER(600,48),GOLD,WARM)
    def text(s,base,t,n,u,d):
        out=clamp((d-u)/0.22);X=60;S52=SER(600,52)
        if n=="store":
            show(base,ICON,X,1030,out);show(base,TK("姐夫探店",SER(600,54),WARM,8),X+110,1050,out)
            show(base,TK("後驛鵝肉店",SER(700,128),WARM,14),X-4,1124,out);show(base,line3(150,4,GOLD),X,1278,out)
            show(base,TK("台北車站後站・巷弄老店",SER(600,50),WARM,4),X,1302,out)
        elif n=="case":cshow(base,TK(SUB["case"],S52,WARM,2),1330,rv(u,0.5,0.3),out)
        elif n=="chop":
            im=TK("師傅現切",SER(700,100),WARM,0,True,True,1.04);v=clamp((u-0.15)/0.9)
            if v>0:show(base,wipe(im,ease(v)),X,1030,out)
            cshow(base,TK(SUB["chop"],S52,WARM,2),1420,rv(u,0.5,0.6),out)
        elif n in DISHES:
            i=DISHES.index(n);kicker4(base,CN[i],X,1150,out,v=rv(u,0.5,0.15),size=60)
            show_rise(base,TK(DISH[i],SER(700,96),WARM,8),X-2,1222,rv(u,0.55,0.25),out)
            cshow(base,TK(SUB[n],S52,WARM,2),1420,rv(u,0.5,0.45),out)
        elif n=="all":
            im=TK("四道必點",SER(700,104),WARM,0,True,True,1.04);v=clamp((u-0.15)/0.9)
            if v>0:show(base,wipe(im,ease(v)),X,1000,out)
            cshow(base,TK(SUB["all"],S52,WARM,2),1420,rv(u,0.5,0.6),out)
    def info(s,u):
        b=Image.new("RGBA",(OW,OH),(14,12,10,255));R=lambda d0:rv(u,0.55,d0)
        cshow(b,TK("後驛鵝肉店",SER(700,104),WARM,14),620,R(0.3),1)
        L=140*ease(clamp((u-0.55)/0.5))
        if L>3:show(b,line3(L,4,GOLD),540-L/2,790)
        X=80;y=850
        for j,(lab,val) in enumerate((("地址",ADDR),("交通",MRT))):
            show_rise(b,TK(lab,SER(600,44),GOLD,4),X,y+j*78,R(0.75+0.1*j),1);show_rise(b,TK(val,SER(600,44),WARM,2),X+118,y+j*78,R(0.8+0.1*j),1)
        show_rise(b,TK("必點",SER(600,44),GOLD,4),X,1040,R(1.05))
        show_rise(b,TK("當歸鵝腸湯・乾鴨血",SER(600,54),WARM,4),X+118,1034,R(1.1));show_rise(b,TK("白切鴨・煙燻鵝腿",SER(600,54),WARM,4),X+118,1112,R(1.18))
        d=ImageDraw.Draw(b);d.rectangle((0,0,OW,250),fill=(8,7,6,255));d.rectangle((0,1690,OW,OH),fill=(8,7,6,255));paste_mark(b);return b
# ======================= 2｜紀錄片字卡 =======================
class Docu(Craft):
    name="docu";TW=(84,940)
    grade=staticmethod(mk_grade(0.035,0.95,(0,0,0.012),(0.018,0.008,-0.012),0.0))
    def setup(s):s.TICK=ticker_img(SER(600,46),SER(600,48),GOLD,WARM)
    def bar(s,base,y,h,a):show(base,line3(6,h,GOLD),60,y,a)
    def tick_extra(s,base,a):s.bar(base,s.TY-6,62,a)
    def text(s,base,t,n,u,d):
        out=clamp((d-u)/0.22);X=60;S52=SER(600,52)
        if n=="store":
            show(base,ICON,X,1030,out);lab=TK("姐夫探店",SER(600,54),WARM,8);show(base,lab,X+110,1050,out)
            lx=X+110+vis(lab)[0]+24;show(base,line3(3,52),lx,1052,out);show(base,TK("台北車站後站",SER(600,48),WARM,4),lx+24,1056,out)
            show(base,TK("後驛鵝肉店",SER(700,140),WARM,14),X-6,1130,out)
        elif n=="case":
            v=rv(u,0.5,0.3);s.bar(base,1322,62,out*v);show_rise(base,TK(SUB["case"],S52,WARM,2),X+26,1330,v,out)
        elif n=="chop":
            v=rv(u,0.5,0.3);L=140*ease(clamp((u-0.2)/0.4));s.bar(base,1262,L,out)
            show_rise(base,TK("後驛鵝肉店・師傅",SER(700,64),WARM,6),X+26,1268,v,out);show_rise(base,TK(SUB["chop"],S52,WARM,2),X+26,1350,rv(u,0.5,0.45),out)
        elif n in DISHES:
            i=DISHES.index(n);kicker4(base,ORD[i],X,1140,out,v=rv(u,0.5,0.15),size=52)
            show_rise(base,TK(DISH[i],SER(700,104),WARM,8),X-4,1210,rv(u,0.55,0.25),out)
            v=rv(u,0.5,0.45);s.bar(base,1372,62,out*v);show_rise(base,TK(SUB[n],S52,WARM,2),X+26,1380,v,out)
        elif n=="all":
            kicker4(base,"四道必點",X,1130,out,v=rv(u,0.5,0.15),size=56)
            show_rise(base,TK("當歸鵝腸湯・乾鴨血",SER(700,70),WARM,4),X,1204,rv(u,0.55,0.25),out)
            show_rise(base,TK("白切鴨・煙燻鵝腿",SER(700,70),WARM,4),X,1294,rv(u,0.55,0.35),out)
            v=rv(u,0.5,0.6);s.bar(base,1392,62,out*v);show_rise(base,TK(SUB["all"],S52,WARM,2),X+26,1400,v,out)
    def info(s,u):
        if not hasattr(s,"BG"):
            bg=s.last_clean.filter(ImageFilter.GaussianBlur(26)).convert("RGBA");bg.alpha_composite(Image.new("RGBA",(OW,OH),(14,10,8,150)));s.BG=bg
        b=s.BG.copy();R=lambda d0:rv(u,0.55,d0);X=80
        kicker4(b,"姐夫探店",X,700,1.0,v=R(0.3),size=52)
        show_rise(b,TK("後驛鵝肉店",SER(700,112),WARM,12),X-4,770,R(0.4))
        L=900*ease(clamp((u-0.6)/0.6))
        if L>3:show(b,line3(L,3,WARM),X,920)
        y=960
        for j,(lab,val) in enumerate((("地址",ADDR),("交通",MRT))):
            show_rise(b,TK(lab,SER(600,44),GOLD,4),X,y+j*78,R(0.8+0.1*j));show_rise(b,TK(val,SER(600,44),WARM,2),X+118,y+j*78,R(0.85+0.1*j))
        show_rise(b,TK("必點",SER(600,44),GOLD,4),X,1150,R(1.05))
        show_rise(b,TK("當歸鵝腸湯・乾鴨血",SER(600,54),WARM,4),X+118,1144,R(1.1));show_rise(b,TK("白切鴨・煙燻鵝腿",SER(600,54),WARM,4),X+118,1222,R(1.18))
        paste_mark(b);return b
# ======================= 3｜老店手寫 =======================
SEAL_TAN=seal("姐夫探店",108,seed=21);SEAL_BD=seal("必點",120,seed=22);SEAL_CN=[seal(c,84,seed=30+i) for i,c in enumerate(CN)]
class Oldshop(Craft):
    name="oldshop";grain=3.5;vig=0.18;TW=(200,940)
    grade=staticmethod(mk_grade(0.05,0.95,(0.02,0.0,-0.03),(0.05,0.025,-0.05),0.03))
    def setup(s):s.TICK=ticker_img(KA(46),KA(48),GOLD,WARM)
    def text(s,base,t,n,u,d):
        out=clamp((d-u)/0.22);S54=KA(54)
        if n=="store":
            ic=ink2(shop_icon(84),5,10,0.5,0.6);show(base,ic,68,858,out)
            col=TK("後驛鵝肉店",KA(100),WARM,0,True,True,1.04);show(base,col,60,960,out)
            show(base,TK("台北車站後站",KA(48),WARM,0,True,True,1.08),214,984,out)
            put(base,SEAL_TAN,246,1352,out)
        elif n=="case":cshow(base,TK(SUB["case"],S54,WARM,2),1330,rv(u,0.5,0.3),out)
        elif n=="chop":
            im=TK("師傅現切",KA(110),WARM,0,True,True,1.04);v=clamp((u-0.15)/0.9)
            if v>0:show(base,wipe(im,ease(v)),60,1000,out)
            cshow(base,TK(SUB["chop"],S54,WARM,2),1420,rv(u,0.5,0.6),out)
        elif n in DISHES:
            i=DISHES.index(n);stamp(base,SEAL_CN[i],102,940,u-0.1,out)
            im=TK(DISH[i],KA(92),WARM,0,True,True,1.04);v=clamp((u-0.25)/0.8)
            if v>0:show(base,wipe(im,ease(v)),60,1000,out)
            cshow(base,TK(SUB[n],S54,WARM,2),1420,rv(u,0.5,0.5),out)
        elif n=="all":
            im=TK("四道必點",KA(110),WARM,0,True,True,1.04);v=clamp((u-0.15)/0.9)
            if v>0:show(base,wipe(im,ease(v)),60,1000,out)
            stamp(base,SEAL_BD,262,1066,u-0.9,out);cshow(base,TK(SUB["all"],S54,WARM,2),1420,rv(u,0.5,0.6),out)
    def info(s,u):
        if not hasattr(s,"PAPER"):s.PAPER=gs.paper((244,236,222),6,3,12)
        b=s.PAPER.copy();R=lambda d0:rv(u,0.55,d0);INKC=(52,40,32);RED=(170,64,44)
        cshow(b,TK("後驛鵝肉店",KA(112),INKC,10,False),640,R(0.3),1);stamp(b,SEAL_TAN,540,860,u-0.7)
        X=110;y=960
        for j,(lab,val) in enumerate((("地址",ADDR),("交通",MRT))):
            show_rise(b,TK(lab,KA(44),RED,4,False),X,y+j*76,R(0.85+0.1*j));show_rise(b,TK(val,KA(44),INKC,2,False),X+112,y+j*76,R(0.9+0.1*j))
        show_rise(b,TK("必點",KA(44),RED,4,False),X,1150,R(1.1))
        show_rise(b,TK("當歸鵝腸湯・乾鴨血",KA(54),INKC,4,False),X+112,1142,R(1.15));show_rise(b,TK("白切鴨・煙燻鵝腿",KA(54),INKC,4,False),X+112,1220,R(1.22))
        paste_mark(b);return b
STY={"cinema":Cinema,"docu":Docu,"oldshop":Oldshop}
TITLE={"cinema":"職人1_電影黑邊","docu":"職人2_紀錄片字卡","oldshop":"職人3_老店手寫"}
if __name__=="__main__":
    k=sys.argv[2];V=STY[k]()
    if sys.argv[1]=="render":V.render(SP+f"goose/後驛鵝肉_姐夫探店_{TITLE[k]}.mp4")
    elif sys.argv[1]=="sheet":
        ts=[float(x) for x in sys.argv[3].split(",")];ims=[V.still(t) for t in ts]
        cw=432;ch=768;n=5;sh=Image.new("RGB",(cw*min(n,len(ims)),ch*((len(ims)+n-1)//n)),(255,255,255))
        for i,im in enumerate(ims):sh.paste(im.resize((cw,ch),Image.LANCZOS),((i%n)*cw,(i//n)*ch))
        sh.save(SP+f"goose/craft_{k}_sheet.jpg",quality=86);print("ok")
