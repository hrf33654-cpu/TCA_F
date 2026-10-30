import json,sys
from pathlib import Path
ROOT=Path('E:/projects/TCA_ID');BASE=Path(__file__).parent
sys.path.insert(0,r'C:/Users/Lenovo/.codex/plugins/cache/frameronin-local/frameronin-imagegen/1.1.0');from server.main import HANDLERS
from server import assurance
s=json.loads((BASE/'smooth_v3_state.json').read_text(encoding='utf-8'));old=Path(s['task']['task_dir']);t=json.loads((old/'task.json').read_text(encoding='utf-8'));a=assurance.active_results(t,old)
fix=[57,58,59,61,62,63,137,138,139,141,142,143]
refs=[{'path':str(old/a[p['plan_id']]['task_path']),'role':'reference','description':p['label']+'; exact source provenance retained in parent fr-20261018-3804622d.'} for p in s['plans']]
r=HANDLERS['fr_create_task'](workspace_root=str(ROOT),name='oxygen-360-smooth-v4',asset_type='directions',brief='Finish smooth 192-frame 24fps Oxygen 360-degree turntable using existing 26 source keys and direct ImageGen cleanup of 12 remaining damaged motion frames. These 12 drawings replace failed optical interpolation; do not re-interpolate or crossfade them. Same user v002 character, asymmetry, level camera, neutral standing pose and transparent native PNG 1024x1536. Preserve all history and report any actual remaining defect.',style='Fine clean anime linework and restrained cel shading. Original Oxygen black/white/mint dress, left cape and right sleeve/vine.',references=refs,directions=[p['label'] for p in s['plans']]+[f'direct cleanup output frame {f}, same geometry and angle' for f in fix],animation={'frame_count':192,'durations_ms':[1000/24]*192,'fps':24,'loop':True},layout={'cell_width':1024,'cell_height':1536,'frame_count':192,'columns':16,'rows':12,'resampling':'lanczos','direction_convention':'front-left-back-right-front; headings approximate, actual playback frames authoritative'},alpha_required=True,output_dir=str(BASE/'交付'))
p=HANDLERS['fr_build_generation_plan'](workspace_root=str(ROOT),task_id=r['task_id'])
for i in range(26):HANDLERS['fr_reuse_plan_reference'](workspace_root=str(ROOT),task_id=r['task_id'],plan_id=p['plans'][i]['plan_id'],reference_index=i,reason='Reuse immutable prior generation source. Source quality and final motion are still reviewed independently; no new generation claimed.')
out={'task':r,'plans':[{'plan_id':x['plan_id'],'label':x['label']} for x in p['plans']],'fix_frames':fix,'parent':s['task']['task_id']}
(BASE/'smooth_v4_state.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,ensure_ascii=True))
