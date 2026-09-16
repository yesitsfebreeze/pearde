---
complexity: medium
footprint:
- src/service.rs
- src/files.rs
- src/search.rs
- src/worker.rs
- src/store.rs
- src/overlay.rs
- .cartridge/tests/unit/git_mode.rs
- .cartridge/help.md
---

# Git and local modes for the file tools

`mode = "git"` (the default): `tool.write`/`tool.edit` commit once per change to
the session branch `refs/gitfs/<session>` and leave the worktree alone;
`tool.read`, `tool.glob`, `tool.grep` and `tool.digest` see the session's
changes before the worktree. `mode = "local"`, or a workspace outside a Git
repository, writes the worktree directly and creates no `refs/gitfs/` ref.

A stale observation is refused after another writer moves the branch, and the
refused edit adds no commit. Evidence for branch mutations is
`Provider::Gitfs` with overlay coordinates. Known ceiling: grep of branch
content uses the Rust regex engine and file-name glob matching, close to but
not identical to rg's options.

## Acceptance

- [x] Git mode: write, edit and a new file each add one commit, the worktree
  keeps its bytes, read returns the branch content, evidence is
  `Provider::Gitfs` with overlay coordinates (`git_mode.rs`).
- [x] A stale observation is refused after another writer moves the branch;
  the branch gains no commit from the refused edit.
- [x] glob lists a branch-only file; grep reports branch content and hides
  the worktree's stale copy of a changed path.
- [x] Local mode and a non-repository workspace write the worktree and create
  no `refs/gitfs/` ref.

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
suite (the `git_mode.rs` unit tests included through `src/files.rs`) that this
PRD owns.