# Memory tool adapter improvement plan — review

Canonical PRD: [@memory/improve-memory-tool-programme](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-memory-tool-programme](../../../root/reviews/round-1/improve-memory-tool-programme.md): reviewer 82/100; Rehome. The owner is scheduled for retirement; reparent all three leaf contracts to memory and record compatibility migration before implementation.
  Original SHA-256: `da373db0814bb2f34676d46f86f831b6fb7e8318277c3de9c280832d7968f0b2`.

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
Reconciliation verdict: **REBASE — round-1 'owner is scheduled for retirement' is now history: memory-tool dropped (root `9e4cde8`), `tool.memory` served by memory (`src/cartridge.rs`). Children still open and rebased this round.**

Presented revision: `prd.md` SHA-256 `7a7fdd341d87059c43a66f587eba1be4375e51669dee3703046d77ddfecad797`. Rebased in this round (prior text `a9526e61666f0bd3cb4786eed20d921a48bfe11dfe1b0fdf614a0c0b990f74d8`).
Source inspected: memory.ctg `c25af4d` (main), root `24aa2be`, prd.ctg `077e57a2` plus working tree.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Index for three tool improvements; -2 parent-only value. |
| Ownership and reuse | 20 | Owner fixed; no implementation of its own. |
| Dependencies and implementable slices | 20 | Three needs resolve; order get → errors/correct stated in leaves. |
| Observable acceptance and baseline evidence | 18 | Integration gate with a concrete call sequence and command. -2: case does not yet exist and must be created. |
| Failure, recovery and compatibility | 17 | Limitations recorded, not silently closed. -3: no rollback statement at parent level (leaves carry it). |
| Reviewer total | 93/100 | |

Agent score: **93/100 — PASS**.
Findings: Wrapper framing removed; integration gate added; owner key fixed.
Blocking findings: none.
Validation: Existence checks only: cited source/test/doc paths exist (`ls`), `needs` targets and local links resolve (script over frontmatter and markdown links), memory.ctg `just --list` shows `check`, `test`, `e2e`, `all`, `eval-mature`, `eval-replay`, `test-reload`. Leaf body word count checked. No product gates were run.
Rounds used / remaining: 3 / 2.
Next: Leaves proceed; run the gate when all three land.
