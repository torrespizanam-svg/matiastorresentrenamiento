exec(open('fusion2.py').read().split("# A · Degradado suave")[0])
P = open(D+'shape_orig.txt').read()
EXTRA += '''
<filter id="smoke2" x="-10%" y="-10%" width="120%" height="130%"><feTurbulence type="fractalNoise" baseFrequency=".006 .02" numOctaves="5" seed="5" result="t"/><feDisplacementMap in="SourceGraphic" in2="t" scale="80" xChannelSelector="R" yChannelSelector="G" result="d"/><feGaussianBlur in="d" stdDeviation="2.5"/></filter>
<linearGradient id="fadeA3" gradientUnits="userSpaceOnUse" x1="0" y1="470" x2="0" y2="650"><stop offset="0" stop-color="#0b0b0b"/><stop offset=".35" stop-color="#0b0b0b" stop-opacity=".8"/><stop offset=".7" stop-color="#1a1200" stop-opacity=".3"/><stop offset="1" stop-color="#0b0b0b" stop-opacity="0"/></linearGradient>
<linearGradient id="fadeC3" gradientUnits="userSpaceOnUse" x1="0" y1="730" x2="0" y2="840"><stop offset="0" stop-color="#0b0b0b" stop-opacity="0"/><stop offset=".45" stop-color="#1a1200" stop-opacity=".55"/><stop offset="1" stop-color="#0b0b0b"/></linearGradient>
'''
import random
def spray(y0, up=True, seed=21):
    random.seed(seed); o=[]
    for i in range(240):
        x=random.uniform(140,1060); y=random.gauss(y0, 38)
        if (up and y>y0+10) or ((not up) and y<y0-10): continue
        r=random.choice([1.5,2,2.5,3,3.5,4,5,6])
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#0b0b0b" opacity="{random.uniform(.6,1):.2f}"/>')
    return ''.join(o)
def base(b,k):
    frame(b)
    b.append(sc(P,K,extra='fill="url(#yel)"')); b.append(sc(P,K,extra='fill="url(#yelHi)"'))
    b.append(enamel_overlays(P,K,'c'+k))
    b.append(f'<clipPath id="k{k}">{sc(P,K)}</clipPath>')
def top_dark(b, mode, k):
    if mode=='deg':
        b.append(f'<g clip-path="url(#k{k})"><rect width="1200" height="660" fill="url(#fadeA3)"/></g>')
    else:
        b.append(f'<g clip-path="url(#k{k})"><rect x="-100" y="-100" width="1400" height="600" fill="#0b0b0b" filter="url(#smoke)"/>{spray(545,False,21)}</g>')
def bottom_dark(b, mode, k):
    if mode=='deg':
        b.append(f'<g clip-path="url(#k{k})"><rect y="730" width="1200" height="111" fill="url(#fadeC3)"/><rect y="840" width="1200" height="600" fill="#0b0b0b"/></g>')
    else:
        b.append(f'<g clip-path="url(#k{k})"><rect x="-100" y="805" width="1400" height="700" fill="#0b0b0b" filter="url(#smoke2)"/>{spray(790,True,7)}</g>')
def finish(b, name):
    b.append(sc(P,K,extra='fill="url(#sheen2)"')); out(name,b)

for mode,k,nm in [('deg','A','9a-degradado'),('humo','B','9b-humo')]:
    b=[]; base(b,k); top_dark(b,mode,k)
    m,h=art('name','url(#goldV)',600,372,560,'bevelS'); b.append(m)
    m,h=art('fig','#0b0b0b',600,522,380,'sink'); b.append(m)
    m,h=art('one','#0b0b0b',600,786,150,'sink'); b.append(m)
    b.append(txt('ENTRENADOR PERSONAL',600,952,56,'#0b0b0b',1.5,fam='Anton',weight=400,extra='filter="url(#sink)"'))
    b.append('<rect x="460" y="972" width="280" height="3" fill="#0b0b0b" opacity=".7"/>')
    b.append(txt('ORIHUELA',600,1014,26,'#0b0b0b',14,fam='Montserrat',weight=700,extra='filter="url(#sink)"'))
    finish(b,nm)

for mode,k,nm in [('deg','C','9c-degradado-invertido'),('humo','D','9d-humo-invertido')]:
    b=[]; base(b,k); bottom_dark(b,mode,k)
    m,h=art('name','#0b0b0b',600,372,560,'sink'); b.append(m)
    b.append('<rect x="330" y="492" width="540" height="3" fill="#0b0b0b" opacity=".55"/>')
    m,h=art('fig','#0b0b0b',600,515,380,'sink'); b.append(m)
    m,h=art('one','url(#yel)',600,850,135,'glow'); b.append(m)
    b.append(txt('ENTRENADOR PERSONAL',600,992,52,'url(#yel)',1.5,fam='Anton',weight=400,extra='filter="url(#glow)"'))
    b.append('<rect x="470" y="1008" width="260" height="2" fill="url(#gold)"/>')
    b.append(txt('ORIHUELA',600,1046,24,'url(#goldV)',14,fam='Montserrat',weight=700))
    finish(b,nm)
print('ok')
