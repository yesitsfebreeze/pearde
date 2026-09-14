# Correct or forget one identified fact through the tool boundary — review

Canonical PRD: [@memory/improve-memory-tool-correct](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-memory-tool-correct](../../../root/reviews/round-1/improve-memory-tool-correct.md): reviewer 84/100; Rehome. Choose the surviving memory adapter as owner before extending a wrapper scheduled for retirement; split atomic correction from forget and specify tombstone/history semantics.
  Original SHA-256: `008a429a749e939f284cb1616c9beee8647becf393921e1d6e68fe425b5566b2`.

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
Reconciliation verdict: **REBASE — the wrapper this plan was migrating from is gone (root `9e4cde8` dropped memory-tool; `src/cartridge.rs` now serves `tool.memory` directly). Removal semantics are decided: memory decision `does-a-removal-need-a-tombstone` (hard removal, no tombstones). Tool descriptors declare `reads` (decision `a-cartridge-brings-its-own-surface`). Service `forget` (`tool_forget`, `ForgetRefusal`) and supersede chains exist; no correct/supersede-by-id op exists.**

Presented revision: `prd.md` SHA-256 `0fc45d8b44eced1dd1af5eb480cbb77ca5e2d61778f5ba6ca19a6bd8fa30e112`. Rebased in this round (prior text `4d2aac1c0f94e954f7ba2d0b4ffd5a8553ede7b84cd89094a46130331efc702a`).
Source inspected: memory.ctg `c25af4d` (main), root `24aa2be`, prd.ctg `077e57a2` plus working tree.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | Lets an agent fix a wrong fact. -3: exposing mutations to the model has limited demonstrated demand; kept opt-in (`tool_writes` default false). |
| Ownership and reuse | 19 | Reuses `forget_entity` refusal policy and Supersedes reasons; no tombstones. -1: supersede-by-id path unprobed. |
| Dependencies and implementable slices | 17 | Hard need on get added for readback. -3: two operations in one leaf (forget exposure and new correct op); mitigated by separate specs/commits. |
| Observable acceptance and baseline evidence | 19 | Four checks incl. no-byte-change refusals, opt-in gate, unknown-outcome. -1 baseline to capture. |
| Failure, recovery and compatibility | 19 | Never repeats a mutation; rollback by setting off. -1: history retention of superseded rows depends on existing GC policy. |
| Reviewer total | 91/100 | |

Agent score: **91/100 — PASS**.
Findings: (1) Wrapper-migration framing removed. (2) Tombstone ambiguity resolved by the recorded decision. (3) Opt-in setting and `reads` exclusion make write exposure explicit. (4) Added `@memory/improve-memory-tool-get` as a hard need; graph stays acyclic. (5) Owner key typo fixed. Body ~308 words, slightly over the 300 aim, under the 400 split limit.
Blocking findings: none.
Validation: Existence checks only: cited source/test/doc paths exist (`ls`), `needs` targets and local links resolve (script over frontmatter and markdown links), memory.ctg `just --list` shows `check`, `test`, `e2e`, `all`, `eval-mature`, `eval-replay`, `test-reload`. Leaf body word count checked. No product gates were run.
Rounds used / remaining: 3 / 2.
Next: After get lands, probe the supersede path, then spec forget exposure first.
