# 開煮｜日系雜誌 v3 — legibility pass: every word readable on a phone over bright footage
# - size floor ~38-40 px on footage, heavier weight (serif 600), minimal tracking on small type
# - warm-white type with a tight dark edge + a soft glow that follows the letter shapes (no boxes)
# - copper/gold only for the big numerals and thin lines; recipe page uses deeper copper + darker ink
import sys,os,math
SP="__ROOT__/"
sys.path.insert(0,SP+"soup")
from magv2 import *
GOLD=(238,192,128);DCOP=(146,92,52);INK2=(78,86,80)
_I3={}
def ink2(im,d=7,b=14,ga=0.5,ea=0.62,col=(16,11,8)):
    W,H=im.size[0]+2*P,im.size[1]+2*P;A=Image.new("L",(W,H),0);A.paste(im.getchannel("A"),(P,P))
    g=A.filter(ImageFilter.MaxFilter(d|1)).filter(ImageFilter.GaussianBlur(b)).point(lambda v:int(v*ga))
    e=A.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1.4)).point(lambda v:int(v*ea))
    out=Image.new("RGBA",(W,H),col+(0,));out.putalpha(ImageChops.lighter(g,e));out.alpha_composite(im,(P,P));return out
def halo(im,size):
    if size<52:return ink2(im,7,12,0.56,0.66)
    if size<90:return ink2(im,7,16,0.5,0.6)
    return ink2(im,9,22,0.42,0.5)
def T3(text,kind,w,size,col=WARM,track=0,sh=True):
    k=(text,kind,w,size,col,round(track*2)/2,sh)
    if k not in _I3:
        im=tx(text,font(kind,w,size),col,round(track*2)/2);_I3[k]=halo(im,size) if sh else bare(im)
    return _I3[k]
def num3(s):
    k=("num3",s)
    if k not in _I3:
        im=blank(GARA_I.getlength(s)+40,260);ImageDraw.Draw(im).text((10,10),s,font=GARA_I,fill=GOLD+(255,));_I3[k]=ink2(crop_vis(im),9,18,0.46,0.55)
    return _I3[k]
def line3(w,h,col=WARM):
    w=max(2,int(w));h=max(2,int(h));k=("ln",w,h,col)
    if k not in _I3:im=blank(w,h);ImageDraw.Draw(im).rectangle((0,0,w,h),fill=col+(255,));_I3[k]=ink2(im,5,8,0.45,0.6)
    return _I3[k]
def kicker3(base,text,x,y,a,v=1.0,col=WARM,size=40,lcol=GOLD,sh=True):
    im=T3(text,"serif","600SemiBold",size,col,4,sh);w,h=vis(im);show_rise(base,im,x,y,v,a)
    L=44*ease(clamp((v-0.3)/0.7))
    if L>2:show(base,line3(L,3,lcol) if sh else bare_line(L,3,lcol),x+w+18,y+h//2-1,a)
# ---------------- cooking timeline: two big labels, thick progress, no tiny numbers ----------------
def timeline3(base,prog,a):
    if a<=0.003:return
    W0=540;lay=blank(W0+80,130);d=ImageDraw.Draw(lay);ox,oy=20,92
    x20=ox+W0*20/60;xe=ox+W0
    d.line([(ox,oy),(xe,oy)],fill=WARM+(170,),width=4)
    for x in (ox,x20,xe):d.line([(x,oy-11),(x,oy+11)],fill=WARM+(235,),width=3)
    px=ox+W0*prog/60
    if prog>0.2:d.line([(ox,oy),(px,oy)],fill=GOLD+(255,),width=9)
    d.ellipse((px-10,oy-10,px+10,oy+10),fill=WARM+(255,))
    f=font("serif","600SemiBold",36)
    on1=WARM if prog<20.5 else WARM;d.text(((ox+x20)/2,oy-24),"中火 20 分",font=f,fill=on1+(255,),anchor="md")
    d.text(((x20+xe)/2,oy-24),"小火 40 分",font=f,fill=WARM+(255 if prog>20.5 else 205,),anchor="md")
    show(base,ink2(lay,7,12,0.55,0.62),TL_X0-20-24,1452-oy,a)
def leader3(name,amount,w,size=38):
    fn=font("serif","500Medium",size);fa=font("serif","600SemiBold",size)
    a=tx(name,fn,INK,1);b=tx(amount,fa,DCOP,1);H=max(a.size[1],b.size[1])+8;im=blank(w,H+8)
    im.alpha_composite(a,(0,H-a.size[1]));im.alpha_composite(b,(w-b.size[0],H-b.size[1]));d=ImageDraw.Draw(im)
    x=a.size[0]+16;xe=w-b.size[0]-16;cy=H-9
    while x<xe:d.ellipse((x-2,cy-2,x+2,cy+2),fill=DOT+(255,));x+=12
    return bare(im)
PAGE3=(60,250,1020,780)
POT3=ink2(fine_pot(78,WARM,3.4),5,10,0.5,0.6)
def airy3(img):
    img=ImageEnhance.Color(img.point(LUT)).enhance(0.9)
    sm=img.resize((OW//6,OH//6),Image.BILINEAR).filter(ImageFilter.GaussianBlur(5)).point([int(v*0.72) for v in BLOOM_LUT]).resize((OW,OH),Image.BILINEAR)
    return ImageChops.screen(img,sm)
class Mag3(Mag2):
    name="mag3";grade_fn=staticmethod(airy3);SHADE=low_shade(880,0.5)
    def d_open(s,base,t,a):
        X=58;show(base,POT3,X,1098,a)
        lab=T3("姐夫開煮","serif","600SemiBold",46,WARM,8);show(base,lab,X+98,1114,a)
        lx=X+98+vis(lab)[0]+22;show(base,line3(3,40),lx,1118,a)
        show(base,T3("5 種食材・60 分鐘","serif","600SemiBold",38,WARM,2),lx+22,1120,a)
        show(base,line3(96+44*ease(t/2.3),4),X,1204,a)
        show(base,T3("無水雞湯","serif","600SemiBold",138,WARM,10+8*clamp(t/2.3)),X-4,1232,a)
        show(base,T3("洋蔥・白菜・雞腿・蘋果・玉米","serif","600SemiBold",40,WARM,4),X,1406,a)
    def d_step(s,base,i,num,cn,kick,text,uf,af,ut,at_):
        X=50;nm=num3(num);nw,nh=vis(nm);v=rv(uf,0.6);show(base,nm,X,1214+(1-v)*16,af*v)
        rx=X+nw+24;L=150*ease(clamp((uf-0.1)/0.45))
        if L>3:show(base,line3(3,L),rx,1226,af)
        tx0=rx+30;kicker3(base,kick,tx0,1232,af,v=rv(uf,0.5,0.12))
        show_rise(base,T3(text,"serif","600SemiBold",66,WARM,3),tx0,1292,rv(ut,0.6,0.22),at_)
        if i==4:
            sp=s.vo("s5")+4*B;t=s.vo("s5")+0.12+uf
            p=20*ease(clamp((uf-0.35)/1.1)) if t<sp else 20+40*ease(clamp((t-sp-0.1)/1.5))
            timeline3(base,p,af*rv(uf,0.5,0.3))
    def d_fin(s,base,u):
        X=58;kicker3(base,"60 分鐘後",X,1108,1.0,v=rv(u,0.5),size=42)
        show_rise(base,T3("一鍋鮮甜美味的雞湯","serif","600SemiBold",58,WARM,4),X,1172,rv(u,0.6,0.15))
        L=110*ease(clamp((u-0.55)/0.45))
        if L>3:show(base,line3(L,4),X,1264)
        v2=ease(clamp((u-0.75)/0.9))
        if v2>0:show_rise(base,T3("上桌了","serif","600SemiBold",128,WARM,14+20*(1-v2)),X-4,1302,v2,dist=60)
    def endparts(s,last):
        bg,Pp=super().endparts(last)
        c=(PAGE3[2]-PAGE3[0])/(PAGE3[3]-PAGE3[1]);ch=OW/c;cy=1000;Pp["crop"]=(0,cy-ch/2,OW,cy+ch/2)
        Pp["rows"]=[leader3("洋蔥","鋪滿鍋底",410),leader3("白菜","鋪一層",410),leader3("帶骨大雞腿","2 隻",410),leader3("蘋果","1 個",368),leader3("玉米","1 根",368)]
        Pp["pot"]=bare(fine_pot(62,DCOP,3.0));return bg,Pp
    def recipe(s,Pp,u):
        b=Image.new("RGBA",(OW,OH),CRM+(255,));t=ease(clamp(u/0.75))
        src1=Pp["crop"];k=0.04*clamp((u-0.75)/(RP-0.75))
        cx=(src1[0]+src1[2])/2;cy=(src1[1]+src1[3])/2;hw=(src1[2]-src1[0])/2*(1-k);hh=(src1[3]-src1[1])/2*(1-k)
        src=tuple(a0+(a1-a0)*t for a0,a1 in zip((0,0,OW,OH),(cx-hw,cy-hh,cx+hw,cy+hh)))
        dst=tuple(a0+(a1-a0)*t for a0,a1 in zip((0,0,OW,OH),PAGE3))
        img=Pp["clean"] if u>=0.22 else Image.blend(Pp["last"],Pp["clean"],ease(u/0.22))
        dw,dh=int(round(dst[2]-dst[0])),int(round(dst[3]-dst[1]))
        b.alpha_composite(img.resize((dw,dh),Image.BICUBIC,box=src),(int(round(dst[0])),int(round(dst[1]))))
        X=60
        def R(v0):return rv(u,0.55,v0)
        show(b,Pp["pot"],X,806,R(0.75));kicker3(b,"姐夫開煮",X+80,820,1.0,v=R(0.75),col=DCOP,size=38,lcol=DCOP,sh=False)
        show_rise(b,T3("無水雞湯","serif","600SemiBold",110,GRN,8,False),X-2,870,R(0.85))
        show_rise(b,T3("5 種食材｜60 分鐘","serif","600SemiBold",38,INK2,2,False),X,1004,R(0.95))
        L=960*ease(clamp((u-1.0)/0.6))
        if L>3:show(b,bare_line(L,2,RULE),X,1066)
        show_rise(b,T3("材料","serif","700Bold",38,DCOP,6,False),X,1094,R(1.05))
        for j,rw in enumerate(Pp["rows"]):
            col,row=(0,j) if j<3 else (1,j-3);x=182+col*470;y=1090+row*64
            show_rise(b,rw,x,y,R(1.1+j*0.07))
        L2=960*ease(clamp((u-1.45)/0.6))
        if L2>3:show(b,bare_line(L2,2,RULE),X,1300)
        show_rise(b,T3("做法","serif","700Bold",38,DCOP,6,False),X,1326,R(1.5))
        show_rise(b,T3("依序鋪好食材，不加水，","serif","500Medium",36,INK,1,False),182,1326,R(1.55))
        show_rise(b,T3("中火 20 分鐘轉小火 40 分鐘。","serif","500Medium",36,INK,1,False),182,1378,R(1.6))
        show_rise(b,T3("先收藏，下次照著煮","serif","700Bold",40,DCOP,6,False),X,1440,R(1.8))
        paste_mark(b);return b
def compare(out):
    A=Mag2();Bv=Mag3();M=A.MAIN
    ts=[(0.6,0.6),(11.9,11.9),(15.4,15.4),(21.6,21.6),(M+2.9,M+2.9)]
    labs=["開頭","步驟","開火","上桌","食譜頁"];FW,FH=420,747;G=26;LW=210
    W=LW+len(ts)*(FW+G)+20;H=250+2*(FH+70)+10
    bd=Image.new("RGBA",(W,H),CRM+(255,));put(bd,logo_h(110),90,104)
    paste(bd,ttext("開煮｜小字看得清楚的調整",SANS("900Black",50),GRN+(255,)),165,58)
    paste(bd,ttext("縮成手機大小比較：小字加大加粗、改用暖白字，字的邊緣加一圈很淡的深色光暈，不用底色塊",SANS("500Medium",26),SAGE+(255,)),167,126)
    for r,(V,name) in enumerate(((A,"調整前"),(Bv,"調整後"))):
        y=250+r*(FH+70);paste(bd,ttext(name,SANS("900Black",40),(COP if r==0 else GRN)+(255,)),36,y+FH//2-30)
        for i,(t0,t1) in enumerate(ts):
            fr=V.still(t0 if r==0 else t1).convert("RGB").resize((FW,FH),Image.LANCZOS)
            buf=io.BytesIO();fr.save(buf,"JPEG",quality=72);fr=Image.open(io.BytesIO(buf.getvalue())).convert("RGBA")
            ImageDraw.Draw(fr).rectangle((0,0,FW-1,FH-1),outline=(214,206,192,255),width=2);x=LW+i*(FW+G)
            bd.alpha_composite(shadow(fr,10,(0,5),0.22),(x-20,y-20))
            if r==0:put(bd,ttext(labs[i],SANS("700Bold",28),SAGE+(255,)),x+FW/2,y-26)
    bd.convert("RGB").save(out,quality=88);print(bd.size)
import io
if __name__=="__main__":
    if sys.argv[1]=="render":Mag3().render(SP+"soup/姐夫開煮_無水雞湯_日系雜誌_v3.mp4")
    elif sys.argv[1]=="compare":compare(sys.argv[2])
    elif sys.argv[1]=="sheet":
        V=Mag3();ts=[float(x) for x in sys.argv[2].split(",")];ims=[V.still(t) for t in ts]
        cw=540;sh=Image.new("RGB",(cw*min(4,len(ims)),960*((len(ims)+3)//4)),(255,255,255))
        for i,im in enumerate(ims):sh.paste(im.resize((cw,960),Image.LANCZOS),((i%4)*cw,(i//4)*960))
        sh.save(SP+"soup/mag3_sheet.jpg",quality=86);print("ok")
