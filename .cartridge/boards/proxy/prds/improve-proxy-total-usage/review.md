# Account for every internal model round consistently — review

Canonical PRD: [@proxy/improve-proxy-total-usage](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-proxy-total-usage](../../../root/reviews/round-1/improve-proxy-total-usage.md): reviewer 93/100; Keep. Three-round JSON/SSE equivalence and incomplete usage are concrete; preserve standard wire-field meanings.
  Original SHA-256: `2aad690b90361d0a090ff1cf9ea0bad0a3cab460fe2740357434d664328eb249`.

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

## Round 3 — native baseline and shared accounting boundary

Reviewer: Codex self-review. A source-identical disposable copy with an added
three-round probe returned only 20 input tokens for JSON on Chat, Anthropic and
Responses, versus the expected 60. Existing streaming separately sums successful
rounds and treats missing usage as zero; failure loses partial accounting.

Use one opt-in ledger and an additive canonical report so legacy native field
semantics remain intact. Request-owned state and a bounded completed-report ring
make cancellation observable without retaining bodies or inventing delivery.
Provider cumulative snapshots replace current-round counts; finalization occurs
once. Counter validation and checked sums distinguish unknown, zero and overflow.
Existing cancellation/lease/history/continuation fixtures are part of the gate.

Value/scope 19; ownership/reuse 19; dependencies/slices 19; acceptance/baseline 20;
failure/compatibility 19. **96/100 — PASS for the plan**, no blocking finding.
Native trusted usage lookup is bounded telemetry for lost connections, not a new
conversation store. Inputs bound in review-round-3-inputs.json. Three rounds used,
two remain; implementation and product checks are still pending.

## Implementation evidence

The accepted round-3 contract is implemented. Public proxy tests pass (21), proxy check passes, and GitFS (25) and policy (4) consumer tests pass. Verification records bind source file hashes and complete gate logs. An additional immediate-disconnection regression exposed a missing archived report; constructing the request guard before polling fixes it without dispatch. Acceptance checkmarks, corrected source navigation and this evidence update do not alter the reviewed behavior.
