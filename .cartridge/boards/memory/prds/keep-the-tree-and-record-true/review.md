# keep-the-tree-and-record-true — review

Canonical PRD: [@memory/keep-the-tree-and-record-true](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [keep-the-tree-and-record-true](../../../root/reviews/round-1/keep-the-tree-and-record-true.md): reviewer 65/100; Reclassify. Keep as a maintenance index, not a finishable work item: its text says never done while its Check requires every child done.
  Original SHA-256: `0b997373bc55d7cadfce5aab697149748c3bb3686ead153f1ff24a1dccd16cd0`.

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
Reconciliation verdict: **REBASE — the historical source was a never-done standing maintenance terminal (round-1 65/100) whose subwork list no longer exists; the small-PRD rule (review-plan.md) retires such terminals. Round-2 text was a generic snapshot with no integration gate. Rebased as a finite parent: counts, spilled-store ranking and convergence.**

Presented revision: `prd.md` SHA-256 `1ef4189f56609624e1cfdcd3420803bda30e55493f26ee3ae3222381ff13a7de`. Rebased in this round (prior text `bfff25489789ddbbba333934d0de6bf95b0220f0062c3de7d531b3d3e3acb2fb`).
Source inspected: memory.ctg `c25af4d` (main), root `24aa2be`, prd.ctg `077e57a2` plus working tree.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | Coherent theme (reported numbers are true). -3: bucket still groups a decision (004) with two fixes. |
| Ownership and reuse | 19 | Memory-owned leaves only. -1. |
| Dependencies and implementable slices | 20 | Three needs resolve; acyclic; no overlap now that memory-integration-assessment is superseded. |
| Observable acceptance and baseline evidence | 18 | Gate: `just all` plus CLI/RPC count equality and zero dangling reasons on a named fixture. -2: fixture is created by a child. |
| Failure, recovery and compatibility | 16 | Failure keeps parent open. -4: no statement of what happens if 004 decides 'neither' (still closes; implied, not stated). |
| Reviewer total | 90/100 | |

Agent score: **90/100 — PASS**.
Findings: Standing-terminal semantics removed; finite outcome and integration gate added.
Blocking findings: none.
Validation: Existence checks only: cited source/test/doc paths exist (`ls`), `needs` targets and local links resolve (script over frontmatter and markdown links), memory.ctg `just --list` shows `check`, `test`, `e2e`, `all`, `eval-mature`, `eval-replay`, `test-reload`. Leaf body word count checked. No product gates were run.
Rounds used / remaining: 3 / 2.
Next: Children proceed independently; gate at the combined revision.
