import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from fr_local import HANDLERS,ROOT,BASE,STATE
s=json.loads(STATE.read_text(encoding='utf-8'));f=json.loads((BASE/'final_delivery_state.json').read_text(encoding='utf-8'));c={'workspace_root':ROOT,'task_id':s['task']['task_id']}; p=f['selected']; results=[]
HANDLERS['fr_select_deliverables'](**c,image_paths=p,reason='Final selection after all processing and animation decoding; preserve previous exports as history.')
for name,paths,kind,w,h,count,alpha in [('png-frames',p[:16],'frames',1024,1536,16,True),('atlas',[p[16]],'atlas',4096,6144,16,True),('gif-preview',[p[17]],'preview',1024,1536,16,True),('contact-preview',[p[18]],'preview',1280,2016,1,False)]:
    kw={'image_paths':paths,'artifact_kind':kind,'group_name':name,'expected_width':w,'expected_height':h,'expected_frame_count':count,'expected_alpha':alpha}
    if name in ('png-frames','gif-preview'):kw['durations_ms']=[250]*16
    if kind=='atlas':kw.update(expected_columns=4,expected_rows=4)
    r=HANDLERS['fr_verify_delivery'](**c,**kw);results.append({'group':name,'format':r['format_status'],'findings':r['findings']})
review=json.loads((BASE/'review-final.json').read_text(encoding='utf-8'))
for scope in ('visual','semantic'):
    review['review_scope']=scope
    HANDLERS['fr_record_visual_review'](**c,**review)
try: HANDLERS['fr_package_task'](**c)
except Exception as ex:results.append({'packaging':'not-approved','reason':str(ex)})
(BASE/'verification-final.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps(results,ensure_ascii=False))
