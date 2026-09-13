---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: sessions
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: the-board-log-replays-who-did-what
---

# the-board-log-replays-who-did-what

Make the sessions journal the durable ordering authority. Append channel event and its causal telemetry reference atomically in that journal or report a recoverable gap; do not promise a total order from unrelated append files. Derived follow output uses global journal sequence and scoped references, with bounded retention.

## Acceptance

- [ ] Crash between post commit and telemetry projection rebuilds the projection from the journal and reports any unavailable range.
- [ ] A two-agent trace identifies post-to-wake causality, run/call outcomes and cancellation without storing secret payloads.
- [ ] Session/channel/run filters preserve the same sequence order and cannot reveal unauthorized records; rotation preserves monotonic sequence and names dropped ranges.

## Proof and recovery

Start at [main.rs](../../../main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test sessions` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

External evidence prerequisites: [the-board-is-channels-of-lines](../../../../memos/work/root--the-board-is-channels-of-lines.md). Resolve their current completion and source revision before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `the-board-log-replays-who-did-what`; maximum five rounds.
