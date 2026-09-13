# Use consistent stale-write checks for filesystem mutations — review

Canonical PRD: [@fs/improve-fs-revision-guards](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-fs-revision-guards](../../../root/reviews/round-1/improve-fs-revision-guards.md): reviewer 88/100; Resequence. Basic stale-write protection should not wait on client mapping and provenance rollout; add a concurrent check-to-write race fixture, not only stale sequential input.
  Original SHA-256: `7790a477496bc505a7732759c2d7360bbf473921ed3c8eb047c6c6829f96c265`.

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

## Round 3 — 2026-09-13

Reviewer: `/root` self-review; no delegation authorized. Inputs are bound in
[review-round-3-inputs.json](review-round-3-inputs.json).

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | Baseline reproduces actual loss of newer bytes, with a success response. |
| Ownership and reuse | 19 | One fs helper reuses observations, locks and touch; independent overlay owner has compatibility proof only. |
| Dependencies and slices | 20 | No provenance dependency; four owner-local paths, direct checkout after review. |
| Acceptance and baseline | 19 | Deterministic boundary hook, two-session contention, cancellation and mode assertions. |
| Failure and compatibility | 18 | Atomic publication, explicit post-commit partial success; final external check/rename race is disclosed, not falsely claimed as CAS. |

Agent score: **95/100 — PASS**. No blocking findings. Keep cross-process CAS
outside the claim; the controlled external edit occurs during preparation and
is checked at publication. Baseline failed as intended; implementation gates
remain pending. Rounds used: 3/5.

## Round 4 — Verification entry-point correction

Self-review `/root`: **95/100 — PASS** (19/19/20/19/18). Collection's
explicit justfile invocation changed the memo owner directory and failed before
running tests. The spec now changes to the runtime and uses the already-passing
public `just test fs` entry point. Product scope and implementation are unchanged.
No blockers; inputs in review-round-4-inputs.json. Rounds used: 4/5.
