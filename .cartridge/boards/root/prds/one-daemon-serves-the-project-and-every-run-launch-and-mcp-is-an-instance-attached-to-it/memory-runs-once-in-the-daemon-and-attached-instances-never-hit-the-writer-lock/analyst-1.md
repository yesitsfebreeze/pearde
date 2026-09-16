# analyst-1 — SPECCED

PRD `@root/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/memory-runs-once-in-the-daemon-and-attached-instances-never-hit-the-writer-lock`,
state `analyzing`, prio 80. Repo `memory.ctg` at `5097a83` (clean working tree).
Analyst session 2026-09-16.

Drafts:

- `.state/loop/one-daemon-.../memory-runs-once-.../spec01.md`
- `.state/loop/one-daemon-.../memory-runs-once-.../attempt-1.patch`

## Verdict

**SPECCED.** No production change. One regression test in
`.cartridge/tests/unit/src/cartridge/engine_test.rs`, proven non-vacuous by
patching in two regressions and watching it fail.

## Did the audit premise hold?

**Partly — and the PRD's own reading of it is right.**

- *Held as stated:* a second **composed** memory node over one data dir really is
  refused, with exactly `another memory writer holds this data dir`
  (`src/store/core/src/lock.rs:53-56`, raised at `:112-120`). The cartridge takes
  the lock in `commands::memory::Engine::open`
  (`src/commands/src/memory.rs:14-15`) and holds it through `Engine._writer`
  (`:5-9`), so under many hosts every call on the loser fails, ledger appends
  included.
- *Already false:* the PRD's escape hatch, "if any memory path still assumes
  process-exclusivity beyond the file lock … e.g. attach-mode memory must not
  try to take the writer lock read-only". memory.ctg **already has** an attached
  shape, `ServiceConfig::Attached` (`src/cartridge/src/lib.rs:23-29`, selected at
  `:31-92` when the `owner` setting is a table), and it never touches the lock:
  calls return over `memory_transport::owner::read_observed`
  (`lib.rs:300-312`) before `status.engine` is consulted, and the status probe
  takes the same branch (`src/cartridge/src/status.rs:208-224`). Only the
  `Local` branch reaches `store::lock::observe` (`status.rs:245`), and only when
  the engine is not open. Nothing to fix.
- *No other exclusivity assumption found.* `PASS` and `IMPORTED_AT`
  (`src/rpc/src/ledger.rs:30-36`) are process statics, but the node has exactly
  one `Engine` — `SERVICE` is a process-global (`src/cartridge/src/lib.rs:360`)
  and the engine is a `OnceCell` on the service's `Tracker`
  (`src/cartridge/src/status.rs:54`), opened once under `INITIALIZATION`
  (`lib.rs:318-338`) — so "per process" is "per store". Every other
  `store::lock::acquire` call site is an admin CLI command that is *meant* to
  refuse against a live writer (`commands_gc.rs:10`, `commands_reembed.rs:18`,
  `commands_export.rs:164`/`:202`, `commands_hub.rs:93`/`:156`/`:291`,
  `commands_check.rs:260`, `commands_graph_ops.rs:341`/`:437`/`:702`,
  `commands_admin_compact.rs:13`/`:38`, `commands_queue_cmd.rs:112`,
  `commands_ingest_cmd.rs:158`, `commands/src/lib.rs:718`), plus the standalone
  `memory daemon` (`commands_serve.rs:71-100`), which the project daemon does not
  compose.

So this is the agent sibling's shape again: the right deliverable is the
regression that pins the property, not a change.

## The condensing loop

`spawn_ledger` (`src/commands/src/memory.rs:59-81`) is the only rollover
scheduler in the repo (60 s, 900 s after a failed pass), and it is called from
exactly one place: the last line of `Engine::open` (`:44`), after the lock, into
an `Engine` that holds it. A service refused the lock gets `Err` from
`Engine::open`, no `Engine`, and therefore no loop. The 5-minute hold-off the PRD
names is `IMPORTED_AT`/`IMPORT_QUIET_MS` (`src/rpc/src/ledger.rs:32-36`, set at
`:725`, read at `:746-751`); `PASS` (`:30-31`) stops the loop and an explicit
`rollover` condensing one unit twice. Ownership is structural, not scheduled.

## What was probed

Worktrees under the scratchpad, sibling `memo.ctg` symlinked, isolated
`CARGO_TARGET_DIR`. The live project daemon was never started, stopped, replaced
or called; no memory call ran against a live store; every store in every probe
was a `tempfile::tempdir()`.

| # | command (cwd) | exit |
|---|---|---|
| 1 | `git worktree add --detach <scratch>/lane/memory.ctg 5097a83` (memory.ctg) | 0 |
| 2 | `cargo test -p memory-cartridge --lib …` (lane) | 101 — wrong package name |
| 3 | `cargo test -p memory_cartridge --lib a_second_local_service …` (lane) | **0**, 1 passed |
| 4 | regression R2: `Engine::open` locks a per-pid subdir instead of `data_dir` (lane) | **101**, FAILED at `engine_test.rs:179` "and holds the writer for its lifetime" |
| 5 | regression R1: `service_configuration` always returns `Local` (attached falls back to a local engine) (lane) | **101**, FAILED at `engine_test.rs:214` "attached memory must not reach for the writer lock" |
| 6 | `cargo fmt --check` (lane) | 0 |
| 7 | `cargo test -p memory_cartridge --lib` with the test (lane) | 101 — 20 passed / 1 failed |
| 8 | `cargo test -p memory_cartridge --lib` **baseline, no new test**, ×2 (lane) | 101 — 19 passed / 1 failed |
| 9 | `cargo test -p memory_cartridge --lib -- --test-threads=1` baseline (lane) | 101 — 19 passed / 1 failed |
| 10 | `git apply --check attempt-1.patch` on a fresh `5097a83` worktree | 0 |
| 11 | Verify block 1 verbatim, `sh -eu -c` (lane) | 0 |
| 12 | Verify block 2 verbatim, `sh -eu -c` (lane) | 0 |
| 13 | Verify block 3 verbatim, `sh -eu -c` (lane) | 0 |
| 14 | Verify block 1 on a cold `CARGO_TARGET_DIR`, timed | 0, **16 s** (worst cold build observed elsewhere: 29 s — far inside the 120 s limit) |

Rows 4 and 5 are the non-vacuity proof: two independent regressions, two
different failing assertions, both restored afterwards.

Rows 7–9 matter: **`cargo test -p memory_cartridge --lib` is already red at
`5097a83`**, with or without this change. `dispose`/`drain` sets the
process-wide `util::lifecycle::SHUTTING_DOWN` (`src/util/src/lifecycle.rs:30`),
so whichever engine test runs after
`health_overtakes_blocked_ingestion_and_dispose_drains_it` dies with
`shutting down: the daemon refused this request, retry against a fresh one`.
Baseline 19/1, with the new test 20/1 — the same single failure. The new test
therefore ends with `drop(owner)` and not `drain(…)`, and the Verify block names
the single test rather than the package. The shared-lifecycle-static bug is real
but unrelated; flagged, not fixed here.

## Acceptance boxes: what this repo can and cannot prove

Nothing was silently narrowed. Proposed wordings, coordinator decides.

**Box 1** — "With the daemon running, `cartridge run memory '{"op":"status"}'` and
a proxy-ledger append both succeed with exactly one memory node process; no
`another memory writer holds this data dir` error appears."
*Unprovable from memory.ctg*: it needs a live daemon, `cartridge run`, and a
process count — all cartridge.ctg. Proposed:

> memory.ctg's share of "exactly one memory node, no
> `another memory writer holds this data dir`": the cartridge takes the writer
> lock once in `Engine::open` and holds it for the node's lifetime, a second
> local service over the same data dir is refused with that exact message and
> opens no engine, and the attached shape never asks for the lock at all. (The
> daemon-wide count is delivered by the done sibling
> `an-instance-attaches-to-the-daemon-and-never-composes-silently` and re-proven
> composed by `the-composed-acceptance-test-proves-one-daemon-one-node-per-cartridge-and-attached-instances`.)

**Box 2** — "A memory `ingest` from one attached instance is returned by `query`
from another (parent Acceptance box 3)."
*Unprovable from memory.ctg*: under the host-attach contract both instances are
the same node, so the round trip is entirely cartridge.ctg event routing. Proposed:

> Two callers of the one node see one store: the writer serves ingest, query and
> ledger from a single `Engine`, and a second service that would have been the
> "other instance" gets no engine of its own to diverge in. (The cross-instance
> `ingest`-then-`query` round trip belongs to the composed test.)

**Box 3** — "The condensing loop's status (`{"op":"ledger","action":"status"}`)
shows the daemon's one node doing the condensing."
*Unsatisfiable as written, anywhere.* `ledger status` returns only per-tier row
and byte counts (`src/rpc/src/ledger.rs:289-297`) — no pid, no node, no "who is
condensing". Making it show that would be a production change (a new field), and
the PRD says this child mostly verifies the shape. Proposed:

> The condensing loop belongs to the writer: `spawn_ledger` is called from
> exactly one place, the end of `Engine::open`, after the lock is taken and into
> an `Engine` that holds it — so a service refused the lock, and an attached
> service, run no condensing pass.

If the coordinator would rather keep the literal wording, that is a small
production change (add the owning pid to the `ledger status` reply) and the
footprint must then keep `src/`.

## Footprint change needed

The declared footprint is `src/store/lock.rs` and `src/`.

- **`src/store/lock.rs` does not exist.** The file is
  `src/store/core/src/lock.rs`. Harmless if the entry just never matches, but it
  should be corrected or dropped.
- **The only file the spec changes sits outside the footprint.** This repo
  `#[path]`-includes its unit tests from `src/` (`src/cartridge/src/lib.rs:581`
  includes `.cartridge/tests/unit/src/cartridge/engine_test.rs`), exactly like
  the agent sibling. Add:

      .cartridge/tests/unit/src/cartridge/engine_test.rs

  Otherwise collect refuses the change. `src/` can stay or go; the spec touches
  nothing under it.

## Handed up, out of footprint

- `cargo test -p memory_cartridge --lib` is order-dependent and red at HEAD
  because `util::lifecycle::SHUTTING_DOWN` is a process static that one test sets
  for the whole binary. Worth its own PRD under the memory owner; it will bite
  any future spec that wants a package-wide Verify block here.
- Lane siblings: a lone `memory.ctg` worktree cannot build —
  `src/cartridge/Cargo.toml:13` reaches `../../../memo.ctg/evidence`, a sibling of
  the checkout. The spec's first Verify block creates that symlink when missing
  (`MEMO_CTG` with an absolute default), which is a no-op in pass 2. If the
  collector already seeds lane siblings, the line can be dropped.

## Remaining uncertainty

- The attached leg of the test uses an endpoint nothing listens on. It pins
  *which error comes back* and that the lock is untouched, not a working
  owner-attached read; a live owner round trip needs an RPC listener and belongs
  to the transport's own owner tests.
- Verify block 1 was timed at 16 s cold on this machine. A much slower collector
  could approach the 120 s ceiling on a genuinely cold dependency tree.
