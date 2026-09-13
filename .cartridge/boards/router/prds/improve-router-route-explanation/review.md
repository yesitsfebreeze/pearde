# Explain why a provider was selected — review

Canonical PRD: [@router/improve-router-route-explanation](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-router-route-explanation](../../../root/reviews/round-1/improve-router-route-explanation.md): reviewer 93/100; Keep. Chosen route and actual fallback attribution are testable; bound traces and redact credentials.
  Original SHA-256: `42e4235505ad8caf8c754fc8e22128a1dcfc83dee65592151b5594d6a23ff015`.

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

## Round 3 — Actual decisions and immutable revision attribution

Reviewer `/root` self-review. Inputs: review-round-3-inputs.json.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | Actual fallback currently lacks an attributable decision receipt. |
| Ownership and reuse | 20 | Reuses completed capability admission and current attempt loop. |
| Dependencies and slices | 19 | Router owns trace; existing sha2 dependency resolution and one lockfile sync. |
| Acceptance and baseline | 19 | Real loopback health/fallback/zero-call checks, revision rollback and redaction. |
| Failure and compatibility | 19 | Opt-in bounded metadata; cancellation and stream-start distinguish processing from delivery. |

**96/100 — PASS**. No blockers. Preflight is an observation, not a promise of the
next route. SHA-256 identifies sanitized selection semantics, not authorization or
provider truth. Rounds used: 3/5. Product gates pending.
