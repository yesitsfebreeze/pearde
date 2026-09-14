# Memory improvement plan — review

Canonical PRD: [@memory/improve-memory-programme](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-memory-programme](../../../root/reviews/round-1/improve-memory-programme.md): reviewer 91/100; Keep. Fits current memory database ownership and targets measured access failures, readiness and provenance.
  Original SHA-256: `511f427882894fe9824a7b060916f456a85bea419426185d41c7fdd50205ed92`.

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

Reviewer: agent (independent reviewer, plan refresh pass). No user score was supplied or invented.
Reconciliation verdict: **CURRENT — the three children exist: `improve-memory-owner-access` and `improve-memory-readiness` are `state: done` (commit `a124fd3`), `improve-memory-provenance` is `specced` with a passed round 3. Nothing in the 2026-09-14 direction changes this rollup's targets.**

Presented revision: `prd.md` SHA-256 `803c9322c63bb25c710bd1f269e033e7ddae9dcec1a657c78d41b55aa3875bb7`. Unrevised round-2 text.
Source inspected: memory.ctg `c25af4d` (main), root `24aa2be`, prd.ctg `077e57a2` plus working tree.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Groups three owner outcomes; -2 no current status of children stated. |
| Ownership and reuse | 18 | -2: frontmatter key is malformed (`capability-capability-owner`), so the owner is not machine-readable. |
| Dependencies and implementable slices | 20 | All three needs resolve; acyclic. |
| Observable acceptance and baseline evidence | 17 | -3: rollup has no integration gate or command; 'record tested mitigations' is not observable. |
| Failure, recovery and compatibility | 16 | -4: no failure or recovery statement for a failed integration. |
| Reviewer total | 89/100 | |

Agent score: **89/100 — FAIL**.
Findings: Missing integration gate and failure rule; malformed owner key.
Blocking findings: none.
Validation: Existence checks only: cited source/test/doc paths exist (`ls`), `needs` targets and local links resolve (script over frontmatter and markdown links), memory.ctg `just --list` shows `check`, `test`, `e2e`, `all`, `eval-mature`, `eval-replay`, `test-reload`. Leaf body word count checked. No product gates were run.
Rounds used / remaining: 3 / 2.
Next: Revise within scope (round 4).

## Round 4 — 2026-09-14

Reviewer: agent (independent reviewer, plan refresh pass). No user score was supplied or invented.
Reconciliation verdict: **CURRENT (revised) — same children and states as round 3.**

Presented revision: `prd.md` SHA-256 `61c7dd4a4ca71fb86a4e75cd25c43bfa7671f2c0a3ad4da8dfeb098d2e4dd9e8`. Revised in this round (round-3 text `803c9322c63bb25c710bd1f269e033e7ddae9dcec1a657c78d41b55aa3875bb7`).
Source inspected: memory.ctg `c25af4d` (main), root `24aa2be`, prd.ctg `077e57a2` plus working tree.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | States which children are done and which remains. -1: parent adds no user value beyond its leaves by design. |
| Ownership and reuse | 20 | Owner key fixed; no new scope. |
| Dependencies and implementable slices | 20 | Needs resolve; only provenance remains ready to claim. |
| Observable acceptance and baseline evidence | 17 | Integration gate named with command and cwd. -3: 'as their leaves specify' defers the concrete status fields to the leaves. |
| Failure, recovery and compatibility | 16 | Failed gate reopens only its leaf, no production repair. -4: gate status fields not pinned. |
| Reviewer total | 92/100 | |

Agent score: **92/100 — PASS**.
Findings: Round-3 findings resolved.
Blocking findings: none.
Validation: Existence checks only: cited source/test/doc paths exist (`ls`), `needs` targets and local links resolve (script over frontmatter and markdown links), memory.ctg `just --list` shows `check`, `test`, `e2e`, `all`, `eval-mature`, `eval-replay`, `test-reload`. Leaf body word count checked. No product gates were run.
Rounds used / remaining: 4 / 1.
Next: Implement `improve-memory-provenance`; then run the integration gate.
