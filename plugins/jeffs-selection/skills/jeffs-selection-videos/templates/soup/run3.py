# 姐夫開煮｜無水雞湯 v3 — goose-v3 style configuration (ribbons, highlight captions, doodles, whips, seal) with today's rules:
# opening text at 2/3 of the screen + pot doodle, brighter footage, no text at the top except the logo, copper end line.
import sys,os,math,random
SP="__ROOT__/"
sys.path.insert(0,SP+"eng");sys.path.insert(0,SP+"soup")
from eng import *
import eng
sys.path.insert(0,SP+"brand")
import kit5,open5
WD=SP+"soup/build2"
BGM="__ROOT__/music/食品開箱_joyful-sparks.mp3";BGM_OFF=26.824
B=0.5714;END_D=6*B
eng.COBRAND=blank(1,1)
CH_Y=1150;CAP2=1330   # lower zone: ribbon on the 2/3 line, caption under it
def chapter2(num,title):
    f1=F("k",80);w=int(f1.getlength(title)+190)+60;h=160
    im=blank(w+40,h+40);sh=blank(w+40,h+40);ImageDraw.Draw(sh).polygon([(26,30),(w+26,30),(w-14,h+10),(26,h+10)],fill=(20,8,0,120))
    im=Image.alpha_composite(im,sh.filter(ImageFilter.GaussianBlur(9)));d=ImageDraw.Draw(im)
    d.polygon([(20,20),(w+20,20),(w-20,h),(20,h)],fill=RED+(255,))
    d.ellipse((44,38,148,142),fill=YEL+(255,));d.text((96,90),num,font=F("k",72),fill=INK,anchor="mm")
    d.text((176,92),title,font=f1,fill=WHITE,anchor="lm");return im
def clock_min(n):
    S=300;im=blank(S,S);d=ImageDraw.Draw(im);c=S/2+10
    for sx in (-1,1):
        bx=c+sx*78;by=72;d.ellipse((bx-34,by-34,bx+34,by+34),fill=YEL+(255,),outline=INK+(255,),width=7)
        d.line([(c+sx*70,c+88),(c+sx*96,c+116)],fill=INK+(255,),width=12)
    d.ellipse((c-112,c-112,c+112,c+112),fill=RED+(255,),outline=INK+(255,),width=8)
    d.ellipse((c-86,c-86,c+86,c+86),fill=CREAM+(255,),outline=INK+(255,),width=5)
    d.text((c,c-10),str(n),font=F("k",96),fill=INK+(255,),anchor="mm");d.text((c,c+50),"分鐘",font=F("k",32),fill=INK+(255,),anchor="mm")
    return im
CLK20=clock_min(20);CLK40=clock_min(40)
TAG=label("姐夫開煮",size=60,bg=RED,fg=WHITE).rotate(-6,resample=Image.BICUBIC,expand=True)
HOOKT=hook("無水雞湯",168,-4)
FINH=hook("上桌了！",160,-4)
def badge(d=250,rot=-6,k=3):
    D=d*k;im=blank(D+40*k,D+40*k);dr=ImageDraw.Draw(im);o=20*k
    dr.ellipse((o,o,D+o,D+o),fill=(246,242,233,255))
    m=int(D*0.045);dr.ellipse((o+m,o+m,D+o-m,D+o-m),outline=kit5.COP+(255,),width=max(2*k,int(D*0.011)))
    lg=kit5.logo_h(int(D*0.70));im.alpha_composite(lg,(o+(D-lg.size[0])//2,o+(D-lg.size[1])//2))
    im=im.rotate(rot,resample=Image.BICUBIC,expand=True);im=im.resize((im.size[0]//k,im.size[1]//k),Image.LANCZOS)
    return kit5.shadow(im,12,(0,10),0.5,(0,0,0))
SEAL=badge()
def bump(u):return 0.0 if u<0 or u>0.35 else math.sin(math.pi*u/0.35)
class Soup3(Video):
    def __init__(s):
        super().__init__(WD,BGM,end=END_D,bgmvol=1.0,line="");s.off=BGM_OFF
        _c=kit5.logo_h(470);s.endlogo=_c
    def slide(s,t0,t1,im,x,y,frm="L"):s.el.append(("slide",t0,t1,im,x,y,frm))
    def seal(s,t0,t1,im,x,y):s.el.append(("seal",t0,t1,im,x,y,0))
    def overlay(s,base,t):
        # opening: everything visible from frame 0 (cover), then a bounce on the beat
        if t<s.ve("hook"):
            a=clamp((s.ve("hook")-0.04-t)/0.12);k=1+0.07*bump(t-B)
            pot=open5.doodle_pot(t,205);put(base,pot,150,1100,a)
            put(base,TAG,402,1124,a,1+0.05*bump(t-B-0.08))
            put(base,HOOKT,528,1300,a,k)
            if t>B-0.02:
                ea=a*clamp((t-B+0.02)/0.1);emph(base,955,1222,36,-40,ea);emph(base,92,1395,36,160,ea)
        for kind,t0,t1,a,x,y,r in s.el:
            if not(t0<=t<=t1):continue
            if kind=="slide":
                u=ease((t-t0)/0.34);w=a.size[0];dx=-(1-u)*(x+w/2+30) if r=="L" else (1-u)*(OW-x+w/2+30)
                put(base,a,x+dx,y,clamp((t1-t)/.15))
            elif kind=="seal":u=(t-t0)/0.28;put(base,a,x,y,clamp(u*4)*clamp((t1-t)/.2),2.1-1.1*ease(u))
        super().overlay(base,t)
        kit5.paste(base,kit5.LOGO_W,*kit5.LOGO_XY)
    def endparts(s,last):
        bg=Image.new("RGBA",(OW,OH),kit5.CRM+(255,))
        line=kit5.ttext("姐夫嚴選為您挑選",kit5.SANS("900Black",84),kit5.COP+(255,))
        return bg,dict(last=last.convert("RGBA"),logo=s.endlogo,line=line)
    def endframe(s,bg,P,u):
        base=bg.copy();put(base,P["logo"],540,790,clamp(u/0.3),0.86+0.14*spring(u/0.5))
        v=clamp((u-0.3)/0.3);put(base,P["line"],540,1240+(1-ease(v))*26,v)
        d=ImageDraw.Draw(base);L=int(80*ease(clamp((u-0.55)/0.3)))
        if L>0:d.line([(540-L,1340),(540+L,1340)],fill=kit5.LCOP+(255,),width=4)
        for i,(x,y,r,ph) in enumerate([(260,560,22,0.2),(830,520,30,0.9),(880,1040,22,1.5),(210,1060,26,2.2)]):
            a=clamp((u-0.4-i*0.12)/0.3)*(0.5+0.5*math.sin(u*5+ph))
            if a>0.05:put(base,SPK[22 if r<26 else 30],x,y,a)
        if u<0.22:return Image.blend(P["last"],base,ease(u/0.22))
        return base
    def audio(s):
        SR=48000;T=s.TOTAL
        fx=sfx.build(s.ev,T+1)[:int(T*SR)];sf.write("sfx_mono.wav",fx,SR)
        subprocess.run(["ffmpeg","-v","error","-y","-ss",str(s.off),"-i",s.bgm,"-i","sfx_mono.wav","-filter_complex",
          f"[0:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{T+0.5},asetpts=PTS-STARTPTS,loudnorm=I=-16:TP=-2,afade=t=in:d=0.03,afade=t=out:st={T-1.6:.3f}:d=1.6,apad,atrim=0:{T}[m];"
          f"[1:a]aformat=channel_layouts=stereo[x];[m][x]amix=inputs=2:normalize=0,alimiter=limit=0.84:level=disabled,atrim=0:{T}[o]","-map","[o]","-c:a","pcm_s16le","mix.wav"],check=True)
V=Soup3();vo,ve=V.vo,V.ve;M=V.MAIN
# steps: ribbon on the 2/3 line + highlighted caption under it
STEPS=[("s1","1","第一層","首先[[洋蔥]]鋪底"),("s2","2","第二層","再鋪上[[白菜]]"),("s3","3","第三層","兩隻[[帶骨大雞腿]]"),("s4","4","第四層","一個[[蘋果]]＋一根[[玉米]]")]
for k,n,title,line in STEPS:
    a=vo(k);c=chapter2(n,title);V.slide(a+0.05,ve(k),c,48+c.size[0]/2,CH_Y,"L");V.cap(a+0.3,ve(k),line,CAP2)
c=chapter2("5","開火");a=vo("s5");V.slide(a+0.05,ve("s5"),c,48+c.size[0]/2,CH_Y,"L")
V.cap(a+0.3,a+4*B-0.04,"[[中火 20 分鐘]]",CAP2);V.cap(a+4*B,ve("s5"),"轉[[小火 40 分鐘]]",CAP2)
V.pop(a+0.35,a+4*B-0.04,CLK20,850,930,8);V.pop(a+4*B,ve("s5"),CLK40,850,930,8)
V.fx("steam",a,ve("s5"),x=520,y=760,w=520,h=480,seed=3)
# small doodles on the steps
V.fx("twinkle",vo("s1")+0.4,ve("s1"));V.fx("twinkle",vo("s4")+0.3,ve("s4"))
V.pop(vo("s3")+0.6,ve("s3"),punch("×2",120,YEL,-8),880,880)
# finale: caption first, then the big line, then the seal
a=vo("s6a");V.cap(a+0.08,ve("s6b"),"一鍋[[鮮甜美味]]的雞湯",CH_Y)
V.hook(a+B,ve("s6b"),FINH,540,CAP2+10);V.seal(a+2*B,ve("s6b"),SEAL,850,860)
V.fx("twinkle",a,ve("s6b"));V.fx("steam",a,ve("s6a"),x=540,y=780,w=560,h=460,seed=5)
# camera
V.zoom(0,ve("hook"),1.0,1.05,540,1000);V.zoom(vo("s1"),ve("s1"),1.0,1.05,540,900);V.zoom(vo("s2"),ve("s2"),1.0,1.09,540,900)
V.zoom(vo("s3"),ve("s3"),1.0,1.09,540,900);V.zoom(vo("s4"),ve("s4"),1.0,1.06,540,900);V.zoom(vo("s5"),ve("s5"),1.0,1.05,540,900)
V.zoom(vo("s6a"),ve("s6a"),1.0,1.07,540,960);V.zoom(vo("s6b"),ve("s6b"),1.06,1.0,540,960)
V.whips=[vo(k) for k in ("s1","s2","s3","s4","s5","s6a","s6b")];V.flashes=[B,vo("s6a")]
# sound
V.ev=[(0.03,DING,.5),(0.05,POPH,.38),(B,thud(),.55),(B+0.02,POP,.3),(2*B,sparkle_snd(),.28)]
for k in ("s1","s2","s3","s4","s5","s6a"):V.ev.append((vo(k)-0.14,WR,.34))
for k in ("s1","s2","s3","s4","s5"):V.ev+=[(vo(k)+0.08,WH,.26),(vo(k)+0.3,POP,.34)]
V.ev+=[(vo("s3")+0.6,POPH,.34),(vo("s5")+0.35,POPH,.32),(vo("s5")+4*B,POPH,.34)]
V.ev+=[(vo("s6a")+0.08,BOOM,.42),(vo("s6a")+B,thud(),.7),(vo("s6a")+B+0.04,CHM,.3),(vo("s6a")+2*B,thud(),.6),(vo("s6a")+2.4*B,sparkle_snd(),.3)]
V.ev+=[(M+0.02,WH,.32),(M+0.3,POP,.3),(M+0.55,CHM,.26)]
if __name__=="__main__":
    if "test" in sys.argv:
        ts=[0.0,0.75,vo("s1")+0.7,vo("s2")+1.0,vo("s3")+1.2,vo("s4")+1.5,vo("s5")+1.4,vo("s5")+4*B+1.2,vo("s6a")+1.3,vo("s6b")+2.0,M+0.15,M+2.0]
        V.test(ts);print("ok",M,V.TOTAL)
    if "render" in sys.argv:V.render(SP+"soup/姐夫開煮_無水雞湯_v3.mp4")
