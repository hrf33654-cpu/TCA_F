import json,sys,subprocess,shutil,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops,ImageStat
ROOT=Path('E:/projects/TCA_ID');BASE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'.codex-imagegen/tools/runtime'))
import numpy as np
sys.path.insert(0,r'C:/Users/Lenovo/.codex/plugins/cache/frameronin-local/frameronin-imagegen/1.1.0')
from server.main import HANDLERS
OLD=ROOT/'.codex-imagegen/tasks/fr-20261018-e857e438'
RIFE=ROOT/'.codex-imagegen/tools/rife/rife-ncnn-vulkan-20221029-windows'

def restore():
 t=json.loads((OLD/'task.json').read_text(encoding='utf-8'))
 r=next(r for r in t['generation_records'] if r['task_path']=='raw/yaw-135-final.png')
 return HANDLERS['fr_record_generation'](workspace_root=str(ROOT),task_id=t['task_id'],generated_file=str(OLD/r['task_path']),label='smooth-repair06-rejected-restore',plan_id=r['plan_id'],prompt_text=r['prompt_text'])

def prepare(name,width,height):
 t=json.loads((OLD/'task.json').read_text(encoding='utf-8'));active={r['plan_id']:r for r in t['generation_records']}
 work=OLD/'work'/name;work.mkdir(exist_ok=True)
 for kind in ['keys','rgb-input','alpha-input','rgb-out','alpha-out','rgba','rgb-review']:(work/kind).mkdir(exist_ok=True)
 xs=[500,515,500,510,510,520,500,515,520,520,540,540,540,520,510,500]
 maps=[]
 for i in range(16):
  src=OLD/active[f'direction-{i+1:02d}']['task_path'];im=Image.open(src).convert('RGBA')
  # Manual review confirmed shoes are the lowest visible solid part of every key.
  # Alpha metrics only refine their numeric baseline; they are not a foot detector.
  bbox=im.getchannel('A').point(lambda v:255 if v>128 else 0).getbbox()
  scale=.86;scaled=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
  x=round(512-xs[i]*scale);y=round(1450-bbox[3]*scale)
  canvas=Image.new('RGBA',(1024,1536),(0,0,0,0));canvas.alpha_composite(scaled,(x,y));canvas=canvas.resize((width,height),Image.Resampling.LANCZOS)
  canvas.save(work/'keys'/f'{i:04d}.png')
  arr=np.asarray(canvas,dtype=np.float32);alpha=arr[:,:,3:4]/255
  # Interpolate premultiplied RGB and alpha separately. Never discard alpha.
  premul=np.rint(arr[:,:,:3]*alpha).astype(np.uint8)
  Image.fromarray(premul).save(work/'rgb-input'/f'{i:04d}.png')
  a=canvas.getchannel('A');Image.merge('RGB',(a,a,a)).save(work/'alpha-input'/f'{i:04d}.png')
  maps.append({'index':i,'source':str(src),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'scale':scale,'source_axis_x_manually_reviewed':xs[i],'solid_bbox':bbox,'placement':[x,y],'output_size':[width,height]})
 for kind in ['rgb-input','alpha-input']:shutil.copy2(work/kind/'0000.png',work/kind/'0016.png')
 (work/'coordinate-mappings.json').write_text(json.dumps(maps,indent=2),encoding='utf-8')
 return work

def interpolate(work,count):
 key_count=len(list((work/'keys').glob('*.png')))
 raw_count=round(count*(key_count+1)/key_count)
 for kind in ['rgb','alpha']:
  out=work/f'{kind}-out'
  if len(list(out.glob('*.png')))!=raw_count:
   cmd=[str(RIFE/'rife-ncnn-vulkan.exe'),'-i',str(work/f'{kind}-input'),'-o',str(out),'-n',str(raw_count),'-m',str(RIFE/'rife-v4.6'),'-g','1','-j','2:2:2','-f','%08d.png','-z']
   r=subprocess.run(cmd,capture_output=True);(work/f'{kind}-rife.log').write_bytes(r.stdout+r.stderr)
   if r.returncode:raise RuntimeError((r.stdout+r.stderr).decode('utf-8',errors='replace')[-2000:])
   print(kind,'interpolated',flush=True)
 rgb=sorted((work/'rgb-out').glob('*.png'));alphas=sorted((work/'alpha-out').glob('*.png'))
 assert len(rgb)==raw_count and len(alphas)==raw_count
 for i,(rp,ap) in enumerate(zip(rgb[:count],alphas[:count])):
  pre=np.asarray(Image.open(rp).convert('RGB'),dtype=np.float32);a=np.asarray(Image.open(ap).convert('L'),dtype=np.float32)
  color=np.clip(pre*255/np.maximum(a[:,:,None],1),0,255).astype(np.uint8)
  rgba=np.dstack((color,a.astype(np.uint8)));im=Image.fromarray(rgba);im.save(work/'rgba'/f'{i:04d}.png')
  bg=Image.new('RGBA',im.size,'#e9e7e3');bg.alpha_composite(im);bg.convert('RGB').save(work/'rgb-review'/f'{i:04d}.png')
 output=work/'turntable.mp4'
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-n','-framerate','24','-i',str(work/'rgb-review/%04d.png'),'-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(output)],check=True)
 frames=sorted((work/'rgba').glob('*.png'));scores=[]
 for i,p in enumerate(frames):
  im=Image.open(p).convert('RGBA');prev=Image.open(frames[i-1]).convert('RGBA')
  scores.append(float(np.abs(np.asarray(im,dtype=np.float32)-np.asarray(prev,dtype=np.float32)).mean()))
 (work/'temporal-scores.json').write_text(json.dumps({'frame_count':count,'fps':24,'seconds':count/24,'cyclic_mean_absolute_change':scores,'max_index':int(np.argmax(scores)),'max':max(scores),'median':float(np.median(scores)),'closure':scores[0]},indent=2),encoding='utf-8')
 for start in range(0,count,32):
  sheet=Image.new('RGB',(8*192,4*312),'#e9e7e3');d=ImageDraw.Draw(sheet)
  for j,i in enumerate(range(start,min(start+32,count))):
   im=Image.open(work/'rgb-review'/f'{i:04d}.png');im.thumbnail((192,288));sheet.paste(im,((j%8)*192,(j//8)*312));d.text(((j%8)*192+4,(j//8)*312+290),f'{i:03d}',fill='black')
  sheet.save(work/f'review-{start:03d}.jpg')
 print(json.dumps({'work':str(work),'mp4':str(output),'count':count,'maximum_change':max(scores),'median':float(np.median(scores)),'closure':scores[0]}),flush=True)

if __name__=='__main__':
 if sys.argv[1]=='restore': print(json.dumps(restore(),ensure_ascii=True)[:300])
 else:
  name=sys.argv[1];w=int(sys.argv[2]);h=int(sys.argv[3]);count=int(sys.argv[4]);work=prepare(name,w,h);interpolate(work,count)
