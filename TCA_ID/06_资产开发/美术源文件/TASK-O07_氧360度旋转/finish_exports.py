import json, sys, subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageSequence
sys.path.insert(0,str(Path(__file__).parent))
from fr_local import HANDLERS, ROOT, BASE, STATE

s=json.loads(STATE.read_text(encoding='utf-8')); e=json.loads((BASE/'export_state.json').read_text(encoding='utf-8'))
c={'workspace_root':ROOT,'task_id':s['task']['task_id']}
delivery=Path(s['task']['delivery_dir'])
seq=e['sequence']['delivery_files'][:-1]
paths=[r['path'] for r in seq]
atlas=e['atlas'].get('atlas') or e['atlas'].get('atlas_path')
if not atlas:
    atlas=next(r['path'] for r in e['atlas']['delivery_files'] if r['path'].endswith('.png'))
gif=e['gif']['gif']; contact=e['contact']['preview']
selected=paths+[atlas,gif,contact]
selection=HANDLERS['fr_select_deliverables'](**c,image_paths=selected,reason='Select latest corrected 16-view reference sequence and matching atlas/GIF/contact. Earlier exports are preserved as rejected history, not final delivery.')
verification=[]
verification.append(HANDLERS['fr_verify_delivery'](**c,image_paths=paths,artifact_kind='frames',group_name='png-frames',expected_alpha=True,expected_frame_count=16,expected_width=1024,expected_height=1536,durations_ms=[250]*16,minimum_alpha_margin_px=24))
verification.append(HANDLERS['fr_verify_delivery'](**c,image_paths=[atlas],artifact_kind='atlas',group_name='atlas',expected_alpha=True,expected_frame_count=16,expected_width=4096,expected_height=6144,expected_columns=4,expected_rows=4,minimum_alpha_margin_px=24))
verification.append(HANDLERS['fr_verify_delivery'](**c,image_paths=[gif],artifact_kind='preview',group_name='gif-preview',expected_alpha=True,expected_frame_count=16,expected_width=1024,expected_height=1536,durations_ms=[250]*16))
verification.append(HANDLERS['fr_verify_delivery'](**c,image_paths=[contact],artifact_kind='preview',group_name='contact-preview',expected_frame_count=1,expected_width=1280,expected_height=2016))
rgb_dir=BASE/'视频预览帧';rgb_dir.mkdir(exist_ok=True)
for i,p in enumerate(paths):
    im=Image.open(p).convert('RGBA'); bg=Image.new('RGBA',im.size,'#e9e7e3'); bg.alpha_composite(im);bg.convert('RGB').save(rgb_dir/f'{i:04d}.png')
video=delivery/'oxygen-360-turntable.mp4'
if not video.exists():
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-n','-framerate','4','-i',str(rgb_dir/'%04d.png'),'-c:v','libx264','-crf','17','-preset','medium','-r','24','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True)
probe=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)],capture_output=True,text=True,encoding='utf-8',check=True)
(delivery/'video-inspection.json').write_text(probe.stdout,encoding='utf-8')
gif_frames=HANDLERS['fr_extract_frames'](**c,image_path=gif,label='gif-playback-review')
out=Image.new('RGB',(1280,2016),'#e9e7e3'); draw=ImageDraw.Draw(out)
with Image.open(gif) as g:
    for i,f in enumerate(ImageSequence.Iterator(g)):
        im=f.convert('RGBA');bg=Image.new('RGBA',im.size,'#e9e7e3');bg.alpha_composite(im);out.paste(bg.convert('RGB').resize((320,480)),((i%4)*320,(i//4)*504));draw.text(((i%4)*320+8,(i//4)*504+482),f'GIF frame {i:02d}',fill='black')
review=Path(s['task']['task_dir'])/'work/previews/final-gif-playback-review.jpg';out.save(review)
manifest={'task_id':c['task_id'],'reference':'TASK-O04 v002 explicitly supplied by user','frame_count':16,'frame_size':[1024,1536],'duration_ms':250,'cycle_seconds':4,'loop':True,'angle_note':'Yaw names are nominal requested targets; generated views are approximate, not geometrically measured. Camera is level as supplied reference, not exploration pitch.','frames':[{'index':i,'target_yaw_deg':i*22.5,'png':p,'prompt_plan':f'direction-{i+1:02d}'} for i,p in enumerate(paths)],'mp4':str(video),'gif':gif,'atlas':atlas,'contact':contact,'visual_limitations':['Flower number, vine routing, dress fold pattern, glove/hand and hat details vary across views.','Some intermediate yaw steps are uneven; this is a generated directional-reference candidate, not a rigid 3D model turntable or approved production animation.','Original PNGs retain full alpha; GIF has binary transparency, MP4 has a neutral preview background.'],'prompt_source':str(Path(s['task']['task_dir'])/'task.json')}
(delivery/'rotation-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(BASE/'final_delivery_state.json').write_text(json.dumps({'selected':selected,'verification':[{'group':r['group_name'],'status':r['group_format_status'],'findings':r['findings']} for r in verification],'manifest':manifest,'gif_review':str(review),'gif_extracted':gif_frames},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'selected':selected,'verification':[{'group':r['group_name'],'status':r['group_format_status'],'findings':r['findings']} for r in verification],'video':str(video),'gif_review':str(review)},ensure_ascii=False))
