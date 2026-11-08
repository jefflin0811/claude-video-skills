# 姐夫開煮 signature opening: series line with a hand-drawn pot doodle + big dish name, sitting at 2/3 of the screen height
import sys,math
sys.path.insert(0,"__ROOT__/brand")
from kit5 import *
def _wavy(x,y0,y1,amp,ph,n=24):
    return [(x+amp*math.sin(ph+i/n*math.pi*2.2),y0+(y1-y0)*i/n) for i in range(n+1)]
def doodle_pot(t=0.0,h=150,line=CRM,acc=LCOP):
    """white line-art pot with a lid and rising steam; t animates the steam (seconds)"""
    k=3;S=200;W=S*k;im=blank(W,W);d=ImageDraw.Draw(im);lw=int(7.5*k)
    def P(x,y):return (x*k,y*k)
    # body (U shape with rounded bottom) + rim
    d.rounded_rectangle((P(40,98)+P(160,178)),radius=34*k,outline=line+(255,),width=lw)
    d.rectangle((P(46,92)+P(154,116)),fill=(0,0,0,0))
    d.line([P(40,104),P(40,130)],fill=line+(255,),width=lw);d.line([P(160,104),P(160,130)],fill=line+(255,),width=lw)
    d.line([P(28,104),P(172,104)],fill=line+(255,),width=lw,joint="curve")
    # handles
    d.arc((P(14,112)+P(44,136)),90,270,fill=line+(255,),width=int(6*k));d.arc((P(156,112)+P(186,136)),270,90,fill=line+(255,),width=int(6*k))
    # lid dome + knob
    d.arc((P(42,72)+P(158,124)),182,358,fill=line+(255,),width=lw)
    d.ellipse((P(91,58)+P(109,76)),fill=acc+(255,),outline=line+(255,),width=int(4.5*k))
    # small heart on the pot body
    hx,hy,hr=100,142,13
    d.ellipse((P(hx-hr,hy-hr*0.9)+P(hx,hy+hr*0.1)),fill=acc+(255,));d.ellipse((P(hx,hy-hr*0.9)+P(hx+hr,hy+hr*0.1)),fill=acc+(255,))
    d.polygon([P(hx-hr*0.98,hy-hr*0.28),P(hx+hr*0.98,hy-hr*0.28),P(hx,hy+hr*1.15)],fill=acc+(255,))
    # steam: three wavy strands drifting up
    for i,x in enumerate((74,100,126)):
        ph=t*5.2+i*1.9;rise=(t*18+i*7)%14
        pts=[P(px,py-rise) for px,py in _wavy(x,54,6,6.5,ph)]
        st=blank(W,W);sd=ImageDraw.Draw(st);sd.line(pts,fill=line+(255,),width=int(7*k),joint="curve")
        g=np.linspace(0,1,W)[:,None];a=np.asarray(st.getchannel("A")).astype(np.float32)
        ramp=np.clip((g*W-14*k)/(46*k),0,1);st.putalpha(Image.fromarray((a*ramp).astype(np.uint8)));im.alpha_composite(st)
    # sparkle
    for j,(cx,cy,rr,ph) in enumerate(((178,40,12,0.0),(22,58,8,2.1),(170,80,6,4.0))):
        r=rr*(0.55+0.45*(0.5+0.5*math.sin(t*6.0+ph)))
        d.polygon([P(cx,cy-r),P(cx+r*.28,cy-r*.28),P(cx+r,cy),P(cx+r*.28,cy+r*.28),P(cx,cy+r),P(cx-r*.28,cy+r*.28),P(cx-r,cy),P(cx-r*.28,cy-r*.28)],fill=acc+(255,))
    im=im.resize((int(S*h/S*1.0),int(S*h/S*1.0)),Image.LANCZOS) if False else im.resize((h,h),Image.LANCZOS)
    # outline shadow so the white lines hold on bright food
    a=im.getchannel("A");sh=Image.new("RGBA",im.size,DEEP+(0,));sh.putalpha(a.filter(ImageFilter.MaxFilter(5)).point(lambda v:min(255,int(v*0.85))))
    out=blank(h+16,h+16);out.alpha_composite(shadow(sh,3,(0,2),0.0) if False else sh,(8,8));out.alpha_composite(im,(8,8));return shadow(out,6,(0,3),0.35,(0,0,0))
def opening(series,dish,t=0.0,layout="A"):
    """returns (image, visible offset) — left-aligned block, visible content starts at (44,44)"""
    l1=vis(tline(series,70,LCOP,9));l2=vis(tline(dish,160,CRM,14,maxw=900))
    if layout=="A":   # [pot] 姐夫開煮 / 無水雞湯
        pot=doodle_pot(t,128);pv=pot.crop(pot.getchannel("A").getbbox())
        r1h=max(pv.size[1],l1.size[1]);r1=blank(pv.size[0]+12+l1.size[0],r1h)
        r1.alpha_composite(pv,(0,(r1h-pv.size[1])//2));r1.alpha_composite(l1,(pv.size[0]+12,(r1h-l1.size[1])//2+6))
        blk=lstack([r1,l2],[0])
    else:             # 姐夫開煮 / 無水雞湯 [pot]
        pot=doodle_pot(t,236);pv=pot.crop(pot.getchannel("A").getbbox())
        r2h=max(pv.size[1],l2.size[1]);r2=blank(l2.size[0]+18+pv.size[0],r2h)
        r2.alpha_composite(l2,(0,(r2h-l2.size[1])//2));r2.alpha_composite(pv,(l2.size[0]+10,(r2h-pv.size[1])//2-26))
        blk=lstack([l1,r2],[8])
    return shadow(blk,10,(0,6),0.45,(0,0,0))
def corner_shade(amax=0.38):
    yy,xx=np.mgrid[0:OH,0:OW];r=np.sqrt((xx/1.0)**2+(yy/1.2)**2);a=np.clip(1-r/430,0,1)**1.6*amax
    im=Image.new("RGBA",(OW,OH),(10,14,12,0));im.putalpha(Image.fromarray((a*255).astype(np.uint8)));return im
def low_shade(y0=980,amax=0.34):
    g=np.clip((np.arange(OH)-y0)/(OH-y0),0,1)**1.2*amax;g=np.minimum(g,amax)
    im=Image.new("RGBA",(OW,OH),(8,14,10,0));im.putalpha(Image.fromarray((np.tile(g[:,None],(1,OW))*255).astype(np.uint8)));return im
