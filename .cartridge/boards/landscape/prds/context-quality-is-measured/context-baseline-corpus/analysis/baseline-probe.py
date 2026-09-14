from pathlib import Path
import importlib.util,json,hashlib,subprocess,tempfile,shutil,time,select,sys,os
base=Path('/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/landscape/prds/context-quality-is-measured/context-baseline-corpus/analysis')
spec=importlib.util.spec_from_file_location('corpus',base/'corpus-generator.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
root=Path('/Users/feb/dev/cartridge');temp=Path(tempfile.mkdtemp(prefix='context-quality-baseline-'));pins={'generator':h(base/'corpus-generator.py'),'manifest':h(base/'corpus-manifest.json'),'sources':{},'binaries':{},'toolchain':{}}
for owner in ['memo','landscape','fs','cartridge']:
 pins['sources'][owner]=subprocess.check_output(['git','-C',str(root/(owner+'.ctg')),'rev-parse','HEAD'],text=True).strip()
for bin in ['memo_cartridge','fs']:
 src=root/'cartridge.ctg/target/tool-result-contract/debug'/bin;before=h(src);shutil.copy2(src,temp/bin);assert h(src)==h(temp/bin)==before;pins['binaries'][bin]={'source_before':before,'copy':before,'source_after':before}
for command in [['rustc','--version'],['cargo','--version'],['python3','--version'],['bun','--version']]:pins['toolchain'][command[0]]=subprocess.check_output(command,text=True).strip()
(base/'pre-measurement-pins.json').write_text(json.dumps(pins,indent=2)+'\n')
class SDK:
 def __init__(self,binary,handler,config):
  self.p=subprocess.Popen([str(binary)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1);self.handler=handler;self.calls=[];self.next=0;self.buffer=b'';self.send({'apply':{'name':binary.name,'config':config}})
  while True:
   f=self.frame()
   if f.get('ready'):break
   if f.get('error'):raise RuntimeError(f)
 def send(self,f):self.p.stdin.write(json.dumps(f,separators=(',',':'))+'\n');self.p.stdin.flush()
 def frame(self):
  while b'\n' not in self.buffer:
   if not select.select([self.p.stdout],[],[],10)[0]:raise RuntimeError('SDK deadline')
   chunk=os.read(self.p.stdout.fileno(),65536)
   if not chunk:raise RuntimeError('SDK EOF '+self.p.stderr.read())
   self.buffer+=chunk
  line,self.buffer=self.buffer.split(b'\n',1)
  return json.loads(line)
 def request(self,args,key='memo'):
  self.next+=1;id=self.next;self.send({'id':id,'call':key,'args':args})
  while True:
   f=self.frame()
   if f.get('reply')==id:
    if 'error'in f:raise RuntimeError(f['error'])
    return f['data']
   if 'id'in f:
    self.calls.append(f);self.send({'reply':f['id'],'data':self.handler(f)})
 def close(self):
  self.send({'dispose':True});self.p.stdin.close();self.p.wait(timeout=10);assert self.p.returncode==0
results=[]
try:
 for size in g.manifest()['sizes']:
  c=g.corpus(size);fixture=temp/str(size);fixture.mkdir();public=fixture/'public';public.mkdir()
  for d in c['documents']:
   p=fixture/d['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_text(d['text'])
  (public/c['file']['path']).write_bytes(c['file']['text'].encode());(public/c['undeclared_file']['path']).write_text(c['undeclared_file']['text'])
  fs=SDK(temp/'fs',lambda f:(_ for _ in ()).throw(RuntimeError('unexpected FS callback')), {})
  def callback(f):
   if f.get('cartridges'):return []
   if f.get('injections'):return ['memory','fs.context']
   if f.get('landscape'):return {'entries':[dict(c['kernel'],dir=str(public))]}
   if f.get('call')=='fs.context':return fs.request(f['args'],'fs.context')
   if f.get('call')=='memory':
    m=c['memory']
    if f['args']['op']=='query':return {'entities':[{'id':m['id'],'source':m['source'],'status':'active','text':'QUERY_PREVIEW_FORBIDDEN'}]}
    if f['args']['op']=='get':return dict(m,compact=True,text_truncated=False,extension='MEMORY_EXTENSION_FORBIDDEN')
   raise RuntimeError('unexpected callback '+str(f))
  memo=SDK(temp/'memo_cartridge',callback,{'context_files':[{'owner':c['file']['owner'],'path':c['file']['path']}]})
  try:
   for scenario in g.manifest()['scenarios']:
    args={'op':'context','action':'prepare','cwd':str(fixture),'limits':g.manifest()['limits'],**{k:scenario[k] for k in ['query','documents','memory','files','kernel']}}
    # pre-spec measured smoke: one native run; reviewed implementation records warmup+five.
    start=len(memo.calls);tick=time.perf_counter_ns();r=memo.request(args);elapsed=time.perf_counter_ns()-tick;wire=json.dumps(r,separators=(',',':'),ensure_ascii=False).encode();text=wire.decode();rows=r['rows'];reads=[]
    for row in rows:
     v=memo.request({'op':'context','action':'read','cwd':str(fixture),'reference':row['reference'],'limits':g.manifest()['limits']});reads.append(v=={'status':'available','evidence':row})
    item={'size':size,'scenario':scenario['name'],'elapsed_ns':elapsed,'wire_bytes':len(wire),'critical_present':[x for x in scenario['critical'] if x in text],'critical_missing':[x for x in scenario['critical'] if x not in text],'forbidden_present':[x for x in g.manifest()['forbidden'] if x in text],'kinds':sorted(set(x['reference']['kind'] for x in rows)),'exact_read_matches':reads,'response':r,'callbacks':memo.calls[start:]};results.append(item);(base/'baseline-raw.json').write_text(json.dumps(results,indent=2)+'\n')
    print(size,scenario['name'],len(rows),len(wire),round(elapsed/1e6,2),item['critical_missing'],flush=True)
  finally:memo.close();fs.close()
 (base/'baseline-raw.json').write_text(json.dumps(results,indent=2)+'\n')
finally:shutil.rmtree(temp)
