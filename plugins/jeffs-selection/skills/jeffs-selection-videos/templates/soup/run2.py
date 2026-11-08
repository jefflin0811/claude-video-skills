# 姐夫嚴選｜無水雞湯 — recipe short in the round-5 brand system (logo top-left, #姐夫開箱 pill, left-aligned titles, step captions)
import sys,os,math
SP="__ROOT__/"
sys.path.insert(0,SP+"brand");sys.path.insert(0,SP+"eng");sys.path.insert(0,SP+"goose");sys.path.insert(0,SP+"work")
from kit5 import *
import sty,sfx,soundfile as sf
SP="__ROOT__/"
WD=SP+"soup/build2";os.makedirs(WD,exist_ok=True)
U="/mnt/user-data/uploads/";BGM="__ROOT__/music/食品開箱_joyful-sparks.mp3"
BEAT=0.5714;BGM_OFF=26.824;FPS=30
SEG=[("hook",U+"39532_1.mp4",2.10,4.40,4),
     ("s1",U+"39518_1.mp4",0.15,3.60,6),
     ("s2",U+"39521.mp4",0.15,2.45,4),
     ("s3",U+"39524_1.mp4",0.20,2.50,4),
     ("s4",U+"39525_1.mp4",0.25,3.70,6),
     ("s5",U+"39529_1.mp4",2.40,7.00,8,"crop=w=1214:h=2160:x='545+845*min(t/4.6,1)':y=0"),
     ("s6a",U+"39532_1.mp4",0.30,2.00,3),
     ("s6b",U+"39534_1.mp4",0.75,3.45,5)]
if "cut" in sys.argv:
    sys.path.insert(0,SP+"soup");import cutg2;print(cutg2.run(SEG,WD,BEAT,grade="colorbalance=rs=0.03:gs=0.01:bs=-0.04:rm=0.02:bm=-0.02,curves=all='0/0 0.25/0.33 0.5/0.62 0.75/0.86 1/1',eq=saturation=1.15"));sys.exit()
END_D=6*BEAT
def clamp(u):return min(max(u,0.0),1.0)
def ease(u):u=clamp(u);return 1-(1-u)**3
def spring(u):u=clamp(u);return 1-math.exp(-7*u)*math.cos(11*u)
def fadeim(im,a):
    if a>=0.999:return im
    c=im.copy();c.putalpha(c.getchannel("A").point(lambda v:int(v*a)));return c
def zoomimg(img,z,cx=540,cy=960):
    if z<=1.0001:return img
    w,h=OW/z,OH/z;x0=min(max(cx-w/2,0),OW-w);y0=min(max(cy-h/2,0),OH-h)
    return img.crop((int(x0),int(y0),int(x0+w),int(y0+h))).resize((OW,OH),Image.BILINEAR)
sys.path.insert(0,SP+"soup")
from open5 import doodle_pot,corner_shade,low_shade
CS=corner_shade(0.38);LS=low_shade(1000,0.26)
OPEN_L1=vis(tline("姐夫開煮",70,LCOP,9));OPEN_L2=vis(tline("無水雞湯",160,CRM,14,maxw=900))
OPEN_TXT=shadow(lstack([OPEN_L1,OPEN_L2],[8]),10,(0,6),0.45,(0,0,0))
OPEN_VH=OPEN_L1.size[1]+8+OPEN_L2.size[1];OPEN_TOP=int(1280-OPEN_VH/2)
_P0=doodle_pot(0.0,236);_pb=_P0.getchannel("A").getbbox()
POT_X=X0+OPEN_L2.size[0]+10-_pb[0];POT_Y=OPEN_TOP+OPEN_L1.size[1]+8+(OPEN_L2.size[1]-(_pb[3]-_pb[1]))//2-26-_pb[1]
def step_badge(n,d=104):
    k=3;D=d*k;im=blank(D,D);dr=ImageDraw.Draw(im);dr.ellipse((0,0,D-1,D-1),fill=TER+(255,))
    dr.ellipse((int(D*.06),int(D*.06),int(D*.94),int(D*.94)),outline=CRM+(200,),width=int(D*.025))
    dr.text((D/2,D/2+k*2),str(n),font=SANS("900Black",int(D*.56)),fill=CRM+(255,),anchor="mm");return im.resize((d,d),Image.LANCZOS)
def step_cap(n,text,size=84):
    bd=step_badge(n);tl=vis(tline(text,size,CRM,10,maxw=840));gap=22
    W=bd.size[0]+gap+tl.size[0];H=max(bd.size[1],tl.size[1]);im=blank(W+48,H+48)
    im.alpha_composite(bd,(24,24+(H-bd.size[1])//2));im.alpha_composite(tl,(24+bd.size[0]+gap,24+(H-tl.size[1])//2))
    return shadow(im,10,(0,6),0.5,(0,0,0))   # visible content starts at (24+20, 24+20)
CAPY=1300   # vertical centre of the step captions: the 2/3 line, same zone as the opening title
CAPS={"s1":step_cap(1,"首先洋蔥鋪底"),"s2":step_cap(2,"再鋪上白菜"),"s3":step_cap(3,"兩隻帶骨大雞腿"),"s4":step_cap(4,"一個蘋果＋一根玉米"),
      "s5a":step_cap(5,"中火 20 分鐘"),"s5b":step_cap(5,"轉小火 40 分鐘")}
FIN=shadow(lstack([tline("一鍋鮮甜美味的雞湯",100,CRM,12),tline("上桌了",128,LCOP,12)],[6]),10,(0,6),0.45,(0,0,0))
FIN_VH=FIN.size[1]-88
def ring(prog,num,R=92,sw=16):
    k=3;S=(R*2+sw+40)*k;im=blank(S,S);d=ImageDraw.Draw(im);c=S/2;r=R*k
    d.ellipse((c-r-sw*k/2-10*k,c-r-sw*k/2-10*k,c+r+sw*k/2+10*k,c+r+sw*k/2+10*k),fill=(10,18,14,120))
    d.ellipse((c-r,c-r,c+r,c+r),outline=CRM+(90,),width=sw*k)
    if prog>0.002:d.arc((c-r,c-r,c+r,c+r),-90,-90+360*prog,fill=LCOP+(255,),width=sw*k)
    d.text((c,c-14*k),num,font=SANS("900Black",74*k),fill=CRM+(255,),anchor="mm");d.text((c,c+46*k),"分鐘",font=SANS("700Bold",28*k),fill=CRM+(255,),anchor="mm")
    return im.resize((S//k,S//k),Image.LANCZOS)
FLAME={}
def endcard(u):
    b=Image.new("RGBA",(OW,OH),CRM+(255,))
    lg=logo_h(520);a=ease(u/0.45);sc=0.92+0.08*ease(u/0.5)
    l2=lg.resize((int(lg.size[0]*sc),int(lg.size[1]*sc)),Image.LANCZOS);put(b,fadeim(l2,a),OW/2,800)
    v=clamp((u-0.3)/0.35);t1=ttext("姐夫嚴選為您挑選",SANS("900Black",80),COP+(255,))
    put(b,fadeim(t1,ease(v)),OW/2,1236+(1-ease(v))*24)
    w=clamp((u-0.55)/0.3);d=ImageDraw.Draw(b);L=int(70*ease(w))
    if L>0:d.line([(OW/2-L,1330),(OW/2+L,1330)],fill=LCOP+(255,),width=3)
    return b
class Soup(sty.SV):
    def compose(s,raw,t):
        n,lt,d=s.seg(t);b=raw
        if n in("s2","s3"):b=zoomimg(b,1.0+0.07*(lt/d),540,900)
        if n=="s6b":b=zoomimg(b,1.04-0.04*(lt/d),540,960)
        b=b.convert("RGBA");b.alpha_composite(CS);b.alpha_composite(LS);paste(b,LOGO_W,*LOGO_XY)
        m=44
        if n=="hook":
            a=clamp((s.ve("hook")-0.06-t)/0.12);paste(b,fadeim(OPEN_TXT,a),X0-m,OPEN_TOP-m)
            paste(b,fadeim(doodle_pot(t,236),a),POT_X,POT_Y)
        elif n in("s1","s2","s3","s4","s5"):
            key=n
            if n=="s5":key="s5a" if lt<4*BEAT else "s5b"
            t0=s.vo(n)+(4*BEAT if key=="s5b" else 0);u=(t-t0-0.04)/0.28
            end=s.ve(n) if key!="s5a" else s.vo(n)+4*BEAT
            a=clamp(u*1.6)*clamp((end-0.04-t)/0.12);cap=CAPS[key];vh=cap.size[1]-2*m
            if a>0:paste(b,fadeim(cap,a),X0-m-(1-ease(u))*36,CAPY-vh/2-m)
        else:
            t0=s.vo("s6a")+0.08;u=(t-t0)/0.4;a=clamp(u*2)
            if a>0:paste(b,fadeim(FIN,a),X0-m,1290-FIN_VH/2-m+(1-ease(u))*30)
        return b
    def endframe(s,u):
        e=endcard(u)
        if u<0.22 and s.lastraw is not None:
            last=s.compose(s.lastraw,s.MAIN-0.04).convert("RGBA");return Image.blend(last,e,ease(u/0.22))
        return e
V=Soup(WD,BGM,BGM_OFF,END_D,lufs=-16,fade_out=1.6)
vo=V.vo;B=BEAT
POP=sfx.pop(900);POPL=sfx.pop(640);DING=sfx.ding();CH=sfx.chime(1568);CH2=sfx.chime(2093)
V.ev=[(0.03,DING,0.55)]
for n in("s1","s2","s3","s4","s5"):V.ev.append((vo(n)+0.05,POP,0.32))
V.ev+=[(vo("s5")+4*B+0.05,POPL,0.32),(vo("s6a")+0.08,CH,0.28),(V.MAIN+0.04,CH2,0.22)]
if __name__=="__main__":
    if "test" in sys.argv:
        ts=[0.0,1.2,vo("s1")+0.6,vo("s2")+1.0,vo("s3")+1.0,vo("s4")+1.5,vo("s5")+1.2,vo("s5")+4*B+1.2,vo("s6a")+0.9,vo("s6b")+2.0,V.MAIN+0.1,V.MAIN+1.8]
        V.test(ts,SP+"soup/chk2.jpg");print("ok",V.MAIN,V.TOTAL)
    if "render" in sys.argv:V.render(SP+"soup/姐夫嚴選_姐夫開煮_無水雞湯.mp4")
