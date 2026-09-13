---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: a-listener-subscribes-to-event-types
needs:
- '@agent/an-event-declares-its-type'
---

# a-listener-subscribes-to-event-types

Use durable journal sequence numbers with at-least-once notifications; listeners acknowledge their cursor after processing and deduplicate by event identity where effects permit it. Bounded queues never block the run. An overflow/error retires the subscription with a visible gap and replay position.

## Acceptance

- [ ] Replay after disconnect delivers the missing range in order; duplicate notification preserves one event identity and does not fabricate exactly-once side effects.
- [ ] A hung listener leaves agent progress intact, with bounded resources and explicit delivery failure.
- [ ] Listener-origin posts retain authenticated attribution; removing or reloading the owner tears down only its subscription and old callbacks cannot revive it.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `a-listener-subscribes-to-event-types`; maximum five rounds.
