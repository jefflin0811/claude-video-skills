import sys,os,json,math,random,subprocess
BD="__ROOT__/";sys.path.insert(0,BD+"beef");sys.path.insert(0,BD+"work")
from ill8 import *
import numpy as np,soundfile as sf,sfx
OW,OH,FPS=1080,1920,30
def clamp(u):return min(max(u,0.0),1.0)
def ease(u):u=clamp(u);return 1-(1-u)**3
def spring(u):u=clamp(u);return 1-math.exp(-7*u)*math.cos(11*u)
BOT=1720;TOP=380
_LP=BD+"beef/brandlogo.png"   # 牛肉爐合作 logo（含合作品牌，技能包未附；三個系列版型都用不到）
lg=Image.open(_LP).convert("RGBA") if os.path.exists(_LP) else Image.new("RGBA",(1011,730),(0,0,0,0));_top=lg.crop((0,0,lg.size[0],340))
_s=_top.resize((360,int(340*360/lg.size[0])),Image.LANCZOS)
COBRAND=blank(_s.size[0]+40,_s.size[1]+24);ImageDraw.Draw(COBRAND).rounded_rectangle((0,0,COBRAND.size[0]-1,COBRAND.size[1]-1),radius=22,fill=(40,16,6,170));COBRAND.alpha_composite(_s,(20,12))
GLOW={}
def glowstar(r):
    if r in GLOW:return GLOW[r]
    s=r*4;im=blank(s,s);d=ImageDraw.Draw(im);c=s/2
    d.polygon([(c,c-r*1.6),(c+r*.18,c-r*.18),(c+r*1.6,c),(c+r*.18,c+r*.18),(c,c+r*1.6),(c-r*.18,c+r*.18),(c-r*1.6,c),(c-r*.18,c-r*.18)],fill=(255,255,240,255))
    g=im.filter(ImageFilter.GaussianBlur(r*.35));g.alpha_composite(im);GLOW[r]=g;return g
rs=random.Random(5)
STP=[(rs.uniform(140,940),rs.uniform(420,1250),rs.choice([10,14,18,24]),rs.uniform(0,1),rs.uniform(.6,1.1)) for _ in range(16)]
GH=[(rs.uniform(80,240) if i%2 else rs.uniform(840,1000),rs.uniform(1300,1600),rs.uniform(0,2.4)) for i in range(10)]
def twinkle(base,t,a,b,pts):
    for x,y,r,ph,per in pts:
        u=t-a-ph*0.8
        if u<0:continue
        tw=math.sin(math.pi*((u%per)/per))*clamp((b-t)/.4)
        if tw>.05:put(base,glowstar(r),x,y,tw)
def stampimg(txt="完美"):
    w=440;im=blank(w,w);d=ImageDraw.Draw(im)
    d.ellipse((20,20,w-20,w-20),fill=(255,247,232,90),outline=RED+(255,),width=18);d.ellipse((50,50,w-50,w-50),outline=RED+(255,),width=6)
    d.text((w/2,w/2),txt,font=F("k",136),fill=RED+(255,),anchor="mm");return im.rotate(-14,expand=True)
BUY=label("點下方連結購買",icon="↓",size=60,bg=CREAM,fg=INK,accent=RED)
FFL=label("倍速播放 ▶▶",size=40,bg=INK,fg=WHITE)
class Video:
    def __init__(s,wd,bgm,end=3.5,bgmvol=0.8,line="一鍋牛肉爐，[[變化更多料理]]"):
        s.wd=wd;os.chdir(wd);C=json.load(open("cut.json"));s.S={x["name"]:x for x in C["seg"]};s.MAIN=C["total"];s.END=end;s.TOTAL=s.MAIN+end
        s.bgm=bgm;s.bgmvol=bgmvol;s.el=[];s.cam=[];s.flashes=[];s.whips=[];s.ev=[];s.line=line;s.shakes=[]
    def vo(s,n):return s.S[n]["o"]
    def ve(s,n):return s.S[n]["o"]+s.S[n]["d"]
    # element adders
    def cap(s,t0,t1,txt,y=BOT):s.el.append(("cap",t0,t1,caption(txt),540,y,0))
    def pop(s,t0,t1,im,x,y,rot=0):s.el.append(("pop",t0,t1,im,x,y,rot))
    def hook(s,t0,t1,im,x=540,y=360):s.el.append(("hook",t0,t1,im,x,y,0));s.shakes.append((t0+0.25,t0+0.7))
    def fx(s,kind,t0,t1,**k):s.el.append((kind,t0,t1,k,0,0,0))
    def zoom(s,t0,t1,z0,z1,cx=540,cy=960):s.cam.append((t0,t1,z0,z1,cx,cy))
    def overlay(s,base,t):
        for kind,t0,t1,a,x,y,r in s.el:
            if not(t0<=t<=t1):continue
            if kind=="cap":u=(t-t0)/0.2;put(base,a,x,y+(1-ease(u))*16,clamp(u)*clamp((t1-t)/.12),0.9+0.1*ease(u))
            elif kind=="pop":u=(t-t0)/0.4;put(base,a,x,y,clamp(u*3)*clamp((t1-t)/.2),0.5+0.5*spring(u),r)
            elif kind=="hook":
                u=(t-t0)/0.4;rr=random.Random(int(t*24));j=6 if t>t0+0.4 else 0
                put(base,a,x+rr.uniform(-j,j),y+rr.uniform(-j,j),clamp(u*3)*clamp((t1-t)/.2),0.4+0.6*spring(u))
                emph(base,960,y-110,40,-40,clamp(u*2)*clamp((t1-t)/.2));emph(base,120,y+110,40,160,clamp(u*2)*clamp((t1-t)/.2))
            elif kind=="steam":steam_layer(base,t,a.get("x",540),a.get("y",1000),a.get("w",380),a.get("h",380),3,clamp((t-t0)/.4)*clamp((t1-t)/.2),a.get("seed",1))
            elif kind=="twinkle":twinkle(base,t,t0,t1,STP)
            elif kind=="hearts":
                for hx,hy,ph in GH[:a.get("n",6)]:
                    v=t-t0-ph*0.4
                    if v>0:put(base,HEART,hx+math.sin(v*4)*20,hy-v*170,clamp(v*4)*clamp(1.4-v)*clamp((t1-t)/.15),0.6+0.2*math.sin(v*6))
            elif kind=="buy":u=(t-t0)/0.4;put(base,BUY,540,a.get("y",1440)+(1-ease(u))*80,clamp(u*3)*clamp((t1-t)/.25),1+0.04*math.sin(t*7))
            elif kind=="clock":
                u=t-t0;n=max(0,int(round(30-30*u/(t1-t0-0.1))));put(base,clock(n),880,a.get("y",640),clamp(u/0.2)*clamp((t1-t)/.15),0.8+0.2*spring(u/.4))
                put(base,FFL,860,a.get("y",640)+200,clamp(u/0.2)*clamp((t1-t)/.15),1+0.05*math.sin(t*12))
            elif kind=="burst":u=(t-t0)/0.3;put(base,burst(a.get("text","叮！")),a.get("x",800),a.get("y",560),clamp(u*3)*clamp((t1-t)/.2),0.5+0.5*spring(u),10)
            elif kind=="stamp":u=(t-t0)/0.35;put(base,a["im"],a.get("x",800),a.get("y",420),clamp(u*3)*clamp((t1-t)/.2),2.2-1.2*ease(u))
            elif kind=="chars":
                for i,(im,cx) in enumerate(a["ims"]):
                    u=(t-t0-i*a.get("step",0.25))/0.25
                    if u>0:hop=abs(math.sin((t-t0-i*0.25)*7))*40*math.exp(-(t-t0)*0.6);put(base,im,cx,a.get("y",1640)-hop,clamp(u*3)*clamp((t1-t)/.2),0.4+0.6*spring(u),(i%2*2-1)*6)
        put(base,COBRAND,230,96,0.92 if t>0.15 else 0)
    def camera(s,t):
        z,cx,cy,dx,dy=1.0,540,960,0,0
        for t0,t1,z0,z1,x,y in s.cam:
            if t0<=t<t1:z=z0+(z1-z0)*ease((t-t0)/(t1-t0));cx,cy=x,y
        for a,b in s.shakes:
            if a<=t<b:r=random.Random(int(t*60));k=(b-t)/(b-a)*18;dx,dy=r.uniform(-k,k),r.uniform(-k,k)
        return z,cx,cy,dx,dy
    def compose(s,img,t):
        z,cx,cy,dx,dy=s.camera(t)
        if z>1.001 or dx or dy:
            w2,h2=OW/z,OH/z;x0=min(max(cx-w2/2,0),OW-w2)+dx;y0=min(max(cy-h2/2,0),OH-h2)+dy
            x0=min(max(x0,0),OW-w2);y0=min(max(y0,0),OH-h2);img=img.resize((OW,OH),Image.BILINEAR,box=(x0,y0,x0+w2,y0+h2))
        for c in s.whips:
            if c-0.15<=t<c+0.15:
                sh=(1-abs(t-c)/0.15)*60;arr=np.asarray(img).astype(np.float32);acc=np.zeros_like(arr)
                for j in range(7):acc+=np.roll(arr,int(j*sh/7),axis=1)
                img=Image.fromarray((acc/7).astype(np.uint8))
        img=img.convert("RGBA");s.overlay(img,t)
        f=0
        for a in s.flashes:
            if a-0.08<=t<=a+0.2:f=max(f,(1-abs(t-a)/(0.08 if t<a else 0.2))*0.55)
        if f>0:img=Image.blend(img,Image.new("RGBA",(OW,OH),(255,250,235,255)),f)
        return img.convert("RGB")
    def endparts(s,last):
        bg=last.convert("RGB").filter(ImageFilter.GaussianBlur(22));bg=Image.blend(bg,Image.new("RGB",(OW,OH),(52,20,10)),0.6).convert("RGBA")
        sc=980/lg.size[0];top=_top.resize((int(_top.size[0]*sc),int(_top.size[1]*sc)),Image.LANCZOS)
        title=lg.crop((0,345,lg.size[0],lg.size[1]));title=title.resize((int(title.size[0]*sc*1.05),int(title.size[1]*sc*1.05)),Image.LANCZOS)
        a=title.getchannel("A");out=a.filter(ImageFilter.MaxFilter(25));halo=Image.new("RGBA",title.size,(255,246,232,0));halo.putalpha(out)
        t2=blank(title.size[0]+40,title.size[1]+40);sh=Image.new("RGBA",title.size,(0,0,0,0));sh.putalpha(out.filter(ImageFilter.GaussianBlur(14)).point(lambda v:int(v*.5)))
        t2.alpha_composite(sh,(26,30));t2.alpha_composite(halo,(20,20));t2.alpha_composite(title,(20,20))
        sub=textrun(parse(s.line),F("k",72),(WHITE,YEL),9,INK)
        return bg,dict(top=top,title=t2,line=sub,btn=label("購買連結",size=80,bg=RED,fg=WHITE))
    def endframe(s,bg,P,u):
        base=bg.copy()
        put(base,P["top"],540,470,clamp(u/0.3),0.6+0.4*spring(u/0.5));put(base,P["title"],540,820,clamp((u-0.25)/0.3),0.5+0.5*spring((u-0.25)/0.5))
        put(base,P["line"],540,1170,clamp((u-0.6)/0.3));p=1+0.06*math.sin(max(0,u-0.9)*6)
        put(base,P["btn"],540,1340,clamp((u-0.9)/0.25),(0.5+0.5*spring((u-0.9)/0.4))*p);d=ImageDraw.Draw(base)
        for k in range(3):
            a=clamp((u-1.2)/0.3)*(0.4+0.6*abs(math.sin(u*4-k*0.6)));cy=1520+k*54
            d.line([(485,cy),(540,cy+34),(595,cy)],fill=YEL+(int(255*a),),width=12,joint="curve")
        twinkle(base,u+5,0,10,STP[:10]);return base
    def frame_at(s,t):
        raw=subprocess.run(["ffmpeg","-v","error","-ss",str(min(t,s.MAIN-0.25)),"-i","video.mp4","-frames:v","1","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
        return Image.frombytes("RGB",(OW,OH),raw)
    def audio(s):
        SR=48000
        fx=sfx.build(s.ev+[(s.MAIN+0.05,sfx.whoosh(.45,True),.35),(s.MAIN+0.9,sfx.pop(1300),.5),(s.MAIN+1.0,sfx.chime(),.35)],s.TOTAL+1)[:int(s.TOTAL*SR)];sf.write("sfx_mono.wav",fx,SR)
        T=s.TOTAL
        subprocess.run(["ffmpeg","-v","error","-y","-i","voice_raw.wav","-af",f"highpass=f=80,acompressor=threshold=-20dB:ratio=2.5:makeup=2,loudnorm=I=-15:TP=-1.5,aformat=sample_rates=48000:channel_layouts=stereo,apad,atrim=0:{T}","-c:a","pcm_s16le","voice.wav"],check=True)
        subprocess.run(["ffmpeg","-v","error","-y","-i",s.bgm,"-i","voice.wav","-filter_complex",
          f"[0:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{T},loudnorm=I=-17:TP=-2,volume={s.bgmvol},afade=t=in:d=0.3,afade=t=out:st={T-1.5}:d=1.5,apad,atrim=0:{T}[m];[m][1:a]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[d]","-map","[d]","-c:a","pcm_s16le","bgm.wav"],check=True)
        subprocess.run(["ffmpeg","-v","error","-y","-i","voice.wav","-i","bgm.wav","-i","sfx_mono.wav","-filter_complex",
          f"[2:a]aformat=channel_layouts=stereo[x];[0:a][1:a][x]amix=inputs=3:normalize=0,alimiter=limit=0.8:level=disabled,apad,atrim=0:{T}[o]","-map","[o]","-c:a","pcm_s16le","mix.wav"],check=True)
    def test(s,ts):
        os.makedirs("t",exist_ok=True)
        for t in ts:
            if t<s.MAIN:s.compose(s.frame_at(t),t).save(f"t/{t:05.2f}.jpg",quality=85)
            else:bg,P=s.endparts(s.compose(s.frame_at(s.MAIN-0.25),s.MAIN-0.25).convert("RGBA"));s.endframe(bg,P,t-s.MAIN).convert("RGB").save(f"t/{t:05.2f}.jpg",quality=85)
        fs=sorted(os.listdir("t"));Wd,H=240,427;sh=Image.new("RGB",(Wd*len(fs),H))
        for i,f in enumerate(fs):sh.paste(Image.open("t/"+f).resize((Wd,H)),(i*Wd,0))
        sh.save("chk.jpg",quality=85)
    def render(s,out):
        s.audio()
        rd=subprocess.Popen(["ffmpeg","-v","error","-i","video.mp4","-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE,bufsize=10**8)
        wr=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s","1080x1920","-r","30","-i","-","-i","mix.wav","-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-t",str(s.TOTAL),"-movflags","+faststart",out],stdin=subprocess.PIPE)
        N=int(round(s.MAIN*FPS));last=None;lr=None
        for i in range(N):
            b=rd.stdout.read(OW*OH*3)
            img=Image.frombytes("RGB",(OW,OH),b) if len(b)==OW*OH*3 else lr;lr=img
            last=s.compose(img,i/FPS);wr.stdin.write(last.tobytes())
        bg,P=s.endparts(last.convert("RGBA"))
        for i in range(int(round(s.END*FPS))):wr.stdin.write(s.endframe(bg,P,i/FPS).convert("RGB").tobytes())
        wr.stdin.close();wr.wait();print("done",flush=True)
POP=sfx.pop(900);POPH=sfx.pop(1300);CHM=sfx.chime();BOOM=sfx.boom();WH=sfx.whoosh(.45,True);WR=sfx.whoosh(.35,False);DING=sfx.ding()
SR=48000
def tick():n=int(.04*SR);tt=np.arange(n)/SR;return np.sin(2*np.pi*2400*tt)*np.exp(-tt*150)*.5
def alarm(dur=0.6):
    n=int(dur*SR);tt=np.arange(n)/SR;g=(np.sin(2*np.pi*18*tt)>0).astype(float);return (np.sin(2*np.pi*2600*tt)+.6*np.sin(2*np.pi*3900*tt))*g*np.exp(-tt*2.5)*.25
def sparkle_snd():
    out=np.zeros(int(.9*SR))
    for k,f in enumerate([2093,2637,3136,4186]):
        L=int(.5*SR);tt=np.arange(L)/SR;i=int(k*.07*SR);out[i:i+L]+=np.sin(2*np.pi*f*tt)*np.exp(-tt*9)*.18
    return out
def thud():
    rng=np.random.default_rng(3);n=int(.5*SR);tt=np.arange(n)/SR;f=90*np.exp(-tt*9)+45;return (np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*9)+rng.standard_normal(n)*np.exp(-tt*60)*.3)*.9
DDC=[(255,110,80),(90,180,255),(255,214,64),(120,210,120),(255,150,200)]
def dd_char(ch,col,size=140):return textrun([(ch,False)],F("k",size),(col,col),12,INK,outer=(WHITE,10),pad=50)
