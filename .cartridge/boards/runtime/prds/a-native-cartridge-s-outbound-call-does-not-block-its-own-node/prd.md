---
state: "done"
origin: requested
priority: 75
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
footprint:
- "src/node/mod.rs"
- "src/transport/cartridge.rs"
- ".cartridge/tests/unit/src/tests/host.rs"
- ".cartridge/help.md"
- "src/node/README.md"
commit: "e4821bf5ecad81e542047372b81082faa4e5da0b"
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

- [x] While one event on a native cartridge's node is parked in an outbound call, a second event dispatched to the same node runs to completion before the first call returns.
- [x] A test drives both events against a real node and goes red when the yieldable branch is removed from the `EITHER` chunk in `src/node/mod.rs`.
- [x] The existing guarantee holds: the listener never runs on a tokio worker, and the transport suite stays green.

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

## Decision (2026-09-19, coordinator, after analyst-1 returned QUESTION)

Analyst-1 returned QUESTION rather than a spec, on the ground that the user's
Option A leaves no work inside the declared footprint and makes Acceptance box
2 unsatisfiable. Both findings are correct and both are measured, but neither
is a product question — the user has already made the product decision, and
what is left is bookkeeping this PRD's own record got wrong. So the coordinator
resolves it here instead of spending a second question round on the user.

**The footprint is widened to the paths Option A's own deliverables live in.**
Option A asks for a host regression test and one sentence of documentation. The
test cannot live in either originally declared file: `src/lib.rs:15-17` mounts
the whole host suite through `#[path = "../.cartridge/tests/unit/src/tests/mod.rs"]`,
and that suite's helpers (`cartridge`, `descriptor`, `boot`, `node_binary`,
`trust`, `host.rs:11-58`) are private to `crate::tests`, so an inline
`#[cfg(test)] mod` inside `src/node/mod.rs` would have to duplicate about fifty
lines of harness to reach them. The sentence belongs in `.cartridge/help.md`
(`cartridge help host`) and, for a source reader, `src/node/README.md`. The
footprint therefore becomes `src/node/mod.rs`, `src/transport/cartridge.rs`,
`.cartridge/tests/unit/src/tests/host.rs`, `.cartridge/help.md` and
`src/node/README.md`.

This does not reopen the user's answer. Option A says "the host does not
change", and none of the three added paths changes host behaviour: two are
documentation and one is a test. The two original files stay in the footprint
because the rule the PRD says is missing from the comment at
`src/transport/cartridge.rs:976-980` is recorded there and at the `EITHER` site
in `src/node/mod.rs`, which is exactly where the mutant below bites.

**Acceptance box 2 is reworded from "fails on the current tree" to the executed
mutant.** Analyst-1 wrote the 44-line test Option A asks for and ran it against
a `git clone --local` of `cartridge.ctg` at `beb8213`: it exits 0,
`finished in 6.09s`. The host already behaves, because it releases the Lua lock
whenever the caller yields; only a caller that cannot yield serializes the node,
and under Option A that caller is fixed in `mcp.ctg`, not here. A box demanding
the test fail today can never be ticked. What the box must demand instead is
that the test is behavioural, and that is established: with the yieldable branch
deleted from the `EITHER` chunk in `src/node/mod.rs` so every `cartridge.bail`
takes `wait()`, the same test exits 101 with
`the second event did not run while the first was parked: 901.865875ms`.

Boxes 1 and 3 stand as written; analyst-1 measured both green.

**Two gate facts for the spec, both measured, so no review round rediscovers
them.** `cargo test --lib` bare is unusable: twelve trust/`CARTRIDGE_HOME`
tests already fail at `beb8213` in a pristine clone, name for name, with and
without the new test, so any gate must be scoped by filter. And the timings fit
a 120-second Verify block with room — a cold isolated target dir costs 16 s
here (the `kache` rustc wrapper in `~/.cargo/config.toml`), the single test 3 s
warm, and `transport::cartridge::tests` 4 s for 15 passed.

The full evidence is in
`prd.ctg/.cartridge/boards/runtime/.state/loop/outbound-call-does-not-block/analyst-1.md`,
which also carries the ready-to-publish spec text and the test source verbatim.

## Decision (2026-09-19, coordinator, after review round 2 passed at 96)

Round 2 passed at 96 of 100 with no blocking findings, two rounds of five used.
The reviewer checked each of round 1's six findings by execution rather than by
reading the revision, and all six were genuinely fixed. The false twelve-failure
census is withdrawn and both measurements are now tabled: `env -u CARTRIDGE_YOLO`
gives exit 0 and `175 passed; 0 failed`, while `CARTRIDGE_YOLO=1` gives exit 101
and `163 passed; 12 failed` — the same twelve names, none of them under
`transport::` or among the selected host names. The mutant held in five runs
across both environments, always exit 101 with the new test the sole failure,
so it is not measuring the environment variable. The cold gate measured 35 s
against the 120-second limit, making the spec's own 47 s table conservative
rather than optimistic.

The analyst's self-retraction was confirmed in both halves:
`a_call_that_comes_back_into_its_sender_is_answered` does fail under the mutant,
self-deadlocking at `host.rs:317:10` with
`left serves pong while its go handler waits: Elapsed(())`, while
`a_node_serves_other_events_while_a_handler_waits` genuinely stays green. The
coverage argument rests on the sibling that holds.

**Non-blocking finding 7 is resolved here rather than left for whoever ticks a
box.** The reviewer observed that Acceptance box 1 says "a **native**
cartridge's node" while this spec's test exercises a yielding Lua caller, and
that no sentence tells a later reader which half this PRD locks and which half
its sibling delivers. The answer, now that both exist: this PRD pins the
**host** half — that the node is released whenever the caller yields, which the
mutant proves is a real property of `src/node/mod.rs` and not an accident. The
**cartridge** half, making a native handler actually yield instead of blocking,
was delivered by
`@mcp/a-cartridge-call-is-cancellable-and-bounded/a-cancelled-tool-call-reaches-its-running-tool`,
collected earlier today at `mcp.ctg` `624afb3`. Together they are the whole of
the user's Option A. Whoever ticks box 1 should tick it for the host property
this spec's gate measures, and not read it as a claim about any particular
native cartridge.

**Non-blocking finding 8 is accepted as a known ceiling.** The 250 ms timing
assertion can fail spuriously under load. That is a false **red**, never a
false pass, so it costs a rerun rather than admitting a defect — the correct
direction for a gate to be wrong in. The implementer should rerun a lone
failure of that assertion before treating it as real, particularly with eight
coordinator sessions sharing this machine.
