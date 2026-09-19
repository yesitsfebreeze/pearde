import os, subprocess, json, tempfile, pathlib, time, pty, select, fcntl, termios, struct
B='/tmp/scope-owner-baseline-target/debug/cartridge'
PY='/tmp/cartridge-scope-env/bin/python'
env=dict(os.environ); env.pop('CARTRIDGE_YOLO',None)
with tempfile.TemporaryDirectory(prefix='scope-baseline-project-') as d:
 p=pathlib.Path(d); (p/'.cartridge').mkdir(); (p/'sample').mkdir()
 (p/'sample/cartridge.json').write_text(json.dumps({'name':'sample','entry':'init.lua','events':{'asp.sample':{}},'listen':['asp.sample'],'asp':{'roots':['memo:jev'],'schemes':{'memo':{'owner':True}},'attributes':{'sample.body':{}},'search':True}}))
 (p/'sample/init.lua').write_text('cartridge.listen("asp.sample", function(r) return {nodes={{id="memo:jev",name="jev memo",attributes={["sample.body"]="needle for composable search"}}}} end)')
 (p/'.cartridge/init.lua').write_text('return {{id="sample",path="sample"}}')
 (p/'search.txt').write_text('needle here\nother line\n')
 def run(*args):
  q=subprocess.run([B,'--dir',d,*args],cwd=d,env=env,capture_output=True,text=True,timeout=30)
  assert q.returncode==0,(args,q.stderr);return q.stdout
 run('trust',d)
 host=subprocess.Popen([B,'--dir',d,'daemon'],cwd=d,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
 try:
  for _ in range(100):
   try: run('call','asp','{"op":"types"}');break
   except AssertionError: time.sleep(.1)
  snap=json.loads(run('scope','--once','--python',PY)); assert any(i['id']=='asp:root' for i in snap['items']),snap
  os.environ['CARTRIDGE_SCOPE_HOST']=B
  import sys,asyncio
  sys.path.insert(0,'/tmp/scope-owner-baseline-20260919/ui')
  from cartridge_scope.client import Client
  from cartridge_scope.model import Context
  from cartridge_scope.search_engine import SearchEngine
  async def search():
   c=Client(d,B); m=Context(); m.types=await c.asp('types'); engine=SearchEngine(d,c,m)
   rows=await engine.evaluate('ASP jev > Grep needle'); assert [r['id'] for r in rows]==['memo:jev'],rows
   rows=await engine.evaluate('Files search.txt > Grep needle'); assert len(rows)==1 and rows[0]['content']=='needle here',rows
   print('Real ASP and disk filter chains passed.')
  asyncio.run(search())
  master,slave=pty.openpty(); fcntl.ioctl(slave,termios.TIOCSWINSZ,struct.pack('HHHH',40,120,0,0))
  child=subprocess.Popen([B,'--dir',d,'scope','--python',PY],cwd=d,env=dict(env,TERM='xterm-256color'),stdin=slave,stdout=slave,stderr=slave); os.close(slave)
  output=bytearray(); end=time.monotonic()+8
  while time.monotonic()<end:
   if select.select([master],[],[],.1)[0]:
    try: output.extend(os.read(master,65536))
    except OSError: break
   if b'FILTER' in output or b'Search' in output: break
  os.write(master,b'Files search.txt'); time.sleep(1); os.write(master,b'\x11')
  while child.poll() is None:
   if select.select([master],[],[],.1)[0]:
    try: output.extend(os.read(master,65536))
    except OSError: break
  child.wait(timeout=10); os.close(master)
  assert child.returncode==0,output[-4000:]
  assert b'Traceback' not in output,output[-4000:]
  assert b'\x1b[?1049h' in output,output[:1000]
  pathlib.Path('/tmp/memory-stack-scope-readiness/pty-output.bin').write_bytes(output)
  print('Embedded --once and real PTY launch/filter/exit passed against isolated host.')
 finally:
  subprocess.run([B,'--dir',d,'stop'],cwd=d,env=env,capture_output=True,timeout=10)
  host.wait(timeout=10)
