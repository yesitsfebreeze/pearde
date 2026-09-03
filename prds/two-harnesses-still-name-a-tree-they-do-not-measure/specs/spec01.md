---
complexity: 8
footprint:
  - prds/every-run-session-works-in-a-worktree-of-its-own/probe/verify.sh
  - prds/every-run-session-works-in-a-worktree-of-its-own/a-session-ledger-names-who-holds-what-and-reaps-what-is-gone/probe/verify.sh
  - prds/resources-are-organised-by-responsibility/probe/verify.sh
  - prds/resources-are-organised-by-responsibility/every-module-finds-its-siblings-by-one-rule/probe/verify.sh
  - prds/two-harnesses-still-name-a-tree-they-do-not-measure/probe/verify.sh
---

# spec01 — the four harnesses that were still rooting themselves take their root from the runner

`a-harness-measures-the-tree-its-worker-built-in` rooted sixty-five harnesses
in the runner and came back `BLOCKED` on two it was forbidden to touch. Two
more have landed since, so the set is four. Each gets the same preamble the
other sixty-five carry, replacing whatever it computes its root with now:

```sh
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
BOARD="$HERE"
while [ "$BOARD" != / ] && [ "$(basename "$BOARD")" != .pearde ] && [ "$(basename "$BOARD")" != pearde ]; do BOARD="$(dirname "$BOARD")"; done
ROOT="${PEARDE_ROOT:-$(dirname "$BOARD")}"
```

Four different defects, one edit each:

| file | what it did | what changes |
|---|---|---|
| `every-run-session-…/probe/verify.sh` | hardcoded `LANE=/Users/feb/dev/infra/pearde/pearde/.lanes/every-run-session-…`, read no root at all | gains the whole preamble; `LANE` defaults to `$ROOT` |
| `…/a-session-ledger-…/probe/verify.sh` | read `PEARDE_ROOT` but fell back to `$HERE/../../../../..` | the count of `..` becomes the board walk |
| `resources-are-organised-…/probe/verify.sh` | read `PEARDE_ROOT` but fell back to `$HERE/../../../..` | the same, one level shallower |
| `…/every-module-finds-its-siblings-by-one-rule/probe/verify.sh` | a `find_root` that walked up for `resources/pearde.py`, **preferring `$PWD`** | the board walk, and the `$PWD` preference goes |

The fourth is not a counting bug and deserves its reason written down. Its
`find_root "$PWD"` made a by-hand run resolve a different tree depending on
where it was started from — measured: from the `resources-are-organised-by-responsibility`
lane it reported `tree …/.lanes/resources-are-organised-by-responsibility`,
where its sibling reported `tree /Users/feb/dev/infra/pearde`. `spec01` of the
parent PRD settles which is right: "`ROOT` is the runner's tree when it names
one, that board's repo otherwise — the walk-up survives as the fallback, so a
harness run by hand from anywhere behaves as it does today." The runner names
the root; cwd does not.

**The session harness's green was the defect, and it goes red here.** Before
this edit `every-run-session-…/probe/verify.sh` exited `0` from the
orchestrator's checkout — because it read `sessions.py` out of a lane it named
in the file, never out of the tree it was run against. `resources/board/sessions.py`
does not exist in the checkout; it exists only in that PRD's lane. Rooted, the
harness exits `10` with `ModuleNotFoundError: No module named 'sessions'`, and
exits `0` again under `PEARDE_ROOT=<that lane>`. That is the whole point of
the parent PRD, arriving as a number: a box that was ticked on a tree holding
none of the work now says so. The other three keep their counts exactly —
`1` failure, `20 passed 1 failed`, `3 passed 20 failed`, before and after.

**Already standing (this analyst's uncommitted pass one):** all four files
carry the preamble and `probe/verify.sh` reports `27 passed, 0 failed`. What is
left for an implementer is to re-run it, confirm the three unchanged counts,
and stage the five files in the board repo — all four are untracked there and
belong to PRDs whose lanes are live, so `collect` must stage them whole rather
than by hunk.

**The verify is scoped to these four on purpose.** The parent PRD's
`probe/verify.sh` asserts the whole harness population with no exception list.
It reported `69 harnesses` at the start of this pass and `70` at the end — a
fifth landed from another lane while these four were being edited, and it is
red on that one now. A verify command another lane can redden is not a check
on this unit's work; the population census stays the parent PRD's problem.

## Acceptance

- [x] All four files carry the board walk: `basename "$BOARD"` appears in each. — `grep -cF 'basename "$BOARD"'` prints `1` for every one of the four, in footprint order.
- [x] All four read `${PEARDE_ROOT:-` — none computes its root without consulting the runner. — `grep -cF '${PEARDE_ROOT:-'` prints `1` for each, and the line is `ROOT="${PEARDE_ROOT:-$(dirname "$BOARD")}"` in all four (lines 16, 21, 22, 28).
- [x] No file in the footprint counts `..` to reach the repo, and none names `/Users/feb/dev/infra/pearde`. — the four print `0` and `0` for both greps. The fifth footprint file, this PRD's own probe, roots itself with the same board walk and carries the two strings only as data: line 44 is the detector's own needle, lines 100-101 are planted-defect `sed` spells applied to copies under `$TMPDIR`. Neither reaches its root computation, and the board already settles that class in `nothing-left-open/a-quoted-walk-is-data`.
- [x] `every-run-session-…/probe/verify.sh` is red from the checkout, naming the missing `sessions` module, and green under `PEARDE_ROOT` pointing at the lane that holds `resources/board/sessions.py`. — from the checkout: exit `10`, last line `verify: 10 FAIL`, five `ModuleNotFoundError: No module named 'sessions'` lines. Under `PEARDE_ROOT=<board>/.lanes/every-run-session-works-in-a-worktree-of-its-own` (which does hold `resources/board/sessions.py`): exit `0`, last line `verify: green`.
- [x] Each of the four, run with `PEARDE_ROOT` naming a scratch tree that holds none of their modules, reads that tree rather than the board's repo. — three of them print the scratch path back: `probe: a session ledger … — tree /var/folders/…/impl-tworoot.fS4DUA/fake`, `probe: resources are organised by responsibility — tree …/fake`, `probe: every module finds its siblings by one rule — tree …/fake`, each with `no …/fake/resources/board/session.py`-shaped misses under it. The session harness prints no tree line, so its own evidence is the box above: red against the checkout, green against the lane — the two trees it is pointed at decide its colour.
- [x] The other three report the counts they reported before the edit, and this unit moved none of them. — the verify block's loop prints, in that order against the ledger, `resources-are-organised-…` and `every-module-finds-its-siblings-…` harnesses: `PROBE GREEN`, `probe: 20 passed, 1 failed`, `probe: 3 passed, 20 failed`. Two are the counts the edit was measured against. The ledger's rose from `PROBE RED — 1 failure(s)` to `PROBE GREEN` (`29 passed, 0 failed`) between the first pass and this one, and the rise is not this unit's: that harness reads `$ROOT/resources/board/session.py`, and the checkout's copy was last written by `31620bb` at `2026-09-02 23:45`, hours after the harness itself was last touched (`22:03`, unmoved since). A count that rose on a harness this unit did not touch is the neighbour's landing.
- [x] `prds/two-harnesses-still-name-a-tree-they-do-not-measure/probe/verify.sh` exits 0, reports `16 passed, 0 failed`, and its section C plants each of the four defects back into a scratch copy and sees every one — so the census in section A is a check that can fail. Nothing under the board is written by the run. — exit `0`, `probe: 16 passed, 0 failed`, `C1`-`C4` each name the defect they saw (`does not read ${PEARDE_ROOT:-;counts .. to reach the repo`, `…;names an absolute root`, `does not walk up to its board`, `does not read ${PEARDE_ROOT:-`) and `C5` shows the copied-from file unchanged. A `stat` census of all 14 971 files under the board before and after the run differs on nothing but this session's own `.state/guard/<session>.json`, which moves on a no-op call too.

## Verify and Proof

```sh
# The four harnesses under measurement live on the board and are addressed
# board-relative, so the board is the cwd. It is not in the code repo — a
# worktree of it holds an empty `.pearde/` — and it moved from `pearde/` to
# `.pearde/` on 2026-09-03, so neither an absolute path nor a cwd-relative
# one survives. The board sits beside the main `.git`, which every worktree
# and the checkout alike resolve the same way.
cd "$(cd "$(git rev-parse --git-common-dir)/.." && pwd)/.pearde"
# The probe carries its own falsifiability in section C, on copies under
# $TMPDIR. This block writes nothing: an earlier draft planted a defect in
# the real harness and, aborting under `bash -e` before its restore, left the
# board holding a reverted file.
bash prds/two-harnesses-still-name-a-tree-they-do-not-measure/probe/verify.sh
# the three whose counts must not have moved, quoted back. `|| true` because
# all three are red on their own subject and that is their baseline, not a
# failure of this unit.
for h in \
  prds/every-run-session-works-in-a-worktree-of-its-own/a-session-ledger-names-who-holds-what-and-reaps-what-is-gone/probe/verify.sh \
  prds/resources-are-organised-by-responsibility/probe/verify.sh \
  prds/resources-are-organised-by-responsibility/every-module-finds-its-siblings-by-one-rule/probe/verify.sh ; do
  line="$(bash "$h" 2>&1 | tail -1 || true)"
  echo "$line  <- $h"
done
```
