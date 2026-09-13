---
repo: /Users/feb/dev/cartridge/memo.ctg
state: "done"
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
- src/main.rs
- src/service.rs
- src/board.rs
- .cartridge/templates/board
- .cartridge/tests/unit/board.rs
- .cartridge/docs/board.md
commit: "0976a3b0035c67bbb828063a1def17a1f5297d14"
---

# Preview and install a board without overwriting edits

Copy the owner-local template with explicit preview and collision handling.

## Acceptance

- [x] An empty fixture receives the declared files.
- [x] Repeated application changes no bytes.
- [x] A conflicting edited file is reported and preserved; interrupted application is resumable.

## Proof and recovery

Start at [service.rs](../../../../../../../memo.ctg/src/service.rs), [record.rs](../../../../../../../memo.ctg/src/record.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test memo` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `memo-board-template`; maximum five rounds.
