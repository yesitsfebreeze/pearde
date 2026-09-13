---
complexity: low
footprint:
- .cartridge/docs/capabilities.md
- .cartridge/docs/cost-latency.md
- .cartridge/docs/decisions.md
- .cartridge/tests/unit/catalog/capabilities.rs
- .cartridge/tests/unit/proxy/capabilities.rs
- .cartridge/tests/unit/sync/tests.rs
- .cartridge/tests/unit/telemetry.rs
- Cargo.toml
- src/catalog.rs
- src/decision.rs
- src/main.rs
- src/proxy.rs
- src/requirements.rs
- src/sync.rs
- src/telemetry.rs
---


# Verify the integrated router improvement programme

This rollup adds no product behavior. At collection time validate all three
external `needs` with the PRD engine's own completion checks: committed receipt,
ancestor source commit, exact spec digest, checked acceptance, clean verified
source footprint and no active lane. Verify the current recorded review is passed,
within five rounds and at least 90/100. Pin the three reviewed spec contracts below
and record current PRD/review/receipt digests and source revisions in proof output.

The source footprint is exactly the union of those leaves. Run the full router
suite and public check together after dependency receipt refresh, covering admission, fallback, request decisions and attributed cost/latency, including
finite recovery interacting with their shared provider boundary. A stale/missing dependency or changed contract fails this proof;
no rollup completion is inferred from a historical done marker.

This is a point-in-time integration receipt. The engine does not treat external
`needs` as nested children. The source union detects later implementation changes;
if a dependency contract changes without source changes, explicitly reverify this
rollup rather than claiming recursive engine invalidation that does not exist.

## Acceptance

- [x] All three dependency receipts and reviews validate at integrated revisions, and the recorded source footprint equals their union.
- [x] Complete owner tests and check pass with these contracts together; proof records current source and dependency artifact digests.
- [x] Retained limitations are explicit: capability declarations are evidence rather than provider guarantees; stale/unknown pricing remains explicit; estimates are not invoices; stream handoff is partial and does not prove client delivery; bounded decision archives are process-local.

## Verify and Proof

```sh
set -eu
cd /Users/feb/dev/cartridge/prd.ctg
bun -e '
import fs from "node:fs";
import path from "node:path";
import {scan,specs,hash,git,codeRepo} from "./src/records.ts";
import {completionProblem} from "./src/lifecycle.ts";
import {feet} from "./src/planner.ts";
const graph=scan(process.cwd()+"/.cartridge/boards/root");
const expected={
  "@router/improve-router-route-explanation": "3d2578f2a869363880c15e05b90530ce52f7e4d0c7c29e8264fa2aa3d99d8571",
  "@router/improve-router-capability-routing": "aeada460bce0000ca8ff3c31f07f988c9aed27208518552c18521e3322e39044",
  "@router/improve-router-cost-latency": "a0b3c29c5806e1fe5175185242774370ef52e6a210cd5689c12b237eec690b6a"
};
const parent=graph.get("@router/improve-router-programme");
if(!parent) throw Error("missing canonical rollup");
const owner=codeRepo(parent), union=new Set(), evidence=[];
for(const [ref,digest] of Object.entries(expected)) {
  const child=graph.get(ref); if(!child) throw Error("missing dependency "+ref);
  const problem=completionProblem(child,graph);if(problem)throw Error(ref+": "+problem);
  const contracts=specs(child);
  if(contracts.length!==1 || hash(contracts[0].text)!==digest)throw Error(ref+": reviewed child contract changed");
  const round=Number(child.fm["review-round"]);
  const review=fs.readFileSync(path.join(child.dir,"review.md"),"utf8");
  const section=review.split("## Round "+round+" ")[1]?.split("\n## Round ")[0];
  const score=Number(section?.match(/\*\*(\d+)\/100/)?.[1]);
  if(child.fm["review-status"]!=="passed" || round<1 || round>5 || score<90 || !Number.isFinite(score))throw Error(ref+": missing passing current agent review");
  for(const footprint of feet(child))union.add(path.relative(owner,footprint));
  evidence.push({ref,commit:child.fm.commit,prd_sha256:child.revision,spec_sha256:digest,review_round:round,score,review_sha256:hash(review),collection_sha256:hash(fs.readFileSync(path.join(child.dir,"collection.md")))});
}
const covered=[...new Set(feet(parent).map(file=>path.relative(owner,file)))].sort();
if(JSON.stringify(covered)!==JSON.stringify([...union].sort()))throw Error("rollup footprint does not equal child union");
console.log(JSON.stringify({source_commit:git(owner,["rev-parse","HEAD"]),records_commit:git(process.cwd(),["rev-parse","HEAD"]),footprint:covered,dependencies:evidence},null,2));
'
cd /Users/feb/dev/cartridge/cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just test router
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just check router
```

The baseline records integrated recovery source and the older three receipts.
Refresh those receipts before this gate. Preserve prior receipts as history;
a failed integration check leaves the rollup unfinished.
