---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
---

# Lua calls into the host without blocking a worker

## Outcome

A Lua cartridge dispatching an event or calling a service does not park a Tokio worker thread. Today `src/lua.rs:511` implements `block_on` as `block_in_place` plus a nested `Handle::current().block_on`, and every Lua-facing operation routes through it: `ctx:emit`, `ctx:bail`, `ctx:parallel`, `ctx:gather`, and `dispose` in `src/context.rs:64-144`, remote service calls at `src/lua.rs:408` and `src/lua.rs:437`. That design only works on a multi-thread runtime, panics on `current_thread`, costs a worker per nested call, and deadlocks whenever the awaited future needs the same Lua state.

## Acceptance

- [ ] `block_on` in `src/lua.rs` is removed; `grep -n block_on src/` finds only the manifest discovery runtime in `src/cartridge.rs:285`, which owns its own runtime.
- [ ] Lua functions that await host work are created with `mlua`'s async function API (`create_async_function`) or the Lua state runs on one dedicated thread that talks to the host over channels; the PRD's specification names which and why.
- [ ] The full suite passes under `#[tokio::test]` default flavor (`current_thread`) as well as multi-thread.
- [ ] A test issues 64 concurrent Lua `ctx:gather` calls on a two-worker runtime and completes; today that starves.
- [ ] A Lua listener that calls back into a service provided by the same Lua cartridge completes without deadlock.

## Proof and recovery

Start at `src/lua.rs:398-440` and `src/context.rs:120-150`. Keep the public Lua API (`ctx:emit`, `ctx:bail`, `ctx:gather`, `ctx:parallel`) unchanged so no cartridge changes. Measure before and after with the existing `lifecycle` and `stream` tests.
