import random, math
random.seed(11)
W, H = 1080, 1350

# ---------- suela (punta arriba) ----------
SOLE = ("M260 0 C366 0 436 74 446 196 C454 300 424 382 404 444 C388 496 384 548 396 628 "
        "C410 724 404 828 342 890 C300 930 220 930 178 890 C120 834 112 736 128 644 "
        "C140 572 138 510 116 446 C90 372 72 280 82 190 C96 72 160 0 260 0 Z")

def lugs():
    out = []
    # antepié: tacos en chevron
    for r in range(15):
        y = 40 + r * 30
        for c in range(-1, 10):
            x = 60 + c * 44 + (22 if r % 2 else 0)
            out.append(f'<path d="M{x} {y+12} l18 -12 l18 12 l0 9 l-18 -12 l-18 12 Z" class="lug"/>')
    # puente: ranuras
    for r in range(5):
        y = 500 + r * 24
        out.append(f'<rect x="110" y="{y}" width="300" height="10" rx="5" class="lug2"/>')
    # talón: círculos
    for r in range(7):
        for c in range(9):
            x = 120 + c * 34 + (17 if r % 2 else 0); y = 640 + r * 36
            out.append(f'<circle cx="{x}" cy="{y}" r="12" class="lug"/>')
    return "\n".join(out)

def blob(cx, cy, r, n=9, j=0.35):
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = r * (1 + random.uniform(-j, j))
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a) * random.uniform(.7, 1)))
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f} "
    for i in range(n):
        p0 = pts[i]; p1 = pts[(i + 1) % n]
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        d += f"Q{p0[0]:.1f} {p0[1]:.1f} {mx:.1f} {my:.1f} "
    return d + "Z"

def debris():
    out = []
    # barro
    for _ in range(26):
        x = random.uniform(110, 410); y = random.uniform(40, 880)
        out.append(f'<path d="{blob(x,y,random.uniform(10,34))}" fill="#5b4329" opacity="{random.uniform(.55,.9):.2f}" filter="url(#rough)"/>')
    # piedrecitas
    for _ in range(40):
        x = random.uniform(110, 410); y = random.uniform(30, 890)
        col = random.choice(["#b9ab94", "#8d8270", "#d6cbb5", "#6f675a"])
        out.append(f'<path d="{blob(x,y,random.uniform(4,10),7,.4)}" fill="{col}"/>')
    # arenilla
    for _ in range(260):
        x = random.uniform(95, 425); y = random.uniform(20, 900)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(.8,2.4):.1f}" fill="#c9bda5" opacity="{random.uniform(.4,.9):.2f}"/>')
    # elementos señalados
    for _ in range(14):
        out.append(f'<circle cx="{random.uniform(180,235):.0f}" cy="{random.uniform(70,110):.0f}" r="{random.uniform(2,4):.1f}" fill="#f2d14a" opacity=".9"/>')
    out.append('<path d="M350 160 l14 -6 l10 10 l-6 14 l-16 -2 Z" fill="#7d7f86" stroke="#c9ccd3" stroke-width="1.5"/>')
    out.append(f'<path d="{blob(165,255,26,10,.35)}" fill="#6b4a22" filter="url(#rough)"/><path d="{blob(172,250,12,8,.3)}" fill="#8a6430" opacity=".8"/>')
    out.append(f'<path d="{blob(385,480,18,9,.35)}" fill="#0b0b0b" stroke="#444" stroke-width="1.5"/><path d="M378 474 q6 -4 12 0" stroke="#888" stroke-width="2" fill="none"/>')
    out.append(f'<path d="{blob(170,585,24,12,.25)}" fill="#6f8f6a" opacity=".75" filter="url(#rough)"/>')
    for _ in range(18):
        out.append(f'<circle cx="{random.uniform(150,190):.0f}" cy="{random.uniform(565,605):.0f}" r="1.6" fill="#d8f0c8"/>')
    out.append('<path d="M190 750 l18 -6 l5 13 l-19 6 Z" fill="#3c8fd6"/><path d="M215 772 l10 -3 l3 8 l-10 3 Z" fill="#e24b4b"/><circle cx="182" cy="776" r="4" fill="#f5f5f5"/>')
    out.append('<path d="M290 850 l26 -8 l6 12 l-28 10 Z" fill="#9aa0a8" stroke="#e1e4ea" stroke-width="1.5"/>')
    # chicle rosa
    out.append(f'<path d="{blob(330,300,24,10,.3)}" fill="#e889b0" opacity=".92"/><path d="M322 292 q12 -8 20 3" stroke="#fff" stroke-opacity=".5" stroke-width="4" fill="none" stroke-linecap="round"/>')
    # mancha de aceite irisada
    out.append(f'<path d="{blob(300,345,38,12,.25)}" fill="url(#oil)" opacity=".85"/>')
    # hoja seca
    out.append('<g transform="translate(300 665) rotate(-30)"><path d="M0 0 C20 -30 60 -30 80 0 C60 30 20 30 0 0 Z" fill="#7c8b3a"/><path d="M0 0 L80 0" stroke="#4d5822" stroke-width="2"/></g>')
    # cristal
    out.append('<path d="M150 150 l26 -10 l8 22 l-30 6 Z" fill="#bfe6e8" opacity=".75" stroke="#fff" stroke-opacity=".6"/>')
    # trozo de plástico azul
    out.append('')
    # colilla
    out.append('<g transform="translate(120 420) rotate(25)"><rect width="56" height="13" rx="3" fill="#efe9dc"/><rect width="20" height="13" rx="3" fill="#d48b3a"/></g>')
    # pelo
    out.append('<path d="M240 780 c30 -40 60 20 90 -30" stroke="#2b2118" stroke-width="2" fill="none"/>')
    return "\n".join(out)

def microbes(n, box, scale=1):
    x0, y0, x1, y1 = box; out = []
    for i in range(n):
        x = random.uniform(x0, x1); y = random.uniform(y0, y1); a = random.uniform(0, 180)
        s = random.uniform(.7, 1.3) * scale
        k = random.random()
        col = "#FFD51F" if random.random() < .7 else "#ffffff"
        if k < .5:  # bacilo con flagelos
            out.append(f'<g transform="translate({x:.0f} {y:.0f}) rotate({a:.0f}) scale({s:.2f})" class="glow" stroke="{col}">'
                       f'<rect x="-16" y="-6" width="32" height="12" rx="6" fill="{col}" fill-opacity=".18" stroke-width="2"/>'
                       f'<path d="M16 0 c8 -6 12 6 20 0 M-16 0 c-8 6 -12 -6 -20 0" fill="none" stroke-width="1.4"/></g>')
        elif k < .8:  # cocos
            out.append(f'<g transform="translate({x:.0f} {y:.0f}) scale({s:.2f})" class="glow" stroke="{col}" fill="{col}" fill-opacity=".18" stroke-width="1.8">'
                       '<circle r="5"/><circle cx="10" cy="2" r="5"/><circle cx="4" cy="10" r="5"/></g>')
        else:  # espora de moho
            out.append(f'<g transform="translate({x:.0f} {y:.0f}) scale({s:.2f})" class="glow" stroke="{col}" fill="none" stroke-width="1.6">'
                       '<circle r="7"/>' + "".join(f'<path d="M{7*math.cos(t):.1f} {7*math.sin(t):.1f} l{5*math.cos(t):.1f} {5*math.sin(t):.1f}"/>' for t in [i*math.pi/4 for i in range(8)]) + '</g>')
    return "\n".join(out)

ICONS = {
 "flor":  '<g fill="none" stroke-width="2"><circle r="3"/>' + "".join(f'<circle cx="{7*math.cos(t):.1f}" cy="{7*math.sin(t):.1f}" r="4"/>' for t in [i*2*math.pi/6 for i in range(6)]) + '</g>',
 "pb":    '<text y="5" text-anchor="middle" font-family="Anton" font-size="15" stroke="none" fill="#FFD51F">Pb</text>',
 "gota_h":'<path d="M0 -10 C6 -2 9 3 9 6 A9 9 0 0 1 -9 6 C-9 3 -6 -2 0 -10Z" fill="none" stroke-width="2"/><path d="M-4 6 h8" stroke-width="2"/>',
 "gota":  '<path d="M0 -11 C7 -2 10 3 10 6 A10 10 0 0 1 -10 6 C-10 3 -7 -2 0 -11Z" fill="#FFD51F" fill-opacity=".25" stroke-width="2"/>',
 "bac":   '<rect x="-11" y="-5" width="22" height="10" rx="5" fill="none" stroke-width="2"/><path d="M11 0 c4 -4 7 4 10 0" fill="none" stroke-width="1.6"/>',
 "asf":   '<path d="M-11 6 L-4 -8 L4 -8 L11 6 Z" fill="none" stroke-width="2"/><path d="M0 -6 v3 M0 0 v3" stroke-width="2"/>',
 "moho":  '<circle r="5" fill="none" stroke-width="2"/>' + "".join(f'<path d="M{6*math.cos(t):.1f} {6*math.sin(t):.1f} l{4*math.cos(t):.1f} {4*math.sin(t):.1f}" stroke-width="2"/>' for t in [i*math.pi/4 for i in range(8)]),
 "hoja":  '<path d="M-10 8 C-10 -6 2 -10 10 -10 C10 0 6 10 -10 8Z" fill="none" stroke-width="2"/><path d="M-10 8 L6 -6" stroke-width="1.6"/>',
 "micro": '<rect x="-9" y="-9" width="7" height="7" fill="none" stroke-width="2"/><rect x="2" y="-3" width="5" height="5" fill="#FFD51F" stroke="none"/><rect x="-5" y="4" width="4" height="4" fill="none" stroke-width="2"/><circle cx="7" cy="7" r="2.5" fill="#FFD51F" stroke="none"/>',
 "metal": '<path d="M-11 6 L-6 -6 H6 L11 6 Z" fill="none" stroke-width="2"/><path d="M-6 -1 H6" stroke-width="1.6"/>',
}

ITEMS = [
 ("Alérgenos", "polen, ácaros y polvo", "flor", (205, 90)),
 ("Plomo", "polvo urbano y pintura vieja", "pb", (362, 166)),
 ("Heces y orina", "de perros, gatos y palomas", "gota_h", (165, 255)),
 ("Aceite de motor", "calzada y aparcamientos", "gota", (300, 345)),
 ("E. coli", "bacteria intestinal", "bac", (240, 420)),
 ("Restos de asfalto", "alquitrán y caucho", "asf", (385, 480)),
 ("Moho", "esporas y humedad", "moho", (170, 585)),
 ("Herbicidas y pesticidas", "parques y jardines", "hoja", (340, 665)),
 ("Microplásticos", "neumáticos y basura", "micro", (200, 760)),
 ("Metales pesados", "tráfico e industria", "metal", (305, 857)),
]
SOLE_TX, SOLE_TY, SOLE_ROT, SOLE_S = 50, 352, -6, 0.86

def to_canvas(px, py):
    # aplica scale, rotate alrededor del centro (260,465), translate
    cx, cy = 260, 465
    x, y = (px - cx) * SOLE_S, (py - cy) * SOLE_S
    a = math.radians(SOLE_ROT)
    xr = x * math.cos(a) - y * math.sin(a); yr = x * math.sin(a) + y * math.cos(a)
    return xr + cx + SOLE_TX, yr + cy + SOLE_TY

def labels():
    out = []
    top, step = 410, 76
    lx = 628
    for i, (t, d, ic, pt) in enumerate(ITEMS):
        y = top + i * step
        px, py = to_canvas(*pt)
        e1 = 500 + i*4
        out.append(f'<path d="M{px:.0f} {py:.0f} L{e1} {py:.0f} L{e1+40} {y} L{lx-34} {y}" class="ln"/>')
        out.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="6" class="dot"/><circle cx="{px:.0f}" cy="{py:.0f}" r="13" class="ring"/>')
        out.append(f'<g transform="translate({lx-8} {y})" stroke="#FFD51F" fill="none"><circle r="20" stroke-width="1.5" stroke-opacity=".55"/><g transform="translate(0 0)">{ICONS[ic]}</g></g>')
        out.append(f'<text x="{lx+24}" y="{y+2}" class="lt">{t}</text>')
        out.append(f'<text x="{lx+24}" y="{y+27}" class="ld">{d}</text>')
    return "\n".join(out)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
 <radialGradient id="bg" cx="30%" cy="55%" r="80%"><stop offset="0" stop-color="#232016"/><stop offset=".55" stop-color="#121212"/><stop offset="1" stop-color="#090909"/></radialGradient>
 <linearGradient id="rubber" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3b3b3b"/><stop offset="1" stop-color="#232323"/></linearGradient>
 <radialGradient id="oil" cx="40%" cy="40%"><stop offset="0" stop-color="#3a2b5c"/><stop offset=".35" stop-color="#1d5e57"/><stop offset=".65" stop-color="#5b4a12"/><stop offset="1" stop-color="#111"/></radialGradient>
 <filter id="rough"><feTurbulence type="fractalNoise" baseFrequency=".09" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="9"/></filter>
 <filter id="grime" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="4" seed="21"/><feColorMatrix values="0 0 0 0 .36  0 0 0 0 .27  0 0 0 0 .17  0 0 0 1.3 -.62"/></filter>
 <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="18" stdDeviation="22" flood-color="#000" flood-opacity=".7"/></filter>
 <clipPath id="sole"><path d="{SOLE}"/></clipPath>
 <clipPath id="lens"><circle cx="0" cy="0" r="92"/></clipPath>
 <style>
  .lug{{fill:#565656;stroke:#1a1a1a;stroke-width:2}}
  .lug2{{fill:#161616}}
  .glow{{filter:url(#glow)}}
  .ln{{fill:none;stroke:#FFD51F;stroke-width:1.6;stroke-opacity:.85}}
  .dot{{fill:#FFD51F}}
  .ring{{fill:none;stroke:#FFD51F;stroke-width:1.5;stroke-opacity:.6}}
  .lt{{font-family:Anton;font-size:30px;fill:#fff;letter-spacing:.5px}}
  .ld{{font-family:Poppins;font-size:17px;fill:#b9b9b9}}
 </style>
</defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<!-- polvo amarillo de fondo -->
{"".join(f'<circle cx="{random.uniform(0,W):.0f}" cy="{random.uniform(0,H):.0f}" r="{random.uniform(.6,2.2):.1f}" fill="#FFD51F" opacity="{random.uniform(.08,.45):.2f}"/>' for _ in range(220))}
<!-- escudo de marca de agua grande -->
<image href="escudo.png" x="20" y="460" width="560" height="538" opacity=".07"/>
<!-- titulo -->
<text x="70" y="72" font-family="Poppins" font-size="24" font-weight="500" fill="#FFD51F" letter-spacing="3">¿SABES QUÉ METES EN CASA?</text>
<image href="t1.png" x="66" y="92" width="750" height="125"/>
<image href="t2.png" x="66" y="231" width="669" height="114"/>
<rect x="70" y="364" width="120" height="5" fill="#FFD51F"/>
<!-- microbios alrededor -->
{microbes(18, (20, 420, 540, 1200))}
<!-- suela -->
<g transform="translate({SOLE_TX} {SOLE_TY}) translate(260 465) rotate({SOLE_ROT}) scale({SOLE_S}) translate(-260 -465)" filter="url(#shadow)">
  <path d="{SOLE}" fill="url(#rubber)"/>
  <g clip-path="url(#sole)">
    {lugs()}
    <rect width="520" height="940" filter="url(#grime)"/>
    {debris()}
    {microbes(14, (110, 60, 410, 860), .8)}
  </g>
  <path d="{SOLE}" fill="none" stroke="#5a5a5a" stroke-width="10"/>
  <path d="{SOLE}" fill="none" stroke="#111" stroke-width="2" transform="translate(0 0)"/>
</g>
{labels()}
<!-- lupa -->
<g transform="translate(150 1110) scale(.85)">
  <line x1="-62" y1="62" x2="-118" y2="118" stroke="#FFD51F" stroke-width="16" stroke-linecap="round"/>
  <circle r="92" fill="#0b0b0b"/>
  <g clip-path="url(#lens)">
    <circle r="92" fill="#1b170c"/>
    {microbes(16, (-80, -80, 80, 80), 2.0)}
  </g>
  <circle r="92" fill="none" stroke="#FFD51F" stroke-width="7"/>
  <text x="0" y="122" text-anchor="middle" font-family="Anton" font-size="18" fill="#FFD51F" letter-spacing="2">x1000</text>
</g>
<!-- pie -->
<rect x="0" y="{H-120}" width="{W}" height="120" fill="#FFD51F"/>
<text x="70" y="{H-70}" font-family="Anton" font-size="34" fill="#0d0d0d">POR ESO, EN NUESTRA SALA NO ENTRA EL CALZADO DE LA CALLE.</text>
<text x="70" y="{H-36}" font-family="Poppins" font-size="20" font-weight="500" fill="#0d0d0d">Entrenas en calcetines o con barefoot de uso exclusivo en el centro.</text>
<!-- escudo firma -->
<image href="escudo.png" x="{W-232}" y="60" width="190" height="182"/>
</svg>'''
open("suela.svg", "w").write(svg)
open("suela.html", "w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:#000}}</style></head><body>{svg}</body></html>')
print("ok")
