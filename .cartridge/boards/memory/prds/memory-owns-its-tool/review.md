# Memory owns its service and tool interface — review

Canonical PRD: [@memory/memory-owns-its-tool](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [memory-owns-its-tool](../../../root/reviews/round-1/memory-owns-its-tool.md): reviewer 88/100; Revise. Reconcile the three memory-tool enhancement leaves with adapter retirement and specify the mixed-version interval and exact profile exposure snapshots.
  Original SHA-256: `4725b397890c58624ff423048e24c77dc8863973320aae8be1dc272549d0563a`.

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
Reconciliation verdict: **DELIVERED — memory serves its service and agent tool directly: `src/cartridge.rs` provides `memory`, `tool.memory` and `context.memory` (comment: 'the former separate memory-tool cartridge ... lives here'; `cartridge.json` `provide`). The wrapper was removed (root `9e4cde8` 'drop memory-tool'; no `memory-tool.ctg`, no remaining references outside prd.ctg). One-writer and tool reach are tested in `.cartridge/tests/integration/cartridge.rs` (`memory_persists_and_replacement_does_not_open_a_second_writer`, which calls `tool.memory`). Children memory-adapter-core, memory-consumer-parity and memory-wrapper-retirement appear delivered by the same evidence but are outside this reviewer's assignment.**

Presented revision: `prd.md` SHA-256 `f9ce41471f113536e01ead0a00b4c65ba75c0764d0facd229508c4fae8055042`. Frontmatter only changed (review-round, review-status, owner key typo `capability-capability-owner` → `capability-owner`, value unchanged); body unchanged.
Source inspected: memory.ctg `c25af4d` (main), root `24aa2be`, prd.ctg `077e57a2` plus working tree.

Agent score: not scored (delivered-pending-verification).
Findings: Recommend verifying the three children against the cited evidence (run `just test` in memory.ctg) before marking done. `state:` left untouched.
Blocking findings: none.
Validation: Existence checks only: cited source/test/doc paths exist (`ls`), `needs` targets and local links resolve (script over frontmatter and markdown links), memory.ctg `just --list` shows `check`, `test`, `e2e`, `all`, `eval-mature`, `eval-replay`, `test-reload`. Leaf body word count checked. No product gates were run.
Rounds used / remaining: 3 / 2.
Next: Coordinator verification; no further plan revision.
