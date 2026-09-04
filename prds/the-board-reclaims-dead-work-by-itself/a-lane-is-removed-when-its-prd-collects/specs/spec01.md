---
complexity: 14
footprint:
  - resources/board/lanes.py
---

# spec01 — `lanes.spent`/`lanes.drop_if_spent`, and `pearde lanes` reads the same predicate over the backlog

Nothing on this board could tell a lane that merely finished from one still
being worked, so nothing ever dropped the first kind. This unit adds the one
predicate that tells them apart — `spent(board, repo, slug, feet=None)`:
`(True, "")` when nothing is standing uncommitted in the lane (outside its
PRD's own footprint, when `feet` is given) and nothing on its branch the
checkout has not merged; `(False, <reason>)` naming exactly what still holds
it — and `drop_if_spent`, which removes the worktree when `spent` clears it
and says so in one line, or says why it kept it. Both are read-only unless
`spent` already cleared the lane: the PRD's own constraint, "this must not
become a second way to lose work," is `spent`'s two checks and nothing else.

`pearde lanes [--board <path>] [--apply]` runs the same predicate over
every lane the board already holds — the backlog spec02 does not reach,
since `collect` only ever sees the one PRD it is closing. Read-only by
default, one line per lane naming it spent or kept and why; `--apply`
removes what is spent. A lane whose slug no PRD claims any more is checked
the same way, with no footprint to spare it.

What already stands (built and probed in this pass, uncommitted in the
lane):

- `spent` and `drop_if_spent` in `resources/board/lanes.py`, `feet` an
  optional list of footprint paths excluded from the "uncommitted" count —
  the PRD's own in-progress edit is not yet a reason to call its lane
  un-droppable, since a real collect commits and merges it whole.
- `cmd_lanes`, exposed as `COMMANDS = {"lanes": cmd_lanes}` — routed by
  `pearde.py`'s own discovery, no edit to that file. Declared with
  `planlib.Flags(("board",), ("apply",))` and `translib.Args`, the same
  parser every other command in this tree uses.
- Bootstrap: `lanes.py` now finds `pearde_path`, `plan` and `transitions`
  itself, on the pattern `collect.py` already carries — needed once its
  top level imports them, and it did not before.

## Acceptance

- [x] `spent(board, repo, slug)` returns `(False, "no lane")` for a slug
  with no worktree, `(True, "")` for one with nothing standing and nothing
  unmerged, `(False, "<n> uncommitted: <paths>")` for one holding
  uncommitted paths, and `(False, "<n> commit(s) the checkout has not
  merged")` for one committed but not yet landed
  - proof `probe/spent_test.py` on the lane: `ok no lane: (False, 'no lane')` · `ok empty lane is spent: True` · `ok dirty lane names the path: True` (`1 uncommitted: stray.txt`) · `ok unmerged lane says how many: '1 commit(s) the checkout has not merged'`
- [x] `spent(board, repo, slug, feet=[...])` excludes every path inside
  `feet` from the uncommitted count and list; a lane dirty ONLY inside
  `feet` reads as `(True, "")`
  - proof same run, section 3b (added this pass — the earlier probe had no `feet` check at all): `ok dirty only inside feet is spent (dir foot): (True, '')` · `ok ... (exact foot): (True, '')` · `ok no feet, the same lane is not spent: False` · `ok a path outside feet still keeps it: (False, '1 uncommitted: other.txt')`. The exact-foot row FAILED first — `(False, '1 uncommitted: src/')` — and `dirty()` was fixed to `-z -uall`; see `## Findings` in the report
- [x] `drop_if_spent` removes the worktree and returns `"lane
  lane/<slug> removed, branch kept"` when `spent` clears it, `""` when
  there was no lane, and `"lane kept — <reason>"` otherwise, without
  touching the worktree
  - proof same run: `ok empty lane drops: 'lane lane/p2 removed, branch kept'` · `ok empty lane gone: False` · `ok branch kept: True` · `ok no lane says nothing: ''` · `ok unmerged lane is kept: 'lane kept — 1 commit(s) the checkout has not merged'` · `ok dirty lane still there: True` · `ok the byte survives: 'worker wandered\n'`
- [x] `pearde lanes` prints `lanes: <n>` for `<n>` lanes found, one line
  each reading `spent — \`--apply\` removes it` or `kept — <reason>`, is
  read-only with no flag, and is listed in `pearde help`
  - proof `probe/verify.sh` section E: `ok E1 routed with no edit to pearde.py` · `ok E1 the dirty lane is kept, with the reason` · `ok E1 the empty lane is spent` · `ok E2 it is in the help`. And on the lane itself: `python3 $LANE/resources/pearde.py help | grep lanes` → `  pearde lanes                 \`lanes [--board <path>] [--apply]\` — every lane…`
- [x] `pearde lanes --apply` removes every lane its own read found spent,
  leaves every kept lane and its uncommitted bytes exactly as they stood,
  and prints `lanes: <n> · <k> removed`
  - proof `probe/verify.sh` section E3: `ok E3 --apply removed exactly one` · `ok E3 the spent lane is gone` · `ok E3 the lane holding work is still there` · `ok E3 and its byte survived`

## Verify and Proof

```sh
# The tree holding this unit's build: a worker in a lane exports PEARDE_ROOT;
# `collect` runs this block with the code repo as cwd, after the merge landed
# it there, and `--git-common-dir` names that repo absolutely from a linked
# worktree as well as from the checkout itself.
LANE="${PEARDE_ROOT:-$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")}"
LANE_REPO="$LANE" python3 /Users/feb/dev/infra/pearde/.pearde/prds/the-board-reclaims-dead-work-by-itself/a-lane-is-removed-when-its-prd-collects/probe/spent_test.py
python3 "$LANE/resources/pearde.py" doctor "$LANE" 2>&1 | grep -q "\`lanes\` is claimed by both" && exit 1 || true
python3 "$LANE/resources/pearde.py" lanes --help
grep -qF 'def spent(board, repo, slug, feet=None):' "$LANE/resources/board/lanes.py"
grep -qF 'COMMANDS = {"lanes": cmd_lanes}' "$LANE/resources/board/lanes.py"
```
