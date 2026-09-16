---
repo: /Users/feb/dev/cartridge/fs.ctg
state: "analyzing"
origin: requested
priority: 50
blast-radius: wide
workflow: develop-one-cartridge
capability-owner: fs
work-kind: rollup
needs:
- "@gitfs/absorb-fs-and-give-file-work-branch-backed-commits/merge-fs-source-into-gitfs-with-no-behavior-change"
- "@gitfs/absorb-fs-and-give-file-work-branch-backed-commits/branch-backed-file-tools-with-an-overlay-worktree-mode"
- "@gitfs/absorb-fs-and-give-file-work-branch-backed-commits/roll-back-a-session-change-by-rewinding-the-branch"
claim: "coordinator-main 2026-09-16T06:48:21.142Z"
---

# One fs cartridge whose file work commits to Git branches

The file surface was split: fs wrote the worktree, gitfs wrote a session branch.
gitfs is absorbed into fs. A `mode` setting (`git` default, `local`) decides
where `tool.write` and `tool.edit` land. In git mode each change is one commit
on `refs/gitfs/<session>`, the worktree waits for `tool.gitfs materialize`,
reads and searches prefer the session's changes, any agent can list another
session's branch, and one commit at a time can be rolled back. The gitfs
cartridge is out of the composition; its sources, tests and docs live in fs.

## Acceptance

- [x] The composition loads one `fs` cartridge serving read/write/edit/search/glob/grep/digest/draft, `tool.gitfs` and `tool.ship`; `gitfs` is gone from `.cartridge/init.lua` and the gate owner lists.
- [x] Each leaf's acceptance holds with the fs suite: `just check fs` and `just test fs` pass (109 tests).
- [x] Attributed agent review >= 90 with no blockers.

## Review

93/100, no blocking findings, 2026-09-16. The reviewer independently reran
`just check fs` and `just test fs` (109 passed) and grepped the composition
clean of gitfs. One recorded note: fs inherits gitfs's wildcard `exec: ["*"]`
and `net: ["*"]` grants — a consolidation of grants the composition already
carried, not an escalation; push may later narrow `net` to remote scopes.

## Proof and recovery

Evidence 2026-09-15 from `/Users/feb/dev/cartridge`: `just check fs` pass,
`just test fs` pass, `just describe fs` loads the merged manifest. `just verify`
was blocked by an untrusted change in `lsp.ctg`, outside this work.
`gitfs.ctg` is kept on disk and in `.gitmodules`: it holds two unpushed commits
whose content is already in fs. Retire the submodule once those are pushed.
Evidence wire names stay `gitfs`/`gitfs_overlay`/`refs/gitfs/` so sessions and
existing records need no change.

## Work items

- [Merge gitfs into fs](merge-fs-source-into-gitfs-with-no-behavior-change/prd.md)
- [Git and local modes for the file tools](branch-backed-file-tools-with-an-overlay-worktree-mode/prd.md)
- [Roll back one session commit](roll-back-a-session-change-by-rewinding-the-branch/prd.md)
