exec(open('fusion4.py').read().split("# ---- V1")[0])
import math
EXTRA += '<linearGradient id="fadeH" gradientUnits="userSpaceOnUse" x1="0" y1="250" x2="0" y2="520"><stop offset="0" stop-color="#0b0b0b"/><stop offset=".35" stop-color="#0b0b0b" stop-opacity=".75"/><stop offset=".7" stop-color="#2a1d00" stop-opacity=".22"/><stop offset="1" stop-color="#2a1d00" stop-opacity="0"/></linearGradient>'
b=[]; base(b,'H')
b.append('<g clip-path="url(#kH)"><rect width="1200" height="560" fill="url(#fadeH)"/></g>')
b.append('<g clip-path="url(#kH)"><rect width="1200" height="1400" fill="url(#spot)"/></g>')
b.append(sc(P,.885,extra='fill="none" stroke="url(#gold)" stroke-width="5"'))
m,h=art('fig','#0b0b0b',600,470,560,'sink'); b.append(m)
m,h=art('one','#0b0b0b',600,840,250,'sink'); b.append(m)
finish(b,'11-escudo-cabecera')
