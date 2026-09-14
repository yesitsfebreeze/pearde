// Disposable native baseline. Each PTY receives an isolated child environment
// and fixture cwd; no existing shell, rc file or user store is contacted.
import {spawn} from 'node:child_process';
import {createInterface} from 'node:readline';
import fs from 'node:fs';import os from 'node:os';import path from 'node:path';
const binary='/Users/feb/dev/cartridge/cartridge.ctg/target/tool-result-contract/debug/pty';
async function bounded<T>(p:Promise<T>,label:string,ms=8000):Promise<T>{let timer:any;try{return await Promise.race([p,new Promise<T>((_,reject)=>{timer=setTimeout(()=>reject(Error(label+' deadline')),ms);})]);}finally{clearTimeout(timer);}}
const results=[];
for(const [name,program] of [['unsupported','/bin/sh']]){
 const root=fs.mkdtempSync(path.join(os.tmpdir(),'pty-context-baseline-'));for(const d of ['home','config','sub'])fs.mkdirSync(path.join(root,d));
 const child=spawn(binary,[],{cwd:root,stdio:'pipe',env:{PATH:'/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin',HOME:path.join(root,'home'),ZDOTDIR:path.join(root,'home'),XDG_CONFIG_HOME:path.join(root,'config'),XDG_DATA_HOME:path.join(root,'config'),TERM:'xterm-256color',LANG:'C.UTF-8'}});
 const pending=new Map<number,(v:any)=>void>();let next=1;let ready!:()=>void;const readiness=new Promise<void>(r=>ready=r);let stderr='';child.stderr.on('data',d=>{stderr=(stderr+d).slice(-2048)});
 createInterface({input:child.stdout}).on('line',line=>{const row=JSON.parse(line);if(row.ready)ready();if(row.reply){pending.get(row.reply)?.(row);pending.delete(row.reply);}});
 const exited=new Promise<void>(resolve=>child.on('exit',()=>resolve()));
 async function call(key:string,args:any){const id=next++;const response=new Promise<any>(resolve=>pending.set(id,resolve));child.stdin.write(JSON.stringify({id,call:key,args})+'\n');const row=await bounded(response,key);if(row.error)throw Error(row.error);return row.data;}
 async function until(check:()=>Promise<any>){return bounded((async()=>{for(;;){const v=await check();if(v)return v;await Bun.sleep(20);}})(),'observation');}
 child.stdin.write(JSON.stringify({apply:{config:{shell:program}}})+'\n');
 try{
  await bounded(readiness,'native ready');
  if(name!=='unsupported')await until(async()=>{const r=await call('pty',{op:'commands'});return r.phase==='prompt'?r:null});
  let metadata_error:string|null=null;try{await call('pty',{op:'context_metadata'});}catch(error){metadata_error=String(error);}
  const before=await call('pty',{op:'commands'});
  const tool=JSON.parse((await call('tool.shell',{op:'call',input:{}})).content);
  const raw=await call('pty',{op:'read'}),screen=await call('pty',{op:'screen'}),viewport=await call('pty',{op:'viewport'}),frame=await call('pty',{op:'frame'});
  const command=name==='nu'?"cd sub; print (['identity-' 'fixture-ok'] | str join)":"cd sub; printf 'identity-%s\\n' fixture-ok";
  await call('pty',{op:'write',data:Buffer.from(command+'\r').toString('base64')});
  const after=await until(async()=>{const r=JSON.parse((await call('tool.shell',{op:'call',input:{}})).content);return r.screen.includes('identity-fixture-ok')&&(name==='unsupported'||r.cwd.endsWith('/sub'))?r:null});
  const env=await call('environment',{});
  const attached=await call('pty',{op:'control',owner:'agent',start:true});
  const afterAttach=await call('pty',{op:'commands'});
  results.push({metadata_error,name,program,before,tool_fields:Object.keys(tool),read_fields:Object.keys(raw),screen_fields:Object.keys(screen),viewport_fields:Object.keys(viewport),frame_fields:Object.keys(frame),environment:{shell:env.shell,cwd:env.cwd},after:{cwd:after.cwd,phase:after.phase,literal_visible:after.screen.includes('identity-fixture-ok')},attachment_preserves_command_history:JSON.stringify(afterAttach.commands)===JSON.stringify(after.commands),attachment_control:attached.control,identity_absent:tool.shell===undefined&&tool.identity===undefined});
  await call('pty',{op:'write',data:Buffer.from('exit\r').toString('base64')});
  await until(async()=>{const r=await call('pty',{op:'read'});return r.exit!==null?r:null});
 }finally{child.stdin.write(JSON.stringify({dispose:true})+'\n');try{await bounded(exited,'dispose',3000);}catch{child.kill('SIGKILL');await exited;}fs.rmSync(root,{recursive:true,force:true});}
}
console.log(JSON.stringify({binary,sha256:new Bun.CryptoHasher('sha256').update(fs.readFileSync(binary)).digest('hex'),results},null,2));
