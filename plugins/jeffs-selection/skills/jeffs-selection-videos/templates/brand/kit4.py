# round 4 — fixed text placement: titles only in the empty top band or bottom band, never over faces/products; left margin shared with the logo
import sys;sys.path.insert(0,"__ROOT__/brand")
from kit3 import *
B4="__ROOT__/brand/hero/"
HERO4=[Image.open(B4+n+".png").convert("RGBA") for n in ["h0","h1","h2b","h3","h4","h5","h6b","h7","h8"]] if os.path.exists(B4+"h0.png") else []  # 舊版封面測試圖，技能包未附
ANCH=["top","top","top","bottom","top","top","bottom","top","bottom"]
TOPY=(270,600);BOTY=(1150,1480)
def shade(anchor,amax=0.55):
    if anchor=="top":g=np.clip(1-np.arange(OH)/800,0,1)**1.3*amax
    else:g=np.clip((np.arange(OH)-950)/970,0,1)**1.1*(amax+0.1)
    im=Image.new("RGBA",(OW,OH),(8,5,3,0));im.putalpha(Image.fromarray((np.tile(g[:,None],(1,OW))*255).astype(np.uint8)));return im
def pill(series,size=40):
    c=SERIES[series]["col"];f=SANS("900Black",size);tx="#"+SERIES[series]["name"];w=int(f.getlength(tx))+52;h=int(size*1.55);pl=blank(w+20,h+20);pd=ImageDraw.Draw(pl)
    pd.rounded_rectangle((10,10,w+10,h+10),radius=h//2,fill=c+(255,));pd.text((10+w/2,10+h/2+1),tx,font=f,fill=WH,anchor="mm");return shadow(pl,6,(0,3),0.35)
def stack(items,gap=14):
    """vertical stack of images (centered); returns image"""
    W=max(i.size[0] for i in items);H=sum(i.size[1] for i in items)+gap*(len(items)-1);im=blank(W,H);y=0
    for i in items:im.alpha_composite(i,((W-i.size[0])//2,y));y+=i.size[1]+gap
    return im
TOPMIN={3:1075,6:1150,8:1160}
CUR=[0]
def place(b,blk,anchor,align="center",x0=56):
    y0,y1=TOPY if anchor=="top" else BOTY;h=blk.size[1]
    y=y0-12 if anchor=="top" else max(TOPMIN.get(CUR[0],1150),min(1600-h,y1-h+12))
    if align=="center":paste(b,blk,(OW-blk.size[0])/2,y)
    else:paste(b,blk,x0,y)
def base(h,anchor):
    b=h.copy();b.alpha_composite(TOPS);b.alpha_composite(shade(anchor));paste(b,LOGO_W,34,30);return b
# A 鉤子大字（修正）
def a4(i):
    CUR[0]=i;series,title,sub=ITEMS[i];hk=HOOK[i];an=ANCH[i];b=base(HERO4[i],an)
    l1=stroked(hk[0],fitf(hk[0],ROUND,118,960,11),WH,BLK,11);l2=stroked(hk[1],fitf(hk[1],ROUND,100,960,10),YEL,BLK,10)
    place(b,stack([pill(series),l1,l2],0),an);return b
# B 真人＋賣點（修正）
def b4(i):
    CUR[0]=i;series,title,sub=ITEMS[i];hk=HOOK[i];an=ANCH[i];c=SERIES[series]["col"];b=base(HERO4[i],an)
    br=stroked("＼ "+SERIES[series]["name"]+" ／",SANS("900Black",44),WH,c,7);t=stroked(title,fitf(title,SANSB,140,960,14),WH,c,14);s=stroked(hk[1],SANS("900Black",54),YEL,BLK,7)
    place(b,stack([br,t,s],0),an);return b
CALL4={0:[("煙燻鵝腿",(430,1150),(230,1460)),("現切薑絲",(800,760),(880,1000))],1:[("牛肉爐湯底",(560,1150),(300,1500)),("大塊牛肉",(650,820),(880,1000))],
       2:[("牛肉爐",(560,1560),(860,1330)),("加料",(520,1370),(220,1180))],3:[],4:[("鵝腸",(520,1020),(240,1350)),("當歸湯",(760,1300),(840,1560))],
       5:[("高麗菜",(700,760),(880,1040))],6:[("大塊牛肉",(430,620),(800,420))],7:[("Q 彈麵條",(560,820),(860,1060)),("牛肉湯",(480,1380),(240,1560))],8:[("現切櫥窗",(500,1000),(820,780))]}
# C 雜誌標註（修正）：標題跟 logo 同一條左邊線，標註只指食物、商品
def c4(i):
    CUR[0]=i;series,title,sub=ITEMS[i];hk=HOOK[i];an=ANCH[i];c=SERIES[series]["col"];b=base(HERO4[i],an)
    lab=tsh(T(SERIES[series]["name"]+"｜"+hk[1],SANS("700Bold",38),WH,track=4),6,0.6);bar=blank(90,8);ImageDraw.Draw(bar).rectangle((0,0,90,8),fill=c+(255,))
    t=tsh(T(title,fit(title,SER,124,960,4),track=4),12,0.65)
    blk=blank(max(lab.size[0],t.size[0])+10,lab.size[1]+18+t.size[1]);blk.alpha_composite(lab,(0,0));blk.alpha_composite(bar,(14,lab.size[1]-4));blk.alpha_composite(t,(0,lab.size[1]+18))
    place(b,blk,an,"left",40)
    for lbl,p,q in CALL4.get(i,[]):callout(b,lbl,p,q)
    return b
# D 統一封面卡（修正）：字放大、照片縮小，整塊放在個人頁顯示範圍內
def d4(i):
    series,title,sub=ITEMS[i];hk=HOOK[i];c=SERIES[series]["col"];b=Image.new("RGBA",(OW,OH),CARDBG+(255,));d=ImageDraw.Draw(b)
    D=600;cx,cy=540,820;h=HERO4[i].convert("RGB")
    ccx,ccy,S={2:(600,1120,1240),3:(560,800,1000),8:(540,900,1250)}.get(i,(540,900,1100));ph=h.crop((ccx-S/2,ccy-S/2,ccx+S/2,ccy+S/2)).resize((D,D),Image.LANCZOS)
    m=Image.new("L",(D*3,D*3),0);ImageDraw.Draw(m).ellipse((0,0,D*3-1,D*3-1),fill=255);m=m.resize((D,D),Image.LANCZOS)
    circ=Image.new("RGBA",(D,D));circ.paste(ph,(0,0));circ.putalpha(m);paste(b,shadow(circ,22,(0,16),0.35),cx-D/2-44,cy-D/2-44)
    d.ellipse((cx-D/2-16,cy-D/2-16,cx+D/2+16,cy+D/2+16),outline=c+(255,),width=5)
    put(b,logo_h(120),540,380)
    put(b,T(title,fit(title,SER,128,940,4),INK,track=4),540,1270)
    put(b,T(hk[1],KAI("700Bold",58),c,track=2),540,1405)
    pl=pill(series,36);put(b,pl,540,1530);return b
DIRS4=[("A 鉤子大字",a4),("B 真人＋賣點",b4),("C 雜誌標註",c4),("D 統一封面卡",d4)]
