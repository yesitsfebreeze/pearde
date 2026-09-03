---
state: deferred
origin: derived
from: the-doctor-refuses-drift/one-primitive-one-definition/the-core-board-modules-delegate-to-common
priority: 55
complexity: 0
blast-radius:
---

# a lanes own fast forward refuses on a laneless workers live dirt

`collect.land_lane` (`resources/board/collect.py`) rebases a lane's own
commit(s) onto the branch the checkout is on, then `lanes.merge` runs a
plain `git merge --ff-only` **directly in the shared checkout** (the taken
session's own worktree, `repo_of`'s answer) — with no `_park`-style step
first to set aside dirt the incoming commit does not own. `guarded_run`'s
own `_park`/`_snapshot` (further down the same file, used for the later
VERIFY step) exists precisely because the checkout is shared and other
workers' uncommitted work stands in it; `land_lane`'s merge has no
equivalent guard.

Consequence for two requested PRDs, both measured live this pass, both a
genuine DONE implementer report:
`the-doctor-refuses-drift/one-primitive-one-definition/the-core-board-
modules-delegate-to-common` and its sibling `…/the-lane-and-repo-modules-
delegate-to-common`. Both `collect`s refused with `merge conflict: lane/…
into session/s98669 — see git status` and **`conflicts()`
(`git diff --name-only --diff-filter=U`) named no file** — because the
failure is not a content conflict at all: `git -C
.pearde/.sessions/s98669 status --short` at the time showed 5 tracked
files dirty (`resources/board/{dispatch,plan,prdfile,silence,
transitions}.py`), live, uncommitted work belonging to a **different,
laneless, actively-claimed PRD**
(`the-board-reclaims-dead-work-by-itself/a-claim-names-the-process-that-
holds-it`, claim `an-claim-pid2`, `analyzing` — an analyst builds
directly `in <repo>` per its brief, with no lane of its own). One of the
five dirty files, `resources/board/transitions.py`, is also inside both
blocked PRDs' own `footprint:` — `git merge --ff-only` refuses a
fast-forward that would touch a file the working tree already holds
uncommitted changes to, exactly as git always does, and `lanes.merge`'s
own `Conflict` exception (raised for a REAL rebase/merge conflict
elsewhere in the same function) is the only exception type
`land_lane`/`block_conflict` know how to report — so a plain git refusal
for an unrelated reason surfaces identically, `## Blocked` naming no file
because there genuinely is no *conflicting* file, only a *dirty* one.

Likely fix: `land_lane`'s `lanes.merge` call parks the checkout's foreign
dirt (a `_park`-shaped stash of paths outside every currently-`claimed`/
`analyzing` PRD's own footprint — or more simply, of paths outside *this*
PRD's footprint specifically, since that is all the incoming commit can
touch) before the `git merge --ff-only`, and restores it after, win or
lose — mirroring what `guarded_run` already does for the verify step
later in the same function. Not measured against every PRD on the board,
only the two instances above; on a board this heavily concurrent
(multiple simultaneously-claimed, laneless, analyzing/claimed PRDs
routinely dirtying the one shared session tree), this is likely to recur
for any lane-based PRD whose footprint overlaps a laneless worker's
in-progress files.
