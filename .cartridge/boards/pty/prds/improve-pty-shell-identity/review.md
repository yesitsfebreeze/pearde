# Return explicit shell and working-directory identity — review

Canonical PRD: [@pty/improve-pty-shell-identity](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-pty-shell-identity](../../../root/reviews/round-1/improve-pty-shell-identity.md): reviewer 93/100; Keep. Separates configured executable, observed dialect and unsupported integration; preserves literal input and PTY lifetime.
  Original SHA-256: `c281e1c88fca68fd1e846c18931d767ec969ff01ee4e3fe3fc3853f8d1877bc2`.

Historical dimension scores were not recorded. The original user-rating field was pending; the current workflow delegates scoring to the agent. Splitting does not reset the allowance.

## Round 2 — 2026-09-13

Revision: the working-tree PRD and the exact input digests in [review-inputs.json](review-inputs.json).
Change: small owner-local contract; broad parents point to leaves, and canonical aliases share one implementation scope.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | The PRD states its bounded outcome; inherited broader requirements are retained in source history and linked children. |
| Ownership and reuse | 19 | Named cartridge and existing starting files; historical duplicate IDs are mapped to this canonical scope. |
| Dependencies and slices | 19 | Qualified hard dependencies resolve; the complete parent/child graph is acyclic. |
| Acceptance and baseline | 18 | Unchecked behavioral acceptance and a real repository gate; fixture details and measured baselines must be captured before specs. |
| Failure and compatibility | 19 | Negative outcomes and a recovery boundary are retained; implementation must supply the specified failure proof. |

Agent score: **94/100 — PASS**.
Finding: One bounded outcome with explicit positive/negative checks. Fixture-specific specs and baseline measurements remain analysis work; proposed tests are not reported as passed.
Blocking review findings: none; implementation prerequisites remain in the PRD.
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Independent round 3 — PASS 95/100

Reviewer /root; dimensions19/20/18/19/19. Spec 560b4619ac03f28c6b9342c24184293d5dbd4045fb031996c3c1210487ad8d7d and actual baselinecacd7e13. No blocking findings. Configured identity and forgeable terminal evidence stay separate, existing OSC/bootstrap and shared Shell are reused, additive observations preserve tool strings/frame cursors, and real disposable Host/shell fixtures prove lifecycle continuity. Seven-path scope excludes wait/input-lease/context changes. Exact input binding and deductions: independent-round-3-review.json.

## Implementation review and wording clarification

Root independently reviewed the seven source paths at e8e6b319b03dcc9e1dea66b4fd3a0f6b83ab2d47 and the real-shell/UI continuity proof. Public30tests/check passed. Exact source digests are in implementation-review.json. Cwd wording now explicitly says latest observation if valid, null otherwise; [before/after binding](cwd-observation-clarification.json) preserves the original acceptance, executable gates and round3 review. Collection reruns those gates.
