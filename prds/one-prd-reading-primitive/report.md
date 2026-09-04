Verdict: DONE

Second pass of `probe-then-spec` on this PRD, as implementer. The analyst's
pass wrote `specs/spec01-03.md` from a build in a scratch clone that is gone;
the lane held none of it, so this pass entered step 3 for all three specs,
built them in `.pearde/.lanes/one-prd-reading-primitive` and committed them as
`9ac52f5`. 10 of 10 acceptance boxes ticked, each against a command run here.
This PRD's own probe goes 5/10 to 10/10; the other 10 harnesses in the
baseline set print exactly their baseline counts.

## Per-spec box status

**spec01 - `common.py` gains the PRD reader** - 3/3 - `resources/common.py`

- `prd_shape` defined and returning the six-tuple, the malformed fixture
  naming both problems, and `est:   # a note` reading as absent: the block
  prints `spec01: ok` (exit 0).
- The comment-only fix is in `common._clean` now, so every
  `common.split_frontmatter` caller gets it, not only `prdfile.py`'s copy.

**spec02 - guard reads state through the one reader** - 3/3 -
`resources/guard.py`

- `grep -E '^(KEY_RE|ITEM_RE|STATE_RE)\s*=\s*re\.compile' resources/guard.py`
  exits 1, nothing found. `STATE_RE` is gone; `fm_state` is two lines on
  `common.split_frontmatter`.
- `spec02: ok` - `state: open`, `state: open  # note`, `no fence` and a
  frontmatter with no `state:` all read as before.
- The committed guard harness, `PEARDE_ROOT` at the lane, before and after:
  `41 checks - 35 pass - 6 fail` both times, and the failing **set** is
  identical - `FAIL P3 P4 S1 S2 S3 T5`, all inherited, all before the first
  edit.
- `guard.fm_state` and `plan.parse_prd` both return no state for a `prd.md`
  with no `state:` key - one fact, two paths.

**spec03 - prdfile delegates its parse** - 4/4 -
`resources/board/prdfile.py`

- `grep -E '^(KEY_RE|ITEM_RE)\s*=\s*re\.compile' resources/board/prdfile.py`
  exits 1. Both names are `common`'s by alias, as is `strip_comment`.
- `plan`, `specs`, `transitions`, `collect` all import cleanly;
  `plan.KEY_RE = re.compile('^\s*([A-Za-z][A-Za-z0-9_-]*):\s*(.*?)\s*$')`
  still resolves for `specs.fm_lines`.
- `plan.py scan` of the live board, pre-build tree against built tree, run
  back to back: **byte-identical**, 91 lines each. A control pair (the
  pre-build tree scanned twice) was taken in the same minute to prove the
  board itself did not move between them. An earlier pair differed on two
  rows only - this PRD's own box count and a sibling's - which was the live
  board moving under two scans minutes apart, not the code.
- A `prd.md` whose fence never closes now parses to `fm == {}` with the whole
  file as body, the same fact `prd_shape` and `guard.fm_state` report.

Every block was also run the way `collect` runs it -
`bash -e -o pipefail -c "$(awk '/^```sh/{f=1;next} /^```/{f=0} f' <spec>)"`
from the lane root - and each exits 0. Each was then mutated and re-run to
prove it can fail: spec01 with `_clean`'s `^` anchor reverted gave exit 1,
spec02 with a `STATE_RE` appended to `guard.py` gave exit 1, spec03 with the
`common.split_frontmatter` call stubbed out gave exit 1. Every restore proved
by `cmp` against a scratch backup, and `git status --short` in the lane is
clean after them.

## Harnesses

Baseline taken before the first edit, `PEARDE_ROOT` at the lane, run from the
board - the 11 harnesses that name a footprint path
(`grep -ln 'resources/common\.py|resources/guard\.py|resources/board/prdfile\.py'`
over all 98). The full sweep was not run: it is known on this board to
outlast the window.

| harness | before the first edit | after |
|---|---|---|
| `one-prd-reading-primitive` (this PRD's own) | 10 checks - 5 pass - 5 fail | **10 pass - 0 fail** |
| `nothing-left-open/the-skill-tree-is-guarded` | 41 - 35 pass - 6 fail | 41 - 35 pass - 6 fail |
| `a-harness-measures-the-tree-its-worker-built-in` | 19 pass, 1 fail, 20 checks | same |
| `a-session-start-brings-the-board-up` | 46 - 40 pass - 6 fail - 0 skip | same |
| `complexity-is-guarded-like-priority` | 61 - 61 pass - 0 fail | same |
| `nothing-left-open/a-quoted-walk-is-data` | 19 - 19 pass - 0 fail | same |
| `every-module-finds-its-siblings-by-one-rule` | 22 passed, 1 failed | same |
| `the-board-name-is-one-dotted-constant` | red: `PEARDE_BOARD_DIR is not .pearde` | same |
| `the-loop-is-commands` | 61 - 59 pass - 2 fail | same |
| `the-round-runs-in-a-window-that-ends` | 26 - 25 pass - 1 fail | same |
| `guard-on-is-one-command` | 78 - 71 pass - 7 fail | same |

Every red above is recorded as red **before the first edit**. The only count
that moved is this PRD's own probe, and its predicate was run against the
pre-build files to prove the flip is this build's: `git show
1be5d2b:resources/common.py` holds no `def prd_shape` (0 matches) and
`git show 1be5d2b:resources/board/prdfile.py` holds 2 frontmatter regex
definitions.

Repo gate, in the lane, before and after: `python3 resources/index.py check`
exit 1 on the same 3 lines both times (`resources/common.py is on disk with no
row in references/files.md`, and two on a `hotreload-test.js` that is not on
disk) - all three inherited, all outside this footprint. `doctor.sh` exit 1,
rows identical before and after except `harnesses 98 -> 99`: two sibling PRDs
added a `verify.sh` to the board mid-run.

## Findings

Carried forward from the analyst pass, still true or now measured:

- **The lane's base carries three commits that are not on `main`, and one of
  them conflicts.** `lane/one-prd-reading-primitive` was cut at `1be5d2b`,
  which sits on `77665a3` - not on `main` (`4a94475`) - together with
  `e861cca` and `56f7ce5`. Fifteen other lanes share that base.
  `git merge-tree --write-tree --name-only HEAD lane/one-prd-reading-primitive`
  names exactly one conflict, **`references/files.md`**, and it comes from the
  base, not from this build: the same conflict was there before this pass's
  commit, and `git diff 1be5d2b 9ac52f5` touches only the three footprint
  files. This build has no conflict of its own. The repair the orchestrator
  can run without resolving anything outside a footprint is
  `git -C .pearde/.lanes/one-prd-reading-primitive rebase --onto main 1be5d2b`,
  which replays `9ac52f5` alone onto `main` and leaves the siblings' commits
  on their own branches. `attempt-the-build`'s `## Fails when` told me to stop
  and report on a conflict outside the footprint; I report it and did not
  resolve it, and built anyway because the row's premise - that the work might
  already stand somewhere - was false: `prd_shape` existed nowhere, so
  stopping would have produced no build and left the same conflict.
  The analyst pass called this "another PRD's lane"; it is more precisely a
  lane cut from a tip that is not `main`.
- **The source page names a different fourth module in its title.** The
  recovered page titles itself "transitions, guard, collect and **lanes**",
  the body and `## Done when` say "the **plan**". The body is authoritative:
  `resources/board/lanes.py` parses no `prd.md` and was never a fourth reader.
  Unchanged this pass.
- **The `## Done when`'s malformed-fixture example is wrong.** Specs carry no
  `subject:` key; `subject:` is a memo/workflow key. The fixture used instead
  is a `prd.md` with no `state:` and a spec with no closed fence, which is
  what the four paths actually agree about.
- **`transitions.fake_prd` and `registry._scan_one` still build their own
  children/parent graph.** Unchanged, for the analyst's reason: that graph
  serves cross-repo `@member/rel` addressing over a whole scan, not one
  directory. `prd_shape`'s specs/children capability therefore stands
  available and unused by the four modules, which measure only the
  frontmatter-parse consolidation.

New this pass:

- **Two of the three verify blocks could not have passed as written.** Run the
  way `collect` runs them, spec02 exited 127 and spec03 exited 2: both spelled
  the board as the relative `.pearde/...`, which does not exist in a lane, and
  both let a board-wide command (a neighbour's harness; a full `plan.py scan`)
  decide the block's exit - the harness is red on 6 inherited checks, so
  spec02 could never have passed however green this unit was. Repaired per
  `write-the-specs`'s own `## Fails when`: the board is resolved absolutely
  from the shared git dir
  (`BOARD="$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")/.pearde"`,
  correct from the lane and from the checkout, and not a hardcoded root), the
  board-wide command is captured and printed rather than gated on, and each
  block now ends on a bare assertion reading a path in its own `footprint:`.
  `pearde specced one-prd-reading-primitive --check` answers `ok`, with no
  whole-workspace warning left.
- **`resources/common.py` has no row in `references/files.md`.** The index
  gate says so, before and after this pass. `references/files.md` is outside
  this footprint and is also the one file the lane's base conflicts on, so it
  is reported, not fixed - but the file this PRD is about is the one the map
  is missing.
- The board's own `.pearde` worktree holds this pass's spec and report edits
  uncommitted; the lane holds the code as `9ac52f5`.

## Workflow probe-then-spec

| # | step | outcome |
|---|------|---------|
| 1 | `read-the-contract` | pass. `prd.md`, three specs and the analyst's `report.md` read; no `@`/`@@` in the body dangles. Footprint: all three files on disk in the lane. Recorded before the first edit - lane `git status --short` empty at `1be5d2b`; checkout dirty on 15 paths, **none** of them a footprint path, so nothing of this PRD was waiting in the checkout to carry in. The lane's verify blocks spelled a board it does not have: handled by the atomic's last row, `PEARDE_ROOT=<lane>` from the board rather than a symlink, since all 11 baseline harnesses honour it. |
| 2 | `capture-the-harness-baseline` | pass. 11 harnesses plus `index.py check` and `doctor.sh`, all before the first edit, outputs kept under a run-named scratch directory. Sweep narrowed to the footprint-naming subset by the atomic's own row. |
| 3 | `attempt-the-build` | pass. Second pass of the route: the atomic's first row says enter step 3 only for specs whose build is not in the tree - that was all three, checked per spec with `git status` and `git diff`, not on the PRD as a whole. Every change is an edit to an existing footprint file, so it was built in place, not staged under `probe/`. No new PRD directory appeared on the board. One row of this table was applied and departed from, with the reason recorded above and an edit proposed below. |
| 4 | `re-run-the-harnesses` | pass. Same 11, same order, same command line, same `PEARDE_ROOT`. Every count at or above its baseline; the one that rose is this PRD's own probe, shown against the pre-build files rather than claimed. The one doctor row that moved (`harnesses 98 -> 99`) is two siblings landing a harness each. |
| 5 | `write-the-specs` | pass, in its second-pass form: no spec authored, the `## Fails when` table applied to the three blocks that already stood. Two were repaired (board resolved absolutely, board-wide gates captured not gated, a footprint assertion last and bare); each was then proved able to fail. The previous pass's `## Findings` are carried forward by name above, per the table's own row about a report path that already holds one. |

### Edits

Two rows I would change, offered rather than made - the workflow files were
not touched.

**`attempt-the-build` `## Fails when`** - the row beginning *"the brief says
the probe's code is uncommitted, and `git status --short` is clean"* ends
"Where a conflicting file is outside the footprint, stop and report it."
Taken literally that strands a build that has no conflict of its own: on this
board fifteen lanes were cut from a tip that is not `main`, and the conflict
belongs to the base, not to any of them. Replacement for that last clause:

> Where a conflicting file is outside the footprint, run `git diff
> --name-only <lane-base> <your commit>` first. Where your own commits touch
> none of the conflicting files, the conflict is the **lane's base** -
> `lanes.create` cut it from a tip that is not the checkout's branch - and it
> is neither yours to resolve nor a reason to stop: build, commit, and report
> the base with the one command that lands you anyway, `git -C <lane> rebase
> --onto <checkout branch> <lane-base>`, which replays your commits alone.
> Stop only where a conflicting file is one **your own commits touch** and it
> is outside your footprint.

**`capture-the-harness-baseline` `## Fails when`** - the row naming
`statusline` as the row every live session moves is one row short. Add:

> | `doctor`'s `harnesses` row differs between step 2 and step 4 by a count of
> harnesses, not of failures | that row carries the board's harness census,
> and every sibling that lands a probe moves it | compare doctor's rows
> without `statusline` **and without `harnesses`' count**; confirm with `find
> <board>/prds -name verify.sh -newermt <run start>`, which names the
> siblings' new ones. On **darwin** `find`'s `-newermt` takes an ISO
> timestamp (`2026-09-03T18:20`) and refuses `'-40 minutes'` |

No word in the contract was missing from `grammar.py show`, and nothing was
learned outside this repo, so nothing was written back with `knowledge.py
remember`.

## Scores

complexity: 22
blast-radius: mid
workflow: probe-then-spec
