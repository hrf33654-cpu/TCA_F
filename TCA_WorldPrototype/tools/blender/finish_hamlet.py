import bpy, ast, math, random, json
from pathlib import Path
from mathutils import Vector
ROOT=Path(r'E:\TCA_F\TCA_WorldPrototype'); OUT=ROOT/'art'/'alchemist_hamlet';S=bpy.context.scene
source=ast.parse((ROOT/'tools'/'blender'/'build_hamlet.py').read_text(encoding='utf8'))
exec(compile(ast.Module(body=[n for n in source.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),'primitives','exec'),globals())
random.seed(7012)
leafm=[bpy.data.materials['Leaf canopy '+str(i)] for i in range(5)]
wood=bpy.data.materials['Honey oak planks'];timber=bpy.data.materials['Aged chestnut beams'];metal=bpy.data.materials['Forged dark iron'];brass=bpy.data.materials['Aged brass']
# Replace the round trim treatment with actual small shaped leaves.
for o in list(S.objects):
    if o.name.startswith(('TREE_Fine_leaf_cloud','TREE_Fir_needle_boughs')):bpy.data.objects.remove(o,do_unlink=True)
batches=[([],[]) for _ in leafm]
for o in [o for o in S.objects if o.name.startswith('TREE_Foliage_cluster')]:
    sc=Vector(o.scale)/.82;center=o.location.copy();o.scale= sc*.66
    for polygon in o.data.polygons:polygon.use_smooth=True
    for k in range(330):
        a=random.random()*math.tau;zz=random.uniform(-.95,1);rr=math.sqrt(1-zz*zz)
        normal=Vector((rr*math.cos(a),rr*math.sin(a),zz))
        co=center+Vector((normal.x*sc.x,normal.y*sc.y,normal.z*sc.z))*random.uniform(.78,1)
        u=normal.cross(Vector((0,0,1)))
        if u.length<.01:u=Vector((1,0,0))
        u.normalize();v=normal.cross(u).normalized()
        angle=random.random()*math.tau;u,v=u*math.cos(angle)+v*math.sin(angle),-u*math.sin(angle)+v*math.cos(angle)
        ln=random.uniform(.17,.28)*max(sc);wd=ln*random.uniform(.4,.65)
        verts,faces=batches[random.randrange(5)];idx=len(verts)
        coords=[(0,-ln*.6,0),(-wd,-ln*.1,0),(-wd*.7,ln*.35,0),(0,ln*.65,0),(wd*.7,ln*.35,0),(wd,-ln*.1,0),(0,0,ln*.15)]
        verts.extend([tuple(co+u*x+v*y+normal*z) for x,y,z in coords])
        faces.extend([(idx+j,idx+(j+1)%6,idx+6) for j in range(6)])
for k,(v,f) in enumerate(batches):mesh('TREE_Individual_leaf_canopies_'+str(k),v,f,leafm[k])
# Each evergreen has a broken, asymmetric skirt rather than a perfectly straight cone.
for o in [o for o in S.objects if o.name.startswith('TREE_Layered_fir')]:
    vs=[];fs=[];ma=o.data.materials[0]
    radius=max(Vector(v.co[:2]).length for v in o.data.vertices)
    low=min(v.co.z for v in o.data.vertices);high=max(v.co.z for v in o.data.vertices);ht=high-low
    count=40
    for ring,(z,r) in enumerate([(0,.80),(.09,1),(.25,.68),(.47,.52),(.70,.31),(.88,.15),(1,0.015)]):
        for j in range(count):
            a=j*math.tau/count; rand=random.uniform(.85,1.13);jag=(j%2)*.08 if ring<3 else 0
            vs.append((math.cos(a)*radius*r*rand,math.sin(a)*radius*r*rand,low+ht*(z-jag)+random.uniform(-.03,.03)))
    for ring in range(6):
        for j in range(count):
            a=ring*count+j;b=ring*count+(j+1)%count
            fs.append((a,b,b+count,a+count))
    me=bpy.data.meshes.new('Handshaped_fir_boughs');me.from_pydata(vs,[],fs);me.materials.append(ma);me.update();o.data=me

# A small mill wheel on the river side makes the apothecary setting distinct.
cx,cy,cz=.12,4.1,1.35; radius=1.02
for xx in [cx-.18,cx+.18]:
    pts=[(xx,cy+math.cos(i*math.tau/64)*radius,cz+math.sin(i*math.tau/64)*radius) for i in range(65)]
    curve('INN_Waterwheel_wooden_rim',pts,.075,wood)
    for k in range(8):
        a=k*math.tau/8
        beam('INN_Waterwheel_spoke',(xx,cy,cz),(xx,cy+math.cos(a)*radius,cz+math.sin(a)*radius),.044,timber)
for k in range(18):
    a=k*math.tau/18;y=cy+math.cos(a)*radius;z=cz+math.sin(a)*radius
    paddle=cube('INN_Waterwheel_paddle',(cx,y,z),(.58,.25,.10),wood,.018);paddle.rotation_euler.x=a
beam('INN_Waterwheel_axle',(-.45,cy,cz),(.82,cy,cz),.12,metal,12)
for xx in [-.49,.48]:
    beam('INN_Wheel_support',(xx,cy-.47,.5),(xx,cy,1.45),.09,timber)
    beam('INN_Wheel_support',(xx,cy+.47,.5),(xx,cy,1.45),.09,timber)
cube('INN_Mill_sluice',(-.25,5.2,1.16),(1.15,1.70,.14),timber,.04)
for xx in [-.79,.29]:cube('INN_Sluice_edge',(xx,5.2,1.30),(.10,1.7,.22),wood,.025)
# Real ground contrast under foliage and warm surface variation.
for o in S.objects:
    if o.type=='LIGHT' and o.name.startswith('Lantern_warm_pool'):o.data.energy=75
S.camera.data.dof.aperture_fstop=6.3
S.cycles.samples=112
S.render.resolution_x=2400;S.render.resolution_y=1500;S.render.resolution_percentage=100
S.render.filepath=str(OUT/'renders'/'Lanternbrook_final.png')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Lanternbrook_HD2D.blend'))
bpy.ops.render.render(write_still=True)
print('FINAL_HERO_RENDER_COMPLETE',flush=True)
