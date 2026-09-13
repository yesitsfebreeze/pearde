---
kind: work
level: 10
status: open
estimate: 4h
needs: ["@prd/work/memory--memory-daemon-boots-a-root-context.md"]
description: the daemon's hand-wired signals — the shutdown `Notify`, the takeover flag, the model service's `watch` stop — become extension events any plugin can listen to
read_when: "wanting a plugin to run at shutdown or on a store save, or touching the daemon's Notify wiring"
---

# memory-signals-become-events

## Do

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

## Check

`just test` green. A unit test in `commands` mounts a plugin listening to
`memory/shutdown` and asserts it ran, with `store` still `Active`, before the
`memory-core` disposer's fake save; a second asserts `memory/saved` carries the
save path. `grep -rn "watch::channel" src/mine/src/service.rs` finds
nothing.
