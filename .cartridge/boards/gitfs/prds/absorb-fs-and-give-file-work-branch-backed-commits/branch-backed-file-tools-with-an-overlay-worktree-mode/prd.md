---
repo: /Users/feb/dev/cartridge/fs.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: fs
work-kind: leaf
needs:
- "@gitfs/absorb-fs-and-give-file-work-branch-backed-commits/merge-fs-source-into-gitfs-with-no-behavior-change"
commit: "75e76e63d8f97954759bf294f4b0d86d78d5643b"
---

# Git and local modes for the file tools

`mode = "git"` (default): `tool.write`/`tool.edit` commit once per change to the
session branch and leave the worktree alone; `tool.read`, `tool.glob`,
`tool.grep` and `tool.digest` see the session's changes before the worktree.
`mode = "local"`, or a workspace outside Git, writes the worktree as before.

## Acceptance

- [x] Git mode: write, edit and a new file each add one commit, the worktree keeps its bytes, read returns the branch content, evidence is Provider::Gitfs with overlay coordinates (`git_mode.rs`).
- [x] A stale observation is refused after another writer moves the branch; the branch gains no commit from the refused edit.
- [x] glob lists a branch-only file; grep reports branch content and hides the worktree's stale copy of a changed path.
- [x] Local mode and a non-repository workspace write the worktree and create no `refs/gitfs/` ref.

## Proof and recovery

`fs.ctg/.cartridge/tests/unit/git_mode.rs`, run by `just test fs`, pass.
Known ceiling: grep of branch content uses the Rust regex engine and file-name
glob matching, close to but not identical to rg's options.
