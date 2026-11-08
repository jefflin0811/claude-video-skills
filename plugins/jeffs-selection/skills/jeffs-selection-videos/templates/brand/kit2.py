# 姐夫嚴選 opening templates, round 2 — no solid panels behind text, natural (card-less) logo
import sys;sys.path.insert(0,"__ROOT__/brand")
from kit import *
B="__ROOT__/brand/"
WH=(252,249,244)
ITEMS=[("探店","後驛鵝肉店","台北車站後站｜必吃 4 道"),("開箱","牛肉爐變咖哩","一包牛肉爐｜多一道料理"),("開箱","半筋半肉牛肉爐","丸滿 × 姐夫嚴選｜開箱試吃"),
       ("團購","HABA 柔膚水","日本 HABA｜限時團購"),("探店","當歸鵝腸湯","後驛鵝肉店｜暖胃必喝"),("開箱","老店薑母雞","在家加熱｜湯頭超清甜"),
       ("團購","全肉牛肉爐","丸滿 × 姐夫嚴選｜限時團購"),("開箱","30 秒牛肉麵","一包牛肉爐｜快速上桌"),("探店","巷弄鵝肉老店","後驛鵝肉店｜台北車站後站")]
HERO=[Image.open(B+f"hero/h{i}.png").convert("RGBA") for i in range(9)] if os.path.exists(B+"hero/h0.png") else []  # 舊版封面測試圖，技能包未附
def wlogo(h=150,al=0.96):
    lg=logo_h(h,WH);return shadow(fade(lg,al),6,(0,2),0.45,(10,5,0))
LOGO_W=wlogo(172)
def corner():
    yy,xx=np.mgrid[0:OH,0:OW];r=np.sqrt((xx/1.0)**2+(yy/1.15)**2);a=np.clip(1-r/520,0,1)**1.7*0.55
    im=Image.new("RGBA",(OW,OH),(12,6,2,0));im.putalpha(Image.fromarray((a*255).astype(np.uint8)));return im
CORNER=corner()
def scrim(y0,y1,amax=0.78,col=(22,13,8),curve=1.4,side="bottom"):
    if side=="bottom":
        g=np.clip((np.arange(OH)-y0)/(y1-y0),0,1)**curve*amax;a=np.tile(g[:,None],(1,OW))
    else:
        g=np.clip(1-np.arange(OW)/y1,0,1)**curve*amax;a=np.tile(g[None,:],(OH,1))
    im=Image.new("RGBA",(OW,OH),col+(0,));im.putalpha(Image.fromarray((a*255).astype(np.uint8)));return im
TOP=scrim(0,1,0.0)
def topshade():
    g=np.clip(1-np.arange(OH)/320,0,1)**1.6*0.45;im=Image.new("RGBA",(OW,OH),(15,8,4,0));im.putalpha(Image.fromarray((np.tile(g[:,None],(1,OW))*255).astype(np.uint8)));return im
TOPS=topshade();TOPS.alpha_composite(CORNER);SB=scrim(820,1920,0.80);SB2=scrim(980,1920,0.70)
def T(text,font,col=WH,track=0,al=255):return ttext(text,font,col+(al,),track=track)
def tsh(im,b=10,al=0.55):return shadow(im,b,(0,3),al,(10,5,0))
def fit(text,fn,size,maxw,track=0):
    while fn(size).getlength(text)+track*len(text)>maxw and size>40:size-=4
    return fn(size)
SANSB=lambda s:SANS("900Black",s);SER=lambda s:SERIF("900Black",s)
def series_line(series,col_text=WH,size=38,dash=56):
    c=SERIES[series];t=T(c["name"],SANS("700Bold",size),col_text,track=6);w=dash+18+t.size[0];im=blank(w,t.size[1])
    ImageDraw.Draw(im).rectangle((0,im.size[1]/2-3,dash,im.size[1]/2+3),fill=c["col"]+(255,));im.alpha_composite(t,(dash+18-6,0));return im
# ---------------- six options ----------------
def o1(h,series,title,sub):   # 海報宋體：底部漸層＋白色粗宋大標
    b=h.copy();b.alpha_composite(TOPS);b.alpha_composite(SB);paste(b,LOGO_W,34,30)
    paste(b,tsh(series_line(series)),66,1100-30)
    tt=tsh(T(title,fit(title,SER,136,940,4),track=4),12,0.6);paste(b,tt,52,1190)
    paste(b,tsh(T(sub,SANS("500Medium",40),WH,track=2,al=235),8,0.5),62,1360);return b
def o2(h,series,title,sub):   # 系列色漸層：每個系列一種色光
    c=SERIES[series]["col"];b=h.copy();b.alpha_composite(TOPS);b.alpha_composite(scrim(760,1920,0.93,c,1.25));b.alpha_composite(scrim(1100,1920,0.35,(10,6,4),1.0))
    paste(b,LOGO_W,34,30)
    ic=icon(SERIES[series]["icon"],44,WH+(255,));lab=T(SERIES[series]["name"],SANS("700Bold",40),track=8);w=ic.size[0]+16+lab.size[0];lb=blank(w,max(ic.size[1],lab.size[1]))
    lb.alpha_composite(ic,(0,(lb.size[1]-ic.size[1])//2));lb.alpha_composite(lab,(ic.size[0]+10,(lb.size[1]-lab.size[1])//2));put(b,tsh(lb,6,0.4),540,1135)
    put(b,tsh(T(title,fit(title,SANSB,140,960,2),track=2),10,0.45),540,1280)
    put(b,tsh(T(sub,SANS("500Medium",40),WH,track=2,al=240),6,0.4),540,1415);return b
def seal2(series,s=104):
    c=SERIES[series]["col"];k=3;S=s*k;im=blank(S,S);d=ImageDraw.Draw(im);d.rounded_rectangle((0,0,S-1,S-1),radius=12*k,fill=c+(255,))
    d.rounded_rectangle((7*k,7*k,S-7*k,S-7*k),radius=8*k,outline=WH+(255,),width=2*k);t=series
    f=SERIF("900Black",int(S*0.36));d.text((S/2,S*0.32),t[0],font=f,fill=WH,anchor="mm");d.text((S/2,S*0.70),t[1],font=f,fill=WH,anchor="mm")
    return shadow(im.resize((s,s),Image.LANCZOS),6,(0,3),0.4)
def o3(h,series,title,sub):   # 直排題字：左側直排宋體＋系列印章
    b=h.copy();b.alpha_composite(scrim(0,640,0.72,side="left",curve=1.3));b.alpha_composite(TOPS);paste(b,LOGO_W,34,30)
    t=title.replace(" ","");n=len(t);fs=128 if n<=5 else (112 if n<=6 else 98)
    vt=tsh(vtext(t,SERIF("900Black",fs),WH+(255,),1.08),12,0.6);paste(b,vt,70,300)
    s1=sub.split("｜")[0].replace(" ","").replace("×","")
    vs=tsh(vtext(s1,SANS("500Medium",38),WH+(230,),1.14),8,0.5);paste(b,vs,70+vt.size[0]-10,318)
    paste(b,seal2(series),78+fs/2-52+6,300+vt.size[1]-10);return b
def o4(h,series,title,sub):   # 細框：白色細框包住畫面，logo 嵌在框角
    b=h.copy();b.alpha_composite(TOPS);b.alpha_composite(SB);d=ImageDraw.Draw(b);m=38;col=WH+(235,)
    lg=wlogo(132);paste(b,lg,m-4,m-10)
    x_after=m+lg.size[0]-12;y_after=m+lg.size[1]-18
    d.line([(x_after,m),(OW-m,m)],fill=col,width=3);d.line([(OW-m,m),(OW-m,OH-m)],fill=col,width=3);d.line([(OW-m,OH-m),(m,OH-m)],fill=col,width=3);d.line([(m,OH-m),(m,y_after)],fill=col,width=3)
    c=SERIES[series]["col"];lab=T(SERIES[series]["name"],SANS("700Bold",36),track=10);w=lab.size[0]+2*(60+20);lb=blank(w,lab.size[1]);ld=ImageDraw.Draw(lb)
    ld.rectangle((0,lb.size[1]/2-2,60,lb.size[1]/2+2),fill=c+(255,));ld.rectangle((w-60,lb.size[1]/2-2,w,lb.size[1]/2+2),fill=c+(255,));lb.alpha_composite(lab,(80,0))
    put(b,tsh(lb,6,0.45),540,1160)
    put(b,tsh(T(title,fit(title,SER,128,900,6),track=6),12,0.6),540,1290)
    put(b,tsh(T(sub,SANS("500Medium",38),WH,track=3,al=235),6,0.45),540,1420);return b
def o5(h,series,title,sub):   # 粗黑大字：置中大字＋系列色粗底線
    c=SERIES[series]["col"];b=h.copy();b.alpha_composite(TOPS);b.alpha_composite(scrim(700,1920,0.72,curve=1.1));paste(b,LOGO_W,34,30)
    ic=icon(SERIES[series]["icon"],46,c+(255,));lab=T(SERIES[series]["name"],SANS("900Black",42),track=4);w=ic.size[0]+14+lab.size[0];lb=blank(w,max(ic.size[1],lab.size[1]))
    lb.alpha_composite(ic,(0,(lb.size[1]-ic.size[1])//2));lb.alpha_composite(lab,(ic.size[0]+10,(lb.size[1]-lab.size[1])//2))
    tt=T(title,fit(title,SANSB,156,980,0));put(b,tsh(lb,6,0.5),540,1110)
    d=ImageDraw.Draw(b);uw=min(tt.size[0]-30,760);d.rounded_rectangle((540-uw/2,1312,540+uw/2,1330),radius=9,fill=c+(255,))
    put(b,tsh(tt,14,0.65),540,1225)
    put(b,tsh(T(sub,SANS("700Bold",40),WH,track=2,al=240),6,0.5),540,1400);return b
def brush(w,col,seed=1,th=16):
    k=3;im=blank((w+40)*k,(th*3)*k);d=ImageDraw.Draw(im);r=random.Random(seed);pts=[]
    for i in range(30):x=20*k+i*(w*k)/29;y=(th*1.5+math.sin(i/29*math.pi*1.2)*-5+r.uniform(-1.5,1.5))*k;pts.append((x,y))
    d.line(pts,fill=col+(255,),width=th*k,joint="curve");d.ellipse((pts[0][0]-th*k/2,pts[0][1]-th*k/2,pts[0][0]+th*k/2,pts[0][1]+th*k/2),fill=col+(255,))
    return im.resize((im.size[0]//k,im.size[1]//k),Image.LANCZOS)
def o6(h,series,title,sub):   # 手寫溫度：手寫大標＋系列色筆刷線
    c=SERIES[series]["col"];b=h.copy();b.alpha_composite(TOPS);b.alpha_composite(SB);paste(b,LOGO_W,34,30)
    lab=T("#"+SERIES[series]["name"],KAI("700Bold",50),track=2);put(b,tsh(lab,6,0.5),90+lab.size[0]/2,1085,1,1,4)
    tt=T(title,fit(title,lambda s:KAI("700Bold",s),150,940,0));br=brush(min(tt.size[0]-20,820),c,len(title))
    put(b,br,72+br.size[0]/2,1300,1,1,3);put(b,tsh(tt,12,0.6),60+tt.size[0]/2,1215,1,1,3)
    put(b,tsh(T(sub,KAI("400Regular",46),WH,track=2,al=240),6,0.5),74+T(sub,KAI("400Regular",46)).size[0]/2,1405,1,1,3);return b
OPTS=[("1 海報宋體","底部漸層＋白色粗宋大標，像電影海報",o1),("2 系列色光","畫面下方染上系列色，一看顏色就知道是哪個系列",o2),
      ("3 直排題字","左側直排宋體大標，加系列印章，東方質感",o3),("4 白色細框","整個畫面一圈細框，logo 嵌在框角",o4),
      ("5 粗黑大字","置中粗黑大字＋系列色粗底線，最醒目",o5),("6 手寫溫度","手寫字大標＋筆刷底線，親切像姐夫在介紹",o6)]
