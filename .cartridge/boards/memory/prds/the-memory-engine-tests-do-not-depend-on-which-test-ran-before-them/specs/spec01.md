---
complexity: small
footprint:
  - src/util/src/lifecycle.rs
  - .cartridge/tests/unit/src/cartridge/engine_test.rs
---

# spec01 — the engine tests serialize on one latch and put the shutdown bit back after each drain

Base: memory.ctg 1351865 (HEAD; probed there on 2026-09-17 in a throwaway
worktree, see the attempt diff named below). No `needs`.

## Cause

Two process-wide mechanisms, both reached by `drain`, make one engine test's
result depend on which tests ran before or beside it:

1. **The one-way latch leaks.** `drain` (src/cartridge/src/lib.rs:552) ends in
   `engine.shutdown()` when a service opened its engine, and
   `Engine::shutdown` (src/commands/src/memory.rs:50-54) calls
   `util::lifecycle::begin_shutdown()`, which swaps the process-global
   `SHUTTING_DOWN` static to true (src/util/src/lifecycle.rs:75) and never
   clears it. `src/util/src/lifecycle.rs:221-230` documents the latch as
   "one-way on purpose" for production. The test binary is one process, so
   every later bridge-using test is refused with
   `shutting down: the daemon refused this request, retry against a fresh one`
   (src/llm/src/llm.rs:837) — observed twice: serial run, the next test
   (`ingest_query_tool_and_context_reach_one_engine`, engine_test.rs:39)
   failed with exactly that string; parallel run of the four engine tests
   alone, the same test failed with it at engine_test.rs:46.
2. **The drain write blocks concurrent tests.** `drain` takes
   `CALLS.write().await` (src/cartridge/src/lib.rs:553) while a parked call
   in the same or another test holds `CALLS.read()` inside
   `spawn_blocking` (src/cartridge/src/lib.rs:345-350). tokio's RwLock is
   write-preferring, so any *further* read queues behind the pending write
   even though the first reader is still parked. In the full parallel suite
   this starved the health call in
   `health_overtakes_blocked_ingestion_and_dispose_drains_it` until its
   2 s timeout fired: panic `health is independent of ingestion: Elapsed(())`
   at engine_test.rs:137 — the failure the coordinator recorded on
   2026-09-17.

Both were reproduced at 1351865 (commands and exit codes in the analyst
report). The suite is red at HEAD in every shape: parallel full suite
(20/1, `Elapsed(())`), serial (20/1, refusal at engine_test.rs:39),
engine-tests-only parallel (3/1, refusal at engine_test.rs:46).

The fix machinery already exists in the footprint:
`util::lifecycle::shutting_down_for_tests()` (src/util/src/lifecycle.rs:247)
takes the shipped `SHUTDOWN_LATCH` for write, flips the bit, and its
`ShutdownForTests::drop` (src/util/src/lifecycle.rs:239-243) stores the bit
back to false. Ten other test files in this repo already use exactly this
protocol (tick_test.rs:611, llm_test.rs:645, server_admin_test.rs:541,
cli_test.rs:200, commands_route tests.rs:67). The engine tests are the only
drain callers that never use it. **lifecycle.rs itself needs no change**;
the two footprint paths are kept because the PRD names them and the helper
the tests call is declared there.

## Steps

1. In `.cartridge/tests/unit/src/cartridge/engine_test.rs`, add a test-file
   mutex and a drain wrapper (reference diff, applied and fully validated at
   1351865:
   `prd.ctg/.cartridge/boards/memory/.state/loop/the-memory-engine-tests-do-not-depend-on-which-test-ran-before-them/analyst-1/attempt-engine-test-serialize-and-relatch.diff`):

   - `static ONE_AT_A_TIME: tokio::sync::Mutex<()> = tokio::sync::Mutex::const_new(());`
   - `async fn drain_without_leaking_liveness(status: Option<Arc<status::Tracker>>)`,
     which records whether the service had opened its engine, calls the real
     `drain(status).await`, then — if an engine was open — asserts
     `util::lifecycle::is_shutting_down()` (this is the drain/dispose
     shutdown assertion the PRD requires: the one-way latch is what makes a
     production `dispose` refuse later work), and finally takes
     `util::lifecycle::shutting_down_for_tests().await` and drops it, which
     restores liveness for the sibling tests.

2. Replace the three `drain(...)` call sites (after the first test's context
   read, in `a_corrupt_store_is_refused_without_rewriting_it`, and the
   spawned drain in `health_overtakes...`) with
   `drain_without_leaking_liveness(...)`. The corruption test's service
   never opens an engine, so its wrapper takes no latch and asserts nothing.

3. Add `let _one = ONE_AT_A_TIME.lock().await;` as the first line of all
   four `#[tokio::test]` functions. This removes the cross-test lock cycle
   (a parked read in one test can no longer queue another test's drain
   write ahead of a third call). It does not serialize them against the rest
   of the binary: only these four tests open stores.

4. Replace the stale comment in
   `a_second_local_service_is_refused_and_the_attached_one_never_asks_for_the_writer`
   (engine_test.rs:279-281, "No `drain` here: it calls
   `util::lifecycle::begin_shutdown`...") — the accurate reason is that a
   drain would begin the process shutdown; `drop(owner)` releasing the
   writer is what that test is about.

Do not change `lifecycle.rs`, `drain`, `Engine::shutdown` or any other
caller: the latch's one-way shape is correct in production, and the shipped
test protocol exists precisely so tests do not have to reach into the
static. Do not add `--test-threads` flags or `#[serial]` annotations; the
mutex is in-file and owns only what these four tests actually contend on.

## Acceptance

- [x] `cargo test -p memory_cartridge --lib` exits 0 from a clean checkout,
      with no test skipped, ignored or filtered to achieve it.
- [x] The suite passes with `--test-threads=1` and with the engine tests run
      alone in the default parallel harness; the order and thread count do
      not change the result.
- [x] `health_overtakes_blocked_ingestion_and_dispose_drains_it` still
      asserts the shutdown its drain was written for — the wrapper asserts
      `util::lifecycle::is_shutting_down()` after a real drain of an opened
      engine — and its existing asserts (`dispose must drain ingestion`,
      `dispose completes after ingestion`) are unchanged.
- [x] No production code changed: the diff touches only
      `.cartridge/tests/unit/src/cartridge/engine_test.rs`.

## Verify and Proof

<!--
Engine facts honoured: `sh -eu -c`, 120 s, runs twice (lane, then repo);
paths relative to the repo root; no `cd` to an absolute checkout; every
cargo command pins CARGO_TARGET_DIR (pass 2 runs in the live checkout and
the host hot-restarts on target/debug changes); no block writes inside the
footprint; negations use `if grep -qn ...; then exit 1; fi`, never `! grep`,
which is inert under `set -e`. Budget: cold build measured 24.9 s
(cargo test --no-run, empty target dir), each suite run 0.4 s, so all three
cargo commands in block 1 fit the 120 s limit with room; the engine-only and
serial runs reuse the same profile. The negative control — block 1 on
unmodified HEAD — exits 1 on its first grep.
-->

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/engine-tests-order-verify}"
f=.cartridge/tests/unit/src/cartridge/engine_test.rs
grep -q "ONE_AT_A_TIME" "$f"
grep -q "drain_without_leaking_liveness" "$f"
grep -q "is_shutting_down" "$f"
if grep -qn "begin_shutdown\`, which is a" "$f"; then echo "the stale drain comment survives in $f"; exit 1; fi
cargo test -p memory_cartridge --lib
cargo test -p memory_cartridge --lib -- --test-threads=1
cargo test -p memory_cartridge --lib engine_tests::
```

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/engine-tests-order-verify}"
log="$(mktemp -t engine-drain-verify)"
cargo test -p memory_cartridge --lib > "$log" 2>&1 || { cat "$log"; exit 1; }
for t in ingest_query_tool_and_context_reach_one_engine a_corrupt_store_is_refused_without_rewriting_it health_overtakes_blocked_ingestion_and_dispose_drains_it a_second_local_service_is_refused_and_the_attached_one_never_asks_for_the_writer; do
	grep -q "$t ... ok" "$log" || { cat "$log"; exit 1; }
done
grep -qE "^test result: ok\. 21 passed; 0 failed" "$log" || { cat "$log"; exit 1; }
```