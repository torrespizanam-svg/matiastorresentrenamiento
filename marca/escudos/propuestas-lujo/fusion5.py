exec(open('fusion4.py').read().split("# ---- V1")[0])
import math, random
EXTRA += '''
<filter id="ink2" x="-20%" y="-20%" width="140%" height="140%"><feTurbulence type="fractalNoise" baseFrequency=".008 .02" numOctaves="5" seed="23" result="t"/><feDisplacementMap in="SourceGraphic" in2="t" scale="46" xChannelSelector="R" yChannelSelector="G" result="d"/><feGaussianBlur in="d" stdDeviation="6"/></filter>
<filter id="chip" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency=".11" numOctaves="2" seed="9" result="n"/><feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -30 21" result="holes"/><feComposite in="SourceGraphic" in2="holes" operator="in" result="c"/><feDropShadow in="c" dx="0" dy="2" stdDeviation="1.4" flood-color="#5a3c00" flood-opacity=".6"/></filter>
<linearGradient id="fadeHalf" gradientUnits="userSpaceOnUse" x1="0" y1="690" x2="0" y2="840"><stop offset="0" stop-color="#0b0b0b"/><stop offset=".35" stop-color="#0b0b0b" stop-opacity=".82"/><stop offset=".7" stop-color="#1a1200" stop-opacity=".3"/><stop offset="1" stop-color="#1a1200" stop-opacity="0"/></linearGradient>
<filter id="ink" x="-20%" y="-20%" width="140%" height="140%"><feTurbulence type="fractalNoise" baseFrequency=".0045 .009" numOctaves="4" seed="17" result="t"/><feDisplacementMap in="SourceGraphic" in2="t" scale="210" xChannelSelector="R" yChannelSelector="G" result="d"/><feGaussianBlur in="d" stdDeviation="16"/></filter>
<linearGradient id="rim" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffbe0"/><stop offset=".5" stop-color="#fff3c4" stop-opacity=".2"/><stop offset="1" stop-color="#fffbe0" stop-opacity=".7"/></linearGradient>
<linearGradient id="starHi" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3a3a3d"/><stop offset="1" stop-color="#1c1c1e"/></linearGradient>
'''
def frame2(b):
    # marco perfeccionado: canto negro, bisel dorado con brillo de arista, surco oscuro, filete fino
    b.append(f'<g filter="url(#drop)">{sc(P,1.0,extra="fill=\"#050505\"")}</g>')
    b.append(sc(P,.985,extra='fill="url(#goldDark)"'))
    b.append(sc(P,.975,extra='fill="url(#gold)" filter="url(#bevel)"'))
    b.append(sc(P,.972,extra='fill="none" stroke="url(#rim)" stroke-width="2.2" opacity=".9"'))
    b.append(sc(P,.94,extra='fill="#050505"'))
    b.append(sc(P,.928,extra='fill="url(#goldDark)"'))
    b.append(sc(P,.922,extra='fill="#0b0b0b"'))
def base2(b,k):
    frame2(b)
    b.append(sc(P,K,extra='fill="url(#yel)"')); b.append(sc(P,K,extra='fill="url(#yelHi)"'))
    b.append(enamel_overlays(P,K,'c'+k))
    b.append(f'<clipPath id="k{k}">{sc(P,K)}</clipPath>')
def guill(k):
    g=[]
    for i in range(52):
        y0=480+i*14; pts=[]
        for x in range(100,1101,8):
            y=y0+7*math.sin(x/38+i*.55)+4*math.sin(x/17-i*.3); pts.append(f'{x},{y:.1f}')
        g.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#7a5200" stroke-width="1" opacity=".12"/>')
    return f'<g clip-path="url(#k{k})">{"".join(g)}</g>'
def star(cx,cy,R,fill_dark='#0b0b0b',fill_lite='url(#starHi)',edge='url(#gold)'):
    # estrella tallada: cada punta con dos facetas (luz/sombra) y filo dorado
    r=R*.44; P5=[]
    for i in range(10):
        a=-math.pi/2+i*math.pi/5; rr=R if i%2==0 else r
        P5.append((cx+rr*math.cos(a), cy+rr*math.sin(a)))
    out=[]
    for i in range(0,10,2):
        tip=P5[i]; lv=P5[i-1]; rv=P5[(i+1)%10]
        out.append(f'<path d="M{cx:.1f},{cy:.1f} L{lv[0]:.1f},{lv[1]:.1f} L{tip[0]:.1f},{tip[1]:.1f} Z" fill="{fill_lite}"/>')
        out.append(f'<path d="M{cx:.1f},{cy:.1f} L{tip[0]:.1f},{tip[1]:.1f} L{rv[0]:.1f},{rv[1]:.1f} Z" fill="{fill_dark}"/>')
    poly=' '.join(f'{x:.1f},{y:.1f}' for x,y in P5)
    out.append(f'<polygon points="{poly}" fill="none" stroke="{edge}" stroke-width="{R*.11:.1f}" stroke-linejoin="miter"/>')
    # muesca desgastada en una punta (guiño a tu letra)
    return '<g filter="url(#chip)">'+''.join(out)+'</g>'
def stars(y=1072,R=22,gap=58,**kw):
    return ''.join(star(600+(i-2)*gap,y,R,**kw) for i in range(5))
def desde(b, y=511):
    b.append('<g fill="url(#goldV)"><rect x="330" y="'+str(y-8)+'" width="62" height="1.6"/><rect x="808" y="'+str(y-8)+'" width="62" height="1.6"/>'
             f'<path d="M398,{y-7} l7,-7 l7,7 l-7,7 z"/><path d="M788,{y-7} l7,-7 l7,7 l-7,7 z"/></g>')
    b.append(txt('DESDE 2021',600,y,19,'url(#goldV)',9,fam='Montserrat',weight=600))
def bottom_text(b, col='#0b0b0b', filt='sink'):
    m,h=art('one',col,600,792,150,filt); b.append(m)
    b.append(txt('ENTRENADOR PERSONAL',600,958,62,col,1.5,fam='Anton',weight=400,extra=f'filter="url(#{filt})"'))
    b.append(txt('ORIHUELA',600,1018,33,col,12,fam='Montserrat',weight=800,extra=f'filter="url(#{filt})"'))
    b.append(stars())
def close(b,k,name):
    b.append(sc(P,.9,extra='fill="none" stroke="url(#gold)" stroke-width="2.2" opacity=".9"'))
    b.append(sc(P,K,extra='fill="url(#sheen2)"')); out(name,b)

# 1 · Como está, perfeccionado
b=[]; base2(b,'S1'); b.append(guill('S1'))
b.append('<g clip-path="url(#kS1)"><rect width="1200" height="800" fill="url(#fadeSoft)"/><rect width="1200" height="1400" fill="url(#spot)"/></g>')
m,h=art('name','url(#goldV)',600,372,560,'bevelS'); b.append(m); desde(b)
m,h=art('fig','#0b0b0b',600,530,380,'sink'); b.append(m)
bottom_text(b); close(b,'S1','12a-clasico')

# 2 · Negro hasta la mitad, figuras en oro
b=[]; base2(b,'S2'); b.append(guill('S2'))
b.append('<g clip-path="url(#kS2)"><rect width="1200" height="700" fill="#0b0b0b"/><rect width="1200" height="700" fill="url(#inkHi)" opacity=".7"/><rect y="689" width="1200" height="152" fill="url(#fadeHalf)"/></g>')
m,h=art('name','url(#goldV)',600,372,560,'bevelS'); b.append(m); desde(b)
m,h=art('fig','url(#goldV)',600,530,380,'bevelS'); b.append(m)
bottom_text(b); close(b,'S2','12b-mitad')

# 3 · Negro irregular, como tinta en agua
b=[]; base2(b,'S3'); b.append(guill('S3'))
b.append('<g clip-path="url(#kS3)"><path d="M-100,-100 H1300 V660 C1180,700 1080,640 970,600 C870,556 790,532 700,536 C620,540 560,530 480,546 C380,578 300,640 210,690 C140,730 60,760 -100,760 Z" fill="#0b0b0b" filter="url(#ink2)"/></g>')
b.append('<g clip-path="url(#kS3)"><rect width="1200" height="1400" fill="url(#spot)" opacity=".7"/></g>')
m,h=art('name','url(#goldV)',600,372,560,'bevelS'); b.append(m); desde(b)
m,h=art('fig','#0b0b0b',600,548,350,'sink'); b.append(m)
bottom_text(b); close(b,'S3','12c-tinta')
print('ok')
