---
title: "one git worktree per worker — cut `lane/<slug>` on the claim, board dir sparse-checked out of it, rebase-then-ff-only so the lane's commit is the PRD's, drop the worktree on a sweep and keep the branch"
type: fileindex
path: resources/board/lanes.py
kind: resource
area: board
ext: py
keywords: [own, share]
present: true
---

# resources/board/lanes.py

one git worktree per worker — cut `lane/<slug>` on the claim, board dir sparse-checked out of it, rebase-then-ff-only so the lane's commit is the PRD's, drop the worktree on a sweep and keep the branch

→ `resources/board/lanes.py` — not a note; Dataview cannot read it, which is why this page exists.

## Keywords

- `@@own` — which tree a session holds, and what may be run in one it does not
- `@@share` — one copy per machine of what every lane regenerates

## Same scope — `@@own`

- [[.pearde/wiki/index/resources-board-collect-py|resources/board/collect.py]]
- [[.pearde/wiki/index/resources-board-refuse-py|resources/board/refuse.py]]
- [[.pearde/wiki/index/resources-board-session-py|resources/board/session.py]]
- [[.pearde/wiki/index/resources-guard-py|resources/guard.py]]

## Same scope — `@@share`

- [[.pearde/wiki/index/resources-board-shared-py|resources/board/shared.py]]
- [[.pearde/wiki/index/resources-invariants-one-copy-per-machine-of-what-every-lane-regenerates-sh|resources/invariants/one-copy-per-machine-of-what-every-lane-regenerates.sh]]
