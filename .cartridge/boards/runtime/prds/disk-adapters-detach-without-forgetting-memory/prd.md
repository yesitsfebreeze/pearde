---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 3
review-status: superseded-recommend-retire
canonical-scope: disk-adapters-detach-without-forgetting-memory
---

# disk-adapters-detach-without-forgetting-memory

Keep watcher/memo interpretation and mounted-adapter lifecycle with the host owners. Memory exposes ordinary validated ingest and explicit source retraction, remaining usable with every adapter absent. This candidate preserves the engine invariant while superseding the old memory plugin-loader prerequisite.

## Acceptance

- [ ] With adapters disabled, direct ingest/query/get still work in a disposable store.
- [ ] Stopping a watcher or reloading memo does not delete durable facts; only an explicitly owned retractable source can be retracted.
- [ ] Reattachment does not duplicate a writer or silently change source identity, and failed optional adapters produce visible status while memory remains usable.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `disk-adapters-detach-without-forgetting-memory`; maximum five rounds.
