---
kind: work
level: 10
status: done
estimate: 0.5d
actual: 0.25d
description: Add an installed-generation canary that spans provider stalls, drain, watchdog replacement, and durable recovery.
read_when: isolated daemon tests pass while the installed service returns EOF or stalls
---

# memory-integration-lifecycle-canary

## Do

Extend the existing lifecycle and end-to-end harness with a sustained canary against an identified installed binary generation. Exercise query, answer, report, readiness, direct-ID lookup, provider timeout, shutdown admission, stalled final flush, watchdog replacement, and recovery of committed data. Set deadlines for every operation and capture generation changes so EOF cannot be attributed without evidence. Reuse existing fake-provider and fresh-store fixtures. This does not replace the one-hour normal-use observation in [[@prd/work/memory--one-daemon-per-store.md]] and must not stop the shared development daemon during ordinary test runs.

## Spec

Landed on main at `2a76d905` (four commits fast-forwarded over `d057b368`; `just check` clean, `just test` 1520 passed in the lane), lane removed.

Probe of 2026-09-09, lane `memory-integration-lifecycle-canary`
(`/Users/feb/dev/memory/.claude/worktrees/memory-integration-lifecycle-canary`,
rebased onto `d057b368`: `61db4a33` harness, `49045266` canary, `92be1070`
recipe, `2a76d905` isolation step). The build went through and the Check ran
green from the lane on 2026-09-09, twice (private `CARGO_TARGET_DIR`, see the build
note); `just check` and `just test` (1520 passed) are green at `2a76d905`.

Files:

- `tests/e2e/harness.rs` — `run_deadline(args, Duration)` (a CLI call with a
  ceiling; code `DEADLINE = -2` when killed), `node_socket()`, `ask` made
  `pub` (one raw JSON envelope over the socket, no runtime), and
  `spawn_takeover_successor(sock, restarts)`: re-binds a dead daemon's socket
  path and spawns `--daemon` with the listener as fd 0, `MEMORY_TAKEOVER=1`,
  `MEMORY_WATCHDOG_RESTARTS=<n>` — what `identity::spawn_successor` hands the
  watchdog's successor.
- `tests/e2e/lifecycle_canary.rs` — the canary and its verdict; registered in
  `tests/e2e/main.rs` beside `lifecycle` (unix only).
- `justfile` — `canary bin=\`command -v memory\` rounds='1'`, the documented
  command.

What one round proves, on one `MemoryProject` (private store, runtime dir and
config home; `[reason] timeout_secs = 1`, intake off), every step under a
deadline (`READY_DEADLINE` 5s, `OP_DEADLINE` 30s, `HANG_DEADLINE` 20s,
successor 60s) and stamped with the generation that answered it (`pid`,
`watchdog_restarts`, `build_stamp` from the graph-free `ready` operation):

1. `ready`; routed `ingest` of three facts; the local `query --mode vector`
   sees the fact on disk (what "committed" means to a successor); the routed
   `query` sees it (polled — the first routed read after a routed write
   missed by ~300 ms on the probe); `get <12-char prefix>` resolves the full
   id; `query`, `get <full id>`, `report`, `ask` (the fake echoes the prompt).
2. `ask` carrying `CHAT_HANG_MARKER`: exits non-zero naming `timeout` in
   ~8 s; a `ready` sent 300 ms into the hang answers in ~1 ms from the same
   pid; `health` answers.
3. A routed `query` carrying `STALL_MARKER` (embed parked 5 s) in flight,
   then `shutdown` over the raw socket: the in-flight query exits 1 with
   `memory query: shutting down: the daemon refused this request, retry against
   a fresh one` (`BridgeRefusal::ShuttingDown`, category `shutting_down`), the
   daemon's stderr carries `shutting down...` and `done`, and after the exit
   `memory ready` says `no daemon serving` while `memory query` answers from disk
   — no EOF.
4. A fresh `--daemon` over the same store: new pid, 0 restarts, the three
   reads answer.
5. SIGKILL (the dark exit), then `spawn_takeover_successor(sock, 1)`: the
   successor answers `ready` with a new pid and `watchdog_restarts == 1` on
   the same socket inode the test bound (adopted, not re-bound), and `query`,
   `get`, `report` are answered by that pid.

Before round one, an `isolation` step records where the run lives: the socket
every step addresses is under the `/tmp/memory-test-<pid>-<nanos>` runtime dir
the harness minted, and the writer lock the daemon claimed is under the
project's own temp cwd. That is the proof the shared root was never touched
— the daemon serving `/Users/feb/dev/memory` replaces itself under other
writers every few minutes ([[@prd/work/memory--one-daemon-per-store.md]]), so its pid or uptime
before and after a run says nothing about the canary.

`verdict(&[Step])` is the pass: every step ok, a `takeover` step present,
`query`/`get`/`report` after the last takeover answered by the successor's
pid, and the pid unchanged under every step that is not `restart` or
`takeover` — a generation that moved under `ask` is a finding.
`a_health_only_takeover_does_not_pass_the_verdict` is the regression the Do
asks for: a ledger whose takeover is followed only by `ready`, or where any
one of the three reads failed, or where the reads were answered by the
predecessor's pid, is rejected.

Measured: one round 10–14 s (`just canary` against `~/.cargo/bin/memory`:
10.2 s; three rounds on the build under test: 33.7 s). The one-round default
runs inside `just test` / `cargo nextest run --workspace`.

What the probe could not provoke from outside the binary, and where it stays:

- Admission refusal of *new* work during the drain: the window from the
  latch to the exit is 25–100 ms on this store (the shutdown answers in
  ~24 ms; the flush is milliseconds), shorter than a CLI spawn. The canary
  proves the same refusal on the crossing already in flight; the admission
  check on `invoke` is the same `MODEL_DEPENDENT` + `is_shutting_down()` line
  and stays with `server_admin_test`.
- A stalled final flush and the watchdog's 30 s stall detection: no lever
  outside the process stalls the async beat (`STALL_LIMIT` and the 5 s
  `FLUSH_DEADLINE_SECS` are constants, `fault` is deliberately not an
  operation — `daemon_exposes_only_headless_consumer_contracts`). The canary
  drives what the watchdog produces (successor as fd 0 with the restart
  count) and leaves the detection with `watchdog_flush_tests`. Widening this
  needs a daemon-side fault hook, which is a Do of its own.

Steps for the hand, from the lane:

```sh
cd /Users/feb/dev/memory/.claude/worktrees/memory-integration-lifecycle-canary
just canary                                   # the installed memory, one round
just canary "$(just target-dir)/debug/memory" 3 # the build under test, three rounds
cargo test --test e2e -- lifecycle:: health_surface::
```

Then land: `just land memory-integration-lifecycle-canary` from the trunk, per
[[git-policy]], and `just lane-rm` after the ancestry check.

Build note: every lane links `target/debug/memory` into the one shared
`target/`, and cargo's fingerprints there are keyed on relative paths, so a
sibling lane's `transport` (one carrying `LaunchOpenReq.recall`) is taken as
fresh for this lane's `commands` and the build fails with `missing field
recall`; the same happened once in a private dir two lanes had shared. The
Check runs with `RUSTC_WRAPPER= CARGO_TARGET_DIR=<a dir only this lane
uses>` — the 2026-09-09 run did — and a failure the canary cannot explain is
first rebuilt that way.

## Check

- [x] `just canary` (the `memory` on PATH, one round) reports `2 passed; 0 failed` and a `canary takeover ... ok` line with `restarts 1` and `listener adopted true`.
- [x] `MEMORY_CANARY_ROUNDS=3` on the build under test passes with no `canary ... FAIL` line: healthy operations (`ready`, `ingest`, `committed-on-disk`, `visible-routed`, `get-by-prefix`, `query`, `get`, `report`, `ask`) all `ok`.
- [x] `ask-hang` exits non-zero naming `timeout` inside `HANG_DEADLINE`, and `ready-during-hang` answers from the same pid inside `READY_DEADLINE`: a provider stall does not block readiness.
- [x] `drain-refuses` carries `shutting down: the daemon refused this request` and `orderly-flush` sees `shutting down...` and `done`; `ready-after-exit` says `no daemon serving` and `fallback-after-exit` returns the bicycle hit: drain refuses with the shutdown category and the CLI never EOFs.
- [x] `takeover` records a pid different from `restart`'s with `watchdog_restarts == 1` on the adopted listener inode, and `query`, `get`, `report` after it are answered by that pid: takeover changes generation identity and committed data stays readable.
- [x] `a_health_only_takeover_does_not_pass_the_verdict` passes: a ledger with a takeover followed only by `ready`, or with any of `query`/`get`/`report` failed or answered by the predecessor, is rejected.
- [x] `cargo test --test e2e -- lifecycle:: health_surface::` passes with the lane's own `target/debug/memory` (rebuild first if a sibling lane linked last).
- [x] Both `just canary` runs record `canary isolation ... ok` (socket under the harness's `/tmp/memory-test-*` runtime dir, writer lock under the project's temp cwd), and the full `--nocapture` log of the run names neither `/Users/feb/dev/memory/.memory` nor a user-level `/tmp/memory-<tag>-<user>.sock`: the canary never addresses the shared root.

```sh
cd /Users/feb/dev/memory/.claude/worktrees/memory-integration-lifecycle-canary
export RUSTC_WRAPPER= CARGO_TARGET_DIR="${TMPDIR:-/tmp}/memory-target-lifecycle-canary"   # a dir only this lane uses
log="$(mktemp -t canary)"
just canary 2>&1 | tee "$log" | grep -E 'canary (isolation|takeover)|canary .* FAIL|test result'
just canary "$(just target-dir)/debug/memory" 3 2>&1 | tee -a "$log" | grep -E 'canary .* FAIL|test result'
cargo test --test e2e -- lifecycle:: health_surface:: 2>&1 | grep -E 'FAILED|test result'
[ "$(grep -c 'canary isolation .* ok' "$log")" = 2 ] && echo "isolation recorded on both runs" || echo "ISOLATION STEP MISSING"
grep -qE '/Users/feb/dev/memory/\.memory|/tmp/memory-[0-9a-f]+-[^/ ]+\.sock' "$log" \
  && { echo "SHARED ROOT NAMED:"; grep -nE '/Users/feb/dev/memory/\.memory|/tmp/memory-[0-9a-f]+-[^/ ]+\.sock' "$log" | head; } \
  || echo "shared root never named"
```
