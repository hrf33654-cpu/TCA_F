import json, sys
from pathlib import Path
sys.path.insert(0, r'C:/Users/Lenovo/.codex/plugins/cache/frameronin-local/frameronin-imagegen/1.1.0')
from server.main import HANDLERS

BASE = Path(__file__).parent
STATE = BASE / 'local_state.json'
ROOT = 'E:/projects/TCA_ID'

if sys.argv[1] == 'init':
    names = ['front', 'front-left shallow 22.5 degrees', 'front-left three-quarter 45 degrees', 'left-front near profile 67.5 degrees', 'left profile 90 degrees facing screen left', 'left-back near profile 112.5 degrees', 'back-left three-quarter 135 degrees', 'back-left shallow 157.5 degrees', 'back 180 degrees', 'back-right shallow 202.5 degrees', 'back-right three-quarter 225 degrees', 'right-back near profile 247.5 degrees', 'right profile 270 degrees facing screen right', 'right-front near profile 292.5 degrees', 'front-right three-quarter 315 degrees', 'front-right shallow 337.5 degrees']
    result = HANDLERS['fr_create_task'](workspace_root=ROOT, name='oxygen-360-turnaround-v002', asset_type='directions', brief='Create a full 360 degree turntable of the exact Oxygen character from the user supplied v002 reference. Sixteen distinct views spaced by 22.5 degrees, same relaxed standing pose, same level orthographic camera, no walking. Reference image is authoritative for this task. Keep non-mirrored asymmetric costume: black cape on character anatomical LEFT shoulder, white puff sleeve on anatomical RIGHT arm; white flower vine and mint ruffles on anatomical RIGHT side of skirt, opposite cape. Preserve flat hand-drawn anime linework, restrained cel shading, black/white/pale mint palette, blue white hair streaks and small tilted flower hat. Full body on transparent background, no text or model-sheet layout. Body axis centered, shoes bottom at y=1440 and hat top about y=100 on a 1024x1536 canvas. Arms relaxed slightly away from torso as in reference, no motion except rigid change of viewing azimuth.', style='Match reference exactly: clean anime production model sheet, fine weighted linework, restrained cel shade. No 3D rendered or pixel aesthetic.', references=[{'path':str(Path(ROOT)/'06_资产开发/美术源文件/TASK-O04_氧礼服着装三视图/generations/tca_oxygen_formal_turnaround_v002.png'), 'role':'reference', 'description':'User explicitly selected v002 for this turntable; preserve its body, face and dress.'}], directions=names, animation={'frame_count':16,'durations_ms':[250]*16,'loop':True,'camera':'level orthographic fixed camera; character changes azimuth only'}, layout={'columns':4,'rows':4,'cell_width':1024,'cell_height':1536,'frame_count':16,'resampling':'lanczos','direction_convention':'0 front -> face turns toward screen LEFT -> left profile 90 -> back 180 -> right profile 270 -> front 360. Positive yaw reveals character anatomical LEFT/cape side. Angles are intended nominal views, not recovered 3D measurements.'}, alpha_required=True, output_dir=str(BASE/'交付'))
    plan=HANDLERS['fr_build_generation_plan'](workspace_root=ROOT,task_id=result['task_id'])
    STATE.write_text(json.dumps({'task':result,'plan':plan},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
elif sys.argv[1] == 'call':
    s=json.loads(STATE.read_text(encoding='utf-8'))
    payload=json.loads(Path(sys.argv[3]).read_text(encoding='utf-8-sig'))
    payload.setdefault('workspace_root', ROOT)
    payload.setdefault('task_id',s['task']['task_id'])
    result=HANDLERS[sys.argv[2]](**payload)
    Path(str(sys.argv[3])+'.result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
