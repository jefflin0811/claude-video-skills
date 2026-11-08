# 質感版型：三個高級感方向（日系雜誌／東方雅緻／極簡留白），同一支無水雞湯剪輯，柔和弦樂
import sys,os,math,random
SP="__ROOT__/"
sys.path.insert(0,SP+"soup")
from base3 import *
from kit5 import SERIF,SANS,logo_h,CRM,COP,LCOP,TER,GRN,SAGE,CARD,ttext,shadow,paste,fade,put,blank
from PIL import ImageChops,ImageEnhance
try:FPS
except NameError:FPS=30
GBGM="__ROOT__/music/食品開箱_gourmet-flavors.mp3"
WHITE=(255,255,255);P=44;DIS=0.3
# ---------------- type helpers ----------------
_FC={}
def font(kind,w,size):
    k=(kind,w,size)
    if k not in _FC:_FC[k]=SERIF(w,size) if kind=="serif" else SANS(w,size)
    return _FC[k]
def crop_vis(im):return im.crop(im.getchannel("A").getbbox())
def tx(text,f,col=WHITE,track=0):
    ws=[f.getlength(c) for c in text];asc,desc=f.getmetrics();pad=10
    im=blank(sum(ws)+track*max(0,len(text)-1)+2*pad,asc+desc+2*pad);d=ImageDraw.Draw(im);x=pad
    for c,w in zip(text,ws):d.text((x,pad),c,font=f,fill=col+(255,));x+=w+track
    return crop_vis(im)
def vtx(text,f,col=WHITE,lead=1.04):
    s=f.size;im=blank(s*1.4,len(text)*s*lead+20);d=ImageDraw.Draw(im)
    for i,c in enumerate(text):d.text((im.size[0]/2,10+i*s*lead+s/2),c,font=f,fill=col+(255,),anchor="mm")
    return crop_vis(im)
def ink(im,b1=16,a1=0.42,b2=3,a2=0.42,dy=2):
    W,H=im.size[0]+2*P,im.size[1]+2*P;A=Image.new("L",(W,H),0);A.paste(im.getchannel("A"),(P,P))
    s1=A.filter(ImageFilter.GaussianBlur(b1)).point(lambda v:int(v*a1))
    A2=Image.new("L",(W,H),0);A2.paste(im.getchannel("A"),(P,P+dy));s2=A2.filter(ImageFilter.GaussianBlur(b2)).point(lambda v:int(v*a2))
    out=Image.new("RGBA",(W,H),(18,12,8,0));out.putalpha(ImageChops.lighter(s1,s2));out.alpha_composite(im,(P,P));return out
def bare(im):o=blank(im.size[0]+2*P,im.size[1]+2*P);o.alpha_composite(im,(P,P));return o
def vis(im):return im.size[0]-2*P,im.size[1]-2*P
_IC={}
def T(text,kind,w,size,col=WHITE,track=0,sh=True):
    k=("h",text,kind,w,size,col,round(track*2)/2,sh)
    if k not in _IC:
        im=tx(text,font(kind,w,size),col,round(track*2)/2);_IC[k]=ink(im) if sh else bare(im)
    return _IC[k]
def VT(text,kind,w,size,col=WHITE,lead=1.04):
    k=("v",text,kind,w,size,col,lead)
    if k not in _IC:_IC[k]=ink(vtx(text,font(kind,w,size),col,lead))
    return _IC[k]
def show(base,im,x,y,a=1.0):
    if a>0.003:paste(base,fade(im,min(a,1.0)),x-P,y-P)
def rv(u,d=0.5,delay=0.0):return ease(clamp((u-delay)/d))
def wipe(im,v,soft=90):
    """top-to-bottom soft reveal (brush feel) for vertical type"""
    if v>=1:return im
    H=im.size[1];edge=v*(H+soft)-soft;y=np.arange(H,dtype=np.float32)
    m=np.clip((edge-y)/soft+1,0,1)*255;M=Image.fromarray(np.tile(m.astype(np.uint8)[:,None],(1,im.size[0])))
    o=im.copy();o.putalpha(ImageChops.multiply(im.getchannel("A"),M));return o
_LC={}
def hline(w,h=3,col=WHITE):
    w=max(2,int(w));k=("hl",w,h,col)
    if k not in _LC:im=blank(w,h);ImageDraw.Draw(im).rectangle((0,0,w,h),fill=col+(255,));_LC[k]=ink(im,6,0.35,2,0.3,1)
    return _LC[k]
def vline(h,w=3,col=WHITE):
    h=max(2,int(h));k=("vl",h,w,col)
    if k not in _LC:im=blank(w,h);ImageDraw.Draw(im).rectangle((0,0,w,h),fill=col+(255,));_LC[k]=ink(im,6,0.35,2,0.3,1)
    return _LC[k]
# ---------------- fine line-art (small illustrations) ----------------
def fine_pot(h=70,col=WHITE,sw=3.2,k=4):
    S=100;im=blank(S*k,S*k);d=ImageDraw.Draw(im);w=int(sw*k*100/h)
    def Q(x,y):return (x*k,y*k)
    d.arc(Q(18,30)+Q(82,92),0,180,fill=col+(255,),width=w);d.line([Q(18,61),Q(18,50)],fill=col+(255,),width=w);d.line([Q(82,61),Q(82,50)],fill=col+(255,),width=w)
    d.line([Q(10,50),Q(90,50)],fill=col+(255,),width=w);d.arc(Q(22,34)+Q(78,66),180,360,fill=col+(255,),width=w)
    d.ellipse(Q(46,28)+Q(54,36),outline=col+(255,),width=w)
    for x in (40,60):d.line([Q(x+3*math.sin(i/10*math.pi*2),24-i*1.6) for i in range(11)],fill=col+(255,),width=w,joint="curve")
    d.arc(Q(4,56)+Q(18,68),90,270,fill=col+(255,),width=w);d.arc(Q(82,56)+Q(96,68),270,90,fill=col+(255,),width=w)
    return crop_vis(im.resize((h,h),Image.LANCZOS))
POT70=ink(fine_pot(70),8,0.35,2,0.35,1);POT58=ink(fine_pot(58,WHITE,2.6),8,0.35,2,0.35,1)
_SG=np.clip(np.linspace(0,1.25,130),0,1)[:,None]
def steam(t,h=130,col=WHITE,sw=3.0,k=3):
    W=int(h*0.8);im=blank(W*k,h*k);d=ImageDraw.Draw(im);w=int(sw*k)
    for j,x in enumerate((0.36,0.64)):
        ph=t*2.2+j*1.7
        pts=[(k*(W*x+W*0.09*math.sin(i/22*math.pi*2.4+ph)),k*(h-4-i*(h-8)/22)) for i in range(23)];d.line(pts,fill=col+(255,),width=w,joint="curve")
    im=im.resize((W,h),Image.LANCZOS);a=np.asarray(im.getchannel("A")).astype(np.float32)
    g=np.clip(np.linspace(0,1.3,h),0,1)[:,None];im.putalpha(Image.fromarray((a*g).astype(np.uint8)))
    return ink(im,8,0.35,2,0.3,1)
def seal(chars,s=100,col=TER,fg=CRM,seed=2):
    k=3;S=s*k;im=blank(S,S);d=ImageDraw.Draw(im);d.rounded_rectangle((0,0,S-1,S-1),radius=int(S*.07),fill=col+(255,))
    m=int(S*.075);d.rounded_rectangle((m,m,S-m,S-m),radius=int(S*.04),outline=fg+(255,),width=max(2,int(S*.022)))
    n=len(chars)
    if n==1:d.text((S/2,S/2+k*2),chars,font=font("serif","900Black",int(S*.56)),fill=fg+(255,),anchor="mm")
    elif n==2:
        f=font("serif","900Black",int(S*.35))
        for i,c in enumerate(chars):d.text((S/2,S*(0.315+0.37*i)),c,font=f,fill=fg+(255,),anchor="mm")
    else:
        f=font("serif","900Black",int(S*.33))
        for i,c in enumerate(chars):d.text((S*(0.69 if i<2 else 0.31),S*(0.32+0.36*(i%2))),c,font=f,fill=fg+(255,),anchor="mm")
    rng=np.random.default_rng(seed);a=np.asarray(im.getchannel("A")).astype(np.float32)
    nz=Image.fromarray((rng.random((S//6,S//6))*255).astype(np.uint8)).resize((S,S),Image.BICUBIC);nz=np.asarray(nz).astype(np.float32)/255
    im.putalpha(Image.fromarray(np.clip(a*np.clip(0.55+nz*0.9,0,1)**0.45,0,255).astype(np.uint8)))
    return im.resize((s,s),Image.LANCZOS)
def pbar(n,k,frac,seg=62,gap=10,h=4):
    im=blank(n*seg+(n-1)*gap,h);d=ImageDraw.Draw(im)
    for i in range(n):
        x=i*(seg+gap);d.rectangle((x,0,x+seg-1,h-1),fill=(255,255,255,96))
        f=1.0 if i<k else (frac if i==k else 0.0)
        if f>0:d.rectangle((x,0,x+int((seg-1)*f),h-1),fill=(255,255,255,255))
    return ink(im,5,0.3,1,0.3,1)
# ---------------- grade + shade ----------------
def make_grade(sat,lift,tint,tint_a,gamma=1.0):
    lut=[]
    for c in range(3):
        for v in range(256):
            x=v/255;y=lift+(1-lift)*(x**gamma);y=y*(1-tint_a)+tint[c]/255*tint_a;lut.append(int(round(min(max(y,0),1)*255)))
    def g(img):
        img=img.point(lut)
        return ImageEnhance.Color(img).enhance(sat) if abs(sat-1)>0.01 else img
    return g
def low_shade(y0=900,amax=0.48,left=0.0):
    yy=np.clip((np.arange(OH)-y0)/(OH-y0),0,1)**1.4*amax;A=np.tile(yy[:,None],(1,OW))
    if left>0:
        xx=np.clip(1-np.arange(OW)/460,0,1)**1.6*left;band=np.clip(1-np.abs(np.arange(OH)-1250)/430,0,1)[:,None];A=np.maximum(A,xx[None,:]*np.clip(band*1.6,0,1))
    im=Image.new("RGBA",(OW,OH),(14,10,6,0));im.putalpha(Image.fromarray((A*255).astype(np.uint8)));return im
STEPS=[("s1","01","壹","第一層","首先洋蔥鋪底"),("s2","02","貳","第二層","再鋪上白菜"),("s3","03","參","第三層","兩隻帶骨大雞腿"),
       ("s4","04","肆","第四層","一個蘋果＋一根玉米"),("s5","05","伍","開火",("中火 20 分鐘","轉小火 40 分鐘"))]
# ---------------- shared video base ----------------
class Prem(Base):
    name="x";grade_fn=None;SHADE=None
    def __init__(s):
        wd=SP+f"soup/prem_{s.name}";os.makedirs(wd,exist_ok=True)
        for f in ("video.mp4","cut.json"):
            p=os.path.join(wd,f)
            if not os.path.exists(p):os.symlink(SP+"soup/build2/"+f,p)
        Video.__init__(s,wd,GBGM,end=END_D,bgmvol=1.0,line="");s.off=0.0;s.held={}
        s.cuts=[s.vo(k) for k in ("s1","s2","s3","s4","s5","s6a","s6b")]
        for k in ("hook","s1","s2","s3","s4","s5","s6a","s6b"):s.cam.append((s.vo(k),s.ve(k),1.0,1.035,540,960))
        f=s.vo("s6a");M=s.MAIN
        s.ev=[(f+0.1+0.75,CHM,.14),(M+0.45,CHM,.18)]
    def camera(s,t):
        for t0,t1,z0,z1,x,y in s.cam:
            if t0<=t<t1:return z0+(z1-z0)*clamp((t-t0)/(t1-t0)),x,y,0,0
        return 1.0,540,960,0,0
    def cam_tf(s,img,t):
        z,cx,cy,_,_=s.camera(t)
        if z>1.001:
            w2,h2=OW/z,OH/z;x0=min(max(cx-w2/2,0),OW-w2);y0=min(max(cy-h2/2,0),OH-h2)
            img=img.resize((OW,OH),Image.BICUBIC,box=(x0,y0,x0+w2,y0+h2))
        return s.grade_fn(img) if s.grade_fn else img
    def compose(s,img,t):
        img=s.cam_tf(img,t)
        for c in s.cuts:
            if c-1.5/FPS<=t<c:s.held[c]=img
            elif c<=t<c+DIS:
                h=s.held.get(c)
                if h is None:tp=c-1/FPS;h=s.cam_tf(s.frame_at(tp),tp);s.held[c]=h
                img=Image.blend(h,img,ease((t-c)/DIS))
        img=img.convert("RGBA");s.overlay(img,t);return img.convert("RGB")
    def extra(s,base,t):base.alpha_composite(s.SHADE)
    def persist(s,base,t):pass
    def extra_top(s,base,t):
        h=s.ve("hook")
        if t<h:s.d_open(base,t,clamp((h-0.04-t)/0.25))
        for i,(k,num,cn,kick,txt) in enumerate(STEPS):
            a0=s.vo(k)+0.12;a1=s.ve(k)-0.02
            if not(a0<=t<a1):continue
            af=clamp((a1-t)/0.22);uf=t-a0
            if k=="s5":
                sp=s.vo("s5")+4*B
                if t<sp:s.d_step(base,i,num,cn,kick,txt[0],uf,af,uf,min(af,clamp((sp-0.02-t)/0.2)))
                else:s.d_step(base,i,num,cn,kick,txt[1],uf,af,t-sp,af)
            else:s.d_step(base,i,num,cn,kick,txt,uf,af,uf,af)
        s.persist(base,t)
        f=s.vo("s6a")
        if t>=f+0.1:s.d_fin(base,t-(f+0.1))
    def endparts(s,last):return Image.new("RGBA",(OW,OH),CRM+(255,)),dict(last=last.convert("RGBA"),logo=logo_h(460))
    def end_blend(s,P,b,u):return Image.blend(P["last"],b,ease(u/0.3)) if u<0.3 else b
    def still(s,t):
        if t<s.MAIN:return s.compose(s.frame_at(t),t)
        bg,Pp=s.endparts(s.compose(s.frame_at(s.MAIN-0.1),s.MAIN-0.1).convert("RGBA"));return s.endframe(bg,Pp,t-s.MAIN).convert("RGB")
# ---------------- 質感 1｜日系雜誌 ----------------
class Mag(Prem):
    name="mag";grade_fn=staticmethod(make_grade(0.9,0.05,(246,240,228),0.05));SHADE=low_shade()
    def d_open(s,base,t,a):
        X=58;show(base,POT70,X,1118,a);show(base,T("姐夫開煮","serif","500Medium",40,WHITE,14),X+90,1136,a)
        show(base,hline(96+44*ease(t/2.3)),X,1214,a)
        show(base,T("無水雞湯","serif","600SemiBold",138,WHITE,10+8*clamp(t/2.3)),X-4,1240,a)
        show(base,T("洋蔥・白菜・雞腿・蘋果・玉米","serif","400Regular",34,WHITE,6),X,1414,a*0.96)
    def d_step(s,base,i,num,cn,kick,text,uf,af,ut,at_):
        X=54;v=rv(uf,0.6);show(base,T(num,"serif","200ExtraLight",124,LCOP,4),X,1248+(1-v)*14,af*v)
        L=134*ease(clamp((uf-0.1)/0.45))
        if L>3:show(base,vline(L),X+152,1240,af)
        v2=rv(uf,0.45,0.12);show(base,T(kick,"serif","500Medium",32,LCOP,10),X+182,1248+(1-v2)*12,af*v2)
        v3=rv(ut,0.5,0.2);show(base,T(text,"serif","600SemiBold",58,WHITE,4),X+182,1302+(1-v3)*14,at_*v3)
    def d_fin(s,base,u):
        X=58;v=rv(u,0.6);show(base,T("一鍋鮮甜美味的雞湯","serif","500Medium",50,WHITE,6),X,1182+(1-v)*14,v)
        L=110*ease(clamp((u-0.5)/0.45))
        if L>3:show(base,hline(L),X,1262)
        v2=ease(clamp((u-0.7)/0.9))
        if v2>0:show(base,T("上桌了","serif","600SemiBold",128,WHITE,14+20*(1-v2)),X-4,1302+(1-v2)*10,v2)
    def endparts(s,last):
        bg,Pp=super().endparts(last);Pp["line"]=tx("姐夫嚴選為您挑選",font("serif","600SemiBold",62),COP,10);return bg,Pp
    def endframe(s,bg,Pp,u):
        b=bg.copy();v=ease(clamp(u/0.6));put(b,Pp["logo"],540,800-(1-v)*10,v)
        Ln=Pp["line"];v2=ease(clamp((u-0.35)/0.5));put(b,Ln,540,1238+(1-v2)*12,v2)
        r=ease(clamp((u-0.65)/0.5));hw=Ln.size[0]/2;d=ImageDraw.Draw(b)
        if r>0.02:
            d.line([(540-hw-40-90*r,1240),(540-hw-40,1240)],fill=COP+(255,),width=2);d.line([(540+hw+40,1240),(540+hw+40+90*r,1240)],fill=COP+(255,),width=2)
        return s.end_blend(Pp,b,u)
# ---------------- 質感 2｜東方雅緻 ----------------
SEAL4=seal("姐夫開煮",112,seed=4);SEALN=[seal(c,96,seed=10+i) for i,c in enumerate("壹貳參肆伍")];SEAL2=seal("嚴選",84,seed=7)
def stamp(base,im,cx,cy,u,a=1.0):
    v=ease(clamp(u/0.28))
    if v>0:put(base,im,cx,cy,a*clamp(u/0.12),1.22-0.22*v)
class Ori(Prem):
    name="ori";grade_fn=staticmethod(make_grade(1.0,0.03,(250,232,205),0.05));SHADE=low_shade(left=0.30)
    CX=140
    def d_open(s,base,t,a):
        title=VT("無水雞湯","serif","700Bold",116,WHITE,1.02);w,h=vis(title);top=1024;cx=s.CX
        show(base,steam(t),cx-52,top-158,a);show(base,title,cx-w//2,top,a)
        show(base,vline(268,2,LCOP),cx+w//2+36,top+14,a*0.95)
        put(base,SEAL4,cx+w//2+36+64,top+h-56,a)
    def d_step(s,base,i,num,cn,kick,text,uf,af,ut,at_):
        X=58;stamp(base,SEALN[i],X+48,1310,uf,af)
        v3=rv(ut,0.5,0.15);im=T(text,"serif","600SemiBold",60,WHITE,6);w,h=vis(im)
        show(base,im,X+124-(1-v3)*18,1310-h//2,at_*v3)
    def d_fin(s,base,u):
        sm=VT("一鍋鮮甜美味的雞湯","serif","600SemiBold",46,WHITE,1.06);ws,hs=vis(sm);top=1018
        v=clamp(u/1.0)
        if v>0:show(base,wipe(sm,ease(v)),302-ws//2,top)
        big=VT("上桌了","serif","700Bold",126,WHITE,1.02);wb,hb=vis(big);v2=clamp((u-0.75)/0.9)
        if v2>0:show(base,wipe(big,ease(v2)),s.CX-wb//2,1062)
    def endparts(s,last):
        bg,Pp=super().endparts(last);Pp["line"]=tx("姐夫嚴選為您挑選",font("serif","700Bold",60),COP,10);return bg,Pp
    def endframe(s,bg,Pp,u):
        b=bg.copy();v=ease(clamp(u/0.6));put(b,Pp["logo"],540,790-(1-v)*10,v)
        Ln=Pp["line"];v2=ease(clamp((u-0.35)/0.5));x0=540-(Ln.size[0]+20+84)/2
        paste(b,fade(Ln,v2),x0,1238-Ln.size[1]/2+(1-v2)*12)
        stamp(b,SEAL2,x0+Ln.size[0]+20+42,1238,u-0.8)
        return s.end_blend(Pp,b,u)
# ---------------- 質感 3｜極簡留白 ----------------
class Mini(Prem):
    name="min";grade_fn=staticmethod(make_grade(0.9,0.04,(244,244,240),0.05));SHADE=low_shade()
    # centered composition: everything on the vertical center line, lots of air
    def c(s,base,im,top,a=1.0):show(base,im,540-vis(im)[0]//2,top,a)
    def d_open(s,base,t,a):
        s.c(base,POT58,1094,a);s.c(base,T("姐夫開煮","sans","400Regular",34,WHITE,20),1176,a)
        s.c(base,T("無水雞湯","sans","300Light",126,WHITE,30),1232,a)
    def persist(s,base,t):
        f=s.vo("s6a");x=540-(5*62+4*10)//2
        if t<f+0.1:
            k=0;frac=0.0
            for i,(key,*_) in enumerate(STEPS):
                if t>=s.vo(key)+0.12:k=i;frac=ease(clamp((t-s.vo(key)-0.32)/0.6))
            if t<s.vo("s1")+0.12:show(base,pbar(5,0,0),x,1404);return
            show(base,pbar(5,k,frac),x,1404)
        else:show(base,pbar(5,5,0),x,1404,clamp((f+0.1+0.9-t)/0.4))
    def d_step(s,base,i,num,cn,kick,text,uf,af,ut,at_):
        v=rv(uf,0.5);s.c(base,T(f"{num}／05","sans","300Light",40,LCOP,6),1236+(1-v)*10,af*v)
        v3=rv(ut,0.5,0.12);s.c(base,T(text,"sans","400Regular",58,WHITE,8),1298+(1-v3)*12,at_*v3)
    def d_fin(s,base,u):
        v=rv(u,0.6);s.c(base,T("一鍋鮮甜美味的雞湯","sans","400Regular",42,WHITE,12),1200+(1-v)*10,v)
        v2=rv(u,0.8,0.6);s.c(base,T("上桌了","sans","300Light",120,WHITE,34),1270+(1-v2)*14,v2)
    def endparts(s,last):
        bg,Pp=super().endparts(last);Pp["logo"]=logo_h(440);Pp["line"]=tx("姐夫嚴選為您挑選",font("sans","400Regular",52),COP,18);return bg,Pp
    def endframe(s,bg,Pp,u):
        b=bg.copy();v=ease(clamp(u/0.7));put(b,Pp["logo"],540,800,v)
        v2=ease(clamp((u-0.4)/0.6));put(b,Pp["line"],540,1236,v2)
        r=ease(clamp((u-0.8)/0.5))
        if r>0.02:ImageDraw.Draw(b).line([(540-40*r,1312),(540+40*r,1312)],fill=COP+(255,),width=2)
        return s.end_blend(Pp,b,u)
STY={"mag":Mag,"ori":Ori,"min":Mini}
TITLES={"mag":"質感版型1_日系雜誌","ori":"質感版型2_東方雅緻","min":"質感版型3_極簡留白"}
def board(out):
    rows=[("質感 1","日系雜誌",["襯線字（思源宋體）","細線、01～05 大編號","霧面柔和色調","像生活風格雜誌"],Mag()),
          ("質感 2","東方雅緻",["直排宋體大字","紅色印章、壹貳參肆伍","暖色調","有老店、職人的味道"],Ori()),
          ("質感 3","極簡留白",["細黑體、字距拉開","步驟進度條","乾淨明亮","像精品品牌"],Mini())]
    TS=[0.6,11.9,21.6,None]
    FW,FH=460,818;G=34;LW=400;W=LW+4*(FW+G)+30;RH=FH+96;H=300+len(rows)*RH+20
    bd=Image.new("RGBA",(W,H),CRM+(255,));put(bd,logo_h(120),100,118)
    paste(bd,ttext("姐夫嚴選｜質感版型範例",SANS("900Black",56),GRN+(255,)),180,62)
    paste(bd,ttext("三種都照規則走：開頭字在螢幕三分之二處＋小插畫、左上角半透明圓形標誌、上方不放字、片尾銅色字",SANS("500Medium",28),SAGE+(255,)),182,140)
    labels=["開頭","步驟","上桌","片尾"]
    for r,(kk,name,desc,V) in enumerate(rows):
        y=300+r*RH
        paste(bd,ttext(kk,SANS("700Bold",30),COP+(255,)),44,y+30);paste(bd,ttext(name,SERIF("700Bold",58),GRN+(255,)),40,y+78)
        yy=y+178
        for ln in desc:paste(bd,ttext("・"+ln,SANS("500Medium",27),SAGE+(255,)),44,yy);yy+=48
        for i,t in enumerate(TS):
            fr=V.still(t if t is not None else V.MAIN+1.6);fr.save(f"{out}/{V.name}_{i}.jpg",quality=90)
            x=LW+i*(FW+G);f=fr.convert("RGBA").resize((FW,FH),Image.LANCZOS);ImageDraw.Draw(f).rectangle((0,0,FW-1,FH-1),outline=(214,206,192,255),width=2)
            bd.alpha_composite(shadow(f,12,(0,6),0.22),(x-24,y-24))
            if r==0:put(bd,ttext(labels[i],SANS("700Bold",30),SAGE+(255,)),x+FW/2,y-40)
    bd.convert("RGB").save(out+"/姐夫嚴選_質感版型範例.jpg",quality=88);print(bd.size)
if __name__=="__main__":
    if sys.argv[1]=="board":board(sys.argv[2])
    elif sys.argv[1]=="render":
        V=STY[sys.argv[2]]();V.render(SP+f"soup/姐夫開煮_無水雞湯_{TITLES[V.name]}.mp4")
    elif sys.argv[1]=="sheet":
        V=STY[sys.argv[2]]();ts=[float(x) for x in sys.argv[3].split(",")];ims=[V.still(t).resize((360,640)) for t in ts]
        sh=Image.new("RGB",(len(ims)*366,640),(255,255,255))
        for i,im in enumerate(ims):sh.paste(im,(i*366,0))
        sh.save(SP+f"soup/prem_{V.name}_sheet.jpg",quality=86);print("ok")
