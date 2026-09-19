---
complexity: 5
footprint:
  - src/base.rs
  - src/lib.rs
  - init.lua
  - .cartridge/tests/integration/cancel.test.ts
---

# spec01 — `answer` hands its outbound calls back to a yieldable listener

## Scope

Option A of the answer the user gave on 2026-09-19: a trampoline in this
cartridge, the host unchanged. `mcp.answer` stops waiting for another cartridge
on the base's own thread. Instead it runs the message as a job on this module's
runtime and returns a **step** for every outbound call; `init.lua` makes that
call with `cartridge.bail` from the listener body, which is yieldable, so the
node is free while the call is out and a second `mcp` line — the one carrying
`notifications/cancelled` — runs `notified()` while `inflight` still holds the
entry.

`src/service.rs` needs **no change**: the whole defect is at the Lua boundary.
The PRD's declared footprint lists it; this spec does not use it.

One path here was outside the PRD's four when this spec was drafted: the new
integration test `.cartridge/tests/integration/cancel.test.ts`. Acceptance box
three demands a test that drives a real in-flight call and none of the four
declared paths can hold one. The coordinator has since recorded that widening
on the PRD ("Decision (2026-09-19, coordinator, at publish of spec01)"), so
this spec's footprint is now entirely inside the declared set. No production
path outside the original four is touched, and no `Cargo.toml` change is needed
— see the section on `create_async_function` below.

## What was measured, not assumed

Every number below was observed by this analyst on 2026-09-19 against
`mcp.ctg` `1595a6f` and the prebuilt `cartridge.ctg` daemon at `beb8213`.

1. **A yielding `cartridge.bail` in a listener releases the node.** A fixture
   cartridge whose listener called `cartridge.bail` into a ~3.1 s provider was
   sent a second, independent event 0.8 s in: it answered in **10 ms**, while
   the first was still parked. Two events on one node do interleave once the
   first parks in a yieldable context.
2. **A bare `coroutine.yield()` in a listener releases it too.** A listener
   spinning on `coroutine.yield()` saw a flag set by a second event's listener
   after 817 123 yields, and the second event answered in 10 ms. This is what
   makes the `wait` step below cost no host traffic.
3. **The whole trampoline was prototyped and run end to end.** With it,
   a real `cartridge mcp` bridge, a real `tools/call`, and a real
   `notifications/cancelled` sent 400 ms in, the fixture tool's own answer was
   `stopped-on-cancel 280052`. On the unmodified tree the same test answers
   `ran-to-completion 3000000`.
4. **No regression in what exists.** `cargo test --lib` on the prototype:
   `23 passed; 0 failed; 1 ignored` in 5.8 s (with `CARTRIDGE_BIN` and
   `MCP_MODULE` set, which the shelling-out unit test needs; without them that
   one test fails identically on the unmodified tree). `approval.test.ts` and
   `instances.test.ts` pass on both trees; `refresh.test.ts` fails on both
   trees the same way ("Live catalog did not settle"), so it is pre-existing
   and not this change's.

## The mechanism

### `src/base.rs` — a `job` module, vendored with the rest of the file

The trampoline belongs here, not in `lib.rs`, because `base.rs` is the file
`@root/the-vendored-base-rs-stays-identical-across-native-cartridges` will
carry into `agent.ctg` and `router.ctg`.

- `ASKS`: a `tokio::task_local!` holding an `mpsc::UnboundedSender` of
  `(String, Value, oneshot::Sender<Result<Value>>)`.
- `pub async fn ask(name: String, data: Value) -> Result<Value>` — the outbound
  call from inside a job: send on the task-local sender, await the oneshot.
  `try_with`, not `with`: outside a job it must error, not panic.
- `pub fn begin<F>(lua: &Lua, future: F) -> LuaResult<LuaValue>` where
  `F: Future<Output = Value> + Send + 'static` — makes the channel, spawns
  `ASKS.scope(sender, future)` on `runtime()`, files the job under a fresh id,
  and returns its first step.
- `pub fn resume(lua: &Lua, args: &Value) -> LuaResult<LuaValue>` — takes
  `{id, value?, error?}`, completes the job's outstanding oneshot, returns the
  next step.
- Both go through one private `advance(lua, id, answer)` that **removes** the
  job from the map before any `block_on` (never hold the map lock across it)
  and then selects, `biased`, over: the join handle completing, the ask channel
  producing a call, and a 25 ms sleep.

Three steps come back to Lua:

| step | shape | meaning |
| --- | --- | --- |
| `call` | `{step="call", id, call, data}` | make this call and resume me |
| `wait` | `{step="wait", id}` | I have not finished; give the node back and resume me |
| `done` | `{step="done", reply}` | the JSON-RPC answer, or null for a notification |

The `wait` step is not decoration. Without it the trampoline deadlocks: two
messages of one instance both reach `Instance::session`'s
`tokio::sync::OnceCell`, the loser awaits the winner, and the loser's `answer`
would hold the node's Lua state forever while the winner's listener waits for
it to be given back. With `wait`, the loser's `answer` returns after 25 ms,
`init.lua` yields once, the winner runs, and the loser resumes. Keep the
timeout arm.

### `src/lib.rs`

- `answer` gains a `"resume"` arm delegating to `base::job::resume`.
- The `"message"` arm clones the `Arc<Service>`, owns `line` and `instance`,
  and calls `base::job::begin(lua, async move { service.message(&instance, &line).await.unwrap_or(Value::Null) })`.
  The future is `Send + 'static` — this compiles as written; no `service.rs`
  change is needed to make it so.
- The `Call` becomes `Arc::new(|key, args| base::job::ask(key, args).boxed())`.
- **`base::needs` must stop being the `Needs` closure.** It reads the base
  through the `ENTERED` thread-local, and a job runs off that thread, so from a
  job it returns the empty default and `tools/list` silently lists nothing.
  Snapshot it instead: a `static NEEDS: OnceLock<Mutex<Vec<String>>>`, written
  at the top of every `"message"` (on the base's thread, where it is legal),
  read by `with_needs(Arc::new(|| needs().lock()…clone()))`. Per message is
  still "read per use", so a changed composition still shows up. Acceptance box
  four exists because this is the one silent way to get this wrong.

### `init.lua`

The listener becomes the loop. It is the yieldable context, which is the whole
point: `cartridge.bail` called from here takes the yielding branch of `either`
(`cartridge.ctg/src/node/mod.rs:48-72`) instead of `wait()`'s blocking one.

```lua
cartridge.listen("mcp", function(args)
	local step = mcp.answer(args)
	while type(step) == "table" and step.step do
		if step.step == "done" then return step.reply end
		local resume = { op = "resume", id = step.id }
		if step.step == "call" then
			local ok, value = pcall(cartridge.bail, step.call, step.data)
			if ok then resume.value = value else resume.error = tostring(value) end
		else
			coroutine.yield()
		end
		step = mcp.answer(resume)
	end
	return step
end)
```

`{op="ready"}` still answers `nil`, which is not a table, so it falls out of the
loop untouched. A provider error becomes `resume.error`, which `ask` returns as
the `Err` the existing code already handles.

### Documentation

`.cartridge/docs/README.md:113-114` already states that
`notifications/cancelled` "invokes the named request's tool `cancel` op with
that call's own context". That sentence is what this change finally makes true,
so it needs no edit. `README.md` and `.cartridge/help.md` say nothing about the
answer path or cancellation (checked by grep), so neither needs updating.

## Why the three-line `create_async_function` fix does not apply here

A peer session (`cartridge-eb`) proved the same root cause in `pty.ctg` and
fixed it in three lines with no host change and no trampoline: mlua's `async`
feature, the fn becomes `async`, `create_async_function` instead of
`create_function`, dispatching through `runtime().spawn(...)`. That is a better
fix wherever it works. **It does not work here**, and the reason is a property
of `mcp.ctg`, not of the host.

Built and run, not argued (`$TMPDIR/an-cancel/work/mcp-async`, a third clone of
`1595a6f` carrying exactly that shape — `Cargo.toml` gains `"async"`, `answer`
becomes `async fn answer(lua: Lua, args: LuaValue)`, registered with
`lua.create_async_function(answer)`, the message spawned on `base::runtime()`;
`init.lua` untouched). It compiles in 5.57 s and the server answers. Then:

```
tools/list, with the surface pinned to tool.slow by config so `needs` is not
in the way, one profile, one set of fixtures, only the module differing:

  create_async_function shape : {"result":{"tools":[]}}
  this spec's trampoline      : {"result":{"tools":[{"name":"slow",…}]}}
```

The outbound call itself, asked directly from both positions:

```
{"inline":"Err(\"not on the base's thread\")","spawned":"Err(\"not on the base's thread\")"}
```

`pty.ctg` never calls back into its own node: `grep -rn 'base::bail|base::notify|cartridge.call_function|base::needs' pty.ctg/src/` returns
**nothing**, and `tool::dispatch` only spawns processes. `mcp.ctg` calls back
for *every* unit of work — `policy`, `sessions`, `tool.*` describe, `tool.*`
call, the cancel op — through `base::bail` → `with()` → `ENTERED`
(`src/base.rs:30-54`), the thread-local that `base::entered` pushes and that
only a thread the base called into has. `create_function` gives that thread;
`create_async_function` does not, and a `runtime().spawn` worker never could.
Both readings above are the same `Err`, so re-adding `entered` does not rescue
it either: it is a synchronous scope and cannot span an await whose future the
host's driver may poll anywhere.

The trampoline is what closes that gap. It does not try to reach the base from
an async context at all — it hands the call back out to the cartridge's own Lua
listener, which is already on the base's thread and is already yieldable.
`Cargo.toml` therefore needs no `async` feature, and no footprint widening
beyond the one test file is asked for.

## Acceptance

- [x] `mcp.answer` never waits on another cartridge on the base's thread: an
      outbound call leaves as a step and the listener in `init.lua` makes it,
      so the node is free for the duration of the call.
- [x] A `notifications/cancelled` for an in-flight `tools/call` reaches
      `notified` while that call's entry is still in `inflight`, and the tool's
      provider is called with `{"op":"cancel", context}` carrying that call's
      own context.
- [x] The running tool stops: an end-to-end test over a real `cartridge mcp`
      stdio bridge cancels a real in-flight `tools/call`, and the **tool's own
      answer** says it was stopped. The same test, run against the tree before
      this change, reports the completion it denies.
- [x] The tool surface survives the move off the base's thread: the same test's
      `tools/list` still lists the composed `tool.*` provider.
- [x] `cargo test --lib` still reports every test it reported before.

## Verify and Proof

Measured on this machine: the build block took 4 s into a cold
`target/a-cancelled-tool-call-verify`, the test block 2.5 s, and
`cargo test --lib` 10 s including its own compile — each far inside the 120 s
limit.

`CARTRIDGE_RUNTIME` names an already-built daemon. Nothing here builds
`cartridge.ctg`.

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/a-cancelled-tool-call-verify}"
cargo build
if [ ! -f "$CARGO_TARGET_DIR/debug/libmcp.dylib" ] && [ ! -f "$CARGO_TARGET_DIR/debug/libmcp.so" ]; then
	echo "the module did not build"
	exit 1
fi
```

```sh
# The base's thread must not be the one that waits for another cartridge, and
# the listener must be the one that calls out. Cheap structural guards only —
# the gate is the test block below.
if grep -qn 'block_on' src/lib.rs; then
	echo "src/lib.rs still waits for another cartridge on the base's own thread"
	exit 1
fi
if ! grep -qn 'cartridge.bail' init.lua; then
	echo "the listener does not make this cartridge's outbound calls"
	exit 1
fi
```

```test
run: CARGO_TARGET_DIR="$PWD/target/a-cancelled-tool-call-verify" CARTRIDGE_RUNTIME="${CARTRIDGE_RUNTIME:-/Users/feb/dev/cartridge/cartridge.ctg}" bun test ./.cartridge/tests/integration/cancel.test.ts --reporter=junit --reporter-outfile="$PRD_TEST_REPORT"
pass: a cancelled tools/call reaches the running tool
```

The unit suite has to be handed the two variables its shelling-out test reads,
or `initialized_live_client_inspects_real_policy_without_granting_writes` fails
for want of a binary — it fails that way on the unmodified tree too, so
without them this block would prove nothing about this change. The `ls` picks
whichever extension this platform built. Observed: `23 passed; 0 failed;
1 ignored` in 3 s.

```test
run: CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/a-cancelled-tool-call-verify}" CARTRIDGE_BIN="${CARTRIDGE_BIN:-/Users/feb/dev/cartridge/cartridge.ctg/target/debug/cartridge}" MCP_MODULE="$(ls "$PWD"/target/a-cancelled-tool-call-verify/debug/libmcp.dylib "$PWD"/target/a-cancelled-tool-call-verify/debug/libmcp.so 2>/dev/null | head -1)" cargo test --lib
pass: cancelling_a_call_reaches_the_tool_under_that_calls_own_identity
pass: two_instances_keep_separate_sessions_and_in_flight_calls
pass: an_empty_tool_list_follows_the_needs_and_is_described_on_every_list
pass: initialized_live_client_inspects_real_policy_without_granting_writes
```

## The gate, run both ways

The test is not a census and not a grep. It drives a real bridge and asserts on
the string the **fixture tool itself** returns, which is `stopped-on-cancel …`
only if the provider's `cancel` op ran while the call was still looping.

- With the change: `1 pass, 0 fail` in 2.27 s; the tool answered
  `stopped-on-cancel 280052`.
- Mutant — the same test file, unchanged, against `mcp.ctg` `1595a6f` with the
  old `src/lib.rs` and `init.lua`: `0 pass, 1 fail` in 4.94 s, with
  `Expected: "stopped-on-cancel" / Received: "ran-to-completion"`, the tool
  having run all 3 000 000 of its iterations.

The fixture tool parks on `coroutine.yield()` rather than a busy loop, because
this Lua sandbox is `StdLib::ALL_SAFE ^ IO ^ PACKAGE`
(`cartridge.ctg/src/lua/mod.rs:26`) — there is no sleep — and because a tool
that spins without yielding holds its *own* node and could not observe its own
cancel either. It is the same shape a real provider has: parked, not spinning.

The test composes its own `policy`, `sessions` and `tool.slow` fixtures inside
its temp profile and reaches into no sibling checkout, per
`@mcp/the-mcp-instances-fixture-composes-policy-without-reaching-across-the-boundary`.
