from PIL import Image, ImageDraw
from pathlib import Path
import random
OUT=Path(__file__).resolve().parents[1]/'world/maps/lanternbrook_hd2d/textures'
r=random.Random(7427)
for kind in ['fern','reeds','blueflowers']:
    im=Image.new('RGBA',(64,64),(0,0,0,0));d=ImageDraw.Draw(im)
    if kind=='fern':
        for direction in [-1,1]:
            for slope in [.28,.55,.95]:
                end=(32+int(direction*24*slope),30-int(20*(1-slope)))
                d.line((32,58,*end),fill=(89,118,67,255),width=1)
                for j in range(2,9):
                    t=j/10;x=int(32+(end[0]-32)*t);y=int(58+(end[1]-58)*t);ln=int(9*(1-t))+1
                    for side in [-1,1]:
                        d.line((x,y,x+side*ln,y-3),fill=(105,133,77,255) if side<0 else (62,94,57,255),width=2)
    elif kind=='reeds':
        for i in range(11):
            x=r.randrange(17,46);top=r.randrange(10,35);tilt=r.randrange(-9,10)
            d.line((x,61,x+tilt,top),fill=r.choice([(93,115,64,255),(63,91,61,255),(123,134,75,255)]))
            if i%3==0:d.rectangle((x+tilt-1,top-5,x+tilt+1,top+4),fill=(118,96,59,255))
    else:
        for x,y in [(15,35),(29,21),(44,30),(35,44),(20,48)]:
            d.line((x,60,x,y),fill=(63,100,65,255))
            d.line((x,y+12,x+6,y+6),fill=(87,119,70,255),width=2)
            for dx,dy in [(-3,0),(3,0),(0,-3),(0,3)]:d.rectangle((x+dx-1,y+dy-1,x+dx+1,y+dy+1),fill=(144,178,187,255))
            d.point((x,y),fill=(217,197,134,255))
    im.save(OUT/(kind+'.png'))
print('Woodland detail sprites saved')
