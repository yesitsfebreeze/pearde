# the-agent-surface-is-usable — review

Canonical PRD: [@memory/the-agent-surface-is-usable](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [the-agent-surface-is-usable](../../../root/reviews/round-1/the-agent-surface-is-usable.md): reviewer 40/100; Reconcile. Do not restore the old memory MCP/answer/router surface; retain current ingest/query/get integrity checks and rehome client/proxy acceptance.
  Original SHA-256: `5d994ec952663a508b5ccba80af991ed316bbdec5df42a24ee384a5eadf848de`.

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
Reconciliation verdict: **REBASE — the 22-tool `memory mcp` surface this parent measured is gone; MCP hosting left memory (WORK_ITEMS.md), memory ported to transport (`9cc0f0b`), and agents reach `tool.memory` served by `src/cartridge.rs` and relayed by consumers without sibling knowledge (decision `a-cartridge-brings-its-own-surface`). Children resolve; readiness is done; adapter-core appears delivered.**

Presented revision: `prd.md` SHA-256 `65e697b2d2b4cfb0bdae2afbae12d8359d82dd37342d885e56dd0d096c26a17b`. Rebased in this round (prior text `8570336ca48fb507181270a52d9c312b84d5ae5348e00ede4e3f3cb656144083`).
Source inspected: memory.ctg `c25af4d` (main), root `24aa2be`, prd.ctg `077e57a2` plus working tree.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Agent-facing memory usability, current surface. -1. |
| Ownership and reuse | 19 | Memory-owned; no MCP/proxy acceptance pulled back in. -1. |
| Dependencies and implementable slices | 19 | Four needs resolve. -1: adapter-core status pending verification. |
| Observable acceptance and baseline evidence | 18 | Integration test sequence, size bound, codes; live probe separate. -2: test case to be created. |
| Failure, recovery and compatibility | 17 | No production repair on failed probe. -3: no rollback statement at parent level. |
| Reviewer total | 92/100 | |

Agent score: **92/100 — PASS**.
Findings: Replaced historical MCP framing; absorbed the live-probe requirement from the superseded memory-integration-assessment.
Blocking findings: none.
Validation: Existence checks only: cited source/test/doc paths exist (`ls`), `needs` targets and local links resolve (script over frontmatter and markdown links), memory.ctg `just --list` shows `check`, `test`, `e2e`, `all`, `eval-mature`, `eval-replay`, `test-reload`. Leaf body word count checked. No product gates were run.
Rounds used / remaining: 3 / 2.
Next: Leaves get and errors proceed; gate when done.
