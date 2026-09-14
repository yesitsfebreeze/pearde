# Return actionable memory failures and enforce the tool schema — review

Canonical PRD: [@memory/improve-memory-tool-errors](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-memory-tool-errors](../../../root/reviews/round-1/improve-memory-tool-errors.md): reviewer 86/100; Rehome. Preserve the useful committed/refused/unknown taxonomy in the surviving adapter and common result schema, with one translation boundary.
  Original SHA-256: `9c5e29d3b58783439d35607504ad626d8e1be8cd5e4ea186103b465425727545`.

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
Reconciliation verdict: **REBASE — 'across wrapper retirement' and 'MCP/proxy consumers' referred to the dropped memory-tool wrapper (root `9e4cde8`). Current tool: `tool_failure` prose in `src/cartridge.rs`; `memory(...).await?` lets engine/transport errors escape as provider errors rather than tool results (new finding).**

Presented revision: `prd.md` SHA-256 `ac07b86a75ec3c1b691628b81ebfea34642d8a50de8158bf9f1e6839debfd48a`. Rebased in this round (prior text `ea274c6e1ea639e4d63e45212a1374e36faffa7597c3b35bc47d454c33477602`).
Source inspected: memory.ctg `c25af4d` (main), root `24aa2be`, prd.ctg `077e57a2` plus working tree.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Agents currently cannot distinguish contention, dead embedder and refused ingest. -1. |
| Ownership and reuse | 19 | One translation point in the memory adapter; wire unchanged. -1: codes land in content JSON, consumers parse it. |
| Dependencies and implementable slices | 19 | Needs adapter-core (appears delivered); ordering with get stated. -1. |
| Observable acceptance and baseline evidence | 18 | Codes, triggers and fixtures named (embed stub, held writer, disconnected owner). -2: `ingest_unknown` trigger (worker failure after dispatch) is hard to inject; probe must confirm. |
| Failure, recovery and compatibility | 18 | No retries, no stored-state change. -2: host behaviour for provider-level errors versus tool results not verified. |
| Reviewer total | 93/100 | |

Agent score: **93/100 — PASS**.
Findings: (1) Wrapper framing removed. (2) Named the code set and the `?` escape path. (3) Owner key typo fixed.
Blocking findings: none.
Validation: Existence checks only: cited source/test/doc paths exist (`ls`), `needs` targets and local links resolve (script over frontmatter and markdown links), memory.ctg `just --list` shows `check`, `test`, `e2e`, `all`, `eval-mature`, `eval-replay`, `test-reload`. Leaf body word count checked. No product gates were run.
Rounds used / remaining: 3 / 2.
Next: Land after get; reproduce each failure first.
