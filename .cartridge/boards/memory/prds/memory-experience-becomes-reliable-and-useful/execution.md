# Execution handoff — 2026-09-19

Reassessment is complete. This pass changes planning documentation and captures evidence; it does not implement engine fixes or complete implementation acceptance criteria.

## Verified state

The 13 recorded critical-source digests and reviewed plan inputs are unchanged. The existing independent reviews still apply: 11 implementation leaves plus their parent roll-up passed outcome-plan review. All remain open and unclaimed, with implementation specs still to write. See [inventory](plan-inventory.json), [investigation](investigation.md), and [fresh evidence](evidence/reassessment-2026-09-19/).

All 21 services report active and ASP responds. That is not proof of memory health: cycle 306 failed with `activity graph commit refused stale snapshot; reload required, inputs retained` (one failure in the retained 64-cycle snapshot). The intake snapshot contains 145 pending rows; it excludes historical backlog and is not a total remaining-work count. Jeff timed out and explicitly returned fallback guidance to gather evidence directly.

The existing experience tests passed: graph 5, RPC 7, store 2. All eight saved characterization probes passed; they reproduce defects, not repaired behavior. Root PRD validation passed across 754 records with no problems or warnings. Proposed retrieval/latency thresholds remain unmeasured.

## Before starting implementation

1. Reconcile the existing claim on `@memory/memory-crystallizes-the-systems-activity-by-its-reasons/memory-stands-alone-with-clear-engine-and-integration-boundaries` with its owner. It overlaps the first new leaves. Inspect and collect completed work or use an appropriate owner-approved PRD transition; do not erase the claim or someone else's changes.
2. Establish a committed, verified integration baseline containing the existing crystallization implementation. The memory brief currently names HEAD `55863b356c7c75032b6a525dbe8addc5b29b924f`; significant implementation is still in the working tree. Implementation claims create worktrees from HEAD. Preserve unrelated changes and reconcile the original feature PRDs rather than committing the entire dirty workspace.
3. Reconcile the existing frozen-query and readback PRDs with implemented APIs. Prefer the existing canonical read-only contract over introducing competing `touch:false`, `--no-touch`, and `read_only` semantics. Preserve the existing `tool.memory` readback carve-out unless explicitly revised and reviewed.

These are coordination prerequisites, not reasons to redesign the approved plan.

## Execution order

| Stage | Work | Gate |
| --- | --- | --- |
| 1 | Writer coordination, total-backlog/progress status, memory-owned acceptance/refusal contract | Establish the advancing writer using a deterministic interleaving; preserve the stale-snapshot guard. Serialize overlapping footprints. |
| 2 | Bounded/fair intake after writer coordination; host delivery handling after the acceptance contract | Invalid or expensive records cannot starve healthy intake; permanent refusals cannot wedge host delivery. Recheck runtime claims before claiming. |
| 3 | Evidence/uncertainty attribution, then outcome/context/validity merge boundaries; output-fidelity readback | Similarity must not erase outcome, scope, validity, or evidence distinctions. Exact-ID single/batch reads and ASP report representative/sample/unavailable fidelity honestly. |
| 4 | Existing frozen-query/readback prerequisites; reproducible evaluation baseline; separate recurrence and retrieval-use signals | Capture the baseline before changing ranking or similarity thresholds. Evaluate each change against hard-boundary, quality, and latency gates. |
| 5 | Scope integration after status and signal contracts; integrated restart and failure-recovery proof | Show actual memory use and stalled processing in the existing ASP graph/inspector, with freshness and loaded-generation evidence. |

Stage order is an execution recommendation; canonical hard dependencies remain in each PRD. Independent leaves can proceed only when their actual footprints and ownership permit it. The parent is a roll-up, not another implementation job. Existing initial-feature PRDs remain authoritative for their unfinished work.

Keep ownership clear: memory owns semantic records, crystallization, retrieval, and retention. Base/runtime owns genuinely shared transport and negotiated delivery mechanics, without importing memory semantics. Scope consumes the memory/ASP contracts. Semantic condensation preserves declared representative evidence; it cannot reconstruct information that was discarded.

## Commands and per-leaf workflow

Run from the composition root:

```sh
./prd.ctg/prd check --board root --json
./prd.ctg/prd plan --board root --limit 200 --json
prd_ref='@memory/memory-experience-becomes-reliable-and-useful/crystallization-keeps-progressing-beside-ordinary-persistence'
./prd.ctg/prd brief "$prd_ref" --board root --role analyst --json
./prd.ctg/prd claim "$prd_ref" memory-coordinator --board root --dry --json
```

The dry claim is a readiness check, not an override. After the prerequisites above are resolved, use the checked PRD lifecycle:

1. Claim the open leaf for analysis and write `specNN.md` using the repository spec template and assigned analyst workflow. An open-state claim does not create an implementation worktree. Define canonical source/test footprints, migrations, recovery, and named acceptance tests. Include runtime's actual launch integration test path when specifying delivery.
2. Review the spec against the approved PRD, then run `prd specced` with the same ref and `--board root`. This validates required specs and clears the analysis claim. Substantive contract changes require renewed plan review; do not reset review history.
3. Claim the specced leaf for implementation. Verify the created worktree's baseline and follow its brief. Do not use an old checkout or edit beyond the assigned footprint.
4. Implement and run spec verification. Use an isolated `CARGO_TARGET_DIR` for builds, for example `${CARGO_TARGET_DIR:-$PWD/target/memory-writer-verify}`, so checks do not inadvertently replace a loaded development cartridge. Verification commands must work from both the lane and repository, use relative paths, and prove named tests actually ran.
5. Obtain independent verification, then use checked `prd collect` with the ref and board. Collect only the assigned footprint; preserve unrelated work. Run owner audit and isolation checks, update ranking evidence, and rescan dependencies before selecting the next leaf.
6. At the integration gate, use a backed-up test store and controlled activation. Verify loaded artifact/generation, durable intake through crystallization and retrieval into ASP/Scope, restart recovery, model outage, and stale-writer recovery. Do not equate a successful build or active service with deployment of the intended artifact.

Use `./prd.ctg/prd` before each operation named above. `prd run` requires a configured adapter; it is not a substitute for this lifecycle. Avoid a global `next` that can select unrelated board work; restrict selection to this inventory and its existing prerequisites.

## Completion evidence

Completion requires repaired-behavior tests for writer races and crash recovery, intake fairness and disposition handling, outcome/context/validity exclusions, read-only retrieval, signal separation, honest output fidelity, and Scope behavior. Extend the existing evaluation harness rather than introducing another engine. Measure the proposed gates (zero harmful hard-boundary merges, recall@5 at least 0.90, no more than two percentage points recall regression, and at most 10% p95 latency regression on the same pinned workload) before claiming they pass. Retain integrated live proof and all PRD collection receipts.
