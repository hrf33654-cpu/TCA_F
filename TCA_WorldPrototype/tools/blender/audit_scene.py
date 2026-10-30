import bpy,json
from pathlib import Path
root=Path(r'E:\TCA_F\TCA_WorldPrototype');out=root/'art'/'alchemist_hamlet';s=bpy.context.scene
report={'file':bpy.data.filepath,'blender_version':bpy.app.version_string,'objects':len(s.objects),'mesh_objects':sum(o.type=='MESH' for o in s.objects),'source_polygons':sum(len(o.data.polygons) for o in s.objects if o.type=='MESH'),'collections':{c.name:len(c.objects) for c in s.collection.children},'camera':s.camera.name if s.camera else None,'resolution':[s.render.resolution_x,s.render.resolution_y],'has_characters':False,'character_note':'No character geometry or sprites were authored or imported.','render_files':{}}
for path in sorted((out/'renders').glob('*.png')):
    im=bpy.data.images.load(str(path),check_existing=False)
    report['render_files'][path.name]={'width':im.size[0],'height':im.size[1],'bytes':path.stat().st_size}
    bpy.data.images.remove(im)
report['glb_bytes']=(root/'world'/'environments'/'lanternbrook'/'lanternbrook.glb').stat().st_size
(out/'audit_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
(out/'build_stats.json').write_text(json.dumps({k:report[k] for k in ['objects','mesh_objects','source_polygons','camera','resolution']},indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False))
