# Memory counts use consistent public terminology — review

Canonical PRD: [@memory/memory-002](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [MEMORY-002](../../../root/reviews/round-1/MEMORY-002.md): reviewer 92/100; Keep. Keep the bounded terminology reconciliation; preserve current APIs/store layout and owner-reserved worktree, and prove CLI/RPC counts and legacy decoding.
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
Reconciliation verdict: **REBASE — the reserved owner `codex/memory-terminology`, worktree `memory-memory-terminology` and commits `0d3ce338`/`15862820` named by `.cartridge/docs/WORK_ITEMS.md` do not exist in memory.ctg (`git branch -a`, `git worktree list`, object lookup) and no `~/dev/memory-worktree-archives` exists. Actual count sites: `health_stats` (`src/rpc/src/server.rs`) keys `entities/reasons/memories` vs CLI `thoughts:` (`src/commands/src/commands_health.rs`), hub `loaded/cold` (`src/commands/src/commands_hub.rs`). The old starting files did not contain these.**

Presented revision: `prd.md` SHA-256 `0acb93f8baeaa12079d34e67da196ba1e2e40d5b78e36b86f1009c528f6b14b2`. Rebased in this round (prior text `3a0dc03451e58cdf65492606267170f39d0538f3e2f22d34ecb69692cabb3e23`).
Source inspected: memory.ctg `c25af4d` (main), root `24aa2be`, prd.ctg `077e57a2` plus working tree.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Real vocabulary split confirmed. -2: lower priority per WORK_ITEMS. |
| Ownership and reuse | 19 | Labels/docs only; wire keys and layout frozen. -1: stored (hot+cold) count may need new computation. |
| Dependencies and implementable slices | 19 | No needs. -1: lapsed reservation must be confirmed before claiming. |
| Observable acceptance and baseline evidence | 18 | Equality test on one snapshot, half-cold distinction, legacy tests. -2: no baseline captured yet. |
| Failure, recovery and compatibility | 18 | No data change; rollback trivial. -2: CLI label changes may break scripts grepping `thoughts:`; not addressed. |
| Reviewer total | 92/100 | |

Agent score: **92/100 — PASS**.
Findings: (1) Stale owner/worktree claim replaced by a verify-before-claim step (prose reference only; no frontmatter claim changed). (2) Starting files corrected. (3) Acceptance tied to existing e2e health test.
Blocking findings: none.
Validation: Existence checks only: cited source/test/doc paths exist (`ls`), `needs` targets and local links resolve (script over frontmatter and markdown links), memory.ctg `just --list` shows `check`, `test`, `e2e`, `all`, `eval-mature`, `eval-replay`, `test-reload`. Leaf body word count checked. No product gates were run.
Rounds used / remaining: 3 / 2.
Next: Confirm reservation lapsed; probe a half-cold fixture.
