import sys,json
from pathlib import Path
sys.path.insert(0,r'C:/Users/Lenovo/.codex/plugins/cache/frameronin-local/frameronin-imagegen/1.1.0')
from server.main import HANDLERS
B=Path(r'E:/projects/TCA_ID/06_资产开发/美术源文件/TASK-O10_氧像素360旋转')
root='E:/projects/TCA_ID'
brief='Create a 360-degree in-place turntable of the exact pixel-art Oxygen woman in the supplied front/side/back reference. Fixed level orthographic camera; relaxed standing pose unchanged. Preserve slender adult proportions, short dark hair with blue-white streaks, tilted black miniature hat with white roses and mint ribbons, cyan gem at collar, black gloves, long black gown and mint-white drapery. Anatomical LEFT arm has the BLACK CAPE; anatomical RIGHT arm has the WHITE PUFF sleeve. White rose vine and cascading white ruffles run down anatomical RIGHT skirt side (opposite cape). These are fixed physical sides, NEVER mirror. At FRONT cape is screen RIGHT and rose cascade screen LEFT; at BACK cape is screen LEFT and rose cascade screen RIGHT. Reference side is face toward screen LEFT, showing cape side. No walking, no pose changes, no camera movement, no text, no labels. Crisp detailed pixel clusters and dark stepped outlines matching reference. Each generation is a compact four-pose 2x2 sheet, requested 1024x1536, cell512x768. Full figure per cell: hat top y48, shoe bottom y720, body vertical center axis x256. Final delivery combines four sheets into 16-frame cycle, final 4x4 atlas. Read each generated sheet TOP LEFT, TOP RIGHT, BOTTOM LEFT, BOTTOM RIGHT. Transparent background, no checkerboard, no ground shadows. Maintain identical height, costume volume and footing across all views.'
poses=[]
for g in range(4):
 angles=[(g*4+i)*22.5 for i in range(4)]
 descriptions=[]
 for a in angles:
  if a==0: desc='exact FRONT, face square to viewer'
  elif a<90: desc=f'FRONT turning face toward screen LEFT by {a} degrees, progressively reveal cape side'
  elif a==90: desc='EXACT LEFT-FACING PROFILE, nose points screen LEFT, cape side nearest viewer'
  elif a<180: desc=f'BACK-LEFT view yaw {a}, face increasingly hidden, cape side nearest'
  elif a==180: desc='EXACT BACK, NO face visible; cape screen LEFT, rose cascade screen RIGHT'
  elif a<270: desc=f'BACK-RIGHT view yaw {a}, white puff sleeve/rose side nearest'
  elif a==270: desc='EXACT RIGHT-FACING PROFILE, nose points screen RIGHT, white puff sleeve/rose side nearest, cape far side'
  else: desc=f'FRONT-RIGHT view yaw {a}, face returns toward viewer, white sleeve/rose side nearest'
  descriptions.append(desc)
 poses.append({'frame_index':g+1,'description':'Generate ONLY these FOUR full-body views as 2x2 equal cells in row-major order: '+'; '.join(descriptions)+'. All four must differ in facing exactly as specified.'})
t=HANDLERS['fr_create_task'](workspace_root=root,name='oxygen-pixel-360-v001',asset_type='animation',brief=brief,style='High-detail pixel art exactly matching attached reference. No smooth illustration, no chibi, no 3D render. Nearest-neighbor only for later scaling.',references=[{'path':r'C:/Users/Lenovo/AppData/Local/Temp/codex-clipboard-2873bba3-c136-4eb3-acde-60f0cbfe069b.png','role':'reference','description':'User supplied authoritative pixel three-view character design.'}],animation={'mode':'keyframes','frame_count':16,'key_poses':poses,'durations_ms':[200]*16,'loop':True,'camera':'fixed orthographic level','direction':'front -> screen left -> back -> screen right -> front','baseline_y':720},layout={'columns':4,'rows':4,'cell_width':512,'cell_height':768,'frame_count':16,'resampling':'nearest','generation_layout':'Each plan generates one 2x2 group, 1024x1536; delivery atlas is 4x4.'},alpha_required=True,output_dir=str(B/'交付'))
p=HANDLERS['fr_build_generation_plan'](workspace_root=root,task_id=t['task_id'])
(B/'state.json').write_text(json.dumps({'task':t,'plan':p},ensure_ascii=False,indent=2),encoding='utf-8')
for i,plan in enumerate(p['plans']): (B/f'prompt-{i+1}.txt').write_text(plan['prompt'],encoding='utf-8')
print(json.dumps(t,ensure_ascii=False)); print(p['plans'][0]['prompt'])
