---
state: open
origin: requested
priority: 60
repo: "/Users/feb/dev/cartridge"
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
wave: 4
date: "2026-09-15"
footprint:
- "prd.ctg/src/coordinator.ts"
- "prd.ctg/src/process.ts"
- "prd.ctg/.cartridge/adapters"
needs:
- the-repository-answers-by-text
---

# run-board dispatches through the orchestrator

## Outcome

The board and the orchestrator share one worker registry and one proxy; the board can drive itself.

## Acceptance

- [ ] `prd run --adapter cartridge --workers 2` spawns workers through `live_agent spawn kind=claude`, takes two ready leaves through analyst → specced → lane → implementer → verifier → collect; lanes are removed after collect and the transitions are in the PRD files.
- [ ] The `claude --print` adapter is deleted.

## Folds

Deferred with `superseded-by` pointing here:

- @prd/consolidate-planning-in-prd (claimed item)
- @root/the-work-can-be-proven
- @sessions/the-board-log-replays-who-did-what (transitions as events)

## Result

Not started.
