import fs from "node:fs";
import path from "node:path";
import {scan,specs,hash,git,codeRepo} from "../../../../../src/records.ts";
import {completionProblem} from "../../../../../src/lifecycle.ts";
import {feet} from "../../../../../src/planner.ts";
const root=path.resolve(import.meta.dir,"../../../../..");
const binding=JSON.parse(fs.readFileSync(path.join(import.meta.dir,"rollup-bindings.json"),"utf8"));
const graph=scan(path.join(root,".cartridge/boards/root"));
const parent=graph.get(binding.parent);if(!parent)throw Error("missing parent");
const same=(a:unknown,b:unknown)=>JSON.stringify(a)===JSON.stringify(b);
if(!same([...parent.fm.needs].sort(),binding.direct))throw Error("direct prerequisites changed");
const closure=new Set<string>();function visit(id:string){if(closure.has(id))return;closure.add(id);const r=graph.get(id);if(!r)throw Error("missing "+id);for(const n of r.fm.needs??[])visit(n);}
binding.direct.forEach(visit);
if(!same([...closure].sort(),Object.keys(binding.contracts).sort()))throw Error("dependency closure changed");
const evidence=[];const union=new Set<string>();const owner=codeRepo(parent);
for(const [ref,pin] of Object.entries(binding.contracts) as [string,any][]){
 const child=graph.get(ref)!;const problem=completionProblem(child,graph);if(problem)throw Error(ref+": "+problem);
 const contract=specs(child);if(contract.length!==1||hash(contract[0].text)!==pin.spec_sha256)throw Error(ref+": contract changed");
 if(!same([...child.fm.needs??[]].sort(),pin.needs))throw Error(ref+": prerequisites changed");
 if(child.fm.commit!==pin.source_commit||git(codeRepo(child),["rev-parse","HEAD"])!==pin.source_commit)throw Error(ref+": source identity changed");
 const round=Number(child.fm["review-round"]),review=fs.readFileSync(path.join(child.dir,"review.md"),"utf8");
 const headings=[...review.matchAll(/^## Round\s*(\d+)\b[^\n]*$/gm)],at=headings.findIndex(h=>Number(h[1])===round);
 const section=at<0?"":review.slice(headings[at].index,headings[at+1]?.index??review.length);
 const score=Number(section.match(/\b(\d{1,3})\/100\b/)?.[1]);
 if(!["passed","accepted"].includes(child.fm["review-status"])||!section.includes("PASS")||round<1||round>5||!Number.isFinite(score)||score<90||score>100)throw Error(ref+": current review missing");
 if(binding.direct.includes(ref)&&codeRepo(child)===owner)for(const f of feet(child))union.add(path.relative(owner,f));
 evidence.push({ref,source_commit:pin.source_commit,prd_sha256:child.revision,spec_sha256:pin.spec_sha256,review_round:round,score,review_sha256:hash(review),collection_sha256:hash(fs.readFileSync(path.join(child.dir,"collection.md")))});
}
const footprint=[...new Set(feet(parent).map(f=>path.relative(owner,f)))].sort();
if(!same(footprint,[...union].sort()))throw Error("parent footprint differs from direct FS outcome union");
for(const [file,digest] of Object.entries(binding.fixtures))if(hash(fs.readFileSync(file))!==digest)throw Error("native fixture changed: "+file);
console.log(JSON.stringify({source_commit:git(owner,["rev-parse","HEAD"]),records_commit:git(root,["rev-parse","HEAD"]),footprint,dependencies:evidence,fixtures:binding.fixtures},null,2));
