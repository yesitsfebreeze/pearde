---
complexity: 10
footprint:
  - resources/board/collect.py
---

# spec02 — a successful collect drops the lane it just landed

`collect_one` merges a PRD's lane and commits the record, but nothing
after that asked whether the lane it just finished with was still needed.
This unit calls `lanes.drop_if_spent` once the record commit has landed —
after `land_session`, so a crash between the merge and here still leaves
the worktree standing rather than gone with no commit to show for it — and
folds what it says into the same progress line `collect` already prints,
so a person reading one line learns the lane went with the merge, the same
way they already learn the commit did. `--dry` says what a real run would
do without touching the lane: spent when nothing inside the PRD's own
footprint is the only thing left dirty in it, kept and why otherwise.

What already stands (built and probed in this pass, uncommitted in the
lane):

- `collect_one`'s success path: `lane_note = laneslib.drop_if_spent(board,
  repo, rel)` right after `land_session`, folded into `extra` on the
  progress line — `""` (and so nothing added) for a PRD that never held a
  lane.
- `land_lane`'s own `--dry` branch: alongside its existing "would merge"
  line, one more naming whether the lane would end up removed — `not
  outside` (nothing standing outside the PRD's footprint) — or kept, and
  why, without querying git for anything the merge preview had not
  already read.

## Acceptance

- [x] a PRD collected from a lane holding only its own footprint's commits
  and nothing else standing: the lane's worktree and registration are
  gone after `collect`, its branch is kept and shows merged, and the
  progress line names the branch removed
  - proof `probe/verify.sh` section A: `ok A0 the lane is on disk before collect` · `ok A1 collect exits 0` · `ok A1 the worker's code is in the checkout` · `ok A2 the lane directory is gone` · `ok A2 the registration went with it` · `ok A2 collect said so on its line` · `ok A2 ...and said the branch is kept` · `ok A3 the branch is kept` · `ok A3 ...and it is merged`
- [x] a PRD collected from a lane also holding a path outside its
  footprint: the lane is still on disk after `collect`, the byte no
  commit holds survives untouched, and the line names the path and says
  the lane was kept
  - proof section B: `ok B1 collect exits 0` · `ok B1 the PRD is done` · `ok B2 the lane is still on disk` · `ok B2 the byte no commit holds survived` · `ok B2 collect said why it kept it` · `ok B2 ...naming the path`
- [x] `collect --dry` on a lane whose only standing path is inside the
  footprint prints a line containing "would remove the lane"; nothing on
  disk moves and the PRD's state is unchanged
  - proof section C: `ok C1 dry exits 0` · `ok C1 the lane is untouched` · `ok C1 the PRD did not move` · `ok C1 dry says it would remove it`
- [x] a PRD whose claim cut no lane collects exactly as before this unit —
  nothing in the output mentions a lane
  - proof section D: `ok D1 collect exits 0` · `ok D1 the PRD is done` · `ok D1 nothing said about a lane`. Whole run after the `dirty()` fix: `33 checks · 33 pass · 0 fail`

## Verify and Proof

```sh
# The tree holding this unit's build: a worker in a lane exports PEARDE_ROOT;
# `collect` runs this block with the code repo as cwd, after the merge landed
# it there, and `--git-common-dir` names that repo absolutely from a linked
# worktree as well as from the checkout itself.
LANE="${PEARDE_ROOT:-$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")}"
PEARDE_ROOT="$LANE" bash /Users/feb/dev/infra/pearde/.pearde/prds/the-board-reclaims-dead-work-by-itself/a-lane-is-removed-when-its-prd-collects/probe/verify.sh
grep -qF 'laneslib.drop_if_spent(board, repo, rel)' "$LANE/resources/board/collect.py"
```
