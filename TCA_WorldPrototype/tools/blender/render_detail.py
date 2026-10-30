import bpy
from mathutils import Vector
from pathlib import Path
OUT=Path(r'E:\TCA_F\TCA_WorldPrototype\art\alchemist_hamlet');S=bpy.context.scene
hero=S.camera;resolution=(S.render.resolution_x,S.render.resolution_y)
data=bpy.data.cameras.new('CAM_Detail_Mill');cam=bpy.data.objects.new('CAM_Detail_Mill',data);S.collection.objects.link(cam)
cam.location=(-15,-22,17);cam.rotation_euler=(Vector((1,2.0,2.0))-cam.location).to_track_quat('-Z','Y').to_euler()
data.type='ORTHO';data.ortho_scale=21.5;S.camera=cam
S.render.resolution_x=1800;S.render.resolution_y=1350
S.render.filepath=str(OUT/'renders'/'Lanternbrook_reverse_view.png')
bpy.ops.render.render(write_still=True)
S.camera=hero;S.render.resolution_x,S.render.resolution_y=resolution
S.render.filepath=str(OUT/'renders'/'Lanternbrook_final.png')
# Do not overwrite the source after the separately grouped export save.
print('REVERSE_VIEW_RENDER_COMPLETE',flush=True)
