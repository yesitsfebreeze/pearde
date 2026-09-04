---
complexity: 3
footprint:
  - resources/board/collect.py
---

# spec01 — the lane stages what stands, never the whole footprint

`land_lane` commits the lane's standing dirt before merging it. Today it
gates on the standing paths inside the footprint but stages the whole
footprint union — so a path the lane's own commits already deleted (the
lane IS the work that deleted it) is an untracked pathspec, and
`fatal: pathspec '<path>' did not match any files` aborts the whole
collect. What stands, staged; what the merge already carries, left to the
merge.

What already stands: the fix is built and green in the working tree —
`land_lane` computes `mine = sorted({p for p in standing if inside(p,
feet)})` and runs `git add -A -- *mine` instead of `git add -- *feet`, with
the comment naming why `-A` is not what carries a committed deletion. Left
to finish: nothing in `collect.py`; the verify below must hold on the
merged tree, and the two held PRDs
(`the-skills-fold-into-one-index`, `the-template-twins-fold-into-the-reference`)
must collect with nothing re-implemented.

Measured facts this spec rests on (git 2.55.0, this machine): `git add -A
-- <a gone-untracked pathspec>` fails exactly like plain `--`; `git add --
<a worktree-deleted still-tracked path>` stages the removal; a committed
deletion needs no staging at all — the merge carries it.

## Acceptance

- [x] a fixture PRD whose lane deletes a footprint file and modifies a
      sibling collects: the staging call names only the standing
      intersection, and the collect's commits carry both the deletion and
      the modification — `reproduce.py` prints `delete=True: landed. the
      collect's commits carry: D resources/install.sh / M
      resources/keep.txt`
- [x] dirt outside the footprint is still left in the lane, never staged — `reproduce.py`: `outside dirt stays outside`
- [x] a fixture PRD whose lane only modifies a footprint file collects
      unchanged from the pre-fix behaviour — `reproduce.py`: `delete=False:
      landed. the collect's commits carry: M resources/install.sh`
- [x] a fixture PRD whose lane holds a STAGED (uncommitted) deletion
      of a main-tracked footprint path collects: the staging set drops
      the gone path, and the merge's own commit carries `D <path>`
      alongside the standing modification — `staged.py`: `LANDED. range:
      'D resources/gone.txt / M resources/keep.txt'` then `PASS`

## Verify and Proof

```sh
python3 .pearde/prds/a-collect-stages-a-deleted-footprint-path-as-a-deletion/probe/reproduce.py
python3 .pearde/prds/a-collect-stages-a-deleted-footprint-path-as-a-deletion/probe/staged.py
```