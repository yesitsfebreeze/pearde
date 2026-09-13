# Require compatible model capabilities before fallback — review

Canonical PRD: [@router/improve-router-capability-routing](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-router-capability-routing](../../../root/reviews/round-1/improve-router-capability-routing.md): reviewer 92/100; Keep. Unknown mandatory capability fails explicitly and fallback preserves requirements; verify current catalog fields first.
  Original SHA-256: `e86b5d2ac113347ab891fcb9cc59e0bc4405179e91dbe3360393f1f029d96ab7`.

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

## Round 3 — Uniform admission and per-hop evidence

Reviewer `/root` self-review. Inputs: review-round-3-inputs.json.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | Baseline confirms all three bypasses; prevents incompatible fallback. |
| Ownership and reuse | 19 | Existing routing/translation path owns admission; one new pure gate. |
| Dependencies and slices | 19 | No external provider or policy ownership change; context estimates explicitly limited. |
| Acceptance and baseline | 19 | Source-identical failing probe plus actual loopback failover and zero-call exclusions. |
| Failure and compatibility | 19 | Unknown/expired evidence fails; configured declarations remain distinguishable; no automatic replay added. |

**95/100 — PASS**. No blockers. Stricter admission intentionally refuses formerly
unchecked pinned/local routes. A declared capability is not labelled empirical
verification; context estimates remain heuristic. Common conversion is retained,
and unsupported advanced conversion fails rather than silently dropping intent.
Rounds used: 3/5. Product gates pending.

## Implementation proof

The accepted admission contract passes 23 router tests and the public check, with 21 proxy and 15 MCP compatibility tests. Source hashes and complete logs are in verification.json. Additional failure checks show that existing health adaptations cannot strip required fields, and re-reading a subscription cache cannot establish a new live observation. These implement the accepted preservation/evidence requirements without expanding into the separate health/explanation/recovery PRDs.
