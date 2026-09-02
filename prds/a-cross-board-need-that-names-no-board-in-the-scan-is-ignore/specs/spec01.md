---
complexity: 8
footprint:
  - resources/board/plan.py
  - resources/board/transitions.py
  - references/parts/master.md
  - references/parts/contract.md
---

# spec01 — a cross-board need whose board is not in the scan is ignored, not held

`plan.dispatchable` and `transitions.gate_unblock` stop treating an
unresolvable `@<board>/<prd>` need as a hold when `<board>` is not a board this
scan can answer for. One helper, `plan.unscanned_need`, is the single place
that decides, and both gates plus `plan.resolve_needs`'s warning read it — so
the edges the schedule is built from and the gate every dispatcher shares give
one answer instead of two.

The narrowness is the point. A qualified need naming a board that **is** in the
scan and holds no such PRD is a typo, and still holds. A bare name naming
nothing still holds. Only the case nothing in this session can see is let
through, and it is reported on stderr as it already was.

## What already stands

All of it, uncommitted in the lane
`.pearde/.lanes/a-cross-board-need-that-names-no-board-in-the-scan-is-ignore`,
built and measured by the probe. Four files, +56/-6.

- `plan.need_board(d)` — the board a `@<board>/<prd>` entry names, or `None`.
- `plan.scanned_boards(prds, board=None)` — every member name in the scan,
  plus `board_name(board)` when the caller knows the path. A master's own PRDs
  carry `board: None`, so without that second half a need written under the
  master's own `name:` reads as a board that is not here and would be let
  through; the probe's `ownname` row is that case.
- `plan.unscanned_need(prds, d, board=None)` — `True` only when `d` names a
  board and that board is not in `scanned_boards`.
- `plan.dispatchable` — the `needs` gate `continue`s on `unscanned_need`
  before returning `needs: ... names no PRD on this board`. It passes
  `board or prd["board_path"]`, so the gate is right whether the caller
  handed it a board or not.
- `plan.resolve_needs` gained a `board=None` fourth argument, threaded from
  `compute_plan`, and now says which of the two things went wrong: `that
  board is not in this scan, ignored`, or `that board is in this scan and
  holds no such PRD`. Before, every `@`-prefixed need got the first message,
  including one into a member sitting right there.
- `transitions.gate_unblock` `continue`s on the same helper.
- `references/parts/master.md`'s `needs:` scope row and
  `references/parts/contract.md`'s `needs` row say the rule.
- `plan.dispatchable`'s docstring gate list names the exception.

Measured on the real board, 104 PRDs: `dispatchable` returns exactly the same
string for every one of them before and after. No PRD here carries a
cross-board need, so this lands as a no-op on this board and a fix on a
master.

## What is left

Nothing in the code, and nothing for the implementer to merge — the merge is
the orchestrator's act (`lanes.commit_all`: *"The worker never commits; this
is the ORCHESTRATOR closing the lane before it merges"*). The implementer
re-runs the probe both ways and the repo gate against the lane and reports.
A red there is a regression.

The collision at the merge, measured rather than predicted. The claimed PRD
`the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-dispatched-in-parallel`
is editing `resources/board/plan.py` and `resources/board/transitions.py` in
the main working tree at the same time, including `dispatchable` itself (it
removes the footprint gate). This lane was cut from `HEAD` and does not hold
that work. A three-way `git merge-file` of the two, over the common base,
gives **one conflict in `transitions.py`: none; in `plan.py`: exactly one**,
and it is four lines of docstring, not code. Both code edits — the `continue`
into the `needs` loop and the removal of the footprint block — land clean.
The resolution is to keep this lane's four docstring lines and drop the
`- footprint — overlaps a `claimed` PRD's.` row the sibling deletes:

    - needs — a `needs:` entry naming nothing, or a PRD not `done`. The
      one exception is a cross-board need whose board is not in this
      scan: nothing here can say whether it is done, so it is ignored,
      the answer `resolve_needs` already gives the schedule.
    - workflow — `workflow:` names no workflow in any library it can see;

Resolved that way, the merged pair parses, the probe is 9/9 on it, and
`dispatchable` over all 104 PRDs is byte-identical to the main checkout
without this lane — so this change is a no-op on top of the sibling's too.

## Acceptance

- [x] On a plain board, an open PRD carrying `needs: '@other/thing'` for a
  board that is not in the scan is dispatchable and unblocks, while a PRD
  carrying a bare name no board holds is still refused with `needs:` — the
  probe's `plain board` table, rows `crossboard` and `typo`.
- [x] On a master merging one member, a PRD carrying `needs: '@member/nope'`
  — the member is in the scan and holds no such PRD — is still refused, and
  one carrying `needs: '@elsewhere/thing'` is dispatchable. The probe's
  `master board, one member` table, rows `membertypo` and `absent`.
- [x] A PRD carrying `needs: '@masterboard/nope'` under the master's own
  `name:` is refused, not let through — `scanned_boards` counts the board's
  own name. The probe's `ownname` row.
- [x] `plan.resolve_needs` names the two cases apart on stderr: `that board
  is not in this scan, ignored` for `@elsewhere/thing`, and `that board is
  in this scan and holds no such PRD` for `@member/nope`.
- [x] The boxes above can fail: run against `git show HEAD:` copies of the
  two readers, at least the `crossboard` and `absent` rows go red.
- [x] `dispatchable` returns the identical string for all 104 PRDs on this
  board before and after the change — the fix is a no-op where no
  cross-board need is written.
- [x] `python3 resources/index.py` reports nothing this change introduced.
  `resources/board/edit.py references @questions.py — not on disk` stands at
  `HEAD` and is not ours.

## Verify and Proof

```sh
# the contract, and that its boxes can fail
python3 .pearde/prds/a-cross-board-need-that-names-no-board-in-the-scan-is-ignore/probe/harness.py
python3 .pearde/prds/a-cross-board-need-that-names-no-board-in-the-scan-is-ignore/probe/harness.py --vs-head

# no-op on the real board: same gate string for every PRD, before and after
python3 - <<'PY'
import subprocess, sys, tempfile, os, shutil
sys.path.insert(0, "resources/board")
import plan
b = os.path.abspath(".pearde")
prds = plan.scan(b)
for r in sorted(prds):
    print(r, "|", plan.dispatchable(prds[r], prds, b))
PY

# both gates read the one helper, and the docs carry the rule
grep -n "def unscanned_need" resources/board/plan.py
grep -c "unscanned_need" resources/board/plan.py           # 3 — def, dispatchable, resolve_needs
grep -n "unscanned_need" resources/board/transitions.py
grep -c "reported and ignored" references/parts/master.md references/parts/contract.md

# the repo gate — printed whole, gated only on lines naming this footprint.
# `index.py` exits 1 on `resources/board/edit.py references @questions.py`,
# which stands at HEAD and is not ours; `collect` runs this block under
# `bash -e -o pipefail`, so a bare call here would hand the block that exit.
out=$(python3 resources/index.py 2>&1) && rc=0 || rc=$?
[ -n "$out" ] || { echo "index.py printed nothing"; exit 1; }
printf '%s\n' "$out"
if printf '%s\n' "$out" | grep -E 'resources/board/(plan|transitions)\.py|references/parts/(master|contract)\.md'; then
  echo "index.py names a file in this footprint — a regression"; exit 1
fi
```
