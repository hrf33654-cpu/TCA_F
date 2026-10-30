import json,sys,shutil,subprocess
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent));from smooth_pass import ROOT,BASE,HANDLERS
s=json.loads((BASE/'smooth_v4_state.json').read_text(encoding='utf-8'));f=json.loads((BASE/'smooth_v4_final_state.json').read_text(encoding='utf-8'));c={'workspace_root':str(ROOT),'task_id':s['task']['task_id']};delivery=Path(s['task']['delivery_dir']);td=Path(s['task']['task_dir']);frames=f['frames'];timing=[1000/24]*192
seq=HANDLERS['fr_export_png_sequence'](**c,frame_paths=frames,durations_ms=timing,label='oxygen-192-transparent-png')
small=HANDLERS['fr_scale_frames'](**c,frame_paths=frames,factor=.5,mode='lanczos',label='gif-preview-half-size')
# Error-distributed 10ms GIF durations total exactly 8000ms. PNG retains 1/24s.
gif_ms=[round((i+1)*100/24)*10-round(i*100/24)*10 for i in range(192)]
gif=HANDLERS['fr_export_gif'](**c,frame_paths=[x['path'] for x in small['frames']],durations_ms=gif_ms,loop=True,label='oxygen-rotation-review')
contact=HANDLERS['fr_make_preview'](**c,frame_paths=[frames[i*8] for i in range(24)],columns=6,cell_width=256,cell_height=384,label='oxygen-rotation-24-keys')
video=delivery/'oxygen-360-review-v4.mp4';shutil.copy2(f['video'],video)
selected=[r['path'] for r in seq['delivery_files'] if r['path'].endswith('.png')]+[gif['gif'],contact['preview']]
HANDLERS['fr_select_deliverables'](**c,image_paths=selected,reason='Latest 192-frame review version after direct cleanup; preserve rejected versions. This selection does not approve visual quality.')
groups=[]
for name,paths,kind,w,h,count,durs,alpha in [('transparent-png',selected[:192],'frames',1024,1536,192,timing,True),('gif-preview',[gif['gif']],'preview',512,768,192,gif_ms,True),('key-contact',[contact['preview']],'preview',1536,1632,1,None,False)]:
 kw={'image_paths':paths,'artifact_kind':kind,'group_name':name,'expected_width':w,'expected_height':h,'expected_frame_count':count,'expected_alpha':alpha}
 if durs is not None:kw['durations_ms']=durs
 r=HANDLERS['fr_verify_delivery'](**c,**kw);groups.append({'group':name,'status':r['group_format_status'],'findings':r['findings']})
findings=['All 192 frames inspected as six filmstrips and critical transitions at native scale. Browser playback confirmed actual video rendering.','Major optical smears at two transitions were replaced with 12 direct ImageGen cleanup drawings. Rotation is much denser than original 16-frame candidate, but not production-smooth.','Remaining blockers: local garment/flower/hand detail flicker, uneven angular speed near back, posture and cloth contour variations around frames 57-63 and 137-144. Direct cleanup trades smearing for local temporal detail changes. Do not approve as a finished smooth turntable.','The 8s loop has no duplicated closure hold, but remaining decorative changes and mild loop-boundary contour change require temporal-consistent animation production. PNG preserves full alpha; GIF is 512x768 preview with quantized timing.']
for scope in ['visual','semantic']:HANDLERS['fr_record_visual_review'](**c,status='needs_fix',review_scope=scope,findings=findings,inspected_paths=selected+frames)
try:HANDLERS['fr_package_task'](**c)
except Exception as ex:package_status=str(ex)
probe=subprocess.run(['ffprobe','-v','error','-show_entries','stream=width,height,r_frame_rate,nb_frames,duration','-of','json',str(video)],capture_output=True,encoding='utf-8',check=True)
report={'task_id':c['task_id'],'parent_tasks':['fr-20261018-e857e438','fr-20261018-ea765584','fr-20261018-3804622d'],'status':'needs_fix','goal_achieved':False,'video':str(video),'gif':gif['delivery_files'][0]['path'],'frames_dir':str(Path(seq['delivery_files'][0]['path']).parent),'contact':contact['delivery_file']['path'],'format_checks':groups,'visual_findings':findings,'video_probe':json.loads(probe.stdout),'packaging':package_status,'next_requirement':'A workflow with explicit temporal pose/cloth consistency, or actual animation repair, rather than more unconstrained independent still generation.'}
(delivery/'review-status.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');(BASE/'latest_review_delivery.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=True))
