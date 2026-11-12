import numpy as np, wave, sys
sr=44100; D=32.0; N=int(sr*D); t=np.arange(N)/sr
rng=np.random.default_rng(7)
L=np.zeros(N); R=np.zeros(N)
def add(sig,start,gain=1.0,pan=0.0):
    i=int(start*sr); n=min(len(sig),N-i)
    if n<=0: return
    L[i:i+n]+=sig[:n]*gain*(1-pan)/1.0; R[i:i+n]+=sig[:n]*gain*(1+pan)/1.0
def env(n,a,d):
    e=np.ones(n); na=int(a*sr); e[:na]=np.linspace(0,1,na) if na>0 else 1
    e*=np.exp(-np.arange(n)/(d*sr)); return e
def lp(x,a):  # one-pole lowpass
    y=np.empty_like(x); s=0.0
    for i in range(len(x)): s+=a*(x[i]-s); y[i]=s
    return y
def lpf(x,a): # fast vectorised approx via scipy-free filter
    from numpy.fft import rfft,irfft,rfftfreq
    X=rfft(x); f=rfftfreq(len(x),1/sr); X/= (1+(f/a)**4)**.5; return irfft(X,len(x))
# --- drone / pad: A minor progression, saw stacks low-passed
chords=[(0,[55,110,130.81,164.81]),(8.5,[43.65,87.31,130.81,174.61]),(17,[65.41,130.81,164.81,196.0]),(24.5,[49.0,98.0,146.83,196.0]),(28,[55,110,164.81,220.0,261.63])]
pad=np.zeros(N)
for k,(st,fr) in enumerate(chords):
    en=chords[k+1][0] if k+1<len(chords) else D
    n=int((en-st+1.5)*sr); tt=np.arange(n)/sr; s=np.zeros(n)
    for f in fr:
        for det in (-0.12,0.12):
            ph=2*np.pi*(f+det)*tt+rng.uniform(0,6); s+= (2*((ph/(2*np.pi))%1)-1)*0.5
    e=np.minimum(1,tt/1.2)*np.minimum(1,np.maximum(0,(en-st+1.5-tt)/1.5))
    i=int(st*sr); m=min(n,N-i); pad[i:i+m]+=(s*e)[:m]
pad=lpf(pad,900)*0.045
swell=0.55+0.45*np.clip((t-8.5)/19.5,0,1); swell[t>=28]=1.0
pad*=swell
L+=pad; R+=pad
# sub
sub=np.sin(2*np.pi*55*t)*0.10*np.clip(t/3,0,1)*np.where(t<28,1,np.exp(-(t-28)/3)); L+=sub; R+=sub
# --- kick
def kick(g=1.0):
    n=int(.55*sr); tt=np.arange(n)/sr; f=45+110*np.exp(-tt*28)
    ph=2*np.pi*np.cumsum(f)/sr; return np.sin(ph)*np.exp(-tt*7)*g
def hit():  # cinematic boom
    n=int(3.5*sr); tt=np.arange(n)/sr; f=30+90*np.exp(-tt*6)
    b=np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-tt*1.3)
    nz=lpf(rng.standard_normal(n),1800)*np.exp(-tt*9)*0.5
    return (b+nz)
def tick():
    n=int(.08*sr); tt=np.arange(n)/sr; x=rng.standard_normal(n)
    x=x-lpf(x,6000); return x*np.exp(-tt*60)
def whoosh(dur):
    n=int(dur*sr); tt=np.arange(n)/sr; x=rng.standard_normal(n)
    out=np.zeros(n); seg=int(.05*sr)
    for j in range(0,n,seg):
        fc=200+6000*(j/n)**2; out[j:j+seg]=lpf(x[j:j+seg],fc)
    return out*(tt/dur)**2
beat=.5
for b in np.arange(8.5,28,beat):
    add(kick(0.55 if (b-8.5)%1==0 else 0.35),b)
for b in np.arange(8.75,28,beat):
    add(tick(),b,0.06,pan=0.3)
for c in [3.0,5.5,8.5,13.0,17.0,21.0,24.5]:
    add(hit(),c,0.42)
add(hit(),28.0,0.75)
for k,c in enumerate([13.0,13.6,14.2,14.8,15.4,16.0]):
    add(tick(),c,0.35,pan=(-1)**k*0.4); add(kick(0.4),c)
for k,c in enumerate([18.5,19.3,20.1]): add(tick(),c,0.3)
add(whoosh(2.0),1.0,0.12); add(whoosh(1.5),7.0,0.15); add(whoosh(1.4),15.6,0.14); add(whoosh(3.0),25.0,0.22)
# shimmer bell on reveals
def bell(f,g=1):
    n=int(2.5*sr); tt=np.arange(n)/sr
    return (np.sin(2*np.pi*f*tt)+0.4*np.sin(2*np.pi*f*2.76*tt)*np.exp(-tt*3))*np.exp(-tt*1.6)*g
for c,f in [(3.0,880),(5.5,659.25),(10.6,1046.5),(23.1,880),(28.6,659.25),(29.3,880),(29.6,1318.5)]:
    add(bell(f),c,0.05,pan=0.2)
# --- reverb (stereo convolution)
ir_n=int(2.2*sr); it=np.arange(ir_n)/sr
from numpy.fft import rfft,irfft
def conv(x,ir):
    m=len(x)+len(ir); n2=1<<int(np.ceil(np.log2(m))); return irfft(rfft(x,n2)*rfft(ir,n2),n2)[:len(x)]
irL=rng.standard_normal(ir_n)*np.exp(-it*2.8); irR=rng.standard_normal(ir_n)*np.exp(-it*2.8)
irL=lpf(irL,5000); irR=lpf(irR,5000)
wl=conv(L,irL); wr=conv(R,irR); s=np.max(np.abs(wl))+1e-9
L=L+wl/s*np.max(np.abs(L))*0.35; R=R+wr/s*np.max(np.abs(R))*0.35
# master fade + limiter
fade=np.clip(t/0.3,0,1)*np.clip((D-t)/1.2,0,1)
L*=fade; R*=fade
st=np.stack([L,R],1); st=np.tanh(st/np.max(np.abs(st))*1.6)/np.tanh(1.6)*0.89
w=wave.open(sys.argv[1],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((st*32767).astype('<i2').tobytes()); w.close()
