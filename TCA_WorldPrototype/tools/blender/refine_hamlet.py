import bpy, ast, math, random, json
from mathutils import Vector
from pathlib import Path
ROOT=Path(r'E:\TCA_F\TCA_WorldPrototype'); OUT=ROOT/'art'/'alchemist_hamlet'; S=bpy.context.scene
random.seed(8876)
# Reuse the authoring primitives without rerunning the build.
source=ast.parse((ROOT/'tools'/'blender'/'build_hamlet.py').read_text(encoding='utf8'))
exec(compile(ast.Module(body=[n for n in source.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),'primitives','exec'),globals())
def get(n):return bpy.data.materials[n]
earth=get('Mossy earth'); wood=get('Honey oak planks'); timber=get('Aged chestnut beams'); metal=get('Forged dark iron'); brass=get('Aged brass'); glass=get('Amber windows'); bark=get('Bark')
leafm=[get('Leaf canopy '+str(i)) for i in range(5)]; grassm=[get('Meadow '+str(i)) for i in range(4)]; stone=[get('Weathered limestone '+str(i)) for i in range(4)]
roofm=[get('Oxidised teal slate '+str(i)) for i in range(5)]; flower=[get('Flowers '+str(i)) for i in range(3)]
HX,HY=3.2,3; FY=.77
# Move the foreground tree that blocked the entrance into the right framing edge.
for o in list(S.objects):
    if o.name.startswith(('TREE','Birch')) and 7.7<o.location.x<12.1 and -12.1<o.location.y<-7.7:
        o.location.x+=4.8; o.location.y-=1.0
# Smaller tree shapes in the middle ground, to give the inn breathing room.
for o in list(S.objects):
    if o.name.startswith('TREE_Layered_fir') and o.location.x>10 and o.location.y<6:
        o.scale.x*=.78;o.scale.y*=.78

# Break up the large faceted canopy balls with a fine, irregular leafy silhouette.
unit=next(o.data for o in S.objects if o.name.startswith('TREE_Foliage_cluster'))
uverts=[Vector(v.co).normalized() for v in unit.vertices]
ufaces=[tuple(p.vertices) for p in unit.polygons]
leaf_batches=[([],[]) for _ in range(5)]
canopies=[o for o in S.objects if o.name.startswith('TREE_Foliage_cluster')]
for o in canopies:
    sc=Vector(o.scale); center=o.location.copy()
    o.scale*=.82
    for k in range(27):
        a=random.random()*math.tau; zz=random.uniform(-.85,1); rr=math.sqrt(1-zz*zz)
        d=Vector((rr*math.cos(a),rr*math.sin(a),zz))
        co=center+Vector((d.x*sc.x,d.y*sc.y,d.z*sc.z))*.86
        size=random.uniform(.19,.35)*max(sc)
        vs,fs=leaf_batches[random.randrange(5)]; idx=len(vs)
        vs.extend([tuple(co+Vector((v.x*size,v.y*size*.78,v.z*size*.72))) for v in uverts])
        fs.extend([tuple(idx+i for i in face) for face in ufaces])
for k,(vs,fs) in enumerate(leaf_batches):mesh('TREE_Fine_leaf_cloud_'+str(k),vs,fs,leafm[k])

# Irregular soft tips disguise the geometric edges of the nearby firs.
pinev=[]; pinef=[]
for o in [o for o in S.objects if o.name.startswith('TREE_Layered_fir') and o.location.y<17]:
    r=max(v.co.xy.length for v in o.data.vertices)*o.scale.x
    for k in range(13):
        a=k*math.tau/13; co=o.location+Vector((math.cos(a)*r*.78,math.sin(a)*r*.78,-.37))
        size=r*.24; idx=len(pinev)
        pinev.extend([tuple(co+Vector((v.x*size,v.y*size,v.z*size*.55))) for v in uverts])
        pinef.extend([tuple(idx+i for i in f) for f in ufaces])
mesh('TREE_Fir_needle_boughs',pinev,pinef,leafm[3])

# Richer bank vegetation with recognisable fern fronds and broad leaves.
fernmat=mat('Fern fresh yellow green',(.27,.42,.13),rough=.8)
fv=[]; ff=[]
for k in range(180):
    y=random.uniform(-13,15); x=riverx(y)+random.choice([-1,1])*random.uniform(1.8,3.1)
    if ispath(x,y) or (abs(x-HX)<3 and abs(y-HY)<3):continue
    z=h(x,y)
    for j in range(6):
        a=j*math.tau/6+random.uniform(-.2,.2); ln=random.uniform(.35,.75)
        for t in [.22,.36,.50,.64,.78,.90]:
            cx=x+math.cos(a)*ln*t; cy=y+math.sin(a)*ln*t; cz=z+ln*(1.3*t-.7*t*t)
            w=ln*.2*(1-t)+.02
            for side in [-1,1]:
                v=len(fv); end=(cx+math.cos(a+side*1.0)*w,cy+math.sin(a+side*1.0)*w,cz+.025)
                fv.extend([(cx-.02*math.cos(a),cy-.02*math.sin(a),cz),end,(cx+.08*math.cos(a),cy+.08*math.sin(a),cz+.02)])
                ff.append((v,v+1,v+2))
mesh('ENV_Riverbank_ferns',fv,ff,fernmat)

# Windowed side facade: warm interior light visible from the hero camera.
XX=HX+2.61
for yy in [HY-.95,HY+.95]:
    z=3.78; w=.86; ht=1.2
    cube('Side_window_reveal',(XX,yy,z),(.16,w+.20,ht+.2),timber,.035)
    cube('Side_window_glow',(XX+.10,yy,z),(.025,w,ht),glass,.018)
    for y2 in [yy-w/2,yy,yy+w/2]:cube('Side_window_mullion',(XX+.15,y2,z),(.07,.05,ht+.04),wood,.012)
    for z2 in [z-ht/2,z+.1,z+ht/2]:cube('Side_window_transom',(XX+.15,yy,z2),(.07,w+.06,.05),wood,.012)
    cube('Side_window_sill',(XX+.20,yy,z-ht/2-.1),(.40,w+.35,.14),stone[1],.025)
    cube('Side_window_flower_box',(XX+.27,yy,z-ht/2-.24),(.34,w+.20,.22),wood,.02)
    for k in range(7):
        co=(XX+.34,yy+random.uniform(-.4,.4),z-ht/2-.05)
        ico('Side_window_flowers',co,(.13,.13,.09),flower[k%3],1)
# Individually jointed foundation blocks on front and visible side.
for j in range(2):
    for k in range(11):
        x=HX-2.5+k*.49+(j%2)*.23
        cube('INN_Foundation_ashlar',(x,FY+.03,.52+j*.23),(.46,.18,.20),random.choice(stone),.035)
    for k in range(8):
        y=HY-1.95+k*.52+(j%2)*.22
        cube('INN_Foundation_ashlar',(HX+2.61,y,.52+j*.23),(.17,.49,.20),random.choice(stone),.035)

# Ivy climbs the right gable edge; separate leaf clusters soften plaster and timber.
ivy=mat('Ivy deep green',(.095,.23,.09))
for k in range(10):
    y=HY+1.7-random.random()*.7; z0=.9; ht=random.uniform(2.0,3.7)
    pts=[(XX+.12,y+.10*math.sin(i*.9+k),z0+i*ht/12) for i in range(13)]
    curve('INN_Ivy_vine',pts,.015,bark)
    for i in range(1,13):
        for side in [-1,1]:
            x,y2,z=pts[i]; ico('INN_Ivy_leaf',(x+.02,y2+side*.12,z),(.035,.13,.10),ivy,1)
# Porch bunting and a modest, welcoming bench.
curve('Porch_festival_cord',[(.6,-.82,2.95),(3.2,-.82,2.72),(5.9,-.82,2.95)],.012,wood)
for i in range(12):
    x=.7+i*.44; z=2.73+.22*((x-3.2)/2.7)**2
    mesh('Porch_small_pennant',[(x,-.84,z),(x+.27,-.84,z+.01),(x+.13,-.84,z-.32)],[(0,1,2)],roofm[2] if i%2 else get('Woven saffron canopy'))
cube('Porch_bench_seat',(1.35,-.55,.99),(1.28,.42,.13),wood,.035)
for x in [.87,1.83]:cube('Porch_bench_leg',(x,-.55,.73),(.12,.30,.48),timber,.025)
cube('Porch_bench_back',(1.35,-.30,1.27),(1.28,.09,.28),wood,.025)

# Extra varied paving across the center of the route near the entrance.
for i in range(60):
    y=random.uniform(-5.7,-.7); x=3.5+.47*y+random.uniform(-.55,.55)
    if abs(x-riverx(y))<1.7:continue
    o=cube('Route_small_infill_stone',(x,y,h(x,y)+.045),(random.uniform(.13,.29),random.uniform(.16,.30),.065),random.choice(stone),.04)
    o.rotation_euler.z=random.uniform(-.35,.35)

# Deliberate warm late-afternoon lighting, local glow, and shallow optical falloff.
S.world.node_tree.nodes.get('Background')
for n in S.world.node_tree.nodes:
    if n.type=='BACKGROUND':n.inputs[0].default_value=(.25,.36,.48,1);n.inputs[1].default_value=.28
sun=bpy.data.objects.get('SUN_Last_light');sun.data.energy=3.7;sun.data.color=(1,.68,.36);sun.data.angle=math.radians(9)
bpy.data.objects['SKY_Large_cool_fill'].data.energy=1300
bpy.data.objects['INN_Window_spill'].data.energy=220
light('KEY_Inn_warm_softbox',(-4,-6,11),1700,(1,.69,.40),kind='AREA',target=(2,1,2),size=8)
light('RIM_Sun_on_leaves',(-9,9,12),2400,(1,.79,.43),kind='AREA',target=(1,2,1),size=7)
S.camera.data.ortho_scale=28.2
S.camera.data.dof.aperture_fstop=5.6
S.render.resolution_x=1920;S.render.resolution_y=1200;S.cycles.samples=64
# Compositor glare replaces fake glow meshes; optional group API for Blender 5.
ng=bpy.data.node_groups.new('Lanternbrook_soft_highlights','CompositorNodeTree')
ng.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor')
rl=ng.nodes.new('CompositorNodeRLayers');rl.scene=S;gl=ng.nodes.new('CompositorNodeGlare')
if hasattr(gl,'glare_type'):
    gl.glare_type='FOG_GLOW';gl.quality='HIGH';gl.threshold=1.8;gl.mix=-.92
else:
    gl.inputs['Type'].default_value='Fog Glow';gl.inputs['Quality'].default_value='High'
    gl.inputs['Threshold'].default_value=1.8;gl.inputs['Strength'].default_value=.16;gl.inputs['Size'].default_value=.25
out=ng.nodes.new('NodeGroupOutput');ng.links.new(rl.outputs['Image'],gl.inputs['Image']);ng.links.new(gl.outputs['Image'],out.inputs['Image'])
if hasattr(S,'compositing_node_group'):S.compositing_node_group=ng
else:
    S.use_nodes=True
    cn=S.node_tree.nodes;cn.clear();r=cn.new('CompositorNodeRLayers');g=cn.new('CompositorNodeGlare');g.glare_type='FOG_GLOW';g.threshold=1.8;g.mix=-.92
    c=cn.new('CompositorNodeComposite');S.node_tree.links.new(r.outputs['Image'],g.inputs['Image']);S.node_tree.links.new(g.outputs['Image'],c.inputs['Image'])
S.render.filepath=str(OUT/'renders'/'Lanternbrook_preview_v02.png')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Lanternbrook_HD2D.blend'))
bpy.ops.render.render(write_still=True)
print('REFINEMENT_RENDER_COMPLETE',flush=True)
