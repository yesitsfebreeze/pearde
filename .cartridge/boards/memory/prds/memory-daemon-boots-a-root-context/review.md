# memory-daemon-boots-a-root-context — review

Canonical PRD: [@memory/memory-daemon-boots-a-root-context](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [memory-daemon-boots-a-root-context](../../../root/reviews/round-1/memory-daemon-boots-a-root-context.md): reviewer 25/100; Rehome. Do not add the removed extension/MCP/model stack back to memory; retain only demonstrated daemon startup/shutdown gaps under current engine APIs.
  Original SHA-256: `55bd769b3b4154bf2cb4d7976d29a8326c249e7037e7385486253354b6c68be8`.
- [memory-boots-as-a-plugin-tree](../../../root/reviews/round-1/memory-boots-as-a-plugin-tree.md): reviewer 25/100; Rehome. Contradicts current repository scope and absent extension infrastructure; preserve memory daemon ownership while placing general composition in cartridge.
  Original SHA-256: `2ba98937bc64f94ef1879a193a88c4e3057e2172b8885327e85e669d5754614d`.

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
Reconciliation verdict: **REBASE — memory now runs under two lifecycles: CLI daemon (`run_server`, `src/commands/src/commands_serve.rs`) and the transport cartridge ported 2026-09-14 (`9cc0f0b`; `on_dispose` in `src/cartridge.rs`). Plugin-tree/root-Context design (memory decision `memory-is-a-plugin-tree`) conflicts with `.cartridge/docs/AGENTS.md` scope and stays dropped. Demonstrated gaps: non-model mutations admitted during drain (`src/rpc/src/server.rs` MODEL_DEPENDENT gate), eviction before boot validation (`evict_predecessor`), `ready` lacks store state.**

Presented revision: `prd.md` SHA-256 `5520344fa06c02d6251f3f7bd384376de710ca874bbfb4aa15a25cdcc1f6495f`. Rebased in this round (prior text `31202a1f7eb4e949a8b1d34831b4dcc09dc0bc719ff67fb6ac9e2be0ba5b8725`).
Source inspected: memory.ctg `c25af4d` (main), root `24aa2be`, prd.ctg `077e57a2` plus working tree.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Durability/ownership gaps confirmed in source. -2: impact of late mutations during save not measured. |
| Ownership and reuse | 19 | Existing latch, writer lock and e2e harness reused. -1. |
| Dependencies and implementable slices | 17 | Three gaps in one leaf. -3: they share files and a lifecycle but could land separately; stated per-gap rollback mitigates. |
| Observable acceptance and baseline evidence | 18 | Named tests per check. -2: 'store-directory validation' before eviction is limited because the lock cannot be taken first; probe must define it. |
| Failure, recovery and compatibility | 18 | Writer lock and guarded flush stay the boundary. -2: cartridge-mode ordering (drain before latch) change not fully specified. |
| Reviewer total | 90/100 | |

Agent score: **90/100 — PASS**.
Findings: Obsolete plugin framing replaced with three source-observed gaps and current file paths.
Blocking findings: none.
Validation: Existence checks only: cited source/test/doc paths exist (`ls`), `needs` targets and local links resolve (script over frontmatter and markdown links), memory.ctg `just --list` shows `check`, `test`, `e2e`, `all`, `eval-mature`, `eval-replay`, `test-reload`. Leaf body word count checked. No product gates were run.
Rounds used / remaining: 3 / 2.
Next: Reproduce each gap in e2e; land before memory-signals-become-events.
