from pathlib import Path
import tempfile,subprocess,json,hashlib,shutil,sys
base=Path('/Users/feb/dev/cartridge'); runtime=base/'cartridge.ctg'; binary=runtime/'target/tool-result-contract/debug/cartridge'
root=Path(tempfile.mkdtemp(prefix='memo-real-host-file-kernel-'))
(root/'builtin').mkdir(); (root/'builtin/memo').symlink_to(base/'memo.ctg',target_is_directory=True);(root/'builtin/fs').symlink_to(base/'fs.ctg',target_is_directory=True)
(root/'builtin/sessions.lua').write_text('return {provide={"sessions"},apply=function(ctx) ctx:provide("sessions",function() error("unexpected session touch") end) end}')
(root/'builtin/alpha').mkdir();(root/'builtin/alpha/init.lua').write_text('return {provide={"native.fixture"},apply=function(ctx) ctx:provide("native.fixture",function() error("must not activate evidence capability") end) end}')
(root/'builtin/alpha/cartridge.json').write_text(json.dumps({'name':'alpha','entry':'init.lua','provide':['native.fixture']}))
(root/'builtin/alpha/fixture.txt').write_bytes(b'FULL\r\nREAL_HOST\r\n')
(root/'config.lua').write_text('return {memo={context_files={{owner="alpha",path="fixture.txt"}}}}')
def run(present):
 profile='return {{id="memo",path="memo",inject={'+('"fs.context"' if present else '')+'}},{id="alpha",path="alpha"}'+(',{id="sessions",path="sessions.lua"},{id="fs",path="fs"}' if present else '')+'}'
 (root/'init.lua').write_text(profile)
 args={'op':'context','action':'prepare','cwd':str(root),'query':'fixture','documents':False,'files':True,'kernel':True,'limits':{'deadline_ms':500,'max_rows':16,'max_bytes':16384}}
 proc=subprocess.run([str(binary),'--dir',str(root/'builtin'),'--profile',str(root),'run','memo',json.dumps(args)],text=True,capture_output=True,timeout=20)
 return {'present':present,'exit':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,'profile':profile}
try:
 result={'runtime_binary':str(binary),'manifest_sha256':hashlib.sha256((base/'fs.ctg/cartridge.json').read_bytes()).hexdigest(),'manifest':json.loads((base/'fs.ctg/cartridge.json').read_text()),'cases':[run(True),run(False)]}
 present,omitted=result['cases']
 assert present['exit']==0,present
 parsed=json.loads(present['stdout'])
 assert parsed['complete'] and len(parsed['rows'])==2,parsed
 file=next(r for r in parsed['rows'] if r['reference']['kind']=='file')
 assert file['reference']['id']=='@alpha/fixture.txt' and file['text']=='FULL\r\nREAL_HOST\r\n',file
 assert file['reference']['revision']==hashlib.sha256(file['text'].encode()).hexdigest(),file
 assert any(r['reference']['kind']=='kernel' for r in parsed['rows']),parsed
 assert omitted['exit']==0,omitted
 missing=json.loads(omitted['stdout'])
 states={r['contributor']:r['state'] for r in missing['sources']}
 assert states['files']=='absent' and states['kernel']=='available',missing
 assert all(r['reference']['kind']!='file' for r in missing['rows']),missing
 assert (root/'builtin/alpha/fixture.txt').read_bytes()==b'FULL\r\nREAL_HOST\r\n'
 assert sorted(f.name for f in (root/'builtin/alpha').iterdir())==['cartridge.json','fixture.txt','init.lua']
 result['assertions']='Real Host present grant loads FS/Memo and returns exact bytes + kernel; omitted FS/grant keeps Memo loaded with files absent/kernel available; source bytes and directory entries unchanged.'
 result['assertion_count']=10
 print(json.dumps(result,indent=2))
finally:shutil.rmtree(root)
