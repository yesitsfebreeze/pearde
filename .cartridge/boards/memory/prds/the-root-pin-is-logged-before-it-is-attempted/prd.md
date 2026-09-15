---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# `main` logs "re-pinned cwd to project root" and then calls `set_current_dir` with `let _ =`, so a failed chdir prints a re-pin that did not happen — and the socket tag, which reads the process cwd, then names the launch directory instead of the root

## Do

`src/main.rs:67-76`:

```rust
let root = Config::resolve_root(&cwd);
if root != cwd {
    tracing::info!(target: "memory", from = %cwd.display(), to = %root.display(),
        "re-pinned cwd to project root (nearest ancestor with .memory)");
    let _ = std::env::set_current_dir(&root);
}
```

The line is emitted first and the action is attempted second, with its `Result`
discarded. On failure the log says the re-pin happened and nothing says
otherwise.

The config survives it — `Config::load(&root)` (`:88`) takes the resolved path,
not the cwd — which is why this is not a corrupt boot. What does not survive is
everything keyed on the process cwd. `Endpoint::memory()`
(`src/transport/src/typed.rs:328-339`) tags the socket from
`std::env::current_dir()` whenever `MEMORY_DIR` is unset, so a daemon that failed
its chdir serves the root's store on a socket named for the launch directory:
every client resolving the same root computes the other tag and finds nothing,
which is the split-brain [[uncanonical-root-gets-own-daemon]] closed by a
different route. `intake.dir` is cwd-relative on purpose
(`config.rs`'s own note) and moves with it, and `memory insights` writes
repo-relative ([[insights-writes-repo-relative]]).

A vanished cwd is not hypothetical here: [[the-machine-carries-memory-s-dead]]
counted up to 32 memory processes on this machine whose working directory no
longer exists. `resolve_root` walking from such a cwd, and the chdir onto a
path that has since gone, are the same condition.

Swap the order and keep the result: attempt the chdir, log the re-pin on
success, and on failure warn with the path and the error — a daemon that cannot
stand where it serves should say so, because every symptom downstream of it
points somewhere else.

Landed 2026-09-07 as `f4f901e1` on main after recovery into
`drive-recover-root-pin`. Full `just all` exit 0: formatting, workspace clippy,
terminal checks, 1,388 nextest tests passed (17 skipped), and workspace
doctests passed. The real removed-directory warning test and existing-directory
success test both passed. Success logs are unchanged; failure names the target
and OS error. This supersedes the earlier incomplete gate report below.

## Acceptance
With the target directory made unreachable, boot logs a warning naming the path
and the error rather than an info line claiming a re-pin; the success path logs
exactly as before; `just all` green.

Planning recheck 2026-09-07: `src/main.rs` still logs success before discarding
`set_current_dir`'s result. This is independent ready work. Keep the change
limited to attempting the re-pin and reporting its result, not altering boot
failure policy. The failure Check must exercise a real failed directory change
on a disposable path and capture its warning; a source-text assertion alone
cannot establish it. Isolate any successful cwd-changing test in a subprocess
so it cannot redirect parallel tests. Preserve the existing success message
and include the target path plus OS error in the warning.

Execution 2026-09-07: implementation is uncommitted in lane
`.claude/worktrees/the-root-pin-is-logged-before-it-is-attempted`, changing
only `src/main.rs`. Behavioral red reproduced false success logging; targeted
green passed 3 tests, all binary boot tests passed 7, with no ignored helper.
The literal `just all` passed formatting, clippy and 3 terminal tests, then
nextest stopped at 778 passed / 1 failed / 602 not run (17 skipped): the
shared record's `persistence` memo is now atomic but this lane's base still
lists it in `memos-bundles.txt`. Doc tests were not reached. Trunk already has
a concurrent uncommitted removal of that entry; it was not copied or committed
by this work. Status remains open; review, prerequisite landing and a full
green Check are still required before this lane can land.
