---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: memory-signals-become-events
---

# memory-signals-become-events

Retain only notifications needed to observe current memory persistence and owner handoff. Reuse existing lifecycle primitives and publish facts after the event they describe; external runtime listeners own subscriptions. Remove the obsolete mine/watch-channel deletion prescription.

## Acceptance

- [ ] A saved notification follows a successful durable save and carries store/source revision, not merely a requested path.
- [ ] Shutdown observers cannot indefinitely prevent admission closure and save; failure is bounded and visible.
- [ ] An old owner cannot emit a successor's completion, and memory requires no general plugin-event framework to satisfy the contract.

## Proof and recovery

Start at [cartridge.rs](../../../../../../memory.ctg/src/cartridge.rs), [main.rs](../../../../../../memory.ctg/src/main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `memory-signals-become-events`; maximum five rounds.
