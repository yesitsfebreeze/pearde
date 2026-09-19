---
state: "open"
origin: requested
priority: 75
repo: "/Users/feb/dev/cartridge/mcp.ctg"
footprint:
- "src/service.rs"
- "src/lib.rs"
- "src/base.rs"
- "init.lua"
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
`345871e` and `cartridge.ctg` HEAD `63ff234`. Re-verified 2026-09-19 against
current HEADs — `mcp.ctg` `5a7c54c` (the `inflight` map moved from the
service onto each attached `Instance`) and `cartridge.ctg` `beb8213` (the
child need below, now done) — by `git show <HEAD>:<path>` and by an executed
probe; every line reference below is current.

The cartridge already implements MCP cancellation: the per-instance `inflight`
map (`src/service.rs:120,126`), registered in `invoke` (`:612-616`), consumed by
`notified` on `notifications/cancelled` (`:254-262`); and `pty.ctg/src/tool.rs:44-58`
genuinely honours `{"op":"cancel", context}`.

It is dead code by construction. `answer` in `src/lib.rs:41-64` is a synchronous
Lua function (registered via `create_function`, `src/lib.rs:74`) that does
`base::runtime().block_on(service.message(...))` (`:58`). `invoke`'s call goes
`(self.call)` -> `base::bail` (`src/base.rs:71-73`) -> `with(...)`'s
`cartridge.call_function("bail", ...)` (`src/base.rs:49-67`), a **synchronous**,
thread-pinned call ("only a thread the base called into may touch it",
`src/base.rs:6-7,30-38`) that reaches `cartridge.bail` and takes the
**blocking** branch of `either` (`cartridge.ctg/src/node/mod.rs:48-72`, bound at
`:266-278`), because `coroutine.isyieldable()` is false behind mlua's
non-continuation C-call boundary. The thread holds `mcp.ctg`'s node's Lua state
for the whole tool call, including the wait on the tool's own reply — the exact
scenario the host's own comment now names in prose
(`cartridge.ctg/src/transport/cartridge.rs:976-980`, added by the child need's
own commit): "a listener takes its node's Lua lock synchronously, and a lock
held by a handler waiting on another cartridge would park the worker whose
queue carries that very reply." The cancellation line is bridged concurrently
(`cartridge.ctg/src/cli/host.rs`, `Backend::message`/`stdio`'s
`serving.spawn(...)` per line), and it does reach the transport as its own
independent `event` request with its own permit and its own cancellation token
(`cartridge.rs:855-889`) — dispatch itself is not serialized. But its `mcp`
event's Lua call still queues behind the same node's Lua lock that the first
event's `answer()` is holding, so `notified` runs only after `invoke` has
already removed its entry and the lookup at `src/service.rs:261` always misses.

**Probed 2026-09-19** (the parent's own "first step," previously unexecuted):
fresh debug builds of both repos at these exact HEADs, composed with a fixture
tool whose Lua listener busy-loops (CPU-bound, since this sandbox is
`StdLib::ALL_SAFE ^ IO ^ PACKAGE` — no `io`, no `os.execute` — per
`cartridge.ctg/src/lua/mod.rs:26`) and checks a shared upvalue set by its own
`{"op":"cancel"}` arm. A real `cartridge mcp` bridge process called the tool,
and 300 ms into a ~5.5 s call sent a real `notifications/cancelled` for that
request id on the same stdio. The call ran to completion
(`"completed-without-cancel …"`) rather than stopping early — reproducing the
exact failure this PRD names, unchanged by the now-`done` child need. Command
and result are in the analyst report; the harness is the same shape as this
cartridge's own `.cartridge/tests/integration/instances.test.ts` (which already
sends a real `notifications/cancelled` over real stdio, just not against an
in-flight call).

**What the child need actually changed, and why it does not reach here:**
`@runtime/a-cartridge-call-can-be-cancelled` (done, `beb8213`) makes the
*transport* observe a *caller's own* abandoned call — an expired bound now
cancels that specific `event` RPC's listener via a `select!` inside its
`spawn_blocking`/`block_on` (`cartridge.rs:976-993`). That is orthogonal to this
PRD's mechanism: the MCP `notifications/cancelled` here is not a caller giving
up on the first `tools/call`'s own RPC — it is a **second, independent** `mcp`
event whose own Lua call cannot start running its `notified()` logic until the
first event's `answer()` releases the same node's Lua lock. Nothing in the
child need's change touches that lock, and the probe confirms it: the lock is
acquired by `base::bail`'s synchronous, thread-pinned call convention
(`src/base.rs`, vendored into every native cartridge, not part of this PRD's
declared footprint), not by anything `cartridge.ctg`'s transport layer
arbitrates.

## Acceptance

- [ ] A `notifications/cancelled` for an in-flight tool call is observed by
      `notified` while that call is still registered in `inflight`.
- [ ] The running tool receives the cancel and stops; a tool that honours
      `{"op":"cancel"}` is proven to have been reached.
- [ ] A test drives a real in-flight call and a cancellation of it, failing in
      the world it denies — a test that passes when the lookup misses proves
      nothing.

## Needs

`@runtime/a-cartridge-call-can-be-cancelled` — done, but insufficient alone
(see Evidence): it lets a caller abandon its own call, not a second event
interleave with a first on the same node. Still needed, and not yet proposed
as a PRD: a `runtime`-board outcome that lets a native cartridge's own
outbound call to another cartridge (`base::bail`'s synchronous, thread-pinned
convention behind `cartridge.bail`'s blocking branch) not hold its whole
node's Lua state for the call's duration, so a second, independent event
dispatched to that node can run while the first is parked on another
cartridge's reply. Analyst verdict: SPLIT: propose that outcome as a sibling
child, this PRD's `needs` gains it, and this PRD is not specced until it
lands. See the analyst's `2026-09-19` report for the proposed child text.

## First step for the analyst

Done 2026-09-19: probed rather than argued from source alone. See Evidence.
The result is negative — dispatching a second `mcp` event while one is in
flight still does not let its cancellation reach the running tool, at the
current HEAD of the child need this PRD already lists.

## Answer applied (2026-09-19, user chose option A)

The user chose option A for
`@runtime/a-native-cartridge-s-outbound-call-does-not-block-its-own-node`: a
trampoline in each cartridge, with the host unchanged. So this PRD no longer
waits on a host change and owns the mcp side. `answer` returns a
`{call, data, id}` step instead of blocking in `base::bail`, and `init.lua`
loops `cartridge.bail` in the yieldable listener until the handler is done. The
footprint gains `src/base.rs` and `init.lua`. The proof is the probe from
`analyst-cancelled-1`: a `notifications/cancelled` sent 300 ms into a long call
reaches the tool. `base.rs` is vendored identically into `agent.ctg` and
`router.ctg`; bringing those copies in line is
`@root/the-vendored-base-rs-stays-identical-across-native-cartridges`, which
needs this PRD.
