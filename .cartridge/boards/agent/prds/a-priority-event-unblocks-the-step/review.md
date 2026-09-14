# a-priority-event-unblocks-the-step — review

Canonical PRD: [@agent/a-priority-event-unblocks-the-step](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [a-priority-event-unblocks-the-step](../../../root/reviews/round-1/a-priority-event-unblocks-the-step.md): reviewer 84/100; Revise. Define priority-versus-cancel precedence, partial tool-group projection and completion-unknown outcomes; retain late effects for reconciliation even when late responses are excluded.
  Original SHA-256: `1db4330f39fd80a1ee22241ac505b40ff96b6d7a0009e1484dff3e65b35e21e0`.

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

## Round 3 — 2026-09-14 (reconciliation and rebase)

Reconciliation verdict: **REBASE**. Outcome still wanted and agent-internal; the cut machinery it builds on still exists (`agent.ctg/src/stream.rs:120,144`, `agent.ctg/src/lib.rs:127,149,428`, `agent.ctg/src/model_loop.rs:60`), but paths moved to `src/` and the priority post now arrives as a declared host event (see `@agent/a-live-run-accepts-events-from-outside`). Not delivered: cancel is a single `watch<bool>` and every cut is terminal.

Presented revision: prd.md SHA-256 `ed613f9b2c824dade164e8a490ea94c01e342c0a5e296aabb06e73e8f14d39c6` (rebased from `24aaf495960b7d69b88e8ebc887934b63403e3b5ec868d5ecdbf96b4c1e50db8`). Source revisions: agent.ctg `fad6d3b`, cartridge.ctg `c9ef10b`, sessions.ctg `e9725e8`, harness.ctg `336f2d1`, prd.ctg `077e57a2` (dirty tree).

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | One outcome: preempt a step, same run continues; cancel semantics preserved. −1: model-stream and tool cases share one leaf (acceptable, same signal split). |
| Ownership and reuse | 19 | Splits the existing cancel watch; reuses stream partial, exact-call cancel and `interrupted-outcome-unknown`. −1: approval binding interplay with `approve()` not yet probed. |
| Dependencies and slices | 17 | Need resolves; order explicit. −3: need is open and only just rebased; events-port precondition has no PRD. |
| Observable acceptance and baseline | 18 | Four checks incl. precedence and approval preservation; first probe names the existing test at `run_state.rs:419`. −2: source-reading baseline; gate cannot build until the port. |
| Failure, recovery and compatibility | 18 | Failure ends `failed` without replay; transcripts unchanged. −2: wait-duration bound for uncancellable work unspecified. |
| Reviewer total | **91 / 100** | |

Findings and concrete revisions: (1) starting-file links resolved to nonexistent `boards/model_loop.rs`/`boards/run_state.rs`; run state now lives in `agent.ctg/src/lib.rs` and `run_state.rs` is a test module under `.cartridge/tests/unit/` — replaced with real paths and a footprint. (2) Restored round-1 checks dropped in migration: stream partial kept and run reaches `completed`; no priority path yields `cancelled`. (3) Baseline and first probe now name concrete source lines and test.
Program finding (non-blocking for this plan, blocks implementation): agent.ctg `fad6d3b` still calls `transport::cartridge::run`, `ctx.call` and `ctx.provide` (`agent.ctg/src/main.rs:14,33,42`) and declares `provide` in `cartridge.json`; cartridge.ctg `ee7e295` removed that API and manifests now refuse unknown fields (`cartridge.ctg/docs/creating-cartridges.txt`). No agent gate builds until the agent is ported to declared events; no PRD owns that port. Coordinator action.
Disposition: keep (rebased).
Validation: `ls`/`rg`/`grep` existence checks of every cited path and line, needs resolution under `boards/<owner>/prds/<slug>/prd.md`, root `.cartridge/justfile` recipes (`test`, `check`, `verify`, `smoke`) and the `agent` case in `.cartridge/memos/routine/cartridge-development.md`, `git log` of agent.ctg and cartridge.ctg, decision memo reads. No product gates were run.
Reviewer identity: agent (independent reviewer, plan refresh pass). User rating: not required under delegation; none supplied. User feedback: none supplied for this revision.
Result: **PASS** (91/100).
Unresolved blocking findings: none.
Rounds used / remaining: 3 / 2.
Next action: wait for the post leaf and the events port; then probe and write specs.
