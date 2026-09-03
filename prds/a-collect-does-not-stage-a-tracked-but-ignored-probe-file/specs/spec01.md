---
complexity: 6
footprint:
  - resources/board/collect.py
---

# spec01 — collect's own `git add` no longer refuses a tracked-but-ignored path

`dirty_paths()` reports a tracked file's modification or deletion
regardless of `.gitignore` — that part is fine, git never hides a tracked
path's dirt from `status`. The refusal is in the next step: `git add --
<path>` itself refuses an EXPLICIT pathspec that resolves inside an
ignored directory even when the named path is tracked, exit 1, `The
following paths are ignored by one of your .gitignore files`. Collect's
`git_out` turns that non-zero exit into a `Stop`, which aborts the whole
PRD's commit for that repo — not only the one path.

This is not hypothetical: `.pearde/.gitignore` gained `prds/**/probe/`
after dozens of probe files across other PRDs were already force-tracked
(`git -C .pearde ls-files | grep 'prds/.*/probe/'` lists them today). Any
of those, or any probe file a future worker force-adds and then keeps
editing, hits this the next time `collect` runs on its PRD: the "PRD's
own folder is the board's record: added whole, always" promise in
collect.py's own module docstring silently does not hold for a path
under an ignored directory.

Already built and probed against the real `collect.py` (imported, not
reimplemented) in this PRD's `probe/reproduce.py`: `dirty_paths()`
correctly classifies the tracked-ignored path as dirty; the unpatched
`git_out(root, "add", "--", *p["add"])` at the staging step (module-level
loop under `with private_index(roots):`, `cmd_collect`) raises `Stop`;
adding `-f` to that one call — the only site in `collect.py` where
`p["add"]` (paths already known-dirty from `dirty_paths()`, never a
fresh untracked-and-ignored file, since `dirty_paths()` never surfaces
one of those without `--ignored`) is passed to `git add` — resolves it,
staging the file, verified under `private_index` too so the scratch-index
commit-building path is covered, not just a bare working-tree `git add`.
The fix already stands in this lane's `resources/board/collect.py`,
`git_out(root, "add", "-f", "--", *p["add"])`, one line, comment
explaining why `-f` is scoped-safe there.

Not touched: the three other `git_out(..., "add", ...)` call sites in
`collect.py` (`prd_rel`, `pmd_rel` — the PRD's own directory and its
`prd.md`) and the lane-merge `git add` in `land_lane` (footprint paths, a
different set of paths entirely) — none of them showed the refusal in
the probe (adding a directory whose child is ignored does not trigger
it; only naming the ignored child itself does), and widening the fix to
paths this PRD never observed failing is not this contract's job.

## Acceptance

- [x] `git_out(root, "add", "-f", "--", *p["add"])` at the PRD-folder
      staging step in `cmd_collect` (currently line 2337) — the only
      change
- [x] `probe/reproduce.py` exits 0 against the patched file

## Verify and Proof

```sh
grep -n 'git_out(root, "add", "-f", "--", \*p\["add"\])' resources/board/collect.py
python3 .pearde/prds/a-collect-does-not-stage-a-tracked-but-ignored-probe-file/probe/reproduce.py
```
