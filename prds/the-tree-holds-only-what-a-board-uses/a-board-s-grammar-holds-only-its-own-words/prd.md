---
state: failed
origin: requested
priority: 50
complexity: 22
blast-radius: mid
workflow: probe-then-spec
---


# a board's grammar holds only its own words

A board's `grammar.md` holds `## This repo` only. `grammar.py` reads the shipped vocabulary from the repo's `references/grammar-board.md` and merges it on `list`, `show` and `brief`; `init` stops copying 308 lines into every board; existing boards are upgraded by `pearde upgrade`.

## Done means

A fresh board's `grammar.md` is under 20 lines and `grammar show prd` still answers.

## Needs

No gate.

## History

**failed, retried 2026-09-03 21:03**

swept 2026-09-03 20:59 — claim impl-grammar-words 2026-09-03 12:37, silent 8.2h: no file of this PRD's moved past `claim-ttl`. Read the worker's output before a retry; partial code stands on branch `lane/the-tree-holds-only-what-a-board-uses-a-board-s-grammar-holds-only-its-own-words`, whose worktree this sweep removed — the branch is kept.

## Failure

swept 2026-09-04 02:41 — claim impl-nova2-a-board-s-gr 2026-09-03 21:40, silent 4.8h: no file of this PRD's moved past `claim-ttl`. Read the worker's output before a retry; partial code stands on branch `lane/the-tree-holds-only-what-a-board-uses-a-board-s-grammar-holds-only-its-own-words`, whose worktree this sweep removed — the branch is kept.
