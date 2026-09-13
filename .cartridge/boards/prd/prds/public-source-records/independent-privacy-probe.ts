import fs from 'node:fs';import os from 'node:os';import path from 'node:path';
import {sourceRecords} from '/Users/feb/dev/cartridge/prd.ctg/src/source-records.ts';
import {hash} from '/Users/feb/dev/cartridge/prd.ctg/src/records.ts';
const temp=fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(),'prd-source-review-'))),root=path.join(temp,'root');
fs.mkdirSync(path.join(root,'prds/private'),{recursive:true});fs.writeFileSync(path.join(root,'settings.md'),'---\nmembers: {}\n---\n');
const source=hash(fs.readFileSync(path.join(root,'settings.md')));
try{
 for(const header of ['private: true\nprivate: false','visibility: private\nvisibility: public']){
  fs.writeFileSync(path.join(root,'prds/private/prd.md'),'---\n'+header+'\n---\n# PRIVATE_TITLE\nPRIVATE_BODY\n');
  console.log(JSON.stringify({case:'duplicate-privacy',header,result:await sourceRecords(temp,'root',{action:'index',expected_source_revision:source},2000)}));
 }
 const open=fs.promises.opendir.bind(fs.promises);let handle:any,closed=false;let work:Promise<any>|undefined;
 fs.promises.opendir=(async(...args:any[])=>{handle=await (open as any)(...args);const close=handle.close.bind(handle);handle.close=async()=>{closed=true;return close()};await Bun.sleep(30);return handle}) as any;
 const result=await sourceRecords(temp,'root',{action:'index',expected_source_revision:source},5,w=>work=w);
 await work;fs.promises.opendir=open as any;
 console.log(JSON.stringify({case:'opendir-deadline',result,actual_work_settled:true,opened:!!handle,closed}));
 if(handle&&!closed)await handle.close();
}finally{fs.rmSync(temp,{recursive:true,force:true})}
