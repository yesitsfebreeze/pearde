# collect-must-not-reset-the-checkout-it-did-not-write — implementer report

Verdict: DONE

Pass two on this route. The build stood uncommitted in the lane from pass
one; spec02's paragraph was unwritten and both specs' `## Verify and Proof`
blocks could not fail. Both are closed. 14/14 boxes ticked, each against a
command actually run: spec01 8/8, spec02 6/6.

## What landed this pass

- `references/parts/commits.md` — the "Where the commit is made: the lane"
  paragraph's last sentence, replaced. It now names the **branch pointer**
  and `git reset --keep`, says the checkout's uncommitted work standing
  beside the merge is kept, says a merge that merged nothing is not rolled
  back at all, and says a rollback that cannot keep the work refuses and
  leaves the merge standing with the `git reset --keep` line that finishes
  it. One paragraph, no new heading, no new row.
- `specs/spec01.md` and `specs/spec02.md` — the verify blocks repaired (see
  **Blocks that could not fail**), boxes ticked.
- `resources/board/collect.py` — unchanged this pass; pass one's `unland`
  stands exactly as the analyst report describes it.

Lane `lane/collect-must-not-reset-the-checkout-it-did-not-write` carries two
modified files and nothing else:

```
 M references/parts/commits.md
 M resources/board/collect.py
```

Neither is modified in the orchestrator's checkout, so the merge is clean.

## Blocks that could not fail

Both blocks as written by pass one exited non-zero on a green tree, so
`collect` would have refused this PRD with `spec<NN> exit 1 — nothing
written` while every box was ticked. Two shapes, both named in
`probe-then-spec` step 5's `Fails when` table:

- **spec02** ran `python3 resources/index.py check 2>&1 | grep -c '…' |
  grep -qx 0`. `index.py check` exits 1 on this board (three pre-existing
  lines, none this PRD's), and under `pipefail` that exit became the block's.
  Repaired by capturing (`out=$(… 2>&1) && rc=0 || rc=$?`) and greping the
  capture; the rows stay visible and stop deciding the exit.
- **both blocks** ended on `grep -c <needle> <file> | grep -qx 0`. `grep -c`
  exits 1 on exactly the count that means the block passed — zero — so under
  `pipefail` the passing case was the failing case. Repaired by guarding the
  producer (`$(grep -cF … || true)`) and ending on a bare counter test.

While repairing them I widened each block from one needle to the boxes it
backs, so the blocks read the contract rather than one string.

**Measured, the way `collect` runs them** —
`bash -e -o pipefail -c "$(awk '/^```sh/{f=1;next} /^```/{f=0} f' <spec>)"`
from the merged tree's root:

| block | green tree | mutated tree |
|---|---|---|
| spec01 | exit 0 · `31 checks · 31 pass · 0 fail` · `spec01: 0 problem(s)` | exit 1 · `31 checks · 25 pass · 6 fail` |
| spec02 | exit 0 · `spec02: 0 problem(s)` | exit 1 |

spec01's mutation is **behavioural**, not a renamed string: `"reset",
"--keep"` → `"reset", "--hard"` in `resources/board/collect.py`, the one
constant the unit exists to change. Six checks went red. Restored by `cp`
from a scratch dir outside the repo and proved back with `cmp` (clean).
spec02's mutation was the paragraph restored to `HEAD`.

## How the tree was measured

Every board harness on this board computes its own `ROOT` by walking up from
`$0`, so none of them can read a lane — the case `probe-then-spec` step 2's
last `Fails when` row covers. Two scratch trees were built by its method,
both `git clone --shared` of the orchestrator's checkout with the checkout's
1683-line uncommitted diff applied and its untracked
`references/personas/writer.md` copied in, and `.pearde` symlinked to the
live board:

- `base` — `resources/board/collect.py` at `HEAD` (`3587817`). The pre-edit
  baseline.
- `merged` — the lane's `collect.py` and `commits.md` overlaid. What
  `collect` will see after it merges.

`HEAD` was `3587817` before the first run and `3587817` at the flip.

## Harnesses

Baseline set: every harness naming `resources/board/collect.py` (8) or
`references/parts/commits.md` (1), plus the three that enumerate the board
(`grep -l 'find.*verify\.sh'`). Each run on `base`, then on `merged`, same
command line, same order.

| harness | base | merged |
|---|---|---|
| this PRD's `probe/verify.sh` | 31 checks · 23 pass · **8 fail** | 31 checks · **31 pass · 0 fail** |
| `collect-stages-a-shared-file-whole` | 25 passed, 7 failed | 25 passed, 7 failed |
| `filing-refuses-a-file-it-does-not-hold` | 52 · 52 · 0 | 52 · 52 · 0 |
| `the-brief-names-the-verdict-line-collect-requires` | 13 ok · 2 FAIL | 13 ok · 2 FAIL |
| `nothing-left-open/the-line-tells-the-truth` | 85 · 49 · 36 fail | 85 · 49 · 36 fail |
| `the-tool-keeps-its-word/collect-keeps-its-word` | 101 · **101 pass · 0 fail** | 101 · **101 pass · 0 fail** |
| `the-board-runs-itself/collect-is-a-command` | 133 · 133 · 0 | 133 · 133 · 0 |
| `the-board-runs-itself/hunks-land-where-they-came-from` | 47 · 47 · 0 | 47 · 47 · 0 |
| `workflows-on-the-board/workflow-improve` | 71/71 pass | 71/71 pass |
| `graph-probe-makes-harness-sweep-unaffordable` | 4 · 3 · 1 fail | 4 · 3 · 1 fail |
| `the-gate-runs-the-harnesses` | 57 · 27 · 30 fail | 57 · 27 · 30 fail |
| `seven-closed-probes-drifted-red/the-fixtures-meet-the-tool` | 35 · 23 · 12 fail | 35 · 23 · 12 fail |

Every count outside this PRD's own probe is **identical** on the two trees.
The six pre-existing reds were red **before the first edit** and are named
here as inherited, not as findings of this pass.

The one flip — 23 pass → 31 pass on this PRD's probe — is this unit's, shown
against the pre-build file two independent ways: `base` runs the same probe
against `HEAD`'s `collect.py` and reports 8 fail, and the probe's own
section A re-runs the reproduction against `git show 3587817:` and asserts
both faults are present there. No other harness's colour moved, so nothing
here is a neighbour's landing taken as ours.

## The repo's own gate

`python3 resources/index.py check` — exit 1, three lines, **identical on
both trees**, none naming a footprint path:

```
references/personas/writer.md is on disk with no row in references/files.md
references/skills/pearde-machine.md is on disk with no row in references/files.md
resources/board/edit.py references @questions.py — not on disk
```

`bash resources/doctor.sh` — exit 1 on both trees. Diffing the rows of the
two runs (excluding `statusline`, which carries the tree's dirty-file count)
leaves only the scratch root's own path in `guard`, `board`, `vault`,
`harnesses` and `jstests`. **No row's status word differs.** Red rows on
both: `index broken (3 problems)`, `health broken (2 problems)`,
`knowledge broken`. All three are inherited.

## Findings

Pass one's findings, carried forward by name and still standing:

**The refusal branch is reachable only through a verify block that writes.**
`git merge --ff-only` refuses to merge over local changes, so every path the
merge touches is clean at merge time. The one way such a path is dirty by
rollback time is a verify block that wrote into the checkout before going
red — which is what the probe's C1 does. Not dead code, but nearly.

**The same fault survives in the lane, out of this PRD's scope.**
`resources/board/lanes.py:180`, in `merge()`: `git(wt, "rebase", onto,
check=False)` refuses outright on a dirty tree, and the recovery
`git(wt, "reset", "--hard", was, check=False)` then destroys exactly the
paths `land_lane` had just printed as `outside the footprint, left in the
lane`. Same shape as the reported bug, one repo over. It is now the only
`reset --hard` left in `resources/`. Reported, not fixed — the PRD puts the
lane mechanism out of scope. **This is the one thing worth routing to a new
PRD.**

**Pre-existing red in the gate, recorded before the first edit.** Pass one
recorded two `index.py check` lines; this pass records **three** — a sibling
session dropped an untracked `references/personas/writer.md` with no row in
`references/files.md` between the two passes. It is that session's, not this
PRD's; it is red on `base` as well as on `merged`.

**`doctor.sh` cannot be read inside a lane.** The lane is materialised
without the board (sparse-checkout excludes `.pearde/`), so every
board-reading row measures a board that is not there. Confirmed again this
pass: the gate has to be run against a merged tree, never in the lane.
Related to `a-harness-measures-the-tree-its-worker-built-in`.

**Knowledge gap.** Pass one's `knowledge.py query` returned 0 hits and
enqueued `.pearde/wiki/pending/260902-d65b.md`. Nothing this pass learned
came from outside this repo, so nothing new was written back.

New this pass:

**The board's harnesses cannot all be redirected by a symlink.**
`collect-stages-a-shared-file-whole` computes `HERE` with `pwd -P`, which
resolves a `<scratch>/.pearde` symlink straight back to the live board and
lands `ROOT` in the orchestrator's checkout — so it silently measured the
wrong tree until `PEARDE_ROOT` was set explicitly. It honours `PEARDE_ROOT`,
as does this PRD's own probe; the other ten do not, and for those the
symlink is the only lever. Nothing to fix in any harness — it is the
measuring method that needs the extra step, and it is written up as an Edit
below.

## Words

No term in the contract was missing from `grammar.py show`.

## Workflow probe-then-spec

| # | step | outcome |
|---|------|---------|
| 1 | `read-the-contract` | pass — PRD, both specs, both footprint files read; `git status --short` recorded in **both** roots (lane: 1 file; checkout: 21 files, none a footprint path) before the first edit |
| 2 | `capture-the-harness-baseline` | pass — 12 harnesses + `index.py check` + `doctor.sh`, all on a `base` scratch tree built by step 2's lane row; outputs whole under `<scratch>/unland-run/out-base/` |
| 3 | `attempt-the-build` | **not entered** — step 3's first `Fails when` row: the specs exist and the build stands, so this is the route's second pass. No rebuild, no flip claimed that the pass which built it did not earn |
| 4 | `re-run-the-harnesses` | pass — same 12, same order, same command lines, on `merged`; every count outside this PRD's probe identical, the one flip shown against `HEAD` two ways |
| 5 | `write-the-specs` | pass — no spec authored; step 5's `Fails when` table applied to the two blocks that already stood, both of which could not fail. Both now run green under `bash -e -o pipefail` and red under a mutation |

Back-edges taken: none.

### Edits

`probe-then-spec` step 2, `capture-the-harness-baseline`, `## Fails when`,
the last row (`every board harness computes its own ROOT by walking up from
$0, and the repo: root is a lane`). Its `do` cell prescribes the symlink and
stops there. A harness that computes its own directory with `pwd -P` —
`collect-stages-a-shared-file-whole` on this board does — resolves the
symlink away and reads the orchestrator's checkout instead, printing a
plausible count for a tree that holds none of the work. Replacement text for
that cell:

> build the merged tree in scratch — `git clone --shared <checkout>
> <scratch>` (a `git archive` or `git init` copy loses the history a
> pinned-sha harness reads), `git apply` the checkout's uncommitted diff,
> overlay the lane's files — then symlink `<scratch>/.pearde` to the live
> board and run each harness **through that path**, so its own `cd
> …/../../../..` resolves to the merged tree. The symlink alone is not
> enough: `grep -l "pwd -P" $(find <board>/prds -name verify.sh)` first, and
> for every harness it names — and for every harness that honours it —
> export `PEARDE_ROOT=<scratch>` on the run, because `pwd -P` resolves the
> symlink back to the live board and the harness then measures the
> orchestrator's checkout while printing a count that looks like yours. Say
> in the report that the counts are the merged tree's, not the lane's, and
> name any harness that could be pointed at neither.
