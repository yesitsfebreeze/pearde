import fs from 'node:fs';
import path from 'node:path';
import * as records from '/Users/feb/dev/cartridge/prd.ctg/src/records.ts';
const root=fs.realpathSync(process.argv[2]), scope=path.join(root,'.cartridge/boards');
function put(file:string,text:string|Buffer){fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,text);}
for(const [name,members,body] of [['root',{base:'base'},'ROOTAMBER'],['root/base',{plugin:'plugin'},'BASEBERYL'],['root/base/plugin',{},'PLUGINCOBALT']] as const){
 put(path.join(scope,name,'settings.md'),'---\nmembers: '+JSON.stringify(members)+'\n---\n');
 put(path.join(scope,name,'prds/same/prd.md'),'---\nstate: open\n---\n# Same\n'+body+'\n');
}
for(const [name,header] of [['private-flag','private: true'],['private-visibility','visibility: private'],['unknown-visibility','visibility: internal']] as const)
 put(path.join(scope,'root/base/prds',name,'prd.md'),'---\n'+header+'\n---\n# PRIVATE_TITLE_'+name+'\nPRIVATE_BODY_'+name+'\n');
const malformed=path.join(scope,'root/base/prds/invalid-utf8/prd.md');
put(malformed,Buffer.from([35,32,65,10,0xff,10]));
const files=()=>fs.readdirSync(scope,{recursive:true,withFileTypes:true}).filter(e=>e.isFile()).map(e=>{const f=path.join(e.parentPath,e.name);return [path.relative(scope,f),records.hash(fs.readFileSync(f))]}).sort();
const before=files();
const declarations=[];
for(const board of ['root','root/base','root/base/plugin'])declarations.push(await records.sourceDeclarations(scope,board,2000));
const scanned=[...records.scan(path.join(scope,'root')).values()];
const privateRows=scanned.filter(r=>r.local.includes('private')||r.local.includes('unknown-visibility')).map(r=>({ref:r.ref,title:r.title,body:r.body,private:r.fm.private,visibility:r.fm.visibility}));
const invalid=records.document(malformed);
const native=Bun.spawn(['/Users/feb/dev/cartridge/cartridge.ctg/target/tool-result-contract/debug/memo_cartridge'],{cwd:root,stdin:'pipe',stdout:'pipe',stderr:'pipe'});
const send=(m:any)=>{native.stdin.write(JSON.stringify(m)+'\n');native.stdin.flush()};
let ready!:()=>void;const started=new Promise<void>(r=>ready=r),pending=new Map<number,(v:any)=>void>();let id=1;const callbacks:any[]=[];
const reading=(async()=>{let buf='';for await(const chunk of native.stdout){buf+=new TextDecoder().decode(chunk);while(buf.includes('\n')){let end=buf.indexOf('\n'),frame=JSON.parse(buf.slice(0,end));buf=buf.slice(end+1);if(frame.ready)ready();if(pending.has(frame.reply)){pending.get(frame.reply)!(frame);pending.delete(frame.reply)}else if(frame.id){callbacks.push(frame);if(frame.cartridges)send({reply:frame.id,data:[]});else send({reply:frame.id,error:'baseline unexpected callback'})}}}})();
const errors=new Response(native.stderr).text();send({apply:{name:'memo',config:{}}});
await Promise.race([started,Bun.sleep(5000).then(()=>{throw Error('ready timeout')})]);
const results=[];
for(const args of [
 {op:'document',action:'index',cwd:path.join(scope,'root'),directory:'prds'},
 {op:'document',action:'read',cwd:path.join(scope,'root'),path:'prds/same/prd.md'},
 {op:'document',action:'read',cwd:path.join(scope,'root'),owner:'root/base/plugin',path:'.cartridge/documents/same.md'}
]){const call=id++;const answer=new Promise<any>(resolve=>pending.set(call,resolve));send({id:call,call:'memo',args});results.push({args,answer:await Promise.race([answer,Bun.sleep(5000).then(()=>{throw Error('request timeout')})])});}
send({dispose:true});native.stdin.end();await native.exited;await reading;
const proof={source_records_export:typeof (records as any).sourceRecords,declared_roots:declarations,scanned_refs:scanned.map(r=>r.ref),private_rows_returned_by_trusted_planning_scan:privateRows,invalid_utf8:{body:invalid.body,exact_bytes_sha256:records.hash(fs.readFileSync(malformed)),decoded_text_sha256:records.hash(invalid.text)},memo_native_results:results,memo_callbacks:callbacks,memo_exit:native.exitCode,memo_stderr:await errors,source_bytes_unchanged:JSON.stringify(before)===JSON.stringify(files())};
put(path.join(root,'baseline-results.json'),JSON.stringify(proof,null,2)+'\n');
put(path.join(root,'declarations.json'),JSON.stringify(declarations));
console.log(JSON.stringify(proof,null,2));
