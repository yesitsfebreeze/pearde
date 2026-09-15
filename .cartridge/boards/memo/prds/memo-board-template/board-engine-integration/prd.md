---
repo: /Users/feb/dev/cartridge/memo.ctg
state: deferred
deferred-from: specced
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memo
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: memo-board-template
footprint:
- src/board.rs
- .cartridge/templates/board
- .cartridge/tests/unit/board.rs
- .cartridge/tests/integration/board-engine.test.ts
- .cartridge/docs/board.md
needs:
- '@memo/memo-board-template/initialize-board'
commit: "154bde9d8f97fb1c015fe34cf62ae79b153e6feb"
---

# The generated board uses the pinned Pearde workflow

Connect the generated template to the maintained native PRD engine and its full planner entry; keep engine ownership external to memo. The current PRD docs supersede the retired external Pearde CLI.

## Acceptance

- [x] A generated fixture resolves cross-board dependencies and exposes the ready frontier.
- [x] Invalid transitions and overlapping claims are refused.
- [x] The same fixture works from a second checkout path without developer-home assumptions.

## Proof and recovery

Start at [service.rs](../../../../../../../memo.ctg/src/service.rs), [record.rs](../../../../../../../memo.ctg/src/record.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test memo` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `memo-board-template`; maximum five rounds.
