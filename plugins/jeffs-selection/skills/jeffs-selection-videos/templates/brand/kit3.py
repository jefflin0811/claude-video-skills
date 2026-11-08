# round 3 — directions modelled on what popular Taiwanese creators do (hook titles on footage, talent + selling point, magazine callouts, uniform cover card)
import sys;sys.path.insert(0,"__ROOT__/brand")
from kit2 import *
FR="__ROOT__/fonts/"
def ROUND(s):return sty._f(FR+"ChironGoRoundTC_900Black.ttf",s)
YEL=(255,214,74);BLK=(18,12,8)
HOOK=[("台北車站後站","巷子裡的鵝肉老店"),("一包牛肉爐","變出咖哩牛肉"),("半筋半肉牛肉爐","呂捷開箱實測"),
      ("HABA 柔膚水","日本 HABA 限時團購"),("當歸鵝腸湯","後驛鵝肉店必點"),("老店薑母雞","在家加熱就能吃"),
      ("全肉牛肉爐","一包有幾塊肉？"),("30 秒牛肉麵","30 秒快速出爐"),("後驛鵝肉店","巷弄裡的現切櫥窗")]
def stroked(text,font,fill,stroke=BLK,sw=10,track=0,sh=True):
    ws=[font.getlength(c) for c in text];asc,desc=font.getmetrics();pad=sw+8;W=int(sum(ws)+track*max(0,len(text)-1))+2*pad;H=asc+desc+2*pad
    im=blank(W,H);d=ImageDraw.Draw(im);x=pad
    for c,w in zip(text,ws):d.text((x,pad),c,font=font,fill=fill+(255,),stroke_width=sw,stroke_fill=stroke+(255,));x+=w+track
    return shadow(im,8,(0,6),0.5,(0,0,0)) if sh else im
def fitf(text,fn,size,maxw,sw=10):
    while fn(size).getlength(text)+2*sw>maxw and size>40:size-=4
    return fn(size)
def slabel(series,size=40,col=WH,stroke=BLK):
    c=SERIES[series];return stroked("#"+c["name"],SANS("900Black",size),col,stroke,6)
# R1 鉤子大字：標題放上半部，白字黑邊＋黃色第二行（探店熱門寫法）
def r1(h,series,title,sub,hook):
    b=h.copy();b.alpha_composite(TOPS);b.alpha_composite(scrim(0,1,0));g=np.clip(1-np.abs(np.arange(OH)-560)/520,0,1)**1.2*0.35
    sh=Image.new("RGBA",(OW,OH),(0,0,0,0));sh.putalpha(Image.fromarray((np.tile(g[:,None],(1,OW))*255).astype(np.uint8)));b.alpha_composite(sh)
    paste(b,LOGO_W,34,30)
    c=SERIES[series]["col"];f=SANS("900Black",42);tx="#"+SERIES[series]["name"];w=int(f.getlength(tx))+56;pl=blank(w+20,84);pd=ImageDraw.Draw(pl)
    pd.rounded_rectangle((10,10,w+10,74),radius=32,fill=c+(255,));pd.text((10+w/2,42),tx,font=f,fill=WH,anchor="mm");put(b,shadow(pl,6,(0,3),0.35),540,335)
    l1=stroked(hook[0],fitf(hook[0],ROUND,128,1000),WH,BLK,11);put(b,l1,540,470)
    l2=stroked(hook[1],fitf(hook[1],ROUND,112,1000),YEL,BLK,11);put(b,l2,540,620);return b
# R2 真人＋賣點：主角入鏡，大字賣點用系列色描邊（團購熱門寫法）
def r2(h,series,title,sub,hook):
    c=SERIES[series]["col"];b=h.copy();b.alpha_composite(TOPS);b.alpha_composite(scrim(900,1920,0.55,curve=1.3));paste(b,LOGO_W,34,30)
    br=stroked("＼ "+SERIES[series]["name"]+" ／",SANS("900Black",44),WH,c,7);put(b,br,540,1080)
    t=stroked(title,fitf(title,SANSB,150,1000,14),WH,c,14);put(b,t,540,1230)
    s=stroked(hook[1],SANS("900Black",54),YEL,BLK,7);put(b,s,540,1385);return b
CALL={0:[("煙燻鵝腿",(560,1080),(250,1380)),("現切薑絲",(800,640),(820,980))],1:[("牛肉爐湯底",(560,1150),(300,1450)),("大塊牛肉",(620,820),(800,560))],
      2:[("半筋半肉",(600,1000),(840,1260)),("呂捷",(540,430),(250,700))],3:[("翠蕊",(560,560),(820,820))],4:[("鵝腸",(520,1020),(250,1350)),("當歸湯",(760,1250),(820,1500))],
      5:[("高麗菜",(700,700),(860,1000)),("薑母雞湯",(500,1300),(260,1520))],6:[("大塊牛肉",(520,700),(260,1000)),("湯頭",(560,1400),(840,1560))],
      7:[("Q 彈麵條",(560,900),(250,1180)),("牛肉湯",(480,1400),(800,1560))],8:[("招牌",(540,330),(820,620)),("現切櫥窗",(450,1000),(250,1250))]}
def callout(b,label,p,q):
    sh=blank(OW,OH);sd=ImageDraw.Draw(sh);sd.line([p,q],fill=(0,0,0,150),width=9);b.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)))
    d=ImageDraw.Draw(b);d.line([p,q],fill=WH+(255,),width=5);d.ellipse((p[0]-14,p[1]-14,p[0]+14,p[1]+14),outline=WH+(255,),width=5);d.ellipse((p[0]-5,p[1]-5,p[0]+5,p[1]+5),fill=WH+(255,))
    t=stroked(label,SANS("900Black",54),WH,BLK,6);w=t.size[0];x=q[0]-w/2 if 120<q[0]<960 else (q[0]-w+20 if q[0]>=960 else q[0]-20)
    x=min(max(x,30),OW-w-30);paste(b,t,x,q[1]-(t.size[1]+6 if q[1]<p[1] else -6))
# R3 雜誌標註：大標在上，細線標註商品／菜色重點（日系雜誌感）
def r3(h,series,title,sub,hook,idx=0):
    b=h.copy();b.alpha_composite(TOPS);g=np.clip(1-np.arange(OH)/760,0,1)**1.3*0.62
    sh=Image.new("RGBA",(OW,OH),(10,6,3,0));sh.putalpha(Image.fromarray((np.tile(g[:,None],(1,OW))*255).astype(np.uint8)));b.alpha_composite(sh);paste(b,LOGO_W,34,30)
    c=SERIES[series]["col"];lab=tsh(T(SERIES[series]["name"]+"｜"+hook[1],SANS("700Bold",36),WH,track=4),6,0.6);putl(b,lab,232,300)
    ImageDraw.Draw(b).rectangle((232,342,312,348),fill=c+(255,))
    t=tsh(T(title,fit(title,SER,120,820,4),track=4),12,0.65);putl(b,t,222,430)
    for lbl,p,q in CALL.get(idx,[]):callout(b,lbl,p,q)
    return b
# R4 統一封面卡：同底色、圓形菜色照、同一句型標題（像果妹的「○○的秘密」），只當個人頁封面用
CARDBG=(240,232,224)
def r4(h,series,title,sub,hook):
    b=Image.new("RGBA",(OW,OH),CARDBG+(255,));d=ImageDraw.Draw(b);c=SERIES[series]["col"]
    D=700;cx,cy=540,820;ph=h.convert("RGB").resize((OW,OH)).crop((540-D*0.75,cy-D*0.75,540+D*0.75,cy+D*0.75)).resize((D,D),Image.LANCZOS)
    m=Image.new("L",(D*3,D*3),0);ImageDraw.Draw(m).ellipse((0,0,D*3-1,D*3-1),fill=255);m=m.resize((D,D),Image.LANCZOS)
    circ=Image.new("RGBA",(D,D));circ.paste(ph,(0,0));circ.putalpha(m);paste(b,shadow(circ,22,(0,16),0.35),cx-D/2-44,cy-D/2-44)
    d.ellipse((cx-D/2-18,cy-D/2-18,cx+D/2+18,cy+D/2+18),outline=c+(255,),width=4)
    put(b,logo_h(150),540,300)
    t=T(title,fit(title,SER,104,900,4),INK,track=4);put(b,t,540,1320)
    s=T("姐夫說："+hook[1],KAI("700Bold",48),c,track=2);put(b,s,540,1440)
    return b
DIRS=[("A 鉤子大字","探店熱門寫法：標題放上半部，白字黑邊＋黃色第二行，字句寫成鉤子",lambda h,i:r1(h,*ITEMS[i],HOOK[i])),
      ("B 真人＋賣點","團購熱門寫法：人拿商品入鏡，大字直接寫賣點，系列色描邊",lambda h,i:r2(h,*ITEMS[i],HOOK[i])),
      ("C 雜誌標註","日系雜誌感：大標在上，用細線標出菜色、商品的重點",lambda h,i:r3(h,*ITEMS[i],HOOK[i],i)),
      ("D 統一封面卡","學果妹：封面另外做一張，同底色、圓形照片、同一句型標題，只當個人頁封面",lambda h,i:r4(h,*ITEMS[i],HOOK[i]))]
