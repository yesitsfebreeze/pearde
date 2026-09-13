import fs from 'node:fs';import os from 'node:os';import path from 'node:path';
import {sourceRecords} from '/Users/feb/dev/cartridge/prd.ctg/src/source-records.ts';
import {hash,sourceDeclarations} from '/Users/feb/dev/cartridge/prd.ctg/src/records.ts';
const temp=fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(),'prd-deadline-review-'))),root=path.join(temp,'root');
fs.mkdirSync(path.join(root,'prds/a'),{recursive:true});const settings='---\nmembers: {}\n---\n',content='# public\nbody\n';
fs.writeFileSync(path.join(root,'settings.md'),settings);fs.writeFileSync(path.join(root,'prds/a/prd.md'),content);
const stringify=JSON.stringify;let delayed=false;
try{
 JSON.stringify=((value:any,...args:any[])=>{if(value?.schema==='cartridge-source-records/v1'&&value?.action==='read'){delayed=true;Bun.sleepSync(60)}return (stringify as any)(value,...args)})as any;
 const started=performance.now(),result=await sourceRecords(temp,'root',{action:'read',path:'prds/a/prd.md',expected_source_revision:hash(settings),expected_revision:hash(content)},30);
 JSON.stringify=stringify;console.log(JSON.stringify({case:'final-read-serialization-deadline',elapsed_ms:performance.now()-started,deadline_ms:30,delayed,result}));
 const hidden=path.join(temp,'.hidden');fs.renameSync(root,hidden);
 console.log(JSON.stringify({case:'granted-hidden-board',declarations:await sourceDeclarations(temp,'.hidden',2000),records:await sourceRecords(temp,'.hidden',{action:'index',expected_source_revision:hash(settings)},2000)}));
}finally{JSON.stringify=stringify;fs.rmSync(temp,{recursive:true,force:true})}
