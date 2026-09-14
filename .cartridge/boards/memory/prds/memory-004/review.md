# Mixed and cold recall preserve per-ability ranking — review

Canonical PRD: [@memory/memory-004](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [MEMORY-004](../../../root/reviews/round-1/MEMORY-004.md): reviewer 93/100; Keep. Keep the measured mixed/cold ranking question; unify parked-memory evidence, predeclare per-ability regression gates and retain the explicit no-default-switch boundary.
  Original SHA-256: `c61c9070c7a2a1b5a8a81b2c8c919efb4769cd62ddf6ca8d70fab8cb72b42b97`.

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

## Round 3 — 2026-09-14

Reviewer: agent (independent reviewer, plan refresh pass). No user score was supplied or invented.
Reconciliation verdict: **REBASE — fixtures and per-layout/per-category reporting already exist (`.cartridge/tests/integration/bench/mature.json`, `replay.json`, `bench/src/replay.rs`, `RESULTS.md` linked_evidence 0.967/0.532/0.511), so round-2 acceptance 1 was largely delivered; the decision itself is absent (WORK_ITEMS.md MEMORY-004 open). Old starting files were wrong. The partial-cold-status check moved to parked-memory-remains-recallable to remove overlap.**

Presented revision: `prd.md` SHA-256 `5f15705e724fb64ca1c3e4d35c30b85ecb8becb163c4513447bfe6eda98faf47`. Rebased in this round (prior text `787bc978ec7f65fc43863a9b509744aa22c951542c9f7135dc200cfca6a79edd`).
Source inspected: memory.ctg `c25af4d` (main), root `24aa2be`, prd.ctg `077e57a2` plus working tree.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Measured 0.53 vs 0.92 deficit; bounded to a decision. -1. |
| Ownership and reuse | 20 | Reuses existing harness, fixtures and recipes; no default switch. |
| Dependencies and implementable slices | 18 | No needs. -2: evals' offline status unconfirmed; stop condition given. |
| Observable acceptance and baseline evidence | 18 | Pre-declared thresholds, three layouts, recorded decision. -2: 'stated noise' not quantified in RESULTS.md yet. |
| Failure, recovery and compatibility | 17 | Candidates behind an off knob; rejected code not merged. -3: no bound on candidate count/effort. |
| Reviewer total | 92/100 | |

Agent score: **92/100 — PASS**.
Findings: Delivered parts recorded; scope narrowed to the decision; overlap with parked-memory removed.
Blocking findings: none.
Validation: Existence checks only: cited source/test/doc paths exist (`ls`), `needs` targets and local links resolve (script over frontmatter and markdown links), memory.ctg `just --list` shows `check`, `test`, `e2e`, `all`, `eval-mature`, `eval-replay`, `test-reload`. Leaf body word count checked. No product gates were run.
Rounds used / remaining: 3 / 2.
Next: Rerun baseline evals and write thresholds before candidates.
