# round 5 — brand palette system for the IP proposal doc (姐夫嚴選 deck colours, left-aligned titles, fixed zones)
import sys;sys.path.insert(0,"__ROOT__/brand")
from kit4 import *
GRN=(39,60,50);TER=(160,95,60);CRM=(246,242,233);CARD=(237,230,214);SAGE=(98,103,94);COP=(179,127,88);LCOP=(235,195,155);DEEP=(16,27,21)
SER5={"探店":("#姐夫探店",GRN,CRM),"開箱":("#姐夫開箱",CRM,GRN),"團購":("#姐夫團購",TER,CRM)}
T5="/mnt/user-data/uploads/Downloads/公司牛肉爐_素材總覽/trim/"
# logo (white line version) placement: visible left edge defines the shared left margin
_lb=LOGO_W.getchannel("A").getbbox();LOGO_XY=(34,30);X0=LOGO_XY[0]+_lb[0]
ICON=LOGO.crop((0,0,LOGO.size[0],570));ICON=ICON.crop(ICON.getchannel("A").getbbox())
def icon_h(h,col):
    im=ICON.resize((int(ICON.size[0]*h/ICON.size[1]),h),Image.LANCZOS);c=Image.new("RGBA",im.size,col+(255,));c.putalpha(im.getchannel("A"));return c
def ss_round(w,h,r,fill,k=3,outline=None,width=0):
    im=blank(w*k,h*k);d=ImageDraw.Draw(im);d.rounded_rectangle((0,0,w*k-1,h*k-1),radius=r*k,fill=fill,outline=outline,width=width*k);return im.resize((w,h),Image.LANCZOS)
def pill5(series,size=42,outline=False):
    tx,bg,fg=SER5[series];k=3;f=SANS("900Black",size*k);tw=f.getlength(tx);h=int(size*1.62);w=int(tw/k+size*1.15)
    im=blank(w*k,h*k);d=ImageDraw.Draw(im);d.rounded_rectangle((0,0,w*k-1,h*k-1),radius=h*k//2,fill=bg+(255,),outline=(GRN+(255,)) if (outline and bg==CRM) else None,width=3*k if (outline and bg==CRM) else 0)
    d.text((w*k/2,h*k/2+k),tx,font=f,fill=fg+(255,),anchor="mm");return im.resize((w,h),Image.LANCZOS)
def tline(text,size,col,sw,maxw=860):
    f=fitf(text,SANSB,size,maxw,sw);return stroked(text,f,col,DEEP,sw,sh=False)
def vis(im):return im.crop(im.getchannel("A").getbbox())
def lstack(items,gaps,pad=24):
    """left-align visible content of items, stack with gaps (between visible boxes); visible content starts at (pad,pad)"""
    vs=[vis(i) for i in items];W=max(v.size[0] for v in vs)+2*pad;H=sum(v.size[1] for v in vs)+sum(gaps)+2*pad
    out=blank(W,H);y=pad
    for v,g in zip(vs,[0]+list(gaps)):y+=g;out.alpha_composite(v,(pad,y));y+=v.size[1]
    return out
def title5(series,l1,l2,s1=112,s2=96):
    blk=lstack([pill5(series),tline(l1,s1,CRM,12),tline(l2,s2,LCOP,11)],[22,4]);return shadow(blk,10,(0,6),0.5,(0,0,0))
def shade5(anchor,amax=0.55):
    if anchor=="top":g=np.clip(1-np.arange(OH)/820,0,1)**1.35*amax
    else:g=np.clip((np.arange(OH)-960)/960,0,1)**1.1*(amax+0.08)
    im=Image.new("RGBA",(OW,OH),(8,16,12,0));im.putalpha(Image.fromarray((np.tile(g[:,None],(1,OW))*255).astype(np.uint8)));return im
TOPZ=(270,600);BOTZ=(1150,1480)
def cover5(hero,series,l1,l2,anchor,ytop=None,s1=112,s2=96):
    b=hero.convert("RGBA").copy();b.alpha_composite(TOPS);b.alpha_composite(shade5(anchor));paste(b,LOGO_W,*LOGO_XY)
    blk=title5(series,l1,l2,s1,s2);m=24+20;vh=blk.size[1]-2*m
    if ytop is None:ytop=300 if anchor=="top" else BOTZ[1]-vh
    paste(b,blk,X0-m,ytop-m);return b
def frame_at(path,t):
    return herofrom(path,t)
# ---------------- signature-device frames ----------------
def sub5(text,size=58,col=(255,255,255)):
    return stroked(text,SANS("900Black",size),col,DEEP,8,sh=True)
def price_card(w=840):
    k=1;rows=[("市價","○○○ 元","strike"),("團購價","○○○ 元","big"),("一人份","約 ○○ 元","norm")]
    h=560;card=ss_round(w,h,36,CRM+(246,));d=ImageDraw.Draw(card)
    tab=ss_round(260,74,37,TER+(255,));ImageDraw.Draw(tab).text((130,38),"算給你看",font=SANS("900Black",40),fill=CRM+(255,),anchor="mm")
    y=150
    for lab,val,kind in rows:
        d.text((56,y),lab,font=SANS("700Bold",46),fill=(SAGE if kind!="big" else GRN)+(255,),anchor="lm")
        if kind=="big":f=SANS("900Black",92);col=TER
        elif kind=="strike":f=SANS("900Black",64);col=SAGE
        else:f=SANS("900Black",64);col=GRN
        d.text((w-56,y),val,font=f,fill=col+(255,),anchor="rm")
        if kind=="strike":tw=f.getlength(val);d.line([(w-56-tw-6,y+2),(w-50,y+2)],fill=TER+(255,),width=6)
        if kind!="norm":d.line([(56,y+(70 if kind=="big" else 52)),(w-56,y+(70 if kind=="big" else 52))],fill=CARD+(255,),width=3)
        y+=150 if kind=="big" else 120
    d.text((56,h-58),"滿 ○○○○ 元免運｜截止 ○ 月 ○ 日",font=SANS("700Bold",36),fill=SAGE+(255,),anchor="lm")
    out=blank(w+40,h+60);out.alpha_composite(shadow(card,18,(0,12),0.35),(-16,10));out.alpha_composite(tab,(40,0));return out
def nag_tag():
    w,h=300,84;im=ss_round(w,h,42,TER+(255,));d=ImageDraw.Draw(im);d.text((w/2,h/2+2),"姐夫碎碎念",font=SANS("900Black",42),fill=CRM+(255,),anchor="mm")
    tail=blank(w,h+26);tail.alpha_composite(im,(0,0));td=ImageDraw.Draw(tail);td.polygon([(54,h-6),(96,h-6),(50,h+24)],fill=TER+(255,));return shadow(tail,8,(0,5),0.4)
def check_badge(d=78,col=GRN,fg=CRM,ring=None):
    k=3;D=d*k;im=blank(D,D);dr=ImageDraw.Draw(im);dr.ellipse((0,0,D-1,D-1),fill=col+(255,),outline=(ring+(255,)) if ring else None,width=int(D*.06) if ring else 0)
    dr.line([(D*.27,D*.52),(D*.44,D*.68),(D*.74,D*.34)],fill=fg+(255,),width=int(D*.1),joint="curve");return im.resize((d,d),Image.LANCZOS)
def num_badge(n,d=78):
    k=3;D=d*k;im=blank(D,D);dr=ImageDraw.Draw(im);dr.ellipse((0,0,D-1,D-1),fill=TER+(255,));dr.text((D/2,D/2+k),f"{n:02d}",font=SANS("900Black",int(D*.42)),fill=CRM+(255,),anchor="mm")
    return im.resize((d,d),Image.LANCZOS)
FIVE=["親身體驗","品質清楚","日常實用","價格實在","值得再選"]
def seal(size=300,rot=-9,seed=3):
    k=2;S=size*k;im=blank(S,S);d=ImageDraw.Draw(im);d.rounded_rectangle((0,0,S-1,S-1),radius=int(S*.06),fill=TER+(255,))
    m=int(S*.055);d.rounded_rectangle((m,m,S-m,S-m),radius=int(S*.04),outline=CRM+(255,),width=int(S*.014))
    ic=icon_h(int(S*.36),CRM);im.alpha_composite(ic,((S-ic.size[0])//2,int(S*.11)))
    f=SERIF("900Black",int(S*.2));d.text((S/2,S*.72),"姐夫拍板",font=f,fill=CRM+(255,),anchor="mm")
    # stamped texture: knock out speckles so it reads as ink, not a sticker
    rng=np.random.default_rng(seed);a=np.asarray(im.getchannel("A")).astype(np.float32)
    n=rng.random((S//6,S//6));n=np.asarray(Image.fromarray((n*255).astype(np.uint8)).resize((S,S),Image.BICUBIC)).astype(np.float32)/255
    a=a*np.clip(0.55+n*0.9,0,1)**0.6;im.putalpha(Image.fromarray(np.clip(a,0,255).astype(np.uint8)))
    im=im.resize((size,size),Image.LANCZOS).rotate(rot,resample=Image.BICUBIC,expand=True);return im
def endcard():
    b=Image.new("RGBA",(OW,OH),CRM+(255,));d=ImageDraw.Draw(b)
    lg=logo_h(430);paste(b,lg,(OW-lg.size[0])/2,250)
    put(b,ttext("我是姐夫 JEFF",SANS("900Black",66),GRN+(255,)),OW/2,820)
    put(b,ttext("自己吃過、用過、會再買的，才推薦給你。",SANS("500Medium",40),SAGE+(255,)),OW/2,892)
    # five passes, two rows of chips
    chips=[]
    for t in FIVE:
        f=SANS("700Bold",38);w=int(f.getlength(t))+96;c=ss_round(w,72,36,CARD+(255,));cd=ImageDraw.Draw(c);ck=check_badge(44,TER)
        c.alpha_composite(ck,(16,14));cd.text((70,37),t,font=f,fill=GRN+(255,),anchor="lm");chips.append(c)
    for row,yy in ((chips[:3],990),(chips[3:],1082)):
        W=sum(c.size[0] for c in row)+20*(len(row)-1);x=(OW-W)/2
        for c in row:paste(b,c,x,yy);x+=c.size[0]+20
    d.line([(OW/2-60,1204),(OW/2+60,1204)],fill=COP+(255,),width=3)
    put(b,ttext("好吃、好用，",SANS("900Black",76),GRN+(255,)),OW/2,1282);put(b,ttext("也值得分享給家人。",SANS("900Black",76),GRN+(255,)),OW/2,1378)
    f=SANS("900Black",42);tx="加入姐夫的 LINE 社群";w=int(f.getlength(tx))+110;p=ss_round(w,88,44,GRN+(255,));ImageDraw.Draw(p).text((w/2,46),tx,font=f,fill=CRM+(255,),anchor="mm")
    put(b,shadow(p,8,(0,5),0.25),OW/2,1470)
    return b
