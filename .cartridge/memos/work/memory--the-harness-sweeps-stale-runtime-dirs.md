---
kind: work
level: 10
status: done
description: a killed suite run orphans its /tmp/memory-test-* runtime dir forever, and the obvious sweep for them silently matches nothing on macOS
read_when: "cleaning /tmp, or touching the e2e harness's runtime dir"
---

# the-harness-sweeps-stale-runtime-dirs

Carries what [[@prd/work/memory--the-e2e-harness-removes-its-runtime-dir.md]] left open: `Drop`
closes the normal exit, not the abnormal one.

## Do

`MemoryProject::with_bin` (`tests/e2e/harness.rs:83`) mints
`/tmp/memory-test-<pid>-<ns>` as its private `XDG_RUNTIME_DIR`
(`e2e-forces-short-runtime-dir`), and `Drop` removes it. `Drop` does not run
when the test process is killed — an interrupted `just test`, a SIGKILL, a
panic that aborts — so every abnormal exit still leaves one directory per
`MemoryProject`, each holding a dead daemon and hub socket. 2211 of them stood
on this machine early on 2026-09-06, 1028 sockets inside, all from runs that
ended the wrong way. Re-measured at 03:51 the same day: **2**. One date is not
one number (`one-reading-is-not-a-measurement`) — the population is a moment,
driven by whatever ran and whatever swept in between, so quote it with its hour
or not at all.

Sweep siblings before minting: in `with_bin`, read the parent directory, and
remove each `memory-test-*` entry whose mtime is older than an hour. Age, not
liveness — a pid check wants `kill(pid, 0)` and this tree carries no `libc`
dependency (`spawn_successor` goes out of its way to avoid one). An hour is
longer than any suite run, so a sweep can never take a live peer's directory,
and the harness is the only writer of that name.

The trap this part exists to name: on macOS `/tmp` is a symlink to
`/private/tmp`, and `find` does not cross a symlink given as its start path
without `-H`. `find /tmp -maxdepth 1 -name 'memory-test-*'` therefore reports
**zero while thousands exist** — it matched the symlink and stopped. The sweep
must resolve the path before scanning, and any hand-run cleanup must say
`/private/tmp`. A sweep written against `/tmp` would pass its own check by
finding nothing to do.

**Done 2026-09-06.** `sweep_stale_runtime_dirs` runs in `with_bin` before the
directory is minted, canonicalizing `parent` first — the trap reproduces on
demand and was confirmed twice before any code was written, `ls -d
/private/tmp/memory-test-*` answering 2 while `find /tmp -maxdepth 1` answered 0.
`STALE_RUNTIME_AGE` is one hour and only the production call reads the clock.

**The Check was not run as written, because obeying it would have damaged the
machine.** It asks for a real `/tmp/memory-test-0-0` and an e2e run — but an e2e
test sweeping the real `/tmp` deletes the runtime directories of every other
session holding one there, and three were running suites at the time. Setting an
mtime also needs a crate this tree does not carry. So `sweep_stale_runtime_dirs`
takes a `cutoff: SystemTime` instead of reading the clock itself, and
`the_sweep_takes_the_old_runtime_dirs_and_leaves_the_rest` drives it over a
tempdir at `UNIX_EPOCH` (nothing stale) and `now + 60s` (everything stale), with
an unrelated directory surviving both. The parameter is what makes the narrowing
safe rather than merely convenient: it makes the test deterministic *and*
incapable of reaching outside its own tempdir. A Check authored against a quiet
machine becomes destructive on a busy one, and nothing in a part records which
it was written for (`the-worktree-check-passes-without-its-fix` collects the
family).

## Check

Create `/tmp/memory-test-0-0` with an mtime two hours old, run one e2e test, and
the directory is gone; create a second with a current mtime and it survives.
`ls -d /private/tmp/memory-test-* | wc -l` reports the same count before and
after a `just test` that is interrupted halfway.

Suite green at 1,239 passed with the sweep in place.
