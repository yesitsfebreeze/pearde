---
state: open
origin: requested
priority: 75
repo: "/Users/feb/dev/cartridge/mcp.ctg"
footprint:
- "src/service.rs"
- "src/lib.rs"
needs:
- "@runtime/a-cartridge-call-can-be-cancelled"
---

# A cancelled tool call reaches its running tool

## Outcome

An MCP client that cancels a tool call stops the tool that is running. The
cancellation machinery this cartridge already ships actually fires, instead of
always arriving after the call it was meant to stop has finished.

## Evidence

Established 2026-09-17 by analyst-1 of the parent, against `mcp.ctg` HEAD
`345871e` and `cartridge.ctg` HEAD `63ff234`.

The cartridge already implements MCP cancellation: the `inflight` map
(`src/service.rs:113`), registered in `invoke` (`:576-585`), consumed by
`notified` on `notifications/cancelled` (`:232-243`); and `pty.ctg/src/tool.rs:44-58`
genuinely honours `{"op":"cancel", context}`.

It is dead code by construction. `answer` in `src/lib.rs` is a synchronous Lua
function, so `invoke`'s call goes `base::bail` -> `cartridge.bail` and takes the
**blocking** branch of `either` (`cartridge.ctg/src/node/mod.rs:48-72,266-278`),
because `coroutine.isyieldable()` is false behind mlua's C boundary. The thread
holds Lua for the whole tool call. The cancellation line is bridged concurrently
(`cartridge.ctg/src/cli/host.rs:340-347` spawns per line), but its `mcp` event
queues behind that lock, so `notified` runs only after `invoke` has already
removed its entry and the lookup at `src/service.rs:239` always misses.

## Acceptance

- [ ] A `notifications/cancelled` for an in-flight tool call is observed by
      `notified` while that call is still registered in `inflight`.
- [ ] The running tool receives the cancel and stops; a tool that honours
      `{"op":"cancel"}` is proven to have been reached.
- [ ] A test drives a real in-flight call and a cancellation of it, failing in
      the world it denies — a test that passes when the lookup misses proves
      nothing.

## Needs

`@runtime/a-cartridge-call-can-be-cancelled`. Until a second `mcp` event can be
dispatched while one is in flight, no change inside `mcp.ctg` can reach this
code, because the event carrying the cancellation cannot run.

## First step for the analyst

The queueing behind the Lua lock follows from the source and from the host's own
comment at `cartridge.ctg/src/transport/cartridge.rs:924-926`, but it was NOT
observed in a run. Probe it before designing anything: dispatch a second `mcp`
event while one is in flight and record what happens.
