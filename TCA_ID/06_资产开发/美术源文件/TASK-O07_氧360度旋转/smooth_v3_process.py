import json,sys,shutil,hashlib
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).parent))
from smooth_pass import ROOT,BASE,np,interpolate,HANDLERS
from server import pipeline,assurance
s=json.loads((BASE/'smooth_v3_state.json').read_text(encoding='utf-8'));td=Path(s['task']['task_dir']);c={'workspace_root':str(ROOT),'task_id':s['task']['task_id']}
old=ROOT/'.codex-imagegen/tasks/fr-20261018-ea765584/work/smooth-native01';work=td/'work'/'smooth-native02';work.mkdir(exist_ok=True)
for kind in ['keys','rgb-input','alpha-input','rgb-out','alpha-out','rgba','rgb-review']:(work/kind).mkdir(exist_ok=True)
t=json.loads((td/'task.json').read_text(encoding='utf-8'));act=assurance.active_results(t,td);raw=[td/act[p['plan_id']]['task_path'] for p in s['plans']]
norm=HANDLERS['fr_normalize_frames'](**c,frame_paths=[str(p) for p in raw[24:]],canvas_width=1024,canvas_height=1536,anchor='center',offsets=[{'x':0,'y':0}]*2,label='repaired-midpoints')
bridges={60:Path(norm['frames'][0]['path']),140:Path(norm['frames'][1]['path'])};key_sources=[]
for k in range(48):
 frame=k*4
 source=bridges.get(frame) or (old/'keys'/f'{frame//8:04d}.png' if frame%8==0 else old/'rgba'/f'{frame:04d}.png')
 im=Image.open(source).convert('RGBA');im.save(work/'keys'/f'{k:04d}.png');arr=np.asarray(im,dtype=np.float32);a=arr[:,:,3:4]/255
 Image.fromarray(np.rint(arr[:,:,:3]*a).astype(np.uint8)).save(work/'rgb-input'/f'{k:04d}.png');aa=im.getchannel('A');Image.merge('RGB',(aa,aa,aa)).save(work/'alpha-input'/f'{k:04d}.png')
 key_sources.append({'frame':frame,'path':str(source),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'generation_key_indices':([24] if frame==60 else [25] if frame==140 else [frame//8,(frame//8+1)%24])})
for kind in ['rgb-input','alpha-input']:shutil.copy2(work/kind/'0000.png',work/kind/'0048.png')
with pipeline._task_lock(td):
 task=pipeline._load_task(td)
 for k,rec in enumerate(key_sources):assurance.lineage(task,td,[work/'keys'/f'{k:04d}.png'],[raw[i] for i in rec['generation_key_indices']])
 task.setdefault('coordinate_mappings',[]).append({'operation':'reuse-normalized-parent-and-redraw-midpoints','parent_task':'fr-20261018-ea765584','parent_transform_file':str(ROOT/'06_资产开发/美术源文件/TASK-O07_氧360度旋转/smooth-native01-state.json'),'source_keys':key_sources,'all_transforms':'Parent normalized keys and RIFE midpoints preserve exact canvases; two new ImageGen mids normalized center with no scale or offset.'})
 pipeline._event(task,'stage_repaired_keyframes',key_sources,{'key_count':48,'work':str(work)});pipeline._save_task(td,task)
interpolate(work,192)
with pipeline._task_lock(td):
 task=pipeline._load_task(td);outs=sorted((work/'rgba').glob('*.png'))
 for i,dest in enumerate(outs):k=i//4;assurance.lineage(task,td,[dest],[work/'keys'/f'{k:04d}.png',work/'keys'/f'{(k+1)%48:04d}.png'])
 task.setdefault('coordinate_mappings',[]).append({'operation':'local_rife_interpolation','model':'rife-v4.6','tta':'temporal','alpha_method':'premultiplied RGB + alpha interpolation then unpremultiply','key_count':48,'source_key_paths':[str(work/'keys'/f'{k:04d}.png') for k in range(48)],'frame_count':192,'fps':24,'closed_loop_sampling':'49 input keys including repeated closure, generate196, deliver first192; no repeated closure hold','mirror':False})
 pipeline._event(task,'local_rife_interpolation',{'keys':48},{'frames':192,'work':str(work)},['Derived intermediate frames, never declared new ImageGen calls.']);pipeline._save_task(td,task)
(BASE/'smooth-native02-state.json').write_text(json.dumps({'task_id':c['task_id'],'work':str(work),'frames':[str(p) for p in outs]},ensure_ascii=False,indent=2),encoding='utf-8')
