# shared base for the 姐夫開煮 creative variants (same cut + music as v3; round semi-transparent mark top-left; copper end line)
import sys,os,math,random
SP="__ROOT__/"
sys.path.insert(0,SP+"eng");sys.path.insert(0,SP+"soup");sys.path.insert(0,SP+"brand")
from eng import *
import eng,kit5,open5
from doodles import *
WD=SP+"soup/build2"
BGM="__ROOT__/music/食品開箱_joyful-sparks.mp3";BGM_OFF=26.824
B=0.5714;END_D=6*B
eng.COBRAND=blank(1,1)
def bump(u,d=0.35):return 0.0 if u<0 or u>d else math.sin(math.pi*u/d)
class Base(Video):
    def __init__(s):
        super().__init__(WD,BGM,end=END_D,bgmvol=1.0,line="");s.off=BGM_OFF;s.endlogo=kit5.logo_h(470)
    def slide(s,t0,t1,im,x,y,frm="L"):s.el.append(("slide",t0,t1,im,x,y,frm))
    def seal(s,t0,t1,im,x,y):s.el.append(("seal",t0,t1,im,x,y,0))
    def extra(s,base,t):pass          # version-specific drawing before the shared elements
    def extra_top(s,base,t):pass      # version-specific drawing above the shared elements
    def overlay(s,base,t):
        s.extra(base,t)
        for kind,t0,t1,a,x,y,r in s.el:
            if not(t0<=t<=t1):continue
            if kind=="slide":
                u=ease((t-t0)/0.34);w=a.size[0];dx=-(1-u)*(x+w/2+30) if r=="L" else (1-u)*(OW-x+w/2+30)
                put(base,a,x+dx,y,clamp((t1-t)/.15))
            elif kind=="seal":u=(t-t0)/0.28;put(base,a,x,y,clamp(u*4)*clamp((t1-t)/.2),2.1-1.1*ease(u))
        super().overlay(base,t)
        s.extra_top(base,t)
        paste_mark(base)
    def end_extra(s,base,u):pass
    def endparts(s,last):
        bg=Image.new("RGBA",(OW,OH),kit5.CRM+(255,))
        line=kit5.ttext("姐夫嚴選為您挑選",kit5.SANS("900Black",84),kit5.COP+(255,))
        return bg,dict(last=last.convert("RGBA"),logo=s.endlogo,line=line)
    def endframe(s,bg,P,u):
        base=bg.copy();put(base,P["logo"],540,760,clamp(u/0.3),0.86+0.14*spring(u/0.5))
        v=clamp((u-0.3)/0.3);put(base,P["line"],540,1210+(1-ease(v))*26,v)
        d=ImageDraw.Draw(base);L=int(80*ease(clamp((u-0.55)/0.3)))
        if L>0:d.line([(540-L,1306),(540+L,1306)],fill=kit5.LCOP+(255,),width=4)
        s.end_extra(base,u)
        if u<0.22:return Image.blend(P["last"],base,ease(u/0.22))
        return base
    def audio(s):
        SR=48000;T=s.TOTAL
        fx=sfx.build(s.ev,T+1)[:int(T*SR)];sf.write("sfx_mono.wav",fx,SR)
        subprocess.run(["ffmpeg","-v","error","-y","-ss",str(s.off),"-i",s.bgm,"-i","sfx_mono.wav","-filter_complex",
          f"[0:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{T+0.5},asetpts=PTS-STARTPTS,loudnorm=I=-16:TP=-2,afade=t=in:d=0.03,afade=t=out:st={T-1.6:.3f}:d=1.6,apad,atrim=0:{T}[m];"
          f"[1:a]aformat=channel_layouts=stereo[x];[m][x]amix=inputs=2:normalize=0,alimiter=limit=0.84:level=disabled,atrim=0:{T}[o]","-map","[o]","-c:a","pcm_s16le","mix.wav"],check=True)
    def sheet(s,ts,name):
        os.makedirs("tt",exist_ok=True)
        for f in os.listdir("tt"):os.remove("tt/"+f)
        ims=[]
        for t in ts:
            if t<s.MAIN:im=s.compose(s.frame_at(t),t)
            else:bg,P=s.endparts(s.compose(s.frame_at(s.MAIN-0.25),s.MAIN-0.25).convert("RGBA"));im=s.endframe(bg,P,t-s.MAIN).convert("RGB")
            ims.append(im.resize((360,640)))
        W=6;sh=Image.new("RGB",(W*366,((len(ims)+W-1)//W)*646),(255,255,255))
        for i,im in enumerate(ims):sh.paste(im,((i%W)*366,(i//W)*646))
        sh.save(name,quality=86)
# rustle / bubbling sounds for the comic version
def rustle(d=0.5):
    n=int(d*SR);rng=np.random.default_rng(7);x=rng.standard_normal(n);t=np.arange(n)/SR
    e=(np.sin(np.pi*t/d)**2)*(0.6+0.4*np.sin(2*np.pi*13*t)**2);y=np.convolve(x,np.ones(6)/6,"same")-np.convolve(x,np.ones(60)/60,"same")
    return y*e*0.5
def blub():
    n=int(0.09*SR);t=np.arange(n)/SR;f=420+900*t/0.09;return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*30)*0.45
