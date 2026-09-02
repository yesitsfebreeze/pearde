---
complexity: 4
footprint:
  - pearde/.gitignore
---

# spec03 — the session tree and its ledger are not dirt on the board branch

The board is its own git worktree on branch `pearde`, and its `.gitignore`
names every machine-local path under it one row at a time — `.lanes/` for a
worker's worktree, `.state/serve.json` for the daemon's registration.
`spec01` adds two paths of exactly that kind and neither has a row, so both
show as untracked on the board branch the moment a session takes a tree.

`.sessions/` matters more than the tidiness: each entry under it is a git
repository of its own, so a person's `git add -A` on the board branch gets
`warning: adding embedded git repository` for every live session — the
identical failure the `.lanes/` row exists to prevent, and its comment says
so in as many words.

Two rows, written in the voice of the ones around them:

    # a run session's own worktree, checked out here while the session holds
    # it. Each is a git repository of its own — the same reason .lanes/ is
    # here.
    .sessions/

and, in the machine-local block beside `.state/serve.json`:

    .state/sessions.json

**Where this file is, and who commits it.** `pearde/.gitignore` is on the
board branch, not the code branch: the code repo's own `.gitignore` holds
`/pearde/` out, a lane sparse-checks the board out of its worktree, and
`pearde collect` commits the code repo's footprint and not this. So the edit
is made against the board directory by absolute path and lands on the board
branch with the rest of the board's own history — not through the merge that
carries spec01 and spec02. An implementer that assumes `collect` will commit
this file will report it done and leave it uncommitted.

## Acceptance

- [x] `pearde/.gitignore` carries a `.sessions/` row with a comment saying each entry is a git repository of its own
- [x] `pearde/.gitignore` carries a `.state/sessions.json` row in the machine-local block
- [x] `git -C pearde check-ignore -v .sessions` names the new row
- [x] `git -C pearde check-ignore -v .state/sessions.json` names the new row
- [x] `git -C pearde status --short` shows neither path after a `pearde session take`
- [x] no row already in that file is changed or reordered

## Verify and Proof

```sh
B="$(git rev-parse --show-toplevel)/pearde"
# the trailing slash matters: `.sessions/` is a directory pattern, and
# check-ignore reads a bare `.sessions` as a file whenever the directory is
# not on disk — which it is not between sessions.
git -C "$B" check-ignore -v .sessions/
git -C "$B" check-ignore -v .state/sessions.json
if git -C "$B" status --short | grep -E '\.sessions|sessions\.json'; then
  echo "still dirt"; exit 1
fi
```
