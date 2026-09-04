---
state: failed
origin: requested
priority: 95
complexity: 22
blast-radius: mid
workflow: probe-then-spec
---


# the board locks by realpath

One dispatcher per physical board directory. The daemon's watch set and `pearde run` key on `os.path.realpath(board)`, so a symlink and its target are one board: the second registration of a path whose realpath is already held names the first holder and refuses, and `.state/serve.json` records one name per realpath.

Supersedes `two-board-aliases-for-one-directory-fan-a-run-out-twice` (was deferred) and folds in `the-untracked-pearde-symlink-stops-being-a-second-board` (found `done` on the board at filing time, so left as it is). Their text, folded: two aliases of one directory — a symlink beside its target, or a board registered once by its symlink path and once by its real path — fanned a `pearde run` out twice, two dispatchers cutting lanes on one tree; an untracked `.pearde` symlink in a repo read as a second board to the walk-up. Both are one defect: identity by spelling instead of by realpath.

## Done means

Two `pearde run` invocations, one via a symlink and one via the real path — the second refuses and names the first's pid; `.state/serve.json` never holds two names for one realpath.

## Needs

No gate. Sibling of the other Phase 0 rows under `no-work-is-lost-on-the-board`.

## History

**failed, retried 2026-09-03 21:03**

swept 2026-09-03 20:59 — claim impl-lock-realpath 2026-09-03 11:57, silent 6.9h: no file of this PRD's moved past `claim-ttl`. Read the worker's output before a retry; partial code stands on branch `lane/no-work-is-lost-on-the-board-the-board-locks-by-realpath`, whose worktree this sweep removed — the branch is kept.

## Failure

swept 2026-09-04 02:41 — claim impl-lock-realpath2 2026-09-03 21:37, silent 4.9h: no file of this PRD's moved past `claim-ttl`. Read the worker's output before a retry; partial code stands on branch `lane/no-work-is-lost-on-the-board-the-board-locks-by-realpath`, whose worktree this sweep removed — the branch is kept.
