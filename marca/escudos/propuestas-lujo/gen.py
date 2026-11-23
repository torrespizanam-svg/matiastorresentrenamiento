import math
D = '/home/claude/matiastorresentrenamiento/marca/escudos/propuestas-lujo/'  # copiar aquí name/fig/1a1 _mask.png de la carpeta superior
RAT = {'name': 1600/293, 'fig': 1159/746, 'one': 840/532, 'ep': 4395/409, 'entr': 2392/409, 'pers': 1911/400}
FILE = {'name': 'name_mask.png', 'fig': 'fig_mask.png', 'one': '1a1_mask.png', 'ep': 'ep_mask.png', 'entr': 'entr_mask.png', 'pers': 'pers_mask.png'}
CX, CY = 600, 715
_n = [0]

def art(kind, fill, cx, y, w, filt='', clip=''):
    """Pieza real de la marca (máscara) centrada en cx, con relleno y filtro."""
    _n[0] += 1
    mid = f'm{_n[0]}'
    h = w / RAT[kind]; x = cx - w/2
    m = (f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}">'
         f'<image href="{D}{FILE[kind]}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" preserveAspectRatio="none"/></mask>')
    f = f' filter="url(#{filt})"' if filt else ''
    c = f' clip-path="url(#{clip})"' if clip else ''
    return m + f'<g{f}{c}><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" mask="url(#{mid})"/></g>', h

def sc(path, k, cx=CX, cy=CY, extra=''):
    return f'<path d="{path}" transform="translate({cx} {cy}) scale({k}) translate({-cx} {-cy})" {extra}/>'

DEFS = '''
<linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">
 <stop offset="0" stop-color="#6e4e0c"/><stop offset=".18" stop-color="#f6dc8a"/><stop offset=".32" stop-color="#b8862a"/>
 <stop offset=".5" stop-color="#fff3c4"/><stop offset=".66" stop-color="#c3922f"/><stop offset=".82" stop-color="#f2d27a"/><stop offset="1" stop-color="#5e420a"/></linearGradient>
<linearGradient id="goldV" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="#fff0b8"/><stop offset=".3" stop-color="#e8c15c"/><stop offset=".55" stop-color="#a97a1c"/><stop offset=".75" stop-color="#f4d67e"/><stop offset="1" stop-color="#7a5710"/></linearGradient>
<linearGradient id="goldDark" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a6516"/><stop offset="1" stop-color="#3e2b05"/></linearGradient>
<linearGradient id="yel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe95c"/><stop offset=".5" stop-color="#ffd51f"/><stop offset="1" stop-color="#e09c00"/></linearGradient>
<radialGradient id="yelHi" cx="42%" cy="28%" r="70%"><stop offset="0" stop-color="#fff" stop-opacity=".5"/><stop offset=".45" stop-color="#fff" stop-opacity=".08"/><stop offset="1" stop-color="#7a4a00" stop-opacity=".35"/></radialGradient>
<linearGradient id="ink" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#26262a"/><stop offset=".5" stop-color="#0c0c0d"/><stop offset="1" stop-color="#000"/></linearGradient>
<radialGradient id="inkHi" cx="50%" cy="30%" r="75%"><stop offset="0" stop-color="#fff" stop-opacity=".13"/><stop offset=".5" stop-color="#fff" stop-opacity=".02"/><stop offset="1" stop-color="#000" stop-opacity=".4"/></radialGradient>
<linearGradient id="white" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#e9e6dd"/></linearGradient>
<linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".42"/><stop offset=".38" stop-color="#fff" stop-opacity=".08"/><stop offset=".39" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<radialGradient id="pearl" cx="35%" cy="30%" r="70%"><stop offset="0" stop-color="#fffbe6"/><stop offset=".35" stop-color="#f0cf6e"/><stop offset=".8" stop-color="#8a6312"/><stop offset="1" stop-color="#4a3305"/></radialGradient>
<filter id="bevel" x="-5%" y="-5%" width="110%" height="110%">
 <feGaussianBlur in="SourceAlpha" stdDeviation="5" result="b"/>
 <feSpecularLighting in="b" surfaceScale="7" specularConstant="1.1" specularExponent="22" lighting-color="#fff8dc" result="s"><feDistantLight azimuth="225" elevation="42"/></feSpecularLighting>
 <feComposite in="s" in2="SourceAlpha" operator="in" result="s2"/>
 <feComposite in="SourceGraphic" in2="s2" operator="arithmetic" k2="1" k3=".75"/></filter>
<filter id="bevelS" x="-5%" y="-5%" width="110%" height="110%">
 <feGaussianBlur in="SourceAlpha" stdDeviation="2" result="b"/>
 <feSpecularLighting in="b" surfaceScale="4" specularConstant="1" specularExponent="28" lighting-color="#fff8dc" result="s"><feDistantLight azimuth="225" elevation="45"/></feSpecularLighting>
 <feComposite in="s" in2="SourceAlpha" operator="in" result="s2"/>
 <feComposite in="SourceGraphic" in2="s2" operator="arithmetic" k2="1" k3=".6" result="o"/>
 <feDropShadow in="o" dx="0" dy="3" stdDeviation="2.5" flood-color="#000" flood-opacity=".55"/></filter>
<filter id="sink" x="-5%" y="-5%" width="110%" height="110%">
 <feDropShadow dx="0" dy="-2" stdDeviation="0" flood-color="#000" flood-opacity=".35" result="a"/>
 <feDropShadow dx="0" dy="2.5" stdDeviation=".6" flood-color="#fff4c0" flood-opacity=".55"/></filter>
<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur in="SourceAlpha" stdDeviation="8" result="b"/><feFlood flood-color="#ffd51f" flood-opacity=".45"/><feComposite in2="b" operator="in" result="g"/><feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="drop" x="-10%" y="-10%" width="120%" height="125%"><feDropShadow dx="0" dy="14" stdDeviation="16" flood-color="#000" flood-opacity=".55"/></filter>
<filter id="brush" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".003 .55" numOctaves="2" seed="7" result="t"/><feColorMatrix in="t" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .55 -.18"/></filter>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="3" result="t"/><feColorMatrix in="t" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .22 -.06"/></filter>
'''

def svg(body, defs='', w=1200, h=1400):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<defs>{DEFS}{defs}</defs>{body}</svg>')

def txt(s, x, y, size, fill, ls=0, fam='Montserrat', weight=600, extra=''):
    return (f'<text x="{x}" y="{y}" text-anchor="middle" font-family="{fam}" font-weight="{weight}" font-size="{size}" '
            f'letter-spacing="{ls}" fill="{fill}" {extra}>{s}</text>')

def enamel_overlays(path, k, clipid):
    """Brillo de cristal + cepillado + grano, recortados al campo."""
    return (f'<clipPath id="{clipid}">{sc(path,k)}</clipPath>'
            f'<g clip-path="url(#{clipid})"><rect width="1200" height="1400" filter="url(#brush)" opacity=".35"/>'
            f'<rect width="1200" height="1400" filter="url(#grain)" opacity=".5"/></g>')

def sheen(path, k):
    return sc(path, k, extra='fill="url(#sheen)"')

SV = {}

# ---------- 1 · MODENA (escudo alto de escudería, esmalte amarillo) ----------
P1 = 'M150,110 H1050 V780 C1050,1020 870,1180 600,1300 C330,1180 150,1020 150,780 Z'
b = []
b.append(f'<g filter="url(#drop)">{sc(P1,1,extra="fill=\"#0b0b0b\"")}</g>')
b.append(sc(P1, .975, extra='fill="url(#gold)" filter="url(#bevel)"'))
b.append(sc(P1, .945, extra='fill="#0b0b0b"'))
b.append(sc(P1, .93, extra='fill="url(#yel)"'))
b.append(sc(P1, .93, extra='fill="url(#yelHi)"'))
b.append(enamel_overlays(P1, .93, 'c1'))
# franja superior negra con filete dorado y el nombre
b.append('<clipPath id="c1b"><path d="' + P1 + '" transform="translate(600 715) scale(.93) translate(-600 -715)"/></clipPath>')
b.append('<g clip-path="url(#c1b)"><rect x="0" y="0" width="1200" height="345" fill="url(#ink)"/><rect x="0" y="0" width="1200" height="345" fill="url(#inkHi)"/>'
         '<rect x="0" y="345" width="1200" height="12" fill="url(#gold)" filter="url(#bevelS)"/></g>')
m, h = art('name', 'url(#goldV)', 600, 175, 720, 'bevelS'); b.append(m)
m, h = art('fig', '#0b0b0b', 600, 400, 560, 'sink'); b.append(m)
m, h = art('one', '#0b0b0b', 600, 790, 250, 'sink'); b.append(m)
b.append(txt('ENTRENADOR PERSONAL', 600, 1040, 22, '#3a2a00', 8, weight=700))
b.append(sheen(P1, .93))
SV['1-modena'] = svg(''.join(b))

# ---------- 2 · STUTTGART (cuartelado con franjas, escudo central) ----------
P2 = 'M175,175 Q600,85 1025,175 L1025,700 C1025,1000 830,1175 600,1285 C370,1175 175,1000 175,700 Z'
b = []
b.append(f'<g filter="url(#drop)">{sc(P2,1,extra="fill=\"url(#gold)\" filter=\"url(#bevel)\"")}</g>')
b.append(sc(P2, .955, extra='fill="#0b0b0b"'))
b.append('<clipPath id="c2"><path d="' + P2 + '" transform="translate(600 715) scale(.94) translate(-600 -715)"/></clipPath>')
q = ['<g clip-path="url(#c2)">', '<rect width="1200" height="1400" fill="url(#ink)"/>']
# franjas amarillas/negras en cuarteles 1 y 4
for x0, y0 in [(0, 300), (600, 720)]:
    for i in range(0, 420, 60):
        q.append(f'<rect x="{x0}" y="{y0+i}" width="600" height="30" fill="url(#yel)"/>')
# cuarteles 2 y 3: negro con trama dorada fina
q.append('<pattern id="hatch" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="14" height="14" fill="#0d0d0e"/><rect width="1.4" height="14" fill="#b8862a" opacity=".55"/></pattern>')
q.append('<rect x="600" y="300" width="600" height="420" fill="url(#hatch)"/><rect x="0" y="720" width="600" height="600" fill="url(#hatch)"/>')
q.append('<rect width="1200" height="1400" fill="url(#inkHi)"/>')
# banda superior dorada con el nombre
q.append('<rect x="0" y="0" width="1200" height="300" fill="url(#gold)" filter="url(#bevel)"/><rect x="0" y="292" width="1200" height="10" fill="#0b0b0b"/>')
q.append('</g>')
b.append(''.join(q))
b.append(enamel_overlays(P2, .94, 'c2g'))
m, h = art('name', '#0b0b0b', 600, 168, 640, 'sink'); b.append(m)
# escudo central
PI = 'M420,430 H780 V720 C780,850 700,930 600,975 C500,930 420,850 420,720 Z'
b.append(f'<g filter="url(#drop)">{sc(PI,1.12,600,700,"fill=\"url(#gold)\" filter=\"url(#bevel)\"")}</g>')
b.append(sc(PI, 1.04, 600, 700, 'fill="#0b0b0b"'))
b.append(sc(PI, 1.0, 600, 700, 'fill="url(#yel)"'))
b.append(sc(PI, 1.0, 600, 700, 'fill="url(#yelHi)"'))
m, h = art('fig', '#0b0b0b', 600, 500, 300, 'sink'); b.append(m)
m, h = art('one', '#0b0b0b', 600, 715, 150, 'sink'); b.append(m)
b.append(sc(PI, 1.0, 600, 700, 'fill="url(#sheen)"'))
b.append(txt('ORIHUELA', 600, 1160, 30, 'url(#goldV)', 14, weight=700, extra='filter="url(#bevelS)"'))
b.append(sheen(P2, .94))
SV['2-stuttgart'] = svg(''.join(b))

# ---------- 3 · SANT'AGATA (escudo ancho, negro y oro macizo) ----------
P3 = 'M115,135 L1085,135 L1040,250 L1040,690 C1040,975 845,1150 600,1290 C355,1150 160,975 160,690 L160,250 Z'
b = []
b.append(f'<g filter="url(#drop)">{sc(P3,1,extra="fill=\"url(#gold)\" filter=\"url(#bevel)\"")}</g>')
b.append(sc(P3, .95, extra='fill="#050505"'))
b.append(sc(P3, .93, extra='fill="url(#ink)"'))
b.append(sc(P3, .93, extra='fill="url(#inkHi)"'))
b.append(enamel_overlays(P3, .93, 'c3'))
b.append(sc(P3, .885, extra='fill="none" stroke="#ffd51f" stroke-width="3" opacity=".9"'))
m, h = art('name', 'url(#goldV)', 600, 225, 700, 'bevelS'); b.append(m)
b.append('<rect x="330" y="385" width="540" height="3" fill="url(#gold)"/>')
m, h = art('fig', 'url(#goldV)', 600, 420, 580, 'bevelS'); b.append(m)
m, h = art('one', '#ffd51f', 600, 815, 240, 'glow'); b.append(m)
b.append(txt('ENTRENADOR PERSONAL', 600, 1048, 22, '#cfc6ad', 8, weight=500))
b.append(sheen(P3, .93))
SV['3-santagata'] = svg(''.join(b))

# ---------- 4 · MOLSHEIM (medallón ovalado con perlas doradas) ----------
b = []
b.append('<g filter="url(#drop)"><ellipse cx="600" cy="700" rx="560" ry="420" fill="url(#gold)" filter="url(#bevel)"/></g>')
b.append('<ellipse cx="600" cy="700" rx="530" ry="392" fill="#0b0b0b"/>')
b.append('<ellipse cx="600" cy="700" rx="515" ry="377" fill="url(#ink)"/><ellipse cx="600" cy="700" rx="515" ry="377" fill="url(#inkHi)"/>')
b.append('<clipPath id="c4"><ellipse cx="600" cy="700" rx="515" ry="377"/></clipPath><g clip-path="url(#c4)"><rect width="1200" height="1400" filter="url(#grain)" opacity=".5"/></g>')
# perlas
n = 64
for i in range(n):
    t = 2*math.pi*i/n
    x = 600 + 478*math.cos(t); y = 700 + 342*math.sin(t)
    b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="url(#pearl)"/>')
# óvalo interior amarillo con figuras
b.append('<ellipse cx="600" cy="700" rx="420" ry="292" fill="url(#gold)" filter="url(#bevelS)"/>')
b.append('<ellipse cx="600" cy="700" rx="405" ry="277" fill="url(#yel)"/><ellipse cx="600" cy="700" rx="405" ry="277" fill="url(#yelHi)"/>')
b.append('<clipPath id="c4b"><ellipse cx="600" cy="700" rx="405" ry="277"/></clipPath><g clip-path="url(#c4b)"><rect width="1200" height="1400" filter="url(#brush)" opacity=".35"/></g>')
m, h = art('name', '#0b0b0b', 600, 470, 560, 'sink'); b.append(m)
m, h = art('fig', '#0b0b0b', 600, 590, 330, 'sink'); b.append(m)
m, h = art('one', '#0b0b0b', 600, 812, 140, 'sink'); b.append(m)
b.append('<ellipse cx="600" cy="700" rx="405" ry="277" fill="url(#sheen)"/>')
b.append('<ellipse cx="600" cy="700" rx="530" ry="392" fill="url(#sheen)" opacity=".5"/>')
SV['4-molsheim'] = svg(''.join(b))

# ---------- 5 · GAYDON (alas doradas + escudo) ----------
def wing(sgn):
    out = []
    for i in range(9):
        y = 470 + i*30
        L = 560 - i*52
        x0 = 600 + sgn*120
        tipx = x0 + sgn*L
        tipy = y - 70 + i*9
        th = 22 - i*1.2
        d = (f'M{x0},{y} Q{x0+sgn*L*.55:.0f},{y-18:.0f} {tipx:.0f},{tipy:.0f} '
             f'Q{x0+sgn*L*.5:.0f},{y+th*.6:.0f} {x0},{y+th:.0f} Z')
        out.append(f'<path d="{d}" fill="url(#goldV)" stroke="#5e420a" stroke-width="1.5"/>')
        # nervio
        out.append(f'<path d="M{x0},{y+th*.45:.0f} Q{x0+sgn*L*.5:.0f},{y-4:.0f} {tipx-sgn*20:.0f},{tipy+4:.0f}" fill="none" stroke="#fff3c4" stroke-width="1.6" opacity=".7"/>')
    return f'<g filter="url(#bevelS)">{"".join(reversed(out))}</g>'
P5 = 'M440,380 H760 V700 C760,860 690,960 600,1010 C510,960 440,860 440,700 Z'
b = []
b.append(f'<g filter="url(#drop)">{wing(-1)}{wing(1)}</g>')
# placa central con nombre
b.append('<g filter="url(#drop)"><rect x="300" y="195" width="600" height="120" rx="8" fill="url(#gold)" filter="url(#bevel)"/></g>')
b.append('<rect x="314" y="209" width="572" height="92" rx="4" fill="url(#ink)"/>')
m, h = art('name', 'url(#goldV)', 600, 219, 470, 'bevelS'); b.append(m)
b.append(f'<g filter="url(#drop)">{sc(P5,1.08,600,700,"fill=\"url(#gold)\" filter=\"url(#bevel)\"")}</g>')
b.append(sc(P5, 1.0, 600, 700, 'fill="#0b0b0b"'))
b.append(sc(P5, .96, 600, 700, 'fill="url(#yel)"'))
b.append(sc(P5, .96, 600, 700, 'fill="url(#yelHi)"'))
m, h = art('fig', '#0b0b0b', 600, 480, 270, 'sink'); b.append(m)
m, h = art('one', '#0b0b0b', 600, 690, 150, 'sink'); b.append(m)
b.append(sc(P5, .96, 600, 700, 'fill="url(#sheen)"'))
b.append(txt('ENTRENADOR PERSONAL', 600, 1080, 26, 'url(#goldV)', 10, weight=700, extra='filter="url(#bevelS)"'))
SV['5-gaydon'] = svg(''.join(b))

# ---------- 6 · HERÁLDICO (partido amarillo/negro, figuras en contracambio, cintas) ----------
P6 = 'M200,250 Q400,290 600,225 Q800,290 1000,250 L1000,700 C1000,975 820,1130 600,1230 C380,1130 200,975 200,700 Z'
b = []
b.append(f'<g filter="url(#drop)">{sc(P6,1,extra="fill=\"url(#gold)\" filter=\"url(#bevel)\"")}</g>')
b.append(sc(P6, .955, extra='fill="#0b0b0b"'))
b.append('<clipPath id="c6"><path d="' + P6 + '" transform="translate(600 715) scale(.935) translate(-600 -715)"/></clipPath>')
b.append('<clipPath id="L"><rect x="0" y="0" width="600" height="1400"/></clipPath><clipPath id="R"><rect x="600" y="0" width="600" height="1400"/></clipPath>')
b.append('<g clip-path="url(#c6)"><rect x="0" width="600" height="1400" fill="url(#yel)"/><rect x="600" width="600" height="1400" fill="url(#ink)"/>'
         '<rect width="1200" height="1400" fill="url(#yelHi)" opacity=".6"/><rect x="597" width="6" height="1400" fill="url(#gold)"/></g>')
b.append(enamel_overlays(P6, .935, 'c6g'))
# figuras en contracambio: negras sobre amarillo, amarillas sobre negro
m, h = art('fig', '#0b0b0b', 600, 430, 560, 'sink', 'L'); b.append(m)
m, h = art('fig', 'url(#yel)', 600, 430, 560, 'glow', 'R'); b.append(m)
m, h = art('one', '#0b0b0b', 600, 820, 250, 'sink', 'L'); b.append(m)
m, h = art('one', 'url(#yel)', 600, 820, 250, 'glow', 'R'); b.append(m)
b.append(sheen(P6, .935))
# cintas
def ribbon(y, w, hgt, flip=False):
    x0 = 600 - w/2; x1 = 600 + w/2; d = 1 if not flip else -1
    tails = (f'<path d="M{x0-70},{y+20*d} L{x0},{y} L{x0},{y+hgt} L{x0-70},{y+hgt+20*d} L{x0-35},{y+hgt/2+10*d} Z" fill="#8a6516"/>'
             f'<path d="M{x1+70},{y+20*d} L{x1},{y} L{x1},{y+hgt} L{x1+70},{y+hgt+20*d} L{x1+35},{y+hgt/2+10*d} Z" fill="#8a6516"/>')
    body = f'<path d="M{x0},{y} Q600,{y-30*d} {x1},{y} L{x1},{y+hgt} Q600,{y+hgt-30*d} {x0},{y+hgt} Z" fill="url(#gold)" filter="url(#bevel)"/>'
    return f'<g filter="url(#drop)">{tails}{body}</g>'
b.append(ribbon(140, 700, 110))
m, h = art('name', '#0b0b0b', 600, 150, 520, 'sink'); b.append(m)
b.append(ribbon(1185, 620, 90, True))
m, h = art('ep', '#0b0b0b', 600, 1210, 470, ''); b.append(m)
SV['6-heraldico'] = svg(''.join(b))

for k, s in SV.items():
    open(f'{D}{k}.html', 'w').write('<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:transparent}svg{display:block}</style></head><body>' + s + '</body></html>')
print('ok', list(SV))
