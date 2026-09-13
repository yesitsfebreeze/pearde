---
complexity: low
footprint:
- src/main.rs
- src/service.rs
- src/streaming.rs
- src/usage.rs
- src/continuation.rs
- src/trace.rs
- .cartridge/tests/unit/tests.rs
- .cartridge/docs/usage.md
- .cartridge/docs/continuations.md
- .cartridge/docs/traces.md
- Cargo.toml
- cartridge.json
- src/context.rs
- src/wire.rs
---

# Verify the integrated proxy improvement programme

This rollup adds no product behavior. At collection time validate all three
external `needs` with the PRD engine's own completion checks: committed receipt,
ancestor source commit, exact spec digest, checked acceptance, clean verified
source footprint and no active lane. Verify the current recorded review is passed,
within five rounds and at least 90/100. Pin the three reviewed spec contracts below
and record current PRD/review/receipt digests and source revisions in proof output.

The source footprint is exactly the union of those leaves. Run the full proxy
suite and public check together after dependency receipt refresh, covering JSON,
all three SSE wires, accounting, continuation authority/recovery and bounded tool
trace semantics. A stale/missing dependency or changed contract fails this proof;
no rollup completion is inferred from a historical done marker.

This is a point-in-time integration receipt. The engine does not treat external
`needs` as nested children. The source union detects later implementation changes;
if a dependency contract changes without source changes, explicitly reverify this
rollup rather than claiming recursive engine invalidation that does not exist.

## Acceptance

- [x] All three dependency receipts and reviews validate at integrated revisions, and the recorded source footprint equals their union.
- [x] Complete owner tests and check pass with these contracts together; proof records current source and dependency artifact digests.
- [x] Retained limitations are explicit: usage counts are provider-reported rather than billing guarantees; traces and continuation maps are bounded/process-local; shared HTTP keys denote shared principals; cancellation requests do not prove rollback or completion; caller history and native provider IDs remain caller/provider owned.

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
  "@proxy/improve-proxy-total-usage":"d352e4dd49e0dc9547cf7bae2f5e9603df2145d4bc50a7fbca2032d2796b73c0",
  "@proxy/improve-proxy-tool-trace":"098dcdd949a8e71002438f17bbd0638922934b95cd68b8807a32c6602774ca1e",
  "@proxy/improve-proxy-continuation-recovery":"e47b432ca4747609f5d62a90decd713ee630747f01f7d9285d0b13af1930e172"
};
const parent=graph.get("@proxy/improve-proxy-programme");
if(!parent) throw Error("missing canonical rollup");
const owner=codeRepo(parent), union=new Set(), evidence=[];
for(const [ref,digest] of Object.entries(expected)) {
  const child=graph.get(ref); if(!child) throw Error("missing dependency "+ref);
  const problem=completionProblem(child,graph);if(problem)throw Error(ref+": "+problem);
  const contracts=specs(child);
  if(contracts.length!==1 || hash(contracts[0].text)!==digest)throw Error(ref+": reviewed child contract changed");
  const round=Number(child.fm["review-round"]);
  const review=fs.readFileSync(path.join(child.dir,"review.md"),"utf8");
  const section=review.split(/^## Round\s*(\d+)\b[^\n]*$/m).reduce((found,part,i,parts)=>part===String(round)?parts[i+1]:found,undefined);
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
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/proxy-trace" just test proxy
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/proxy-trace" just check proxy
```

The baseline records source `4395941`: tool-trace was already collected, while
older accounting and continuation receipts were stale after shared-file changes.
Refresh those receipts before executing this gate. Preserve prior receipts as
history; failure leaves the rollup unfinished and does not alter product source.
