"""Original, deterministic pixel surfaces. No screen-space pixel filter."""
from pathlib import Path
import random, json
from PIL import Image, ImageDraw

DEST = Path(__file__).resolve().parents[1] / 'world/maps/lanternbrook_hd2d/textures'
DEST.mkdir(parents=True, exist_ok=True)
r = random.Random(271027)

def surface(name, colors, kind):
    im = Image.new('RGB', (64, 64), colors[1]); d = ImageDraw.Draw(im)
    # Compact groups of pixels rather than full-frame photographic noise.
    for _ in range(95 if kind == 'plaster' else 190):
        x,y = r.randrange(64),r.randrange(64)
        w,h = r.choice([(2,1),(3,2),(1,1),(4,1)])
        d.rectangle((x,y,x+w,y+h), fill=r.choice(colors))
    if kind == 'wood':
        for y in range(0,64,16):
            d.line((0,y,63,y), fill=colors[0]); d.line((0,y+1,63,y+1),fill=colors[2])
            for _ in range(9):
                x=r.randrange(64); yy=y+r.randrange(3,15)
                d.line((x,yy,min(63,x+r.randrange(4,18)),yy),fill=r.choice([colors[0],colors[3]]))
        for x,y in [(12,9),(43,37),(24,55)]:
            d.ellipse((x-3,y-1,x+3,y+2),outline=colors[0]);d.point((x,y),fill=colors[2])
    elif kind == 'stone':
        # Individual masonry blocks already exist in the geometry; no second grid.
        for _ in range(12):
            x,y=r.randrange(64),r.randrange(64)
            d.line((x,y,x+3,y+1,x+5,y+1),fill=colors[3])
        for _ in range(9):
            x,y=r.randrange(64),r.randrange(64)
            d.rectangle((x,y,x+3,y+2),fill=(112,126,94))
    elif kind == 'slate':
        for y in range(0,64,16):
            for x in range(-8 if y%32 else 0,64,16):
                d.line((x,y,x,y+15),fill=colors[0]);d.line((x,y+15,x+15,y+15),fill=colors[0])
                d.line((x+2,y+2,x+12,y+2),fill=colors[2])
                for _ in range(5):
                    xx=x+r.randrange(2,14);yy=y+r.randrange(3,14)
                    d.line((xx,yy,xx+2,yy),fill=colors[3])
    elif kind == 'plaster':
        for _ in range(16):
            x,y=r.randrange(64),r.randrange(64)
            d.line((x,y,x+2,y+3,x+1,y+6),fill=colors[3])
    elif kind == 'earth':
        for _ in range(85):
            x,y=r.randrange(64),r.randrange(64)
            d.line((x,y,x+2,y-1,x+4,y),fill=r.choice(colors[2:]))
    im.save(DEST/(name+'.png'))

surface('chestnut',[(49,38,33),(92,64,45),(133,95,61),(72,49,38)],'wood')
surface('oak',[(78,56,41),(139,105,67),(178,141,91),(113,79,51)],'wood')
surface('bark',[(36,39,35),(67,66,45),(97,91,58),(48,52,39)],'wood')
surface('slate',[(23,50,57),(42,83,86),(72,116,111),(47,95,91)],'slate')
surface('limestone',[(113,119,104),(133,136,116),(153,153,128),(120,128,108)],'stone')
surface('plaster',[(172,161,130),(184,173,140),(194,183,148),(167,158,128)],'plaster')
surface('earth',[(37,53,43),(58,76,48),(83,96,57),(47,65,43)],'earth')
surface('path',[(94,82,60),(139,121,86),(164,143,104),(117,104,74)],'earth')
surface('canvas',[(116,76,42),(171,122,63),(197,150,85),(147,100,51)],'plaster')

# Grass and moss stamps use native alpha, authored as pixel clusters.
for name,palette in [('grass',[(39,63,47),(66,88,48),(105,119,65),(143,144,83)]),
                     ('moss',[(36,57,45),(53,76,47),(80,98,54),(112,118,67)])]:
    im=Image.new('RGBA',(64,64),(0,0,0,0));d=ImageDraw.Draw(im)
    for _ in range(110):
        x,y=r.randrange(4,60),r.randrange(5,59)
        if ((x-32)/29)**2+((y-32)/25)**2>r.uniform(.45,1):continue
        c=palette[r.randrange(4)]+(255,)
        if name=='grass':
            d.line((x,y,x-1,y-r.randrange(2,6)),fill=c,width=1)
            d.line((x,y,x+2,y-2),fill=c)
        else:d.rectangle((x,y,x+r.randrange(2,6),y+r.randrange(1,4)),fill=c)
    im.save(DEST/(name+'.png'))

(DEST/'surface_manifest.json').write_text(json.dumps({'source':'Original deterministic pixel drawing','seed':271027,'size':64,'textures':[p.name for p in DEST.glob('*.png')]},indent=2),encoding='utf8')
print(DEST)
