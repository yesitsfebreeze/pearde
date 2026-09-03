# every-module-finds-its-siblings-by-one-rule — implementer

Verdict: DONE

Sixth pass, and the first with an answer to the fork. `prd.md` now carries an
`## Answers` block settling it: the four files that held three boxes red are
in scope, the footprints were what was wrong, and they have been grown —
`resources/board/session.py`, `resources/board/shared.py` and
`resources/knowledge.py` onto spec03, the destructive-git invariant harness
onto spec04.

They were fixed the way their siblings were fixed. **All 27 boxes are ticked**
— spec01 7/7, spec02 7/7, spec03 7/7, spec04 6/6 — and all four
`## Verify and Proof` blocks exit 0 under `bash -e -o pipefail`, against a
baseline of spec03 exit 1 and spec04 exit 1 taken before the first edit. The
probe goes **21 passed / 2 failed to 23 passed / 0 failed**.

One thing is not closed and is not mine to close: **the lane cannot land as it
stands.** `main` has moved thirteen commits since the lane was cut, and among
them a rename (`resources/board/machine.py` to `run.py`) and thirteen new
modules with hand-rolled preambles. Both redden spec03 on the merged tree, and
both repairs are frontmatter edits to a spec. The whole of it, with the
resolutions proved in scratch, is under **The landing** below.

## What this pass built

| file | was | now |
|---|---|---|
| `resources/board/session.py` | `HERE = …` then `sys.path.insert(0, HERE)` | the three-line rule, `import pearde_path` |
| `resources/board/shared.py` | the same two lines | the same rule |
| `resources/knowledge.py` | `sys.path.insert(0, dirname(abspath(__file__)))` | the same rule; and its deferred `import index` inside `cmd_index` drops the `sys.path.insert` it opened with — the rule already put `resources/` on the path, which is what `workflows.py`'s deferred `import plan` does |
| `resources/invariants/no-destructive-git-runs-in-a-tree-the-session-does-not-own.sh` | `os.path.join(root, "resources", "board", "refuse.py")` | `REFUSE=$(ls "$ROOT"/resources/refuse.py "$ROOT"/resources/*/refuse.py 2>/dev/null \| head -1)` in the shell, passed to the heredoc as `sys.argv[2]` — the shape the other two harnesses already use |

`HERE` was dead in both Python modules after the substitution — the two lines
were its only readers — so it went with them. The harness searches the tree
being **measured** (`$ROOT`), not the tree the file sits in: it takes a root
argument and is run against fixtures, so a `$(dirname "$0")/..` spelling would
have measured the wrong tree while printing a green line.

Every change is an edit to an existing footprint file, so none of it is staged
under `probe/` — a preamble has no meaning outside the module it opens.

## The numbers

Roots. Lane tip `3e676c2`, parent `1880990`, five files uncommitted — four of
them this pass's, plus `resources/guard.py` from the fourth pass, untouched
here. Checkout `/Users/feb/dev/infra/pearde` on `main` at **`f8968fe`**, clean
working tree, thirteen commits ahead of the lane's base. Board repo at
`6956bd3`. `git status --short` taken in all three before the first edit.

| gate | before the first edit | after | reading |
|---|---|---|---|
| spec01 block | exit 0, `spec01 ok` | exit 0, `spec01 ok` | held |
| spec02 block | exit 0, `spec02 ok` | exit 0, `spec02 ok` | held |
| spec03 block | exit 1, `AssertionError: ['knowledge.py', 'session.py', 'shared.py']` | **exit 0, `spec03 ok`** | this pass's flip |
| spec04 block | exit 1, `FAIL no module imports a sibling without the rule (plan.py excepted) — want 'none', got 'knowledge.py session.py shared.py'` | **exit 0, `spec04 ok`** | this pass's flip |
| probe, `PEARDE_ROOT=<lane>` | `21 passed, 2 failed` | **`23 passed, 0 failed`** | this pass's flip |
| probe, `PEARDE_ROOT=<checkout>` | `3 passed, 20 failed` | `3 passed, 20 failed` | the differential spec04 box 6 needs — the probe still fails on a tree without the rule |
| spec03 sweep B (`boardstr` grep) | one hit, the invariant harness line 77 | no hit, `grep` rc=1 | this pass's flip |
| the invariant harness itself | not run in the baseline set | exit 0, 6 PASS, `29 Python file(s) under resources/ hold no ungated destructive git` | the rewrite did not weaken the rule it asserts |
| `index.py check` lane | exit 1, 2 problems | exit 1, 2 problems, `diff` empty | inherited, unmoved |
| `index.py check` checkout | exit 1, 4 problems | exit 1, 4 problems, `diff` empty | inherited, unmoved |
| `doctor.sh` lane / checkout | exit 1, 20 rows each | exit 1, verdict sequence unchanged in **both**, and identical **between** them | spec04 box 5 holds |

Both flips were shown against the pre-build file, not only against the result.
The lane's HEAD did not move this pass (`3e676c2` at both ends), so `git show
HEAD:` is the right baseline: `grep -c '^import pearde_path'` on
`HEAD:session.py`, `HEAD:shared.py` and `HEAD:knowledge.py` returns **0** for
each and 1 for each working file; the sweep-B matcher run over
`HEAD:no-destructive-git-…sh` **hits line 77** and misses the working file.
Neither predicate was satisfied by the old text, so neither flip is a
neighbour's landing.

The four modules were then exercised, not only matched: `knowledge.py index`,
`session.py list`, `shared.py` and `pearde.py help` all exit 0.

## The landing

`git merge-base --is-ancestor HEAD lane/<slug>` answers **no** — the lane is
thirteen commits behind `f8968fe`, so `lanes.merge --ff-only` refuses today.
`git merge-tree --write-tree --name-only HEAD lane/<slug>` names four
conflicting files, **all four inside the footprint**:

| file | HEAD's side | the lane's side | resolution |
|---|---|---|---|
| `index.md` | `@resources/board/mapfile.py` added to `@@view` and `@@pass`; `pearde-machine.md` dropped from `@@skills` | `@resources/pearde_path.py` added to `@@handles` and `@@install` | both — HEAD's rows, with `pearde_path.py` inserted after `pearde.py` |
| `references/files.md` | `` `skills/` `` renamed to `` `references/skills/` `` in the `install.sh` row | `pearde.py`'s description rewritten and a `pearde_path.py` row added | both |
| `resources/board/dispatch.py` | `import machine as mach` becomes `import run as runlib` | the preamble becomes the rule | the rule, then HEAD's import |
| `resources/doctor.sh` | `pwd` becomes `pwd -P` in `DIR` and `SKILL_ROOT` | `res()` added below them | both |

A fifth conflict follows on the uncommitted work: `resources/knowledge.py`,
where HEAD replaced `import memos` with `import common` + `import memos as
memos_lib` and added a `_plan()` that spells `board/`. The resolution is
HEAD's imports opened by the rule, and `_plan()` reduced to a bare `import
plan` — the rule has already put every directory under `resources/` on the
path, so the directory it spells is exactly the second edit this PRD removes.

All five were resolved in a scratch clone (`git clone --shared` of the lane,
the working tree committed, `git fetch` the checkout's `main`, `git rebase`)
and the rebase ran to completion: `Successfully rebased and updated`, tip
`08c1309` on `f8968fe`. **The live lane was deliberately not rebased**, for a
reason the earlier passes did not have — see the finding below.

## Findings

Earlier passes' findings are carried forward by name. Three are closed by this
pass; the rest stand.

- **CLOSED — Three acceptance boxes on this PRD measure the whole live
  checkout.** Answered by the orchestrator's `## Answers` block and fixed
  here. The underlying shape is not closed; it is the finding below.
- **CLOSED — The four files outside the footprint.** Fixed, and the three
  boxes ticked.
- **CLOSED — a DONE report on a lane that cannot merge leaves the board
  silent.** Not closed as a route defect, but discharged for this PRD: the
  merge state is measured and written above rather than left for `collect` to
  discover.
- **NEW, and the reason the lane was not rebased. The merged tree reddens
  spec03 twice, and both repairs are frontmatter edits an implementer may not
  make.** Measured by running all four blocks against the rebased scratch
  tree: spec01 exit 0, spec02 exit 0, **spec03 exit 1**, **spec04 exit 1**
  (probe `21 passed, 2 failed`). Two distinct causes:
  1. `resources/board/machine.py` was renamed to `run.py` on `main` in
     `60f49d1` (*machine becomes run*). spec03's `footprint:` names
     `machine.py`, and its block reads it twice — in `FILES` and in `MOVES`.
     On the merged tree the block dies at `FileNotFoundError:
     'resources/board/machine.py'`, and spec04's probe fails
     `machine.py imports its siblings from its new directory`.
  2. **Thirteen new modules** landed on `main` since the lane was cut, each
     with a hand-rolled preamble: `grammar.py`, `health.py`, `memos.py`,
     `questions.py`, `boards.py`, `mapfile.py`, `needs.py`, `prdfile.py`,
     `registry.py`, `repos.py`, `schedule.py`, `silence.py`, `vision.py`.
     Verified by hand on the checkout — `resources/grammar.py:29` is
     `sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))`,
     `resources/board/mapfile.py:29-30` two inserts, `resources/board/run.py:38-39`
     the `BOARD` pair. spec03 box 2 and spec04 box 6 are population sweeps
     over every module under `resources/`, so all thirteen redden them.

  Rebasing the live lane would therefore have un-ticked three boxes this pass
  just ticked, and left the repair — a `footprint:` edit and two block edits —
  in the hands of a worker forbidden to make it. The lane was left where it
  is, green, with the resolutions written down.

  **The repair, in the order it has to happen.** (a) In spec03, rename
  `machine.py` to `run.py` in `footprint:` and in both places the block reads
  it. (b) Either grow spec03's `footprint:` by the thirteen and convert them —
  the `## Answers` block's own reasoning, *the contract is every module*,
  applies to them word for word — **or** take the repair the fourth and fifth
  passes recommended and this pass now has the evidence for: aim spec03 box 2
  and spec04 box 6 at the **named set this PRD converted**, and file the
  tree-wide sweep as a standing invariant under `resources/invariants/`. The
  second is the durable one. This is the third dispatch at which new modules
  have appeared under an open population sweep; on the evidence the sweep will
  redden again before any fourth one lands, however many modules are converted
  in between.
- **The parent report's claim about `plan.py` is true only for today.** Still
  stands. `plan.py` is excepted by both spec03 and the probe and is the
  sibling PRD `the-largest-module-is-cut-by-responsibility`'s footprint;
  whichever pass cuts it must open each module it produces with the rule. On
  the evidence above that cut has begun on `main` — `mapfile.py`,
  `prdfile.py`, `needs.py`, `boards.py`, `repos.py`, `vision.py` and
  `silence.py` are pieces of it, and not one of them carries the rule.
- **A broken module still takes down every command.** Still stands.
  `discover()` catches `Exception`; `brief.py`'s root probe ends in
  `sys.exit(2)`, a `BaseException`. Not in this contract.
- **The `plugins` doctor row still cannot fail.** Still stands — a row gated
  on a directory existing disappears rather than reddening.
- **Data directories are not covered by this rule, and are the next trap.**
  Unchanged. A finding for `every-file-sits-under-what-it-is-responsible-for`.
- **`index.py check` is red in both roots before the first edit.** Inherited.
  The lane's two are `references/language.md references
  @references/personas/writer.md` and the structural `@pearde/…` dangle the
  route's own step-2 row describes. The checkout's four are the same dangle
  plus three about `resources/common.py` and `hotreload-test.js` — a
  sibling's, landed after the lane was cut. Neither root names `pearde_path`,
  which is what spec01 box 7 asserts.
- **A word the grammar does not have.** Still true, and this report hit it a
  fourth time. The three lines every module opens with have no term:
  `preamble`, `bootstrap` and *rule* are all in use in the tree and none is in
  `python3 resources/grammar.py show`. Written here as "the rule" and "the
  three lines" interchangeably, again.
- **`lanes.merge` refuses a dirty lane outright.** Still open and still
  relevant. The lane now carries five uncommitted files. `land_lane` commits
  them; `release blocked` does not. Nothing here may be lost by the next pass.
- **NEW, and mine — a smoke test wrote into the live board.** Running
  `python3 resources/knowledge.py index` from the lane to prove the deferred
  `import index` still resolves rewrote 169 notes under `<board>/wiki/index/`
  on the **live** board rather than in the lane. This is the standing
  `knowledge.py`-writes-the-live-record finding, reached through `index` this
  time rather than `query`. Exactly one tracked file was actually moved by it
  — `wiki/index/resources-board-shared-py.md`, mtime 11:52, matching the run —
  and it was **restored from the board's own HEAD** (`git show HEAD:<path> >
  <path>`, a plain write, not a `checkout --`); `git status` on that path is
  now empty. Everything else the run rewrote came out byte-identical. The
  other rows still dirty under `wiki/` are not this pass's: `Dashboard.md`
  carries an mtime of Sep 2 19:26, the `D` of
  `wiki/index/references-skills-pearde-machine-md.md` predates the run (the
  lane still holds that skill file, so this run would have kept it), and the
  six `wiki/pending/` files are another session's. The finding for the board
  is that a read-shaped verb (`index`) writes the live record from a lane with
  no flag saying so; a worker cannot smoke-test `knowledge.py` without
  touching a tree it does not own.
- **The knowledge record has nothing on this question.** Unchanged. Nothing
  was learned outside this repo this pass, so nothing was owed to
  `knowledge.py remember`.

Nothing was written outside the PRD folder and the footprint, except the one
restored wiki note named above. `git status --short` in the checkout is empty;
in the lane it names five files, four of them this pass's; on the board it
names this PRD's own directory and other sessions' PRDs.

## Health

The brief names no footprint file under the health floor, and none was
touched beyond the contracted edit.

## Workflow probe-then-spec

| step | atomic | outcome |
|---|---|---|
| 1 | `read-the-contract` | pass. `prd.md` now carries `## Answers`; four specs read; the previous pass's `report.md` read first so its findings could be carried forward, per step 5's row. Two rows fired: the brief's premise that the build is uncommitted is stale for a fourth time (it is committed at `3e676c2` with five files beside it), and the footprint row — spec03 and spec04 have both grown since the fifth pass, which is the whole of what changed |
| 2 | `capture-the-harness-baseline` | pass. All four blocks, the probe both ways, sweep B, `index.py check` and `doctor.sh` in both roots, recorded before the first edit, whole outputs under a run-named scratch subdirectory `…/scratchpad/pass6/`. Both gates recorded **red before the first edit** and named as inherited |
| 3 | `attempt-the-build` | entered for the four newly-in-footprint files only. Row 1 of the table governs: this is the route's second pass, so step 3 is entered only for the specs whose build is not in the tree — spec01 and spec02 were left alone, and spec03 and spec04 were entered only for the four files the `## Answers` block added. Each is an edit to an existing footprint file, so none is staged under `probe/`, per the atomic's own second point |
| 4 | `re-run-the-harnesses` | pass. Every recorded count is greater than or equal to its baseline; three moved and all three moved up. Both flips shown against `git show HEAD:` with the predicate extracted and run over the old file. `index.py check` and `doctor.sh` `diff` empty in both roots. The `doctor` `statusline` row was excluded from the comparison, per the table's own row |
| 5 | `write-the-specs` | not entered as authoring. Its `Fails when` table was applied to the blocks that stand: each run under `bash -e -o pipefail` with the fence awked out, all four exit 0. The report-path row fired — every earlier finding is carried forward above by name. The boxes were ticked as they closed, each against output quoted in **The numbers** |

### Edits

No atomic sent a wrong command or a stale path this pass, and no file under
`workflows/` was touched. The fifth pass's two proposed rows stand unmerged
and are not repeated. One row is new, and it is the one that would have saved
this pass its longest measurement.

**Step 4, `Fails when`, proposed row.** The route tells a worker to rebase the
lane when `merge-tree` names only footprint files, and has no row for the case
where the rebase is *mechanically* clean and *semantically* red — the merged
tree satisfying every conflict resolution and still failing the spec, because
the specs were written against a tree the intervening commits renamed and grew.
Replacement text:

    | `merge-tree` names only footprint files, the rebase resolves cleanly in scratch, and a spec's block fails on the rebased tree | the conflicts were the easy half. A rename on the trunk makes a `footprint:` entry a stale spelling, and a population sweep in an acceptance box goes red on every module that landed while the lane waited — neither is a conflict and neither shows in `merge-tree` | run every block against the rebased scratch tree BEFORE rebasing the live lane. Where a block fails there and the repair is a `footprint:` line, leave the live lane un-rebased: rebasing would un-tick boxes the pass just closed and hand the repair to a worker forbidden to make it. Report the resolutions, the failing blocks and the frontmatter edit each needs, and let the orchestrator take both in one move |

Standing observation, repeated because it is still true: step 5's instruction
to run each block "from the root `collect` will run it from — the
orchestrator's checkout, not your lane" cannot be honoured by an implementer
on this route. The build is in the lane and only in the lane; run from the
checkout, every block fails correctly because the code is not there. The
blocks hard-code no path and `collect` will run them unchanged after the
merge — which is exactly why the rebased-scratch run above is the measurement
that matters, and why it deserves the row.

## Scores

complexity: 34
blast-radius: high
workflow: probe-then-spec
