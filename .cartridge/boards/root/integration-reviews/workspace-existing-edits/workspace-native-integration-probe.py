import subprocess,tempfile,pathlib,json,select,time
owner=pathlib.Path('/Users/feb/dev/cartridge/workspace.ctg')
with tempfile.TemporaryDirectory(prefix='workspace-native-review-') as folder:
 p=subprocess.Popen(['bun','src/main.ts'],cwd=owner,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1)
 def send(v):p.stdin.write(json.dumps(v)+'\n');p.stdin.flush()
 def receive():
  if not select.select([p.stdout],[],[],5)[0]:raise RuntimeError('native response timed out')
  return json.loads(p.stdout.readline())
 def call(i,args):
  send({'id':i,'call':'workspace','args':args})
  response=receive();assert response.get('reply')==i,response
  return response
 try:
  send({'apply':{'config':{'dir':folder}}})
  # Readline may buffer several startup lines, so avoid mixing select with its
  # internal read-ahead: the three fixed synchronous startup lines are expected.
  lines=[json.loads(p.stdout.readline()) for _ in range(3)]
  assert lines==[{'provide':'workspace'},{'provide':'tool.workspace'},{'ready':True}],lines
  created=call(1,{'op':'save','id':'notes','title':'Notes','kind':'editor','content':'Original','sources':['agent']});assert created['data']['saved']
  before=call(2,{'op':'read','id':'notes'})['data'];assert before['native'] and 'cartridge:save' in before['html']
  navigation=call(3,{'op':'list'})['data']['revision']
  saved=call(4,{'op':'update','id':'notes','content':'Updated','expected_updated':before['updated']})['data']
  assert saved['content']=='Updated'
  stale=call(5,{'op':'update','id':'notes','content':'Stale overwrite','expected_updated':before['updated']});assert 'changed elsewhere' in stale['error']
  after=call(6,{'op':'read','id':'notes'})['data'];assert after['content']=='Updated' and after['sources']==['agent']
  assert call(7,{'op':'list'})['data']['revision']==navigation
  print(json.dumps({'actual_native_process':'bun src/main.ts','startup':'workspace and tool.workspace ready','native_save_update_read':'PASS','stale_exact_prior_version':'refused','source_metadata':'preserved','navigation_revision':'unchanged','call_count':7},indent=2))
 finally:
  p.stdin.close()
  try:p.wait(timeout=5)
  except subprocess.TimeoutExpired:p.terminate();p.wait(timeout=5)
  assert p.returncode==0,p.stderr.read()
