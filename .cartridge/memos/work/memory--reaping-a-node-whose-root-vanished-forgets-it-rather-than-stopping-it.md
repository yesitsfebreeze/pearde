---
kind: work
level: 10
status: done
description: the reaper drops a node whose project directory was deleted while `alive()` says the process is running, and dropping a `NodeHandle` drops a `std::process::Child` — which does not kill — so the daemon keeps running, untracked and unreachable, which is the mechanism behind the 32 memory processes whose cwd is gone
read_when: "touching the hub reaper, or counting memory processes on a machine"
---

# reaping-a-node-whose-root-vanished-forgets-it-rather-than-stopping-it

## Do

The hub has a graceful stop. `shutdown(&mut NodeHandle)`
(`src/hub/src/lib.rs:126-145`) asks the node over its own socket, waits
`READY_RETRIES` for the child to exit, and kills only if that stalls — "the
node's flush already had ~10s; kill beats a zombie holding the socket". It is
reached from exactly two places: the `unload` operation (`:550`, `:563`) and
`idle_pass` (`:735`), which removes the handle and then calls it.

The reaper reaches it from none. Its three removals all drop the handle and
stop there (`:592-611`):

- **`!handle.alive()`** — `try_wait` says the process is gone. Correct.
- **`!root.is_dir()`** — the project directory was deleted, and `alive()`
  returned *true*: the process is running. The handle is dropped anyway.
- **`drop_dead_adopted`** — a daemon someone else started, whose socket does
  not answer. Not ours to stop, so dropping is right.

Dropping the handle drops its `Option<Child>`, and `std::process::Child`'s
`Drop` does not kill; nothing in this file sets `kill_on_drop`. So the middle
case logs "reaped node whose root no longer exists" and leaves a live daemon
behind — now absent from `hub status`, unreachable through `resolve`, and
holding whatever it held.

The comment above that branch names the scenario itself: "a finished test's
temp dir". That is [[the-machine-carries-memory-s-dead]] from the other end —
up to 32 memory processes on this machine whose working directory is gone, a
peer suite's test daemons, 12 MB each. The observation is recorded; this is
where they come from.

Call `shutdown` on that branch, as `idle_pass` does. The trade to weigh rather
than assume: a node whose root vanished may still hold unflushed state, and
its store may not be under the root at all, since `data_dir` is configurable
([[memory-dir-repoints-two-things]]) — which is an argument for the graceful path
and against the drop, not for leaving it alone.

## Check

A node whose root directory is removed while it runs is gone from `ps` within
one reap interval, and its log shows the shutdown rather than only the hub's
"reaped" line; `just test` green.

Planning recheck 2026-09-07: `src/hub/src/lib.rs` still removes a live handle
inside `spawn_reaper`'s `retain` when `!root.is_dir()`, without calling
`shutdown`. The graceful helper exists and waits for exit before killing on
timeout. Existing `tests/e2e/hub.rs` covers explicit unload, idle unload and a
dead adopted node, but no vanished-root test. The implementation remains
unwritten. Remove handles under the map lock, then await their shutdown after
releasing the lock, as the idle path does; retain the distinction between dead
children and live removed roots. Test only isolated disposable roots, with
state/runtime isolation already present in the e2e harness; do not delete any
live project root to perform the Check.

Race/ownership recheck: `resolve` holds the per-root spawn lock through reuse
or replacement. The reaper must take that same lock before rechecking the root
and removing its handle, and hold it through shutdown so a recreated root
cannot spawn a replacement on the endpoint being stopped. Do not hold the
global nodes lock while awaiting shutdown. Only call shutdown for hub-owned
handles (`child.is_some()`); retain the existing drop-only policy for adopted
processes, which are not the hub's to stop. Cover a still-existing root and an
adopted handle as negative controls as well as an owned vanished-root child.

Execution/recovery 2026-09-07: the two-file implementation and three isolated
process tests were recovered byte-for-byte from surviving Neovim buffers after
the original lane disappeared during disk exhaustion. They are now committed
in `drive-recover-reaper`, rebased onto integrated main as `c5450cb9`. The
original approved process test gave the expected red (owned child survived,
both controls passed), then green (3 passed); original `just check` passed.
The recovered lane is clean and `git diff --check main...HEAD` passes. Its
full current Check remains pending; no completed or landed status is claimed.
Run its suite after the root-pin lane's sole running build ends, preserving
the requirement for approved process inspection when the sandbox denies `ps`.

Done 2026-09-07: `reap_nodes` in `src/hub/src/lib.rs` takes the per-root
spawn lock, removes the handle under the map lock, and calls `shutdown` for a
hub-owned child whose root vanished, still dropping adopted handles without
stopping them. Three process tests in `tests/e2e/hub.rs` pass against the
lane's own binary: the owned child is gone from `ps` within one reap interval
with `shutting down...`/`done` in its log, an adopted daemon survives, a child
with an existing root stays. Lane `herd-drive-p1-3`, commit `13239f35`; the
herd caller runs `just test` and lands it.
