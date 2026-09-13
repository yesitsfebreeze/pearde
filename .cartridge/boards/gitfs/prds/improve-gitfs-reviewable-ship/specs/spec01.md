---
complexity: low
footprint:
- .cartridge/docs/inspection.md
- .cartridge/docs/push.md
- .cartridge/docs/ship.md
- .cartridge/tests/integration/recorded-push.test.ts
- .cartridge/tests/integration/reviewed-ship.test.ts
- .cartridge/tests/integration/tool-result.test.ts
- .cartridge/tests/unit/push/tests.rs
- .cartridge/tests/unit/ship/tests.rs
- .cartridge/tests/unit/snapshot.rs
- .cartridge/tests/unit/store/tests.rs
- .cartridge/tests/unit/tool_result.rs
- init.lua
- src/inspection.rs
- src/main.rs
- src/push.rs
- src/service.rs
- src/ship.rs
- src/store.rs
- src/tool_result.rs
---

# Verify the integrated reviewed shipping path

This rollup adds no GitFS product behavior. Preserve the parent's original three
acceptance conditions. Validate all six hard prerequisites below with the PRD
engine's current completion checks, exact pinned spec digests, current independent
reviews at least90/100 within five rounds, checked acceptance and current clean
source footprints. Record child receipt/review/PRD/source digests. Two prerequisites
are nested local-commit/push children; readable diff, snapshot selection and the two
policy contracts are external needs. External contract changes require explicit
reverification; do not claim recursive invalidation that the engine does not supply.

The parent source footprint is exactly the union of the four GitFS prerequisite
footprints. Policy remains policy-owned, with its exact completion/source evidence
recorded rather than an illegal outside-repository source footprint.

Run a digest-pinned disposable composition proof using actual GitFS and MCP native
processes and real policy Lua. Sessions is only a fixed fixture identity. Explicit
operation grants authorize the separate calls; a denied materialization performs
no write. Write two owned overlays, snapshot only one selected disk path, inspect
base/overlay/disk differences, and retain unrelated staged plus unstaged bytes.
Publish the exact reviewed local tree; neither unrelated staged content nor the
unselected disk change may enter it. With the same trusted session, preview and
commit a recorded push to a disposable bare remote, then read-only reconcile the
same operation. Require identical local/remote target, unchanged unrelated ref,
unchanged shared index/worktree, explicit confirmed state and executable hashes.

Run the full owner suite/check and both maintained native child suites. Their
negative cases prove stale tree/index/head refusal, required gate refusal/timeout
including explicit subjects, pre-publication cancellation, exact advertised remote
head/server CAS, durable unknown outcomes, restart, no replay and bounded helper
cleanup. The combined proof qualifies the original result: it does not claim remote
rollback, default push permission, phase-specific policy, interactive approval,
durable remote acknowledgement from old/different readback, or automatic recovery.
Prior local, remote, readable, snapshot and policy receipts must be current first.

## Acceptance

- [x] Exact current prerequisite receipts/reviews pass, with the GitFS footprint equal to their owner-local union and all source/artifact identities recorded.
- [x] Actual MCP→policy→GitFS composition snapshots/inspects owned content, excludes unrelated staged bytes from the reviewed commit, pushes/reconciles that exact commit and preserves the shared index, disk and unrelated remote ref.
- [x] Public owner checks and both native child suites pass together, retaining all original parent refusal/cancellation/no-replay conditions and explicit policy/unknown-outcome limits.

## Verify and Proof

```sh
set -eu
cd /Users/feb/dev/cartridge/prd.ctg
bun - <<'TS'
import fs from "node:fs";
import path from "node:path";
import {scan,specs,hash,git,codeRepo} from "./src/records.ts";
import {completionProblem} from "./src/lifecycle.ts";
import {feet} from "./src/planner.ts";
const graph=scan(process.cwd()+"/.cartridge/boards/root");
const expected={
  "@policy/ship-push-is-an-explicit-policy-operation": "c313a77d300b54994b0eef60a4474efc57376d6db4882e5e5f9c8175f037e49d",
  "@gitfs/improve-gitfs-readable-diff": "24f1ea5b670c4ad4251838837f85f633f209437c9b5bfc44df8d69dcef483d9b",
  "@gitfs/improve-gitfs-snapshot-selection": "a3bdd842ca5f317edfbe883ee61fd0ddaff465c81c9d44183aab9e6bc852c8c6",
  "@policy/improve-policy-operation-rules": "4c387100550778313009dff4a94703b2b6232c874fe469f56167f487e05d707d",
  "@gitfs/improve-gitfs-reviewable-ship/reviewed-owned-tree-commits-locally": "73b025bce9603f1a750a9597017093fa3980f7e4384dc00317553e85f2430473",
  "@gitfs/improve-gitfs-reviewable-ship/recorded-push-reconciles-the-exact-remote-head": "3191d544dd1c2260d832f51526baa1c59cee84dc4772c9496ff59507d3c61841"
};
const parent=graph.get("@gitfs/improve-gitfs-reviewable-ship");
if(!parent)throw Error("missing parent");
if(JSON.stringify([...parent.fm.needs].sort())!==JSON.stringify(Object.keys(expected).sort()))throw Error("prerequisites changed");
const owner=codeRepo(parent),union=new Set(),evidence=[];
for(const [ref,digest] of Object.entries(expected)) {
 const child=graph.get(ref);if(!child)throw Error("missing "+ref);
 const problem=completionProblem(child,graph);if(problem)throw Error(ref+": "+problem);
 const contracts=specs(child);if(contracts.length!==1||hash(contracts[0].text)!==digest)throw Error(ref+": contract changed");
 const round=Number(child.fm["review-round"]),review=fs.readFileSync(path.join(child.dir,"review.md"),"utf8");
 const headings=[...review.matchAll(/^## Round\s*(\d+)\b[^\n]*$/gm)];
 const at=headings.findIndex(h=>Number(h[1])===round);
 const section=at<0?"":review.slice(headings[at].index,headings[at+1]?.index??review.length);
 const score=Number(section.match(/\b(\d{1,3})\/100\b/)?.[1]);
 if(!["passed","accepted"].includes(child.fm["review-status"])||!section.includes("PASS")||round<1||round>5||!Number.isFinite(score)||score<90||score>100)throw Error(ref+": passing review missing");
 if(codeRepo(child)===owner)for(const f of feet(child))union.add(path.relative(owner,f));
 evidence.push({ref,source_commit:child.fm.commit,prd_sha256:child.revision,spec_sha256:digest,review_round:round,score,review_sha256:hash(review),collection_sha256:hash(fs.readFileSync(path.join(child.dir,"collection.md")))});
}
const covered=[...new Set(feet(parent).map(f=>path.relative(owner,f)))].sort();
if(JSON.stringify(covered)!==JSON.stringify([...union].sort()))throw Error("source footprint is not the owner-local union");
const proof=".cartridge/boards/gitfs/prds/improve-gitfs-reviewable-ship/rollup-proof.ts";
if(hash(fs.readFileSync(proof))!=="b8845814d7e60b7492ece92f6d4f60c1269e7f73e4f5ec7054004c3031dcc9d2")throw Error("composition proof changed");
console.log(JSON.stringify({source_commit:git(owner,["rev-parse","HEAD"]),records_commit:git(process.cwd(),["rev-parse","HEAD"]),footprint:covered,dependencies:evidence,composition_proof_sha256:"b8845814d7e60b7492ece92f6d4f60c1269e7f73e4f5ec7054004c3031dcc9d2"},null,2));
TS
cd /Users/feb/dev/cartridge/cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just test gitfs
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just check gitfs
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just build gitfs
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just build mcp
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" cargo build --manifest-path Cargo.toml --bin cartridge
GITFS_BINARY="$PWD/target/tool-result-contract/debug/gitfs" bun test ../gitfs.ctg/.cartridge/tests/integration/reviewed-ship.test.ts ../gitfs.ctg/.cartridge/tests/integration/recorded-push.test.ts
bun ../prd.ctg/.cartridge/boards/gitfs/prds/improve-gitfs-reviewable-ship/rollup-proof.ts
```

Retain the original stale-tree deletion baseline unchanged. Supplemental integration
baseline at GitFS b4b95bb / policy e442bef proves the combined composition can run;
it does not complete the parent while prerequisite receipts are stale. The new
policy leaf resolves the measured unknown ship.push integration gap. No persistent
user repository, real external remote, model service or credential is involved.
