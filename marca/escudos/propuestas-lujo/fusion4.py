exec(open('fusion3.py').read().split("for mode,k,nm in")[0])
import math
EXTRA += '''
<linearGradient id="fadeSoft" gradientUnits="userSpaceOnUse" x1="0" y1="480" x2="0" y2="780">
 <stop offset="0" stop-color="#0b0b0b"/><stop offset=".18" stop-color="#0b0b0b" stop-opacity=".9"/>
 <stop offset=".42" stop-color="#140e00" stop-opacity=".58"/><stop offset=".68" stop-color="#2a1d00" stop-opacity=".24"/>
 <stop offset=".88" stop-color="#2a1d00" stop-opacity=".06"/><stop offset="1" stop-color="#2a1d00" stop-opacity="0"/></linearGradient>
<radialGradient id="spot" gradientUnits="userSpaceOnUse" cx="600" cy="680" r="330"><stop offset="0" stop-color="#fff6c2" stop-opacity=".55"/><stop offset=".5" stop-color="#fff0a0" stop-opacity=".18"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
'''
def common(b, k):
    base(b, k)
    b.append(f'<g clip-path="url(#k{k})"><rect width="1200" height="800" fill="url(#fadeSoft)"/></g>')
def lower2(b):
    b.append(txt('ENTRENADOR PERSONAL',600,958,62,'#0b0b0b',1.5,fam='Anton',weight=400,extra='filter="url(#sink)"'))
    b.append(txt('ORIHUELA',600,1018,33,'#0b0b0b',12,fam='Montserrat',weight=800,extra='filter="url(#sink)"'))

# ---- V1: los tres cambios ----
b=[]; common(b,'V1')
m,h=art('name','url(#goldV)',600,372,560,'bevelS'); b.append(m)
b.append(txt('DESDE 2021',600,510,19,'url(#goldV)',9,fam='Montserrat',weight=600))
m,h=art('fig','#0b0b0b',600,530,380,'sink'); b.append(m)
m,h=art('one','#0b0b0b',600,792,150,'sink'); b.append(m)
lower2(b); finish(b,'10a-escudo-final')

# ---- V2: premium ----
b=[]; common(b,'V2')
# guilloché grabado en el amarillo (líneas onduladas muy finas)
g=[]
for i in range(46):
    y0=560+i*14; pts=[]
    for x in range(100,1101,10):
        y=y0+7*math.sin(x/38+i*.55)+4*math.sin(x/17-i*.3); pts.append(f'{x},{y:.1f}')
    g.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#7a5200" stroke-width="1.1" opacity=".13"/>')
b.append(f'<g clip-path="url(#kV2)">{"".join(g)}</g>')
# foco de luz detrás de las figuras
b.append('<g clip-path="url(#kV2)"><rect width="1200" height="1400" fill="url(#spot)"/></g>')
# filete dorado interior
b.append(sc(P,.885,extra='fill="none" stroke="url(#gold)" stroke-width="2.4" opacity=".95"'))
m,h=art('name','url(#goldV)',600,372,560,'bevelS'); b.append(m)
# DESDE 2021 con rombos y filetes
b.append('<g fill="url(#goldV)">'
         '<rect x="330" y="503" width="62" height="1.6"/><rect x="808" y="503" width="62" height="1.6"/>'
         '<path d="M398,504 l7,-7 l7,7 l-7,7 z"/><path d="M788,504 l7,-7 l7,7 l-7,7 z"/></g>')
b.append(txt('DESDE 2021',600,511,19,'url(#goldV)',9,fam='Montserrat',weight=600))
m,h=art('fig','#0b0b0b',600,530,380,'sink'); b.append(m)
m,h=art('one','#0b0b0b',600,792,150,'sink'); b.append(m)
lower2(b)
# tres puntos dorados bajo ORIHUELA (remate)
b.append('<g fill="url(#gold)" filter="url(#bevelS)"><circle cx="574" cy="1056" r="4.2"/><circle cx="600" cy="1056" r="5.6"/><circle cx="626" cy="1056" r="4.2"/></g>')
finish(b,'10b-escudo-premium')
print('ok')
