import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';

const runtime='/Users/feb/dev/cartridge/cartridge.ctg';
const binaries={fs:process.env.FS_BINARY||path.join(runtime,'target/tool-result-contract/debug/fs'),gitfs:process.env.GITFS_BINARY||path.join(runtime,'target/tool-result-contract/debug/gitfs'),sessions:process.env.SESSIONS_BINARY||path.join(runtime,'target/sessions-mapping/debug/sessions')};
const digest=(bytes:Buffer|string)=>crypto.createHash('sha256').update(bytes).digest('hex');
const expected={fs:'6dc5fe3749af4547a86e4c43aba85fe5da012a54451b19bdc8d206f5be2ed2fd',gitfs:'8354b64d6220bd75396cd6f14209382b5f7ea1c0a9dffb2ecdfc1f4c62eaf0c2',sessions:'80b9e2759e8faff31d937b5009beb36cb48e54336b2478f5b7d1a0afb436e9ee'};
for(const [name,file] of Object.entries(binaries))assert.equal(digest(fs.readFileSync(file)),expected[name as keyof typeof expected],name+' binary changed; use the measured revision/frozen binary');
const root=fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(),'change-provenance-baseline-')));
const repo=path.join(root,'repo');fs.mkdirSync(repo);
function git(...args:string[]){const out=Bun.spawnSync(['git',...args],{cwd:repo,stdout:'pipe',stderr:'pipe',timeout:10_000});assert.equal(out.exitCode,0,out.stderr.toString());return out.stdout.toString().trim();}

async function sdk(name:keyof typeof binaries,config:any,host:(frame:any)=>Promise<any>) {
 const child=Bun.spawn([binaries[name]],{cwd:repo,stdin:'pipe',stdout:'pipe',stderr:'pipe'});
 let next=1,ready!:()=>void;const calls:any[]=[];
 const initialized=new Promise<void>(resolve=>ready=resolve);
 const pending=new Map<number,{resolve:(v:any)=>void,reject:(e:Error)=>void,timer:ReturnType<typeof setTimeout>}>();
 const send=(frame:any)=>{child.stdin.write(JSON.stringify(frame)+'\n');child.stdin.flush();};
 const output=(async()=>{let buffer='';const decoder=new TextDecoder();for await(const chunk of child.stdout){buffer+=decoder.decode(chunk,{stream:true});while(buffer.includes('\n')){const end=buffer.indexOf('\n'),frame=JSON.parse(buffer.slice(0,end));buffer=buffer.slice(end+1);if(frame.ready)ready();if(pending.has(frame.reply)){const p=pending.get(frame.reply)!;pending.delete(frame.reply);clearTimeout(p.timer);frame.error?p.reject(Error(frame.error)):p.resolve(frame.data);}else if(frame.id){calls.push(frame);void host(frame).then(data=>send({reply:frame.id,data}),e=>send({reply:frame.id,error:String(e)}));}}}})();
 const errors=(async()=>{let out='';for await(const chunk of child.stderr)out+=Buffer.from(chunk).toString();return out;})();
 send({apply:{name,config}});
 let timer:any;await Promise.race([initialized,new Promise((_,reject)=>{timer=setTimeout(()=>reject(Error(name+' not ready')),5000);})]);clearTimeout(timer);
 return {calls,call(capability:string,args:any){const id=next++;return new Promise<any>((resolve,reject)=>{const timer=setTimeout(()=>{pending.delete(id);reject(Error(name+' timed out'));},5000);pending.set(id,{resolve,reject,timer});send({id,call:capability,args});});},async close(){send({dispose:true});child.stdin.end();const status=await Promise.race([child.exited,Bun.sleep(3000).then(()=>{child.kill();return child.exited;})]);await output;const stderr=await errors;assert.equal(status,0,stderr);}};
}
const services:Awaited<ReturnType<typeof sdk>>[]=[];
try {
 git('init','-q');git('config','user.name','Provenance fixture');git('config','user.email','fixture@example.invalid');
 fs.writeFileSync(path.join(repo,'a.txt'),'base\n');fs.writeFileSync(path.join(repo,'b.txt'),'untouched\n');git('add','a.txt','b.txt');git('commit','-qm','fixture base');
 const base=git('rev-parse','HEAD'),indexBefore=git('ls-files','--stage');
 const sessions=await sdk('sessions',{dir:path.join(root,'sessions')},async f=>{throw Error('unexpected sessions callback '+JSON.stringify(f));});services.push(sessions);
 const session=await sessions.call('sessions',{op:'create',cwd:repo,name:'native provenance baseline'});
 const direct=await sdk('fs',{},async frame=>{assert.equal(frame.call,'sessions');return sessions.call('sessions',frame.args);});services.push(direct);
 const overlay=await sdk('gitfs',{store_dir:'.cartridge/gitfs'},async f=>{throw Error('unexpected gitfs callback '+JSON.stringify(f));});services.push(overlay);
 let call=0;const context=()=>({session:session.id,run:'baseline-run',call:'call-'+(++call),cwd:repo});
 const invoke=async(s:typeof direct,key:string,input:any)=>{const out=await s.call(key,{op:'call',context:context(),input});assert.equal(out.error,false,JSON.stringify(out));return out;};
 await invoke(direct,'tool.read',{path:'a.txt'});
 const directResult=await invoke(direct,'tool.edit',{path:'a.txt',old:'base',new:'direct'});
 const afterDirect=await sessions.call('sessions',{op:'get',id:session.id});
 const overlayResult=await invoke(overlay,'tool.gitfs',{op:'write',path:'a.txt',content:'overlay\n'});
 const afterOverlay=await sessions.call('sessions',{op:'get',id:session.id});
 const divergence=JSON.parse((await invoke(overlay,'tool.gitfs',{op:'diff',path:'a.txt'})).content);
 assert.equal(divergence.conflict,true);assert.notEqual(divergence.disk.revision,divergence.overlay.revision);
 assert.deepEqual(afterDirect.files,[path.join(repo,'a.txt')]);assert.deepEqual(afterOverlay.files,afterDirect.files);
 assert.equal(direct.calls.length,1);assert.deepEqual(Object.keys(direct.calls[0].args).sort(),['file','id','op']);assert.equal(overlay.calls.length,0);
 fs.writeFileSync(path.join(repo,'a.txt'),'external\n');fs.writeFileSync(path.join(repo,'unrelated.txt'),'outside change\n');
 await invoke(direct,'tool.read',{path:'unrelated.txt'});
 const afterExternal=await sessions.call('sessions',{op:'get',id:session.id});
 const owned=JSON.parse((await invoke(overlay,'tool.gitfs',{op:'ls'})).content);
 const externalDivergence=JSON.parse((await invoke(overlay,'tool.gitfs',{op:'diff',path:'a.txt'})).content);
 assert.deepEqual(afterExternal.files,afterDirect.files);assert.deepEqual(owned.owned.map((r:any)=>r.path),['a.txt']);
 assert.equal(git('ls-files','--stage'),indexBefore);assert.equal(git('rev-parse','HEAD'),base);assert.equal(fs.readFileSync(path.join(repo,'b.txt'),'utf8'),'untouched\n');
 let unsupported='';try{await sessions.call('sessions',{op:'changes',id:session.id});}catch(e){unsupported=String(e);}assert.match(unsupported,/unknown sessions op/);
 const persisted=JSON.parse(fs.readFileSync(path.join(root,'sessions',session.id+'.json'),'utf8'));
 assert.deepEqual(persisted.session.files,afterDirect.files);assert.equal(persisted.session.changes,undefined);
 console.log(JSON.stringify({sources:{fs:'de1406682a33c5b12cb472787178e2570e5ed0f8',gitfs:'b4b95bb648ea1e99b6ffc9ba3cbd562f255ca9d5',sessions:'c2693a7ca3e23c295b8fe52a664720dde137eedc'},binary_sha256:Object.fromEntries(Object.entries(binaries).map(([name,file])=>[name,digest(fs.readFileSync(file))])),base,session:session.id,direct_result:directResult,direct_callback:direct.calls[0],overlay_result:overlayResult,after_direct:afterDirect,after_overlay:afterOverlay,divergence,external_divergence:externalDivergence,after_external:afterExternal,owned,unsupported_changes:unsupported,legacy_file_records:persisted.session.files,index_unchanged:true,head_unchanged:true,unrelated_not_owned:true,observed_gap:'FS records only absolute path; GitFS emits no touch. Existing diff already shows divergence. No actor/operation/storage target/before-after revisions persist at Sessions boundary.'},null,2));
} finally {for(const service of services.reverse())await service.close();fs.rmSync(root,{recursive:true,force:true});}
