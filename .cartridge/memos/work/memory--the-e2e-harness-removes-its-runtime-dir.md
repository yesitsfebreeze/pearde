---
kind: work
level: 10
status: done
description: MemoryProject::drop kills its children and leaves its private runtime dir behind, so a suite run litters /tmp with one directory per test
read_when: "asking who cleans the e2e harness's runtime dir"
---

# the-e2e-harness-removes-its-runtime-dir

Done 2026-09-05: `Drop` removes the runtime dir after reaping its children.
A full `cargo test --test e2e` (66 tests) now leaves zero new
`/tmp/memory-test-*` behind, and `cargo nextest run --workspace` (1206 passed)
does not move the count. The 2012 dirs already on this machine are historical
and were not swept — nothing here creates more.

## Do

`MemoryProject::new` mints `/tmp/memory-test-<pid>-<ns>` as its private
`XDG_RUNTIME_DIR` (`e2e-forces-short-runtime-dir`) and `Drop`
(`tests/e2e/harness.rs:290`) kills the children and returns. Nothing removes
the directory: **1954 of them older than an hour** stood on this machine, one
per test per run since the suite was ported.

Remove the runtime dir in the same `Drop`, after the children are reaped —
`std::fs::remove_dir_all`, errors ignored, because a test that already failed
must not fail again on cleanup. The sockets inside it are the daemon's and the
hub's; both processes are dead by then. The cwd is a `tempfile::TempDir` and
already cleans itself, which is exactly the shape the runtime dir is missing.

Note what this does *not* fix: the hub a daemon auto-starts is not a child of
the harness and is not killed by `Drop` at all —
`an-auto-started-hub-stops-itself` is what stops it.

## Check

`ls -d /tmp/memory-test-* | wc -l` reports the same count before and after a
full `just test`.
