# Wait and retrieve output for one terminal command — review

Canonical PRD: [@pty/improve-pty-command-wait](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-pty-command-wait](../../../root/reviews/round-1/improve-pty-command-wait.md): reviewer 92/100; Keep. Stable command identity, timeout without cancellation and expired-history errors are explicit.
  Original SHA-256: `002d8a9b69453ea09a39a693a46c5d2d5191b3857626d9593062973bff3df602`.

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

Reconciliation verdict: **REBASE**. Evidence: pty ported to transport (0a21768, 0db055d); source moved to `pty.ctg/src/`, tests to `.cartridge/tests/`; partial baseline in source: `src/marks.rs` `Command.id`/`truncated` with tail-only output, `src/main.rs` `Shell::run` waits on the done mark without killing, `pty {op:"commands"}` lists ids; `src/tool.rs` command result is text without id; `handoff-baseline-context.json` in this directory records unresolved delayed-mark correlation. Pre-revision text (SHA-256 `b3c886d0854dcedf6982c14949ea8e37f0b262676720e03014e2396409e55389`) named five missing paths, ignored the delivered baseline and the recorded race, and listed a constraint as acceptance. Blocking.

Revision reviewed: `prd.md` SHA-256 `f47cd19d6c4eed6c9b5abfd99d6f0024f398d77e0872b96f20812e8bb713df8c` (working tree). Changes: baseline and gaps stated; id in result, wait-by-id, evicted-id and no-integration reasons, delayed-mark fixture; `input.rs` (key encoding) removed from footprint; real paths; gate with known failures.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Closes observable gaps only; -1 paging of truncated output dropped to explicit reporting without saying so. |
| Ownership and reuse | 19 | pty-only, reuses marks/history; -1 wait op name/shape left to implementation. |
| Dependencies and implementable slices | 19 | Need done; ready; -1 shares `src/main.rs`/`tool.rs`/process.rs with input ownership (parent orders landing). |
| Observable acceptance and baseline evidence | 18 | Four checks incl. race fixture, baseline command; -2 no numeric history bound stated for eviction test. |
| Failure, recovery and compatibility | 18 | Additive fields, no shell restart, no live terminal; -2 cancellation during a pending wait not specified. |
| Reviewer total | 93 / 100 | |

Result: **PASS**. Unresolved blocking findings: none.
Validation: existence checks of repo, source, test and doc paths (ls/rg); `./prd check` (cwd `/Users/feb/dev/cartridge/prd.ctg`, root graph) exit 0 with 228 records and no problems (needs resolve, no cycle); `just --list` (cwd `/Users/feb/dev/cartridge`) shows `test`/`smoke` and `.cartridge/memos/routine/cartridge-development.md` accepts the named owners; relative links checked. No product gates were run.
Reviewer: agent (independent reviewer, plan refresh pass). User rating: not requested (delegated).
Rounds used / remaining: 3 / 2.
Next action: ready to claim; coordinate landing order with `@pty/improve-pty-input-ownership`.
