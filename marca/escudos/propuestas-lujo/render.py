import glob, os
from playwright.sync_api import sync_playwright
from PIL import Image
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--allow-file-access-from-files'])
    pg=b.new_page(viewport={'width':1200,'height':1400},device_scale_factor=2)
    for f in sorted(glob.glob('/home/claude/escudos6/[0-9]-*.html')):
        pg.goto('file://'+f); pg.wait_for_timeout(700)
        out=f.replace('.html','.png')
        pg.screenshot(path=out,omit_background=True)
        im=Image.open(out); im=im.crop(im.getbbox()); im.save(out); print(out,im.size)
    b.close()
# contact sheet
fs=sorted(glob.glob('/home/claude/escudos6/[0-9]-*.png'))
th=[Image.open(f) for f in fs]
W=600;H=620
sheet=Image.new('RGB',(W*3,H*2+80),(13,13,13))
from PIL import ImageDraw, ImageFont
dr=ImageDraw.Draw(sheet); fnt=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',24)
names=['1 · MODENA','2 · STUTTGART',"3 · SANT'AGATA",'4 · MOLSHEIM','5 · GAYDON','6 · HERÁLDICO']
for i,t in enumerate(th):
    t=t.copy(); t.thumbnail((W-60,H-60),Image.LANCZOS)
    x=(i%3)*W+(W-t.width)//2; y=(i//3)*(H+40)+(H-40-t.height)//2
    dr.text(((i%3)*W+W//2,(i//3)*(H+40)+H-10),names[i],fill=(255,213,31),font=fnt,anchor='mm')
    sheet.paste(t,(x,y),t)
sheet.save('/home/claude/escudos6/hoja.png')
