#!/usr/bin/env python3
"""Genera site.css y las páginas reales (el-centro/, equipo/, …) a partir de index.html.
Uso:  python3 tools/maak-paginas.py
- Primera vez: extrae el contenido de las vistas v-* de index.html.
- Después: reutiliza el contenido ya guardado entre <!--CONTENIDO--> y <!--/CONTENIDO--> de cada página
  (las vistas se quitan de index.html) y regenera cabecera, pie, CSS y enlaces."""
import re, os, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
DOM="https://matiasentrenadorpersonal.es/"
S=open("index.html",encoding="utf-8").read()
B=S.index("<body")

# nombre de vista -> (carpeta, title, description, nav activo)
PAGES={
 "sobre":("el-centro","El centro de entrenamiento personal · Matías Torres, Orihuela","Conoce el centro de entrenamiento personal de Matías Torres en Orihuela: un entrenador, una sala privada y toda la atención para ti. Pide tu primera valoración de 30 min.","sobre"),
 "equipo":("equipo","Equipo · Matías Torres, entrenador personal en Orihuela","Conoce al equipo del centro de Matías Torres en Orihuela: entrenador personal, readaptación y recuperación trabajando juntos por tu objetivo.","equipo"),
 "metodologia":("como-trabajo","Cómo trabajo · Método de entrenamiento personal en Orihuela","Así trabajamos en Orihuela: primera valoración, plan a medida y seguimiento uno a uno. Entrenamiento personal privado con Matías Torres.","metodologia"),
 "servicios":("servicios","Servicios de entrenamiento personal en Orihuela · Matías Torres","Pierde grasa, gana fuerza, recupera tu espalda o vuelve a entrenar tras una lesión. Servicios de entrenamiento personal privado en Orihuela.","servicios"),
 "programas":("programas","Programas de entrenamiento personal en Orihuela · Matías Torres","Programas a medida en Orihuela: pérdida de grasa, fuerza, Mamá en Forma, readaptación de lesiones y Espalda en Forma.","servicios"),
 "faq":("preguntas-frecuentes","Preguntas frecuentes · Entrenamiento personal en Orihuela","Resolvemos tus dudas sobre la primera valoración, precios, horarios y cómo es entrenar con Matías Torres en Orihuela.","faq"),
}
SLUG={v:p[0] for v,p in PAGES.items()}
SPA_ONLY={"reservar","contacto","opiniones","solo-aqui","centro","test","gestion"}

def fix_links(h,page):
    P="../" if page else ""
    def sub(m):
        name,key=m.group(1),m.group(2)
        if name in SLUG:
            if name=="programas" and key: return 'href="%s%s/#%s"'%(P,SLUG[name],key)
            return 'href="%s%s/"'%(P,SLUG[name])
        if page:
            if name=="inicio": return 'href="%s"'%P
            if name in SPA_ONLY: return 'href="%s#%s%s"'%(P,name,("/"+key) if key else "")
        return m.group(0)
    return re.sub(r'href="#([a-z-]+)(?:/([a-z]+))?"',sub,h)
def fix_assets(h):
    return re.sub(r'((?:src|href|poster|data-src|srcset)=")(?=(?:fotos|video|marca|escudo|favicon|logo-matias|kit-digital)[/.])',r'\1../',h)

# ---- CSS compartido (todos los <style> de la cabecera)
css="\n".join(m.group(1) for m in re.finditer(r"<style[^>]*>(.*?)</style>",S,re.S))
# el CSS vive en la raíz: las url() relativas ya son correctas
open("site.css","w",encoding="utf-8").write(css)

# ---- vistas
vs=[(m.start(),m.group(1)) for m in re.finditer(r'<div class="view[^"]*" id="v-([a-z]+)">',S)]
bodies={}
for i,(st,n) in enumerate(vs):
    en=vs[i+1][0] if i+1<len(vs) else S.index("<section",st)
    t=S[st:en]; t=re.sub(r'(\s*<!--.*?-->)+\s*$',"",t,flags=re.S)
    bodies[n]=t
def old_body(n):
    f=PAGES[n][0]+"/index.html"
    if n in bodies: return bodies[n]
    t=open(f,encoding="utf-8").read()
    t=t[t.index("<!--CONTENIDO-->")+16:t.index("<!--/CONTENIDO-->")]
    # deshacer reescritura para volver a aplicarla limpia
    t=t.replace('src="../','src="').replace('href="../','href="').replace('poster="../','poster="').replace('data-src="../','data-src="')
    return t

header=S[S.index("<header>"):S.index("</header>")+9]
foot=S[S.index("<footer"):S.index("</footer>")+9]
wa=S[S.index('<div class="wa-float"'):]; wa=wa[:wa.index("</a></div>\n")+11] if False else wa
# bloque WhatsApp: hasta el cierre de su div raíz (contamos divs)
def balanced(t):
    d=0
    for m in re.finditer(r"<(/?)div\b",t):
        d+= -1 if m.group(1) else 1
        if d==0: return t[:t.index(">",m.start())+1]
wa=balanced(wa)
dlgs="".join(re.search(r'<dialog id="%s".*?</dialog>'%k,S,re.S).group(0)+"\n" for k in ["d-legal","d-priv","d-cook"])
wajs=re.search(r"<script>\(function\(\)\{var w=document\.querySelector\(\"\.wa-float\"\).*?</script>",S,re.S).group(0)

JS="""<script>
(function(){
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
$("#burger").onclick=()=>$("#nav").classList.toggle("open");
const hd=$("#site header");const f=()=>hd.classList.toggle("mini",scrollY>40);addEventListener("scroll",f,{passive:true});f();
$$("[data-dlg]").forEach(a=>a.addEventListener("click",e=>{e.preventDefault();const d=document.getElementById(a.dataset.dlg);d.showModal();d.scrollTop=0;requestAnimationFrame(()=>{d.scrollTop=0})}));
const ck=$("#ckChange");if(ck)ck.addEventListener("click",()=>{try{localStorage.removeItem("mtCookiesIG")}catch(_){}$("#d-cook").close()});
function prog(){const k=location.hash.slice(1);if(!k)return;const d=document.getElementById("prog-"+k);if(d){d.open=true;setTimeout(()=>d.scrollIntoView({behavior:"smooth",block:"start"}),60)}}
prog();addEventListener("hashchange",prog);
$$("img[data-lb]").forEach(()=>{});
})();
</script>"""

head0=S[:B]
head0=re.sub(r"<style[^>]*>.*?</style>\s*","",head0,flags=re.S)  # fuera CSS inline (va en site.css)
head0=re.sub(r'<script type="application/ld\+json">.*?</script>\s*',"",head0,flags=re.S)
head0=re.sub(r'<link rel="preload"[^>]*>\s*',"",head0)
head0=re.sub(r"<title>.*?</title>\s*","",head0,flags=re.S)
head0=re.sub(r'<meta (name="description"|property="og:(title|description|url)")[^>]*>\s*',"",head0)
head0=re.sub(r'<link rel="canonical"[^>]*>\s*',"",head0)
head0=re.sub(r'<script[^>]*>.*?</script>\s*',"",head0,flags=re.S)
head0=head0.replace('href="./favicon.svg"','href="../favicon.svg"')
head0=re.sub(r'(og:image" content=")[^"]*',r"\1"+DOM+"fotos/sala.webp?v=7",head0)

sitemap=[DOM]
for n,(slug,title,desc,navv) in PAGES.items():
    body=fix_assets(fix_links(old_body(n),True))
    hd=fix_assets(fix_links(header,True))
    # marcar activo
    hd=re.sub(r'(<a href="[^"]*" data-v="%s")'%navv,r'\1 class="on"',hd,count=1) if 'class' not in re.search(r'<a href="[^"]*" data-v="%s"[^>]*>'%navv,hd).group(0) else hd
    ft=fix_assets(fix_links(foot,True))
    url=DOM+slug+"/"
    sitemap.append(url)
    ld=('{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Inicio","item":"%s"},{"@type":"ListItem","position":2,"name":"%s","item":"%s"}]}'%(DOM,title.split(" · ")[0].replace('"',''),url))
    html=(head0.replace("</head>","")
      +'<title>%s</title>\n<meta name="description" content="%s">\n<link rel="canonical" href="%s">\n<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n<meta property="og:url" content="%s">\n'%(title,desc,url,title,desc,url)
      +'<script type="application/ld+json">%s</script>\n<link href="../site.css" rel="stylesheet">\n</head>\n<body>\n<div id="site">\n'%ld
      +hd+"\n<!--CONTENIDO-->"+body.replace('class="view','class="view on',1) if 'view on' not in body else "")
    html=(head0.replace("</head>","")
      +'<title>%s</title>\n<meta name="description" content="%s">\n<link rel="canonical" href="%s">\n<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n<meta property="og:url" content="%s">\n'%(title,desc,url,title,desc,url)
      +'<script type="application/ld+json">%s</script>\n<link href="../site.css" rel="stylesheet">\n</head>\n<body>\n<div id="site">\n'%ld
      +hd+"\n<!--CONTENIDO-->"+(body if 'view on' in body else body.replace('class="view','class="view on',1))+"<!--/CONTENIDO-->\n"
      +ft+"\n"+fix_assets(wa)+"\n</div>\n"+fix_assets(dlgs)+"\n"+wajs+"\n"+JS+"\n</body>\n</html>\n")
    os.makedirs(slug,exist_ok=True)
    open(slug+"/index.html","w",encoding="utf-8").write(html)
    print("página",slug,len(html)//1024,"KB")

# ---- index.html: enlaces reales + vistas fuera
T=S
for n in PAGES:
    if n in bodies:
        T=T.replace(bodies[n],"")
T=re.sub(r"(<!-- =+ [A-ZÁÉÍÓÚÑ ]+ =+ -->\s*){2,}","",T) if False else T
hdr_new=fix_links(header,False)
T=T.replace(header,hdr_new)
# enlaces en el resto del cuerpo (después del header)
k=T.index("</header>")+9
T=T[:k]+fix_links(T[k:],False) if False else T
# solo href="#…" de vistas movidas, en todo el body (excepto scripts)
def only_html(t):
    parts=re.split(r"(<script.*?</script>)",t,flags=re.S)
    return "".join(p if p.startswith("<script") else fix_links(p,False) for p in parts)
T=T[:T.index("<body")]+only_html(T[T.index("<body"):])
open("index.html","w",encoding="utf-8").write(T)
# sitemap
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join("  <url><loc>%s</loc></url>\n"%u for u in sitemap)+"</urlset>\n"
open("sitemap.xml","w",encoding="utf-8").write(sm)
