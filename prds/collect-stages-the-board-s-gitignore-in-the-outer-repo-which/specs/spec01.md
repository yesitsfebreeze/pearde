---
complexity: 8
footprint:
  - resources/board/collect.py
---

# spec01 — a footprint path is filed under the repo that holds it

`collect` spells every footprint path relative to the code repo and files it
there. Since the board became a git repo of its own, a path under the board is
spelled `pearde/<file>` and lives in neither the code repo's index nor its
worktree — the code repo ignores the board — so `git add -- pearde/.gitignore`
is `fatal: pathspec … did not match any files`. `git add` aborts whole on a bad
pathspec, so the lane's commit never happens and every PRD gated behind it
stalls. This unit gives collect one answer to which repo holds a path, and uses
it in all three places that ask.

`foot_root(p, board, board_root, repo)` returns `(root, path)`: the board's
root and the board-relative spelling when the path resolves inside a board
whose root is not the code repo's, and `(repo, p)` unchanged otherwise — so a
board that is not its own repo, where the two roots are one, keeps the
behaviour it had. Its three callers:

- `sort_paths` groups the path under that root, and checks its existence
  there, so step 4 commits the board's own file in the board repo.
- `owned_by` fences the same way, so a verify block's guard and the commit
  agree on whose a path is.
- `land_lane` drops a board-owned path from the lane's `git add` and names it
  on one line — the lane is cut without the board (`lanes.create` excludes it
  by sparse-checkout) so that path was never the lane's to stage.

**What already stands**, uncommitted in this PRD's lane: `foot_root` and all
three call sites, plus `owned_by`'s new trailing `board` parameter and the one
caller that passes it. **What is left**: read the diff, run the checks below,
and commit. Nothing else in `collect.py` is this unit's to touch.

## Acceptance

- [x] `foot_root` is defined in `resources/board/collect.py`, and
      `sort_paths`, `owned_by` and `land_lane` each call it — no fourth
      spelling of the rule anywhere in the file
- [x] on the nested layout — a code repo that ignores its board, a board that
      is its own repo, a spec whose footprint names both a code file and
      `pearde/.gitignore` — `collect` exits 0 and the board repo carries a
      commit holding `.gitignore`, with the board's working tree clean after
- [x] the same run against a copy of the tree whose `foot_root` routes
      nothing exits 1 on `fatal: pathspec 'pearde/.gitignore' did not match
      any files` — the check is watched failing, not assumed to be able to
- [x] on the flat layout — a `.pearde/` board inside the code repo and not a
      repo of its own — `collect` exits 0 and no path is rerouted, unchanged
      from before

## Verify and Proof

```sh
grep -q "^def foot_root" resources/board/collect.py
test "$(grep -c 'foot_root(' resources/board/collect.py)" -ge 4
F=pearde/prds/collect-stages-the-board-s-gitignore-in-the-outer-repo-which/probe/fixture.py
python3 "$F" --check
python3 "$F" --mutant
```
