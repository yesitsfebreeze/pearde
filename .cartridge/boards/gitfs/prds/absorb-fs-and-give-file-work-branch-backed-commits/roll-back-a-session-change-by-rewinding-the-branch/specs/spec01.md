---
complexity: low
footprint:
- src/store.rs
- src/overlay.rs
- .cartridge/tests/unit/git_mode.rs
- .cartridge/help.md
---

# Roll back one session commit by committing the prior content

`tool.gitfs rollback {commit}` undoes one session commit by committing each
path it changed back to its prior content. History is never rewritten, so the
undone change stays saved. `ls` returns the session's commits newest first,
and `ls {session}` shows another agent's.

A commit whose path a later commit changed is refused ("roll that back
first"); a trunk commit is refused as not the session's. Materialize after
rollback writes the restored content to the worktree.

## Acceptance

- [x] Rolling back the newest commit restores the path on the branch with
  one new commit.
- [x] A commit whose path a later commit changed is refused ("roll that
  back first"); a trunk commit is refused as not the session's.
- [x] Materialize after rollback writes the restored content to the
  worktree.

## Verify and Proof

```sh
set -eu
cd /Users/feb/dev/cartridge/fs.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0
cargo fmt -p fs -- --check
cargo clippy -p fs --all-targets -- -D warnings
cargo test -p fs --all-targets git_mode_tests
```

These are the exact commands the composed `just check fs` and
`just test fs` gates run for the fs owner, narrowed to the `git_mode_tests`
suite (the `git_mode.rs` unit tests included through `src/files.rs`) whose
rollback section covers this PRD.