# 開煮｜日系雜誌 v2 — refined: airy diffusion grade, warm-white type, italic numerals, masked line reveals,
# cooking timeline, "60 分鐘後" kicker, recipe page (photo + 材料 with dot leaders + 收藏 CTA), then brand end card
import sys,os,math
SP="__ROOT__/"
sys.path.insert(0,SP+"soup")
from prem2 import *
from prem2 import _IC
from PIL import ImageFont
FX=SP+"fonts/x2/package/"
WARM=(252,248,240);INK=(46,58,50);RULE=(214,206,192);DOT=(186,176,160)
GARA_I=ImageFont.truetype(FX+"400Regular_Italic/CormorantGaramond_400Regular_Italic.ttf",196)
RP=3.4;ENDB=2.9;END2=RP+ENDB
# ---------------- grade: airy, soft contrast, split tone, highlight diffusion ----------------
def _lut():
    lut=[];sh=(-0.012,0.0,0.016);hi=(0.022,0.010,-0.012)
    for c in range(3):
        for v in range(256):
            x=v/255;y=0.045+0.955*x;y=y+0.06*math.sin(math.pi*x)*(0.5-x)*-0.6   # gentle S-curve softening
            y+=sh[c]*(1-x)**2+hi[c]*x**2;lut.append(int(round(min(max(y,0),1)*255)))
    return lut
LUT=_lut();BLOOM_LUT=[0 if v<150 else int(min(255,(v-150)*255/105)*0.24) for v in range(256)]*3
def airy(img):
    img=ImageEnhance.Color(img.point(LUT)).enhance(0.88)
    sm=img.resize((OW//6,OH//6),Image.BILINEAR).filter(ImageFilter.GaussianBlur(5)).point(BLOOM_LUT).resize((OW,OH),Image.BILINEAR)
    return ImageChops.screen(img,sm)
# ---------------- reveal helpers ----------------
def show_rise(base,im,x,y,v,a=1.0,dist=None,soft=26):
    """editorial line reveal: the line rises from just below its baseline through a soft mask"""
    if v<=0.001 or a<=0.003:return
    if v>=0.999:show(base,im,x,y,a);return
    w,h=vis(im);dist=dist or int(h*0.8+10);dy=int(round((1-v)*dist))
    W,H=im.size;can=blank(W,H+dist+2);can.alpha_composite(im,(0,dy))
    line=P+h+8;yy=np.arange(can.size[1],dtype=np.float32);m=np.clip((line-yy)/soft+1,0,1)
    k=clamp((v-0.7)/0.3);m=1-(1-m)*(1-k)
    M=Image.fromarray((np.tile(m[:,None],(1,W))*255).astype(np.uint8));can.putalpha(ImageChops.multiply(can.getchannel("A"),M))
    paste(base,fade(can,a*clamp(v*1.6)),x-P,y-P)
def kicker(base,text,x,y,a,col=LCOP,size=30,line=40,sh=True,v=1.0):
    im=T(text,"serif","500Medium",size,col,12,sh);w,h=vis(im);show_rise(base,im,x,y,v,a)
    L=line*ease(clamp((v-0.3)/0.7))
    if L>2:
        hl=hline(L,2,col) if sh else bare_line(L,2,col)
        show(base,hl,x+w+16,y+h//2,a)
_BL={}
def bare_line(w,h=2,col=RULE):
    w=max(2,int(w));k=(w,h,col)
    if k not in _BL:im=blank(w,h);ImageDraw.Draw(im).rectangle((0,0,w,h),fill=col+(255,));_BL[k]=bare(im)
    return _BL[k]
def num_img(s):
    k=("num",s)
    if k not in _IC:
        f=GARA_I;im=blank(f.getlength(s)+40,260);ImageDraw.Draw(im).text((10,10),s,font=f,fill=LCOP+(255,));_IC[k]=ink(crop_vis(im),14,0.38,3,0.38,2)
    return _IC[k]
# ---------------- cooking timeline (s5) ----------------
TL_X0=276;TL_W=520;TL_Y=1438
def timeline(base,prog,a):
    if a<=0.003:return
    lay=blank(TL_W+120,120);d=ImageDraw.Draw(lay);ox,oy=20,56
    d.line([(ox,oy),(ox+TL_W,oy)],fill=WARM+(150,),width=2)
    for m in (0,20,60):
        x=ox+TL_W*m/60;d.line([(x,oy-7),(x,oy+7)],fill=WARM+(210,),width=2)
    f=font("serif","400Regular",27)
    for m,lab in ((0,"0"),(20,"20"),(60,"60 分")):
        x=ox+TL_W*m/60;d.text((x,oy+16),lab,font=f,fill=WARM+(235,),anchor="ma")
    f2=font("serif","500Medium",27)
    d.text((ox+TL_W*10/60,oy-14),"中火",font=f2,fill=LCOP+(255,),anchor="md");d.text((ox+TL_W*40/60,oy-14),"小火",font=f2,fill=LCOP+(255,),anchor="md")
    px=ox+TL_W*prog/60
    if prog>0.2:d.line([(ox,oy),(px,oy)],fill=LCOP+(255,),width=5)
    d.ellipse((px-7,oy-7,px+7,oy+7),fill=WARM+(255,))
    show(base,ink(lay,8,0.38,2,0.35,1),TL_X0-20,TL_Y-oy,a)
# ---------------- recipe page pieces ----------------
def leader_row(name,amount,w,size=30):
    fn=font("serif","400Regular",size);fa=font("serif","500Medium",size)
    a=tx(name,fn,INK,2);b=tx(amount,fa,COP,2);H=max(a.size[1],b.size[1])+8;im=blank(w,H+8)
    im.alpha_composite(a,(0,H-a.size[1]));im.alpha_composite(b,(w-b.size[0],H-b.size[1]));d=ImageDraw.Draw(im)
    x=a.size[0]+16;xe=w-b.size[0]-16;cy=H-8
    while x<xe:d.ellipse((x-1.7,cy-1.7,x+1.7,cy+1.7),fill=DOT+(255,));x+=11
    return bare(im)
PAGE_PHOTO=(60,250,1020,830)
class Mag2(Prem):
    name="mag2";grade_fn=staticmethod(airy);SHADE=low_shade(900,0.44)
    def __init__(s):
        super().__init__();s.END=END2;s.TOTAL=s.MAIN+END2;s.last_clean=None
        f=s.vo("s6a");M=s.MAIN
        s.ev=[(f+0.1+0.85,CHM,.13),(M+0.04,WR,.10),(M+RP+0.45,CHM,.18)]
    def compose(s,img,t):
        img=s.cam_tf(img,t)
        for c in s.cuts:
            if c-1.5/FPS<=t<c:s.held[c]=img
            elif c<=t<c+DIS:
                h=s.held.get(c)
                if h is None:tp=c-1/FPS;h=s.cam_tf(s.frame_at(tp),tp);s.held[c]=h
                img=Image.blend(h,img,ease((t-c)/DIS))
        s.last_clean=img;img=img.convert("RGBA");s.overlay(img,t);return img.convert("RGB")
    # ---- opening (cover, visible from frame 0) ----
    def d_open(s,base,t,a):
        X=58;show(base,POT70,X,1118,a);lab=T("姐夫開煮","serif","500Medium",40,WARM,14);show(base,lab,X+90,1136,a)
        lx=X+90+vis(lab)[0]+22;show(base,vline(34,2,WARM),lx,1138,a*0.8)
        show(base,T("5 種食材・60 分鐘","serif","400Regular",28,WARM,4),lx+22,1142,a*0.9)
        show(base,hline(96+44*ease(t/2.3),3,WARM),X,1214,a)
        show(base,T("無水雞湯","serif","600SemiBold",138,WARM,10+8*clamp(t/2.3)),X-4,1240,a)
        show(base,T("洋蔥・白菜・雞腿・蘋果・玉米","serif","400Regular",34,WARM,6),X,1414,a*0.96)
    # ---- steps ----
    def d_step(s,base,i,num,cn,kick,text,uf,af,ut,at_):
        X=50;nm=num_img(num);nw,nh=vis(nm);v=rv(uf,0.6);show(base,nm,X,1222+(1-v)*16,af*v)
        rx=X+nw+24;L=140*ease(clamp((uf-0.1)/0.45))
        if L>3:show(base,vline(L,2,WARM),rx,1234,af)
        tx0=rx+30;kicker(base,kick,tx0,1242,af,v=rv(uf,0.5,0.12))
        show_rise(base,T(text,"serif","600SemiBold",58,WARM,4),tx0,1298,rv(ut,0.6,0.22),at_)
        if i==4:
            sp=s.vo("s5")+4*B;t=s.vo("s5")+0.12+uf
            p=20*ease(clamp((uf-0.35)/1.1)) if t<sp else 20+40*ease(clamp((t-sp-0.1)/1.5))
            timeline(base,p,af*rv(uf,0.5,0.3))
    # ---- finale ----
    def d_fin(s,base,u):
        X=58;kicker(base,"60 分鐘後",X,1128,1.0,v=rv(u,0.5))
        show_rise(base,T("一鍋鮮甜美味的雞湯","serif","500Medium",50,WARM,6),X,1182,rv(u,0.6,0.15))
        L=110*ease(clamp((u-0.55)/0.45))
        if L>3:show(base,hline(L,3,WARM),X,1264)
        v2=ease(clamp((u-0.75)/0.9))
        if v2>0:show_rise(base,T("上桌了","serif","600SemiBold",128,WARM,14+20*(1-v2)),X-4,1304,v2,dist=60)
    # ---- recipe page + brand end card ----
    def endparts(s,last):
        clean=(s.last_clean or last).convert("RGBA");Pp=dict(last=last.convert("RGBA"),clean=clean,logo=logo_h(460))
        Pp["line"]=tx("姐夫嚴選為您挑選",font("serif","600SemiBold",62),COP,10)
        c=(PAGE_PHOTO[2]-PAGE_PHOTO[0])/(PAGE_PHOTO[3]-PAGE_PHOTO[1]);ch=OW/c;cy=1000
        Pp["crop"]=(0,cy-ch/2,OW,cy+ch/2)
        Pp["rows"]=[leader_row("洋蔥","鋪滿鍋底",400,34),leader_row("白菜","鋪一層",400,34),leader_row("帶骨大雞腿","2 隻",400,34),
                    leader_row("蘋果","1 個",378,34),leader_row("玉米","1 根",378,34)]
        Pp["pot"]=bare(fine_pot(58,COP,2.6))
        Pp["recipe_end"]=None
        return Image.new("RGBA",(OW,OH),CRM+(255,)),Pp
    def recipe(s,Pp,u):
        b=Image.new("RGBA",(OW,OH),CRM+(255,));t=ease(clamp(u/0.75))
        src0=(0,0,OW,OH);src1=Pp["crop"];k=0.04*clamp((u-0.75)/(RP-0.75))
        cx=(src1[0]+src1[2])/2;cy=(src1[1]+src1[3])/2;hw=(src1[2]-src1[0])/2*(1-k);hh=(src1[3]-src1[1])/2*(1-k)
        src=tuple(a0+(a1-a0)*t for a0,a1 in zip(src0,(cx-hw,cy-hh,cx+hw,cy+hh)))
        dst=tuple(a0+(a1-a0)*t for a0,a1 in zip((0,0,OW,OH),PAGE_PHOTO))
        img=Pp["clean"] if u>=0.22 else Image.blend(Pp["last"],Pp["clean"],ease(u/0.22))
        dw,dh=int(round(dst[2]-dst[0])),int(round(dst[3]-dst[1]))
        ph=img.resize((dw,dh),Image.BICUBIC,box=src);b.alpha_composite(ph,(int(round(dst[0])),int(round(dst[1]))))
        if t<1:paste_mark(b)
        X=60;
        def R(v0):return rv(u,0.55,v0)
        show_rise(b,T("姐夫開煮・無水雞湯","serif","400Regular",24,SAGE,4,False),X,850,R(0.7),1.0)
        show(b,Pp["pot"],X,900,R(0.75));kicker(b,"姐夫開煮",X+76,914,1.0,col=COP,size=32,sh=False,v=R(0.75))
        show_rise(b,T("無水雞湯","serif","600SemiBold",108,GRN,8,False),X-2,966,R(0.85))
        show_rise(b,T("5 種食材｜60 分鐘","serif","400Regular",30,SAGE,4,False),X,1100,R(0.95))
        L=960*ease(clamp((u-1.0)/0.6))
        if L>3:show(b,bare_line(L,2,RULE),X,1158)
        show_rise(b,T("材料","serif","600SemiBold",32,COP,8,False),X,1190,R(1.05))
        for j,rw in enumerate(Pp["rows"]):
            col,row=(0,j) if j<3 else (1,j-3);x=182+col*460;y=1186+row*60
            show_rise(b,rw,x,y,R(1.1+j*0.07))
        L2=960*ease(clamp((u-1.45)/0.6))
        if L2>3:show(b,bare_line(L2,2,RULE),X,1376)
        show_rise(b,T("做法","serif","600SemiBold",32,COP,8,False),X,1404,R(1.5))
        show_rise(b,T("依序鋪好食材，不加水，中火 20 分鐘轉小火 40 分鐘。","serif","400Regular",30,INK,2,False),182,1405,R(1.55))
        show_rise(b,T("先收藏，下次照著煮","serif","500Medium",32,COP,10,False),X,1460,R(1.75))
        paste_mark(b) if t>=1 else None
        return b
    def endframe(s,bg,Pp,u):
        if u<RP:return s.recipe(Pp,u)
        u2=u-RP;b=Image.new("RGBA",(OW,OH),CRM+(255,));v=ease(clamp(u2/0.6));put(b,Pp["logo"],540,800-(1-v)*10,v)
        Ln=Pp["line"];v2=ease(clamp((u2-0.35)/0.5));put(b,Ln,540,1238+(1-v2)*12,v2)
        r=ease(clamp((u2-0.65)/0.5));hw=Ln.size[0]/2;d=ImageDraw.Draw(b)
        if r>0.02:
            d.line([(540-hw-40-90*r,1240),(540-hw-40,1240)],fill=COP+(255,),width=2);d.line([(540+hw+40,1240),(540+hw+40+90*r,1240)],fill=COP+(255,),width=2)
        if u2<0.3:
            if Pp["recipe_end"] is None:Pp["recipe_end"]=s.recipe(Pp,RP-1e-3)
            return Image.blend(Pp["recipe_end"],b,ease(u2/0.3))
        return b
if __name__=="__main__":
    V=Mag2()
    if sys.argv[1]=="render":V.render(SP+"soup/姐夫開煮_無水雞湯_日系雜誌_v2.mp4")
    elif sys.argv[1]=="sheet":
        ts=[float(x) for x in sys.argv[2].split(",")];ims=[V.still(t) for t in ts]
        cw=540;sh=Image.new("RGB",(cw*min(4,len(ims)),960*((len(ims)+3)//4)),(255,255,255))
        for i,im in enumerate(ims):sh.paste(im.resize((cw,960),Image.LANCZOS),((i%4)*cw,(i//4)*960))
        sh.save(SP+"soup/mag2_sheet.jpg",quality=86);print("ok")
