import json, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from fr_local import HANDLERS, ROOT, BASE, STATE

state=json.loads(STATE.read_text(encoding='utf-8'))
task_id=state['task']['task_id']
common={'workspace_root':ROOT,'task_id':task_id}
task=HANDLERS['fr_get_task'](**common)
if 'task' in task: task=task['task']
latest={r['plan_id']:r for r in task['generation_records']}
task_dir=Path(state['task']['task_dir'])
paths=[str(task_dir/latest[f'direction-{i+1:02d}']['task_path']) for i in range(16)]
checks=[HANDLERS['fr_inspect_image'](image_path=p) for p in paths]
(BASE/'source_inspection.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
scaled=HANDLERS['fr_scale_frames'](**common, frame_paths=paths,factor=0.90,mode='lanczos',label='uniform-scale-090')
scaled_paths=[r['path'] for r in scaled['frames']]
normalized=HANDLERS['fr_normalize_frames'](**common,frame_paths=scaled_paths,canvas_width=1024,canvas_height=1536,anchor='bottom_center',baseline_y=1450,offsets=[{'x':0,'y':0}]*16,resampling='lanczos',label='standing-turntable')
frames=[r['path'] for r in normalized['frames']]
results={}
results['sequence']=HANDLERS['fr_export_png_sequence'](**common,frame_paths=frames,durations_ms=[250]*16,label='oxygen-360-png')
results['atlas']=HANDLERS['fr_assemble_atlas'](**common,frame_paths=frames,columns=4,rows=4,cell_width=1024,cell_height=1536,label='oxygen-360-atlas')
results['gif']=HANDLERS['fr_export_gif'](**common,frame_paths=frames,durations_ms=[250]*16,loop=True,label='oxygen-360-preview')
results['contact']=HANDLERS['fr_make_preview'](**common,frame_paths=frames,columns=4,cell_width=320,cell_height=480,label='oxygen-360-contact')
results['frames']=frames
(BASE/'export_state.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in results.items() if k!='frames'},ensure_ascii=False))
