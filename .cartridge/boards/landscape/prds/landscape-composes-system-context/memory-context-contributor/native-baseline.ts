import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
const binary='/Users/feb/dev/cartridge/cartridge.ctg/target/debug/memory_cartridge';
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'memory-compact-baseline-'));
const endpoint=Bun.serve({hostname:'127.0.0.1',port:0,async fetch(r){ const b=await r.json() as any;return Response.json({embeddings:Array.from({length:Array.isArray(b.input)?b.input.length:1},()=>[1,0,0])}); }});
const child=Bun.spawn([binary],{stdin:'pipe',stdout:'pipe',stderr:'inherit',timeout:40000});
const reader=child.stdout.getReader(); const decoder=new TextDecoder(); let buffer='';
async function receive():Promise<any>{for(;;){const n=buffer.indexOf('\n');if(n>=0){const line=buffer.slice(0,n);buffer=buffer.slice(n+1);return JSON.parse(line);}const part=await reader.read();if(part.done)throw Error('memory ended');buffer+=decoder.decode(part.value,{stream:true});}}
let id=0;
async function call(args:any){const n=++id;child.stdin.write(JSON.stringify({id:n,call:'memory',args})+'\n');for(;;){const r=await receive();if(r.reply===n){if(r.error)throw Error(JSON.stringify(r.error));return r.data;}}}
try{
 child.stdin.write(JSON.stringify({apply:{config:{dir,embed:{url:endpoint.url.origin,model:'fixture'},reason:{url:''},tick:{interval_secs:0},queue:{enabled:false}}}})+'\n');while(!(await receive()).ready){}
 const seed=await call({op:'ingest',raw:true,sync:true,text:'Cedar-only-fact '+('x'.repeat(800))});
 const query=await call({op:'query',text:'Cedar-only-fact',k:1});
 console.log(JSON.stringify({binary,binary_sha256:crypto.createHash('sha256').update(fs.readFileSync(binary)).digest('hex'),seed,query},null,2));
 const row=query?.entities?.[0];if(!row?.id)throw Error('query had no entity');
 const get=await call({op:'get',id:row.id,compact:true,edge_limit:1});
 if(get.id!==row.id||JSON.stringify(get.source)!==JSON.stringify(row.source))throw Error('source or ID drift');
 if(!get.text_truncated||[...get.text].length!==503)throw Error('unexpected compact bound');
 console.log(JSON.stringify({get,assertions:'ranked source and ID exactly match compact get; 503 characters including ellipsis; text_truncated true'},null,2));
 child.stdin.write('{"dispose":true}\n');if(await child.exited!==0)throw Error('memory exited nonzero');
}finally{child.kill();endpoint.stop(true);reader.releaseLock();fs.rmSync(dir,{recursive:true,force:true});}
