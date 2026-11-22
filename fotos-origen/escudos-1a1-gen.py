import math, random
exec(open('gen.py').read().split("V = {}")[0])  # reutiliza SH, DEFS, explosion, fig, one

def mk_mask(id_, href, x, y, w, h):
    return f'<mask id="{id_}" maskUnits="userSpaceOnUse" x="{x}" y="{y}" width="{w}" height="{h}"><image href="{href}" x="{x}" y="{y}" width="{w}" height="{h}"/></mask>'

def name(fill, x, y, w, filt="", mid="mName"):
    h = w*293/1600
    f = f' filter="url(#{filt})"' if filt else ""
    return mk_mask(mid, 'name_mask.png', x, y, w, h), f'<g{f}><rect x="{x}" y="{y}" width="{w}" height="{h:.0f}" fill="{fill}" mask="url(#{mid})"/></g>'

def fig_at(fill, x, y, w, filt="", mid="mF2"):
    h = w*746/1159
    f = f' filter="url(#{filt})"' if filt else ""
    return mk_mask(mid, 'fig_mask.png', x, y, w, h), f'<g{f}><rect x="{x}" y="{y}" width="{w}" height="{h:.0f}" fill="{fill}" mask="url(#{mid})"/></g>'

def one_at(fill, x, y, w, filt="", mid="mO2"):
    h = w*532/840
    f = f' filter="url(#{filt})"' if filt else ""
    return mk_mask(mid, '1a1_mask.png', x, y, w, h), f'<g{f}><rect x="{x}" y="{y}" width="{w}" height="{h:.0f}" fill="{fill}" mask="url(#{mid})"/></g>'

def S(k):  # shield scaled around center
    return f'<path d="{SH}" transform="translate(1133 813) scale({k}) translate(-1133 -813)"'

EXTRA = '''
<linearGradient id="yel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe866"/><stop offset=".55" stop-color="#ffd51f"/><stop offset="1" stop-color="#e3a400"/></linearGradient>
<radialGradient id="yelHi" cx="40%" cy="30%" r="60%"><stop offset="0" stop-color="#fff" stop-opacity=".45"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<linearGradient id="rainbow" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ff2fb3"/><stop offset=".25" stop-color="#b04bff"/><stop offset=".45" stop-color="#18c8ff"/><stop offset=".65" stop-color="#2fe06b"/><stop offset=".82" stop-color="#ffd51f"/><stop offset="1" stop-color="#ff4a3a"/></linearGradient>
<filter id="emb2" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur in="SourceAlpha" stdDeviation="1.5" result="b"/><feSpecularLighting in="b" surfaceScale="3" specularConstant=".6" specularExponent="35" lighting-color="#fff" result="s"><feDistantLight azimuth="235" elevation="55"/></feSpecularLighting><feComposite in="s" in2="SourceAlpha" operator="in" result="s2"/><feComposite in="SourceGraphic" in2="s2" operator="arithmetic" k2="1" k3=".18" result="e"/><feDropShadow dx="2" dy="4" stdDeviation="3" flood-color="#7a5600" flood-opacity=".55"/></filter>
<radialGradient id="hiH" cx="50%" cy="38%" r="65%"><stop offset="0" stop-color="#fff" stop-opacity=".16"/><stop offset=".6" stop-color="#fff" stop-opacity=".04"/><stop offset="1" stop-color="#000" stop-opacity=".35"/></radialGradient>
<filter id="crisp" x="-5%" y="-5%" width="110%" height="110%"><feComponentTransfer in="SourceGraphic" result="c"><feFuncA type="linear" slope="1.6" intercept="-.25"/></feComponentTransfer><feDropShadow dx="1.5" dy="2.5" stdDeviation="1.2" flood-color="#6b4a00" flood-opacity=".45"/></filter>
<pattern id="carbon" width="16" height="16" patternUnits="userSpaceOnUse"><rect width="16" height="16" fill="#16171a"/><rect width="8" height="8" fill="#26272c"/><rect x="8" y="8" width="8" height="8" fill="#26272c"/><rect width="8" height="3" fill="#33343a"/><rect x="8" y="8" width="3" height="8" fill="#33343a"/></pattern>
<pattern id="stripes" width="28" height="28" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><rect width="28" height="28" fill="#0b0b0b"/><rect width="14" height="28" fill="#ffd51f"/></pattern>
<filter id="emboss" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur in="SourceAlpha" stdDeviation="2" result="b"/><feSpecularLighting in="b" surfaceScale="4" specularConstant=".9" specularExponent="30" lighting-color="#fff" result="s"><feDistantLight azimuth="235" elevation="50"/></feSpecularLighting><feComposite in="s" in2="SourceAlpha" operator="in" result="s2"/><feComposite in="SourceGraphic" in2="s2" operator="arithmetic" k2="1" k3=".55" result="e"/><feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#000" flood-opacity=".5"/></filter>
'''

def laurel(side):
    sgn = -1 if side == 'l' else 1
    P = []
    for i in range(41):
        t = i/40
        x = 1133 + sgn*(60 + 470*math.sin(math.pi/2*t)**0.7)
        y = 1300 - 760*t
        P.append((x, y))
    out = [f'<polyline points="{" ".join(f"{x:.0f},{y:.0f}" for x,y in P)}" fill="none" stroke="url(#gold)" stroke-width="7" stroke-linecap="round"/>']
    for i in range(3, 41, 3):
        x, y = P[i]; x0, y0 = P[i-1]
        ang = math.degrees(math.atan2(y-y0, x-x0)) + 90
        for d in (-1, 1):
            lx = x + d*20*math.cos(math.radians(ang-90)); ly = y + d*20*math.sin(math.radians(ang-90))
            out.append(f'<ellipse cx="{lx:.0f}" cy="{ly:.0f}" rx="13" ry="38" transform="rotate({ang + d*38:.0f} {lx:.0f} {ly:.0f})" fill="url(#gold)"/>')
    x, y = P[-1]
    out.append(f'<ellipse cx="{x:.0f}" cy="{y-26:.0f}" rx="12" ry="34" fill="url(#gold)"/>')
    return f'<g filter="url(#emboss)">{"".join(out)}</g>'

V = {}
# E · Scuderia
m1, f1 = fig_at("#000000", 813, 468, 640, "crisp")
m2, o1 = one_at("#000000", 953, 905, 360, "crisp")
V['e'] = (m1+m2, f'''<g filter="url(#shadow)">{S(1)} fill="#0b0b0b"/></g>
{S(.955)} fill="url(#gold)" filter="url(#bevel)"/>
{S(.912)} fill="#0b0b0b"/>
{S(.9)} fill="url(#yel)"/>
{S(.9)} fill="url(#yelHi)"/>
{f1}{o1}
{S(.9)} fill="url(#sheen)"/>''')

# F · Blasón
mN, n1 = name("#0b0b0b", 843, 478, 580, "", "mN1")
m3, f2 = fig_at("url(#goldV)", 968, 700, 330, "glowY", "mF3")
m4, o2 = one_at("url(#oneG)", 1048, 940, 170, "glowY", "mO3")
V['f'] = (mN+m3+m4, f'''<g filter="url(#shadow)">{S(1)} fill="url(#gold)" filter="url(#bevel)"/></g>
{S(.92)} fill="#fbfaf6"/>
{S(.92)} fill="url(#yelHi)" opacity=".5"/>
{n1}
<g filter="url(#shadow)"><path d="{SH}" transform="translate(1133 890) scale(.58) translate(-1133 -813)" fill="url(#gold)" filter="url(#bevel)"/></g>
<path d="{SH}" transform="translate(1133 890) scale(.535) translate(-1133 -813)" fill="url(#ink)"/>
{f2}{o2}
<path d="{SH}" transform="translate(1133 890) scale(.535) translate(-1133 -813)" fill="url(#sheen)"/>
{S(.92)} fill="url(#sheen)" opacity=".6"/>''')

# G · Herencia (laurel dorado, esmalte negro, cinta "DESDE 2021")
m5, f3 = fig_at("url(#goldV)", 853, 560, 560, "glowY", "mF4")
m6, o3 = one_at("url(#oneG)", 988, 935, 290, "glowY", "mO4")
V['g'] = (m5+m6, f'''{laurel('l')}{laurel('r')}
<g filter="url(#shadow)">{S(1)} fill="url(#gold)" filter="url(#bevel)"/></g>
{S(.93)} fill="url(#ink)"/>
{S(.88)} fill="none" stroke="url(#gold)" stroke-width="3"/>
<g clip-path="url(#inner)" opacity=".35">{explosion(5, cy=760, scale=.7, alpha=.6)}</g>
{f3}{o3}
{S(.93)} fill="url(#sheen)"/>
<g filter="url(#shadow)"><path d="M760 1150 L820 1120 L1446 1120 L1506 1150 L1446 1180 L1446 1250 L820 1250 L820 1180 Z" fill="url(#gold)" filter="url(#bevel)"/>
<path d="M700 1170 L820 1150 L820 1250 L700 1270 L740 1215 Z" fill="#a87400"/><path d="M1566 1170 L1446 1150 L1446 1250 L1566 1270 L1526 1215 Z" fill="#a87400"/>
<rect x="820" y="1140" width="626" height="100" fill="url(#gold)" filter="url(#bevel)"/></g>
<text x="1133" y="1210" text-anchor="middle" font-family="Anton" font-size="46" letter-spacing="9" fill="#0b0b0b">ORIHUELA · DESDE 2021</text>''')

# H · Fibra de carbono (nombre arriba, figuras grandes, borde de color interior)
mN2, n2 = name("url(#goldV)", 873, 478, 520, "glowY", "mN5")
m7, f4 = fig_at("url(#goldV)", 833, 650, 600, "glowY", "mF5")
m8, o4 = one_at("url(#oneG)", 1043, 1050, 180, "glowY", "mO5")
V['h'] = (mN2+m7+m8, f'''<g filter="url(#shadow)">{S(1)} fill="url(#gold)" filter="url(#bevel)"/></g>
{S(.935)} fill="#050505"/>
{S(.915)} fill="none" stroke="url(#rainbow)" stroke-width="7" opacity=".95" filter="url(#glowW)"/>
{S(.895)} fill="url(#carbon)"/>
{S(.895)} fill="url(#hiH)"/>
{n2}
{f4}{o4}
{S(.895)} fill="url(#sheen)"/>''')

for k, (masks, body) in V.items():
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB}" width="1146" height="1140"><defs>{DEFS}{EXTRA}{masks}</defs>{body}</svg>'
    open(f'{k}.html', 'w').write(f'<!doctype html><html><head><style>html,body{{margin:0;background:transparent}}</style></head><body>{svg}</body></html>')
print("ok")
