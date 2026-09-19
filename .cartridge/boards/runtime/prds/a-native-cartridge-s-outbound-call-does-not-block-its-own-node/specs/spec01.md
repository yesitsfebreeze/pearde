---
complexity: 1
footprint:
  - src/node/mod.rs
  - src/transport/cartridge.rs
  - .cartridge/tests/unit/src/tests/host.rs
  - .cartridge/help.md
  - src/node/README.md
---

# spec01 — a host regression test locks the rule that a yielding handler does not hold its node

Spec for the leaf @runtime/a-native-cartridge-s-outbound-call-does-not-block-its-own-node.
Base: cartridge.ctg **`324f36e`**, confirmed as HEAD immediately before this
revision was written. Under the user's Option A the host does not change:
everything below is one test and three sentences of documentation.

Round 1 of review declared `beb8213` and HEAD moved eight commits underneath it
during the round, which flipped one Verify block red and back again. The base
above is therefore stated as a measurement, not an intention, and the timing
table at the end is re-measured against it. `.cartridge/tests/unit/src/tests/host.rs`
is in this footprint and moved in that window: `804a08b` gave the base its own
`tool.asp`, so a `tool.*` glob now yields it and two assertions were updated —
`a_glob_in_needs_names_what_the_others_listen_to` and
`two_cartridges_that_need_each_other_both_start_when_one_asks_with_a_question_mark`.
Neither is named by this gate, and the test added below asserts on no `tool.*`
needs list, so it needs no `tool.asp` update. That file is being edited by
other PRDs; an implementer should re-check HEAD before cutting the lane.

The rule the PRD set out to settle is settled, and it is not the one the
Evidence section first assumed. A node already serves further events while a
handler waits, provided the handler yields. Measured on a `git clone --local`
of `cartridge.ctg` with a real `Host` and real node processes: a second event
dispatched 300 ms into a 1.2 s outbound `cartridge.bail` answered immediately.
What serializes a node is a caller that cannot yield — a native module's
synchronous call, or pure Lua inside a C-boundary callback such as a
`string.gsub` replacement. Those take the blocking branch of the `EITHER` chunk
at `src/node/mod.rs:48-52`, which calls `wait()` and holds the node's Lua state
for the whole round trip. The host cannot release mlua's lock around that wait
soundly, because each native module links its own copy of mlua built without
`send`; that is why Option A puts the trampoline in the cartridge and leaves the
host alone.

So the host side of this PRD is a lock, not a fix. Nothing here changes
behaviour. What is missing at base is a test of the property box 1 names — that
an **independent** second event completes while the first is parked. Measured
under the mutant described in `## Denied worlds`:
`tests::host::a_node_serves_other_events_while_a_handler_waits` (`host.rs:670`)
stays **green**, because its handler waits on a spawned program rather than on
another cartridge. `tests::host::a_call_that_comes_back_into_its_sender_is_answered`
(`host.rs:296`) does go **red**, but by self-deadlocking a re-entrant call until
its own 5 s timeout, which is a different property and not one box 1 states.
The test added here fails on the property itself.

The test cannot live in either originally declared file. `src/lib.rs:16-18`
mounts the whole host suite through
`#[path = "../.cartridge/tests/unit/src/tests/mod.rs"]`, and that suite's
helpers — `cartridge`, `descriptor`, `boot`, `node_binary`, `trust` at
`host.rs:11-58` — are private to `crate::tests`. An inline `#[cfg(test)] mod`
in `src/node/mod.rs` would have to duplicate about fifty lines of harness to
reach them.

## Steps

1. `.cartridge/tests/unit/src/tests/host.rs`: append the named test below. It
   is already `rustfmt`-clean in this shape; the two-line `assert!` forms it
   was first written in are not, and `cargo fmt --all --check` is a Verify
   block. `provider` busy-loops `os.clock` for 1.2 s, which stays well inside
   both the 60000 ms default `event_timeout_ms` and the 1e9 default
   `lua_instruction_budget`. `caller` declares `needs: ["provider.slow"]`,
   which is the send permission, and listens to two independent events.

   ```rust
   #[tokio::test(flavor = "multi_thread")]
   async fn a_second_event_runs_while_a_yielding_listener_waits_on_another_cartridge() {
   	let dir = tempfile::tempdir().unwrap();
   	cartridge(
   		dir.path(),
   		"provider",
   		json!({"name": "provider", "entry": "init.lua",
   			"events": {"provider.slow": {}}, "listen": ["provider.slow"]}),
   		r#"cartridge.listen("provider.slow", function()
   			local stop = os.clock() + 1.2
   			while os.clock() < stop do end
   			return "slow"
   		end)"#,
   	);
   	cartridge(
   		dir.path(),
   		"caller",
   		json!({"name": "caller", "entry": "init.lua",
   			"events": {"caller.relay": {}, "caller.quick": {}},
   			"listen": ["caller.relay", "caller.quick"], "needs": ["provider.slow"]}),
   		r#"cartridge.listen("caller.relay", function() return cartridge.bail("provider.slow", {}) end)
   		cartridge.listen("caller.quick", function() return "quick" end)"#,
   	);
   	descriptor(dir.path(), &["provider", "caller"]);
   	let host = boot(dir.path()).await;
   	let relay = tokio::spawn({
   		let host = host.clone();
   		async move { host.bail("caller.relay", json!(null)).await }
   	});
   	tokio::time::sleep(Duration::from_millis(300)).await;
   	assert!(
   		!relay.is_finished(),
   		"the relay answered before the second event was sent"
   	);
   	let started = std::time::Instant::now();
   	let answer = host.bail("caller.quick", json!(null)).await.unwrap();
   	let waited = started.elapsed();
   	assert!(
   		!relay.is_finished(),
   		"the relay answered before the second event did"
   	);
   	assert_eq!(answer, Some(json!("quick")));
   	assert!(
   		waited < Duration::from_millis(250),
   		"the second event did not run while the first was parked: {waited:?}"
   	);
   	assert_eq!(relay.await.unwrap().unwrap(), Some(json!("slow")));
   	host.stop().await;
   }
   ```

   The two `!relay.is_finished()` assertions are what stop the test degenerating
   into a tautology. Without them a `provider` that answered instantly would
   also make `caller.quick` fast, and the test would pass while proving nothing
   about concurrency. They are load-bearing in a second way: under the mutant,
   the second of them is sometimes the assertion that fires. See
   `## Denied worlds`.

2. `src/node/mod.rs`: extend the `EITHER` chunk with a comment stating the rule
   it decides — a caller that can yield releases the node's Lua state for the
   duration of the wait, so unrelated events on the same node keep being served;
   a caller that cannot yield takes `wait()` and holds the state until the reply
   arrives. Name the test in step 1 as the lock on the first half. No code
   changes here.

3. `src/transport/cartridge.rs`: the comment at lines 976-980 explains why the
   listener is kept off tokio workers and stops there. The PRD's Evidence says
   it "does not say whether unrelated events on one node must also be
   serialized". Add that second half: running off the workers is about worker
   starvation, and it does not serialize a node — concurrency between events on
   one node is decided by whether the handler yields, at the `EITHER` site in
   `src/node/mod.rs`. No code changes here either.

4. `.cartridge/help.md` (`cartridge help host`) and `src/node/README.md`: one
   sentence each stating the rule for the reader who has to write a cartridge —
   a node keeps answering while a handler waits, as long as the handler yields,
   and a handler that cannot yield holds its node for the whole call.
   `src/node/README.md` is paired with the help page because it is the node's
   own document and states the same rule to a source reader, not because of the
   cartridge README rule: that rule names a cartridge's own top-level
   `README.md`, and `cartridge.ctg/README.md` is deliberately left alone here
   since neither behaviour nor surface changes.

## Denied worlds

**The test is green on an unchanged tree, and that is intended.** Acceptance
box 2 does not ask it to fail at base; it asks it to be behavioural. That was
established by running a mutant, not by argument.

Mutant, applied to `src/node/mod.rs` in a clone at `324f36e`, deleting line 50,
`if yieldable() then return yielding(...) end`, from the `EITHER` chunk so that
every `cartridge.bail` takes `wait()`:

```lua
local yielding, blocking, yieldable = ...
return function(...)
	return blocking(...)
end
```

**The property a diff reviewer must reproduce is: the gate exits 101, and
`a_second_event_runs_while_a_yielding_listener_waits_on_another_cartridge` is
the only failure among the selected tests.** That held in six of six runs at
`324f36e` — four without `CARTRIDGE_YOLO`, two with it — every one
`test result: FAILED. 57 passed; 1 failed; 0 ignored; 0 measured; 117 filtered out`.

Do not pin the panic line. Which of the test's two assertions catches the
mutant alternates run to run, independently of the environment, because the
relay's 1.2 s loop sometimes expires before the blocked `caller.quick` returns.
Both are correct detections of the same serialization. Observed at `324f36e`:

```
the second event did not run while the first was parked: 977.207416ms
the second event did not run while the first was parked: 1.058162208s
the second event did not run while the first was parked: 1.467955375s
the second event did not run while the first was parked: 1.542090041s
the second event did not run while the first was parked: 2.200448083s
the relay answered before the second event did
```

With `src/node/mod.rs` restored, the same command exits 0, `58 passed; 0 failed`.

No Verify block applies this mutant: a block cannot prove why a test died, and
re-running it is the diff reviewer's gate, not collection's.

**Why the gate is scoped by filter, and a correction to round 1.** An earlier
draft of this spec justified the filter by claiming twelve tests fail at base.
**That claim was false and is withdrawn.** The twelve were an artefact of an
inherited `CARTRIDGE_YOLO=1`, exported by `just launch claude --yolo` into the
authoring session; the host merges `yolo: true` into every cartridge declaring
that setting, which is exactly what those twelve assert against. Measured at
`324f36e`, same clone, same warm target dir, both ways:

| `cargo test --lib -- --test-threads=1` | exit | result |
| --- | ---: | --- |
| under `env -u CARTRIDGE_YOLO` | **0** | `175 passed; 0 failed`, 58 s |
| with `CARTRIDGE_YOLO=1` | 101 | `163 passed; 12 failed`, 48 s |

The tree is green. The filter stays, for two reasons that are true:

- A Verify block runs in whatever environment the collector happens to carry
  and cannot assume the variable is absent. The filtered selection is
  green in **both** environments — exit 0, `58 passed; 0 failed`, with and
  without `CARTRIDGE_YOLO` — because none of the twelve sensitive names lies
  under `transport::` or is one of the two `tests::host::` names selected.
  Checked name by name against the run log.
- Speed. 12 s filtered against 58 s bare, warm, and the bare suite's cold cost
  would put it near the 120 s per-block limit on a growing suite.

## Acceptance

- [x] While one event on a native cartridge's node is parked in an outbound call, a second event dispatched to the same node runs to completion before the first call returns.
- [x] A test drives both events against a real node and goes red when the yieldable branch is removed from the `EITHER` chunk in `src/node/mod.rs`.
- [x] The existing guarantee holds: the listener never runs on a tokio worker, and the transport suite stays green.

## Verify

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/outbound-node-verify}"
cargo fmt --all --check
```

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/outbound-node-verify}"
cargo clippy --all-targets
```

```test
run: export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/outbound-node-verify}"; cargo test --lib -- --test-threads=1 tests::host::a_second_event_runs_while_a_yielding_listener_waits_on_another_cartridge tests::host::a_node_serves_other_events_while_a_handler_waits transport::
pass: a_second_event_runs_while_a_yielding_listener_waits_on_another_cartridge
pass: a_node_serves_other_events_while_a_handler_waits
pass: a_listener_that_blocks_does_not_park_the_only_worker
pass: a_cartridge_sends_a_declared_event_and_takes_the_answer
pass: a_cancelled_call_stops_a_listener_waiting_on_another_cartridge
pass: a_connection_runs_at_most_its_in_flight_limit_at_once
```

`libtest` takes several positional filters and ORs them, so the one command
covers box 2's new test, the spawned-program sibling, and every test under
`transport::` — 58 selected, 117 filtered out at `324f36e`. The third filter is
`transport::`, not `transport::cartridge::tests`, so box 3's "the transport
suite stays green" is actually what runs: `transport::cartridge::tests`,
`transport::rpc::tests` and the five `transport::typed::*` modules, 56 tests in
all. `a_listener_that_blocks_does_not_park_the_only_worker`
(`src/transport/tests/cartridge.rs:568`) is pinned by name because it is the
test that locks box 3's first half, that the listener never runs on a tokio
worker. `--test-threads=1` is not decoration: these tests boot real node
processes and the timing assertion is 250 ms.

The sentences of step 4, and the comments of steps 2 and 3, are a reviewer
gate, not a block. They are not among the PRD's three Acceptance boxes, and any
phrase test for them would print the exact words that satisfy it. The diff
reviewer is the backstop for wording, as the spec template says it is for a
block's body.

Measured on a `git clone --local` of cartridge.ctg at **`324f36e`** with step 1
applied, this machine, under `env -u CARTRIDGE_YOLO` unless the row says
otherwise:

| command | target dir | exit | wall |
| --- | --- | ---: | --- |
| the `test` block's command | **empty** | **0** | **47 s** — `58 passed; 0 failed; 117 filtered out` |
| the `test` block's command | warm | 0 | 12 s |
| the `test` block's command, `CARTRIDGE_YOLO=1` | warm | 0 | 8 s — same counts |
| `cargo clippy --all-targets` | **empty** | 0 | 25 s |
| `cargo clippy --all-targets` | warm | 0 | under 1 s |
| `cargo fmt --all --check`, step 1 applied | n/a | 0 | under 1 s |
| `cargo fmt --all --check`, live dirty `.rs` overlaid (pass-2 shape) | n/a | 0 | under 1 s |
| the mutant, six runs, four clean and two with the variable | warm | **101** ×6 | `57 passed; 1 failed` every time |

**This table is a headroom claim against a growing suite, not a constant.** The
same gate measured 20.9 s cold eight commits earlier and 48.8 s two commits
earlier; the `src/asp/` work took the `--lib` suite from 164 to 175 tests in a
day. The margin against the 120 s per-block limit is now about 2.5×, not 4×. An
implementer whose lane sits far from `324f36e` should re-run the cold row before
trusting it, and if the margin has gone, narrow the third filter rather than
widen the limit.

A cold isolated `CARGO_TARGET_DIR` is as cheap as it is here because
`~/.cargo/config.toml` sets `rustc-wrapper = "kache"`. No block writes inside
the footprint: `cargo fmt --all --check` only reports, and the two cargo builds
write solely under `target/outbound-node-verify`, which pass 2 keeps clear of
the live daemon's `target/debug`. After every run above, `git status --porcelain`
in the clone showed only ` M .cartridge/tests/unit/src/tests/host.rs`.

Note, not a box: after collection, `just check cartridge`, `just test cartridge`
and `just isolation` from `/Users/feb/dev/cartridge` are the post-integration
gates. The mcp trampoline and the vendored `base.rs` copies in `agent.ctg` and
`router.ctg` are separate PRDs and are not touched here.
