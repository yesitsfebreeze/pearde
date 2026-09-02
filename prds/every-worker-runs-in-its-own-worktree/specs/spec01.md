---
complexity: 9
footprint:
  - resources/board/lanes.py
  - references/files.md
---

# spec01 — the lane library

One module holding everything a worktree-per-worker needs: cut a lane, drop
it, merge it back, read what stands in it. Every other spec calls this one
and none of them shells out to `git worktree` itself.

**What stands** — `resources/board/lanes.py` is in the tree from the probe,
with `branch_of`, `lane_dir`, `git`, `exists`, `create`, `remove`, `merge`,
`conflicts`, `dirty`, `commit_all`, `list_lanes`. `create` cuts the
worktree, `merge` aborts a conflict and raises `LaneError` naming the
files. Proven in a fixture repo: a lane cut, committed, merged; a conflict
came back red naming `src/a.py` with the checkout left where it was.

**What is left** — three things the probe proved are needed and did not do:

1. `create` must materialise the lane **without the board dir**. When the
   code repo tracks its board, the lane checkout carries a stale copy of
   `.pearde/`, and a worker running any board command from its lane
   resolves to that phantom board — measured: `pearde scan` from inside a
   lane printed `0 PRDs` against a live board holding one. `git worktree
   add --no-checkout`, then `git sparse-checkout set --no-cone '/*'
   '!/<board-rel>'`, then `git checkout`, fixes it; the excluded path keeps
   its skip-worktree bit, so a later `git add -A` in the lane does not
   delete the board from the tree (measured: it did not).
2. `merge` must land the lane as **one** commit and leave the branch
   reading merged. A plain `git merge` onto a checkout that moved writes a
   merge commit on top of the lane's, which is two commits for one PRD.
   Rebase the lane onto the checkout's branch, then `merge --ff-only`:
   measured linear, one commit, and `git branch --merged` listed the lane.
   A rebase conflict is the same red as a merge conflict — the files, and
   the lane branch left as it was.
3. The manifest row. `resources/index.py check` went from green to
   `resources/board/lanes.py is on disk with no row in references/files.md`
   the moment the file landed.

## Acceptance

- [x] `resources/board/lanes.py` exists and imports on Python 3 stdlib alone
- [x] `lanes.create` leaves no board directory inside the lane when the code repo tracks one
- [x] `lanes.merge` lands one commit on the checkout's branch even when the checkout moved since the lane was cut
- [x] after `lanes.merge`, `git branch --merged` lists the lane branch
- [x] `lanes.merge` on a conflicting lane raises `LaneError` naming the conflicting file and leaves the checkout at the commit it was on
- [x] `lanes.remove` drops the worktree and keeps the branch
- [x] `references/files.md` carries a row for `resources/board/lanes.py`
- [x] `python3 resources/index.py check` prints nothing

## Verify and Proof

```sh
python3 -c "import sys; sys.path.insert(0,'resources/board'); import lanes; \
print(lanes.branch_of('a/b'))" | grep -qx 'lane/a-b'
grep -q 'resources/board/lanes.py' references/files.md
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
printf '%s\n' "$out"
if printf '%s\n' "$out" | grep -E '(^|@)(resources/board/lanes\.py|references/files\.md)([ ,:]|$)'; then exit 1; fi
```
