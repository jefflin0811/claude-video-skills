# shared base for the 姐夫嚴選 style explorations (same footage, different looks)
import sys,os,math,random,json,subprocess
import numpy as np,soundfile as sf
from PIL import Image,ImageDraw,ImageFilter,ImageFont
SP="__ROOT__";G=SP+"/goose"
sys.path.insert(0,SP+"/work");import sfx
OW,OH,FPS=1080,1920,30;SR=48000
FX=SP+"/fonts/x2/package/";_fc={}
def _f(path,size):
    k=(path,size)
    if k not in _fc:_fc[k]=ImageFont.truetype(path,size)
    return _fc[k]
def SERIF(w,size):return _f(FX+f"{w}/NotoSerifTC_{w}.ttf",size)        # 300Light 400Regular 500Medium 600SemiBold 700Bold 900Black
def KAI(w,size):return _f(FX+f"{w}/LXGWWenKaiTC_{w}.ttf",size)         # 300Light 400Regular 700Bold
def GARA(w,size):return _f(FX+f"{w}/CormorantGaramond_{w}.ttf",size)   # 300Light 400Regular 500Medium 600SemiBold (+_Italic)
def clamp(u):return min(max(u,0.0),1.0)
def ease(u):u=clamp(u);return 1-(1-u)**3
def inout(u):u=clamp(u);return u*u*(3-2*u)
def spring(u):u=clamp(u);return 1-math.exp(-7*u)*math.cos(11*u)
def blank(w,h):return Image.new("RGBA",(max(1,int(w)),max(1,int(h))),(0,0,0,0))
def paste(base,im,x,y):
    x,y=int(round(x)),int(round(y));W,H=base.size
    x0,y0=max(0,-x),max(0,-y);x1,y1=min(im.size[0],W-x),min(im.size[1],H-y)
    if x1>x0 and y1>y0:base.alpha_composite(im.crop((x0,y0,x1,y1)),(x+x0,y+y0))
def fade(im,a):
    if a>=0.999:return im
    im=im.copy();im.putalpha(im.getchannel("A").point(lambda v:int(v*a)));return im
def put(base,im,cx,cy,a=1.0,sc=1.0,rot=0.0):
    if a<=0.003 or sc<=0.01:return
    if abs(sc-1)>0.002:im=im.resize((max(1,int(im.size[0]*sc)),max(1,int(im.size[1]*sc))),Image.BICUBIC)
    if abs(rot)>0.05:im=im.rotate(rot,resample=Image.BICUBIC,expand=True)
    paste(base,fade(im,a),cx-im.size[0]/2,cy-im.size[1]/2)
def putl(base,im,x,cy,a=1.0,dx=0):paste(base,fade(im,a),x+dx,cy-im.size[1]/2)   # left-anchored
def ttext(text,font,fill,track=0,pad=6):
    ws=[font.getlength(c) for c in text];asc,desc=font.getmetrics();W=int(sum(ws)+track*max(0,len(text)-1))+2*pad;H=asc+desc+2*pad
    im=blank(W,H);d=ImageDraw.Draw(im);x=pad
    for c,w in zip(text,ws):d.text((x,pad),c,font=font,fill=fill);x+=w+track
    return im
def vtext(text,font,fill,lead=1.12,pad=6):
    s=font.size;H=int(s*lead*len(text))+2*pad;im=blank(s+2*pad+8,H);d=ImageDraw.Draw(im)
    for i,c in enumerate(text):d.text((pad+4+s/2,pad+s*lead*(i+0.5)),c,font=font,fill=fill,anchor="mm")
    return im
def shadow(im,blur=10,off=(0,6),al=0.45,col=(0,0,0)):
    a=im.getchannel("A");sh=Image.new("RGBA",im.size,col+(0,));sh.putalpha(a.point(lambda v:int(v*al)).filter(ImageFilter.GaussianBlur(blur)))
    m=blur*2;out=blank(im.size[0]+2*m,im.size[1]+2*m);out.alpha_composite(sh,(m+off[0],m+off[1]));out.alpha_composite(im,(m,m));return out
def wipe(im,u,soft=40):
    if u>=1:return im
    if u<=0:return blank(*im.size)
    w=im.size[0];edge=u*(w+soft);ramp=np.clip((edge-np.arange(w))/soft,0,1)
    m=Image.fromarray((np.tile(ramp,(im.size[1],1))*255).astype(np.uint8));a=Image.fromarray(np.minimum(np.asarray(im.getchannel("A")),np.asarray(m)))
    im=im.copy();im.putalpha(a);return im
def rise(base,im,x,cy,u,dist=26,left=True):
    a=ease(u/0.5);dy=(1-ease(u))*dist
    if left:putl(base,im,x,cy+dy,a)
    else:put(base,im,x,cy+dy,a)

# ---------- brand: 姐夫嚴選 logo (copper line art on cream) ----------
LG_SRC=G+"/assets/jeff_logo_hi.jpg";LBG=(238,229,224);LBOX=(380,192,1267,1919)
def _load():
    a=np.asarray(Image.open(LG_SRC).convert("RGB")).astype(np.float32)
    bg=np.array(LBG,np.float32);ink=np.array([170,123,85],np.float32);v=ink-bg
    t=np.clip(((a-bg)@v)/(v@v),0,1);core=float(np.median(t[t>0.5]));al=np.clip(t/core,0,1)
    col=np.median(a[t>0.8],0).astype(np.uint8);rgba=np.zeros(a.shape[:2]+(4,),np.uint8);rgba[...,:3]=col;rgba[...,3]=(al*255).astype(np.uint8)
    return Image.fromarray(rgba).crop(LBOX),tuple(int(c) for c in col)
LOGO,COPPER=_load()
def logo_h(h,col=None):
    im=LOGO.resize((int(LOGO.size[0]*h/LOGO.size[1]),h),Image.LANCZOS)
    if col:c=Image.new("RGBA",im.size,col+(255,));c.putalpha(im.getchannel("A"));im=c
    return im
def _slate():
    c=Image.open(LG_SRC).convert("RGB").crop(LBOX);k=884/(1899-212);c=c.resize((int(c.size[0]*k),int(c.size[1]*k)),Image.LANCZOS)
    s=Image.new("RGB",(OW,OH),LBG);s.paste(c,((OW-c.size[0])//2,966-c.size[1]//2));return s.convert("RGBA")
SLATE=_slate()
def slate_at(v):
    sc=1.04-0.04*ease(v/1.6);sl=SLATE.resize((int(OW*sc),int(OH*sc)),Image.BICUBIC);x=(sl.size[0]-OW)//2;y=(sl.size[1]-OH)//2
    return sl.crop((x,y,x+OW,y+OH))
def logo_card(h=170,rot=0,k=3,alpha=240):
    lg=logo_h(h*k);w,hh=lg.size[0]+30*k,lg.size[1]+26*k;im=blank(w+30*k,hh+30*k);d=ImageDraw.Draw(im)
    d.rounded_rectangle((15*k,15*k,w+15*k,hh+15*k),radius=20*k,fill=LBG+(alpha,));im.alpha_composite(lg,(30*k,28*k))
    im=im.resize((im.size[0]//k,im.size[1]//k),Image.LANCZOS)
    if rot:im=im.rotate(rot,resample=Image.BICUBIC,expand=True)
    return shadow(im,8,(0,5),0.35)
def badge(d=290,rot=-6,k=3,ring=COPPER,bg=LBG):
    D=d*k;im=blank(D+40*k,D+40*k);dr=ImageDraw.Draw(im);o=20*k;dr.ellipse((o,o,D+o,D+o),fill=bg+(255,))
    m=int(D*0.045);dr.ellipse((o+m,o+m,D+o-m,D+o-m),outline=ring+(255,),width=max(2*k,int(D*0.011)))
    lg=logo_h(int(D*0.70));im.alpha_composite(lg,(o+(D-lg.size[0])//2,o+(D-lg.size[1])//2))
    im=im.rotate(rot,resample=Image.BICUBIC,expand=True);im=im.resize((im.size[0]//k,im.size[1]//k),Image.LANCZOS);return shadow(im,12,(0,10),0.45)

def paper(col=(244,238,229),grain=7,seed=1,blotch=10):
    rng=np.random.default_rng(seed);n=rng.normal(0,grain,(OH,OW,1))
    low=Image.fromarray((rng.random((24,14))*255).astype(np.uint8)).resize((OW,OH),Image.BICUBIC).filter(ImageFilter.GaussianBlur(40))
    lo=(np.asarray(low).astype(np.float32)/255-0.5)[...,None]*blotch
    a=np.clip(np.array(col,np.float32)[None,None,:]+n+lo,0,255).astype(np.uint8);return Image.fromarray(a).convert("RGBA")
def cover(img,w,h,cy=0.5,zoom=1.0,cx=0.5):
    """scale a 1080x1920 frame to cover w x h, then crop (cy/cx = focus 0..1)"""
    s=max(w/img.size[0],h/img.size[1])*zoom;W,H=img.size[0]*s,img.size[1]*s
    x0=(W-w)*cx;y0=(H-h)*cy;return img.resize((w,h),Image.BICUBIC,box=(x0/s,y0/s,(x0+w)/s,(y0+h)/s))

ADDR="台北市大同區長安西路220巷29號";MRT="捷運台北車站／北門站 步行約10分鐘"
DISH=["當歸鵝腸湯","乾鴨血","白切鴨","煙燻鵝腿"]

class SV:
    def __init__(s,wd,bgm,off,end,lufs=-16,fade_out=1.8):
        s.wd=wd;os.chdir(wd);c=json.load(open("cut.json"));s.S={x["name"]:x for x in c["seg"]};s.order=[x["name"] for x in c["seg"]]
        s.MAIN=c["total"];s.END=end;s.TOTAL=s.MAIN+end;s.bgm=bgm;s.off=off;s.ev=[];s.prevlast={};s.lastraw=None;s.lufs=lufs;s.fade_out=fade_out
    def vo(s,n):return s.S[n]["o"]
    def ve(s,n):return s.S[n]["o"]+s.S[n]["d"]
    def seg(s,t):
        for n in s.order:
            if s.vo(n)<=t<s.ve(n)-1e-6:return n,t-s.vo(n),s.S[n]["d"]
        n=s.order[-1];return n,t-s.vo(n),s.S[n]["d"]
    def hits(s,name,src):S=s.S[name];return [S["o"]+(h-S["a"])/S["speed"] for h in src]
    def frame_at(s,t):
        raw=subprocess.run(["ffmpeg","-v","error","-ss",f"{max(0,min(t,s.MAIN-0.04)):.3f}","-i","video.mp4","-frames:v","1","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
        return Image.frombytes("RGB",(OW,OH),raw)
    def prev(s,n):
        if n not in s.prevlast:
            i=s.order.index(n);s.prevlast[n]=s.frame_at(s.vo(n)-0.05) if i>0 else None
        return s.prevlast[n]
    def compose(s,raw,t):raise NotImplementedError
    def endframe(s,u):raise NotImplementedError
    def audio(s):
        T=s.TOTAL;fx=sfx.build(s.ev,T+1)[:int(T*SR)];sf.write("sfx_mono.wav",fx,SR)
        subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{s.off:.3f}","-i",s.bgm,"-i","sfx_mono.wav","-filter_complex",
          f"[0:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{T+0.5},asetpts=PTS-STARTPTS,loudnorm=I={s.lufs}:TP=-2,afade=t=in:d=0.04,afade=t=out:st={T-s.fade_out:.3f}:d={s.fade_out},apad,atrim=0:{T}[m];"
          f"[1:a]aformat=channel_layouts=stereo[x];[m][x]amix=inputs=2:normalize=0,alimiter=limit=0.8:level=disabled,atrim=0:{T}[o]","-map","[o]","-c:a","pcm_s16le","mix.wav"],check=True)
    def test(s,ts,name="chk.jpg"):
        os.makedirs("t",exist_ok=True)
        for f in os.listdir("t"):os.remove("t/"+f)
        for t in ts:
            if t<s.MAIN:img=s.compose(s.frame_at(t),t)
            else:
                if s.lastraw is None:s.lastraw=s.frame_at(s.MAIN-0.05)
                img=s.endframe(t-s.MAIN)
            img.convert("RGB").save(f"t/{t:05.2f}.jpg",quality=88)
        fs=sorted(os.listdir("t"));W,H=360,640;sh=Image.new("RGB",(W*len(fs),H))
        for i,f in enumerate(fs):sh.paste(Image.open("t/"+f).resize((W,H)),(i*W,0))
        sh.save(name,quality=86)
    def render(s,out):
        s.audio()
        rd=subprocess.Popen(["ffmpeg","-v","error","-i","video.mp4","-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE,bufsize=10**8)
        wr=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{OW}x{OH}","-r",str(FPS),"-i","-","-i","mix.wav","-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-t",f"{s.TOTAL:.3f}","-movflags","+faststart",out],stdin=subprocess.PIPE)
        N=int(round(s.MAIN*FPS));cur=None;last=None
        for i in range(N):
            b=rd.stdout.read(OW*OH*3);raw=Image.frombytes("RGB",(OW,OH),b) if len(b)==OW*OH*3 else last
            t=i/FPS;n=s.seg(t)[0]
            if n!=cur:
                if last is not None:s.prevlast[n]=last
                cur=n
            last=raw;wr.stdin.write(s.compose(raw,t).convert("RGB").tobytes())
        s.lastraw=last
        for i in range(int(round(s.END*FPS))):wr.stdin.write(s.endframe(i/FPS).convert("RGB").tobytes())
        wr.stdin.close();wr.wait();rd.kill();print("done",out,flush=True)
