"""Bake static geometry into material batches for an engine-friendly GLB."""
import bpy, json, math
from pathlib import Path
from collections import defaultdict
from mathutils import Vector
from mathutils import noise
ROOT=Path(r'E:\TCA_F\TCA_WorldPrototype')
OUT=ROOT/'art'/'alchemist_hamlet'
DEST=ROOT/'world'/'environments'/'lanternbrook'
DEST.mkdir(parents=True,exist_ok=True)
S=bpy.context.scene
original=list(S.objects)
# Group the editable source file by authoring domain.
groups={}
for label in ['Architecture','Bridge and route','Landscape','Vegetation','Props','Water','Lighting and atmosphere','Camera']:
    c=bpy.data.collections.get(label) or bpy.data.collections.new(label)
    if c.name not in S.collection.children: S.collection.children.link(c)
    groups[label]=c
for o in original:
    n=o.name
    if o.type=='CAMERA' or 'focus' in n: label='Camera'
    elif o.type=='LIGHT' or n.startswith('ATMOSPHERE'):label='Lighting and atmosphere'
    elif n.startswith(('INN','Window','Door','Gable','Porch','Chimney','Shutter')):label='Architecture'
    elif n.startswith(('TREE','Birch','ENV_Meadow','ENV_Wildflower','River_reed','Planter')):label='Vegetation'
    elif n.startswith(('Bridge','Route')):label='Bridge and route'
    elif n.startswith(('Water','ENV_Jade','Firefly')):label='Water'
    elif n.startswith(('ENV_Terrain','CLIFF','Meadow','Riverbank','Moss')):label='Landscape'
    else:label='Props'
    for c in list(o.users_collection):c.objects.unlink(o)
    groups[label].objects.link(o)

# Static triangles are merged by domain and material. Preserve the original editable file.
deps=bpy.context.evaluated_depsgraph_get(); batches={}
for o in original:
    if o.type not in {'MESH','CURVE'} or o.name.startswith('ATMOSPHERE'):continue
    ev=o.evaluated_get(deps)
    me=ev.to_mesh()
    if not me:continue
    me.calc_loop_triangles()
    bucket=o.users_collection[0].name
    positions=[o.matrix_world@v.co for v in me.vertices]
    mats=list(me.materials)
    for tri in me.loop_triangles:
        ma=mats[tri.material_index] if mats and tri.material_index<len(mats) else None
        if ma is None:continue
        key=(bucket,ma.name)
        if key not in batches:batches[key]=[[],[],ma,[]]
        vs,fs,_,normals=batches[key]; a=len(vs)
        vs.extend([tuple(positions[i]) for i in tri.vertices]);fs.append((a,a+1,a+2))
        normal_matrix=o.matrix_world.to_3x3().inverted().transposed()
        normals.extend([tuple((normal_matrix@me.corner_normals[li].vector).normalized()) for li in tri.loops])
    ev.to_mesh_clear()
export_coll=bpy.data.collections.new('ENGINE_EXPORT'); S.collection.children.link(export_coll)
export_objs=[]
engine_materials={}
def engine_material(source):
    if source.name in engine_materials:return engine_materials[source.name]
    # GLTF cannot represent Blender's procedural Noise->ColorRamp graph.
    # Make an explicit PBR material, with a small packed albedo texture where needed.
    m=bpy.data.materials.new('Engine_'+source.name);m.use_nodes=True
    nd=m.node_tree.nodes;nd.clear();p=nd.new('ShaderNodeBsdfPrincipled');out=nd.new('ShaderNodeOutputMaterial');m.node_tree.links.new(p.outputs[0],out.inputs['Surface'])
    p.inputs['Base Color'].default_value=source.diffuse_color
    src=next((n for n in source.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None) if source.use_nodes else None
    if src:
        for key in ['Roughness','Metallic','Emission Color','Emission Strength','Coat Weight']:
            p.inputs[key].default_value=src.inputs[key].default_value
    has_noise=source.use_nodes and any(n.type=='TEX_NOISE' for n in source.node_tree.nodes)
    if has_noise:
        size=96;img=bpy.data.images.new('Albedo_'+source.name,width=size,height=size,alpha=False)
        img.colorspace_settings.name='sRGB'
        pixels=[];col=source.diffuse_color
        woody=any(k in source.name.lower() for k in ['wood','plank','beam','bark','chestnut','oak'])
        for yy in range(size):
            for xx in range(size):
                # Periodic value noise keeps the game texture seamless.
                u=xx/size*math.tau;v=yy/size*math.tau
                c=noise.noise_vector(Vector((math.cos(u)*2+math.sin(v)*.5,math.sin(u)*2+math.cos(v)*.5,math.sin(v)*2)))[0]
                factor=.90+c*.18
                if woody:factor*=.92+.08*math.sin(v*18+c*4)
                linear=[max(0,min(1,float(ch)*factor)) for ch in col[:3]]
                pixels.extend([12.92*c if c<=.0031308 else 1.055*c**(1/2.4)-.055 for c in linear]+[1.0])
        img.pixels.foreach_set(pixels);img.update();img.pack()
        tex=nd.new('ShaderNodeTexImage');tex.image=img;m.node_tree.links.new(tex.outputs['Color'],p.inputs['Base Color'])
    m.diffuse_color=source.diffuse_color;engine_materials[source.name]=m;return m
for (bucket,mname),(verts,faces,ma,normals) in batches.items():
    me=bpy.data.meshes.new(bucket+'_'+mname);me.from_pydata(verts,[],faces);me.materials.append(engine_material(ma));me.update()
    me.normals_split_custom_set_from_vertices(normals)
    uv=me.uv_layers.new(name='UVMap')
    for poly in me.polygons:
        normal=poly.normal;axis=max(range(3),key=lambda i:abs(normal[i]))
        for li in poly.loop_indices:
            co=me.vertices[me.loops[li].vertex_index].co
            pair=(co.y,co.z) if axis==0 else ((co.x,co.z) if axis==1 else (co.x,co.y))
            uv.data[li].uv=(pair[0]*.7,pair[1]*.7)
    o=bpy.data.objects.new(bucket+'_'+mname,me);export_coll.objects.link(o);export_objs.append(o)
for o in original:o.select_set(False)
for o in export_objs:o.select_set(True)
bpy.context.view_layer.objects.active=export_objs[0]
bpy.ops.export_scene.gltf(filepath=str(DEST/'lanternbrook.glb'),export_format='GLB',use_selection=True,export_apply=True,export_cameras=False,export_lights=False,export_extras=True)
report={'source_objects':len(original),'export_meshes':len(export_objs),'export_triangles':sum(len(o.data.polygons) for o in export_objs),'glb_bytes':(DEST/'lanternbrook.glb').stat().st_size,'render_style':'3D hand-built stylized environment for pixel-sprite integration','assets':'All environment geometry and materials original to this project. Blender MCP bridge is separate tooling.'}
(OUT/'export_report.json').write_text(json.dumps(report,indent=2),encoding='utf8')
# Keep only editable originals in the .blend, not the temporary flattened export.
for o in export_objs:
    me=o.data;bpy.data.objects.remove(o,do_unlink=True);bpy.data.meshes.remove(me)
bpy.data.collections.remove(export_coll)
for m in engine_materials.values():
    if m.users==0:bpy.data.materials.remove(m)
for o in original:o.select_set(False)
S.render.filepath=str(OUT/'renders'/'Lanternbrook_final.png')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Lanternbrook_HD2D.blend'))
print(json.dumps(report),flush=True)
