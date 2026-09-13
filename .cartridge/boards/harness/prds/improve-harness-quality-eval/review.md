# Measure multi-round context quality with real task outcomes — review

Canonical PRD: [@harness/improve-harness-quality-eval](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-harness-quality-eval](../../../root/reviews/round-1/improve-harness-quality-eval.md): reviewer 91/100; Keep. Good adversarial and three-round replay coverage; share the long-horizon corpus and keep live-model results distinct from offline gates.
  Original SHA-256: `16da9d3db4fa4bbf2679b61865bd044d685d06b7b0bebe615e20490dce7ab4bc`.
- [long-horizon-recall-benchmark](../../../root/reviews/round-1/long-horizon-recall-benchmark.md): reviewer 82/100; Merge. Merge corpus ownership with harness quality evaluation; freeze dataset/license, per-ability metrics, abstention scoring and model/fixture distinction before runs.
  Original SHA-256: `57458fd6c5de067e9eda2ff13e286cf0138607079be1c99f05f1fda7828a0c6c`.

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
