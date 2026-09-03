# every-module-finds-its-siblings-by-one-rule — implementer

Verdict: DONE

Seventh pass, and the landing pass. The sixth pass closed all 27 boxes on a
lane that could not merge; this one made the lane merge and kept the boxes
closed on the tree that actually landed.

Three pieces of work, in order. The lane was **rebased onto the trunk** and
the five conflicts the sixth pass wrote down were resolved as it wrote them.
`resources/board/machine.py` is `run.py` on the trunk, so spec03's
`footprint:`, its block and its prose were re-spelled and the probe with them.
**Thirteen modules** that landed on the trunk while the lane waited were
converted to the rule and added to spec03's footprint — the `## Answers`
block's own reasoning, *the contract is every module*, applied to them word
for word.

Every box was **un-ticked before the re-run** and re-ticked against output
from the rebased tree, because a rebase can move a box under you. **27 of 27
are ticked** — spec01 7/7, spec02 7/7, spec03 7/7, spec04 6/6 — and all four
`## Verify and Proof` blocks exit 0 under `bash -e -o pipefail`, run from the
**orchestrator's checkout**, on `main` at `e55a0e7`. The probe reads
**23 passed / 0 failed** there and **3 passed / 20 failed** on a tree without
the rule.

The PRD landed mid-pass: `pearde collect` succeeded while this report was
being measured, and `prd.md` now reads `state: done`, `commit: e55a0e7
d4626c9`. Everything quoted below was re-run on that merged trunk afterwards.

## What this pass did

### 1. The rebase — five conflicts, five documented resolutions

Lane base was `1880990`, thirteen commits behind; the trunk had moved twice
more since the sixth pass wrote its table (`f8968fe` → `7a162c2`). `git
rebase main` conflicted on exactly the four files `merge-tree` had named,
plus the fifth on the second commit.

| file | resolution taken |
|---|---|
| `index.md` | HEAD's rows — `mapfile.py` added to `@@view`/`@@pass`, `pearde-machine.md` dropped from and `pearde-run.md` kept in `@@skills` — with `@resources/pearde_path.py` inserted after `@resources/pearde.py` in `@@handles` and `@@install` |
| `references/files.md` | both: HEAD's `references/skills/` spelling in the `install.sh` row, the lane's rewritten `pearde.py` description and its new `pearde_path.py` row |
| `resources/board/dispatch.py` | the rule, then HEAD's `import run as runlib` |
| `resources/doctor.sh` | both: HEAD's `pwd -P` in `DIR` and `SKILL_ROOT`, the lane's `res()` below them |
| `resources/knowledge.py` | HEAD's `import common` + `import memos as memos_lib` opened by the rule, and HEAD's `_plan()` reduced to a bare `import plan` — the rule has already put every directory under `resources/` on the path, so the `board/` the function spelled is exactly the second edit this PRD removes |

Two names went dead in the substitution and went with it: `BOARD = HERE =
os.path.dirname(...)` in `dispatch.py` and in `run.py`, whose only readers
were the `sys.path.insert` lines the rule replaced. `grep -nw` proves neither
name is read anywhere else in either file.

Rebase tip `bfd16d3` on `7a162c2`; `git merge-base --is-ancestor main HEAD`
answered **yes**, which is what `lanes.merge --ff-only` needs and what the
sixth pass could not say.

### 2. `machine.py` is `run.py`

`60f49d1` (*machine becomes run*) renamed it on the trunk. Six spellings were
stale and all six were repaired: spec03's `footprint:` row, its `FILES` list,
its `MOVES` dict, its execution loop, its prose and acceptance box 3, and the
probe's own `mv` line and module loop. Git's rename detection carried the
lane's hunk onto `run.py` by itself, so no code edit was owed — only the
spellings that name it.

### 3. Thirteen modules the trunk grew while the lane waited

`grammar.py`, `health.py`, `memos.py`, `questions.py` under `resources/`, and
`boards.py`, `mapfile.py`, `needs.py`, `prdfile.py`, `registry.py`,
`repos.py`, `schedule.py`, `silence.py`, `vision.py` under `resources/board/`
— every one a hand-rolled preamble, and every one reddening spec03 box 2 and
spec04 box 6, which are population sweeps over the whole tree.

Three dialects, one substitution each:

| shape | count | was |
|---|---|---|
| the nine cut from `plan.py` | 9 | two inserts — `dirname(dirname(__file__))` then `dirname(__file__)` |
| `grammar` `health` `memos` | 3 | one insert — `dirname(abspath(__file__))` |
| `questions.py` | 1 | one insert spelling `"board"` outright |

All fourteen files (the thirteen plus `run.py`'s dead name) parse, import and
execute. Three comments that named a directory — *the skill root, one dir up*,
*beside this script* — were rewritten to *on the path by the rule*, because
after the substitution they were false.

spec03's `footprint:` grew by the thirteen and its `FILES` list with them, so
the block reads every path the frontmatter names. `read_specs` reports **no
problems** and the set weighs **34**, still under `split-above: 40`.

### 4. One probe assertion no longer measured what it said

`plan.py alone still cannot find render — the handoff` ran `plan.py scan` from
a moved directory and expected `No module named 'render'`. On the converted
tree it prints `no .pearde/ board found` instead — because `plan.py` imports
`memos.py`, `memos.py` now carries the rule, and **the rule puts every
directory under `resources/` on the path for the whole process**. A moved
`render` is now found by a sibling's rule rather than by plan's own two lines.

The assertion was re-aimed at what it was always for, per step 4's row on a
check written against behaviour the change makes reachable: plan's two lines
are put into a bare interpreter and `import render` tried there. It is the
only way left to measure `plan.py`'s own preamble, it is stricter than the old
shape, and the comment above it says why. Renamed to `plan.py's own two-line
preamble, alone, still cannot find a moved render — the handoff`.

This is a **finding for the sibling PRD** `the-largest-module-is-cut-by-
responsibility`, below.

## The numbers

Roots. Lane base `1880990`; trunk `7a162c2` at the first command, `e55a0e7`
at the last — the PRD's own landing. Board `94f4833` → `cd9733e`. Both
checkout and lane were **clean before the first edit**; `git status --short`
recorded in all three.

| gate | before (lane `def589f`, base `1880990`) | after the rebase, before the repair | after (checkout, `e55a0e7`) | reading |
|---|---|---|---|---|
| spec01 block | exit 0 | exit 0 | **exit 0**, `spec01 ok` | held through the rebase |
| spec02 block | exit 0 | exit 0 | **exit 0**, `spec02 ok` | held through the rebase |
| spec03 block | exit 0 | **exit 1**, `FileNotFoundError: 'resources/board/machine.py'` | **exit 0**, `spec03 ok` | this pass's flip |
| spec04 block | exit 0 | **exit 1**, `FAIL … got 'grammar.py health.py memos.py questions.py boards.py mapfile.py needs.py prdfile.py registry.py repos.py schedule.py silence.py vision.py'` | **exit 0**, `spec04 ok` | this pass's flip |
| probe, tree with the rule | `23 passed, 0 failed` | `21 passed, 2 failed` | **`23 passed, 0 failed`** | this pass's flip |
| probe, tree without the rule | `3 passed, 20 failed` | — | `3 passed, 20 failed` | the differential spec04 box 6 needs |
| `31 modules open with the one rule` | 18 | 18 | **31** | the thirteen |
| `index.py check` | 2 problems (lane), 4 (checkout) | 4 | **4, byte-identical to the pre-merge trunk** | inherited, unmoved |
| `doctor.sh` | exit 1, 19 rows | exit 1, 19 rows | exit 1, 19 rows | see below |

**The doctor comparison.** Row verdicts were compared with `statusline`
excluded, per the route's own row. Between the pre-merge trunk and the rebased
lane the sequence was **identical, 19 rows, both exit 1** — which is spec04
box 5. On the merged trunk two rows went **up**, and neither is mine:

- `questions broken → ok`. The red line was *this PRD's* `## Answers` with no
  `## Questions` above it. `collect` moved the PRD to `done`; the row stopped
  applying. A consequence of the landing, not of any code.
- `knowledge broken → ok`. `graph.json is behind the files: 260902-4f91,
  260902-aae0, 260903-4626` is gone; something ran `knowledge.py relink`
  between the two measurements. Not this pass — nothing here touched the wiki.

Both are quoted as rises, per step 4's first row, and claimed by nobody here.

**The flips are shown against the tree that does not hold the build**, which
the route calls stronger evidence than `git show HEAD:`: spec03 and spec04
were run *verbatim* against the rebased tree **before** the repair and exited
1 with the two causes named above; the same blocks exit 0 after it. The whole
gate ran on the old file, twice.

**The mutation.** spec03 and spec04 must fail on a mutated footprint file, and
the mutation was aimed at a **newly converted** module so the new footprint
rows are proved wired, not just present: `resources/board/vision.py`'s rule was
reverted to its two old inserts, `cp`-backed up to a scratch dir outside the
repo first. spec03 → **exit 1**, `AssertionError: resources/board/vision.py`;
spec04 → **exit 1**, `FAIL … got 'vision.py'`, probe `22 passed, 1 failed`.
Restored by `cp`, proved with `cmp` (clean), spec03 back to exit 0.

**Exercised, not only matched.** All six of `grammar.py`, `health.py`,
`memos.py`, `questions.py`, `plan.py` and `run.py` import and execute;
`pearde.py help`, `pearde.py scan`, `memos.py check` and `grammar.py show` all
behave identically in the lane and the checkout.

## Findings

Earlier passes' findings are carried forward by name. Four are closed here.

- **CLOSED — the lane cannot land as it stands.** The whole of this pass. The
  rebase is done, the five resolutions are applied, and `collect` landed the
  PRD at `e55a0e7 d4626c9` while the report was being measured.
- **CLOSED — the merged tree reddens spec03 twice, and both repairs are
  frontmatter edits an implementer may not make.** The orchestrator authorised
  both in the dispatch. `machine.py` is `run.py` in six places; the thirteen
  modules are converted and in the footprint.
- **CLOSED — `lanes.merge` refuses a dirty lane outright.** Not closed as a
  route defect, but discharged: the lane was clean at the merge and nothing
  was lost.
- **CLOSED — the parent report's claim about `plan.py` is true only for
  today.** It stopped being true this pass, in a way nobody predicted — see
  the next finding.
- **NEW. The rule is transitive, and that quietly disarms any check written
  as "module X, alone, cannot reach Y".** `pearde_path` puts every directory
  under `resources/` on `sys.path` for the **whole process**, so the moment
  one module on an import chain carries the rule, every module downstream of
  it inherits the full path whether it carries the rule or not. Converting
  `memos.py` was enough to make the unconverted `plan.py` find a `render.py`
  moved two directories away. Measured: the old assertion printed `no .pearde/
  board found` where it expected `No module named 'render'` — it had stopped
  failing for the right reason and would have gone on passing.
  Two consequences worth writing down. For the sibling PRD `the-largest-
  module-is-cut-by-responsibility`: **`plan.py` now moves without carrying the
  rule**, because its siblings carry it for it. That is a convenience, not a
  contract — a `plan.py` invoked as the *first* module in a process still has
  only its own two lines, which is what the repaired assertion measures. It
  should still take the rule when it is cut. And for anyone writing a check
  on this tree: an assertion that a module cannot reach a sibling must put
  that module's own preamble in a fresh interpreter, never run the script.
- **STANDING, and now measured three dispatches running. The population sweeps
  in spec03 box 2 and spec04 box 6 will redden again.** This is the fourth
  dispatch at which new modules appeared under an open tree-wide sweep, and
  the thirteen this pass converted were themselves the *cut of `plan.py`* —
  more of that cut is still to come. The durable repair the fourth, fifth and
  sixth passes all recommended is still owed and still not done: file the
  tree-wide sweep as a standing invariant under `resources/invariants/`, so a
  module landing without the rule reddens the board's own gate at the moment
  it lands rather than an unrelated PRD's spec months later. It is out of this
  contract's scope and is filed here as a finding, not fixed.
- **A broken module still takes down every command.** Still stands.
  `discover()` catches `Exception`; `brief.py`'s root probe ends in
  `sys.exit(2)`, a `BaseException`. Not in this contract.
- **The `plugins` doctor row still cannot fail.** Still stands — a row gated
  on a directory existing disappears rather than reddening.
- **Data directories are not covered by this rule, and are the next trap.**
  Unchanged. A finding for `every-file-sits-under-what-it-is-responsible-for`.
- **`index.py check` is red before the first edit, in both roots.** Inherited
  and byte-identical across the rebase and the merge: `resources/common.py` on
  disk with no row in `references/files.md`, `hotreload-test.js` listed twice
  and absent, and one `@pearde/…` memo dangle. The first is a sibling's landed
  file; none names `pearde_path`, which is what spec01 box 7 asserts.
- **A word the grammar does not have.** Still true, a fifth time. The three
  lines every module opens with have no term: `preamble`, `bootstrap` and
  *rule* are all in use in the tree and none is in `python3
  resources/grammar.py show`. Written here as "the rule" and "the preamble"
  interchangeably, again.
- **`knowledge.py` writes the live record from a lane with no flag saying
  so.** The sixth pass hit it through `index` and restored the one note it
  moved. Not re-triggered this pass — no `knowledge.py` verb was run.
- **The knowledge record has nothing on this question.** Unchanged. Nothing
  was learned outside this repo this pass, so nothing was owed to
  `knowledge.py remember`.
- **Not mine, recorded.** `references/drill.md` and
  `references/skills/pearde-drill.md` were modified in the checkout by a live
  sibling session at 12:07, after this pass's baseline. Untouched here.
- **Not run: the 82-harness board sweep.** `bash resources/doctor.sh
  --harnesses` was attempted against the checkout and **exceeded ten minutes**
  without finishing. doctor's own row calls it opt-in and warns it "costs tens
  of seconds"; the measured cost is far higher than that. The four spec blocks,
  the probe both ways, `index.py check` and the 19 doctor rows stand in its
  place. That the row's own warning understates its cost by an order of
  magnitude is a finding for whoever owns the `harnesses` row.

Nothing was written outside the PRD folder and the footprint. The checkout is
clean but for the two drill files named above; the board carries one
uncommitted file, this PRD's own `probe/verify.sh`, whose last edit is the
explanatory comment written after `collect` committed.

## Health

The brief names no footprint file under the health floor. Two dead names were
removed inside the contracted edit (`BOARD = HERE` in `dispatch.py` and
`run.py`) and three comments that had become false were corrected. No file was
split and no refactor was attempted.

## Workflow probe-then-spec

| step | atomic | outcome |
|---|---|---|
| 1 | `read-the-contract` | pass. `prd.md`, all four specs and the sixth pass's `report.md` read first, per step 5's row, so its `## The landing` table was the starting point rather than something to re-derive. Two rows fired: the footprint row — `resources/board/machine.py` does not exist under the `repo:` root, and `find` gives exactly one match, `run.py`, which is the same file under a new spelling; and the row on a lane whose work is committed — `git status --short` was clean in both roots because the failed `collect` had already committed the lane at `def589f` |
| 2 | `capture-the-harness-baseline` | pass. All four blocks, the probe both ways, `index.py check` and `doctor.sh` in both roots, recorded **before the first edit** under a run-named scratch subdirectory `…/scratchpad/pass7/`. Both gates recorded red before the first edit and named as inherited. The 82-harness sweep was attempted and timed out; recorded as not measured rather than quietly skipped |
| 3 | `attempt-the-build` | entered for the rebase, the rename and the thirteen. Every change is an edit to an existing footprint file, so none is staged under `probe/`, per the atomic's second point. The one file written under `probe/` is the PRD's own `verify.sh`, whose assertion the change made unmeasurable |
| 4 | `re-run-the-harnesses` | pass. Every box was **un-ticked before the re-run** and re-ticked from output, because a rebase can move a box under you. Both flips shown by running the blocks verbatim against the rebased tree that does not hold the repair — the whole gate on the old file. Two doctor rows rose and both are named as not mine. The `statusline` row was excluded from the comparison, per the table's own row |
| 5 | `write-the-specs` | not entered as authoring. Its `Fails when` table applied to the blocks that stand: all four run under `bash -e -o pipefail` with the fence awked out, from the **orchestrator's checkout** — the root `collect` runs them from, which this pass could honour because the work had landed there. `read_specs` reports no problems and 34, under `split-above`. The report-path row fired: every earlier finding is carried forward above by name |

### Edits

No atomic sent a wrong command or a stale path this pass, and no file under
`workflows/` was touched. Earlier passes' proposed rows stand unmerged and are
not repeated. Two rows are new.

**Step 4, `Fails when`, proposed row** — the case that cost this pass its
longest measurement, and that no row covers:

    | a check goes green after the change and the reason it prints is not the reason it asserts | the change made the check's own premise unreachable — a rule that installs process-wide is inherited by every module downstream of the first one that carries it, so "X alone cannot reach Y" stops being measurable the moment any sibling on X's import chain is converted | read the check's OUTPUT, never only its exit. Where the message no longer matches the assertion, re-aim the check at the narrowest thing that still holds the box's sentence — here, X's own preamble in a fresh interpreter rather than X run as a script — and say in the report why the old shape stopped measuring. A check that passes for a new reason is a check that has stopped failing, and it reads identical to one that works |

**Step 1, `Fails when`, proposed row** — the ticked-box hazard a rebase opens:

    | the route's second pass begins with every box already ticked, and the tree is about to be rebased | a tick is a claim about a tree, and a rebase replaces that tree; boxes ticked against the pre-rebase tree say nothing about the post-rebase one, and three of them here were false the moment the rebase finished | un-tick every box of every spec whose footprint the rebase touches BEFORE re-running, and re-tick only from output taken on the rebased tree. Leaving them ticked and "confirming" them reads identical on the board and is how a stale green survives a rename |

Standing observation, now discharged rather than repeated: the sixth pass
noted that step 5's instruction to run each block "from the root `collect`
will run it from — the orchestrator's checkout, not your lane" cannot be
honoured by an implementer whose build is only in a lane. This pass could
honour it, because the lane landed mid-pass. The instruction is right; it is
simply unreachable until the merge, which is an argument for running the
blocks from the checkout once more *after* `collect` rather than for changing
the words.

## Scores

complexity: 34
blast-radius: high
workflow: probe-then-spec
