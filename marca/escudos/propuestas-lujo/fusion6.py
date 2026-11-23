exec(open('fusion5.py').read().split("# 1 · Como está")[0])
EXTRA += '''
<linearGradient id="tipFade" gradientUnits="userSpaceOnUse" x1="0" y1="1020" x2="0" y2="1075"><stop offset="0" stop-color="#0b0b0b" stop-opacity="0"/><stop offset="1" stop-color="#0b0b0b"/></linearGradient>
<linearGradient id="fadeMid" gradientUnits="userSpaceOnUse" x1="0" y1="470" x2="0" y2="870">
 <stop offset="0" stop-color="#0b0b0b"/><stop offset=".22" stop-color="#0b0b0b" stop-opacity=".93"/>
 <stop offset=".42" stop-color="#120c00" stop-opacity=".68"/><stop offset=".6" stop-color="#1e1500" stop-opacity=".38"/>
 <stop offset=".8" stop-color="#2a1d00" stop-opacity=".12"/><stop offset="1" stop-color="#2a1d00" stop-opacity="0"/></linearGradient>
<linearGradient id="figGrad" gradientUnits="userSpaceOnUse" x1="0" y1="540" x2="0" y2="780">
 <stop offset="0" stop-color="#fff0b8"/><stop offset=".3" stop-color="#e8c15c"/><stop offset=".5" stop-color="#a97a1c"/>
 <stop offset=".66" stop-color="#3a2800"/><stop offset=".8" stop-color="#0b0b0b"/><stop offset="1" stop-color="#0b0b0b"/></linearGradient>
<radialGradient id="starGold" cx="35%" cy="30%" r="80%"><stop offset="0" stop-color="#fff3c4"/><stop offset=".5" stop-color="#e0b450"/><stop offset="1" stop-color="#8a6312"/></radialGradient>
'''
def stars_black(y=1098): return stars(y=y,fill_dark='#050505', fill_lite='#141414', edge='url(#gold)')
def stars_gold(y=1098): return stars(y=y,fill_dark='url(#goldDark)', fill_lite='url(#starGold)', edge='#3a2a00')
def tipband(b,k,soft=False):
    if soft:
        b.append(f'<g clip-path="url(#k{k})"><rect y="1020" width="1200" height="400" fill="url(#tipFade)"/></g>')
    else:
        b.append(f'<g clip-path="url(#k{k})"><rect y="1044" width="1200" height="400" fill="url(#ink)"/><rect y="1044" width="1200" height="400" fill="url(#inkHi)" opacity=".5"/><rect y="1040" width="1200" height="5" fill="url(#gold)" filter="url(#bevelS)"/></g>')
def bottom(b, starsfn):
    m,h=art('one','#0b0b0b',600,792,150,'sink'); b.append(m)
    b.append(txt('ENTRENADOR PERSONAL',600,958,62,'#0b0b0b',1.5,fam='Anton',weight=400,extra='filter="url(#sink)"'))
    b.append(txt('ORIHUELA',600,1018,33,'#0b0b0b',12,fam='Montserrat',weight=800,extra='filter="url(#sink)"'))
    b.append(starsfn(y=1098))
def beads(b):
    # cordón de perlas doradas en el surco del marco (perfil distintivo)
    import re
    pts=[tuple(map(float,p.split(','))) for p in re.findall(r'[-\d.]+,[-\d.]+',P)]
    k=.934; P2=[(600+(x-600)*k, 715+(y-715)*k) for x,y in pts]
    # recorrer a distancia constante
    L=[0]
    for i in range(1,len(P2)): L.append(L[-1]+math.dist(P2[i],P2[i-1]))
    step=17; d=0; i=0; out=[]
    while d<L[-1]:
        while L[i+1]<d: i+=1
        t=(d-L[i])/(L[i+1]-L[i]); x=P2[i][0]+(P2[i+1][0]-P2[i][0])*t; y=P2[i][1]+(P2[i+1][1]-P2[i][1])*t
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.3" fill="url(#pearl)"/>'); d+=step
    b.append('<g>'+''.join(out)+'</g>')

# 1 · Clásico (como está) con estrellas negras
b=[]; base2(b,'T1'); b.append(guill('T1'))
b.append('<g clip-path="url(#kT1)"><rect width="1200" height="800" fill="url(#fadeSoft)"/><rect width="1200" height="1400" fill="url(#spot)"/></g>')
m,h=art('name','url(#goldV)',600,372,560,'bevelS'); b.append(m); desde(b)
m,h=art('fig','#0b0b0b',600,530,380,'sink'); b.append(m)
tipband(b,'T1'); bottom(b,stars_gold); close(b,'T1','13a-clasico')

# 2 · Degradado progresivo hasta la mitad de las figuras
b=[]; base2(b,'T2'); b.append(guill('T2'))
b.append('<g clip-path="url(#kT2)"><rect width="1200" height="880" fill="url(#fadeMid)"/></g>')
m,h=art('name','url(#goldV)',600,372,560,'bevelS'); b.append(m); desde(b)
m,h=art('fig','url(#figGrad)',600,530,380,'bevelS'); b.append(m)
tipband(b,'T2'); bottom(b,stars_gold); close(b,'T2','13b-mitad-progresivo')

# 3 · Igual que el 2, con perfil de perlas y estrellas de oro
b=[]; base2(b,'T3'); b.append(guill('T3'))
b.append('<g clip-path="url(#kT3)"><rect width="1200" height="880" fill="url(#fadeMid)"/></g>')
beads(b)
m,h=art('name','url(#goldV)',600,372,560,'bevelS'); b.append(m); desde(b)
m,h=art('fig','url(#figGrad)',600,530,380,'bevelS'); b.append(m)
tipband(b,'T3',soft=True); bottom(b,stars_gold); close(b,'T3','13c-mitad-perlas-oro')
print('ok')
