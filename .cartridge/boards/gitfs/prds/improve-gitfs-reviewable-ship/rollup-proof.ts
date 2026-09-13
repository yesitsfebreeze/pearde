import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
const repos=path.resolve(import.meta.dir,'../../../../../..');
const runtime=path.join(repos,'cartridge.ctg');
const target=path.join(runtime,'target/tool-result-contract/debug');
const executable=path.join(target,'cartridge');
const root=fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(),'gitfs-rollup-')));
const work=path.join(root,'work'), profile=path.join(root,'profile'), bare=path.join(root,'remote.git');
fs.mkdirSync(work);fs.mkdirSync(profile);
const env={...process.env,RUSTC_WRAPPER:'',RUSTC_WORKSPACE_WRAPPER:''};
function command(argv:string[],cwd=work,success=true) {
 const result=Bun.spawnSync(argv,{cwd,env,stdout:'pipe',stderr:'pipe',timeout:30000});
 if(success)assert.equal(result.exitCode,0,result.stderr.toString());
 return result;
}
function git(...args:string[]){return command(['git',...args]).stdout.toString().trim();}
function hash(bytes:Buffer|string){return createHash('sha256').update(bytes).digest('hex');}
let daemon:ReturnType<typeof Bun.spawn>|undefined;
try {
 git('init','-q','-b','main');git('config','user.name','Fixture');git('config','user.email','fixture@example.test');
 fs.writeFileSync(path.join(work,'base'),'base\n');git('add','base');git('-c','commit.gpgsign=false','commit','-qm','base');
 const base=git('rev-parse','HEAD');command(['git','init','--bare','-q',bare],root);git('remote','add','origin',bare);
 git('push','origin','HEAD:refs/heads/main','HEAD:refs/heads/unrelated');
 for(const name of ['gitfs','mcp']) {
  const dir=path.join(profile,name);fs.mkdirSync(path.join(dir,'.cartridge/bin'),{recursive:true});
  for(const file of ['cartridge.json','init.lua'])fs.copyFileSync(path.join(repos,name+'.ctg',file),path.join(dir,file));
  fs.symlinkSync(path.join(target,name),path.join(dir,'.cartridge/bin',name));
 }
 fs.copyFileSync(path.join(repos,'policy.ctg/init.lua'),path.join(profile,'policy.lua'));
 fs.writeFileSync(path.join(profile,'sessions.lua'),'return {provide={"sessions"},apply=function(ctx)ctx:provide("sessions",function()return {id="reviewable-rollup"}end)end}');
 fs.writeFileSync(path.join(profile,'init.lua'),'return {{id="sessions",path="sessions.lua"},{id="policy",path="policy.lua"},{id="gitfs",path="gitfs"},{id="mcp",path="mcp",inject={"tool.*","sessions","policy","policy.explain"}}}');
 fs.writeFileSync(path.join(profile,'config.lua'),`return {policy={default="deny",operations={gitfs={write="allow",read="allow",diff="allow",snapshot="allow",materialize="deny"},ship={ship="allow",push="allow"}}},gitfs={ship={author={name="Rollup Fixture",email="rollup@example.test"}}},mcp={cwd=${JSON.stringify(work)},tools={"tool.gitfs","tool.ship"}}}`);
 const argv=[executable,'--dir',profile,'--profile',profile];
 daemon=Bun.spawn([...argv,'daemon'],{cwd:work,env,stdout:'ignore',stderr:'pipe'});
 const socket=command([...argv,'socket']).stdout.toString().trim();
 const until=Date.now()+10000;while(!fs.existsSync(socket)&&Date.now()<until)await Bun.sleep(10);assert(fs.existsSync(socket));
 const native=(key:string,args:any)=>{const reply=JSON.parse(command([...argv,'call',key,JSON.stringify(args)]).stdout.toString());assert(!reply.error,JSON.stringify(reply));return reply.data;};
 let sequence=0;
 const rpc=(message:any)=>native('mcp',{op:'message',line:JSON.stringify(message)});
 rpc({jsonrpc:'2.0',id:++sequence,method:'initialize',params:{}});rpc({jsonrpc:'2.0',method:'notifications/initialized'});
 const tool=(name:string,input:any)=>{const reply=rpc({jsonrpc:'2.0',id:++sequence,method:'tools/call',params:{name,arguments:input}});assert(!reply.error,JSON.stringify(reply));return reply.result;};
 const payload=(reply:any)=>{assert.equal(reply.isError,false,JSON.stringify(reply));return JSON.parse(reply.content[0].text);};
 payload(tool('gitfs',{op:'write',path:'A',content:'owned original A\n'}));
 payload(tool('gitfs',{op:'write',path:'B',content:'owned original B\n'}));
 fs.writeFileSync(path.join(work,'A'),'snapshot A\n');fs.writeFileSync(path.join(work,'B'),'unselected B\n');
 fs.writeFileSync(path.join(work,'unrelated'),'unrelated staged\n');git('add','unrelated');fs.writeFileSync(path.join(work,'unrelated'),'unrelated unstaged\n');
 const index=fs.readFileSync(path.join(work,'.git/index'));
 payload(tool('gitfs',{op:'snapshot',paths:['A']}));
 const inspection=payload(tool('gitfs',{op:'diff',path:'B'}));
 assert(inspection.revision);assert(JSON.stringify(inspection).includes('owned original B'));assert(JSON.stringify(inspection).includes('unselected B'));
 const denied=tool('gitfs',{op:'materialize',paths:['B']});assert.equal(denied.isError,true);assert(denied.content[0].text.includes('permission denied'));
 const message='Reviewed rollup fixture';const preview=payload(tool('ship',{op:'ship',phase:'preview',message}));
 const local=payload(tool('ship',{op:'ship',phase:'commit',message,expected_revision:preview.revision}));
 assert.equal(local.tree,preview.snapshot.source.tree);assert.equal(local.parent,base);assert.equal(local.push,false);
 assert.equal(git('show','HEAD:A'),'snapshot A');assert.equal(git('show','HEAD:B'),'owned original B');
 assert.notEqual(command(['git','cat-file','-e','HEAD:unrelated'],work,false).exitCode,0);
 assert.deepEqual(fs.readFileSync(path.join(work,'.git/index')),index);assert.equal(fs.readFileSync(path.join(work,'unrelated'),'utf8'),'unrelated unstaged\n');
 assert.equal(fs.readFileSync(path.join(work,'B'),'utf8'),'unselected B\n');
 const push={op:'push',remote:'origin',ref:'refs/heads/main',commit:local.committed,expected_remote_head:base};
 const remotePreview=payload(tool('ship',{...push,phase:'preview'}));
 const pushed=payload(tool('ship',{...push,phase:'commit',expected_revision:remotePreview.revision,operation_id:'rollup-once'}));
 assert.equal(pushed.status,'confirmed');
 const reconciled=payload(tool('ship',{op:'push',phase:'reconcile',operation_id:'rollup-once'}));assert.equal(reconciled.status,'confirmed');assert.equal(reconciled.binding.commit,local.committed);
 assert.equal(command(['git','rev-parse','refs/heads/main'],bare).stdout.toString().trim(),local.committed);
 assert.equal(command(['git','rev-parse','refs/heads/unrelated'],bare).stdout.toString().trim(),base);
 assert.equal(git('rev-parse','HEAD'),local.committed);assert.deepEqual(fs.readFileSync(path.join(work,'.git/index')),index);
 console.log(JSON.stringify({schema:'gitfs-reviewable-rollup/v1',actual_providers:['GitFS native','MCP native','policy Lua'],session:'reviewable-rollup',base,local_commit:local.committed,tree:local.tree,local_revision:preview.revision,push_revision:remotePreview.revision,push_status:pushed.status,reconcile_status:reconciled.status,unrelated_staged_excluded:true,index_unchanged:true,unselected_snapshot_preserved:true,unrelated_remote_ref_unchanged:true,policy_denial_executed:false,binaries:Object.fromEntries(['cartridge','gitfs','mcp'].map(name=>[name,hash(fs.readFileSync(path.join(target,name)))]))},null,2));
} finally {
 if(daemon){daemon.kill();await daemon.exited;}
 fs.rmSync(root,{recursive:true,force:true});
}
