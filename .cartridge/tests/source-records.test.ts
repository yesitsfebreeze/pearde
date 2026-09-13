import { afterEach, beforeEach, expect, test, spyOn } from 'bun:test';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { atomic, hash, scan, sourceDeclarations } from '../../src/records';
import { sourceRecords } from '../../src/source-records';
import { Service } from '../../src/service';
let root: string, boards: string;
function record(board: string, name: string, text: string | Buffer) { const file = path.join(boards, board, 'prds', name, 'prd.md'); fs.mkdirSync(path.dirname(file), {recursive:true}); fs.writeFileSync(file,text); return file; }
const revision = (board='root') => hash(fs.readFileSync(path.join(boards,board,'settings.md')));
const index = (board='root',deadline=2000) => sourceRecords(boards,board,{action:'index',expected_source_revision:revision(board)},deadline);
const read = (item:any,board='root') => sourceRecords(boards,board,{action:'read',expected_source_revision:revision(board),path:item.path,expected_revision:item.revision},2000);
beforeEach(()=>{root=fs.mkdtempSync(path.join(fs.realpathSync(os.tmpdir()),'prd-public-records-'));boards=path.join(root,'.cartridge/boards');for(const [board,child]of [['root','base'],['root/base','plugin'],['root/base/plugin',null]]){atomic(path.join(boards,board!,'settings.md'),`---\nmembers: ${child?JSON.stringify({[child]:child}):'{}'}\n---\n`);record(board!,'same',`\uFEFF---\r\nstate: open\r\n---\r\n# ${board}\r\nUnique body fact ${board}\r\n`);}});
afterEach(()=>fs.rmSync(root,{recursive:true,force:true}));
test('each board indexes only local records and exact reads preserve BOM CRLF and selected owner',async()=>{
 for(const board of ['root','root/base','root/base/plugin']){const result=await index(board);expect(result.status).toBe('available');expect(result.items).toHaveLength(1);const item=result.items[0],actual=await read(item,board);expect(actual.text).toBe(fs.readFileSync(path.join(boards,board,item.path),'utf8'));expect(actual.revision).toBe(hash(Buffer.from(actual.text)));expect(actual.bytes).toBe(Buffer.byteLength(actual.text));expect(actual.root).toBe(path.join(boards,board));expect(actual.complete).toBe(true);expect(result.index_revision).toBe(hash(JSON.stringify({root:result.root,source_revision:revision(board),items:result.items})));}
 expect([...scan(path.join(boards,'root')).keys()]).toEqual(['same','@base/same','@base/plugin/same']);
});
test('private and invalid visibility disappear without path title text or count; trusted scan retains them',async()=>{
 const before=await index();for(const [i,head]of ['private: true','private: "false"','private: null','visibility: private','visibility: internal','visibility: null','visibility: [public]'].entries())record('root',`SECRET${i}`,`---\n${head}\n---\n# SECRET${i}\nSECRET BODY`);
 const result=await index();expect(result).toEqual(before);expect(JSON.stringify(result)).not.toContain('SECRET');expect(scan(path.join(boards,'root')).size).toBe(10);
 for(let i=0;i<7;i++){const file=path.join(boards,'root/prds',`SECRET${i}`,'prd.md');expect(await read({path:`prds/SECRET${i}/prd.md`,revision:hash(fs.readFileSync(file))})).toEqual({schema:'cartridge-source-records/v1',status:'unavailable'});}
 expect(await read({path:'prds/missing/prd.md',revision:'a'.repeat(64)})).toEqual({schema:'cartridge-source-records/v1',status:'unavailable'});
 record('root','explicit','---\nprivate: false\nvisibility: public\n---\n# Public\n');expect((await index()).items).toHaveLength(2);
});
test('malformed UTF8 headers and duplicate visibility never become public exact text',async()=>{
 for(const bytes of [Buffer.from([0xff]),Buffer.from('---\nprivate: true\nprivate: false\n---\n# hidden'),Buffer.from('---\nvisibility: [broken\n---\n# invalid'),Buffer.from('---\nvisibility: public\n# unclosed')]){const file=record('root','bad',bytes);const answer=await read({path:'prds/bad/prd.md',revision:hash(bytes)});expect(answer.status).toBe('malformed');const items=await index();expect(items.status).toBe('partial');expect(items.items.map((i:any)=>i.path)).toEqual(['prds/same/prd.md']);fs.unlinkSync(file);}
});
test('selectors source revision and record revision refuse changed or foreign input',async()=>{
 const initial=await index();const item=initial.items[0];record('root','same','# Changed\n');expect((await read(item)).status).toBe('changed');
 expect((await sourceRecords(boards,'root',{action:'index',expected_source_revision:'0'.repeat(64)})).status).toBe('changed');
 for(const bad of ['../root','/tmp','root//base','root/../hidden','root\\base', 'x'.repeat(513)])expect((await sourceRecords(boards,bad,{action:'index',expected_source_revision:revision()})).status).toBe('malformed');
 for(const bad of ['prds/../same/prd.md','prds/.secret/prd.md','prds/same/other.md','/prds/same/prd.md'])expect((await read({...item,path:bad})).status).toBe('malformed');
 expect((await sourceRecords(boards,'root',{action:'index',expected_source_revision:revision(),root:'/tmp'}as any)).status).toBe('malformed');
});
test('symlinks special files and late directory changes are explicit without outside reads',async()=>{
 const item=(await index()).items[0];const file=path.join(boards,'root',item.path);fs.unlinkSync(file);const outside=path.join(root,'outside');fs.writeFileSync(outside,'# PRIVATE OUTSIDE');fs.symlinkSync(outside,file);expect((await read(item)).status).toBe('malformed');expect(JSON.stringify(await index())).not.toContain('PRIVATE');fs.unlinkSync(file);
 expect(Bun.spawnSync(['mkfifo',file]).exitCode).toBe(0);const started=performance.now();expect((await read(item)).status).toBe('malformed');expect(performance.now()-started).toBeLessThan(500);fs.unlinkSync(file);record('root','same','# Public');
 const original=fs.promises.open;let changed=false;const spy=spyOn(fs.promises,'open').mockImplementation(async(...args:any[])=>{const handle=await (original as any)(...args);if(String(args[0]).endsWith('/same/prd.md')&&!changed){changed=true;record('root','added','# Added');}return handle;});
 try{expect((await index()).status).toBe('changed');}finally{spy.mockRestore();}
});
test('file header public count aggregate and directory entry caps bound partial output',async()=>{
 record('root','large',Buffer.alloc(1048577,97));let result=await index();expect(result.status).toBe('partial');expect(result.truncated).toBe(true);
 record('root','header','---\ncomment: '+ 'a'.repeat(16384)+'\n---\n# Header');expect((await index()).truncated).toBe(true);
 for(let i=0;i<130;i++)record('root',`r${i}`,'# Public\n');result=await index();expect(result.items.length).toBeLessThanOrEqual(128);expect(result.complete).toBe(false);expect(Buffer.byteLength(JSON.stringify(result))).toBeLessThanOrEqual(1048576);
});
test('response deadline retains all shared live I/O slots and closes delayed handles',async()=>{
 const service=new Service({root});const original=fs.promises.open;let release!:()=>void;const gate=new Promise<void>(r=>release=r);let closed=0;
 const spy=spyOn(fs.promises,'open').mockImplementation(async(...args:any[])=>{const handle=await(original as any)(...args);const close=handle.close.bind(handle);handle.close=async()=>{closed++;return close();};await gate;return handle;});
 try{const answers=await Promise.all(Array.from({length:8},()=>service.records({op:'source_records',board:'root',action:'index',expected_source_revision:revision(),deadline_ms:30})));expect(answers.every(a=>a.status==='timeout')).toBe(true);expect(service.declarationReads.size).toBe(8);expect((await service.declarations({op:'source_declarations'})).status).toBe('capacity');expect((await service.records({op:'source_records',action:'index',expected_source_revision:revision()})).status).toBe('capacity');release();await Promise.all([...service.declarationReads]);expect(closed).toBe(8);expect(service.declarationReads.size).toBe(0);}finally{release();spy.mockRestore();await service.close();}expect((await service.records({op:'source_records'})).status).toBe('unavailable');
});

function snapshot(directory: string): string {
 return hash(JSON.stringify(fs.readdirSync(directory,{recursive:true,withFileTypes:true}).map(e=>{const file=path.join(e.parentPath,e.name);return[path.relative(directory,file),e.isFile()?hash(fs.readFileSync(file)):'directory'];}).sort((a,b)=>String(a[0]).localeCompare(String(b[0])))));
}
test.skipIf(!process.env.CARTRIDGE_TEST_BIN)('actual Host indexes and exactly reads all three source owners without Memory events spill or tool exposure', async () => {
  const profile = path.join(root, 'profile'), plugins = path.join(root, 'plugins'); fs.mkdirSync(plugins);
  atomic(path.join(profile, 'init.lua'), 'return {{id="memory",path="memory.lua"},{id="prd",path="prd"},{id="probe",path="probe.lua"}}');
  atomic(path.join(profile, 'config.lua'), `return {prd={root=${JSON.stringify(root)},max_output_bytes=1024}}`);
  atomic(path.join(plugins, 'memory.lua'), `return {provide={"memory"},apply=function(ctx) ctx:provide("memory",function(request) error("declaration operation called Memory") end) end}`);
  fs.symlinkSync(path.resolve(import.meta.dir, '../..'), path.join(plugins, 'prd'));
  const probe = path.join(root, 'probe.ts');
  atomic(probe, `import {createInterface} from 'node:readline';
import {HostBridge} from ${JSON.stringify(path.resolve(import.meta.dir, '../../src/service.ts'))};
if(process.argv[2]==='hello'){console.log(JSON.stringify({inject:['prd','tool.prd'],provide:['probe']}));process.exit(0);}
const send=m=>console.log(JSON.stringify(m)),bridge=new HostBridge(send),events=[];
for await(const line of createInterface({input:process.stdin})){
 const m=JSON.parse(line);if(bridge.accept(m))continue;if(m.dispose)break;
 if(m.apply){send({provide:'probe'});send({subscribe:'prd'});send({ready:true});}
 else if(m.call==='probe')void(async()=>{try{
  const rows=[];for(const board of ['root','root/base','root/base/plugin']){const declaration=await bridge.request('prd',{op:'source_declarations',board});const indexed=await bridge.request('prd',{op:'source_records',board,action:'index',expected_source_revision:declaration.revision});const item=indexed.items[0];rows.push({indexed,read:await bridge.request('prd',{op:'source_records',board,action:'read',expected_source_revision:declaration.revision,path:item.path,expected_revision:item.revision})});}
  const rejected=await bridge.request('tool.prd',{op:'source_records',board:'root',action:'index'});
  const described=await bridge.request('tool.prd',{op:'describe'});
  send({reply:m.id,data:{rows,rejected,described,events}});
 }catch(e){send({reply:m.id,error:String(e)});}})();
 else events.push(m);
}bridge.close();`);
  const launch = path.join(root, 'probe'); atomic(launch, `#!/bin/sh\nexec '${process.execPath.replaceAll("'", "'\\''")}' '${probe.replaceAll("'", "'\\''")}' "$@"\n`); fs.chmodSync(launch, 0o755);
  atomic(path.join(plugins, 'probe.lua'), `return cartridge.process(${JSON.stringify(launch)})`);
  record('root','private','---\nprivate: true\n---\n# PRIVATE_MARKER\nPRIVATE_BODY');
  record('root','same','# Root\n'+ 'Exact source body. '.repeat(150));
  const before = snapshot(boards);
  const child = Bun.spawn([path.resolve(process.env.CARTRIDGE_TEST_BIN!), '--dir', plugins, '--profile', profile, 'run', 'probe', '{}'], { cwd: root, stdout: 'pipe', stderr: 'pipe', timeout: 15000 });
  try {
    const [output, error, code] = await Promise.all([new Response(child.stdout).text(), new Response(child.stderr).text(), child.exited]);
    expect(code, error + '\n' + output).toBe(0);
    const data = JSON.parse(output); expect(data.rows.map((r: any) => r.indexed.status)).toEqual(['available', 'available', 'available']);
    for(const row of data.rows){expect(row.read.text).toBe(fs.readFileSync(path.join(row.indexed.root,row.read.path),'utf8'));expect(row.read.revision).toBe(hash(row.read.text));expect(row.indexed.items).toHaveLength(1);}
    expect(JSON.stringify(data)).not.toContain('PRIVATE_MARKER');expect(data.rows[0].read.bytes).toBeGreaterThan(1024);
    expect(data.rows[1].indexed.root).toBe(path.join(boards, 'root/base'));
    expect(data.rejected.error).toBe(true); expect(data.described.input_schema.properties.op.enum).not.toContain('source_records');
    expect(data.events.filter((e: any) => e.event?.kind !== 'subscribe')).toEqual([]);
    expect(snapshot(boards)).toBe(before); expect(fs.existsSync(path.join(root, '.cartridge/.state'))).toBe(false);
  } finally { if (child.exitCode === null) { child.kill(); await child.exited; } }
}, 20000);

test('strict public YAML rejects escaped flow alias merge and tagged ambiguity while trusted planning stays compatible',async()=>{
 const forbidden=[
  '"private": true\nprivate: false',
  String.raw`"pr\u0069vate": true`+'\nprivate: false',
  '{visibility: private, visibility: public}',
  '<<: {visibility: private}',
  'base: &private {visibility: private}\n<<: *private',
  'flag: &flag false\nprivate: *flag',
  'visibility: !unknown public',
 ];
 for(const header of forbidden){const text='---\n'+header+'\n---\n# PRIVATE_MARKER\n';record('root','ambiguous',text);expect((await read({path:'prds/ambiguous/prd.md',revision:hash(text)})).status).toBe('malformed');expect(JSON.stringify(await index())).not.toContain('PRIVATE_MARKER');}
 for(const header of ['"private": false\n"visibility": public','{private: false, visibility: public}']){const text='---\n'+header+'\n---\n# Public';record('root','ambiguous',text);expect((await read({path:'prds/ambiguous/prd.md',revision:hash(text)})).status).toBe('available');}
 record('root','ambiguous','---\nprivate: true\nprivate: false\n---\n# Trusted legacy');expect(scan(path.join(boards,'root')).get('ambiguous')?.fm.private).toBe(false);
});

test('failed growing reads debit actual bytes and cannot multiply the aggregate budget',async()=>{
 fs.rmSync(path.join(boards,'root/prds'),{recursive:true});for(let i=0;i<10;i++)record('root',String(i),'');
 const original=fs.promises.open;let bytes=0,files=0;
 const spy=spyOn(fs.promises,'open').mockImplementation(async(file:any,...args:any[])=>{const handle=await(original as any)(file,...args);if(String(file).endsWith('/prd.md')){const stat=handle.stat.bind(handle);let first=true;handle.stat=async()=>{const value=await stat();if(first){first=false;files++;fs.writeFileSync(file,Buffer.alloc(1048577,65));}return value;};const read=handle.read.bind(handle);handle.read=async(...params:any[])=>{const value=await(read as any)(...params);bytes+=value.bytesRead;return value;};}return handle;});
 try{const result=await index();expect(result.status).toBe('partial');expect(result.truncated).toBe(true);expect(bytes).toBe(8388608-65536-fs.statSync(path.join(boards,'root/settings.md')).size);expect(files).toBe(8);}finally{spy.mockRestore();}
});
test('directory entry and depth limits are explicit and late opendir closes after timeout',async()=>{
 for(let i=0;i<4100;i++)fs.writeFileSync(path.join(boards,'root/prds',`.ignored${i}`),'');let result=await index();expect(result.status).toBe('partial');expect(result.truncated).toBe(true);
 fs.rmSync(path.join(boards,'root/prds'),{recursive:true});record('root',Array(32).fill('deep').join('/'),'# Too deep');result=await index();expect(result.status).toBe('partial');expect(result.truncated).toBe(true);
 const original=fs.promises.opendir;let closed=false,work:Promise<any>|undefined;
 const spy=spyOn(fs.promises,'opendir').mockImplementation(async(...args:any[])=>{const handle=await(original as any)(...args);const close=handle.close.bind(handle);handle.close=async()=>{closed=true;return close();};await Bun.sleep(40);return handle;});
 try{const answer=await sourceRecords(boards,'root',{action:'index',expected_source_revision:revision()},20,w=>work=w);expect(answer.status).toBe('timeout');await work;expect(closed).toBe(true);}finally{spy.mockRestore();}
});

test('board selectors match declarations while hidden record paths remain excluded',async()=>{
 atomic(path.join(boards,'.hidden/settings.md'),'---\nmembers: {}\n---\n');record('.hidden','public','# Public');
 expect((await sourceDeclarations(boards,'.hidden')).status).toBe('available');expect((await index('.hidden')).status).toBe('available');
 expect((await read({path:'prds/.hidden/prd.md',revision:'a'.repeat(64)},'.hidden')).status).toBe('malformed');
});
test('final exact-read serialization checks the same absolute deadline',async()=>{
 const item=(await index()).items[0];const original=JSON.stringify;
 const spy=spyOn(JSON,'stringify').mockImplementation(((value:any,...args:any[])=>{if(value?.schema==='cartridge-source-records/v1'&&value.action==='read'){const until=performance.now()+60;while(performance.now()<until){}}return(original as any)(value,...args);})as any);
 try{const answer=await sourceRecords(boards,'root',{action:'read',expected_source_revision:revision(),path:item.path,expected_revision:item.revision},30);expect(answer.status).toBe('timeout');}finally{spy.mockRestore();}
});
