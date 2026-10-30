"""Original TCA environment study: Lanternbrook / 溪灯驿站. No character assets."""
import bpy, math, random, json, os
from mathutils import Vector
from pathlib import Path
random.seed(271026)
ROOT=Path(r'E:\TCA_F\TCA_WorldPrototype')
OUT=ROOT/'art'/'alchemist_hamlet'
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'build_error.txt').unlink(missing_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for data in list(bpy.data.materials):
    if data.users==0: bpy.data.materials.remove(data)
S=bpy.context.scene
S.render.engine='CYCLES'
S.cycles.samples=48
S.cycles.use_denoising=True
try:
    cp=bpy.context.preferences.addons['cycles'].preferences
    cp.compute_device_type='OPTIX'; cp.get_devices()
    for dev in cp.devices: dev.use=dev.type!='CPU'
    S.cycles.device='GPU'
except Exception: S.cycles.device='CPU'
S.render.resolution_x=1600; S.render.resolution_y=1000; S.render.resolution_percentage=100
S.render.image_settings.file_format='PNG'
S.view_settings.view_transform='AgX'
S.view_settings.look='AgX - Medium High Contrast'
S.render.film_transparent=False
S.world.color=(.15,.15,.15)
W=bpy.data.worlds.new('Blue hour ambient'); S.world=W; W.use_nodes=True
wn=W.node_tree.nodes; wn.clear(); wb=wn.new('ShaderNodeBackground'); wo=wn.new('ShaderNodeOutputWorld')
W.node_tree.links.new(wb.outputs[0],wo.inputs['Surface'])
wb.inputs[0].default_value=(.22,.34,.48,1)
wb.inputs[1].default_value=.35

def mat(name,col,rough=.75,metal=0,noise=0,emit=0):
    m=bpy.data.materials.new(name); m.diffuse_color=(*col,1); m.use_nodes=True
    n=m.node_tree.nodes; n.clear(); p=n.new('ShaderNodeBsdfPrincipled'); p.name='Principled BSDF'; output=n.new('ShaderNodeOutputMaterial')
    m.node_tree.links.new(p.outputs[0],output.inputs['Surface'])
    p.inputs['Base Color'].default_value=(*col,1); p.inputs['Roughness'].default_value=rough
    p.inputs['Metallic'].default_value=metal
    if emit:
        p.inputs['Emission Color'].default_value=(*col,1); p.inputs['Emission Strength'].default_value=emit
    if noise:
        tex=n.new('ShaderNodeTexNoise'); tex.inputs['Scale'].default_value=noise
        ramp=n.new('ShaderNodeValToRGB')
        ramp.color_ramp.elements[0].position=.2; ramp.color_ramp.elements[0].color=(*[c*.65 for c in col],1)
        ramp.color_ramp.elements[1].position=.8; ramp.color_ramp.elements[1].color=(*[min(c*1.2,1) for c in col],1)
        bump=n.new('ShaderNodeBump'); bump.inputs['Strength'].default_value=.17; bump.inputs['Distance'].default_value=.07
        m.node_tree.links.new(tex.outputs['Fac'],ramp.inputs[0]); m.node_tree.links.new(ramp.outputs[0],p.inputs['Base Color'])
        m.node_tree.links.new(tex.outputs['Fac'],bump.inputs['Height']); m.node_tree.links.new(bump.outputs[0],p.inputs['Normal'])
    return m
earth=mat('Mossy earth',(.15,.215,.115),noise=2)
soil=mat('Riverbank umber',(.16,.125,.085),noise=5)
grassm=[mat('Meadow '+str(i),c) for i,c in enumerate([(.21,.32,.13),(.31,.41,.17),(.16,.28,.15),(.38,.44,.19)])]
stone=[mat('Weathered limestone '+str(i),c,noise=6) for i,c in enumerate([(.36,.405,.36),(.43,.45,.38),(.28,.34,.32),(.49,.48,.39)])]
wall=mat('Warm lime plaster',(.66,.59,.41),noise=8)
timber=mat('Aged chestnut beams',(.16,.085,.044),noise=6)
wood=mat('Honey oak planks',(.34,.195,.086),noise=10)
roofm=[mat('Oxidised teal slate '+str(i),c,rough=.64) for i,c in enumerate([(.055,.23,.235),(.075,.29,.29),(.10,.32,.31),(.07,.20,.23),(.16,.35,.32)])]
metal=mat('Forged dark iron',(.075,.10,.105),rough=.36,metal=.7)
brass=mat('Aged brass',(.48,.29,.09),rough=.34,metal=.65)
glass=mat('Amber windows', (1,.47,.12),rough=.3,emit=2.5)
lampglass=mat('Lantern honey glow',(1,.6,.19),emit=5)
water=mat('Jade river',(.035,.24,.225),rough=.18,metal=.33)
p=water.node_tree.nodes.get('Principled BSDF'); p.inputs['Coat Weight'].default_value=.4
foam=mat('River silver glints',(.41,.70,.63),rough=.24,emit=.14)
leafm=[mat('Leaf canopy '+str(i),c) for i,c in enumerate([(.14,.265,.15),(.24,.36,.17),(.34,.43,.19),(.12,.23,.18),(.47,.49,.22)])]
bark=mat('Bark',(.19,.13,.075),noise=7)
birch=mat('Silver birch bark',(.61,.64,.52),noise=8)
flower=[mat('Flowers '+str(i),c) for i,c in enumerate([(.60,.43,.68),(.85,.64,.31),(.62,.72,.58)])]
cloth=mat('Woven saffron canopy',(.60,.34,.13),noise=25)
bottlem=[mat('Alchemy glass '+str(i),c,rough=.2,metal=.3) for i,c in enumerate([(.06,.38,.34),(.21,.35,.58),(.53,.23,.13)])]

def mesh(name,verts,faces,ma):
    d=bpy.data.meshes.new(name); d.from_pydata(verts,[],faces); d.update()
    o=bpy.data.objects.new(name,d); S.collection.objects.link(o)
    if ma: d.materials.append(ma)
    return o
def cube(name,loc,scale,ma,bev=0):
    x,y,z=[v/2 for v in scale]
    vs=[(-x,-y,-z),(-x,-y,z),(-x,y,-z),(-x,y,z),(x,-y,-z),(x,-y,z),(x,y,-z),(x,y,z)]
    o=mesh(name,vs,[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)],ma); o.location=loc
    if bev:
        b=o.modifiers.new('Soft worn edges','BEVEL'); b.width=bev; b.segments=2
        o.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
    return o
def ico(name,loc,scale,ma,sub=1):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=1,location=loc)
    o=bpy.context.object; o.name=name; o.scale=scale; o.data.materials.append(ma); return o
def cyl(name,loc,r,depth,ma,verts=12,r2=None):
    bpy.ops.mesh.primitive_cone_add(vertices=verts,radius1=r,radius2=r if r2 is None else r2,depth=depth,location=loc)
    o=bpy.context.object; o.name=name; o.data.materials.append(ma); return o
def beam(name,a,b,r,ma,verts=8):
    a,b=Vector(a),Vector(b); o=cyl(name,(a+b)/2,r,(b-a).length,ma,verts)
    o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler(); return o
def curve(name,pts,r,ma):
    d=bpy.data.curves.new(name,'CURVE'); d.dimensions='3D'; d.bevel_depth=r; d.bevel_resolution=2
    s=d.splines.new('POLY'); s.points.add(len(pts)-1)
    for p,co in zip(s.points,pts): p.co=(*co,1)
    o=bpy.data.objects.new(name,d); S.collection.objects.link(o); d.materials.append(ma); return o
def light(name,loc,power,color,r=.4,kind='POINT',target=None,size=5):
    d=bpy.data.lights.new(name,kind); d.energy=power; d.color=color; d.shadow_soft_size=r
    o=bpy.data.objects.new(name,d); S.collection.objects.link(o); o.location=loc
    if kind=='AREA': d.shape='DISK'; d.size=size
    if target: o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    return o
def riverx(y): return -3+.11*y+.55*math.sin(y*.26)
def h(x,y):
    d=abs(x-riverx(y)); und=.10*math.sin(x*.6+y*.2)+.08*math.cos(y*.8-x*.2)
    return -.58+min(1,max(0,(d-1.12)/1.2))*(1.01+und)

# Continuous, sculpted terrain. Broad enough for a game camera, with a true recessed riverbed.
verts=[]; faces=[]; nx,ny=110,140
for j in range(ny+1):
    y=-21+j*.4
    for i in range(nx+1):
        x=-22+i*.4; verts.append((x,y,h(x,y)))
for j in range(ny):
    for i in range(nx):
        a=j*(nx+1)+i; faces.append((a,a+1,a+nx+2,a+nx+1))
terrain=mesh('ENV_Terrain_sculpted_riverbanks',verts,faces,earth)
for p in terrain.data.polygons: p.use_smooth=True
verts=[]; faces=[]
for j in range(231):
    y=-21+j*.24; x=riverx(y)
    verts.extend([(x-1.34,y,-.23),(x+1.34,y,-.23)])
    if j: a=j*2; faces.append((a-2,a,a+1,a-1))
mesh('ENV_Jade_water',verts,faces,water)
for i in range(230):
    y=random.uniform(-19,26); x=riverx(y)+random.uniform(-1.15,1.15); ln=random.uniform(.10,.6)
    curve('Water_current_glint',[(x-ln/2,y,-.207),(x,y+.02,-.204),(x+ln/2,y,-.207)],random.uniform(.006,.018),foam)
# Bank boulders and moss crowns.
for side in [-1,1]:
    for k in range(78):
        y=-19+k*.55+random.uniform(-.25,.25); x=riverx(y)+side*random.uniform(1.25,1.85)
        sc=(random.uniform(.2,.55),random.uniform(.25,.65),random.uniform(.18,.48))
        ico('Riverbank_moss_stone',(x,y,h(x,y)+.03),sc,random.choice(stone),1)
        if k%3==0: ico('Moss_on_bank',(x,y,h(x,y)+sc[2]*.65),(sc[0]*.8,sc[1]*.8,.085),grassm[2],1)

# Stepping cobbles: the open route runs from the foreground through the bridge to the inn.
def path(points,width):
    for a,b in zip(points,points[1:]):
        a,b=Vector(a),Vector(b); steps=max(1,int((b-a).length/.4))
        for k in range(steps):
            p=a.lerp(b,k/steps); tangent=(b-a).normalized(); perp=Vector((-tangent.y,tangent.x))
            for j in range(-int(width/.44),int(width/.44)+1):
                pos=p+perp*(j*.40+random.uniform(-.06,.06)); x,y=pos
                if abs(x-riverx(y))<1.7: continue
                o=cube('Route_worn_cobble',(x,y,h(x,y)+.025),(random.uniform(.30,.42),random.uniform(.29,.39),.065),random.choice(stone),.045)
                o.rotation_euler[2]=random.uniform(-.17,.17)
path([(-11,-12),(-8,-7),(-6.3,-3),(-5.2,-1.8)],.8)
path([(-.9,-1.8),(1,-2.2),(3,-1.3),(4,1),(6.5,6),(9,12),(12,20)],.85)
path([(1,-2.2),(4,-5),(8,-7),(13,-10)],.65)

# Stone bridge, elliptical open arch with radial voussoirs, curved walking deck and low parapets.
BX=riverx(-1.8); BY=-1.8; span=4.9
def bridgez(x): return .50+.70*max(0,math.cos((x-BX)/span*math.pi))
for j in range(18):
    x=BX-span/2+(j+.5)*span/18
    o=cube('Bridge_deck_paving',(x,BY,bridgez(x)),(span/18+.025,2.0,.22),random.choice(stone),.045)
    o.rotation_euler[1]=math.atan(.7*math.pi/span*math.sin((x-BX)/span*math.pi))
for side in [-1,1]:
    y=BY+side*1.02
    for k in range(17):
        t0=math.pi*k/17; t1=math.pi*(k+1)/17; vs=[]
        for yy in [y-.21,y+.21]:
            for rx,rz in [(2.2,1.05),(2.2,.0)]: pass
            vs.extend([(BX+2.24*math.cos(t0),yy,-.18+1.13*math.sin(t0)),(BX+2.24*math.cos(t1),yy,-.18+1.13*math.sin(t1)),(BX+2.53*math.cos(t1),yy,-.18+1.47*math.sin(t1)),(BX+2.53*math.cos(t0),yy,-.18+1.47*math.sin(t0))])
        mesh('Bridge_radial_arch_stone',vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],random.choice(stone))
    for j in range(15):
        x=BX-span/2+(j+.5)*span/15
        cube('Bridge_parapet',(x,y,bridgez(x)+.39),(.33,.39,.5),random.choice(stone),.055)
        cube('Bridge_capstone',(x,y,bridgez(x)+.68),(.35,.47,.13),stone[1],.04)

# Main inn: plaster, exposed timbers, hand-laid slate and a steep fairytale gable.
HX,HY=3.2,3.0; base=.50; width=5.1; depth=4.2; eave=4.7; ridge=7.65
cube('INN_Stone_foundation',(HX,HY,.72),(5.45,4.55,.55),stone[2],.12)
cube('INN_Limewashed_walls',(HX,HY,2.85),(width,depth,4.0),wall,.07)
for yy in [HY-depth/2,HY+depth/2]:
    mesh('INN_Plaster_gable',[(HX-width/2,yy,eave),(HX+width/2,yy,eave),(HX,yy,ridge)],[(0,1,2)],wall)
for xx in [HX-width/2-.04,HX+width/2+.04]:
    for yy in [HY-depth/2-.04,HY+depth/2+.04]: cube('INN_Corner_post',(xx,yy,2.75),(.22,.22,4.2),timber,.035)
for z in [1.05,3.15,4.63]:
    cube('INN_Front_crossbeam',(HX,HY-depth/2-.08,z),(width+.3,.19,.18),timber,.025)
    for xx in [HX-width/2-.08,HX+width/2+.08]: cube('INN_Side_crossbeam',(xx,HY,z),(.19,depth,.18),timber,.025)
for xx in [HX-1.35,HX,HX+1.35]: cube('INN_Facade_stud',(xx,HY-depth/2-.1,3.85),(.14,.16,1.5),timber,.02)
beam('Gable_left_beam',(HX-width/2-.2,HY-depth/2-.15,eave),(HX,HY-depth/2-.15,ridge),.11,timber)
beam('Gable_right_beam',(HX,HY-depth/2-.15,ridge),(HX+width/2+.2,HY-depth/2-.15,eave),.11,timber)
beam('Gable_kingpost',(HX,HY-depth/2-.15,4.65),(HX,HY-depth/2-.15,7.56),.10,timber)
# Handbuilt slate tessellation, grouped as two meshes for practical export.
for side in [-1,1]:
    vs=[]; fs=[]; mi=[]
    rows=15; cols=17
    for row in range(rows):
        t=row/rows; t2=min(1,(row+1.25)/rows)
        def rz(t): return ridge-(ridge-eave)*t+.2*math.sin(t*math.pi)-.13*t*t
        for col in range(cols):
            y0=HY-depth/2-.48+(col+(row%2)*.5)*(depth+.96)/cols
            y1=y0+(depth+.96)/cols*.94
            x0=HX+side*t*(width/2+.55); x1=HX+side*t2*(width/2+.55)
            z0=rz(t)+random.uniform(-.018,.018); z1=rz(t2)
            a=len(vs); thick=.065
            vs.extend([(x0,y0,z0),(x0,y1,z0),(x1,y1,z1),(x1,y0,z1),(x0,y0,z0-thick),(x0,y1,z0-thick),(x1,y1,z1-thick),(x1,y0,z1-thick)])
            fs.extend([tuple(a+i for i in f) for f in [(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]])
            mi.extend([random.randrange(len(roofm))]*6)
    o=mesh('INN_Handlaid_slate_roof_'+str(side),vs,fs,None)
    for m in roofm:o.data.materials.append(m)
    for p,idx in zip(o.data.polygons,mi):p.material_index=idx
for yy in [HY-depth/2-.50,HY+depth/2+.50]:
    for side in [-1,1]: curve('INN_Carved_bargeboard',[(HX+side*t*(width/2+.58),yy,ridge-(ridge-eave)*t+.2*math.sin(t*math.pi)-.13*t*t) for t in [i/20 for i in range(21)]],.11,timber)
curve('INN_Ridge_cap',[(HX,HY-depth/2-.64,ridge+.08),(HX,HY+depth/2+.64,ridge+.08)],.14,roofm[3])
# Chimney with copper cap and decorative bands.
cube('INN_Chimney',(HX+1.35,HY+1.15,7.0),(.75,.7,3.0),stone[2],.06)
for z in [6.5,7.1,7.7,8.25]: cube('Chimney_stone_course',(HX+1.35,HY+1.15,z),(.86,.81,.16),stone[1],.035)
cube('Chimney_dark_flue',(HX+1.35,HY+1.15,8.45),(.51,.48,.18),metal,.02)
cube('Chimney_cap',(HX+1.35,HY+1.15,8.65),(.99,.94,.16),stone[1],.05)

def window(x,y,z,w=1.0,ht=1.35):
    cube('Window_deep_reveal',(x,y,z),(w+.20,.15,ht+.20),timber,.05)
    cube('Window_amber_panes',(x,y-.09,z),(w,.035,ht),glass,.025)
    for xx in [x-w/2,x,x+w/2]:cube('Window_mullion',(xx,y-.135,z),(.055,.07,ht+.04),wood,.012)
    for zz in [z-ht/2,z+ht/2,z+.14]:cube('Window_transom',(x,y-.14,zz),(w+.10,.08,.055),wood,.012)
    cube('Window_stone_sill',(x,y-.20,z-ht/2-.08),(w+.40,.4,.14),stone[1],.035)
    for side in [-1,1]:
        cube('Window_louvred_shutter',(x+side*(w/2+.23),y-.06,z),(.30,.10,ht),roofm[0],.025)
        for k in range(6):cube('Shutter_slat',(x+side*(w/2+.23),y-.13,z-ht/2+.12+k*ht/6),(.32,.06,.06),roofm[2],.015)
FY=HY-depth/2-.13
window(HX-1.4,FY,2.05,.85,1.25); window(HX+1.45,FY,2.05,.85,1.25)
window(HX-.72,FY,3.95,.78,.95); window(HX+.72,FY,3.95,.78,.95)
window(HX,FY-.02,5.75,.85,1.1)
# Heavy door with inset panels, lintel and brass handle.
cube('INN_Door_frame',(HX,FY-.03,1.75),(1.26,.25,2.40),timber,.06)
cube('INN_Oak_door',(HX,FY-.19,1.72),(1.02,.12,2.15),wood,.04)
for xx in [HX-.33,HX,HX+.33]:cube('Door_plank_joint',(xx,FY-.26,1.72),(.018,.015,2.03),timber)
for z in [1.0,2.34]:cube('Door_iron_strap',(HX,FY-.28,z),(.97,.055,.08),metal,.02)
ico('Door_brass_knob',(HX+.33,FY-.36,1.65),(.065,.045,.065),brass,2)
for k in range(3):cube('INN_Entrance_step',(HX,FY-.40-k*.30,.58-k*.035),(1.65,.46,.18),stone[1],.05)
# Porch lean-to, slender posts, hanging flower baskets.
for xx in [HX-2.40,HX+2.40]:
    cube('Porch_support',(xx,FY-1.32,1.85),(.15,.15,2.80),timber,.025)
    beam('Porch_bracket',(xx,FY-1.32,2.35),(xx,FY-.70,3.06),.06,wood)
for i in range(18):
    xx=HX-2.7+i*.30
    o=cube('Porch_slate',(xx,FY-.74,3.03),(.31,1.7,.12),roofm[i%5],.025); o.rotation_euler[0]=.17
cube('Porch_front_beam',(HX,FY-1.57,2.90),(5.6,.16,.20),timber,.03)

def lantern(x,y,z,post=False):
    if post:
        cube('Lantern_post',(x,y,(z+.1)/2),(.15,.15,z+.1),timber,.03)
        beam('Lantern_hook',(x,y,z+.1),(x+.42,y,z+.1),.045,metal)
        x+=.42; z-=.30
    cube('Lantern_glass',(x,y,z),(.25,.25,.40),lampglass,.025)
    for dx in [-.145,.145]:
        for dy in [-.145,.145]:beam('Lantern_iron_frame',(x+dx,y+dy,z-.24),(x+dx,y+dy,z+.24),.018,metal)
    for zz in [z-.26,z+.26]:cube('Lantern_rim',(x,y,zz),(.35,.35,.065),metal,.025)
    cyl('Lantern_pyramidal_cap',(x,y,z+.38),.28,.21,metal,4,.03)
    light('Lantern_warm_pool',(x,y-.15,z),60,(1,.48,.16),.35)
lantern(HX-1.0,FY-.55,2.44); lantern(HX+2.4,FY-1.5,2.40)
lantern(BX-2.75,BY+.9,2.6,True); lantern(BX+2.6,BY+.9,2.6,True)
lantern(7.5,-4.3,2.4,True); lantern(-8.5,-5.0,2.2,True)
# Hanging sign, alchemical emblem rather than text.
beam('Sign_bracket',(HX+2.65,FY,3.9),(HX+3.7,FY-.15,3.9),.055,metal)
for x in [HX+3.0,HX+3.5]:beam('Sign_chain',(x,FY-.15,3.9),(x,FY-.15,3.4),.018,metal)
cube('INN_Hanging_sign',(HX+3.25,FY-.15,3.07),(.94,.14,.66),timber,.13)
curve('Sign_alchemy_triangle',[(HX+3.03,FY-.24,2.88),(HX+3.25,FY-.24,3.30),(HX+3.47,FY-.24,2.88),(HX+3.03,FY-.24,2.88)],.023,brass)
curve('Sign_alchemy_cross',[(HX+3.07,FY-.25,3.03),(HX+3.43,FY-.25,3.03)],.016,brass)

# Outdoor apothecary work area, side market, barrels, produce and glassware.
def barrel(x,y,z=.5,scale=1):
    cyl('Oak_barrel',(x,y,z+.43*scale),.36*scale,.80*scale,wood,14,.31*scale)
    for zz in [.10,.25,.65,.80]:
        bpy.ops.mesh.primitive_torus_add(major_segments=16,minor_segments=4,location=(x,y,z+zz*scale),major_radius=.345*scale,minor_radius=.025*scale)
        bpy.context.object.name='Barrel_iron_hoop'; bpy.context.object.data.materials.append(metal)
    cyl('Barrel_lid',(x,y,z+.85*scale),.32*scale,.035,wood,14)
def crate(x,y,z=.5):
    cube('Crate_dark_interior',(x,y,z+.3),(.66,.58,.55),timber,.02)
    for dz in [.08,.25,.43]:
        for dy in [-.32,.32]:cube('Crate_slats',(x,y+dy,z+dz),(.76,.06,.12),wood,.015)
        for dx in [-.36,.36]:cube('Crate_slats',(x+dx,y,z+dz),(.06,.65,.12),wood,.015)
    for dx in [-.3,.3]:
        for dy in [-.26,.26]:cube('Crate_corner',(x+dx,y+dy,z+.28),(.07,.07,.62),wood,.015)
barrel(6.3,1.8); barrel(6.8,2.4,scale=.8); crate(6.1,.25); crate(6.7,.1); crate(6.3,.25,1.12)
cube('Apothecary_table',(6.85,3.65,1.44),(2.1,.85,.13),wood,.04)
for xx in [6.0,7.7]:
    for yy in [3.35,3.95]:cube('Table_leg',(xx,yy,.97),(.09,.09,.95),timber,.02)
for i in range(10):
    x=random.uniform(6.0,7.65); y=random.uniform(3.35,3.95); z=1.52
    cyl('Apothecary_bottle',(x,y,z+.13),.07,.25,bottlem[i%3],10,.08)
    cyl('Bottle_neck',(x,y,z+.30),.035,.12,bottlem[i%3],10)
    cyl('Bottle_cork',(x,y,z+.37),.038,.035,wood,8)
for x,y in [(1.0,.1),(5.5,.1),(6.5,5.8)]:
    cyl('Terracotta_planter',(x,y,.77),.27,.55,cloth,12,.36)
    for k in range(7):
        a=random.random()*6.28; rr=random.random()*.28
        beam('Planter_stem',(x,y,1.01),(x+rr*math.cos(a),y+rr*math.sin(a),1.55),.013,grassm[2])
        ico('Planter_flower',(x+rr*math.cos(a),y+rr*math.sin(a),1.55),(.09,.09,.06),flower[k%3],1)
# Lean-to cloth canopy next to the table.
for x in [5.8,8.1]:cube('Stall_pole',(x,3.15,1.9),(.1,.1,2.8),wood,.02)
mesh('Saffron_market_canopy',[(5.6,3,3.15),(8.3,3,3.15),(8.3,4.7,3.50),(5.6,4.7,3.50),(6.95,3,2.97),(6.95,4.7,3.35)],[(0,4,5,3),(4,1,2,5)],cloth)
for k in range(10):
    x=5.6+k*.27; mesh('Canopy_scalloped_trim',[(x,3,3.15),(x+.27,3,3.15),(x+.23,3,2.96),(x+.06,3,2.96)],[(0,1,2,3)],cloth)

# Split-rail fencing follows the path, leaving natural entries.
def fence(points):
    for x,y in points:
        z=h(x,y); cube('Fence_post',(x,y,z+.58),(.13,.13,1.2),wood,.035)
        cyl('Fence_post_cap',(x,y,z+1.21),.12,.17,timber,4,.02)
    for a,b in zip(points,points[1:]):
        for ht in [.42,.89]:beam('Fence_rail',(*a,h(*a)+ht),(*b,h(*b)+ht),.055,wood,6)
fence([(-10,-3),(-9,-1.5),(-8,0),(-7.2,1.5)])
fence([(8.0,-5.7),(9.7,-4.8),(11.2,-3.7),(12.1,-2)])
fence([(7.5,8),(8.6,10),(9.8,12),(11,14)])

# Trees with branching silhouettes and clustered, asymmetric foliage.
def tree(x,y,size=1,typ='broad'):
    z=h(x,y); ht=random.uniform(4.3,5.6)*size; ma=birch if typ=='birch' else bark
    o=cyl('TREE_Trunk',(x,y,z+ht*.43),.17*size,ht*.86,ma,9,.065*size)
    if typ=='pine':
        for j in range(4):
            zz=z+ht*(.39+j*.17); r=(1.7-j*.30)*size
            cyl('TREE_Layered_fir',(x,y,zz),r,ht*.42,leafm[(j+1)%4],9,.03)
        return
    for k in range(7):
        a=k*2.4+random.random()*.4; rr=random.uniform(.45,1.3)*size
        end=(x+math.cos(a)*rr,y+math.sin(a)*rr,z+ht*random.uniform(.68,1.02))
        beam('TREE_Branch',(x,y,z+ht*.48),end,.065*size,ma)
        ico('TREE_Foliage_cluster',end,(random.uniform(.9,1.35)*size,random.uniform(.8,1.2)*size,random.uniform(.8,1.25)*size),random.choice(leafm),2)
    if typ=='birch':
        for j in range(9):
            cube('Birch_bark_mark',(x,y-.17*size,z+.3+j*ht*.075),(.18*size,.018,.045*size),bark,.01)
for x,y,s,t in [(-9,3,1.2,'broad'),(-10,8,1.3,'pine'),(-7,9,1.1,'birch'),(-6,14,1.3,'pine'),(-10,16,1.7,'pine'),(1,12,1.2,'broad'),(7,11,1.1,'birch'),(11,5,1.1,'broad'),(13,1,1.2,'pine'),(11,-2,.95,'birch'),(10,-10,1.35,'broad'),(-12,-7,1.25,'broad'),(-9,-11,.95,'birch'),(-14,1,1.6,'pine'),(13,14,1.6,'pine'),(4,18,1.5,'pine'),(-12,22,1.9,'pine')]:tree(x,y,s,t)

# Background escarpment, stepped rocks and distant layered conifer forest.
for k in range(29):
    x=-22+k*1.7; y=19+random.uniform(-1,5); z=h(x,y)
    sc=(random.uniform(1.4,2.7),random.uniform(2,3.5),random.uniform(2.2,4.8))
    ico('CLIFF_Background_outcrop',(x,y,z+sc[2]*.48),sc,stone[k%3],1)
    if k%2==0:tree(x,y+3,random.uniform(1.5,2.1),'pine')
for k in range(20):
    x=random.uniform(-16,16); y=random.uniform(-12,16)
    if abs(x-riverx(y))<2.2 or (abs(x-HX)<4.8 and abs(y-HY)<4.0):continue
    ico('Meadow_boulder',(x,y,h(x,y)+.15),(random.uniform(.3,.8),random.uniform(.35,.8),random.uniform(.3,.7)),random.choice(stone),1)

# Batched vegetation geometry: tens of thousands of blades, not thousands of draw calls.
gv=[]; gf=[]; gi=[]; fv=[]; ff=[]; fi=[]
def ispath(x,y):
    if -7<y<13 and abs(x-(3.5+.47*y))<1.4:return True
    if -13<y<-1 and abs(x-(-5.8+.47*(y+2)))<1.25:return True
    if -10<y<-2 and abs(x-(-.6-1.25*y))<1.0:return True
    return False
for k in range(10000):
    x=random.uniform(-17,17); y=random.uniform(-16,24)
    if abs(x-riverx(y))<1.75 or ispath(x,y) or (abs(x-HX)<3.3 and abs(y-HY)<3.05) or (5.4<x<8.8 and 2<y<5.5):continue
    z=h(x,y); tall=random.uniform(.13,.43)
    for j in range(3):
        a=random.random()*6.28; w=random.uniform(.035,.075); lean=random.uniform(.03,.15)
        v=len(gv); dx,dy=math.cos(a)*w,math.sin(a)*w
        gv.extend([(x-dx,y-dy,z),(x+dx,y+dy,z),(x+math.sin(a)*lean,y+math.cos(a)*lean,z+tall)])
        gf.append((v,v+1,v+2)); gi.append(random.randrange(4))
    if k%13==0:
        fh=tall+.09
        for j in range(3):
            a=j*2.094; xx=x+math.cos(a)*.06; yy=y+math.sin(a)*.06; v=len(fv)
            fv.extend([(xx-.045,yy,z+fh),(xx,yy-.045,z+fh+.03),(xx+.045,yy,z+fh),(xx,yy+.045,z+fh+.03)])
            ff.append((v,v+1,v+2,v+3));fi.append(k%3)
o=mesh('ENV_Meadow_grass_batched',gv,gf,None)
for m in grassm:o.data.materials.append(m)
for p,idx in zip(o.data.polygons,gi):p.material_index=idx
o=mesh('ENV_Wildflowers_batched',fv,ff,None)
for m in flower:o.data.materials.append(m)
for p,idx in zip(o.data.polygons,fi):p.material_index=idx
# Large reeds and lilies along the water, with visible shaped leaves.
for k in range(95):
    y=random.uniform(-15,17); side=random.choice([-1,1]); x=riverx(y)+side*random.uniform(1.3,1.65); z=h(x,y)
    for j in range(4):
        a=random.random()*6.28; ln=random.uniform(.4,.85); dx,dy=math.cos(a)*ln*.35,math.sin(a)*ln*.35
        mesh('River_reed_leaf',[(x,y,z),(x+dx-.035,y+dy,z+ln*.6),(x+dx,y+dy,z+ln),(x+dx+.035,y+dy,z+ln*.6)],[(0,1,2,3)],leafm[j%3])
for k in range(18):
    y=random.uniform(-12,12); x=riverx(y)+random.choice([-1,1])*random.uniform(.6,1.0)
    o=cyl('Water_lily_pad',(x,y,-.195),random.uniform(.10,.21),.018,leafm[1],12)
    if k%4==0:ico('Water_lily_blossom',(x,y,-.14),(.09,.09,.07),flower[0],2)

# Amber specks near riverbank: restrained fairy-tale environmental accent.
firemat=mat('Firefly_gold',(1,.62,.15),emit=7)
for k in range(38):
    y=random.uniform(-8,9); x=riverx(y)+random.uniform(-2.6,2.6)
    ico('Firefly',(x,y,random.uniform(.25,1.8)),(.015,.015,.015),firemat,1)

# Lighting: late amber sun from camera-left, cool skylight, local warm pools.
sun=light('SUN_Last_light',(-12,-8,16),2.6,(1,.73,.43),kind='SUN',target=(0,3,0)); sun.data.angle=math.radians(8)
light('SKY_Large_cool_fill',(1,4,17),1900,(.48,.68,1),kind='AREA',target=(2,1,0),size=18)
light('INN_Window_spill',(HX,FY-1.1,2.9),140,(1,.46,.13),kind='AREA',target=(HX,FY-3,0),size=3)
light('RIM_Distant_glade',(-4,14,10),1400,(.65,.79,1),kind='AREA',target=(0,0,2),size=10)
# A subtle height-independent mist volume, isolated as optional atmosphere.
fogmat=bpy.data.materials.new('Atmospheric blue haze'); fogmat.use_nodes=True
n=fogmat.node_tree.nodes; n.clear(); out=n.new('ShaderNodeOutputMaterial'); vol=n.new('ShaderNodeVolumePrincipled')
vol.inputs['Density'].default_value=.006; vol.inputs['Color'].default_value=(.48,.62,.67,1); vol.inputs['Anisotropy'].default_value=.25
fogmat.node_tree.links.new(vol.outputs['Volume'],out.inputs['Volume'])
cube('ATMOSPHERE_Optional_mist',(0,7,7),(60,70,22),fogmat)

camd=bpy.data.cameras.new('CAM_HD2D_Hero'); cam=bpy.data.objects.new('CAM_HD2D_Hero',camd); S.collection.objects.link(cam)
cam.location=(21,-30,23); target=Vector((.5,3,1.5)); cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
camd.type='ORTHO'; camd.ortho_scale=29.5; camd.lens=48; S.camera=cam
focus=bpy.data.objects.new('Camera_focus_inn_and_bridge',None); S.collection.objects.link(focus); focus.location=(1,1,1.7)
camd.dof.use_dof=True; camd.dof.focus_object=focus; camd.dof.aperture_fstop=8
S['art_direction']='Lanternbrook: original HD-2D environment study; characters intentionally excluded.'
S['authoring_seed']=271026
S['source_assets']='All geometry and materials authored procedurally for this project. No external asset dependency.'
# Useful Blender landing view.
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            area.spaces.active.region_3d.view_perspective='CAMERA'
            area.spaces.active.shading.type='MATERIAL'
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Lanternbrook_HD2D.blend'))
stats={'objects':len(S.objects),'mesh_objects':sum(o.type=='MESH' for o in S.objects),'polygons':sum(len(o.data.polygons) for o in S.objects if o.type=='MESH'),'blend':str(OUT/'Lanternbrook_HD2D.blend')}
(OUT/'build_stats.json').write_text(json.dumps(stats,indent=2),encoding='utf8')
print(json.dumps(stats),flush=True)
S.render.filepath=str(OUT/'renders'/'Lanternbrook_preview_v01.png')
bpy.ops.render.render(write_still=True)
print('RENDER_COMPLETE',flush=True)
