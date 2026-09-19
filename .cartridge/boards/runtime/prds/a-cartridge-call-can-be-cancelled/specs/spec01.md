---
complexity: moderate
footprint:
  - "src/transport/cartridge.rs"
  - "src/transport/rpc.rs"
  - "src/transport/tests/cartridge.rs"
---

# spec02 — an abandoned call cancels the work it started

Base revision: `d1692932449c89106bb1928b717146ee8b0083a8`.

`src/node/mod.rs` is in the PRD footprint and is **not needed by this spec**: the
Lua listener is an ordinary future (`src/node/mod.rs:226-235`) and dropping it at
an await point needs nothing on the Lua side. This narrows nothing about the
footprint itself — `feet()` is a union of the PRD's and every published spec's,
so `src/node/mod.rs` stays reserved and still counts in `clash()` regardless of
what any one spec touches. `src/transport/tests/cartridge.rs` is added here
instead — `feet()` (`prd.ctg/src/planner.ts:5-9`) unions the PRD footprint with
every published spec's, so this declaration is what lets the gate's own test
file be written and collected.

## What is true today

- The caller's bound is inert. `src/transport/cartridge.rs:389-395` wraps the RPC
  in `tokio::time::timeout`; expiry drops the future and the only cleanup is
  `impl Drop for Waiting` (`src/transport/rpc.rs:292-305`), which removes the id
  from the caller's own pending map. No frame leaves the process.
- The provider cannot hear a cancel. `serve` discards every non-request message
  (`cartridge.rs:820-823`); `handle` answers anything but
  `apply`/`directory`/`dispose`/`event` with `METHOD_NOT_FOUND` (`:957-961`).
- The permit is held to completion. `IN_FLIGHT = 64` (`:27`), acquired `:851`,
  dropped only after `handle` returns (`:855-858`).
- The work cannot stop. `:944-948` runs the listener as
  `spawn_blocking(|| runtime.block_on(listener(data)))`; aborting a started
  blocking task is a no-op.

## Change

1. `src/transport/rpc.rs` — add `Request::id() -> Option<u64>`, and make
   `Waiting::drop` emit a `cancel` notification naming the id **only** when
   removing the pending entry actually succeeded. That condition is exact:
   `dispatch` (`rpc.rs:337-341`) removes the id when a response arrives, so a
   surviving entry *is* an abandoned call — a timeout, a dropped future, a turn
   that ended. One path covers all three; no new caller API.
2. `src/transport/cartridge.rs` — `serve` keeps a
   `HashMap<u64, CancellationToken>` beside `in_flight`, registers a token per
   spawned `handle`, removes it when that handle returns, and fires the matching
   token on an incoming `cancel` notification.
3. `src/transport/cartridge.rs` — `handle` takes that token and, in the `event`
   arm, selects it against the listener **inside** the existing
   `spawn_blocking(move || runtime.block_on(...))`.

### What the caller observes, and the two edges

- The cancelled call is answered `Err(application("cancelled"))`. The caller has
  already removed its pending entry, so `dispatch` (`rpc.rs:337-341`) finds no
  waiter and drops it: the caller still observes `Outcome::TimedOut`
  (`cartridge.rs:391-393`), unchanged. Replying explicitly matters anyway,
  because otherwise `impl Drop for Request` (`rpc.rs:117-129`) pushes
  `request dropped without a reply` — an untrue INTERNAL_ERROR in any trace that
  reads the wire.
- `Waiting::drop` also runs on the send-failure path (`rpc.rs:251-253`): the
  frame could not be queued, the entry is still pending, so a cancel is pushed at
  a connection that just refused a frame. `Inner::push` (`rpc.rs:132-143`)
  returns false and closes; the `let _ =` is the whole handling. The other early
  return (`:244-246`) happens before `Waiting` exists, so it emits nothing.

### The deadlock the PRD flags is not reopened — and the ceiling on that claim

The comment at `:939-941` protects one invariant: a listener takes its node's Lua
lock synchronously (`src/node/mod.rs:28-33`, `block_in_place` via `wait()`), so it
must never run on a tokio worker. The `select!` goes *inside* `block_on`, leaving
`spawn_blocking(move || runtime.block_on(...))` intact — the listener never moves
onto a worker, no lock is added, no handle is aborted.

MEASURED CEILING, stated rather than overclaimed: that invariant is **not** held
by an executed gate. A tree that awaits the listener directly on the worker —
the exact shape the comment forbids — passes every test in this spec (measured,
block exit 0; the `wedge` row below). `a_listener_that_blocks_does_not_park_the_only_worker`
encodes the invariant and would catch a gross violation, but it did not catch
that one: with one worker the ping races the listener's first poll, and the race
went the wrong way. Holding this invariant still rests on review of the `event`
arm, not on the gate. A reviewer should read that arm.

### Other ceilings

- Cancellation drops the listener's future at its **next await point**. A Lua
  listener spinning without awaiting is not stopped, and should not be: that is
  `CARTRIDGE_LUA_INSTRUCTION_BUDGET` (`src/node/mod.rs:23`). Listeners registered
  through `cartridge.listen` are invoked with `call_async` (`node/mod.rs:229-232`),
  so nested `bail`/`gather` take the yielding branch of `either`
  (`node/mod.rs:54-73`) and are cancellable; the blocking `wait()` branch is not,
  and a listener does not reach it.
- Only the `event` arm honours the token. `apply`/`directory`/`dispose` run to
  completion — host lifecycle, not calls.
- The permit returns when `handle` returns, i.e. when the select resolves.
  Between the cancel arriving and the listener's next await, it is still held.

## Acceptance

- [x] A call whose bound expires reaches the provider as a cancellation: the
      listener's own future is dropped rather than left running to completion.
- [x] A listener parked on *another cartridge's* answer is released by that
      cancellation.
- [x] The in-flight permit of a cancelled call returns immediately, so a later
      call on the same connection is served while the cancelled work is gone.
- [x] The whole library still passes, and each gate observes something no
      half of the change can satisfy on its own.

## Verify and Proof

<!--
Engine facts per prd.ctg/.cartridge/templates/spec.md: `sh -eu -c`, 120 s, run
once with cwd = the lane and again with cwd = `repo`, paths relative to the repo
root, no `cd` to an absolute checkout, isolated CARGO_TARGET_DIR. Every write is
under CARGO_TARGET_DIR, never in the footprint.

Step 3 is the defence against a gate with the right name and a body that
observes something else. "Fails without the change" alone is satisfied by ANY
difference between the trees, including a one-character constant — measured, the
`const` row. Requiring failure under each half separately makes the observation
depend on both files, which a constant in one of them cannot do.

`--test-threads=1` is not decoration: the three tests below hold threads on
purpose, and `a_listener_that_does_not_answer_reaches_the_log` captures through a
thread-local subscriber. Measured: 1 failure in 3 parallel runs, 0 in 3 serial
runs, against a pristine HEAD that is 3 of 3 either way. A flaky gate gets
deleted; this one is serial.
-->

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/cancel-verify}"
# The engine injects no environment (prd.ctg/src/lifecycle.ts verify()), so
# BASE must default. The pinned sha is this spec's own stated base revision:
# an ancestor of HEAD in both passes (pass 1: the lane worktree branched from
# it; pass 2: repo fast-forwarded past it), so `git archive "$BASE"` resolves
# it from the shared object store regardless of which tree is checked out.
BASE="${BASE:-d1692932449c89106bb1928b717146ee8b0083a8}"
W="$CARGO_TARGET_DIR/cancel"
GATE=a_cancelled_call_drops_the_listener_and_frees_its_permit
NESTED=a_cancelled_call_stops_a_listener_waiting_on_another_cartridge
WORKER=a_listener_that_blocks_does_not_park_the_only_worker
mkdir -p "$W"

# 1. The whole library, serially. A gate that only ever runs its own test lets a
#    change contradicting the rest of the transport collect green. Serial because
#    the three tests below hold threads on purpose, and the suite's thread-local
#    log capture is not robust against that: measured 1 failure in 3 parallel
#    runs, 0 in 3 serial runs, against a pristine HEAD that is 3 of 3 either way.
cargo test --lib -- --test-threads=1 > "$W/suite.log" 2>&1 || {
	tail -40 "$W/suite.log" >&2
	echo "the library suite does not pass" >&2
	exit 1
}

# 2. Each named test must appear in that run and pass. Read from the suite's own
#    output: a filter that matches nothing is a green cargo run.
for name in "$GATE" "$NESTED" "$WORKER"; do
	grep -q "::$name \.\.\. ok" "$W/suite.log" || {
		echo "$name did not run and pass in the library suite" >&2
		exit 1
	}
done

# 3. The two cancellation tests must depend on BOTH halves of the change. They
#    are transplanted onto the revision this work started from with nothing
#    applied, then with one source file applied at a time. An observation that
#    survives a half-application is not observing cancellation; it is observing
#    some other difference between the two trees.
plant() {
	rm -rf "$1"
	mkdir -p "$1"
	git archive "$BASE" | tar -x -C "$1"
	cp src/transport/tests/cartridge.rs "$1/src/transport/tests/cartridge.rs"
	for file in $2; do cp "$file" "$1/$file"; done
}
run_there() {
	( cd "$1" && cargo test --lib "$2" ) > "$3" 2>&1 || true
}

plant "$W/none" ""
plant "$W/rpc" src/transport/rpc.rs
plant "$W/cartridge" src/transport/cartridge.rs
for name in "$GATE" "$NESTED"; do
	# Nothing applied: it must BUILD there and fail. A transplant that does not
	# compile prints no verdict line, and a test leaning on surface the change
	# introduces cannot be told from one that observes nothing.
	run_there "$W/none" "$name" "$W/none-$name.log"
	grep -q 'test result: FAILED' "$W/none-$name.log" || {
		tail -40 "$W/none-$name.log" >&2
		echo "$name does not discriminate: without the change it must build and fail" >&2
		exit 1
	}
	# One half applied, either half: it must not pass. An incoherent half may
	# fail to build, which is a legitimate outcome here; passing is not.
	for half in rpc cartridge; do
		run_there "$W/$half" "$name" "$W/$half-$name.log"
		if grep -q 'test result: ok' "$W/$half-$name.log"; then
			echo "$name passes with only $half applied, so it does not observe the behaviour" >&2
			exit 1
		fi
	done
done
```

## The three tests

Add to `src/transport/tests/cartridge.rs`. The observation in the first two is a
guard the listener's *own future* owns: `Bell::drop` can only run when that
future is dropped, and neither listener can finish inside the test's window.
Nothing under `src/transport/` can reach those counters.

```rust
#[tokio::test]
async fn a_cancelled_call_drops_the_listener_and_frees_its_permit() {
	struct Bell(Arc<AtomicUsize>);
	impl Drop for Bell {
		fn drop(&mut self) {
			self.0.fetch_add(1, Ordering::SeqCst);
		}
	}
	let dir = tempfile::tempdir().unwrap();
	let (a_directory, b_directory) = directories(dir.path());
	let dropped = Arc::new(AtomicUsize::new(0));
	let apply: Apply = {
		let dropped = dropped.clone();
		Box::new(move |ctx: Ctx, _| {
			let dropped = dropped.clone();
			async move {
				ctx.on("slow", move |_| {
					let dropped = dropped.clone();
					async move {
						let _bell = Bell(dropped);
						tokio::time::sleep(Duration::from_secs(3)).await;
						Ok(json!("late"))
					}
				});
				ctx.on("ping", |data| async move { Ok(json!({ "pong": data })) });
				Ok(())
			}
			.boxed()
		})
	};
	let _a = start(&dir.path().join("a.sock"), apply).await;
	let b = start(&dir.path().join("b.sock"), cartridge_b()).await;
	apply_directory(&dir.path().join("a.sock"), "a", &a_directory).await;
	apply_directory(&dir.path().join("b.sock"), "b", &b_directory).await;

	// `slow` is bound at 50 ms by `directories`; every one of these expires.
	let sends = (0..IN_FLIGHT).map(|_| b.ctx.bail("slow", json!(null)));
	for outcome in futures::future::join_all(sends).await {
		assert!(outcome.is_err(), "the bound must expire: {outcome:?}");
	}
	tokio::time::sleep(Duration::from_millis(300)).await;
	assert_eq!(
		dropped.load(Ordering::SeqCst),
		IN_FLIGHT,
		"every expired call must have stopped the work it started"
	);
	// `ping` declares no bound, so it can only answer if the permits came back.
	let answered = tokio::time::timeout(Duration::from_secs(1), b.ctx.bail("ping", json!(1))).await;
	assert_eq!(answered, Ok(Ok(Some(json!({ "pong": 1 })))));
}

#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn a_cancelled_call_stops_a_listener_waiting_on_another_cartridge() {
	// The hazard this PRD owns is about a listener parked on *another
	// cartridge's* answer. This is that listener, cancelled mid-call.
	struct Bell(Arc<AtomicUsize>);
	impl Drop for Bell {
		fn drop(&mut self) {
			self.0.fetch_add(1, Ordering::SeqCst);
		}
	}
	let dir = tempfile::tempdir().unwrap();
	let (mut a_directory, b_directory) = directories(dir.path());
	a_directory.sends.push("ping".to_owned());
	let dropped = Arc::new(AtomicUsize::new(0));
	let entered = Arc::new(AtomicUsize::new(0));
	let apply: Apply = {
		let (dropped, entered) = (dropped.clone(), entered.clone());
		Box::new(move |ctx: Ctx, _| {
			let (dropped, entered, nested) = (dropped.clone(), entered.clone(), ctx.clone());
			async move {
				ctx.on("slow", move |_| {
					let (dropped, entered, nested) =
						(dropped.clone(), entered.clone(), nested.clone());
					async move {
						let _bell = Bell(dropped);
						// Parked on another cartridge's answer, which never comes.
						entered.fetch_add(1, Ordering::SeqCst);
						// The nested call is itself bounded, so a tree that never
						// cancels still finishes instead of wedging the gate.
						let _ = tokio::time::timeout(
							Duration::from_millis(900),
							nested.bail("ping", json!(null)),
						)
						.await;
						Ok(json!("late"))
					}
				});
				ctx.on("ping", |_| async move {
					tokio::time::sleep(Duration::from_millis(1200)).await;
					Ok(json!("eventually"))
				});
				Ok(())
			}
			.boxed()
		})
	};
	let _a = start(&dir.path().join("a.sock"), apply).await;
	let b = start(&dir.path().join("b.sock"), cartridge_b()).await;
	apply_directory(&dir.path().join("a.sock"), "a", &a_directory).await;
	apply_directory(&dir.path().join("b.sock"), "b", &b_directory).await;

	assert!(b.ctx.bail("slow", json!(null)).await.is_err(), "the bound must expire");
	tokio::time::sleep(Duration::from_millis(400)).await;
	assert_eq!(entered.load(Ordering::SeqCst), 1, "the listener must have reached its nested call");
	assert_eq!(
		dropped.load(Ordering::SeqCst),
		1,
		"a listener parked on another cartridge must be released by the cancel"
	);
}

#[tokio::test(flavor = "multi_thread", worker_threads = 1)]
async fn a_listener_that_blocks_does_not_park_the_only_worker() {
	// The invariant the comment above the listener's spawn guards: a listener
	// blocks synchronously, so if it ever runs on a worker it takes the runtime
	// down with it. One worker makes that observable instead of argued.
	let dir = tempfile::tempdir().unwrap();
	let (a_directory, b_directory) = directories(dir.path());
	let apply: Apply = Box::new(move |ctx: Ctx, _| {
		async move {
			ctx.on("slow", |_| async move {
				std::thread::sleep(Duration::from_millis(600));
				Ok(json!("late"))
			});
			ctx.on("ping", |data| async move { Ok(json!({ "pong": data })) });
			Ok(())
		}
		.boxed()
	});
	let _a = start(&dir.path().join("a.sock"), apply).await;
	let b = start(&dir.path().join("b.sock"), cartridge_b()).await;
	apply_directory(&dir.path().join("a.sock"), "a", &a_directory).await;
	apply_directory(&dir.path().join("b.sock"), "b", &b_directory).await;

	let busy = tokio::spawn({
		let ctx = b.ctx.clone();
		async move { ctx.bail("slow", json!(null)).await }
	});
	tokio::time::sleep(Duration::from_millis(100)).await;
	let answered = tokio::time::timeout(Duration::from_millis(300), b.ctx.bail("ping", json!(2))).await;
	assert_eq!(
		answered,
		Ok(Ok(Some(json!({ "pong": 2 })))),
		"a blocking listener must not stop the runtime from serving anything else"
	);
	let _ = busy.await;
}
```

## Measured, before this spec was handed back

Seven trees, all cut from `d169293`, one shared out-of-repo `CARGO_TARGET_DIR`,
each block run exactly as the engine runs it (`sh -eu -c`). Exit codes observed.

| tree | what it is | block exit | rejected by |
| --- | --- | --- | --- |
| **reference** | the change above + the three tests | **0** | — (54 s) |
| base | `d169293` untouched + the three tests | **1** | step 1: the two cancellation tests fail, `161 passed; 2 failed` |
| surface | `Request::id`, a `cancels` map, a `cancel` notification arm, the token threaded into `handle` — every token present, none wired | **1** | step 1: same two, `161 passed; 2 failed` |
| inert | `d169293` + both gates with the right names and empty bodies | **1** | step 3: `does not discriminate: without the change it must build and fail` |
| **const** (the reviewer's cheat) | `IN_FLIGHT` 64→65, both gate bodies `assert_eq!(IN_FLIGHT, 65, "...")`, nothing else | **1** | step 3 partial: `passes with only cartridge applied, so it does not observe the behaviour` |
| **broken** | reference + `Semaphore::new(IN_FLIGHT * 2)`, an unrelated contradiction | **1** | step 1: `a_connection_runs_at_most_its_in_flight_limit_at_once ... FAILED` |
| **wedge** | reference, but the listener awaited on the worker — the hazard reopened | **0** | **NOT REJECTED — see the ceiling above** |

Cost: 54 s for the reference block with warm deps, 36–49 s for the others,
against the engine's 120 s limit. The serial suite alone is ~35 s. This project
sets `rustc-wrapper = "kache"` in `~/.cargo/config.toml`, so a genuine
compilation-cache miss would be slower than any of these numbers and the 120 s
limit is the real ceiling.

`cargo fmt` reshapes two of the reference hunks; run it.
