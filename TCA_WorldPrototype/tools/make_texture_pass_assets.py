"""Authored supporting surfaces: quiet value masses, direction and wear; no image edits."""
from pathlib import Path
from PIL import Image, ImageDraw
import random, math, json

DEST=Path(__file__).resolve().parents[1]/'world/maps/lanternbrook_hd2d/textures'
R=random.Random(271028)
N=256

def clamp(v):return max(0,min(255,int(v)))
def blend(a,b,t):return tuple(clamp(x*(1-t)+y*t) for x,y in zip(a,b))
def smooth_noise(x,y,seed=0):
    ix,iy=math.floor(x),math.floor(y);fx=x-ix;fy=y-iy
    fx=fx*fx*(3-2*fx);fy=fy*fy*(3-2*fy)
    def h(a,b):return (math.sin(a*127.1+b*311.7+seed*19.9)*43758.5453)%1
    return (h(ix,iy)*(1-fx)+h(ix+1,iy)*fx)*(1-fy)+(h(ix,iy+1)*(1-fx)+h(ix+1,iy+1)*fx)*fy

for name,base in [('plaster_v2',(164,155,128)),('forest_floor_v2',(63,77,53)),('path_soil_v2',(119,101,74)),('wet_silt_v2',(65,62,48))]:
    im=Image.new('RGB',(N,N));p=im.load()
    for y in range(N):
        for x in range(N):
            broad=smooth_noise(x/74,y/74,2)-.5
            medium=smooth_noise(x/19,y/19,7)-.5
            fine=smooth_noise(x/3,y/3,3)-.5
            amount=broad*16+medium*6+fine*3
            p[x,y]=tuple(clamp(c+amount) for c in base)
    d=ImageDraw.Draw(im)
    if name=='plaster_v2':
        # Broad areas stay quiet; a handful of fine branching fissures and worn flecks.
        for _ in range(9):
            x,y=R.randrange(N),R.randrange(N)
            pts=[(x,y)]
            for k in range(R.randrange(3,8)):
                x+=R.choice([-2,-1,1,2]);y+=R.randrange(2,5);pts.append((x,y))
            d.line(pts,fill=(128,126,106),width=1)
            d.line([(a+1,b) for a,b in pts],fill=(179,168,141),width=1)
        for _ in range(100):
            x,y=R.randrange(N),R.randrange(N)
            d.line((x,y,x+R.randrange(1,4),y),fill=R.choice([(153,146,122),(173,164,138)]))
    else:
        # Sparse embedded pebbles, compressed earth flakes and quiet root lines.
        for _ in range(90 if name=='path_soil_v2' else 40):
            x,y=R.randrange(N),R.randrange(N);w=R.randrange(1,5);h=R.randrange(1,3)
            c=blend(base,(138,132,103),R.uniform(.18,.48))
            d.polygon([(x,y),(x+w,y-1),(x+w+1,y+h),(x+1,y+h+1)],fill=c)
            d.line((x,y+h+1,x+w,y+h+1),fill=blend(base,(28,32,25),.25))
        if name=='forest_floor_v2':
            for _ in range(16):
                x,y=R.randrange(N),R.randrange(N)
                d.line([(x,y),(x+3,y+1),(x+6,y)],fill=(49,61,43))
    im.save(DEST/(name+'.png'))

# Slate is drawn as a mineral surface only: individual roof tiles already exist in geometry.
im=Image.new('RGB',(N,N));p=im.load()
for y in range(N):
    for x in range(N):
        strata=smooth_noise(x/48,y/7,5)-.5
        masses=smooth_noise(x/61,y/59,9)-.5
        v=strata*12+masses*18
        p[x,y]=(clamp(36+v*.65),clamp(73+v),clamp(76+v))
d=ImageDraw.Draw(im)
for _ in range(85):
    x,y=R.randrange(N),R.randrange(N);w=R.randrange(2,13)
    d.line((x,y,x+w,y+R.choice([-1,0,1])),fill=R.choice([(53,87,84),(31,63,68),(66,96,90)]))
im.save(DEST/'slate_mineral_v2.png')

# Legible slate joints and chipped lips: same palette as the mineral surface.
for y in range(0,N,32):
    for x in range(-32 if (y//32)%2 else 0,N,64):
        d.line((x,y,x+63,y),fill=(16,39,44),width=2)
        d.line((x,y,x,y+31),fill=(20,46,49),width=2)
        d.line((x+3,y+29,x+60,y+29),fill=(73,108,101),width=2)
        d.line((x+3,y+27,x+60,y+27),fill=(52,87,85))
        for k in range(4):
            xx=x+R.randrange(3,60)
            d.line((xx,y+29,xx+R.randrange(2,6),y+29),fill=(33,64,67))
im.save(DEST/'slate_mineral_v2.png')

# Original transparent litter atlas, three silhouettes in one mesh-friendly texture.
im=Image.new('RGBA',(128,128),(0,0,0,0));d=ImageDraw.Draw(im)
for _ in range(24):
    x,y=R.randrange(12,116),R.randrange(12,116)
    c=R.choice([(106,84,43,255),(128,103,58,255),(76,80,43,255),(145,119,64,255)])
    d.polygon([(x-4,y),(x-1,y-3),(x+5,y-2),(x+3,y+2),(x,y+3)],fill=c)
    d.line((x-3,y,x+4,y-1),fill=(64,61,34,255))
im.save(DEST/'leaf_litter_v2.png')
print('TEXTURE_PASS_SUPPORTING_ASSETS_SAVED',DEST)
