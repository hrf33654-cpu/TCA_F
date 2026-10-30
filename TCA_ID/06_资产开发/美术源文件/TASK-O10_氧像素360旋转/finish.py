import sys,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageSequence
sys.path.insert(0,r'C:/Users/Lenovo/.codex/plugins/cache/frameronin-local/frameronin-imagegen/1.1.0')
from server.main import HANDLERS as H
B=Path(__file__).parent;s=json.loads((B/'state.json').read_text(encoding='utf-8'));e=json.loads((B/'exports.json').read_text(encoding='utf-8'));c={'workspace_root':'E:/projects/TCA_ID','task_id':s['task']['task_id']};td=Path(s['task']['task_dir']);delivery=Path(s['task']['delivery_dir'])
frames=[f['path'] for f in e['sequence']['delivery_files'] if f['path'].endswith('.png')]
atlas=e['atlas']['delivery_files'][0]['path'];gif=e['gif']['delivery_files'][0]['path'];contact=e['preview']['delivery_file']['path']
rgb=td/'work/video-frames';rgb.mkdir(exist_ok=True)
for i,p in enumerate(frames):
 im=Image.open(p).convert('RGBA');bg=Image.new('RGBA',im.size,'#e5e3df');bg.alpha_composite(im);bg.convert('RGB').save(rgb/f'{i:04d}.png')
video=delivery/'oxygen-pixel-360.mp4'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-n','-framerate','5','-i',str(rgb/'%04d.png'),'-c:v','libx264','-crf','17','-r','30','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True)
gifex=H['fr_extract_frames'](**c,image_path=gif,label='gif-playback-review')
gifcontact=H['fr_make_preview'](**c,frame_paths=[f['path'] for f in gifex['frames']],columns=4,cell_width=192,cell_height=288,label='gif-playback-contact')
selected=frames+[atlas,gif,contact]
H['fr_select_deliverables'](**c,image_paths=selected,reason='Final 16 aligned RGBA PNGs, 4x4 atlas, exact-timing loop GIF and contact sheet. Diagnostic GIF playback contact excluded; all raw drafts preserved.')
checks=[]
checks.append(H['fr_verify_delivery'](**c,image_paths=frames,artifact_kind='frames',group_name='png-frames',expected_alpha=True,expected_frame_count=16,expected_width=512,expected_height=768,durations_ms=[200]*16,minimum_alpha_margin_px=16,margin_alpha_threshold=128))
checks.append(H['fr_verify_delivery'](**c,image_paths=[atlas],artifact_kind='atlas',group_name='atlas',expected_alpha=True,expected_frame_count=16,expected_width=2048,expected_height=3072,expected_columns=4,expected_rows=4,minimum_alpha_margin_px=16,margin_alpha_threshold=128))
checks.append(H['fr_verify_delivery'](**c,image_paths=[gif],artifact_kind='preview',group_name='gif',expected_alpha=True,expected_frame_count=16,expected_width=512,expected_height=768,durations_ms=[200]*16))
checks.append(H['fr_verify_delivery'](**c,image_paths=[contact],artifact_kind='preview',group_name='contact',expected_frame_count=1,expected_width=1024,expected_height=1632))
manifest={'task_id':c['task_id'],'frame_count':16,'frame_size':[512,768],'atlas_size':[2048,3072],'durations_ms':[200]*16,'loop':True,'cycle_seconds':3.2,'order':'front -> screen left profile -> back -> screen right profile -> front','yaw_note':'22.5-degree targets are nominal; generated views are approximate and angular steps are not uniform.','transforms':e['transforms'],'limitations':['Rose shapes, hat ornaments, face and folds vary slightly across views.','Some angular steps are uneven, notably profile-to-back; first-to-last transitions contain minor detail changes.','This is a complete generated 2D turntable preview, not a rigid 3D model or engine-approved animation.','GIF has binary transparency. PNG sequence retains full RGBA alpha. MP4 uses a neutral background.']}
(delivery/'rotation-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(delivery/'说明.txt').write_text('氧像素角色完整360度旋转预览\n16帧，512×768，200毫秒/帧，3.2秒循环。\n方向：正面→朝屏幕左侧→背面→朝屏幕右侧→正面。\nPNG保留透明通道；4×4图集2048×3072；GIF循环；MP4为中性底色单圈视频。\n目标22.5度为名义角度，实际步进并非严格等角。花朵、帽饰、裙褶与脸部有逐帧细微差异，部分转向间隔不均匀。此为完整逐帧预览，非3D刚性模型转台或引擎验收资产。\n任务：'+c['task_id'],encoding='utf-8')
(B/'checks.json').write_text(json.dumps({'selected':selected,'active':e['active'],'checks':checks,'gif_review':gifcontact['preview'],'video':str(video),'delivery':str(delivery)},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'checks':[{'group':r['group_name'],'status':r['group_format_status'],'findings':r['findings']} for r in checks],'gif_review':gifcontact['preview'],'video':str(video)},ensure_ascii=False))
