import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
const records=import.meta.dir;
const root=path.resolve(records,'../../../../../..');
const owner=path.resolve(process.argv[2]??'');
if(!fs.existsSync(path.join(owner,'.cartridge/packages/writer.ctg/cartridge.json'))) throw Error('writer source owner required');
const digest=(value:Buffer|string)=>new Bun.CryptoHasher('sha256').update(value).digest('hex');
const run=(args:string[],cwd:string,env=process.env,timeout=110_000)=>{
 const out=Bun.spawnSync(args,{cwd,env,stdout:'pipe',stderr:'pipe',timeout});
 if(out.exitCode) throw Error(`${args.join(' ')} failed (${out.exitCode})\n${out.stdout}\n${out.stderr}`);
 return out.stdout.toString();
};
const repositories=['cartridge.ctg','docs.ctg','agent.ctg','fs.ctg','gitfs.ctg','harness.ctg','landscape.ctg','mcp.ctg','memo.ctg','memory-tool.ctg','proxy.ctg','pty.ctg','router.ctg','sessions.ctg','tools.ctg'];
const files=new Map<string,{source:string,sha256:string}>();
const revisions:Record<string,string>={};
for(const repository of repositories) {
 const source=repository==='harness.ctg'?owner:path.join(root,repository);
 revisions[repository]=run(['git','rev-parse','HEAD'],source).trim();
 const names=run(['git','ls-files','-z','--cached','--others','--exclude-standard'],source).split('\0').filter(Boolean);
 if(repository==='cartridge.ctg') names.push('.cartridge/workspace/Cargo.toml','.cartridge/workspace/Cargo.lock');
 for(const name of names) {
  const absolute=path.join(source,name);
  if(!fs.existsSync(absolute)||!fs.statSync(absolute).isFile())continue;
  files.set(repository+'/'+name,{source:absolute,sha256:digest(fs.readFileSync(absolute))});
 }
}
const inputs=Object.fromEntries([...files].sort(([a],[b])=>a.localeCompare(b)));
const identity=digest(JSON.stringify(inputs));
const shadow=fs.mkdtempSync(path.join(os.tmpdir(),'cartridge-writer-verification-'));
for(const [relative,input] of files) {
 const target=path.join(shadow,relative);fs.mkdirSync(path.dirname(target),{recursive:true});fs.copyFileSync(input.source,target);fs.chmodSync(target,fs.statSync(input.source).mode);
 if(digest(fs.readFileSync(target))!==input.sha256)throw Error('source changed while copying '+input.source);
}
const runtime=path.join(shadow,'cartridge.ctg');
const env={...process.env,RUSTC_WRAPPER:'',RUSTC_WORKSPACE_WRAPPER:'',CARGO_TARGET_DIR:path.join(root,'cartridge.ctg/target/writer-proof')};
const commands=[['just','test','harness'],['just','test','memo'],['just','check','harness']];
const results=[];
for(const command of commands) {
 const started=new Date().toISOString();const stdout=run(command,runtime,env);results.push({command,started,completed:new Date().toISOString(),stdout,exit:0});
}
const receipt={owner,identity,shadow,revisions,inputs,results,completed:new Date().toISOString(),scope:'Disposable adjacent source copies; real manifests and public owner gates. This does not integrate or qualify model output.'};
fs.mkdirSync(path.join(records,'integration'),{recursive:true});
fs.writeFileSync(path.join(records,'integration',identity+'.json'),JSON.stringify(receipt,null,2)+'\n');
console.log(`Writer source ${identity}: public harness tests, memo tests and harness check passed.`);
