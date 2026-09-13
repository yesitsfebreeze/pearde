import fs from 'node:fs';import os from 'node:os';import path from 'node:path';
import {sourceRecords} from '/Users/feb/dev/cartridge/prd.ctg/src/source-records.ts';
import {hash} from '/Users/feb/dev/cartridge/prd.ctg/src/records.ts';
const temp=fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(),'prd-budget-review-'))),root=path.join(temp,'root');
fs.mkdirSync(root);fs.writeFileSync(path.join(root,'settings.md'),'---\nmembers: {}\n---\n');
for(let n=0;n<10;n++){const dir=path.join(root,'prds',String(n));fs.mkdirSync(dir,{recursive:true});fs.writeFileSync(path.join(dir,'prd.md'),'');}
const open=fs.promises.open.bind(fs.promises);let readBytes=0,files=0;
fs.promises.open=(async(file:any,...args:any[])=>{const handle=await (open as any)(file,...args);if(String(file).endsWith('/prd.md')){
 const stat=handle.stat.bind(handle);let first=true;
 handle.stat=(async(...a:any[])=>{const info=await (stat as any)(...a);if(first){first=false;files++;fs.writeFileSync(file,Buffer.alloc(1048577,65));}return info})as any;
 const read=handle.read.bind(handle);handle.read=(async(...a:any[])=>{const r=await (read as any)(...a);readBytes+=r.bytesRead;return r})as any;
}return handle})as any;
try{const result=await sourceRecords(temp,'root',{action:'index',expected_source_revision:hash(fs.readFileSync(path.join(root,'settings.md')))},2000);console.log(JSON.stringify({result,files,readBytes,cap:8388608,exceeds_aggregate_cap:readBytes>8388608}));}
finally{fs.promises.open=open as any;fs.rmSync(temp,{recursive:true,force:true})}
