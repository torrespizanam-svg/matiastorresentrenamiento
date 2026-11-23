exec(open('fusion6.py').read().split("# 1 · Clásico")[0])
EXTRA += '''<linearGradient id="figGradH" gradientUnits="userSpaceOnUse" x1="0" y1="460" x2="0" y2="830">
 <stop offset="0" stop-color="#fff0b8"/><stop offset=".3" stop-color="#e8c15c"/><stop offset=".5" stop-color="#a97a1c"/>
 <stop offset=".66" stop-color="#3a2800"/><stop offset=".8" stop-color="#0b0b0b"/><stop offset="1" stop-color="#0b0b0b"/></linearGradient>
<linearGradient id="fadeMidH" gradientUnits="userSpaceOnUse" x1="0" y1="380" x2="0" y2="860">
 <stop offset="0" stop-color="#0b0b0b"/><stop offset=".25" stop-color="#0b0b0b" stop-opacity=".9"/>
 <stop offset=".5" stop-color="#120c00" stop-opacity=".6"/><stop offset=".75" stop-color="#1e1500" stop-opacity=".22"/><stop offset="1" stop-color="#1e1500" stop-opacity="0"/></linearGradient>'''
b=[]; base2(b,'H2'); b.append(guill('H2'))
b.append('<g clip-path="url(#kH2)"><rect width="1200" height="880" fill="url(#fadeMidH)"/></g>')
tipband(b,'H2',soft=True)
beads(b)
m,h=art('fig','url(#figGradH)',600,450,580,'bevelS'); b.append(m)
m,h=art('one','#0b0b0b',600,850,230,'sink'); b.append(m)
close(b,'H2','14-cabecera-perlas')
