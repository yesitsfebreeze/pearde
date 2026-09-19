---
state: "open"
origin: requested
priority: 75
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
footprint:
- "src/node/mod.rs"
- "src/transport/cartridge.rs"
---

# A native cartridge's outbound call does not block its own node

## Outcome

A native cartridge's outbound call to another cartridge does not hold its own
node exclusively for the duration of the call. While the first event is parked
waiting on the other cartridge's reply, a second, independent event dispatched
to the same node runs and can complete.

## Evidence

Found 2026-09-19 by the analyst of
`@mcp/a-cartridge-call-is-cancellable-and-bounded/a-cancelled-tool-call-reaches-its-running-tool`
against mcp.ctg `5a7c54c` and cartridge.ctg `beb8213`; the probe and its output
are in `prd.ctg/.cartridge/boards/mcp/.state/loop/a-cartridge-call-is-cancellable-and-bounded/analyst-cancelled-1.md`.
A real `cartridge mcp` bridge ran a busy-looping fixture tool for about 5.5 s,
and a `notifications/cancelled` sent 300 ms into the call never reached it: the
call ran to completion. A synchronous Lua handler's outbound call takes the
blocking branch of `either` in `src/node/mod.rs`, because
`coroutine.isyieldable()` is false behind mlua's C boundary, and the node's Lua
lock is held until the reply arrives. So the second event queues behind the
first.

The comment at `src/transport/cartridge.rs:976-980` explains why the listener is
kept off tokio workers. It does not say whether unrelated events on one node
must also be serialized, and that is the open design question this PRD owns.

Analyst probe, 2026-09-19, at `beb8213`: a real host with real nodes ran a
second event 300 ms into a 1.5 s outbound call. When the call is made from
yieldable Lua (`cartridge.bail` in the listener), the second event answered in
0.35 ms. When it is made from the native fixture's synchronous `ask`, it
answered only after 1.20 s. When it is made from inside a pure-Lua `string.gsub`
callback, it also took 1.20 s. The host already releases the lock at every
yielding await. It is held because of the non-yieldable caller, not because of
native code as such. mlua 0.12 keeps its lock private, and it swaps
`RawLua.state` in LIFO order on every callback entry. A native module's mlua is
built without `send`, so its mutex does nothing. For these reasons the host
cannot release the lock around `wait()` soundly. See
`.state/loop/a-native-cartridge-s-outbound-call-does-not-block-its-own-node/analyst-1.md`.
`base.rs` is vendored into each native cartridge rather than owned by
cartridge.ctg, so the analyst must first establish whether the fix lives in the
host alone or in the pattern every native cartridge copies; if the latter, this
PRD splits.

## Acceptance

- [ ] While one event on a native cartridge's node is parked in an outbound call, a second event dispatched to the same node runs to completion before the first call returns.
- [ ] A test drives both events against a real node and fails on the current tree, where the second event waits for the first.
- [ ] The existing guarantee holds: the listener never runs on a tokio worker, and the transport suite stays green.

## Answer (2026-09-19, from the user)

**Option A: a trampoline in each cartridge.** The host does not change. This PRD
shrinks to a host regression test showing that a second event runs while a
yielding listener waits on another cartridge, plus one sentence in
`cartridge help host` stating the rule. The mcp trampoline and the identical
`base.rs` copies in `agent.ctg` and `router.ctg` become their own PRDs.

## Questions (answered above)

**How should a native cartridge's outbound call stop serializing its node?**

The analyst established on 2026-09-19 that the fix cannot live in the host alone.
The measurements were made with real host nodes at cartridge.ctg `beb8213`. A
second event sent 300 ms into a 1.5 s outbound call answered in 0.35 ms when
the caller yielded through `cartridge.bail`. It waited 1.20 s behind a native
synchronous call, and also behind a pure-Lua `string.gsub` callback. So the
host already releases the Lua lock whenever the caller yields. What serializes
the node is a caller that cannot yield. Releasing mlua's lock from the host
would be unsound, because each native module carries its own copy of mlua. The
full report, with every option costed, is at
`prd.ctg/.cartridge/boards/runtime/.state/loop/a-native-cartridge-s-outbound-call-does-not-block-its-own-node/analyst-1.md`.

**Recommended: A, a trampoline in each cartridge.** The native handler hands its
outbound call back to Lua as a step, and the cartridge's `init.lua` loops
`cartridge.bail` in the yieldable listener. The host does not change. This PRD
shrinks to a host regression test and one sentence in `cartridge help host`
stating the rule. The mcp side becomes a child with footprint
`mcp.ctg/src/base.rs`, `src/lib.rs` and `init.lua`, and the identical `base.rs`
copies in `agent.ctg` and `router.ctg` are brought in line one after another.

The alternatives:

- **A′:** the same trampoline, but the host adds a helper such as
  `cartridge.drive` so each `init.lua` stays one line. This adds host API
  surface to save about three Lua lines per cartridge.
- **B:** a deferred event reply over `cartridge.pipe`. This needs a new host
  primitive, a FIFO in every native cartridge and a correlation id, and every
  cartridge still has to adopt it.
- **C:** accept serialization as the contract, document it, and close this
  PRD. `@mcp/.../a-cancelled-tool-call-reaches-its-running-tool` then stays
  blocked.
