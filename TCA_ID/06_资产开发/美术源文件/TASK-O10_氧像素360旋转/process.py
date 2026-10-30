import sys,json
from pathlib import Path
sys.path.insert(0,r'C:/Users/Lenovo/.codex/plugins/cache/frameronin-local/frameronin-imagegen/1.1.0')
from server.main import HANDLERS as H
B=Path(__file__).parent
s=json.loads((B/'state.json').read_text(encoding='utf-8')); c={'workspace_root':'E:/projects/TCA_ID','task_id':s['task']['task_id']}; td=Path(s['task']['task_dir'])
G=Path(r'C:/Users/Lenovo/.codex/generated_images/01a154b7-4e5b-7022-86ce-9718a26c3b9d')
rp=json.loads((B/'retry-prompts.json').read_text(encoding='utf-8'))
items=[(0,'exec-a149289b-892a-4af0-928b-64b9ebcfe82e.png',None),(1,'exec-bd3b73fc-e492-44a2-b55d-acfceba00091.png',None),(2,'exec-4bd87456-6c0b-4c2e-b6f9-5d24b58dda61.png',None),(3,'exec-33e5cb98-0346-4ead-82f0-c4dcb78c9d81.png',None),(2,'exec-f4f982b5-5866-4453-8ca6-9624edddb3c9.png','p3fix'),(3,'exec-1fecca72-bf0a-4abc-8612-a47ad964bc00.png','p4fix'),(3,'exec-1fd9ccb5-621c-4808-b00f-3ed9781e9bc5.png','p4fix2')]
active={}
for idx,file,key in items:
 p=s['plan']['plans'][idx]
 r=H['fr_record_generation'](**c,generated_file=str(G/file),label=f'group-{idx+1}-{key or "initial"}',plan_id=p['plan_id'],prompt_text=rp[key] if key else p['prompt'])
 active[idx]=str(td/r['record']['task_path'])
frames=[]
for i in range(4):
 H['fr_inspect_image'](image_path=active[i])
 r=H['fr_slice_grid'](**c,image_path=active[i],columns=2,rows=2,allow_remainder=False,label=f'group-{i+1}-cells')
 frames.extend(f['path'] for f in r['frames'])
# Manually reviewed hat tops and shoe contact lines, in original 512x768 cells.
tops=[1,3,3,3,32,28,20,20,26,28,17,18,26,28,16,18]
feet=[760,760,760,760,754,754,750,752,738,738,740,740,750,750,752,752]
axes=[256,256,263,266,278,258,270,270,285,260,294,270,280,250,286,250]
normalized=[]; transforms=[]
from PIL import Image
for i,f in enumerate(frames):
 factor=672/(feet[i]-tops[i])
 scaled=H['fr_scale_frames'](**c,frame_paths=[f],factor=factor,mode='nearest',label=f'frame-{i:02d}-scaled')
 path=scaled['frames'][0]['path']
 im=Image.open(path); w,h=im.size
 dx=max(0,min(512-w,256-round(axes[i]*factor)))-round((512-w)/2)
 dy=720-round(feet[i]*factor)-round((768-h)/2)
 r=H['fr_normalize_frames'](**c,frame_paths=[path],canvas_width=512,canvas_height=768,anchor='center',offsets=[{'x':dx,'y':dy}],resampling='nearest',label=f'frame-{i:02d}-aligned')
 normalized.append(r['frames'][0]['path']); transforms.append({'index':i,'reviewed_hat_top':tops[i],'reviewed_shoe_contact':feet[i],'reviewed_body_axis':axes[i],'scale':factor,'offset':{'x':dx,'y':dy},'nominal_yaw':i*22.5})
seq=H['fr_export_png_sequence'](**c,frame_paths=normalized,durations_ms=[200]*16,label='oxygen-pixel-360-frames')
atlas=H['fr_assemble_atlas'](**c,frame_paths=normalized,columns=4,rows=4,cell_width=512,cell_height=768,label='oxygen-pixel-360-atlas')
gif=H['fr_export_gif'](**c,frame_paths=normalized,durations_ms=[200]*16,loop=True,label='oxygen-pixel-360')
preview=H['fr_make_preview'](**c,frame_paths=normalized,columns=4,cell_width=256,cell_height=384,label='oxygen-pixel-360-contact')
state={'active':list(active.values()),'frames':normalized,'sequence':seq,'atlas':atlas,'gif':gif,'preview':preview,'transforms':transforms}
(B/'exports.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'gif':gif,'atlas':atlas,'preview':preview},ensure_ascii=False))

