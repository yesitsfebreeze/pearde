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

# Qualify the integrated GitFS improvement programme

This rollup adds no product behavior. Preserve its two original acceptance checks:
the linked readable-diff, selected-snapshot and reviewed-shipping outcomes must
pass together, with tested mitigations and remaining limits recorded at exact
integrated revisions. All three receipts currently remain valid at b4b95bb; that is the
observed baseline, not a reason to skip current verification.

Check the exact three declared needs plus all seven distinct transitive GitFS and
Policy contracts: current completion, checked acceptance, pinned spec digests,
independent current review >=90 within five rounds and clean verified source.
Bind the programme footprint to their GitFS-only source union. Record current
receipt/review/PRD hashes and policy source separately. External prerequisite
changes require explicit revalidation; the engine does not recursively invalidate
all external needs by itself.

Reuse the existing digest-pinned actual MCP→policy→GitFS disposable composition
proof. Run the full owner suite/check/build and maintained local/push native
fixtures. These demonstrate selected owned snapshots and inspected base/overlay/
disk changes, exact reviewed local commit, recorded push and read-only confirmed
reconciliation while unrelated index/worktree/ref bytes remain unchanged.

Retain tested refusal for stale head/tree/index/remote, denied operation and missing
gates, timeout/cancellation before publication, and bounded helper cleanup. A
network outcome may remain unknown; there is no automatic push replay or remote
rollback. Default ship.push remains ask, and native scope grants do not establish
phase-specific policy or interactive approval. Direct FS ownership remains separate
from GitFS overlays; real user repositories/remotes/credentials are never fixtures.

## Acceptance

- [x] All exact linked and transitive contracts retain passing reviews, checked acceptance and current receipts; the declared owner source union and external identities match.
- [x] Current public/native/composition proof passes at the integrated revisions, retaining all selected-content, refusal/no-replay behavior and explicit documented limits above.

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
  "@gitfs/improve-gitfs-readable-diff": "24f1ea5b670c4ad4251838837f85f633f209437c9b5bfc44df8d69dcef483d9b",
  "@gitfs/improve-gitfs-snapshot-selection": "a3bdd842ca5f317edfbe883ee61fd0ddaff465c81c9d44183aab9e6bc852c8c6",
  "@gitfs/improve-gitfs-reviewable-ship": "ab54d545cb3d4c525ce32d4c62c7b5a82c4233286f751c985036a0cfa9b12b3c",
  "@gitfs/improve-gitfs-reviewable-ship/reviewed-owned-tree-commits-locally": "73b025bce9603f1a750a9597017093fa3980f7e4384dc00317553e85f2430473",
  "@gitfs/improve-gitfs-reviewable-ship/recorded-push-reconciles-the-exact-remote-head": "3191d544dd1c2260d832f51526baa1c59cee84dc4772c9496ff59507d3c61841",
  "@policy/improve-policy-operation-rules": "4c387100550778313009dff4a94703b2b6232c874fe469f56167f487e05d707d",
  "@policy/ship-push-is-an-explicit-policy-operation": "c313a77d300b54994b0eef60a4474efc57376d6db4882e5e5f9c8175f037e49d"
};
const parent=graph.get("@gitfs/improve-gitfs-programme");
if(!parent)throw Error("missing parent");
if(JSON.stringify([...parent.fm.needs].sort())!==JSON.stringify(["@gitfs/improve-gitfs-readable-diff", "@gitfs/improve-gitfs-snapshot-selection", "@gitfs/improve-gitfs-reviewable-ship"].sort()))throw Error("prerequisites changed");
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

