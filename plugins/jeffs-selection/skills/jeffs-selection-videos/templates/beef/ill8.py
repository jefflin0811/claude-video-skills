# cartoon illustration helpers (PIL), consistent thick-outline style
from style import *
import math,random
def blank(w,h):return Image.new("RGBA",(int(w),int(h)),(0,0,0,0))
def put(base,im,cx,cy,al=1.0,sc=1.0,rot=0.0):
    if al<=0.01:return
    if rot:im=im.rotate(rot,resample=Image.BICUBIC,expand=True)
    if abs(sc-1)>.01:im=im.resize((max(1,int(im.size[0]*sc)),max(1,int(im.size[1]*sc))),Image.BILINEAR)
    if al<0.999:
        a=im.getchannel("A").point(lambda v:int(v*al));im=im.copy();im.putalpha(a)
    x=int(cx-im.size[0]/2);y=int(cy-im.size[1]/2)
    x0,y0=max(0,x),max(0,y);x1,y1=min(base.size[0],x+im.size[0]),min(base.size[1],y+im.size[1])
    if x1<=x0 or y1<=y0:return
    base.alpha_composite(im.crop((x0-x,y0-y,x1-x,y1-y)),(x0,y0))
def sparkle(r,col=YEL):
    s=int(r*2.6);im=blank(s,s);d=ImageDraw.Draw(im);c=s/2
    pts=[]
    for k in range(8):
        a=k*math.pi/4-math.pi/2;rr=r if k%2==0 else r*0.32;pts.append((c+rr*math.cos(a),c+rr*math.sin(a)))
    d.polygon(pts,fill=col+(255,),outline=INK+(255,),width=max(3,int(r*0.12)));return im
SPK={k:sparkle(k) for k in (22,30,40,52)}
SPKW={k:sparkle(k,WHITE) for k in (22,30,40)}
def steam_layer(base,t,cx,cy,w=260,h=320,n=3,al=1.0,seed=0):
    d=ImageDraw.Draw(base)
    for k in range(n):
        ph=(t*0.55+k/n+seed*0.13)%1.0;x0=cx+(k-(n-1)/2)*w/n
        a=math.sin(math.pi*ph)*al
        if a<0.05:continue
        y_base=cy-ph*h*0.5;L=h*0.55;pts=[]
        for j in range(18):
            u=j/17;yy=y_base-u*L;xx=x0+math.sin(u*5.2+t*3+k*2)*22*(0.4+u)
            pts.append((xx,yy))
        A=int(235*a)
        d.line(pts,fill=INK+(int(A*0.55),),width=26,joint="curve")
        d.line(pts,fill=(255,255,255,A),width=16,joint="curve")
def beef(sz=90,seed=1):
    r=random.Random(seed);im=blank(sz*1.3,sz*1.3);d=ImageDraw.Draw(im);c=sz*0.65;pts=[]
    for k in range(9):
        a=k/9*2*math.pi;rr=sz*0.5*r.uniform(0.75,1.0);pts.append((c+rr*math.cos(a)*1.15,c+rr*math.sin(a)*0.85))
    d.polygon(pts,fill=(140,72,40,255),outline=INK+(255,),width=6)
    d.line([(c-sz*0.35,c-sz*0.05),(c-sz*0.05,c-sz*0.2),(c+sz*0.3,c-sz*0.1)],fill=(245,214,170,255),width=int(sz*0.12),joint="curve")
    d.ellipse((c+sz*0.1,c+sz*0.08,c+sz*0.28,c+sz*0.22),fill=(196,120,80,255))
    return im
BEEF=[beef(90,i) for i in range(4)]
def scallion(sz=34):
    im=blank(sz+8,sz+8);d=ImageDraw.Draw(im);d.ellipse((4,4,sz+4,sz+4),fill=(92,170,60,255),outline=INK+(255,),width=4);d.ellipse((4+sz*0.3,4+sz*0.3,4+sz*0.7,4+sz*0.7),fill=(206,236,170,255));return im
SCAL=[scallion(s) for s in (28,34,40)]
def clock(n,ring=0.0):
    S=300;im=blank(S,S);d=ImageDraw.Draw(im);c=S/2+10
    for sx in (-1,1):
        bx=c+sx*78;by=72;d.ellipse((bx-34,by-34,bx+34,by+34),fill=YEL+(255,),outline=INK+(255,),width=7)
        d.line([(c+sx*70,c+88),(c+sx*96,c+116)],fill=INK+(255,),width=12)
    d.ellipse((c-112,c-112,c+112,c+112),fill=RED+(255,),outline=INK+(255,),width=8)
    d.ellipse((c-86,c-86,c+86,c+86),fill=CREAM+(255,),outline=INK+(255,),width=5)
    d.text((c,c-6),str(n),font=F("k",92),fill=INK+(255,),anchor="mm");d.text((c,c+52),"秒",font=F("k",30),fill=INK+(255,),anchor="mm")
    return im
def burst(text="叮！",col=YEL):
    S=360;im=blank(S,S);d=ImageDraw.Draw(im);c=S/2;pts=[]
    for k in range(24):
        a=k/24*2*math.pi;rr=160 if k%2==0 else 110;pts.append((c+rr*math.cos(a),c+rr*math.sin(a)))
    d.polygon(pts,fill=col+(255,),outline=INK+(255,),width=8);d.text((c,c),text,font=F("k",96),fill=INK+(255,),anchor="mm");return im
def note(col,sz=90,dbl=False):
    im=blank(sz*1.2,sz*1.4);d=ImageDraw.Draw(im);hx,hy=sz*0.35,sz*1.05
    d.ellipse((hx-sz*0.26,hy-sz*0.19,hx+sz*0.26,hy+sz*0.19),fill=col+(255,),outline=INK+(255,),width=5)
    d.line([(hx+sz*0.22,hy-sz*0.05),(hx+sz*0.22,sz*0.15)],fill=INK+(255,),width=9)
    d.line([(hx+sz*0.22,sz*0.15),(hx+sz*0.62,sz*0.38)],fill=INK+(255,),width=12);return im
NOTES=[note((255,120,90)),note((90,180,255)),note(YEL)]
def heart(sz=70,col=(235,70,80)):
    im=blank(sz*1.3,sz*1.3);d=ImageDraw.Draw(im);c=sz*0.65;pts=[]
    for k in range(60):
        t=k/60*2*math.pi;x=16*math.sin(t)**3;y=-(13*math.cos(t)-5*math.cos(2*t)-2*math.cos(3*t)-math.cos(4*t))
        pts.append((c+x*sz/36,c+y*sz/36))
    d.polygon(pts,fill=col+(255,),outline=INK+(255,),width=6);d.ellipse((c-sz*0.3,c-sz*0.28,c-sz*0.14,c-sz*0.14),fill=(255,200,200,255));return im
HEART=heart()
def chopsticks():
    im=blank(260,260);d=ImageDraw.Draw(im)
    for dx in (0,34):
        d.line([(40+dx,230),(200+dx,30)],fill=INK+(255,),width=22);d.line([(40+dx,230),(200+dx,30)],fill=(232,190,120,255),width=12)
    return im
CHOP=chopsticks()
def sweat(sz=70):
    im=blank(sz,sz*1.4);d=ImageDraw.Draw(im);c=sz/2
    d.polygon([(c,6),(c+sz*0.4,sz*0.8),(c-sz*0.4,sz*0.8)],fill=(120,190,255,255));d.ellipse((c-sz*0.4,sz*0.45,c+sz*0.4,sz*1.25),fill=(120,190,255,255),outline=INK+(255,),width=5)
    d.line([(c,8),(c+sz*0.4,sz*0.8)],fill=INK+(255,),width=5);d.line([(c,8),(c-sz*0.4,sz*0.8)],fill=INK+(255,),width=5);d.ellipse((c-sz*0.15,sz*0.75,c-sz*0.02,sz*0.95),fill=WHITE);return im
SWEAT=sweat()
def emph(base,cx,cy,r,ang0,al=1,n=3):
    d=ImageDraw.Draw(base)
    for k in range(n):
        a=math.radians(ang0+(k-(n-1)/2)*24);x0=cx+r*math.cos(a);y0=cy+r*math.sin(a);x1=cx+(r+60)*math.cos(a);y1=cy+(r+60)*math.sin(a)
        d.line([(x0,y0),(x1,y1)],fill=INK+(int(255*al),),width=16);d.line([(x0,y0),(x1,y1)],fill=YEL+(int(255*al),),width=8)
def motion(base,cx,cy,w,al=1):
    d=ImageDraw.Draw(base)
    for k,dy in enumerate((-40,0,40)):
        d.line([(cx-w-20*k,cy+dy),(cx-w+90-20*k,cy+dy)],fill=WHITE+(int(230*al),),width=10)
# caption with bigger highlight words
CF=F("k",74);CFH=F("k",98)
def caption(text):
    ch=parse(text)
    def W(seg):return sum((CFH if h else CF).getlength(c) for c,h in seg)
    lines=[ch]
    if W(ch)>960:
        best=None
        for k in range(2,len(ch)-1):
            if ch[k][0] in "，。！？、～…":continue
            a=W(ch[:k]);s=abs(a-(W(ch)-a))-(2000 if ch[k-1][0] in "，、" else 0)
            if best is None or s<best[0]:best=(s,k)
        lines=[ch[:best[1]],ch[best[1]:]]
    lh=118;H=40+lh*len(lines)+30;Wd=int(max(W(l) for l in lines))+80
    im=blank(Wd,H);G=Image.new("L",(Wd,H),0);d=ImageDraw.Draw(im);g=ImageDraw.Draw(G)
    for li,l in enumerate(lines):
        x=(Wd-W(l))/2;by=40+lh*(li+1)-22
        for c,h in l:
            f=CFH if h else CF;col=YEL if h else WHITE
            g.text((x,by+7),c,font=f,fill=170,stroke_width=10,anchor="ls")
            d.text((x,by),c,font=f,fill=col+(255,),stroke_width=10 if h else 9,stroke_fill=INK+(255,),anchor="ls");x+=f.getlength(c)
    s=Image.new("RGBA",(Wd,H),(15,5,0,0));s.putalpha(G.filter(ImageFilter.GaussianBlur(7)));return Image.alpha_composite(s,im)
