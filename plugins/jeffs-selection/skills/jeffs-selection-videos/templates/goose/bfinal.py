# 姐夫探店｜風格 B 職人紀錄（定版）：保留原版 B 的電影黑邊、調色顆粒、切肉時的大標題字卡、左下菜名＋銅線、黑底資訊頁；
# 只改固定規則衝突的地方：左上角圓形半透明 logo、上方黑邊不放字、開頭三分之二處放「姐夫探店＋店名＋小插畫」、
# 字幕移到畫面內（避開平台下方說明文字區）並放大、直排字移到左邊（避開右側按鈕）、片尾米白底＋銅色字
import sys,os
sys.path.insert(0,"__ROOT__/goose")
from craft import *
def mk_grade2(lift,gamma,sat,sh,hi,con):
    lut=[]
    for c in range(3):
        for v in range(256):
            x=v/255;y=lift+(1-lift)*(x**gamma);y+=con*(y-0.5)*(1-abs(2*y-1));y+=sh[c]*(1-x)**2+hi[c]*x**2;lut.append(int(round(min(max(y,0),1)*255)))
    def g(img):
        img=img.point(lut);return ImageEnhance.Color(img).enhance(sat) if abs(sat-1)>0.01 else img
    return g
def _band(h=560,amax=0.5):
    g=np.clip(1-np.abs(np.linspace(-1,1,h))**1.6,0,1)*amax;a=(np.tile(g[:,None],(1,OW))*255).astype(np.uint8)
    im=Image.new("RGBA",(OW,h),(6,4,3,0));im.putalpha(Image.fromarray(a));return im
BAND=_band()
SUBY=1440
class BFinal(Cinema):
    name="bfinal";grain=4.5;vig=0.26
    grade=staticmethod(mk_grade2(0.02,1.12,0.9,(-0.035,0.0,0.035),(0.05,0.018,-0.045),0.10))
    def text(s,base,t,n,u,d):
        out=clamp((d-u)/0.22);X=60;S52=SER(600,52)
        if n=="store":
            show(base,ICON,X,1030,out);show(base,TK("姐夫探店",SER(600,54),WARM,8),X+110,1050,out)
            show(base,TK("後驛鵝肉店",SER(700,128),WARM,14),X-4,1124,out);show(base,line3(150,4,GOLD),X,1278,out)
            show(base,TK("台北車站後站・巷弄老店",SER(600,50),WARM,4),X,1302,out)
        elif n=="case":cshow(base,TK(SUB["case"],S52,WARM,2),1330,rv(u,0.5,0.3),out)
        elif n=="chop":
            a=clamp(u/0.35)*clamp((3.0-u)/0.5);L=int(320*ease((u-0.1)/0.6))
            if a>0:
                put(base,fade(BAND,a),540,1250)
                tt=TK("巷弄裡的老味道",SER(700,100),WARM,20);w,h=vis(tt);sc=1.04-0.04*ease(u/2.6)
                put(base,tt,540,1210,a,sc)
                put(base,TK("姐夫嚴選・台北車站後站",SER(600,46),WARM,10),540,1322,a*clamp((u-0.4)/0.4))
                if L>3:show(base,line3(2*L,3,GOLD),540-L,1120,a);show(base,line3(2*L,3,GOLD),540-L,1384,a)
            cshow(base,TK(SUB["chop"],S52,WARM,2),SUBY,rv(u,0.5,0.6),out)
        elif n in DISHES:
            i=DISHES.index(n);kicker4(base,CN[i],X,1196,out,v=rv(u,0.5,0.15),size=60)
            show_rise(base,TK(DISH[i],SER(700,96),WARM,10),X-2,1268,rv(u,0.55,0.25),out)
            cshow(base,TK(SUB[n],S52,WARM,2),SUBY,rv(u,0.5,0.45),out)
        elif n=="all":
            im=TK("四道必點",SER(700,104),WARM,0,True,True,1.12);v=clamp((u-0.15)/0.9)
            if v>0:show(base,wipe(im,ease(v)),X,960,out)
            cshow(base,TK(SUB["all"],S52,WARM,2),SUBY,rv(u,0.5,0.6),out)
    def compose(s,raw,t):
        base=super().compose(raw,t);c=s.vo("chop")
        if c-0.1<=t<c:base=Image.new("RGBA",(OW,OH),(8,7,6,255));paste_mark(base)
        if t>s.MAIN-0.35:base=Image.blend(base,Image.new("RGBA",(OW,OH),(14,12,10,255)),inout((t-(s.MAIN-0.35))/0.35))
        s.last_comp=base;return base
def inout(u):u=clamp(u);return u*u*(3-2*u)
if __name__=="__main__":
    V=BFinal()
    if sys.argv[1]=="render":V.render(SP+"goose/後驛鵝肉_姐夫探店_風格B職人紀錄_定版.mp4")
    elif sys.argv[1]=="sheet":
        ts=[float(x) for x in sys.argv[2].split(",")];ims=[V.still(t) for t in ts]
        cw=432;ch=768;n=5;sh=Image.new("RGB",(cw*min(n,len(ims)),ch*((len(ims)+n-1)//n)),(255,255,255))
        for i,im in enumerate(ims):sh.paste(im.resize((cw,ch),Image.LANCZOS),((i%n)*cw,(i//n)*ch))
        sh.save(SP+"goose/bfinal_sheet.jpg",quality=86);print("ok")
