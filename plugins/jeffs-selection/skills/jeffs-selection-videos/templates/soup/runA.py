# 版本 A｜手繪食材圖鑑：each ingredient pops in as a cartoon doodle, then drops into a running ingredient row
from base3 import *
ICON=290;ROW_Y=1458;ROW_S=132
ICONS={"onion":onion(ICON),"cabbage":cabbage(ICON),"drum":drumstick(ICON),"apple":apple(ICON),"corn":corn(ICON)}
X2=punch("×2",70,YEL,-8)
TAG=label("姐夫開煮",size=58,bg=RED,fg=WHITE).rotate(-6,resample=Image.BICUBIC,expand=True)
TITLE=textrun(parse("無水雞湯"),F("k",166),(WHITE,WHITE),14,INK,outer=(YEL,10),pad=80).rotate(-3,resample=Image.BICUBIC,expand=True)
MINI={"corn":corn(150,14),"apple":apple(140),"onion":onion(140)}
FINH=hook("上桌了！",160,-4)
class VA(Base):
    def setup(s):
        vo=s.vo;s.ing=[("onion",vo("s1")+0.12,(800,1010)),("cabbage",vo("s2")+0.12,(800,1010)),("drum",vo("s3")+0.12,(780,1000)),
                       ("apple",vo("s4")+0.12,(700,1010)),("corn",vo("s4")+B+0.12,(880,1060))]
        s.slot={k:(118+i*150,ROW_Y) for i,(k,_,_) in enumerate(s.ing)};s.row_out=s.vo("s6a")+B-0.45
    def extra(s,base,t):
        if t<s.ve("hook"):   # opening (visible from frame 0)
            a=clamp((s.ve("hook")-0.04-t)/0.12)
            put(base,open5.doodle_pot(t,205),150,1100,a)
            for i,(k,(x,y)) in enumerate([("corn",(895,1160)),("apple",(898,1430)),("onion",(112,1440))]):
                put(base,MINI[k],x,y+math.sin(t*5+i*2)*6,a,1+0.12*bump(t-B-i*0.08))
            put(base,TAG,402,1124,a,1+0.05*bump(t-B))
            put(base,TITLE,528,1298,a,1+0.06*bump(t-B))
    def extra_top(s,base,t):
        # ingredient doodles: pop big -> fly into the row -> stay
        row_a=clamp((s.row_out+0.35-t)/0.35)
        for k,tp,(px,py) in s.ing:
            if t<tp:continue
            tf=tp+1.0;sx,sy=s.slot[k];im=ICONS[k]
            if t<tf:
                u=(t-tp)/0.4;put(base,im,px,py,clamp(u*3),0.5+0.5*spring(u),math.sin((t-tp)*7)*5)
                if k=="drum" and t>tp+0.45:put(base,X2,px+150,py-110,1,0.8+0.5*spring((t-tp-0.45)/0.35))
            else:
                v=ease((t-tf)/0.38);x=px+(sx-px)*v;y=py+(sy-py)*v-math.sin(math.pi*v)*120;sc=1+(ROW_S/ICON-1)*v
                put(base,im,x,y,row_a,sc)
                if k=="drum":put(base,X2,x+60,y-46,row_a,0.6)
        # step 5: big flame (中火) -> small flame (小火)
        a=s.vo("s5")
        if a<=t<s.ve("s5"):
            half=t>=a+4*B;lv=0.35 if half else 1.0;u=(t-a-(4*B if half else 0))/0.35
            put(base,flame(310,lv,t),830,1030,clamp(u*3)*clamp((s.ve("s5")-t)/0.15),0.7+0.3*spring(u))
        # finale bowl
        f=s.vo("s6a")
        if t>=f+0.1:
            u=(t-f-0.1)/0.4;bw=bowl(310);put(base,bw,820,990,clamp(u*3),0.5+0.5*spring(u),math.sin(t*3)*3)
            steam_layer(base,t,820,860,200,240,3,clamp(u),2)
    def end_extra(s,base,u):
        for i,k in enumerate(["onion","cabbage","drum","apple","corn"]):
            v=(u-0.75-i*0.1)/0.35
            if v>0:put(base,ICONS[k],300+i*120,1450,clamp(v*3),(0.5+0.5*spring(v))*0.42)
        twinkle(base,u+5,0,10,STP[:8])
V=VA();V.setup();vo,ve=V.vo,V.ve;M=V.MAIN
CAPY=1292
STEPS=[("s1","1","首先洋蔥鋪底"),("s2","2","再鋪上白菜"),("s3","3","兩隻帶骨大雞腿"),("s4","4","一個蘋果＋一根玉米")]
for k,n,txt in STEPS:
    im=label(txt,icon=n,size=70,bg=CREAM,fg=INK,accent=RED);V.slide(vo(k)+0.05,ve(k),im,28+im.size[0]/2,CAPY,"L")
a=vo("s5");i1=label("中火 20 分鐘",icon="5",size=70,bg=CREAM,fg=INK,accent=RED);i2=label("轉小火 40 分鐘",icon="5",size=70,bg=CREAM,fg=INK,accent=RED)
V.slide(a+0.05,a+4*B-0.03,i1,28+i1.size[0]/2,CAPY,"L");V.pop(a+4*B,ve("s5"),i2,28+i2.size[0]/2,CAPY)
V.fx("steam",a,ve("s5"),x=520,y=760,w=520,h=480,seed=3)
f=vo("s6a");c1=label("一鍋鮮甜美味的雞湯",size=70,bg=CREAM,fg=INK);V.slide(f+0.08,ve("s6b"),c1,28+c1.size[0]/2,1150,"L")
V.hook(f+B,ve("s6b"),FINH,520,1330);V.fx("hearts",f+0.4,ve("s6b"),n=6);V.fx("twinkle",f,ve("s6b"))
V.zoom(0,ve("hook"),1.0,1.05,540,1000)
for k,z in (("s1",1.05),("s2",1.09),("s3",1.09),("s4",1.06),("s5",1.05),("s6a",1.07)):V.zoom(vo(k),ve(k),1.0,z,540,900)
V.zoom(vo("s6b"),ve("s6b"),1.06,1.0,540,960)
V.whips=[vo(k) for k in ("s1","s2","s3","s4","s5","s6a")];V.flashes=[B,vo("s6a")]
V.ev=[(0.03,DING,.5),(0.05,POPH,.36),(B,thud(),.45),(B+0.04,POP,.28)]
for k in ("s1","s2","s3","s4","s5","s6a"):V.ev.append((vo(k)-0.14,WR,.3))
for k,tp,_ in V.ing:V.ev+=[(tp,POP,.38),(tp+1.0,WH,.16),(tp+1.36,POPH,.22)]
V.ev+=[(vo("s3")+0.57,POPH,.3),(vo("s5")+0.1,WH,.3),(vo("s5")+4*B,sfx.pop(640),.32)]
V.ev+=[(f+0.08,BOOM,.4),(f+0.1,POP,.3),(f+B,thud(),.65),(f+B+0.04,CHM,.3),(f+2.2*B,sparkle_snd(),.28)]
V.ev+=[(M+0.02,WH,.3),(M+0.3,POP,.28)]+[(M+0.75+i*0.1,POPH if i%2 else POP,.2) for i in range(5)]+[(M+1.4,CHM,.24)]
if __name__=="__main__":
    if "test" in sys.argv:
        V.sheet([0.0,0.75,vo("s1")+0.5,vo("s1")+1.6,vo("s2")+1.5,vo("s3")+0.8,vo("s4")+1.0,vo("s4")+2.6,vo("s5")+1.4,vo("s5")+4*B+1.2,vo("s6a")+1.3,vo("s6b")+2.0,M+0.4,M+2.4],SP+"soup/A_sheet.jpg");print("ok")
    if "render" in sys.argv:V.render(SP+"soup/姐夫開煮_無水雞湯_版本A_手繪食材.mp4")
