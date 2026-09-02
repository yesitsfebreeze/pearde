---
complexity: 8
footprint:
  - resources/board/shared.py
---

# spec01 — share surveys the code checkout, not the board worktree

`pearde/` is a linked git worktree of this repo, checked out on the board's own
branch, so `git rev-parse --show-toplevel` inside it answers the board and not
the code checkout. `cmd_share` resolves the board first and then calls
`find_repo(board)`, so `trees()[0]` is the board worktree — a tree that holds no
`resources/` at all — and the real checkout at the repo root is surveyed by no
invocation that does not pass `--repo`. Measured from this PRD's lane: `trees()`
returned 30 paths and the code checkout was not one of them, while the board
worktree was printed under the label `checkout` with seven permanent
`store-only` rows it can never satisfy.

What already stands: the store, the link and revert mechanism, and the lane
enumeration are correct and need no change. What is left is which trees the
command hands them.

The checkout is the tree that holds `resources/board/`, and it is reached from
any worktree of the repo. `git worktree list --porcelain` from the board names
every worktree of this repo including the main one; the main worktree is the
right root, and the board worktree is a tree in its own right only if it holds
one of the shared patterns, which it does not.

## Acceptance

- [x] `trees()` includes the repo's main worktree whenever `share` is run from a lane, from the board, or from the checkout itself.
- [x] No tree that holds none of the shared patterns is printed at all; the board worktree stops appearing under the label `checkout`.
- [x] The label `checkout` names the tree that holds `resources/board/shared.py`.
- [x] `pearde share --repo <path>` keeps its current meaning and still overrides the resolution.

## Verify and Proof

```sh
cd "$(git rev-parse --show-toplevel)"
python3 resources/pearde.py share --json | python3 -c "
import json, os, sys
d = json.load(sys.stdin)
paths = {r['path'] for r in d['rows']}
root = os.path.realpath(os.getcwd())
assert root in paths, f'checkout {root} is surveyed by nothing: {sorted(paths)[:3]}'
labels = {r['path']: r['tree'] for r in d['rows']}
assert labels[root] == 'checkout', labels[root]
print('ok: the checkout is a tree share visits')
"
```
