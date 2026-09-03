---
state: done
origin: requested
priority: 85
complexity: 12
blast-radius: mid
workflow: probe-then-spec
actual: 0.45h
commit: 77665a3 318b6e5
---

# a conflicted lane is reported not stranded

When a lane's rebase conflicts during collect, the PRD moves to `blocked` with a reason naming the conflicting files and the lane branch. Nothing stays `claimed` silently.

Hit twice on 2026-09-03: `board-commands-run-in-the-session-s-tree` at 89f3e8f, and `the-cross-board-parts` on all.md — both lanes sat claimed with a conflicted rebase nobody was told about.

## Done means

Force a conflict on a scratch lane → `pearde scan` shows the PRD blocked with the file list; `pearde unblock` after resolving returns it to specced.

## Needs

No gate. Sibling of `collect-runs-the-invariants-and-red-refuses`; both act on the collect path.

## Report

spec01: exit 0
A. a conflicting lane
  ok   A1 collect exits 1
  ok   A1 the conflict is named on stderr
  ok   A1 ...with the file on it
  ok   A1 the checkout never moved
  ok   A1 the lane branch still holds the worker's commit
  ok   A1 the lane's tree is clean — the rebase was undone
B. the PRD lands blocked with the reason
  ok   B1 the PRD is blocked, not claimed
  ok   B1 ...and no worker still holds it
  ok   B1 the body carries the reason
  ok   B1 ...naming the conflicting file
  ok   B1 ...and the lane branch
  ok   B1 collect said what it wrote
B. the scan shows it
  ok   B2 the scan names the PRD blocked on one line
  ok   B2 ...and says it is waiting on a person
B. unblock takes it back to specced
  ok   B3 unblock exits 0
  ok   B3 the PRD is specced
C. no conflict, no block
  ok   C1 collect exits 0
  ok   C1 the PRD is done
  ok   C1 the worker's code landed
  ok   C1 nothing was written about a block
Z. hygiene
  ok   Z no fixture committed a lane worktree dir

21 checks · 21 pass · 0 fail

spec02: exit 0
spec02 ok
