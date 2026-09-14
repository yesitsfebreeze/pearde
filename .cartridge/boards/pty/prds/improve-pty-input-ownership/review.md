# Coordinate human and agent input on the shared terminal — review

Canonical PRD: [@pty/improve-pty-input-ownership](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-pty-input-ownership](../../../root/reviews/round-1/improve-pty-input-ownership.md): reviewer 88/100; Revise. Decide human preemption while a command or alternate-screen application is active; lease revocation alone does not make shell input safe for a new command.
  Original SHA-256: `cfac8706ae0c61f05fb0afb080020af017df3cce0f383d3db5f5aa91f93a8ab8`.

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

Reconciliation verdict: **REBASE** (partially delivered). Evidence: pty cacd7e1 "Support explicit user and agent control of the shared terminal" added `pty {op:"control"}`, takeback revocation with one Ctrl+C, and tests `shell_serializes_input_and_only_cancels_the_matching_invocation` and `handoff_blocks_agent_input_and_takeback_interrupts_without_closing_shell` in `pty.ctg/.cartridge/tests/integration/process.rs`; documented in `.cartridge/docs/README.md`; `src/tool.rs` `tool_gate` refuses concurrent input with a generic message (no owner); `src/main.rs` `run` admits on prompt phase, and `../improve-pty-command-wait/handoff-baseline-context.json` records the old prompt being treated as interrupt acknowledgment. Not DELIVERED: owner-bearing refusal and post-takeback readiness boundary are absent. Pre-revision text (SHA-256 `13376de73ba5c4ba9f05d15b74f57e759117e9ec0221beee6ac9787025631e90`) restated delivered behaviour as new work and named five missing paths. Blocking.

Revision reviewed: `prd.md` SHA-256 `29ac20db79dfda3b5472a6f28c7434e45609de64c64b535edae84e7dcf819bb8` (working tree). Changes: delivered baseline cited; acceptance narrowed to owner-bearing refusal, new-prompt-after-interrupt boundary, no cross-invocation release/wedge, PID and nvim survival; documented takeback interrupt kept; real paths.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Remaining gaps only; -1 value of owner info to callers not tied to a consumer. |
| Ownership and reuse | 19 | pty-only; extends existing tests and docs; -1 README update implied, not listed as acceptance. |
| Dependencies and implementable slices | 19 | Need done; ready; -1 shared footprint with command wait. |
| Observable acceptance and baseline evidence | 18 | Four checks with named existing tests; -2 "lost owner" recovery trigger (timeout vs reload) not pinned. |
| Failure, recovery and compatibility | 18 | Compatible control op, additive fields; -2 behaviour when hand-back happens before the shell prints a prompt left to probe. |
| Reviewer total | 93 / 100 | |

Result: **PASS**. Unresolved blocking findings: none.
Validation: existence checks of repo, source, test and doc paths (ls/rg); `./prd check` (cwd `/Users/feb/dev/cartridge/prd.ctg`, root graph) exit 0 with 228 records and no problems (needs resolve, no cycle); `just --list` (cwd `/Users/feb/dev/cartridge`) shows `test`/`smoke` and `.cartridge/memos/routine/cartridge-development.md` accepts the named owners; relative links checked. No product gates were run.
Reviewer: agent (independent reviewer, plan refresh pass). User rating: not requested (delegated).
Rounds used / remaining: 3 / 2.
Next action: ready to claim; `@ui/improve-ui-terminal-owner` (ui renamed tui) depends on it.
