import json,sys,shutil,hashlib
from pathlib import Path
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path(__file__).parent))
from smooth_pass import ROOT,BASE,HANDLERS,np,interpolate
sys.path.insert(0,r'C:/Users/Lenovo/.codex/plugins/cache/frameronin-local/frameronin-imagegen/1.1.0')
from server import pipeline,assurance

s=json.loads((BASE/'smooth_v2_state.json').read_text(encoding='utf-8'));td=Path(s['task']['task_dir']);c={'workspace_root':str(ROOT),'task_id':s['task']['task_id']}
name=sys.argv[1];width=int(sys.argv[2]);height=int(sys.argv[3]);work=td/'work'/name;work.mkdir(exist_ok=True)
for kind in ['keys','rgb-input','alpha-input','rgb-out','alpha-out','rgba','rgb-review']:(work/kind).mkdir(exist_ok=True)
t=json.loads((td/'task.json').read_text(encoding='utf-8'));active=assurance.active_results(t,td);raw=[str(td/active[p['plan_id']]['task_path']) for p in s['plan']['plans']]
scaled=HANDLERS['fr_scale_frames'](**c,frame_paths=raw,factor=.86,mode='lanczos',label=name+'-scaled')
xs={0:500,22:515,35:500,45:490,60:510,75:500,90:510,110:520,125:515,140:510,155:515,165:500,180:520,195:520,205:520,225:540,238:540,250:540,270:540,292:520,305:520,320:510,340:500,350:500}
offsets=[{'x':round((512-xs[a])*.86),'y':0} for a in s['ordered_angles']]
norm=HANDLERS['fr_normalize_frames'](**c,frame_paths=[r['path'] for r in scaled['frames']],canvas_width=1024,canvas_height=1536,anchor='bottom_center',baseline_y=1450,offsets=offsets,resampling='lanczos',label=name+'-normalized')
paths=[r['path'] for r in norm['frames']]
for i,p in enumerate(paths):
 im=Image.open(p).convert('RGBA').resize((width,height),Image.Resampling.LANCZOS);im.save(work/'keys'/f'{i:04d}.png');arr=np.asarray(im,dtype=np.float32);alpha=arr[:,:,3:4]/255
 Image.fromarray(np.rint(arr[:,:,:3]*alpha).astype(np.uint8)).save(work/'rgb-input'/f'{i:04d}.png')
 a=im.getchannel('A');Image.merge('RGB',(a,a,a)).save(work/'alpha-input'/f'{i:04d}.png')
for kind in ['rgb-input','alpha-input']:shutil.copy2(work/kind/'0000.png',work/kind/'0024.png')
sheet=Image.new('RGB',(6*256,4*408),'#e9e7e3');d=ImageDraw.Draw(sheet)
for i,p in enumerate(paths):
 im=Image.open(p).convert('RGBA');bg=Image.new('RGBA',im.size,'#e9e7e3');bg.alpha_composite(im);sheet.paste(bg.convert('RGB').resize((256,384)),((i%6)*256,(i//6)*408));d.text(((i%6)*256+8,(i//6)*408+386),f'{i:02d} yaw~{s["ordered_angles"][i]}',fill='black')
sheet.save(work/'key-contact.jpg')
interpolate(work,192)
# Register the real local transform lineage, with exact input/output hashes.
# This does not declare interpolated frames to be ImageGen generations or alter QA.
with pipeline._task_lock(td):
 task=pipeline._load_task(td);outpaths=sorted((work/'rgba').glob('*.png'))
 for i,dest in enumerate(outpaths):
  k=i//8;assurance.lineage(task,td,[dest],[Path(paths[k]),Path(paths[(k+1)%24])])
 task.setdefault('coordinate_mappings',[]).append({'operation':'local_rife_interpolation','model':'rife-v4.6','model_bin_sha256':hashlib.sha256((ROOT/'.codex-imagegen/tools/rife/rife-ncnn-vulkan-20221029-windows/rife-v4.6/flownet.bin').read_bytes()).hexdigest(),'input_key_frames':paths,'generated_key_plan_ids':[p['plan_id'] for p in s['plan']['plans']],'source_resize_to':[width,height],'alpha_method':'premultiplied RGB and alpha separately interpolated, unpremultiply after interpolation','frame_count':192,'fps':24,'sampling':'25 inputs including closure key; generate 200 frames at x8, take first 192 to exclude duplicated closure hold','tta':'temporal','mirrored':False,'output_frames':[str(p) for p in outpaths]})
 pipeline._event(task,'local_rife_interpolation',{'key_frames':24,'alpha_preserved':True},{'frames':192,'work_dir':str(work)},['Derived frames; not declared as new ImageGen calls. Quality review remains required.'])
 pipeline._save_task(td,task)
(BASE/(name+'-state.json')).write_text(json.dumps({'task_id':c['task_id'],'work':str(work),'key_paths':paths,'frames':[str(p) for p in outpaths]},ensure_ascii=False,indent=2),encoding='utf-8')
