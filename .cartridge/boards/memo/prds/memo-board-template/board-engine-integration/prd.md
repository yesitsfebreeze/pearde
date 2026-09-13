---
repo: /Users/feb/dev/cartridge/memo.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memo
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: memo-board-template
needs:
- '@memo/memo-board-template/initialize-board'
---

# The generated board uses the pinned Pearde workflow

Connect the generated template to the existing external engine and its full planner entry; keep engine ownership external.

## Acceptance

- [ ] A generated fixture resolves cross-board dependencies and exposes the ready frontier.
- [ ] Invalid transitions and overlapping claims are refused.
- [ ] The same fixture works from a second checkout path without developer-home assumptions.

## Proof and recovery

Start at [service.rs](../../../../../../../memo.ctg/src/service.rs), [record.rs](../../../../../../../memo.ctg/src/record.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test memo` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `memo-board-template`; maximum five rounds.
