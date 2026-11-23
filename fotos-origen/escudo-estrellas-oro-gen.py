import math, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy import ndimage as nd
R='/home/claude/matiastorresentrenamiento/'
F=3
crop=Image.open('/home/claude/crop.png').convert('L'); L=np.array(crop).astype(int)
lab,_=nd.label(L<22); cid=[v for v in lab[40:60,460] if v][0]
sh=nd.binary_fill_holes(lab==cid)
ys,xs=np.where(sh); cx=(xs.min()+xs.max())/2
# silueta simétrica y suave a alta resolución
Hc,Wc=sh.shape
m=cv2.resize(sh.astype(np.float32),(Wc*F,Hc*F),interpolation=cv2.INTER_LINEAR)
m=cv2.GaussianBlur(m,(0,0),F*2.2)
W,H=m.shape[1],m.shape[0]; C=int(round(cx*F))
left=m[:,:C]; m=np.concatenate([left,left[:,::-1][:, :W-C]],axis=1)[:, :W]
S0=(m>0.5)
# silueta vectorial: arriba curva suave, lateral polinomio, hombros redondeados
xs_t=np.arange(260,C-10); ys_t=np.array([np.argmax(S0[:,x]) for x in xs_t])
pt=np.polyfit(xs_t,ys_t,2)
yr=np.arange(660,H-140); xr=np.array([np.argmax(S0[y]) for y in yr])
yn=lambda y:(y-1600)/1200
ps=np.polyfit(yn(yr),xr,5)
pts=[]
for x in np.linspace(C,0,400):
    y=np.polyval(pt,x); pts.append((x,y))
ys=np.linspace(400,H,2000); xsd=np.polyval(ps,yn(ys))
side=[(x,y) for x,y in zip(xsd,ys) if x<C]
ytip=side[-1][1]
# corta el arco de arriba donde cruza el lateral
top=[(x,y) for x,y in pts if x>=np.polyval(ps,yn(y))]
poly=top+[p for p in side if p[1]>=top[-1][1]]
poly=poly+[(C,ytip+4)]
full=poly+[(2*C-x,y) for x,y in reversed(poly)]
SSx=2; im=Image.new('L',(W*SSx,H*SSx),0); ImageDraw.Draw(im).polygon([(x*SSx,y*SSx) for x,y in full],fill=255)
mm=cv2.GaussianBlur(np.array(im.resize((W,H),Image.LANCZOS)).astype(np.float32)/255,(0,0),9)
S=mm>0.5
# antialias del borde
Sa=cv2.GaussianBlur(S.astype(np.float32),(0,0),0.8)
dist=nd.distance_transform_edt(S).astype(np.float32)
u=lambda v:v*F
gy,gx=np.gradient(cv2.GaussianBlur(dist,(0,0),1.5))
nn=np.sqrt(gx**2+gy**2)+1e-6; nx,ny=gx/nn,gy/nn  # normal hacia dentro
Lv=np.array([-0.45,-0.75,0.55]); Lv/=np.linalg.norm(Lv)
DK=np.array([104,62,6.]); MD=np.array([222,160,36.]); LT=np.array([255,232,150.])
def bevel(a,b,round_=1.0):
    t=np.clip((dist-a)/(b-a),0,1); band=(dist>=a)&(dist<=b)
    dh=math.pi*np.cos(math.pi*t)*round_*3.0
    N=np.stack([-dh*nx,-dh*ny,np.ones_like(dh)*1.0],-1); N/=np.linalg.norm(N,axis=-1,keepdims=True)
    d=np.clip((N*Lv).sum(-1),0,1); sp=d**28
    col=np.where(d[...,None]<0.6, DK+(MD-DK)*(d[...,None]/0.6), MD+(LT-MD)*((d[...,None]-0.6)/0.4))
    col=col+sp[...,None]*np.array([90,80,60.])
    return band,np.clip(col,0,255)
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
yu=yy/F
# ---------- fondo interior
def sstep(a,b,x):
    t=np.clip((x-a)/(b-a),0,1); return t*t*(3-2*t)
gold=np.array([238,186,38.]); goldhi=np.array([255,222,105.]); blk=np.array([13,12,11.])
g=sstep(255,420,yu)[...,None]
rad=np.exp(-(((xx/F-cx)/250)**2+((yu-470)/210)**2))[...,None]
field=gold+(goldhi-gold)*rad*0.9
hv=np.clip(np.abs(xx/F-cx)/330,0,1)[...,None]; field=field*(1-0.22*hv**2)
bg=blk*(1-g)+field*g
# brillo diagonal suave en la zona negra de arriba
sheen=np.exp(-(((xx/F-cx+120)*0.7+(yu-180))/90)**2)[...,None]*(1-g)
bg=bg+sheen*np.array([38,34,28.])
fb=sstep(756,880,yu)[...,None]*0.82
bg=bg*(1-fb)+blk*fb
rng=np.random.default_rng(7)
nz=cv2.GaussianBlur(rng.standard_normal((H,W)).astype(np.float32),(0,0),sigmaX=F*25,sigmaY=0.7)
nz/=nz.std()+1e-6
bg=bg*(1+0.05*nz[...,None])+rng.standard_normal((H,W,1)).astype(np.float32)*1.6
img=np.zeros((H,W,3),np.float32)
img[:]=bg
# ---------- anillos: contorno negro, bisel dorado, separación, línea fina
img[dist<u(30)]=np.array([16,13,9.])
b1,c1=bevel(u(3.5),u(21)); img[b1]=c1[b1]
b2,c2=bevel(u(37.5),u(40.5),0.6); img[b2]=c2[b2]
# sombra interior bajo el aro
sha=np.clip(1-(dist-u(30))/u(14),0,1)*(dist>=u(30))
img*=(1-0.45*sha[...,None]) if False else 1
img[(dist>=u(30))&(dist<u(37.5))]*= (1-0.35*sha[(dist>=u(30))&(dist<u(37.5))])[...,None]
# contorno exterior negro fino
img[dist<u(3.5)]=np.array([10,8,6.])
out=Image.fromarray(np.clip(img,0,255).astype(np.uint8))
# ---------- utilidades de capa
def place_mask(src,box,smooth=1.2):
    x0,y0,x1,y1=[int(u(v)) for v in box]
    mk=src.resize((x1-x0,y1-y0),Image.LANCZOS)
    a=np.array(mk).astype(np.float32)/255
    a=cv2.GaussianBlur(a,(0,0),smooth*F/3+0.6); a=np.clip((a-0.5)*3.2+0.5,0,1)
    full=np.zeros((H,W),np.float32); full[y0:y1,x0:x1]=a; return full
def comp(base,alpha,color):
    if np.ndim(color)==1: color=np.broadcast_to(np.array(color,np.float32),base.shape)
    return base*(1-alpha[...,None])+color*alpha[...,None]
def shift(a,dx,dy): return nd.shift(a,(dy,dx),order=1)
def ink(base,a,deep=False):
    # sombra proyectada + tinta + bisel claro arriba
    s=cv2.GaussianBlur(shift(a,0,u(1.6)),(0,0),u(1.8))
    base=base*(1-0.42*s[...,None])
    base=comp(base,a,[22,17,10])
    hi=np.clip(a-shift(a,0,u(0.9)),0,1)*0.55
    base=comp(base,hi,[120,92,40])
    lo=np.clip(a-shift(a,0,-u(0.9)),0,1)*0.6
    return comp(base,lo,[4,3,2])
def metal_grad(y0,y1,stops):
    t=np.clip((yy-u(y0))/(u(y1)-u(y0)),0,1)
    ps=[s[0] for s in stops]; cs=np.array([s[1] for s in stops],np.float32)
    return np.stack([np.interp(t,ps,cs[:,k]) for k in range(3)],-1)
arr=np.array(out).astype(np.float32)
# ---------- MATIAS TORRES en oro metálico
nm=Image.open(R+'fotos-origen/nombre-escudo.png').split()[-1]
na=place_mask(nm,(228,196,697,196+469*509/2781),0.8)
glow=cv2.GaussianBlur(na,(0,0),u(6))*0.18
arr=comp(arr,glow,[200,150,40])
ol=np.clip(cv2.dilate(na,np.ones((int(u(1.4))*2+1,)*2,np.uint8)),0,1)
arr=comp(arr,ol,[8,6,3])
gm=metal_grad(196,282,[(0,(255,247,205)),(.3,(246,210,110)),(.52,(196,140,36)),(.6,(170,118,28)),(.78,(232,184,72)),(1,(255,226,140))])
gm=gm*(1+0.06*nz[...,None])
arr=comp(arr,na,gm)
hi=np.clip(na-shift(na,0,u(1.0)),0,1)*0.7; arr=comp(arr,hi,[255,250,225])
# ---------- DESDE 2021 + líneas y rombos
o=Image.fromarray(np.clip(arr,0,255).astype(np.uint8)); d=ImageDraw.Draw(o)
mont=lambda w,s: (lambda f:(f.set_variation_by_name(w),f)[1])(ImageFont.truetype(R+'../matiastorresentrenamiento/'[:0]+'/usr/share/fonts/truetype/google-fonts/ofl/montserrat/Montserrat[wght].ttf',s))
def tracked(img,txt,font,cxu,cyu,track,fill):
    d=ImageDraw.Draw(img); ws=[font.getlength(c) for c in txt]; tw=sum(ws)+track*(len(txt)-1)
    x=u(cxu)-tw/2; bb=font.getbbox('D'); y=u(cyu)-(bb[1]+bb[3])/2
    for c,w in zip(txt,ws): d.text((x,y),c,font=font,fill=fill); x+=w+track
GL=(214,170,78)
tracked(o,'DESDE 2021',mont('SemiBold',int(u(10.5))),cx,304,u(5.2),GL)
for x0,x1 in ((235,288),(cx*2-288,cx*2-235)): d.line([(u(x0),u(304)),(u(x1),u(304))],fill=GL,width=int(u(1.3)))
for xc in (296,cx*2-296):
    r=u(4.2); d.polygon([(u(xc),u(304)-r),(u(xc)+r,u(304)),(u(xc),u(304)+r),(u(xc)-r,u(304))],fill=(240,200,100))
arr=np.array(o).astype(np.float32)
# ---------- figuras y 1 A 1 (tinta con relieve)
fm=Image.open(R+'fotos-origen/fig_mask.png')
fa=place_mask(fm,(300,324,300+325,324+325*746/1159),1.0)
arr=ink(arr,fa)
om=Image.open(R+'fotos-origen/1a1_mask.png')
w1=136; oa=place_mask(om,(cx-w1/2,548,cx+w1/2,548+w1*532/840),1.6)
arr=ink(arr,oa)
# ---------- ENTRENADOR PERSONAL y ORIHUELA nítidos
def text_mask(txt,font,box,track=0):
    ws=[font.getlength(c) for c in txt]; tw=int(sum(ws)+track*(len(txt)-1))+40
    t=Image.new('L',(tw,font.size*2),0); dd=ImageDraw.Draw(t); x=20
    for c,w in zip(txt,ws): dd.text((x,10),c,font=font,fill=255); x+=w+track
    t=t.crop(t.getbbox()); x0,y0,x1,y1=[int(u(v)) for v in box]
    t=t.resize((x1-x0,y1-y0),Image.LANCZOS); a=np.zeros((H,W),np.float32); a[y0:y1,x0:x1]=np.array(t)/255; return a
anton=ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/ofl/anton/Anton-Regular.ttf',600)
ea=text_mask('ENTRENADOR PERSONAL',anton,(cx-234.5,662,cx+234.5,705)); arr=ink(arr,ea)
ra=text_mask('ORIHUELA',mont('Bold',400),(cx-117,742,cx+117,762),track=190); arr=ink(arr,ra)
# ---------- estrellas doradas facetadas con filo
SS=2; st=Image.new('RGB',(W*SS,H*SS),(0,0,0)); sm=Image.new('L',(W*SS,H*SS),0)
dst=ImageDraw.Draw(st); dsm=ImageDraw.Draw(sm)
Rs=u(23); gap=u(55); cy=u(806)
lang=math.atan2(-0.75,-0.45)
for i in range(5):
    x=u(cx)+(i-2)*gap; pts=[]
    for k in range(10):
        a=-math.pi/2+k*math.pi/5; r=Rs if k%2==0 else Rs*0.42
        pts.append((x+r*math.cos(a),cy+r*math.sin(a)))
    dsm.polygon([(px*SS,py*SS) for px,py in pts],fill=255)
    for k in range(10):
        p1,p2=pts[k],pts[(k+1)%10]
        mx,my=(p1[0]+p2[0])/2-x,(p1[1]+p2[1])/2-cy
        # cara a la izquierda o derecha de la arista radial
        ang=math.atan2(my,mx); side=1 if k%2==0 else -1
        lit=0.5+0.5*math.cos(ang+side*0.5-lang)
        SD=np.array([120,70,0.]);SL=np.array([255,214,80.]);c=SD+(SL-SD)*(0.12+0.88*lit**1.3)
        dst.polygon([(x*SS,cy*SS),(p1[0]*SS,p1[1]*SS),(p2[0]*SS,p2[1]*SS)],fill=tuple(int(v) for v in c))
st=st.resize((W,H),Image.LANCZOS); sm=sm.resize((W,H),Image.LANCZOS)
sa=np.array(sm).astype(np.float32)/255
s=cv2.GaussianBlur(shift(sa,0,u(2.2)),(0,0),u(3)); arr=arr*(1-0.65*s[...,None])
glow=cv2.GaussianBlur(sa,(0,0),u(7))*0.22; arr=comp(arr,glow,[230,170,40])
ol=cv2.dilate(sa,np.ones((int(u(1.1))*2+1,)*2,np.uint8)); arr=comp(arr,ol,[52,32,4])
arr=comp(arr,sa,np.array(st).astype(np.float32))
# ---------- salida con transparencia
alpha=(Sa*255).astype(np.uint8)
res=Image.fromarray(np.clip(arr,0,255).astype(np.uint8)).convert('RGBA'); res.putalpha(Image.fromarray(alpha))
res=res.crop(res.getbbox()); res.save('/home/claude/escudo-hd.png'); print(res.size)
bg=Image.new('RGB',res.size,(8,8,8)); bg.paste(res,(0,0),res); bg.save('/home/claude/escudo-hd-negro.jpg',quality=95)
