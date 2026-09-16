---
complexity: small
footprint:
  - .cartridge/tests/unit/src/cartridge/engine_test.rs
---

# spec01 — pin memory's one writer and the loop that belongs to it

Base: memory.ctg `5097a83` ("Keep every Vamana node reachable: prune over one
occlusion factor").

## Option chosen

**No production change. Add the regression test that the outcome is missing.**

The audit's premise holds at the level it was written — a second *composed*
memory node over one data dir is refused with exactly
`another memory writer holds this data dir` — and the PRD's own reading is
right: nothing in memory.ctg has to change for the one daemon. Traced end to
end:

- The lock is one flock on `<data_dir>/writer.lock`, taken by
  `store::lock::acquire` (`src/store/core/src/lock.rs:99-130`) and released by
  dropping `WriterLock` (`:27-38`) — so by process exit, kill included. Only
  `WouldBlock` becomes `LockError::Held` (`:112-120`); the message the audit
  quotes is `:53-56`. `try_lock_patiently` (`:78-95`) retries a bounded 100 ms
  so an inherited fork descriptor is not mistaken for a live writer.
- The cartridge takes it once, for the node's lifetime:
  `commands::memory::Engine::open` (`src/commands/src/memory.rs:14-15`) acquires
  it as `"cartridge memory"` and `Engine._writer` holds it (`:5-9`). The node
  has exactly one `Engine`: `SERVICE` is one process-global
  (`src/cartridge/src/lib.rs:360`) and the engine sits in a
  `OnceCell` on its `Tracker` (`src/cartridge/src/status.rs:54`), opened through
  `get_or_try_init` under `INITIALIZATION` (`src/cartridge/src/lib.rs:318-338`).
- **The condensing loop is owned by the writer, structurally.**
  `spawn_ledger` (`src/commands/src/memory.rs:59-81`) is called from exactly one
  place — the last line of `Engine::open` (`:44`), after the lock — and it is the
  only 60 s / 900 s rollover scheduler in the repo. A node that is refused the
  lock returns `Err` from `Engine::open` and gets no `Engine`, so it schedules no
  pass. The 5-minute import hold-off is `IMPORTED_AT` + `IMPORT_QUIET_MS`
  (`src/rpc/src/ledger.rs:32-36`, `:725`, `:746-751`), and `PASS`
  (`:30-31`) keeps the loop and an explicit `rollover` from condensing one unit
  twice. Both are process statics; with one engine per process they are exactly
  per-store, and the one daemon is what makes that true.
- **The escape hatch is already closed.** memory.ctg has an attached shape:
  `ServiceConfig::Attached` (`src/cartridge/src/lib.rs:23-29`), chosen when the
  `owner` setting is a table (`:31-92`). Its calls go straight out over
  `memory_transport::owner::read_observed` (`:300-312`) and its status probe over
  the same transport (`src/cartridge/src/status.rs:208-224`); neither path ever
  reaches `status.engine` or `store::lock`. So attached memory does **not** take
  the writer lock read-only — the PRD's "if any memory path still assumes
  process-exclusivity beyond the file lock" turned up nothing to fix.
- Nothing else in memory.ctg assumes exclusivity beyond the file lock. Every
  other `acquire` call site is an admin command that is *supposed* to refuse
  against a live daemon (`src/commands/src/commands_gc.rs:10`,
  `commands_reembed.rs:18`, `commands_export.rs:164`, `:202`,
  `commands_hub.rs:93`, `:156`, `:291`, `commands_check.rs:260`,
  `commands_graph_ops.rs:341`, `:437`, `:702`, `commands_admin_compact.rs:13`,
  `:38`, `commands_queue_cmd.rs:112`, `commands_ingest_cmd.rs:158`,
  `lib.rs:718`), and `commands_serve.rs:71-100` is the standalone `memory daemon`,
  which is not what the project daemon composes.

What is missing is the proof. `.cartridge/tests/unit/src/store/core/src/tests/lock_test.rs`
pins the lock primitive well (second acquire refused and named, `:9-29`; a stale
file is not the lock, `:31-45`; two names for one dir are one lock, `:74-100`),
and `commands_writer_boundary_test.rs` pins the two-process write boundary. But
nothing pins the property this PRD is about: that the *cartridge service* is the
one writer, that a refused service opens no engine (and therefore no second
condensing loop), and that the attached shape never asks for the lock. A change
that opened an engine on the attached path, or that decoupled the engine from
the data dir's lock, would pass the whole suite today. This spec pins it.

## Steps

1. `.cartridge/tests/unit/src/cartridge/engine_test.rs`: append
   `a_second_local_service_is_refused_and_the_attached_one_never_asks_for_the_writer`
   (`#[tokio::test(flavor = "multi_thread", worker_threads = 4)]`), reusing the
   file's `settings`, `service_for`, `call` helpers and
   `test_support::spawn_http`. Prototype in `attempt-1.patch`, which passes
   unmodified against `src/`:
   - A local service ingests; assert its engine is open and
     `store::lock::observe(&dir) == Held`, then `query` it back for `Cedar` —
     ingest, query and ledger all off the one engine, which is what box 2 says
     (review round 1, finding 4). The `query` goes here, right after the ingest,
     not after the refusal: placed late it becomes a second victim of the
     process-wide `SHUTTING_DOWN` static below (observed `19 passed; 2 failed`,
     `"shutting down: the daemon refused this request"`), and the package
     baseline has to stay 20/1.
   - A **second** local `Service` over the same dir, called on the ledger path
     the proxy uses (`{"op":"ledger","action":"status"}`): the error contains
     `another memory writer holds this data dir`, and
     `second.status.engine.get().is_none()` — no engine, so no second condensing
     loop.
   - The first service still answers `ledger status` after the refusal.
   - An **attached** `Service` built from `service_configuration` with an `owner`
     endpoint that nothing listens on, over the same held dir: its error must not
     contain `another memory writer`, it opens no engine, and the lock is still
     the first service's.
   - End with `drop(owner)`, **not** `drain(...)`: `drain` calls
     `util::lifecycle::begin_shutdown`, a process-wide static that strands the
     sibling tests in this binary (see Remaining risk).
2. Nothing else. No change under `src/`. If a step wants to touch `src/`, stop
   and report: the behaviour is already correct and the diff would be churn.

## Acceptance

- [x] memory.ctg's share of "exactly one memory node, no
      `another memory writer holds this data dir`": the cartridge takes the
      writer lock once in `Engine::open` and holds it for the node's lifetime, a
      second local service over the same data dir is refused with that exact
      message and opens no engine, and the attached shape never asks for the lock
      at all. (The daemon-wide count of nodes and processes is not observable
      from this repo; it is delivered by the done sibling
      `an-instance-attaches-to-the-daemon-and-never-composes-silently` and
      re-proven composed by
      `the-composed-acceptance-test-proves-one-daemon-one-node-per-cartridge-and-attached-instances`.)
- [x] Two callers of the one node see one store: the writer serves ingest, query
      and ledger from a single `Engine`, and a second service that would have
      been the "other instance" gets no engine of its own to diverge in. (The
      cross-instance `ingest`-then-`query` round trip runs through cartridge.ctg's
      host attach, not through memory.ctg, and belongs to the composed test.)
- [x] The condensing loop belongs to the writer: `spawn_ledger` is called from
      exactly one place, the end of `Engine::open`, after the lock is taken and
      into an `Engine` that holds it — so a service refused the lock, and an
      attached service, run no condensing pass. (`{"op":"ledger","action":"status"}`
      reports only per-tier row and byte counts, `src/rpc/src/ledger.rs:289-297`;
      it names no node, so "shows the daemon's one node doing the condensing" is
      not answerable from that reply in any repo without a new field.)

## Verify and Proof

```sh
# The lane is a lone memory.ctg worktree; src/cartridge/Cargo.toml reaches
# ../../../memo.ctg/evidence, which resolves to a sibling of the checkout.
[ -d ../memo.ctg ] || ln -sfn "${MEMO_CTG:-/Users/feb/dev/cartridge/memo.ctg}" ../memo.ctg
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/memory-one-writer-verify}"
mkdir -p "$CARGO_TARGET_DIR"
cargo test -p memory_cartridge --lib \
  a_second_local_service_is_refused_and_the_attached_one_never_asks_for_the_writer \
  2>&1 | tee "$CARGO_TARGET_DIR/one-writer.log"
# A filter that names a missing, renamed or #[ignore]d test exits 0 with
# "running 0 tests"; only the summary proves this test ran (finding 2).
# (`--exact` would need the `engine_tests::` module path and filters everything
# out without it — the summary grep is what makes the block non-vacuous.)
grep -q 'test result: ok\. 1 passed; 0 failed' "$CARGO_TARGET_DIR/one-writer.log"
```

```sh
# The writer is taken once, in Engine::open, and held for the node's lifetime.
test -f src/commands/src/memory.rs
grep -q '_writer: store::WriterLock,' src/commands/src/memory.rs
grep -q 'store::lock::acquire(&cfg.data_dir, "cartridge memory")' src/commands/src/memory.rs
# The condensing loop has exactly one CALL SITE in the repo — a file count would
# pass a second `spawn_ledger(...)` added inside memory.rs — and that call site
# is the last statement of Engine::open. Every guard here is positive: `set -e`
# ignores a `!`-prefixed command, so `! grep ...` can never fail a block.
test "$(grep -rn 'spawn_ledger(' src --include=*.rs | grep -vc 'fn spawn_ledger(')" = 1
grep -A1 'spawn_ledger(&server);' src/commands/src/memory.rs | grep -q 'Ok(Self {'
# The attached shape still exists and the regression that pins it is present.
test -f src/cartridge/src/lib.rs
grep -q 'ServiceConfig::Attached' src/cartridge/src/lib.rs
test -f .cartridge/tests/unit/src/cartridge/engine_test.rs
grep -q 'a_second_local_service_is_refused_and_the_attached_one_never_asks_for_the_writer' \
  .cartridge/tests/unit/src/cartridge/engine_test.rs
```

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/memory-one-writer-verify}"
cargo fmt --check
```

## Remaining risk

- `cargo test -p memory_cartridge --lib` is **already red at `5097a83`**, with or
  without this change: `dispose`/`drain` sets the process-wide
  `util::lifecycle::SHUTTING_DOWN` (`src/util/src/lifecycle.rs:30`), so whichever
  engine test runs after `health_overtakes_blocked_ingestion_and_dispose_drains_it`
  fails with `shutting down: the daemon refused this request`. Baseline 19
  passed / 1 failed, with this test 20 passed / 1 failed — the same one. The
  Verify block therefore names the single test. Fixing the suite's shared
  lifecycle static is a separate, unrelated PRD.
- The first Verify block writes `../memo.ctg` when it is missing. That is outside
  the repo and outside the footprint; in pass 2 the sibling already exists and
  the line is a no-op. If the collector already seeds lane siblings, the line
  costs nothing.
- `PASS` and `IMPORTED_AT` (`src/rpc/src/ledger.rs:30-36`) are process statics.
  Correct for one engine per process, which `SERVICE` and the engine `OnceCell`
  guarantee. If memory is ever composed twice in one node over two data dirs,
  they become wrong — out of scope, and the one daemon makes it less likely, not
  more.
- The attached leg of the test uses a dead endpoint on purpose: what it pins is
  which error comes back and that the lock is untouched, not a working owner read.
  A live owner-attached round trip needs an RPC listener and belongs to the
  transport's own owner tests.
