# degrade-corrects-the-retrieval-path-it-names — review

Canonical PRD: [@memory/degrade-corrects-the-retrieval-path-it-names](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [degrade-corrects-the-retrieval-path-it-names](../../../root/reviews/round-1/degrade-corrects-the-retrieval-path-it-names.md): reviewer 82/100; Revise. Good query-versus-fact identity diagnosis; add explicit expired/cross-store/no-provenance fixtures, bounded mutation acceptance and current API paths.
  Original SHA-256: `af2bdbc8350ba6e8b42f5397965665dc6b12596a31653da336586a9143abd850`.

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
Reconciliation verdict: **REBASE — outcome still wanted; the round-2 text pointed at `src/cartridge.rs`/`src/main.rs`, which do not contain degrade. Current code: `tool_degrade` (`src/rpc/src/server.rs`, `DegradeArgs{query_id}`), `degrade_entity_reasons` (`src/graph/src/graph_ops.rs`) decays every reason of a thought; `cmd_degrade` (`src/commands/src/commands_graph_ops.rs`). No query provenance is retained anywhere. Memory decision `does-a-removal-need-a-tombstone` rules out tombstone state.**

Presented revision: `prd.md` SHA-256 `9a98d3f57b69be7ac6bcd0afb5400c93cc51fe8d802f1ea4ec6f8324dcc50d9f`. Rebased in this round (prior text `32467682b46cabfcd9b205fdf4c2b46d0187843fb3c6afa11f374df68be77c3d`).
Source inspected: memory.ctg `c25af4d` (main), root `24aa2be`, prd.ctg `077e57a2` plus working tree.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Real defect confirmed in source (thought-wide decay under a misleading `query_id`). -2: feedback quality benefit is argued, not measured. |
| Ownership and reuse | 19 | Memory-owned; reuses reason `score_lamport` and graph `replica_id` instead of a new provenance store. -1: explain output shape not yet confirmed. |
| Dependencies and implementable slices | 18 | Single leaf, no needs. -2: whether explain already returns reason IDs is an unprobed first step that may add work. |
| Observable acceptance and baseline evidence | 18 | Three observable checks incl. untouched sibling reasons and stale replay. -2: fixture/baseline numbers to be captured at probe. |
| Failure, recovery and compatibility | 19 | Refusals write nothing; legacy `query_id` behaviour preserved and documented. -1: concurrent degrade of the same reason relies on lamport check only. |
| Reviewer total | 92/100 | |

Agent score: **92/100 — PASS**.
Findings: (1) Stale starting files replaced with the actual degrade path. (2) 'Retained provenance' had no implementation basis; replaced by a stateless handle validated against live reason lamports, with a stop-and-probe on explain output. (3) Compatibility of the CLI `memory degrade <id>` made explicit.
Blocking findings: none.
Validation: Existence checks only: cited source/test/doc paths exist (`ls`), `needs` targets and local links resolve (script over frontmatter and markdown links), memory.ctg `just --list` shows `check`, `test`, `e2e`, `all`, `eval-mature`, `eval-replay`, `test-reload`. Leaf body word count checked. No product gates were run.
Rounds used / remaining: 3 / 2.
Next: Probe explain output for reason IDs, then spec the handle.
