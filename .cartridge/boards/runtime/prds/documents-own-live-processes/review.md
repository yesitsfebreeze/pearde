# Sidecars, event tools, and reload have explicit lifetimes — review

Canonical PRD: [@runtime/documents-own-live-processes](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [documents-own-live-processes](../../../root/reviews/round-1/documents-own-live-processes.md): reviewer 85/100; Split. Separate sidecar lifetime from event activation; settle event acknowledgement/deduplication and handoff of exclusive listeners or writers before implementation.
  Original SHA-256: `75f4d40c468a29f7c36d7ca8c32ca4d4111e67422c49c65aa3986eb3b1101404`.

Historical dimension scores were not recorded. The original user-rating field was pending; the current workflow delegates scoring to the agent. Splitting does not reset the allowance.

## Round 2 — 2026-09-13

Revision: the working-tree PRD and the exact input digests in [review-inputs.json](review-inputs.json).
Change: small owner-local contract; broad parents point to leaves, and canonical aliases share one implementation scope.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 18 | The PRD states its bounded outcome; inherited broader requirements are retained in source history and linked children. |
| Ownership and reuse | 20 | Named cartridge and existing starting files; historical duplicate IDs are mapped to this canonical scope. |
| Dependencies and slices | 20 | Qualified hard dependencies resolve; the complete parent/child graph is acyclic. |
| Acceptance and baseline | 18 | Unchecked behavioral acceptance and a real repository gate; fixture details and measured baselines must be captured before specs. |
| Failure and compatibility | 18 | Negative outcomes and a recovery boundary are retained; implementation must supply the specified failure proof. |

Agent score: **94/100 — PASS**.
Finding: Parent reduced to linked scope and integration acceptance; only leaves are implementation work.
Blocking review findings: none; implementation prerequisites remain in the PRD.
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Round 3 — 2026-09-14

Reconciliation verdict: **REBASE** (rollup). Old footprint (`src/process.rs`, `src/reload.rs`, `src/stream.rs`, justdown sidecars on fibers) is gone; current equivalents are helper programs via `cartridge.spawn` (`src/node.rs`), channels (`src/transport/cartridge.rs`) and replacement with a generation guard (`src/host/mod.rs:455-534`). Revision points at these paths, fixes the `capability-capability-owner` key typo (value unchanged) and assigns the two sibling overlaps.
Stale presented revision: `bbd271850e9364da579739ebee0339b35415b8bdff8846834f323ee117be80d8`. Revised revision: `8c076523ed1124bb36bbce3f464f2905a1d0e9120f24f44b553f2207c9e942a2`.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 17 | Owned lifetimes remain wanted. -3: "documents" (justdown) framing unverified against current memo-run runner. |
| Ownership and reuse | 17 | Parent assigns overlaps to `extension-loader-plugin-tree` and `a-listener-subscribes-to-event-types`. -3: children still carry the duplicate clauses. |
| Dependencies and slices | 15 | Child needs resolve. -5: both children cite absent `cartridge.ctg/src/runtime.rs`/`service.rs` and need the stale rollup child `one-runner-executes-documents/document-command-result`; not implementable as linked. |
| Acceptance and baseline | 18 | Roll-up acceptance plus `just test runtime`. -2. |
| Failure and compatibility | 18 | No implementation in parent. -2. |
| Reviewer total | 85 / 100 | |

Result: **FAIL**. Blocking findings: children `document-sidecar-lifecycle` and `document-event-activation` (outside this reviewer's assignment) must be rebased and narrowed first; `one-runner-executes-documents` chain is stale.
Validation: cheap existence checks only — ls/rg over cartridge.ctg (HEAD c9ef10b), tools.ctg (caea5b7) and memory.ctg (c25af4d) source; `just --list` at /Users/feb/dev/cartridge; relative-link resolution over prd.md; `shasum -a 256`. No product gates were run.
Reviewer: agent (independent reviewer, plan refresh pass). User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2. Next action: rebase the children, then re-review this parent.
