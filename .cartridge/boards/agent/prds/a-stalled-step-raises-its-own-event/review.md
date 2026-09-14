# a-stalled-step-raises-its-own-event — review

Canonical PRD: [@agent/a-stalled-step-raises-its-own-event](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [a-stalled-step-raises-its-own-event](../../../root/reviews/round-1/a-stalled-step-raises-its-own-event.md): reviewer 90/100; Keep. Clear observation-only threshold behavior; use a monotonic fake clock and verify cancellation/reload removes pending timers.
  Original SHA-256: `9b6f694b5f190f7f39d8cd766c828d54bbcc6f7f315bb999fd4e0a219b821c11`.

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

Reconciliation verdict: **REBASE**. Outcome still wanted and absent (no budget setting in `agent.ctg/cartridge.json`, no stall emission in `agent.ctg/src`). The host now provides the delivery half: `ctx.notify` emits to listeners and publishes on a channel with bounded replay, and `subscribe` with `since` resumes (cartridge.ctg `c9ef10b`, `docs/transport.txt` STREAMS). The hard need on `@runtime/a-listener-subscribes-to-event-types` (open, stale, cites nonexistent `cartridge.ctg/src/runtime.rs`/`service.rs`) is therefore no longer a prerequisite for this leaf and was removed.

Presented revision: prd.md SHA-256 `6d70e9ce6bf98a4ab480d339e7d8b410db707702cc1b4bcff33b040b58a7d4d2` (rebased from `9ca1fc391f4fbbbf5157a05f0a5633004f7bb4b9362baaafe5574b16a8fcc423`). Source revisions: agent.ctg `fad6d3b`, cartridge.ctg `c9ef10b`, sessions.ctg `e9725e8`, harness.ctg `336f2d1`, prd.ctg `077e57a2` (dirty tree).

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Observation-only stall signal, escalating once per threshold. −2: which step types carry budgets (stream vs tool) is left to the probe; 306 words. |
| Ownership and reuse | 19 | Agent-owned; reuses `Live.active`, `Run::emit` and host channels; budgets as declared settings. −1: settings shape not yet written. |
| Dependencies and slices | 18 | No remaining hard need; delivery path cited in host source. −2: events-port precondition has no PRD. |
| Observable acceptance and baseline | 18 | Four checks with paused time, no-budget case, timer cleanup (round-1 note restored), channel delivery. −2: source-reading baseline; gate cannot build until the port. |
| Failure, recovery and compatibility | 18 | Timer error never affects the step; null budget disables; replay buffer bound noted. −2: restart semantics of a partly elapsed budget unspecified. |
| Reviewer total | **91 / 100** | |

Findings and concrete revisions: (1) starting-file links resolved to nonexistent `boards/model_loop.rs`/`boards/run_state.rs`; run state now lives in `agent.ctg/src/lib.rs` and `run_state.rs` is a test module under `.cartridge/tests/unit/` — replaced with real paths and a footprint. (2) Dropped the obsolete runtime-listener need; delivery via host channel subscription. (3) Restored round-1 fake-clock and timer-cleanup requirements. Coordinator note: the rollup `@agent/the-run-is-a-stream-of-typed-events` and `@runtime/a-listener-subscribes-to-event-types` should reconcile the listener leaf against host streams.
Program finding (non-blocking for this plan, blocks implementation): agent.ctg `fad6d3b` still calls `transport::cartridge::run`, `ctx.call` and `ctx.provide` (`agent.ctg/src/main.rs:14,33,42`) and declares `provide` in `cartridge.json`; cartridge.ctg `ee7e295` removed that API and manifests now refuse unknown fields (`cartridge.ctg/docs/creating-cartridges.txt`). No agent gate builds until the agent is ported to declared events; no PRD owns that port. Coordinator action.
Disposition: keep (rebased).
Validation: `ls`/`rg`/`grep` existence checks of every cited path and line, needs resolution under `boards/<owner>/prds/<slug>/prd.md`, root `.cartridge/justfile` recipes (`test`, `check`, `verify`, `smoke`) and the `agent` case in `.cartridge/memos/routine/cartridge-development.md`, `git log` of agent.ctg and cartridge.ctg, decision memo reads. No product gates were run.
Reviewer identity: agent (independent reviewer, plan refresh pass). User rating: not required under delegation; none supplied. User feedback: none supplied for this revision.
Result: **PASS** (91/100).
Unresolved blocking findings: none.
Rounds used / remaining: 3 / 2.
Next action: after the events port, probe with paused time and write specs.
