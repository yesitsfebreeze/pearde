---
repo: /Users/feb/dev/cartridge/memory.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
review-round: 3
review-status: failed
canonical-scope: memory-signals-become-events
needs:
- "@memory/memory-daemon-boots-a-root-context"
---

# Memory announces a durable save as a host event

Memory emits no lifecycle events today. The daemon's `save_fn` returns nothing, while the store computes `Flushed { epoch }` or `RefusedStale` (`src/store/core/src/lib.rs`) and throws the result away. The `events` op is a polled view of graph changes (`tool_events` in `src/rpc/src/server.rs`), not a lifecycle signal. The rewritten host now carries events. `ctx.emit` in `cartridge.ctg/src/transport/cartridge.rs` sends only declared events, never waits for listeners, and reports listener failures on the cartridge's `error` channel. Outcome, owned by memory: after a successful flush the cartridge emits `memory.saved {store, epoch, owner_pid, generation}`; a refused or failed flush emits nothing. Listeners own their reactions (decision `a-cartridge-brings-its-own-surface`), so memory needs no event framework of its own.

## Acceptance

- [ ] A cartridge-mode ingest with `sync:true` is followed by exactly one `memory.saved`, and its epoch equals the persisted store epoch. `RefusedStale` or a save error emits nothing and is logged.
- [ ] A listener that hangs or fails cannot stretch the `on_dispose` drain or the final save past their existing bounds, because `emit` does not wait.
- [ ] Each event names the emitting owner's generation, and `health` and `status` report the same generation. After a replacement, events from the old owner carry the old generation.

## Proof and recovery

First probe: find how a cartridge declares a send so that `prepare` accepts it, and where the cartridge path can observe a flush result. Tests go in `.cartridge/tests/integration/cartridge.rs` with a listener fixture. Gates, from /Users/feb/dev/cartridge/memory.ctg: `just check`, `just test` (not run). Rollback: remove the declaration and the emit call; stored data is unaffected.

## Dependencies and review

No hard needs. Land it after memory-daemon-boots-a-root-context, because both change the same lifecycle files. **Open decision:** no consumer of a memory save event is named. Before claiming, record the consumer or retire this PRD. [Review history](review.md): round 3 of 5.

## From the retired work memo

Folded 2026-09-15 from `@prd/work/memory--memory-signals-become-events.md` (status open, estimate 4h). The PRD state above is authoritative.

> the daemon's hand-wired signals — the shutdown `Notify`, the takeover flag, the model service's `watch` stop — become extension events any plugin can listen to

### Do

- Declare in `commands` the events `memory/shutdown` (`Parallel`, args
  `()`) and `memory/saved` (`Emit`, args `{ path }`), and `memory/takeover`
  (`Emit`) where `identity::spawn_self_watch` flips the flag.
- `run_server` dispatches `memory/shutdown` through `root.parallel` before
  `root.fiber().dispose()`, so a plugin can flush while every service is
  still `Active`; the `memory-core` disposer emits `memory/saved` after the
  save.
- `mine`'s `Service::shutdown` (`src/mine/src/service.rs`) becomes the
  `models` plugin's disposer and its `watch::Sender<bool>` goes; the axum
  graceful shutdown awaits the disposer's signal instead.
- The `shutdown: Arc<Notify>` handed to `MemoryRpcHandler` stays: it is the
  operator's request to stop, which the root disposal then carries out.

### Check

`just test` green. A unit test in `commands` mounts a plugin listening to
`memory/shutdown` and asserts it ran, with `store` still `Active`, before the
`memory-core` disposer's fake save; a second asserts `memory/saved` carries the
save path. `grep -rn "watch::channel" src/mine/src/service.rs` finds
nothing.
