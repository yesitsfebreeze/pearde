---
repo: /Users/feb/dev/cartridge/fs.ctg
state: open
origin: requested
priority: 50
blast-radius: low
workflow: develop-one-cartridge
capability-owner: fs
work-kind: leaf
needs:
- "@gitfs/absorb-fs-and-give-file-work-branch-backed-commits/branch-backed-file-tools-with-an-overlay-worktree-mode"
---

# Roll back one session commit

`tool.gitfs rollback {commit}` undoes one session commit by committing each path
it changed back to its prior content. History is never rewritten, so the undone
change stays saved. `ls` returns the session's commits newest first, and
`ls {session}` shows another agent's.

## Acceptance

- [x] Rolling back the newest commit restores the path on the branch with one new commit.
- [x] A commit whose path a later commit changed is refused ("roll that back first"); a trunk commit is refused as not the session's.
- [x] Materialize after rollback writes the restored content to the worktree.

## Proof and recovery

Covered by `git_mode_commits_each_change_and_leaves_the_worktree_until_materialize`
in `just test fs`, pass. Also fixed: materialize compared millisecond disk times
with whole-second commit times and refused every existing file as newer.
