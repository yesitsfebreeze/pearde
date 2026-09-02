---
complexity: 8
footprint:
  - resources/board/lanes.py
---

# spec01 — a refused rebase leaves the lane's dirt alone

`lanes.merge()` rebases the lane branch onto the checkout's branch inside
the lane's own worktree. When that rebase cannot even start — `git rebase`
refuses outright on a dirty tree, which is exactly what `land_lane` leaves
standing on paths outside a spec's footprint (`resources/board/collect.py`,
`land_lane`) — the current code still runs `git reset --hard <was>` in the
lane, on the theory that it is cleaning up a conflict. There was no
conflict: no rebase ever got under way, `git rebase --abort` fails with
"no rebase in progress" (measured: exit 128), and the `reset --hard`
destroys whatever the worker or `land_lane` left uncommitted in the lane —
silently, since `git status` reads clean immediately after and the raised
`LaneError` falls back to "see git status" with nothing left to see.

This already stands, built and verified against a clean-room reproduction
in `prds/a-refused-rebase-must-not-destroy-the-lane-it-was-left-in/probe/reproduce.sh`
(run with `LANES_PY` pointing at the lane's own copy while this spec is
still unmerged): `merge()` now only runs the `reset --hard` when `git
rebase --abort` itself reports it stopped a rebase that was actually in
progress (`returncode == 0`); when the abort fails because none was
running, the function raises `LaneError` and touches nothing else, leaving
the lane exactly as it was found. A genuine mid-rebase conflict is
unaffected — `--abort` still succeeds there and the belt-and-suspenders
reset still runs, restoring the branch and tree to the pre-rebase tip.

What already stands, and where. The guard is built in place in the
footprint file itself — a branch has no meaning outside the function it
lives in — and it stands in this PRD's lane worktree, not in the
orchestrator's checkout, which is where `collect` merges it from. The
probe now carries its own tally and its own exit, so a `FAIL` line cannot
be printed into a green run, and it takes its tree from `PEARDE_ROOT` when
the runner names one: a lane worktree holds no board, so a walk up from
`$0` always lands in the checkout and would measure a tree holding none of
the work. The temporary `echo "testing: ..."` line is gone.

Nothing is left. The block below is written for the tree `collect`
measures — the checkout, after the lane has landed — and reads
`resources/board/lanes.py` from the root it is run in.

## Acceptance

- [x] `resources/board/lanes.py`'s `merge()` runs `git reset --hard <was>`
      in the lane worktree only inside the branch where `git rebase
      --abort` returned `0` — never unconditionally after a failed rebase.
- [x] `bash prds/a-refused-rebase-must-not-destroy-the-lane-it-was-left-in/probe/reproduce.sh`
      prints `PASS` for both cases against the repo's own
      `resources/board/lanes.py` (no `LANES_PY` override needed).
- [x] A genuine mid-rebase conflict still leaves the lane branch and
      working tree at the exact commit it had before `merge()` was called
      (case 2 of the probe, unchanged behaviour).

## Verify and Proof

```sh
# the guard itself, in the footprint file: the abort's own return code is
# read, and the `reset --hard` sits inside the branch that reads it
grep -n 'aborted = git(wt, "rebase", "--abort", check=False)' resources/board/lanes.py
grep -n 'if aborted.returncode == 0:' resources/board/lanes.py
grep -q '^                git(wt, "reset", "--hard", was' resources/board/lanes.py
# ...and no `reset --hard` is left at the statement level a failed rebase
# falls through to, which is the shape that destroyed the lane
u=$({ grep -c '^            git(wt, "reset", "--hard", was' resources/board/lanes.py || true; })
[ "$u" = 0 ]
# both cases green against the repo's own resources/board/lanes.py, with no
# LANES_PY override. The probe prints a tally and ends on its own exit, so
# a printed FAIL reddens this block.
bash pearde/prds/a-refused-rebase-must-not-destroy-the-lane-it-was-left-in/probe/reproduce.sh </dev/null
```
