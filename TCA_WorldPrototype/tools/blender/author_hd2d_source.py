"""Save an editable HD2D sibling; keep the previous map source intact."""
import bpy, json, math
from pathlib import Path
from mathutils import Vector
ROOT=Path(r'E:\TCA_F\TCA_WorldPrototype')
BASE=ROOT/'world/maps/lanternbrook_hd2d'
OUT=ROOT/'art/lanternbrook_hd2d';OUT.mkdir(parents=True,exist_ok=True)
data=json.loads((ROOT/'world/maps/lanternbrook/map_data.json').read_text(encoding='utf8'))
manifest=json.loads((BASE/'art_pass.json').read_text(encoding='utf8'))
for original,texture in manifest['materials'].items():
    material=bpy.data.materials.get(original.removeprefix('Engine_'))
    if not material:continue
    material.use_nodes=True;nodes=material.node_tree.nodes;nodes.clear()
    output=nodes.new('ShaderNodeOutputMaterial');bsdf=nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Roughness'].default_value=.94
    tex=nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(BASE/'textures'/f'{texture}.png'),check_existing=True)
    tex.interpolation='Closest';tex.projection='BOX';tex.projection_blend=0
    coord=nodes.new('ShaderNodeNewGeometry');mapping=nodes.new('ShaderNodeVectorMath');mapping.operation='SCALE';mapping.inputs[3].default_value=.49
    links=material.node_tree.links;links.new(coord.outputs['Position'],mapping.inputs[0]);links.new(mapping.outputs[0],tex.inputs['Vector'])
    links.new(tex.outputs['Color'],bsdf.inputs['Base Color']);links.new(bsdf.outputs[0],output.inputs['Surface'])
    tex.image.pack()

for o in list(bpy.context.scene.objects):
    if o.type=='MESH' and any(t in o.name for t in ['Foliage','Individual_leaf','Layered_fir','Canopy','Meadow']):
        o.hide_render=True;o.hide_set(True)
collection=bpy.data.collections.new('HD2D Pixel woodland');bpy.context.scene.collection.children.link(collection)
image=bpy.data.images.load(str(BASE/'textures/woodland_crown.png'),check_existing=True);image.pack()
mat=bpy.data.materials.new('HD2D Pixel crown');mat.use_nodes=True
nodes=mat.node_tree.nodes;nodes.clear();bsdf=nodes.new('ShaderNodeBsdfPrincipled');output=nodes.new('ShaderNodeOutputMaterial');mat.node_tree.links.new(bsdf.outputs[0],output.inputs['Surface']);tex=nodes.new('ShaderNodeTexImage');tex.image=image;tex.interpolation='Closest'
mat.node_tree.links.new(tex.outputs['Color'],bsdf.inputs['Base Color']);mat.node_tree.links.new(tex.outputs['Alpha'],bsdf.inputs['Alpha'])
bsdf.inputs['Roughness'].default_value=1
mat.surface_render_method='DITHERED'
def godot_to_blender(p):return (p[0],-p[2],p[1])
count=0
for item in data['colliders']:
    if item['kind']!='trunk':continue
    p=item['position'];height=item['size'][1];width=max(3.5,min(9,height*.95+1.7));hh=width*.91
    center=(p[0],p[1]+height*.42,p[2]);verts=[]
    for x,y in [(-width/2,-hh/2),(width/2,-hh/2),(width/2,hh/2),(-width/2,hh/2)]:
        yy=y*math.cos(.55);zz=-y*math.sin(.55)
        xx=x*math.cos(.56)+zz*math.sin(.56);zz=-x*math.sin(.56)+zz*math.cos(.56)
        verts.append(godot_to_blender((center[0]+xx,center[1]+yy,center[2]+zz)))
    me=bpy.data.meshes.new(f'PixelCrown_{count:03}');me.from_pydata(verts,[],[(0,1,2,3)]);me.materials.append(mat)
    uv=me.uv_layers.new(name='UVMap')
    for loop,co in zip(uv.data,[(0,0),(1,0),(1,1),(0,1)]):loop.uv=co
    obj=bpy.data.objects.new(me.name,me);collection.objects.link(obj);count+=1
# Keep visible trunks beneath the illustrated crown, matching the real-time art pass.
for o in bpy.context.scene.objects:
    if o.type=='MESH' and o.name.startswith(('TREE_Trunk','V1_TreeTrunk')):
        original_height=o.dimensions.z
        o.scale.z*=.72
        o.location.z-=original_height*.14
focus=Vector((3,1.3,1));direction=Vector((math.sin(.56)*math.cos(.55),math.sin(.55),math.cos(.56)*math.cos(.55)))
cam=bpy.context.scene.camera
cam.location=godot_to_blender(focus+direction*68)
target=Vector(godot_to_blender(focus));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=32
bpy.context.scene['HD2D_notes']='Pixel textured inn, bridge, leaf-card woodland; Godot scene is the authoritative real-time lighting and groundcover version. Previous map source unchanged.'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Lanternbrook_HD2D_ArtPass.blend'))
(OUT/'source_report.json').write_text(json.dumps({'pixel_crowns':count,'materials':manifest['materials'],'source':str(OUT/'Lanternbrook_HD2D_ArtPass.blend')},indent=2),encoding='utf8')
print('HD2D_BLENDER_SAVED',count)
