"""Extend the approved visual study without rebuilding or overwriting it.
Run in Blender; coordinates here are Blender XY ground / Z height.
"""
import bpy, bmesh, ast, math, random, json
from pathlib import Path
from mathutils import Vector
ROOT=Path(r'E:\TCA_F\TCA_WorldPrototype')
OUT=ROOT/'art'/'lanternbrook_map_v1'; OUT.mkdir(parents=True,exist_ok=True)
(ROOT/'tools/blender/build_map_v1.error.txt').unlink(missing_ok=True)
DEST=ROOT/'world'/'maps'/'lanternbrook'; DEST.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'art/alchemist_hamlet/Lanternbrook_HD2D.blend'))
S=bpy.context.scene
source=ast.parse((ROOT/'tools/blender/build_hamlet.py').read_text(encoding='utf8'))
exec(compile(ast.Module(body=[n for n in source.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),'primitives','exec'),globals())
def ico(name,loc,scale,ma,sub=1):
    me=bpy.data.meshes.new(name);bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=sub+1,radius=1);bm.to_mesh(me);bm.free()
    o=bpy.data.objects.new(name,me);S.collection.objects.link(o);o.location=loc;o.scale=scale;me.materials.append(ma);return o
def cyl(name,loc,radius,depth,ma,verts=12,r2=None):
    me=bpy.data.meshes.new(name);bm=bmesh.new();bmesh.ops.create_cone(bm,cap_ends=True,cap_tris=False,segments=verts,radius1=radius,radius2=radius if r2 is None else r2,depth=depth);bm.to_mesh(me);bm.free()
    o=bpy.data.objects.new(name,me);S.collection.objects.link(o);o.location=loc;me.materials.append(ma);return o
random.seed(271027)
earth=bpy.data.materials['Mossy earth']
stone=[bpy.data.materials['Weathered limestone '+str(i)] for i in range(4)]
leafm=[bpy.data.materials['Leaf canopy '+str(i)] for i in range(5)]
grassm=[bpy.data.materials['Meadow '+str(i)] for i in range(4)]
bark=bpy.data.materials['Bark'];wood=bpy.data.materials['Honey oak planks'];timber=bpy.data.materials['Aged chestnut beams']
brass=bpy.data.materials['Aged brass'];metal=bpy.data.materials['Forged dark iron'];glass=bpy.data.materials['Lantern honey glow']
water=bpy.data.materials['Jade river']
trailmat=mat('V1 Warm gravel path',(.29,.285,.18),noise=7)
ruinmat=mat('V1 Lichen dressed stone',(.37,.43,.35),noise=5)
main=[(28,-32),(25,-27),(20,-21),(17,-15),(13,-10),(8,-7),(4,-5),(1,-2.2),(-.75,-1.8),(-5.8,-1.8),(-9,-1),(-11,5),(-12,12),(-15,18),(-20,23),(-24,25)]
back=[(-24,25),(-20,29),(-13,28),(-7,23),(-6.4,21),(-6.4,18),(3.8,18),(7,20),(12,20),(12,14),(10,9),(10,4),(10,-2),(7,-4),(4,-5)]
door=[(1,-2.2),(3,-1.2),(3.2,.15)]
routes=[main,back,door]
def segdist(p,a,b):
    p,a,b=Vector(p),Vector(a),Vector(b); d=b-a
    t=max(0,min(1,(p-a).dot(d)/max(.0001,d.length_squared)))
    return (p-a-d*t).length
def route_distance(x,y):return min(segdist((x,y),a,b) for route in routes for a,b in zip(route,route[1:]))
def inside_old(x,y):return -17<x<17 and -16<y<18
original_height=h
def h(x,y):
    r=math.hypot(x+25,y-28);t=max(0,min(1,(7.0-r)/2.0));t=t*t*(3-2*t)
    return original_height(x,y)*(1-t)+.67*t
def safe_side_position(x,y,clearance=3.0):
    if route_distance(x,y)>clearance:return Vector((x,y))
    for radius in [2,3,4,5,6,8]:
        candidates=[Vector((x+math.cos(i*math.tau/24)*radius,y+math.sin(i*math.tau/24)*radius)) for i in range(24)]
        for p in candidates:
            if route_distance(*p)>clearance and abs(p.x-riverx(p.y))>3.0 and math.hypot(p.x+25,p.y-28)>6:return p
    raise RuntimeError('Cannot clear route at '+str((x,y)))
# Move complete original trees, including the individually batched leaf geometry.
trunks=[o for o in S.objects if o.name.startswith('TREE_Trunk')]
tree_moves=[]
for o in trunks:
    x,y=o.location.x,o.location.y;dest=safe_side_position(x,y,2.7)
    tree_moves.append((Vector((x,y)),Vector((dest.x-x,dest.y-y,h(*dest)-h(x,y)))))
for o in list(S.objects):
    if not o.name.startswith(('TREE_','Birch')):continue
    if o.name.startswith('TREE_Individual_leaf'):
        for v in o.data.vertices:
            co=o.matrix_world@v.co;p=Vector((co.x,co.y));center,delta=min(tree_moves,key=lambda item:(p-item[0]).length_squared)
            if (p-center).length<4.8:v.co += o.matrix_world.to_3x3().inverted()@delta
    else:
        p=Vector((o.location.x,o.location.y));center,delta=min(tree_moves,key=lambda item:(p-item[0]).length_squared)
        if (p-center).length<4.8:o.location+=delta
for o in list(S.objects):
    if o.name.startswith('Fence_'):
        bpy.data.objects.remove(o,do_unlink=True)
    elif o.name.startswith('Meadow_boulder'):
        dest=safe_side_position(o.location.x,o.location.y,2.5)
        dz=h(*dest)-h(o.location.x,o.location.y);o.location.x=dest.x;o.location.y=dest.y;o.location.z+=dz
# Remove the old finite ground and distant wall; retain hand-authored inn, props and trees.
for o in list(S.objects):
    if o.name.startswith(('ENV_Terrain','ENV_Jade','CLIFF_Background','Water_current_glint','ATMOSPHERE')):
        bpy.data.objects.remove(o,do_unlink=True)
# Wider original bridge gives >2m clear width between parapets.
for o in list(S.objects):
    if o.name.startswith('Bridge'):
        if o.type=='MESH':
            # Coordinates can be object-local or baked world; transform all vertices in world space.
            inv=o.matrix_world.inverted()
            for v in o.data.vertices:
                co=o.matrix_world@v.co;co.y=-1.8+(co.y+1.8)*1.50;v.co=inv@co
# Trim original meadow blades along new routes, preserving the fine vegetation away from paths.
for o in list(S.objects):
    if o.type=='MESH' and o.name.startswith(('ENV_Meadow','ENV_Wildflower')):
        old=o.data; vs=[];fs=[]; mi=[]
        for p in old.polygons:
            c=o.matrix_world@p.center
            if route_distance(c.x,c.y)<1.85:continue
            j=len(vs);vs.extend([old.vertices[k].co[:] for k in p.vertices]);fs.append(tuple(range(j,len(vs))));mi.append(p.material_index)
        me=bpy.data.meshes.new(o.name+'_cleared');me.from_pydata(vs,[],fs)
        for ma in old.materials:me.materials.append(ma)
        for p,i in zip(me.polygons,mi):p.material_index=i
        o.data=me
# Full 100x80 ground. Background apron continues beyond collision boundaries.
for xa,xb,ya,yb,step,label in [(-50,50,-40,40,.65,'V1_Ground'),(-165,165,-155,155,6,'V1_Backdrop')]:
    nx=math.ceil((xb-xa)/step);ny=math.ceil((yb-ya)/step);vs=[];fs=[]
    for j in range(ny+1):
        y=ya+(yb-ya)*j/ny
        for i in range(nx+1):
            x=xa+(xb-xa)*i/nx
            z=h(x,y)
            if label=='V1_Backdrop':
                z-=.08
                edge=max(abs(x)-50,abs(y)-40,0)
                z+=min(12,edge*.15)*( .7+.3*math.sin(x*.07+y*.06))
            vs.append((x,y,z))
    for j in range(ny):
        for i in range(nx):
            a=j*(nx+1)+i;cx=xa+(xb-xa)*(i+.5)/nx;cy=ya+(yb-ya)*(j+.5)/ny
            if label=='V1_Backdrop' and abs(cx)<49 and abs(cy)<39:continue
            fs.append((a,a+1,a+nx+2,a+nx+1))
    o=mesh(label,vs,fs,earth)
    for p in o.data.polygons:p.use_smooth=True
# River also extends beyond every allowed camera view.
vs=[];fs=[]
for j in range(1241):
    y=-155+j*.25;x=riverx(y);vs.extend([(x-1.34,y,-.23),(x+1.34,y,-.23)])
    if j:a=2*j;fs.append((a-2,a,a+1,a-1))
mesh('V1_River_Jade',vs,fs,water)
# Ribbons and loose edging stones ground the paths in the meadow.
for ri,route in enumerate(routes):
    vs=[];fs=[]
    for a,b in zip(route,route[1:]):
        a,b=Vector(a),Vector(b);d=b-a;perp=Vector((-d.y,d.x)).normalized();steps=max(1,math.ceil(d.length/.42))
        for k in range(steps):
            p=a.lerp(b,k/steps);q=a.lerp(b,(k+1)/steps)
            if abs(p.x-riverx(p.y))<2.55:continue
            width=1.50 if ri<2 else 1.1
            # Subdivide across the path too: broad quads otherwise cut through undulating ground.
            for strip in range(8):
                left=-width+2*width*strip/8;right=-width+2*width*(strip+1)/8
                ring=[p+perp*left,q+perp*left,q+perp*right,p+perp*right];j=len(vs)
                vs.extend([(v.x,v.y,h(v.x,v.y)+.045) for v in ring]);fs.append((j,j+1,j+2,j+3))
            if k%5==0 and not inside_old(p.x,p.y):
                for side in [-1,1]:
                    v=p+perp*side*random.uniform(1.55,1.95)
                    ico('V1_Path_edge_stone',(v.x,v.y,h(v.x,v.y)+.04),(.22,.16,.08),random.choice(stone),1)
    mesh('V1_Path_'+str(ri),vs,fs,trailmat)
# Upper bridge: full-width planked crossing, stone abutments and railings.
bx=riverx(18);by=18
for k in range(25):
    x=bx-3.3+(k+.5)*6.6/25
    cube('V1_BridgeDeck',(x,by,.57),(.272,3.15,.20),wood,.025)
for side in [-1,1]:
    yy=by+side*1.62
    for x in [bx-3.1,bx-1.55,bx,bx+1.55,bx+3.1]:
        cube('V1_BridgeRail_post',(x,yy,1.13),(.17,.17,1.2),timber,.025)
    for zz in [.97,1.53]:beam('V1_BridgeRail',(bx-3.3,yy,zz),(bx+3.3,yy,zz),.075,wood,8)
for x in [bx-3.0,bx+3.0]:cube('V1_BridgeAbutment',(x,by,.06),(.65,3.6,1.05),stone[2],.06)
# Broad inn doorstep, deliberately separate from tiny visual cobbles.
for k in range(3):cube('V1_DoorStep',(3.2,.03+k*.23,.52+k*.14),(1.8,.42,.18),stone[1],.025)
# Entrance gateway and noticeboard. No story text is treated as canon.
for x in [25.65,30.35]:
    cube('V1_Entrance_post',(x,-32,2.0),(.35,.4,3.4),timber,.05)
    ico('V1_Entrance_stone_foot',(x,-32,.65),(.48,.46,.45),stone[2],1)
beam('V1_Entrance_lintel',(25.45,-32,3.7),(30.55,-32,3.7),.22,wood,8)
cube('V1_Entrance_sign',(28,-32,3.15),(2.1,.14,.60),wood,.04)
for x in [27.35,28,28.65]:cyl('V1_Brass_waymark',(x,-32.09,3.15),.15,.035,brass,6).rotation_euler.x=math.pi/2
# Ruined observatory: circular terrace, broken pillars, complete arch on the skyline.
rx,ry=-25,28
cyl('V1_RuinTerrace',(rx,ry,.57),5.1,.25,ruinmat,40)
cyl('V1_RuinInset',(rx,ry,.71),3.7,.055,stone[2],40)
for k in range(12):
    a=k*math.tau/12
    if k in [8,9,10]:continue
    x,y=rx+4.1*math.cos(a),ry+4.1*math.sin(a);ht=random.uniform(1.2,3.6)
    if route_distance(x,y)<2.2:continue
    cube('V1_RuinColumn_base',(x,y,.98),(1.05,1.05,.4),stone[2],.07)
    cyl('V1_RuinColumn',(x,y,1.12+ht/2),.33,ht,ruinmat,9,.29)
    if k%3==0:cube('V1_RuinColumn_cap',(x,y,1.16+ht),(.85,.85,.25),stone[1],.06)
for x in [rx-1.7,rx+1.7]:cube('V1_RuinArch_pier',(x,ry+3.7,2.4),(.7,.8,3.6),ruinmat,.07)
for k in range(13):
    a=(k+.5)*math.pi/13;x=rx+1.7*math.cos(a);z=4.15+1.7*math.sin(a)
    o=cube('V1_RuinArch_voussoir',(x,ry+3.7,z),(.47,.85,.65),stone[k%4],.035);o.rotation_euler.y=math.pi/2-a
cyl('V1_Ruin_pedestal',(rx,ry,.99),.72,.5,stone[1],8)
ico('V1_Ruin_brass_armillary',(rx,ry,1.77),(.52,.52,.52),brass,2)
for k in range(3):
    yy=24.05+k*.40;cube('V1_RuinStep',(rx,yy,.45+k*.085),(3.2,.7,.17),ruinmat,.035)
# River rocks and reeds continue through the expanded landscape.
for k in range(210):
    y=random.uniform(-48,48);x=riverx(y)+random.choice([-1,1])*random.uniform(1.5,2.1)
    if route_distance(x,y)<2.1:continue
    ico('V1_BankRock',(x,y,h(x,y)+.08),(random.uniform(.25,.65),random.uniform(.3,.8),random.uniform(.2,.55)),random.choice(stone),1)
    if k%3==0:
        for t in range(4):beam('V1_Reed',(x+t*.06,y,h(x,y)),(x+t*.07+.15,y+.05,h(x,y)+random.uniform(.5,1.0)),.016,grassm[2],4)
# New trees use branching silhouettes, lobe cores and individually shaped leaf cards.
tree_positions=[]
def newtree(x,y,size):
    z=h(x,y);ht=random.uniform(4.5,6.5)*size
    cyl('V1_TreeTrunk',(x,y,z+ht*.43),.19*size,ht*.86,bark,8,.07*size)
    tree_positions.append((x,y))
    lv=[([],[]) for _ in leafm]
    for c in range(5):
        a=c*2.4;cc=Vector((x+math.cos(a)*size*.85,y+math.sin(a)*size*.85,z+ht*(.71+c*.045)))
        beam('V1_TreeBranch',(x,y,z+ht*.5),cc,.07*size,bark,6)
        sc=Vector((1.10,1.0,.85))*size
        o=ico('V1_CanopyCore',cc,sc*.78,leafm[c],2)
        for f in o.data.polygons:f.use_smooth=True
        for j in range(85):
            n=Vector((random.uniform(-1,1),random.uniform(-1,1),random.uniform(-1,1))).normalized()
            co=cc+Vector((n.x*sc.x,n.y*sc.y,n.z*sc.z))*random.uniform(.78,1.04)
            u=n.cross(Vector((0,0,1)));u=Vector((1,0,0)) if u.length<.01 else u.normalized();v=n.cross(u)
            ln=random.uniform(.15,.30)*size;wd=ln*.5;vs,fs=lv[j%5];i=len(vs)
            vs.extend([tuple(co-v*ln),tuple(co-u*wd),tuple(co+v*ln),tuple(co+u*wd),tuple(co+n*.05)])
            fs.extend([(i,i+1,i+4),(i+1,i+2,i+4),(i+2,i+3,i+4),(i+3,i,i+4)])
    for j,(vs,fs) in enumerate(lv):mesh('V1_CanopyLeaves',vs,fs,leafm[j])
for k in range(320):
    x=random.uniform(-68,68);y=random.uniform(-57,57)
    if inside_old(x,y) or abs(x-riverx(y))<3 or route_distance(x,y)<3.65 or (Vector((x-rx,y-ry)).length<7):continue
    if any(math.hypot(x-a,y-b)<4.0 for a,b in tree_positions):continue
    newtree(x,y,random.uniform(.85,1.65))
# Rock escarpments and tall forest at the perimeter physically conceal the map boundary.
for side in [-1,1]:
    for k in range(23):
        x=side*random.uniform(48,54);y=-43+k*3.9
        ico('V1_PerimeterRock',(x,y,random.uniform(1,3)),(random.uniform(2.5,5),random.uniform(2.4,4.4),random.uniform(3,6)),random.choice(stone),1)
    for k in range(24):
        x=-47+k*4.0;y=side*random.uniform(39,44)
        ico('V1_PerimeterRock',(x,y,random.uniform(1,3)),(random.uniform(2.5,5),random.uniform(2.4,4.4),random.uniform(3,6)),random.choice(stone),1)
# Small ground detail is batched and stays out of the walking corridor.
vs=[];fs=[];mi=[]
for k in range(35000):
    x=random.uniform(-51,51);y=random.uniform(-41,41)
    if inside_old(x,y) or abs(x-riverx(y))<1.85 or route_distance(x,y)<1.85 or math.hypot(x-rx,y-ry)<5.6:continue
    z=h(x,y);ht=random.uniform(.12,.38)
    for j in range(2):
        a=random.random()*math.tau;dx=math.cos(a)*.045;dy=math.sin(a)*.045;i=len(vs)
        vs.extend([(x-dx,y-dy,z),(x+dx,y+dy,z),(x+.07,y+.05,z+ht)]);fs.append((i,i+1,i+2));mi.append(random.randrange(4))
o=mesh('V1_MeadowGrass',vs,fs,None)
for ma in grassm:o.data.materials.append(ma)
for p,i in zip(o.data.polygons,mi):p.material_index=i
# Warm wayfinding lamps and resting benches, beside (never inside) the clear corridor.
lamps=[]
for x,y in [(30,-30),(21,-20),(15,-13),(-10,3),(-13,14),(-20,23),(-18,29),(-5,21),(3,20),(11,15),(11,5)]:
    safe=safe_side_position(x,y,2.5);x,y=safe
    z=h(x,y);cube('V1_LampPost',(x,y,z+1.25),(.13,.13,2.5),timber,.02)
    cube('V1_LampHousing',(x,y,z+2.62),(.42,.42,.5),metal,.025)
    cube('V1_LampGlass',(x,y-.225,z+2.62),(.28,.02,.33),glass,.01)
    cube('V1_LampGlass',(x,y+.225,z+2.62),(.28,.02,.33),glass,.01)
    cyl('V1_LampRoof',(x,y,z+2.94),.38,.22,metal,4,.03)
    lamps.append([x,z+2.6,-y])
for x,y in [(22,-19),(-18,21),(15,18)]:
    safe=safe_side_position(x,y,3.1);x,y=safe
    z=h(x,y);cube('V1_BenchSeat',(x,y,z+.65),(2,.65,.15),wood,.04)
    for dx in [-.75,.75]:cube('V1_BenchLeg',(x+dx,y,z+.3),(.14,.45,.6),timber,.025)
    cube('V1_BenchBack',(x,y+.3,z+1.05),(2,.12,.55),wood,.04)
# Dress the extended areas to the same level as the original inn.
flower_mats=[bpy.data.materials.get('Flowers '+str(i)) or mat('V1 Flowers '+str(i),c) for i,c in enumerate([(.60,.43,.68),(.85,.64,.31),(.62,.72,.58)])]
fv=[];ff=[];fi=[]
for k in range(1900):
    x=random.uniform(-45,45);y=random.uniform(-36,36)
    if abs(x-riverx(y))<2.1 or route_distance(x,y)<1.8 or math.hypot(x+25,y-28)<5.8:continue
    z=h(x,y);ht=random.uniform(.18,.42)
    for j in range(4):
        a=j*math.pi/2;dx=math.cos(a)*.065;dy=math.sin(a)*.065;i=len(fv)
        fv.extend([(x,y,z+ht),(x+dx-dy*.5,y+dy+dx*.5,z+ht+.025),(x+dx*1.7,y+dy*1.7,z+ht+.015),(x+dx+dy*.5,y+dy-dx*.5,z+ht+.025)])
        ff.append((i,i+1,i+2,i+3));fi.append(k%3)
o=mesh('V1_MeadowWildflowers',fv,ff,None)
for ma in flower_mats:o.data.materials.append(ma)
for p,i in zip(o.data.polygons,fi):p.material_index=i
# Rear facade is finished for free rotation, with proper timber frames and shutters.
plaster=bpy.data.materials['Warm lime plaster'];amber=bpy.data.materials['Amber windows']
for x in [1.85,4.55]:
    for z in [2.1,4.05]:
        cube('V1_InnRear_window_frame',(x,5.18,z),(1.05,.18,1.15),timber,.025)
        cube('V1_InnRear_glass',(x,5.29,z),(.84,.025,.92),amber,.01)
        cube('V1_InnRear_mullion',(x,5.32,z),(.065,.04,1.03),wood,.01)
        cube('V1_InnRear_mullion',(x,5.32,z),(.96,.04,.065),wood,.01)
        for side in [-1,1]:cube('V1_InnRear_shutter',(x+side*.68,5.19,z),(.23,.12,1.10),wood,.025)
for z in [1.05,3.15,4.63]:cube('V1_InnRear_timber',(3.2,5.18,z),(5.3,.17,.16),timber,.02)
# Broken outer masonry, moss crowns and brass rings make the ruin a distinct destination.
for k in range(24):
    a=k*math.tau/24;x=rx+5.35*math.cos(a);y=ry+5.35*math.sin(a)
    if route_distance(x,y)<2.4:continue
    ht=random.uniform(.35,.95)
    o=cube('V1_RuinWall',(x,y,.65+ht/2),(1.25,.65,ht),stone[k%4],.065);o.rotation_euler.z=a+math.pi/2
    ico('V1_RuinMoss',(x,y,.65+ht),(.65,.43,.07),grassm[2],1)
for radius in [1.6,1.9]:
    curve('V1_Ruin_floor_ring',[(rx+radius*math.cos(j*math.tau/96),ry+radius*math.sin(j*math.tau/96),.744) for j in range(97)],.018,brass)
for k in range(75):
    a=random.random()*math.tau;r=random.uniform(2.4,5.0);x=rx+r*math.cos(a);y=ry+r*math.sin(a)
    if route_distance(x,y)<1.5:continue
    ico('V1_RuinMoss',(x,y,.745),(.20,.35,.035),grassm[2],1)
# Wayfinding boards and small leaf beds sit beyond the 2m corridor.
for x,y in [(24,-25),(-11,7),(-16,24),(8,21)]:
    safe=safe_side_position(x,y,2.4);x,y=safe;z=h(x,y)
    cube('V1_SignPost',(x,y,z+.85),(.13,.13,1.7),timber,.02)
    cube('V1_SignBoard',(x,y,z+1.5),(1.1,.12,.32),wood,.03)
    beam('V1_SignArrow',(x-.3,y-.08,z+1.5),(x+.3,y-.08,z+1.5),.025,brass,5)
    for k in range(9):
        a=k*2.4;xx=x+.6*math.cos(a);yy=y+.6*math.sin(a)
        ico('V1_WaypointFern',(xx,yy,h(xx,yy)+.12),(.20,.28,.12),grassm[k%4],1)
# Metadata is the single shared coordinate source for scene baking and route checks.
def godot(p):return [p[0],h(*p),-p[1]]
meta={'version':1,'bounds':[-50,50,-40,40], 'routes':[[godot(p) for p in r] for r in routes],
      'regions':[{'id':'entrance','label':'林间入口','position':[28,1,30]}, {'id':'courtyard','label':'驿站庭院','position':[3,1,1]}, {'id':'bridge','label':'溪上石桥','position':[-3.4,1,1.8]}, {'id':'riverside','label':'河岸小径','position':[-12,1,-12]}, {'id':'ruins','label':'林中遗迹','position':[-25,1,-28]}],
      'markers':{'Spawn':[28,.55,30],'InnDoor':[3.2,1.05,-.55],'Exit':[28,.55,34],'RuinsEntry':[-25,.75,-25],'UpperBridge':[bx,.7,-18]},'lamps':lamps,'colliders':[]}
bpy.context.view_layer.update()
# Selectively simplified blocking volumes; ground and bridge decks use exact triangle surfaces.
prefixes=('INN_Limewashed','INN_Stone_foundation','TREE_Trunk','Meadow_boulder','Riverbank_moss_stone','Bridge_parapet','Bridge_capstone','V1_TreeTrunk','V1_RuinColumn','V1_RuinWall','V1_RuinArch_pier','V1_Ruin_pedestal','V1_PerimeterRock','V1_BankRock','V1_Entrance_post','V1_LampPost','V1_SignPost','V1_Bench','Fence_post','Fence_rail','Crate','Barrel','Apothecary_table','Table_leg','Stall_pole','Terracotta_planter')
for o in S.objects:
    if o.type!='MESH' or not o.name.startswith(prefixes):continue
    corners=[o.matrix_world@Vector(c) for c in o.bound_box];lo=Vector(tuple(min(p[i] for p in corners) for i in range(3)));hi=Vector(tuple(max(p[i] for p in corners) for i in range(3)))
    center=(lo+hi)/2;size=hi-lo
    # AABBs for sparse props; trunks use a cylinder in engine.
    kind='trunk' if 'Trunk' in o.name else 'box'
    meta['colliders'].append({'name':o.name,'kind':kind,'position':[center.x,center.z,-center.y],'size':[max(.04,size.x),max(.04,size.z),max(.04,size.y)]})
(DEST/'map_data.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
# Organize the source into meaningful authoring collections.
for o in list(S.objects):
    if o.type not in {'MESH','CURVE'}:continue
    n=o.name
    label='V1 Details'
    if n.startswith(('V1_Ground','V1_Backdrop','V1_Perimeter')):label='V1 Landscape'
    elif n.startswith(('V1_Ruin',)):label='V1 Ruins'
    elif n.startswith(('V1_Tree','V1_Canopy','V1_Meadow')):label='V1 Forest'
    elif n.startswith(('V1_Path','V1_Bridge','V1_Door','V1_Entrance')):label='V1 Routes'
    elif n.startswith(('V1_River','V1_Bank','V1_Reed')):label='V1 River'
    elif not n.startswith('V1_'):continue
    c=bpy.data.collections.get(label) or bpy.data.collections.new(label)
    if c.name not in S.collection.children:S.collection.children.link(c)
    for oc in list(o.users_collection):oc.objects.unlink(o)
    c.objects.link(o)
# Region cameras and extended lamp lighting remain editable in the Blender source.
for region in meta['regions']:
    p=region['position'];target=Vector((p[0],-p[2],p[1]));pos=target+Vector((18,-25,26))
    data=bpy.data.cameras.new('MapCamera_'+region['id']);data.type='ORTHO';data.ortho_scale=30
    cam=bpy.data.objects.new(data.name,data);S.collection.objects.link(cam);cam.location=pos;cam.rotation_euler=(target-pos).to_track_quat('-Z','Y').to_euler()
for p in lamps:light('V1_Lantern_pool',(p[0],-p[2],p[1]),55,(1,.55,.2))
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Lanternbrook_Map_v1.blend'))
(OUT/'build_complete.json').write_text(json.dumps({'objects':len(S.objects),'trees_added':len(tree_positions),'routes':len(routes),'colliders':len(meta['colliders'])}),encoding='utf8')
print('MAP_V1_BUILD_COMPLETE',flush=True)
