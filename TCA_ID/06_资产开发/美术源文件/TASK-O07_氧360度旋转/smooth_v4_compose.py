import json,sys,hashlib,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path(__file__).parent));from smooth_pass import ROOT,BASE,np,HANDLERS
from server import pipeline,assurance
s=json.loads((BASE/'smooth_v4_state.json').read_text(encoding='utf-8'));td=Path(s['task']['task_dir']);c={'workspace_root':str(ROOT),'task_id':s['task']['task_id']};t=json.loads((td/'task.json').read_text(encoding='utf-8'));a=assurance.active_results(t,td);raw=[td/a[p['plan_id']]['task_path'] for p in s['plans']]
old=ROOT/'.codex-imagegen/tasks/fr-20261018-3804622d/work/smooth-native02';work=td/'work'/'final-motion';work.mkdir(exist_ok=True)
for name in ['rgba','rgb-review']:(work/name).mkdir(exist_ok=True)
mapping=[]
for i in range(192):
 original=old/'rgba'/f'{i:04d}.png';im=Image.open(original).convert('RGBA');source=original
 if i in s['fix_frames']:
  source=raw[26+s['fix_frames'].index(i)];repaired=Image.open(source).convert('RGBA')
  ob=im.getchannel('A').point(lambda v:255 if v>128 else 0).getbbox();rb=repaired.getchannel('A').point(lambda v:255 if v>128 else 0).getbbox()
  scale=(ob[3]-ob[1])/(rb[3]-rb[1]);resized=repaired.resize((round(repaired.width*scale),round(repaired.height*scale)),Image.Resampling.LANCZOS)
  x=round(512-512*scale);y=round(ob[3]-rb[3]*scale);canvas=Image.new('RGBA',(1024,1536),(0,0,0,0));canvas.alpha_composite(resized,(x,y));im=canvas
  rec={'frame':i,'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'uniform_scale':scale,'placement':[x,y],'reference_solid_bbox':ob,'source_solid_bbox':rb,'semantic_review':'Hat and shoes manually checked; alpha numbers refine shared full-body placement, not infer feet.'}
 else:rec={'frame':i,'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'transform':'exact reuse, same canvas'}
 im.save(work/'rgba'/f'{i:04d}.png');bg=Image.new('RGBA',im.size,'#e9e7e3');bg.alpha_composite(im);bg.convert('RGB').save(work/'rgb-review'/f'{i:04d}.png');mapping.append(rec)
with pipeline._task_lock(td):
 task=pipeline._load_task(td)
 for i in range(192):
  if i in s['fix_frames']:indices=[26+s['fix_frames'].index(i)]
  elif 60<=i<64:indices=[24,8]
  elif 56<=i<60:indices=[7,24]
  elif 140<=i<144:indices=[25,18]
  elif 136<=i<140:indices=[17,25]
  else:indices=[i//8,(i//8+1)%24]
  assurance.lineage(task,td,[work/'rgba'/f'{i:04d}.png'],[raw[j] for j in indices])
 task.setdefault('coordinate_mappings',[]).append({'operation':'reuse-continuous-parent-and-replace-12-cleanups','parent_task':'fr-20261018-3804622d','parent_process':'smooth_v3_process.py','frames':mapping,'cleanup_frames':s['fix_frames'],'fps':24,'loop':True,'alpha':'full alpha preserved; no key color removal','mirror':False})
 pipeline._event(task,'compose_clean_motion',{'direct_imagegen_cleanups':s['fix_frames']},{'frames':192,'work':str(work)});pipeline._save_task(td,task)
video=work/'oxygen-360-smooth.mp4';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-n','-framerate','24','-i',str(work/'rgb-review/%04d.png'),'-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True)
scores=[];masks=[]
files=sorted((work/'rgb-review').glob('*.png'))
for i,p in enumerate(files):
 arr=np.asarray(Image.open(p),dtype=np.float32);prev=np.asarray(Image.open(files[i-1]),dtype=np.float32);scores.append(float(np.abs(arr-prev).mean()))
for start in range(0,192,32):
 out=Image.new('RGB',(8*192,4*312),'#e9e7e3');d=ImageDraw.Draw(out)
 for j,i in enumerate(range(start,start+32)):
  im=Image.open(files[i]).resize((192,288),Image.Resampling.LANCZOS);out.paste(im,((j%8)*192,(j//8)*312));d.text(((j%8)*192+4,(j//8)*312+290),f'{i:03d}',fill='black')
 out.save(work/f'review-{start:03d}.jpg')
summary={'work':str(work),'video':str(video),'frames':[str(work/'rgba'/f'{i:04d}.png') for i in range(192)],'scores':scores,'max':max(scores),'median':float(np.median(scores)),'top_changes':sorted(enumerate(scores),key=lambda q:q[1],reverse=True)[:15],'closure':scores[0]}
(BASE/'smooth_v4_final_state.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in summary.items() if k not in ['frames','scores']},ensure_ascii=True))
