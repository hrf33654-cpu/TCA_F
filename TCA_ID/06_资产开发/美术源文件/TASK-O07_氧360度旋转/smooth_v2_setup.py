import json,sys
from pathlib import Path
ROOT=Path('E:/projects/TCA_ID');BASE=Path(__file__).parent
sys.path.insert(0,r'C:/Users/Lenovo/.codex/plugins/cache/frameronin-local/frameronin-imagegen/1.1.0')
from server.main import HANDLERS
old=ROOT/'.codex-imagegen/tasks/fr-20261018-e857e438';t=json.loads((old/'task.json').read_text(encoding='utf-8'));a={r['plan_id']:r for r in t['generation_records']}
angles=[0,22,35,60,90,110,155,165,180,205,225,250,270,292,320,340]
extra=[45,75,125,140,195,238,305,350]
refs=[{'path':str(old/a[f'direction-{i+1:02d}']['task_path']),'role':'reference','description':f'Previously generated key, approximate yaw {angle}; retain its generation provenance in parent task fr-20261018-e857e438.'} for i,angle in enumerate(angles)]
refs.append({'path':str(ROOT/'06_资产开发/美术源文件/TASK-O04_氧礼服着装三视图/generations/tca_oxygen_formal_turnaround_v002.png'),'role':'reference','description':'User-selected authoritative v002 original model sheet.'})
ordered=sorted(angles+extra)
r=HANDLERS['fr_create_task'](workspace_root=str(ROOT),name='oxygen-360-smooth-v2',asset_type='directions',brief='Continue parent turntable: repair eight intermediate views and reuse existing reviewed keys; produce a smooth looping 360-degree reference animation with 192 distinct temporal frames at 24fps, duration 8 seconds. Generated keys must preserve anatomical-left black cape and anatomical-right vine/ruffles and white puff sleeve. Same identity and clean hand-drawn anime style as user v002. Do not change camera pitch. Interpolation is local RIFE v4.6, explicitly derived, not new image generation. Full-alpha PNG sequence is authoritative. Do not approve morphing or double contours.',style='Original Oxygen clean fine-line anime, restrained cel shading, slim proportions. Black white pale mint and blue/white hair highlights. Neutral standing pose, orthographic level camera.',references=refs,directions=[f'yaw {angle} degrees, approximate intended heading' for angle in ordered],animation={'frame_count':192,'durations_ms':[1000/24]*192,'loop':True,'fps':24,'camera':'fixed orthographic level'},layout={'cell_width':1024,'cell_height':1536,'frame_count':192,'columns':16,'rows':12,'resampling':'lanczos','direction_convention':'front0 -> screen-left-profile90 -> back180 -> screen-right-profile270 -> front360; nominal key headings are approximate'},alpha_required=True,output_dir=str(BASE/'交付'))
p=HANDLERS['fr_build_generation_plan'](workspace_root=str(ROOT),task_id=r['task_id'])
for idx,angle in enumerate(ordered):
 if angle in angles:
  HANDLERS['fr_reuse_plan_reference'](workspace_root=str(ROOT),task_id=r['task_id'],plan_id=p['plans'][idx]['plan_id'],reference_index=angles.index(angle),reason='Reuse preserved earlier ImageGen key and retain parent provenance; selected for broad orientation/style, final motion still requires review.')
state={'task':r,'plan':p,'ordered_angles':ordered,'source_angles':angles,'new_angles':extra,'parent_task':'fr-20261018-e857e438'}
(BASE/'smooth_v2_state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'task':r,'new':[(x,p['plans'][ordered.index(x)]['plan_id']) for x in extra]},ensure_ascii=True))
