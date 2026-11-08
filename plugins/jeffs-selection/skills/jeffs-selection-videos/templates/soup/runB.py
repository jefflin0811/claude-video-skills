# 版本 B｜綜藝音效字：comic sound words with bursts, punch zooms and shakes; 姐夫 speech-bubble captions
from base3 import *
TAG=label("姐夫開煮",size=58,bg=RED,fg=WHITE).rotate(-6,resample=Image.BICUBIC,expand=True)
TITLE=hook("無水雞湯",168,-4);BURST=burst2(300,WHITE,20,4)
GULU=punch("咕嚕咕嚕～",70,WHITE,-6)
BUBS=[bubble_dot(r) for r in (16,22,28)]
FIN=sound("上桌了！",150,YEL,-6,RED)
class VB(Base):
    def extra(s,base,t):
        if t<s.ve("hook"):   # opening (visible from frame 0)
            a=clamp((s.ve("hook")-0.04-t)/0.12)
            put(base,BURST,528,1300,a*0.92,1+0.05*bump(t-B),t*20)
            put(base,open5.doodle_pot(t,205),150,1100,a,1.0,math.sin(t*22)*4)
            put(base,GULU,250,958,a*clamp(t/0.2+1),1+0.08*math.sin(t*9))
            put(base,TAG,402,1124,a,1+0.05*bump(t-B))
            put(base,TITLE,528,1300,a,1+0.07*bump(t-B))
        # cooking: rising bubbles + flame that shrinks from 中火 to 小火
        a5=s.vo("s5")
        if a5<=t<s.ve("s5"):
            rng=random.Random(11)
            for i in range(12):
                ph=rng.uniform(0,1.6);x0=rng.uniform(260,820);sp=rng.uniform(260,420);u=((t-a5)+ph)%1.6
                put(base,BUBS[i%3],x0+math.sin(u*6+i)*14,1080-u*sp,clamp(u*4)*clamp((1.6-u)/0.4))
            half=t>=a5+4*B;lv=0.35 if half else 1.0;u=(t-a5-(4*B if half else 0))/0.35
            put(base,flame(300,lv,t),870,1150,clamp(u*3)*clamp((s.ve("s5")-t)/0.15),0.7+0.3*spring(u))
            g=(t-a5-0.3)/0.35
            if g>0:put(base,GULU,540,930+math.sin(t*7)*10,clamp(g*3)*clamp((s.ve("s5")-t)/0.15),(0.6+0.4*spring(g))*1.35)
    def extra_top(s,base,t):
        f=s.vo("s6a")
        if t>=f+B:confetti_layer(base,t,f+B,5,34)
    def end_extra(s,base,u):
        if u>=0.25:confetti_layer(base,u+100,100.25,9,30)
        twinkle(base,u+5,0,10,STP[:8])
V=VB();vo,ve=V.vo,V.ve;M=V.MAIN
SPY=1318
def say(t0,t1,text):
    im=speech(text,size=70);V.pop(t0,t1,im,24+im.size[0]/2,SPY)
def punchzoom(t0,cx=540,cy=1000,z=1.08):
    V.zoom(t0,t0+0.14,1.0,z,cx,cy);V.zoom(t0+0.14,t0+0.6,z,1.0,cx,cy)
# 1 onions: 唰～
a=vo("s1");say(a+0.25,ve("s1"),"首先[[洋蔥]]鋪底");V.pop(a+0.1,ve("s1"),sound("唰～",150,YEL,-10),770,960,0);punchzoom(a+0.1,600,900)
# 2 cabbage: 沙沙～
a=vo("s2");say(a+0.25,ve("s2"),"再鋪上[[白菜]]");V.pop(a+0.1,ve("s2"),sound("沙沙～",140,(176,226,96),8),760,980,0);punchzoom(a+0.1,540,900)
# 3 chicken: 咚！咚！ ×2
a=vo("s3");say(a+0.25,ve("s3"),"兩隻[[帶骨大雞腿]]")
V.pop(a+0.1,ve("s3"),sound("咚！",150,YEL,-8,WHITE),720,930,0);V.pop(a+B+0.1,ve("s3"),sound("咚！",150,YEL,8,WHITE),860,1080,0)
V.pop(a+2*B,ve("s3"),punch("×2",130,YEL,-8),300,980,0);V.shakes+=[(a+0.1,a+0.4),(a+B+0.1,a+B+0.4)];punchzoom(a+0.1,540,900,1.06);punchzoom(a+B+0.1,540,900,1.06)
# 4 apple + corn: stickers
a=vo("s4");say(a+0.25,ve("s4"),"一個[[蘋果]]＋一根[[玉米]]")
V.pop(a+0.1,ve("s4"),sound("＋蘋果",104,(255,120,104),-8),300,960,0);V.pop(a+B+0.1,ve("s4"),sound("＋玉米",104,YEL,7),780,1030,0)
punchzoom(a+0.1,540,900,1.05);punchzoom(a+B+0.1,540,900,1.05)
# 5 cooking
a=vo("s5");say(a+0.25,a+4*B-0.03,"[[中火]] 20 分鐘");say(a+4*B,ve("s5"),"轉[[小火]] 40 分鐘");V.fx("steam",a,ve("s5"),x=520,y=760,w=520,h=480,seed=3)
# finale
f=vo("s6a");say(f+0.08,ve("s6b"),"一鍋[[鮮甜美味]]的雞湯");V.hook(f+B,ve("s6b"),FIN,560,990);V.fx("twinkle",f,ve("s6b"))
punchzoom(f+B,540,960,1.07)
V.whips=[vo(k) for k in ("s1","s2","s3","s4","s5","s6a")];V.flashes=[B,vo("s6a")+B]
# sound
V.ev=[(0.03,DING,.5),(0.05,POPH,.36),(B,thud(),.5)]+[(0.15+i*0.33,blub(),.3) for i in range(5)]
for k in ("s1","s2","s3","s4","s5","s6a"):V.ev.append((vo(k)-0.14,WR,.3))
for k in ("s1","s2","s3","s4","s5"):V.ev.append((vo(k)+0.25,POP,.28))
V.ev+=[(vo("s1")+0.1,sfx.whoosh(.5,False),.5),(vo("s2")+0.1,rustle(.55),.55)]
V.ev+=[(vo("s3")+0.1,thud(),.85),(vo("s3")+B+0.1,thud(),.85),(vo("s3")+2*B,POPH,.32)]
V.ev+=[(vo("s4")+0.1,POPH,.4),(vo("s4")+B+0.1,POPH,.4)]
V.ev+=[(vo("s5")+0.3+i*0.28,blub(),.3) for i in range(15)]+[(vo("s5")+4*B,sfx.pop(640),.32)]
V.ev+=[(f+0.08,POP,.3),(f+B,BOOM,.45),(f+B+0.02,thud(),.6),(f+B+0.06,CHM,.3)]+[(f+B+0.1+i*0.07,POP if i%2 else POPH,.16) for i in range(6)]
V.ev+=[(M+0.02,WH,.3),(M+0.25,BOOM,.25),(M+0.3,CHM,.24)]
if __name__=="__main__":
    if "test" in sys.argv:
        V.sheet([0.0,0.75,vo("s1")+0.5,vo("s2")+0.6,vo("s3")+0.4,vo("s3")+1.5,vo("s4")+1.2,vo("s5")+1.4,vo("s5")+4*B+1.2,vo("s6a")+1.0,vo("s6b")+1.8,M+2.4],SP+"soup/B_sheet.jpg");print("ok")
    if "render" in sys.argv:V.render(SP+"soup/姐夫開煮_無水雞湯_版本B_綜藝音效.mp4")
