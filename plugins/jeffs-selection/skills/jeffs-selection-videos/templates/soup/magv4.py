# 開煮｜日系雜誌 v4 — type ×1.25 proportionally; long lines go to two lines; long shots use a slow marquee
import sys,os,math
SP="__ROOT__/"
sys.path.insert(0,SP+"soup")
from magv3 import *
from magv3 import _I3
STEP_PX=84;WIN_R=940
def split2(text,size,maxw,maxc=8):
    """one line if it fits; otherwise (or when long with a natural break) two lines"""
    f=font("serif","600SemiBold",size);w=sum(f.getlength(c) for c in text)
    has=[c for c in ("＋","，","、"," ") if c in text]
    if w<=maxw and not(has and len(text)>maxc):return [text]
    if has:
        c=has[0];i=text.index(c)
        if c=="＋":return [text[:i],text[i:]]
        if c in "，、":return [text[:i+1],text[i+1:]]
        return [text[:i],text[i+1:]]
    m=(len(text)+1)//2;return [text[:m],text[m:]]
def num4(s):
    k=("num4",s)
    if k not in _I3:
        f=ImageFont.truetype(FX+"400Regular_Italic/CormorantGaramond_400Regular_Italic.ttf",245)
        im=blank(f.getlength(s)+50,330);ImageDraw.Draw(im).text((12,12),s,font=f,fill=GOLD+(255,));_I3[k]=ink2(crop_vis(im),9,20,0.46,0.55)
    return _I3[k]
def kicker4(base,text,x,y,a,v=1.0,col=WARM,size=50,lcol=GOLD,sh=True):
    im=T3(text,"serif","600SemiBold",size,col,4,sh);w,h=vis(im);show_rise(base,im,x,y,v,a)
    L=56*ease(clamp((v-0.3)/0.7))
    if L>2:show(base,line3(L,4,lcol) if sh else bare_line(L,3,lcol),x+w+20,y+h//2-2,a)
# ---------------- marquee ----------------
_HM={}
def hmask(x0,x1,fw):
    k=(x0,x1,fw)
    if k not in _HM:
        xx=np.arange(OW,dtype=np.float32);_HM[k]=np.clip((xx-x0)/fw,0,1)*np.clip((x1-xx)/fw,0,1)
    return _HM[k]
def marquee_img(parts,size):
    f=font("serif","600SemiBold",size);ims=[tx(p,f,WARM,3) for p in parts];gap=34;dash=72
    W=sum(i.size[0] for i in ims)+(len(ims)-1)*(2*gap+dash);H=max(i.size[1] for i in ims);can=blank(W,H);x=0;d=ImageDraw.Draw(can)
    for j,i in enumerate(ims):
        can.alpha_composite(i,(x,H-i.size[1]));x+=i.size[0]
        if j<len(ims)-1:cy=int(H*0.56);d.line([(x+gap,cy),(x+gap+dash,cy)],fill=GOLD+(255,),width=5);x+=2*gap+dash
    return halo(can,size)
def marquee(base,im,y,xl,a,win,fw=64):
    if a<=0.003:return
    H=im.size[1];band=blank(OW,H);paste(band,im,xl-P,0)
    m=hmask(win[0],win[1],fw);M=Image.fromarray((np.tile(m[None,:],(H,1))*255).astype(np.uint8))
    band.putalpha(ImageChops.multiply(band.getchannel("A"),M));paste(base,fade(band,a),0,y-P)
MQ=marquee_img(["中火 20 分鐘","轉小火 40 分鐘"],STEP_PX)
# ---------------- timeline (labels only 中火／小火, big) ----------------
def timeline4(base,x0,prog,a):
    if a<=0.003:return
    W0=600;lay=blank(W0+80,140);d=ImageDraw.Draw(lay);ox,oy=20,104;x20=ox+W0/3;xe=ox+W0
    d.line([(ox,oy),(xe,oy)],fill=WARM+(170,),width=5)
    for x in (ox,x20,xe):d.line([(x,oy-13),(x,oy+13)],fill=WARM+(235,),width=4)
    px=ox+W0*prog/60
    if prog>0.2:d.line([(ox,oy),(px,oy)],fill=GOLD+(255,),width=11)
    d.ellipse((px-12,oy-12,px+12,oy+12),fill=WARM+(255,))
    f=font("serif","600SemiBold",44)
    d.text(((ox+x20)/2,oy-28),"中火",font=f,fill=WARM+(255,),anchor="md");d.text(((x20+xe)/2,oy-28),"小火",font=f,fill=WARM+(255 if prog>20.5 else 205,),anchor="md")
    show(base,ink2(lay,7,12,0.55,0.62),x0-ox,1452-oy,a)
POT4=ink2(fine_pot(96,WARM,4.0),5,10,0.5,0.6)
PAGE4=(60,250,1020,740)
class Mag4(Mag3):
    name="mag4"
    def extra_top(s,base,t):
        h=s.ve("hook")
        if t<h:s.d_open(base,t,clamp((h-0.04-t)/0.25))
        for i,(k,num,cn,kick,txt) in enumerate(STEPS):
            a0=s.vo(k)+0.12;a1=s.ve(k)-0.02
            if a0<=t<a1:af=clamp((a1-t)/0.22);uf=t-a0;s.d_step(base,i,num,cn,kick,txt,uf,af,uf,af)
        f=s.vo("s6a")
        if t>=f+0.1:s.d_fin(base,t-(f+0.1))
    def d_open(s,base,t,a):
        X=58;show(base,POT4,X,1040,a);lab=T3("姐夫開煮","serif","600SemiBold",58,WARM,8);show(base,lab,X+118,1064,a)
        lx=X+118+vis(lab)[0]+24;show(base,line3(3,50),lx,1066,a);show(base,T3("60 分鐘","serif","600SemiBold",48,WARM,2),lx+24,1071,a)
        show(base,line3(120+55*ease(t/2.3),5),X,1160,a)
        show(base,T3("無水雞湯","serif","600SemiBold",172,WARM,12+8*clamp(t/2.3)),X-5,1190,a)
        show(base,T3("洋蔥・白菜・雞腿・蘋果・玉米","serif","600SemiBold",50,WARM,4),X,1388,a)
    def d_step(s,base,i,num,cn,kick,text,uf,af,ut,at_):
        X=50;Y0=1190;nm=num4(num);nw,nh=vis(nm);v=rv(uf,0.6);show(base,nm,X,Y0-6+(1-v)*16,af*v)
        rx=X+nw+26;c0=rx+30;kicker4(base,kick,c0,Y0,af,v=rv(uf,0.5,0.12))
        if i==4:
            dur=(s.ve("s5")-0.02)-(s.vo("s5")+0.12);u=clamp(uf/dur);w,h=vis(MQ)
            uu=clamp((uf-0.6)/(dur-1.1));q=0.5-0.5*math.cos(math.pi*uu);xl0=c0+10;xl1=WIN_R-40-w
            marquee(base,MQ,Y0+68,xl0+(xl1-xl0)*q,af*rv(uf,0.45,0.18),(rx+4,WIN_R),36)
            p=20*ease(clamp(q/0.35)) if q<0.35 else 20+40*ease(clamp((q-0.35)/0.65))
            timeline4(base,c0,p,af*rv(uf,0.5,0.3));Lh=158
        else:
            lines=split2(text,STEP_PX,WIN_R-c0)
            for j,ln in enumerate(lines):
                show_rise(base,T3(ln,"serif","600SemiBold",STEP_PX,WARM,3),c0,Y0+68+j*102,rv(ut,0.6,0.22+0.12*j),at_)
            Lh=68+102*len(lines)-10
        L=Lh*ease(clamp((uf-0.1)/0.45))
        if L>3:show(base,line3(3,L),rx,Y0-4,af)
    def d_fin(s,base,u):
        X=58;kicker4(base,"60 分鐘後",X,1060,1.0,v=rv(u,0.5),size=52)
        ls=split2("一鍋鮮甜美味的雞湯",72,900)
        for j,ln in enumerate(ls):show_rise(base,T3(ln,"serif","600SemiBold",72,WARM,4),X,1132+j*90,rv(u,0.6,0.15+0.1*j))
        y=1236+(len(ls)-1)*90;L=140*ease(clamp((u-0.55)/0.45))
        if L>3:show(base,line3(L,5),X,y)
        v2=ease(clamp((u-0.75)/0.9))
        if v2>0:show_rise(base,T3("上桌了","serif","600SemiBold",160,WARM,16+24*(1-v2)),X-5,y+32,v2,dist=70)
    def endparts(s,last):
        bg,Pp=super().endparts(last)
        c=(PAGE4[2]-PAGE4[0])/(PAGE4[3]-PAGE4[1]);ch=OW/c;cy=1000;Pp["crop"]=(0,cy-ch/2,OW,cy+ch/2)
        Pp["rows"]=[leader3("洋蔥","鋪滿鍋底",420,42),leader3("白菜","鋪一層",420,42),leader3("帶骨大雞腿","2 隻",420,42),leader3("蘋果","1 個",350,42),leader3("玉米","1 根",350,42)]
        Pp["pot"]=bare(fine_pot(68,DCOP,3.2));return bg,Pp
    def recipe(s,Pp,u):
        b=Image.new("RGBA",(OW,OH),CRM+(255,));t=ease(clamp(u/0.75))
        src1=Pp["crop"];k=0.04*clamp((u-0.75)/(RP-0.75))
        cx=(src1[0]+src1[2])/2;cy=(src1[1]+src1[3])/2;hw=(src1[2]-src1[0])/2*(1-k);hh=(src1[3]-src1[1])/2*(1-k)
        src=tuple(a0+(a1-a0)*t for a0,a1 in zip((0,0,OW,OH),(cx-hw,cy-hh,cx+hw,cy+hh)))
        dst=tuple(a0+(a1-a0)*t for a0,a1 in zip((0,0,OW,OH),PAGE4))
        img=Pp["clean"] if u>=0.22 else Image.blend(Pp["last"],Pp["clean"],ease(u/0.22))
        dw,dh=int(round(dst[2]-dst[0])),int(round(dst[3]-dst[1]))
        b.alpha_composite(img.resize((dw,dh),Image.BICUBIC,box=src),(int(round(dst[0])),int(round(dst[1]))))
        X=60
        def R(v0):return rv(u,0.55,v0)
        show(b,Pp["pot"],X,766,R(0.75));kicker4(b,"姐夫開煮",X+86,780,1.0,v=R(0.75),col=DCOP,size=42,lcol=DCOP,sh=False)
        show_rise(b,T3("無水雞湯","serif","600SemiBold",120,GRN,8,False),X-2,836,R(0.85))
        show_rise(b,T3("5 種食材｜60 分鐘","serif","600SemiBold",42,INK2,2,False),X,978,R(0.95))
        L=960*ease(clamp((u-1.0)/0.6))
        if L>3:show(b,bare_line(L,2,RULE),X,1044)
        show_rise(b,T3("材料","serif","700Bold",42,DCOP,6,False),X,1074,R(1.05))
        for j,rw in enumerate(Pp["rows"]):
            col,row=(0,j) if j<3 else (1,j-3);x=190+col*480;y=1068+row*66
            show_rise(b,rw,x,y,R(1.1+j*0.07))
        L2=960*ease(clamp((u-1.45)/0.6))
        if L2>3:show(b,bare_line(L2,2,RULE),X,1276)
        show_rise(b,T3("做法","serif","700Bold",42,DCOP,6,False),X,1302,R(1.5))
        show_rise(b,T3("依序鋪好食材，不加水，","serif","500Medium",40,INK,1,False),190,1302,R(1.55))
        show_rise(b,T3("中火 20 分鐘轉小火 40 分鐘。","serif","500Medium",40,INK,1,False),190,1360,R(1.6))
        show_rise(b,T3("先收藏，下次照著煮","serif","700Bold",46,DCOP,6,False),X,1426,R(1.8))
        paste_mark(b);return b
if __name__=="__main__":
    if sys.argv[1]=="render":Mag4().render(SP+"soup/姐夫開煮_無水雞湯_日系雜誌_v4.mp4")
    elif sys.argv[1]=="sheet":
        V=Mag4();ts=[float(x) for x in sys.argv[2].split(",")];ims=[V.still(t) for t in ts]
        cw=540;sh=Image.new("RGB",(cw*min(4,len(ims)),960*((len(ims)+3)//4)),(255,255,255))
        for i,im in enumerate(ims):sh.paste(im.resize((cw,960),Image.LANCZOS),((i%4)*cw,(i//4)*960))
        sh.save(SP+"soup/mag4_sheet.jpg",quality=86);print("ok")
