import sys,json,shutil
from pathlib import Path
sys.path.insert(0,r'C:/Users/Lenovo/.codex/plugins/cache/frameronin-local/frameronin-imagegen/1.1.0')
from server.main import HANDLERS as H
B=Path(__file__).parent;s=json.loads((B/'state.json').read_text(encoding='utf-8'));r=json.loads((B/'checks.json').read_text(encoding='utf-8'));c={'workspace_root':'E:/projects/TCA_ID','task_id':s['task']['task_id']};td=Path(s['task']['task_dir']);delivery=Path(r['delivery'])
for name in ['oxygen-pixel-360.mp4','rotation-manifest.json','说明.txt']:
 shutil.copy2(delivery/name,td/'exports'/name)
paths=r['selected']+r['active']+[r['gif_review']]
H['fr_record_visual_review'](**c,status='pass',review_scope='visual',inspected_paths=paths,findings=['Reviewed all 16 final PNG figures through full atlas and contact sheet; separately opened left profile, back, right profile, near-front and GIF. Inspected all four active raw 2x2 sources.','Full bodies stay inside canvas. Reviewed hat tops, shoe contacts and manual body axes; full-alpha PNGs retained. Black cape, white sleeve and floral skirt retained on fixed physical sides.','All GIF frames decoded and viewed in playback contact sheet. No blank frames; final-to-first returns from near-front to front.','Qualified preview quality: small rose, face, hat, fold and silhouette variations remain. Fine low-alpha edge fringe exists in PNGs; GIF edges are binary. Frame 4-to-5 has a larger angle jump. This pass is for a complete generated turntable preview, not production acceptance.'])
H['fr_record_visual_review'](**c,status='pass',review_scope='semantic',inspected_paths=paths,findings=['Visually confirmed ordered complete revolution: front, front-left, left profile, rear-left, back, rear-right, right profile, front-right, then front. Head and torso direction in repaired group 3 agree.','Reference identity cues retained: short dark-blue hair, pale blue streaks, tilted flower hat, mint-white black gown, blue gems. No image mirroring used; cape stays anatomical left and flower cascade anatomical right.','Yaw labels are nominal targets, not measured angles: several steps are uneven, particularly frames 4-to-5, and some near-front views differ less than requested 22.5 degrees.','Loop covers a complete circle and connects near-front to front; minor feature changes remain at the seam. This is a reviewable 16-frame animation candidate, not a rigid 3D turntable or approved engine asset.'])
p=H['fr_package_task'](**c)
(B/'package-result.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
# Convenient compact delivery ZIP containing only usable final assets plus timing, layout and limitations.
import zipfile
compact=delivery/'oxygen-pixel-360-assets.zip'
with zipfile.ZipFile(compact,'x',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(delivery.rglob('*')):
  if f.is_file() and f.suffix.lower()!='.zip' and 'gif-playback-contact' not in f.name: z.write(f,f.relative_to(delivery))
print(json.dumps({'task_id':p['task_id'],'status':p['validation']['overall_status'],'package':p['package'],'compact':str(compact),'delivery':str(delivery)},ensure_ascii=False))
