from PIL import Image,ImageDraw,ImageFont,ImageFilter
import math
FD="__ROOT__/fonts/"
def F(n,s):return ImageFont.truetype(FD+{"k":"ChironGoRoundTC_900Black.ttf","b":"ChironGoRoundTC_800ExtraBold.ttf","h":"Huninn_400Regular.ttf"}[n],s)
INK=(38,18,8);WHITE=(255,255,255);YEL=(255,214,64);RED=(196,40,28);CREAM=(255,247,232)
OW,OH=1080,1920
def parse(t):
    out=[];h=False;i=0
    while i<len(t):
        if t.startswith("[[",i):h=True;i+=2;continue
        if t.startswith("]]",i):h=False;i+=2;continue
        out.append((t[i],h));i+=1
    return out
def textrun(segs,font,fills,stroke,sc,shadow=True,outer=None,pad=60):
    """segs: list of (char,hl); returns RGBA image of a single line"""
    w=int(sum(font.getlength(c) for c,_ in segs))+pad*2;h=int(font.size*1.5)+pad
    im=Image.new("RGBA",(w,h),(0,0,0,0));y=pad//2+int(font.size*0.1)
    def draw(layer_fn):
        x=pad
        for c,hl in segs:layer_fn(x,c,hl);x+=font.getlength(c)
    if shadow:
        sh=Image.new("L",(w,h),0);g=ImageDraw.Draw(sh)
        draw(lambda x,c,hl:g.text((x,y+7),c,font=font,fill=170,stroke_width=stroke+(outer[1] if outer else 0)))
        s=Image.new("RGBA",(w,h),(15,5,0,0));s.putalpha(sh.filter(ImageFilter.GaussianBlur(7)));im=Image.alpha_composite(im,s)
    d=ImageDraw.Draw(im)
    if outer:draw(lambda x,c,hl:d.text((x,y),c,font=font,fill=outer[0],stroke_width=stroke+outer[1],stroke_fill=outer[0]))
    draw(lambda x,c,hl:d.text((x,y),c,font=font,fill=fills[1] if hl else fills[0],stroke_width=stroke,stroke_fill=sc))
    return im
def wrap(ch,font,maxw=940):
    tot=sum(font.getlength(c) for c,_ in ch)
    if tot<=maxw:return [ch]
    best=None
    for k in range(2,len(ch)-1):
        a=sum(font.getlength(c) for c,_ in ch[:k]);p=ch[k-1][0]
        if ch[k][0] in "，。！？、～…":continue
        s=abs(a-(tot-a))-(2000 if p in "，、" else 0)
        if best is None or s<best[0]:best=(s,k)
    return [ch[:best[1]],ch[best[1]:]]
CAPF=F("k",74)
def caption(text):
    lines=wrap(parse(text),CAPF);ims=[textrun(l,CAPF,(WHITE,YEL),9,INK) for l in lines]
    W=max(i.size[0] for i in ims);lh=96;H=ims[0].size[1]+lh*(len(ims)-1)
    out=Image.new("RGBA",(W,H),(0,0,0,0))
    for k,i in enumerate(ims):out.alpha_composite(i,((W-i.size[0])//2,k*lh))
    return out
CAP_Y=1290
def hook(text,size=170,rot=-5):
    im=textrun(parse(text),F("k",size),(YEL,YEL),14,INK,outer=(WHITE,12),pad=80)
    return im.rotate(rot,resample=Image.BICUBIC,expand=True)
def punch(text,size=150,col=YEL,rot=-6):
    return textrun(parse(text),F("k",size),(col,col),12,INK,outer=(WHITE,10),pad=70).rotate(rot,resample=Image.BICUBIC,expand=True)
def label(text,icon=None,size=54,bg=CREAM,fg=INK,accent=RED):
    f=F("k",size);tw=f.getlength(text);ih=int(size*1.75);iw=ih if icon else 0
    w=int(tw+64+iw);im=Image.new("RGBA",(w+40,ih+44),(0,0,0,0))
    sh=Image.new("RGBA",im.size,(0,0,0,0));ImageDraw.Draw(sh).rounded_rectangle((20,28,w+20,ih+28),radius=26,fill=(20,8,0,120));im=Image.alpha_composite(im,sh.filter(ImageFilter.GaussianBlur(9)))
    d=ImageDraw.Draw(im);d.rounded_rectangle((20,20,w+20,ih+20),radius=26,fill=bg+(255,))
    if icon:
        d.rounded_rectangle((20,20,20+iw,ih+20),radius=26,fill=accent+(255,));d.rectangle((20+iw-26,20,20+iw,ih+20),fill=accent+(255,))
        d.text((20+iw/2,20+ih/2),icon,font=F("k",int(size*1.05)),fill=WHITE,anchor="mm")
    d.text((20+iw+32+tw/2,20+ih/2+2),text,font=f,fill=fg,anchor="mm");return im
def chapter(num,title,sub):
    f1=F("k",84);f2=F("h",44);w=int(max(f1.getlength(title)+190,f2.getlength(sub)+60))+80;h=250
    im=Image.new("RGBA",(w+40,h+40),(0,0,0,0));d=ImageDraw.Draw(im)
    sh=Image.new("RGBA",im.size,(0,0,0,0));ImageDraw.Draw(sh).polygon([(26,30),(w+26,30),(w-14,170),(26,170)],fill=(20,8,0,120));im=Image.alpha_composite(im,sh.filter(ImageFilter.GaussianBlur(9)));d=ImageDraw.Draw(im)
    d.polygon([(20,20),(w+20,20),(w-20,160),(20,160)],fill=RED+(255,))
    d.ellipse((44,38,148,142),fill=YEL+(255,));d.text((96,90),num,font=F("k",72),fill=INK,anchor="mm")
    d.text((176,90),title,font=f1,fill=WHITE,anchor="lm")
    d.rounded_rectangle((20,172,int(f2.getlength(sub))+80,236),radius=14,fill=CREAM+(255,));d.text((50,204),sub,font=f2,fill=INK,anchor="lm");return im
def place(bg,im,cx,cy):bg.alpha_composite(im,(int(cx-im.size[0]/2),int(cy-im.size[1]/2)))
