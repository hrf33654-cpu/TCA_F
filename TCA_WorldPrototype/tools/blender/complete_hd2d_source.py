"""Mirror the final, editor-authored Godot dressing into an editable Blender source."""
import bpy, bmesh, json, math
from pathlib import Path
from mathutils import Vector, Matrix, Euler
ROOT=Path(r'E:\TCA_F\TCA_WorldPrototype')
BASE=ROOT/'world/maps/lanternbrook_hd2d'
OUT=ROOT/'art/lanternbrook_hd2d'
data=json.loads((BASE/'complete_data.json').read_text(encoding='utf8'))
blueprint=json.loads((BASE/'region_blueprint.json').read_text(encoding='utf8'))
forest=json.loads((BASE/'forest_placement.json').read_text(encoding='utf8'))
grass=json.loads((BASE/'understory_placement.json').read_text(encoding='utf8'))
R=Matrix(((1,0,0),(0,0,-1),(0,1,0)))
def convert(p):return R@Vector(p)
def collection(name):
    c=bpy.data.collections.new(name);bpy.context.scene.collection.children.link(c);return c
zones={key:collection('HD2D Complete '+key) for key in ['Entrance','Riverside','Ruins','Return','Transitions','Forest','Markers']}
for c in list(bpy.data.collections):
    if c.name=='HD2D Pixel woodland':
        for o in list(c.objects):bpy.data.objects.remove(o,do_unlink=True)
        bpy.data.collections.remove(c)
for o in bpy.context.scene.objects:
    if o.type=='MESH' and o.name.startswith(('TREE_Trunk','V1_TreeTrunk','V1_TreeBranch','V1_Ruin_brass_armillary')):
        o.hide_render=True;o.hide_set(True)
    if o.type=='MESH' and o.name.startswith('V1_PerimeterRock'):
        inv=o.matrix_world.inverted()
        for v in o.data.vertices:
            world=o.matrix_world@v.co
            factor=.28 if world.y<-28 or world.x>41 else .60
            world.z=.2+(world.z-.2)*factor
            v.co=inv@world

# Texture pass v2: use the same original authored/generated surface assets.
surface_files={'chestnut':'chestnut_handpainted_v2','oak':'chestnut_handpainted_v2',
 'limestone':'limestone_handpainted_v2','slate':'slate_mineral_v2',
 'plaster':'plaster_v2','earth':'forest_floor_v2','path':'path_soil_v2'}
manifest=json.loads((BASE/'art_pass.json').read_text(encoding='utf8'))
for old_name,kind in manifest['materials'].items():
    mat=bpy.data.materials.get(old_name.removeprefix('Engine_'))
    if not mat or not mat.use_nodes or kind not in surface_files:continue
    for node in mat.node_tree.nodes:
        if node.type=='TEX_IMAGE':
            node.image=bpy.data.images.load(str(BASE/'textures'/(surface_files[kind]+'.png')),check_existing=True)
            node.image.pack();node.interpolation='Closest'
        if node.type=='BSDF_PRINCIPLED':
            node.inputs['Roughness'].default_value={'slate':.72,'limestone':.88,'chestnut':.82,'oak':.79,'plaster':.97}.get(kind,.98)
    bsdf=next((n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
    tex=next((n for n in mat.node_tree.nodes if n.type=='TEX_IMAGE'),None)
    if bsdf and tex and kind in ['limestone','chestnut','oak','slate']:
        bump=mat.node_tree.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.12;bump.inputs['Distance'].default_value=.025
        mat.node_tree.links.new(tex.outputs['Color'],bump.inputs['Height']);mat.node_tree.links.new(bump.outputs['Normal'],bsdf.inputs['Normal'])
for mat in bpy.data.materials:
    if not mat.use_nodes:continue
    for node in mat.node_tree.nodes:
        if node.type=='BSDF_PRINCIPLED' and ('Amber windows' in mat.name or 'Lantern honey' in mat.name):
            node.inputs['Emission Strength'].default_value=1.7 if 'Amber' in mat.name else 2.7

colors={'brass':(.53,.43,.24,1),'iron':(.12,.19,.2,1),'honey':(1,.68,.30,1),'crystal':(.25,.74,.76,1),'paper':(.64,.62,.46,1),'moss':(.17,.26,.14,1)}
materials={}
def pixel_material(name,texture=None,color=(1,1,1,1),alpha=False):
    m=bpy.data.materials.new('Complete '+name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();l=m.node_tree.links
    p=n.new('ShaderNodeBsdfPrincipled');out=n.new('ShaderNodeOutputMaterial');l.new(p.outputs[0],out.inputs[0]);p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=.94
    if texture:
        image=bpy.data.images.load(str(BASE/'textures'/texture),check_existing=True);image.pack()
        tex=n.new('ShaderNodeTexImage');tex.image=image;tex.interpolation='Closest'
        if not alpha:
            tex.projection='BOX';tex.projection_blend=0
            coord=n.new('ShaderNodeNewGeometry');mapping=n.new('ShaderNodeVectorMath');mapping.operation='SCALE';mapping.inputs[3].default_value=.49
            l.new(coord.outputs['Position'],mapping.inputs[0]);l.new(mapping.outputs[0],tex.inputs['Vector'])
        l.new(tex.outputs['Color'],p.inputs['Base Color'])
        if alpha:
            l.new(tex.outputs['Alpha'],p.inputs['Alpha']);m.surface_render_method='DITHERED'
    if name in ['honey','crystal']:
        p.inputs['Emission Color'].default_value=color;p.inputs['Emission Strength'].default_value=1.8
    return m
for name,texture in {'timber':'chestnut','oak':'oak','slate':'slate','stone':'limestone','bark':'bark'}.items():materials[name]=pixel_material(name,texture+'.png')
for name,kind in {'timber':'chestnut','oak':'oak','slate':'slate','stone':'limestone'}.items():
    materials[name]=pixel_material(name+' TextureV2',surface_files[kind]+'.png')
for name,color in colors.items():materials[name]=pixel_material(name,color=color)
cliff=pixel_material('MossyCliff','limestone.png')
nodes=cliff.node_tree.nodes;links=cliff.node_tree.links
tex=next(n for n in nodes if n.type=='TEX_IMAGE');bsdf=next(n for n in nodes if n.type=='BSDF_PRINCIPLED')
mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=(.47,.63,.56,1)
links.new(tex.outputs['Color'],mix.inputs[1]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
for o in bpy.context.scene.objects:
    if o.type=='MESH' and o.name.startswith('V1_PerimeterRock'):
        o.data.materials.clear();o.data.materials.append(cliff)

def mesh_object(name,verts,faces,mat,zone='Forest',uv=False):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.materials.append(mat)
    if uv:
        layer=me.uv_layers.new(name='UVMap')
        for poly in me.polygons:
            for i,li in enumerate(poly.loop_indices):layer.data[li].uv=[(0,0),(1,0),(1,1),(0,1)][i]
    o=bpy.data.objects.new(name,me);zones[zone].objects.link(o);return o
def primitive(item):
    kind=item['kind'];sx,sy,sz=item['size'];name=item['name']
    if kind=='ring':
        verts=[];faces=[]
        for i in range(48):
            a=i*math.tau/48
            for j in range(6):
                b=j*math.tau/6;radius=sx+sy*math.cos(b)
                verts.append((radius*math.cos(a),radius*math.sin(a),sy*math.sin(b)))
        for i in range(48):
            for j in range(6):faces.append((i*6+j,((i+1)%48)*6+j,((i+1)%48)*6+(j+1)%6,i*6+(j+1)%6))
        obj=mesh_object(name,verts,faces,materials[item['material']],item['zone'])
    else:
        me=bpy.data.meshes.new(name);bm=bmesh.new()
        if kind=='box':
            bmesh.ops.create_cube(bm,size=1)
            for v in bm.verts:v.co.x*=sx;v.co.y*=sz;v.co.z*=sy
        elif kind=='cylinder':bmesh.ops.create_cone(bm,cap_ends=True,segments=10,radius1=sx*.5,radius2=sx*.42,depth=sy)
        else:
            bmesh.ops.create_uvsphere(bm,u_segments=8,v_segments=4,radius=sx*.5)
            for v in bm.verts:v.co.z*=sy/max(.001,sx)
        bm.to_mesh(me);bm.free();me.materials.append(materials[item['material']]);obj=bpy.data.objects.new(name,me);zones[item['zone']].objects.link(obj)
    obj.location=convert(item['position'])
    obj.rotation_euler=(R@Euler(item['rotation'],'YXZ').to_matrix()@R.transposed()).to_euler()
    return obj
for item in blueprint['props']:primitive(item)
if (BASE/'terrain_seam.json').exists():
    vertices=json.loads((BASE/'terrain_seam.json').read_text(encoding='utf8'))
    seam_mat=pixel_material('EarthApronSeam','earth.png')
    mesh_object('CompleteTerrainApronSeam',[convert(p) for p in vertices],[(i,i+1,i+2) for i in range(0,len(vertices),3)],seam_mat,'Transitions')

crown_materials={name:pixel_material(name,name,alpha=True) for name in ['woodland_crown.png','river_willow.png']}
for item in forest:
    width=item['width'];height=item['height'];center=Vector(item['position']);rot=Euler((-.55,.56,0),'YXZ').to_matrix()
    verts=[convert(center+rot@Vector(p)) for p in [(-width/2,-height/2,0),(width/2,-height/2,0),(width/2,height/2,0),(-width/2,height/2,0)]]
    mesh_object(item['name'],verts,[(0,1,2,3)],crown_materials[item['texture']],uv=True)
    sx,sy,sz=item['trunk_size'];primitive({'name':item['name']+'_Trunk','kind':'cylinder','position':item['trunk_position'],'size':[sx,sy,sz],'rotation':[0,0,0],'material':'bark','zone':'Forest'})

def sprite_batch(name,records,texture,size):
    mat=pixel_material(name,texture,alpha=True);verts=[];faces=[];rot=Euler((-.18,.56,0),'YXZ').to_matrix()
    for item in records:
        p=Vector(item['position']);s=item['scale'];w,h=size[0]*s,size[1]*s;a=len(verts)
        verts.extend([convert(p+rot@Vector(v)) for v in [(-w/2,-h/2,0),(w/2,-h/2,0),(w/2,h/2,0),(-w/2,h/2,0)]])
        faces.append((a,a+1,a+2,a+3))
    if verts:mesh_object(name,verts,faces,mat,'Transitions',True)
sprite_batch('RoadsideGrass',grass,'groundcover_handpainted_v2.png',(1.35,.56))
for kind in ['fern','reeds','blueflowers']:sprite_batch(kind,[x for x in blueprint['understory'] if x['kind']==kind],kind+'.png',(1.2,.8))
if (BASE/'texture_finish_data.json').exists():
    patches=json.loads((BASE/'texture_finish_data.json').read_text(encoding='utf8'))['leaf_patches']
    leaf_mat=pixel_material('TreeRootLeafLitter','leaf_litter_v2.png',alpha=True)
    vertices=[];faces=[]
    for item in patches:
        start=len(vertices);vertices.extend([convert(v) for v in item['corners']]);faces.append((start,start+3,start+2,start+1))
    mesh_object('TreeRootLeafLitter',vertices,faces,leaf_mat,'Forest',True)
for name,p in data['markers'].items():
    o=bpy.data.objects.new(name,None);o.empty_display_type='ARROWS';o.empty_display_size=.5;o.location=convert(p);zones['Markers'].objects.link(o)
for region in data['regions']:
    focus=Vector(region['position']);focus.y=max(1.1,focus.y);pitch=math.radians(20);direction=Vector((math.sin(.56)*math.cos(pitch),math.sin(pitch),math.cos(.56)*math.cos(pitch)))
    view_height=14.5 if region['id'] in ['riverside','return'] else 16
    camdata=bpy.data.cameras.new('CompleteCamera_'+region['id']);camdata.type='PERSP';camdata.sensor_fit='VERTICAL';camdata.sensor_height=24;camdata.lens=24*96/view_height
    cam=bpy.data.objects.new(camdata.name,camdata);zones['Markers'].objects.link(cam);cam.location=convert(focus+direction*96);cam.rotation_euler=(convert(focus)-cam.location).to_track_quat('-Z','Y').to_euler()
    if region['id']=='courtyard':bpy.context.scene.camera=cam
bpy.context.scene['HD2D_notes']='Complete outdoor map: six regions, original editable geometry, packed original pixel textures, original generated oak/willow crowns, source markers and cameras. Godot scene is authoritative for collision, navigation, mist, shader edge blending and animation.'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Lanternbrook_HD2D_Complete.blend'))
(OUT/'complete_source_report.json').write_text(json.dumps({'props':len(blueprint['props']),'trees':len(forest),'grass':len(grass),'understory':len(blueprint['understory']),'regions':len(data['regions']),'source':'Lanternbrook_HD2D_Complete.blend'},indent=2),encoding='utf8')
print('COMPLETE_BLENDER_SAVED')
