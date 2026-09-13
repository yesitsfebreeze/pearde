# cartridges-compose-recursively — review

Canonical PRD: [@runtime/cartridges-compose-recursively](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [cartridges-compose-recursively](../../../root/reviews/round-1/cartridges-compose-recursively.md): reviewer 81/100; Reconcile. Separate delivered declarations/nesting from remaining demand/install work; refresh stale core paths and retire unsupported calendar estimates.
  Original SHA-256: `0138d014b8999a5b73368b2fbf434ec4136291a3857a1f405ca7ab425aaae4e7`.
- [build-the-composition-pillar](../../../root/reviews/round-1/build-the-composition-pillar.md): reviewer 30/100; Rehome. Current memory excludes plugin runtimes; reconcile extension requirements with cartridge runtime rather than rebuild the removed subsystem inside memory.
  Original SHA-256: `b192565dabc9b4d4fa896967bfd89c5b7509b2f7beba8f9ae47f338b88d39de1`.
- [the-extension-crate](../../../root/reviews/round-1/the-extension-crate.md): reviewer 25/100; Rehome. The target crate is absent and plugin runtimes are explicitly excluded; use runtime composition or retire this superseded proposal after preserving evidence.
  Original SHA-256: `6dca0f3d93f308243cc91f77af709b67af7109894f259ada298bf9ebed86feee`.

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
