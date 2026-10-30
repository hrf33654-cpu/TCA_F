import bpy
from pathlib import Path
OUT=Path(r'E:\TCA_F\TCA_WorldPrototype\art\alchemist_hamlet');S=bpy.context.scene
ng=bpy.data.node_groups.get('Lanternbrook_soft_highlights');ng.nodes.clear()
rl=ng.nodes.new('CompositorNodeRLayers');rl.scene=S
gl=ng.nodes.new('CompositorNodeGlare')
if hasattr(gl,'glare_type'):
    gl.glare_type='FOG_GLOW';gl.quality='HIGH';gl.threshold=1.8;gl.mix=-.92
else:
    gl.inputs['Type'].default_value='Fog Glow'
    gl.inputs['Quality'].default_value='High'
    gl.inputs['Threshold'].default_value=1.8
    gl.inputs['Strength'].default_value=.16
    gl.inputs['Size'].default_value=.25
out=ng.nodes.new('NodeGroupOutput')
ng.links.new(rl.outputs['Image'],gl.inputs['Image']);ng.links.new(gl.outputs['Image'],out.inputs['Image'])
S.compositing_node_group=ng
S.render.filepath=str(OUT/'renders'/'Lanternbrook_preview_v02.png')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Lanternbrook_HD2D.blend'))
bpy.ops.render.render(write_still=True)
print('REFINEMENT_RENDER_COMPLETE',flush=True)
