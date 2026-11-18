from PIL import Image
import numpy as np, os
SRC='/home/claude/matiastorresentrenamiento/fotos-origen/nombre-escudo.png'
src=Image.open(SRC).convert('RGBA')
Y0,Y1=100,509
H=Y1-Y0
def crop(x0,x1,y0=Y0,y1=Y1): return src.crop((x0,y0,x1,y1))
def arr(im): return np.array(im).copy()
def img(a): return Image.fromarray(a)
def trim(im):
    a=np.array(im)[...,3]; xs=np.where(a.max(0)>0)[0]; return im.crop((xs[0],0,xs[-1]+1,im.height))
def erase(im,x0,x1,y0,y1,ox,oy=Y0):
    a=arr(im); a[max(0,y0-oy):max(0,y1-oy), max(0,x0-ox):max(0,x1-ox),3]=0; return img(a)
G={}
G['M']=trim(crop(0,300))
G['A']=trim(crop(845,1075))
G['O']=trim(crop(1600,1840))
G['R']=trim(crop(1838,2078))
G['E']=trim(crop(2340,2570))
G['S']=trim(crop(2570,2781))
G['I']=trim(crop(1440,1540))
# F
G['F']=trim(erase(crop(2340,2570),2432,2570,380,509,2340))
# L: E without top and middle arms
G['L']=trim(erase(crop(2340,2570),2434,2570,0,405,2340))
# C: O open right
o=crop(1600,1840); G['C']=trim(erase(o,1600+int(240*0.66),1840,205,398,1600))
# U: O open top between stems
# U: two stems + bottom curve of O
_o=G['O']; _u=Image.new('RGBA',(_o.width,H),(0,0,0,0))
_bot=_o.crop((0,300-Y0,_o.width,H)); _u.paste(_bot,(0,300-Y0),_bot)
_ls=trim(crop(2340,2432,Y0,420)); _rs=trim(crop(1446,1534,Y0,420))
_u.paste(_ls,(0,0),_ls); _u.paste(_rs,(_o.width-_rs.width,0),_rs); G['U']=trim(_u)
# D: E stem + right half of O
st=trim(crop(2340,2434)); rh=trim(crop(1722,1840))
d=Image.new('RGBA',(st.width+rh.width-6,H),(0,0,0,0)); d.paste(st,(0,0),st); d.paste(rh,(st.width-6,0),rh); G['D']=d
# P: R without leg
G['P']=trim(erase(crop(1838,2078),1930,2078,338,509,1838))
# N from M
ma=arr(crop(0,300))
for y in range(H):
    gy=y+Y0; xc=int(128+(162-128)*(gy-115)/(500-115)); ma[y,xc:,3]=0
lt=trim(img(ma)); stem=trim(crop(212,300))
n=Image.new('RGBA',(lt.width+stem.width-8,H),(0,0,0,0)); n.paste(lt,(0,0),lt); n.paste(stem,(lt.width-8,0),stem); G['N']=n
# T: I stem + crossbar chunk
bar=src.crop((1650,12,1880,80))
t=Image.new('RGBA',(bar.width,H),(0,0,0,0)); s_=G['I']; t.paste(s_,(bar.width//2-s_.width//2,0),s_)
bt=bar.resize((bar.width,int(bar.height*1.05))); t.paste(bt,(0,10),bt); G['T']=trim(t)
# accent
acc=src.crop((2050,10,2190,80)).rotate(32,expand=True,resample=Image.BICUBIC)
acc=acc.resize((int(acc.width*0.62),int(acc.height*0.62)),Image.LANCZOS)
# Q: O + tail
q=Image.new('RGBA',(G['O'].width+40,H+40),(0,0,0,0)); q.paste(G['O'],(0,0),G['O'])
tail=src.crop((1900,14,2020,74)).rotate(-40,expand=True,resample=Image.BICUBIC); tail=tail.resize((int(tail.width*.8),int(tail.height*.8)))
q.paste(tail,(G['O'].width-tail.width//2-10,H-tail.height//2-20),tail); G['Q']=q
# period
G['.']=trim(src.crop((2200,14,2265,80)).resize((62,62)).crop((0,0,62,62)))
def word(w,gap=22,space=70):
    w=w.upper(); acc_top=acc.height-10
    parts=[];W=0
    for ch in w:
        if ch==' ': parts.append(('sp',space)); W+=space; continue
        base={'Á':'A','É':'E','Í':'I','Ó':'O','Ú':'U'}.get(ch,ch)
        g=G[base]; parts.append((ch,g)); W+=g.width+gap
    W-=gap
    out=Image.new('RGBA',(W,H+acc_top+60),(0,0,0,0)); x=0
    for ch,g in parts:
        if ch=='sp': x+=g; continue
        y=acc_top+(H-g.height if ch=='.' else 0)
        if ch=='.': y=acc_top+H-g.height-8
        out.paste(g,(x,y),g)
        if ch in 'ÁÉÍÓÚ': out.paste(acc,(x+g.width//2-acc.width//2+10,0),acc)
        x+=g.width+gap
    a=np.array(out)[...,3]; ys=np.where(a.max(1)>0)[0]; out=out.crop((0,ys[0],W,ys[-1]+1))
    return out
def colorize(im,rgb):
    a=im.split()[3]; c=Image.new('RGBA',im.size,rgb+(255,)); c.putalpha(a); return c
if __name__=='__main__':
    os.makedirs('glyphs',exist_ok=True)
    for k,g in G.items(): g.save(f'glyphs/{"punto" if k=="." else k}.png')
    rows=[word(t) for t in ['MÁS RESULTADOS.','NUESTRO EQUIPO','MATIAS TORRES','FORMACIÓN']]
    Wm=max(r.width for r in rows); Ht=sum(r.height+40 for r in rows)
    bg=Image.new('RGB',(Wm+40,Ht+40),(13,13,13)); y=20
    for r in rows: bg.paste(colorize(r,(255,230,0)),(20,y),r); y+=r.height+40
    bg.resize((bg.width//3,bg.height//3)).save('preview.png')
