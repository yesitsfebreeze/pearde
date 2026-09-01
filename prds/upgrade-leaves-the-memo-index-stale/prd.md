---
state: done
origin: derived
from: seven-closed-probes-drifted-red/init-seeds-a-board-doctor-calls-green
priority: 0
complexity: 9
blast-radius: low
repo:
needs:
footprint:
  - resources/board/init.py
workflow: probe-then-spec
actual: 0.81h
commit: 030b80d bc1c589
---

# upgrade-leaves-the-memo-index-stale — `init` now regenerates the memo kind-index and `upgrade` still does not, so an upgraded board fails the check a fresh one passes

`cmd_upgrade` and `cmd_init` share `plant_graph` as of `4735940`, but not
`index_memos`. A board created by `init` lands with a current
`memos/README.md`; a board brought forward by `upgrade` keeps whatever index it
had, and `upgrade` then runs `knowledge.py board` over memos it did not index.

## The requested PRD this gets wrong

`seven-closed-probes-drifted-red/init-seeds-a-board-doctor-calls-green` — its
contract is "a fresh `init --example` board passes doctor", and it is `done`.
The sibling path is not covered by it and now diverges: the same board reaches
`memos broken` through `upgrade` and green through `init`. Anyone who upgrades
an existing install gets the failure the requested PRD exists to remove, from
the command whose whole job is to bring a board current.

## Why it is filed `deferred` and not `open`

@references/parts/derived.md — a defect a worker reports outside its scope is
the orchestrator's call, and neither a derived PRD nor a memo is `open` by
default. It is a PRD rather than a memo because fixing it changes what ships,
not how loudly the board notices: an upgraded board is genuinely red.

Widening `init-seeds-a-board-doctor-calls-green` to cover `upgrade` would have
been REFINE, not initiative, and both its analyst and its implementer correctly
declined to do it. This file is where that decision goes so it is not lost.

## What is known

- One line closes the behaviour: `index_memos(board)` beside the
  `write_knowledge` call in `cmd_upgrade`.
- Reproduced twice, independently, on 2026-09-01: delete `memos/README.md` and
  `graph.json` from a board, then `init --example` repairs **neither** and
  `upgrade` repairs the graph and **not** the index. Doctor is not green after
  either.
- The real cost is not the line, it is the proof. Every acceptance box on this
  board is now held to `memos/one-author-is-not-an-accepted-spec.md` — ticked
  only against a predicate seen red — and `memos/a-check-decided-by-scheduling.md`
  governs any check that binds a port or stands down.

## Two neighbours worth reading first

- `ignore_patterns("README.md")` in `write_board` is directory-blind. It drops
  the example board's own README and also `memos/README.md`, and will drop any
  future `README.md` at any depth. Regenerating the index is the right answer
  for a generated page; the glob is still a latent bug and the next file it
  eats will be a different one.
- `resources/index.py`'s manifest rules do not ignore an untracked
  `node_modules/`. A sibling's playwright install made `index.py check` print
  115 lines and exit 1, which reddens `doctor`'s `index` row, the gate, and the
  `readme-in-three-rings` harness all at once. Whether the map should ignore it
  is a real question and belongs to whoever owns that drop.

## Report

spec01: exit 0
764:    indexed = index_memos(board, "upgrade")
resources/board/init.py compiles
A. the old shape is red before anything touches it
  ok    A the copy landed a memo
  ok    A ...and no index beside it
  ok    A memo check exits 1 on it
  ok    A ...calling the kind index stale
  ok    A doctor's memos row reads broken
B. upgrade regenerates the index
  ok    B upgrade exits 0
  ok    B ...and says it regenerated the page
  ok    B memos/README.md is on the board
  ok    B memo check exits 0
  ok    B ...and says nothing
  ok    B the page is the generated one, not a copied one
  ok    B ...and byte-identical to the example board's own page
C. an upgraded board is as healthy as a fresh one
  ok    C doctor exits 0 on the upgraded board
  ok    C ...and closes green
  ok    C the memos row reads ok
  ok    C the knowledge row reads ok
  ok    C the fresh board's init regenerated its index too
  ok    C the row reader read the whole report — 18 rows, not zero
  ok    C no row reads broken on either board
  ok    C every other row's verdict matches the fresh board's
  ok    C ...and the two boards' index pages are the same bytes
D. a second upgrade is additive — it rewrites nothing
  ok    D upgrade exits 0 again
  ok    D ...and the row says the index is already current
  ok    D ...and the page is the same bytes
E. a board with no memo gets no page written over nothing
  ok    E upgrade exits 0
  ok    E ...and says there is nothing to index
  ok    E memos/ holds no generated index
  ok    E doctor calls the empty board green
F. the check can fail — take the call back out and the red returns
  ok    F the mutation reached the copy
  ok    F an upgrade without the call leaves memo check failing
  ok    F ...and doctor's memos row broken
  ok    F ...and the copy is restored
G. a failing index is said, and names upgrade rather than init
  ok    G the failing-index mutation reached the copy
  ok    G the failure is said, not swallowed
  ok    G ...naming what memos.py reported
  ok    G ...and it does not name the wrong command
  ok    G ...and the copy is restored
H. nothing of this machine's was written to
  ok    H no fixture of this run reached the live daemon's board list
  ok    H no fixture of this run reached Obsidian's vault list
  ok    H ...and the vault list is byte-identical, so no session wrote it

40 checks · 40 pass · 0 fail · 0 skip
41 checks · 41 pass · 0 fail · 0 skip
78 checks · 78 pass · 0 fail
74 checks · 74 pass · 0 fail
96 checks · 96 pass · 0 fail
index ok
