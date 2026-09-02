---
memo: a-board-s-own-file-commits-in-the-board-repo
kind: invariant    # decision | note | invariant
status: decided    # open | decided | superseded
tags:
  - memo
  - kind/invariant
  - status/decided
subject: a footprint path inside a board that is its own git repo commits in the board repo, never in the code repo that ignores it
date: 2026-09-02
verify: bash resources/invariants/a-board-s-own-file-commits-in-the-board-repo.sh
prds:
  - collect-stages-the-board-s-gitignore-in-the-outer-repo-which
---
<!-- Unlike a prd.md, a memo's keys are a CLOSED set: an undeclared key is a
     typo and @resources/doctor.sh fails on it. @references/memo.md is the
     format. -->

# a-board-s-own-file-commits-in-the-board-repo — a footprint path is filed under the repo that holds it

## Decision

A `footprint:` path is spelled relative to the **code** repo. A path that
resolves inside a board which is **its own git repo** is committed in the
**board** repo, under its board-relative name. It is never staged in the code
repo, which ignores the board and holds no such path, and it is never staged
in the lane, which `lanes.create` cuts deliberately without the board.

Where the board is not its own repo — the flat `.pearde/` layout, `board_root`
and `repo` the same root — nothing is rerouted and the behaviour is what it
always was.

One function answers which repo holds a path, and all three places that ask go
through it:

```
foot_root(p, board, board_root, repo) -> (root, path)
```

- `sort_paths` groups the path under that root and checks its existence there,
  so step 4 commits the board's own file in the board repo.
- `owned_by` fences the same way, so a verify block's guard and the commit
  agree on whose a path is.
- `land_lane` drops a board-owned path from the lane's `git add` and names it
  on one line.

Three call sites and one definition, because the failure mode of two spellings
is that the guard fences a path the commit files elsewhere, and neither is
wrong on its own.

## Why

`pearde session` needed a row in the board's own `.gitignore`, so a spec's
`footprint:` named `pearde/.gitignore`. That is the honest spelling — the
footprint is code-repo-relative and the board sits at `pearde/` — and it is
a path the code repo neither tracks nor holds, because since 2026-09-02 the
code repo's `.gitignore` carries `/pearde` and the board is a git repo of its
own.

Two things followed, and the probe watched both.

`land_lane` runs `git add -- <every footprint path>` in the lane, a worktree
of the code repo cut without the board. git answers `fatal: pathspec
'pearde/.gitignore' did not match any files` — and `git add` aborts the whole
add on one bad pathspec. So **nothing** was staged, nothing committed, the
lane never merged, and every PRD gated behind that lane stalled. One
unmatchable path in a footprint took down a merge that had nothing else wrong
with it.

Past that, `sort_paths` filed the path under the code repo, whose `git status`
never reports it. The board's own edit would have been committed nowhere at
all — it would have sat dirty on the board branch for ever, invisible to the
step that is supposed to land it.

The rule is worth an invariant rather than a comment because it regresses
**silently in one direction only**. The flat layout stays green through the
regression: its two roots are one, so no reroute is needed and none is missed.
Only the nested layout goes red, and the nested layout is the one this repo
itself runs. A check that read the live tree would be measuring the very board
it runs on, so the script builds three git repos and a worktree in a
`mktemp -d` removed on exit, and asserts arithmetic about the tool instead.

## Alternatives considered

**Making the lane's `git add` tolerant of an unmatched pathspec** — add each
path on its own, skip the ones git refuses. It fixes the symptom of the abort
and keeps the disease: the board's own file is still filed under the wrong
repo and still committed nowhere. It is also a wider contract than this one,
because a footprint naming a file the worker never created is the same abort
for a different reason. That class stays open and is reported, not fixed here.

**Forbidding a footprint path under the board** — refuse the spec at
`specced` time and make the author spell it some other way. There is no other
way to spell it: the board's `.gitignore` is a real file a real spec has to
own, and a rule that says "do not contract this" leaves the work undone. A
gate that refuses the only correct input is a gate against the wrong thing.

**Teaching each of the three call sites its own answer** — the shape the code
was already in, minus the routing. It is what let `owned_by`'s fence and
`sort_paths`' grouping drift apart in the first place, and the drift is not
visible in any test that runs one of them.

**Making the lane carry the board** — check out the board into the worktree so
`git add` finds the path. `lanes.create` excludes it on purpose: a lane that
carries a stale copy of the board makes every board command run from inside it
resolve to a phantom, measured as `pearde scan` printing `0 PRDs` against a
live board holding one. Silently. That cure is worse than the abort.

## Consequences

- A spec author writes the footprint the one way there is —
  `pearde/<file>`, relative to the code repo — and `collect` decides where it
  lands. @references/parts/commits.md carries the rule in prose, so the
  expectation is readable before the merge rather than after it.
- The board's own file lands in the board's commit, beside the PRD's record.
  A reader looking for it in the code repo's history will not find it, and
  should not.
- The invariant script copies `resources/` to a scratch dir to run a
  substituted `collect.py`, because `collect.py` imports its siblings from
  its own directory and a lone copy cannot run. That is about three megabytes
  and a `cp -R` per run, not a per-call cost.
- It does not fix the wider abort: `git add -- <feet>` still fatals on any
  footprint path the lane does not hold for any other reason. This removes
  only the board-owned class.
- It does not make sibling contention visible inside the board repo.
  `sort_paths` builds its `others` list only for paths under `repo`, so two
  PRDs whose footprints share a path under the board are not detected as
  contending. Reported, not closed here.
