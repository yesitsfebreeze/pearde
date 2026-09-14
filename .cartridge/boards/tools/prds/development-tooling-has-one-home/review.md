# Development commands and verification have one owning implementation — review

Canonical PRD: [@tools/development-tooling-has-one-home](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [development-tooling-has-one-home](../../../root/reviews/round-1/development-tooling-has-one-home.md): reviewer 84/100; Split. Separate package relocation, reproducible bundles and gate integration; reconcile existing preflight/provenance/resume leaves before retiring their owner.
  Original SHA-256: `29135b4eab7d6a5fdbaebd508f564c219de7f5df9a20a2920a848d1edd39d9d9`.

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

## Round 3 — 2026-09-14 (reconciliation)

Reconciliation verdict: **SUPERSEDED**.

Reviewed revision: prd.md SHA-256 `06f33c83256d656ef5eab70d8c10dc346c7ac779cef25d1ced9a6c1af25f9b2d` (frontmatter afterwards set to review-round 3 / superseded-recommend-retire; body unchanged). Source revisions: tools.ctg caea5b7, cartridge.ctg c9ef10b, root main 24aa2be, prd.ctg 077e57a2 (dirty tree).

Evidence: the roll-up's route was to relocate tools' implementation into a runtime-owned package in cartridge.ctg (`@runtime/runtime-development-package`, starting files `cartridge.ctg/src/runtime.rs` and `service.rs`, which no longer exist). Later decisions and commits took the other route: (1) `.cartridge/memos/decision/tui-and-tools-are-cartridges.md` keeps repository bundle/lane operations in the tools cartridge, and `tools.ctg/.cartridge/help.md` says tools "stays out of the runtime binary"; (2) cartridge.ctg b1494bb "This repository is the base, not a composition"; (3) `.cartridge/memos/decision/cartridge-repositories-keep-records-and-executable-memos.md` (2026-09-13) moves development operations into routine memos — the one home for build/check/test is now the root `justfile` → `.cartridge/justfile` → `.cartridge/memos/routine/cartridge-development.md` (owner selection with explicit unknown-owner failure, line 78); (4) `.cartridge/memos/decision/a-cartridge-brings-its-own-surface.md` keeps each cartridge's surface in its own directory.
Findings: the clean-checkout / source-absent bundle outcome (`@runtime/development-clean-checkout`) may still be wanted, but it should be rebased as an independent leaf against the routine memos and tools.ctg, not kept under this relocation roll-up (coordinator/runtime board). Its needs on `@runtime/improve-tools-*` and `@memo/one-document-serves-every-reader/document-identity` also need reconciliation there. `capability-capability-owner` typo is board-wide.
Disposition: retire recommendation; do not delete; `state:` unchanged. No score recorded.
Validation: ls of cartridge.ctg/src, reads of decisions, tools help.md, root justfile and routine; `just --list`. No product gates were run.
Reviewer identity: agent (independent reviewer, plan refresh pass). User rating: not required. User feedback: none supplied.
Result: SUPERSEDED — recommend retire. Unresolved blocking findings: none for this roll-up.
Rounds used / remaining: 3 / 2.
Next action: coordinator confirms retirement and rebases the clean-checkout child independently.
