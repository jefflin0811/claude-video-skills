import numpy as np
SR=48000
rng=np.random.default_rng(5)
def env(n,a,d):
    t=np.arange(n)/SR;e=np.minimum(1,t/a)*np.exp(-t/d);return e
def whoosh(dur=0.45,up=True):
    n=int(dur*SR);x=rng.standard_normal(n)
    # sweep band via moving average of varying length -> simple: filter by FFT mask that moves
    t=np.arange(n)/n;out=np.zeros(n);seg=1024
    for i in range(0,n,seg):
        c=x[i:i+seg];f=np.fft.rfft(c,seg);fr=np.fft.rfftfreq(seg,1/SR)
        u=t[min(i,n-1)];fc=(400+3600*u) if up else (4000-3600*u)
        f*=np.exp(-((fr-fc)/(fc*0.6))**2);out[i:i+seg]=np.fft.irfft(f,seg)[:len(c)]
    e=np.sin(np.pi*t)**1.5;y=out*e;return y/np.max(np.abs(y))*0.5
def pop(f=900):
    n=int(0.12*SR);t=np.arange(n)/SR
    fr=f*np.exp(-t*18);ph=2*np.pi*np.cumsum(fr)/SR
    return np.sin(ph)*env(n,0.002,0.03)*0.55
def chime(base=1568):
    n=int(1.1*SR);t=np.arange(n)/SR;y=np.zeros(n)
    for k,(m,a) in enumerate([(1,1),(2.01,.45),(3.02,.25),(4.2,.12)]):
        y+=a*np.sin(2*np.pi*base*m*t)
    y2=np.zeros(n);d=int(0.09*SR)
    for k,b in enumerate([1,1.26,1.5]):
        s=np.sin(2*np.pi*base*b*t)*env(n,0.002,0.25)
        y2[k*d:]+=s[:n-k*d]*0.6
    return (y*env(n,0.002,0.35)*0.25+y2*0.3)
def ding(): 
    n=int(0.8*SR);t=np.arange(n)/SR
    return (np.sin(2*np.pi*1318*t)+0.4*np.sin(2*np.pi*2637*t))*env(n,0.002,0.18)*0.45
def boom():
    n=int(1.2*SR);t=np.arange(n)/SR
    fr=110*np.exp(-t*3)+40;ph=2*np.pi*np.cumsum(fr)/SR
    lo=np.sin(ph)*env(n,0.003,0.35)*0.9
    hi=rng.standard_normal(n)*env(n,0.001,0.06)*0.25
    c=chime(2093);c=np.pad(c,(0,max(0,n-len(c))))[:n]
    return lo+hi+c*0.5
def build(events,total):
    buf=np.zeros(int(total*SR)+SR*2)
    for t,snd,g in events:
        i=int(t*SR)
        if i<0: continue
        buf[i:i+len(snd)]+=snd[:len(buf)-i]*g
    return buf[:int(total*SR)]
