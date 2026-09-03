# board-rel-is-a-third-wrong-board-path-resolution — implementer, pass two

Verdict: DONE

Second pass of `probe-then-spec` on this PRD. The analyst's pass built and
specced the whole change; nothing of it was missing, so step 3 was entered for
no spec. What this pass owed was the sentence the spec's own **What is left**
wrote down: *land it, and re-take the counts on the tree the implementer
holds*. The lane was cut at `64ed54a`; the checkout has since moved to
`1880990`, where the sibling
`collect-resolves-a-board-path-two-ways-and-both-are-wrong` landed in the same
file. Every count below was therefore re-taken on the **merged** tree — the
checkout at `1880990` with the lane's diff applied — and the whole gate was run
verbatim on the checkout **without** the build as the red side of the flip.

All 7 acceptance boxes of `spec01` are ticked and every one was re-run this
pass. The build stands in the lane, uncommitted, exactly as pass one left it:
`collect` lands it.

## What this pass changed

Two edits, both inside the PRD's own folder — no line of `collect.py` moved.

- `specs/spec01.md`, last acceptance box: `a-board-s-own-file-commits-in-the-board-repo`
  read `12 PASS`. Measured now it is **20 PASS**. The invariant grew by eight
  checks inside the sibling's commit `1880990`; the number in the box was
  honest when pass one wrote it and stale by the time an implementer read it.
  Every other count in that box is unchanged.
- `specs/spec01.md`, frontmatter `footprint:`: added
  `references/parts/commits.md`. See **Findings** — this is a wrong footprint
  the first pass left, not new work.
- `specs/spec01.md`, **What is left** paragraph rewritten to say what was
  re-measured and against which commit.

## The flip, shown against the tree that does not hold the build

The spec's whole `## Verify and Proof` block, extracted and run the way
`collect` runs it (`bash -e -o pipefail`):

| tree | command | exit |
|---|---|---|
| checkout `1880990`, **no build** | block verbatim from `/Users/feb/dev/infra/pearde` | **1** |
| merged (`1880990` + lane diff) | block verbatim from the merged root | **0** |

This is stronger than a `git show HEAD:` predicate diff and replaces it: the
whole gate ran on the old file and failed. The old file is
`HEAD:resources/board/collect.py` in the checkout — clean, committed, and
holding neither `board_prefix` nor `under_board`.

The PRD's own probe, same two trees, same `PEARDE_ROOT` convention:

- checkout, no build — `probe: 4 check(s) failed`, 14 PASS, exit 1. The four
  are exactly the four the probe's own header predicts against the pre-PRD
  module: `the arithmetic rows did not run` (there is no `board_prefix` to
  import), `own-repo: the memo written after the claim rides into the commit`,
  `own-repo: the board's own .state/ ledger is not even listed`, and
  `nested-in-code: the board dotfile the footprint names is added anyway`.
- merged — **24 PASS, 0 FAIL**, `probe: 0 check(s) failed`, exit 0.

Behavioural mutation, not a string one. `board_prefix`'s return was changed to
`os.path.relpath(b, r)` unconditionally — the `"."` answer this PRD exists to
remove — leaving every heading and function name the block greps for intact.
The block exited **1** on the arithmetic assertion
(`assert c.board_prefix("/r/pearde", "/r/pearde") == ""`), not on a grep.
Restored by `cp` from a scratch copy outside the repo and proved back with
`cmp` (clean); the block exits 0 again after the restore. So the block detects
a regression in what the tool computes, not merely that a counter is wired.

## Counts, before the first edit and after

Every harness run with `PEARDE_ROOT` set to the tree under test,
`PEARDE_HARNESSES=1`, `PEARDE_PORT=1`, stdin `/dev/null`.

| harness | checkout `1880990` (no build) | merged (with build) |
|---|---|---|
| `collect-keeps-its-word` | `101 checks · 101 pass · 0 fail` | `101 checks · 101 pass · 0 fail` |
| `collect-is-a-command` | `133 checks · 133 pass · 0 fail` | `133 checks · 133 pass · 0 fail` |
| `hunks-land-where-they-came-from` | `47 checks · 47 pass · 0 fail` | `47 checks · 47 pass · 0 fail` |
| `filing-refuses-a-file-it-does-not-hold` | `52 checks · 52 pass · 0 fail` | `52 checks · 52 pass · 0 fail` |
| `collect-must-not-reset-the-checkout-it-did-not-write` | `31 checks · 31 pass · 0 fail` | `31 checks · 31 pass · 0 fail` |
| `a-board-s-own-file-commits-in-the-board-repo` | 20 PASS · 0 FAIL · exit 0 | 20 PASS · 0 FAIL · exit 0 |
| PRD probe | 14 PASS · **4 FAIL** · exit 1 | **24 PASS · 0 FAIL** · exit 0 |

No count dropped. The only count that moves is the PRD's own probe, and it
moves in the direction the contract asks for.

## The repo's own gate, both roots, before the first edit

- `python3 resources/index.py check` — **exit 1** in the checkout and exit 1 in
  the merged tree, on one line, byte-identical in both:
  `references/language.md references @references/personas/writer.md — not on disk`.
  Outside the footprint, present on both sides of the build: inherited, not
  mine, and not closed by this unit.
- `bash resources/doctor.sh` — exit 1 in the checkout before the first edit,
  three `broken` rows, all inherited and all outside the footprint: `index`
  (the line above), `origin` (`33 derived · 1 with no from:`), `knowledge`
  (`graph.json is behind the files: 260902-4f91, 260902-aae0`). `harnesses` and
  `jstests` are `off` by settings. Every other row `ok`, including `board`
  (142 PRDs) and `view` (watching).

## The number the contract asks to be measured

The PRD's *Done when* asks that the mis-sorted paths sort as the board's own
and that the count be measured rather than asserted. Measured today against
the live board with the merged module:

```
board_root                     : /Users/feb/dev/infra/pearde/pearde   (the board IS its repo)
old board_rel (os.path.relpath): '.'
new board_rel (board_prefix)   : ''
dirty board paths              : 530
recognised as the board's own  : old 0   new 530
swallowed as machine-local     : old 0   new 6
```

The six are `.state/history.jsonl`, `.state/pass.md`,
`.state/transitions.jsonl`, `.state/pass.a-harness-and-the-collect-incident.md`,
`.state/pass.dispatcher-cleanup.md`, `.state/pass.lanes-forensics.md` — the
`.state/` ledgers the PRD names, listed to a person as decisions before this
change and dropped in silence after it. 530 today against the 543/523 pass one
measured on 2026-09-02; the board has had PRDs land since, so the population
moved. The shape is what the contract states: **zero** recognised before,
**all of them** after.

## The merge collect will run

`lanes.merge` rebases the lane onto the checkout's branch before its
`--ff-only` merge, and the lane is behind by two commits (`ba69efa`,
`1880990`), both of which touch `resources/board/collect.py`. Proved before the
merge rather than discovered in it: `git clone --shared` of the checkout at
`1880990` into scratch, then `git apply --3way` of the lane's whole diff —

```
Applied patch to 'references/parts/commits.md' cleanly.
Applied patch to 'resources/board/collect.py' cleanly.
```

The two sets of hunks are in different functions and do not touch. The
sibling's work is `holder`, `same_dir`, `foot_places`, `foot_root`,
`tracked_in`, `_park` and the footprint-grouping loop; this PRD's is
`board_prefix`, `under_board`, `scratch`, the `board_rel` assignment, the
dotfile-skip guard and the rider sweep's test. The rebase has nothing to
resolve.

## Findings

**A wrong footprint the first pass left, now repaired in the spec.** The lane
carries an uncommitted edit to `references/parts/commits.md` — 26 added lines
writing down the rule this PRD implements: the board's own edits ride, its
machine-local dotfiles do not, and the prefix that decides both is empty on a
board that is its own repo. `spec01`'s `footprint:` named only
`resources/board/collect.py`. `land_lane` scopes its commit to the footprint
and leaves everything else standing in the lane with `outside the footprint,
left in the lane` — so the paragraph would have been stranded on the lane
branch and the PRD would have closed with the documentation unwritten. Adding
the path to `footprint:` is the repair the workflow's own step-4 table
prescribes (*put the file in the spec's `footprint:`*), and this route hands
spec authorship to the worker at step 5, frontmatter included. It reddens
nothing: `check_spec` requires that *at least one* footprint path appear in the
verify block, not all of them, and no command in the block reads `commits.md`.
`pearde specced … --check --as engineer` answers `ok · complexity 14 ·
footprint references/parts/commits.md, resources/board/collect.py`. The PRD's
*Must not change* asks that a footprint outside `collect.py` be justified; that
is this paragraph.

**`specced --check` warns `7 of 7 boxes already ticked before an implementer
ran them`.** That is this route's second pass by construction — the analyst
probes, builds and ticks, and an implementer is then dispatched on the same
route. Every one of the seven was re-run this pass against the merged tree and
the output is quoted above. The warning is about the shape of the route, not
about this set.

**A live sibling is writing the checkout.** `references/system.md` went dirty
in `/Users/feb/dev/infra/pearde` mid-run (5 insertions, 5 deletions), and was
clean when this pass took its baseline. It is outside this footprint and is not
this pass's. The checkout's `HEAD` did not move (`1880990` at both ends of the
run).

**The board harness set was not swept.** 76 `verify.sh` under `pearde/prds`.
The set baselined here is the six the spec's last box names plus the PRD's own
probe — the ones that read `resources/board/collect.py`. A full 76-harness
sweep is `doctor.sh --harnesses`, which the board has `off` by settings and
which no box here asks for.

## Workflow probe-then-spec

| # | step | outcome |
|---|------|---------|
| 1 | `read-the-contract` | pass. `prd.md` read (body unchanged during the run; only the `claim:` key moved, at 09:00). `specs/spec01.md` read. `@resources/board/collect.py` resolved. `git status --short` recorded in all three roots — lane (2 modified, pass one's build), checkout (clean at start), board (dirty, 530 paths). Every `@` resolved; no dangling reference. |
| 2 | `capture-the-harness-baseline` | pass. Board root located at `pearde/`, a git repo of its own, **not** the code repo. Six board harnesses plus the repo gate baselined before the first edit, each with `PEARDE_ROOT` explicit. All six honour `PEARDE_ROOT`; one (`filing-refuses-a-file-it-does-not-hold`) also uses `pwd -P`, and it was run with `PEARDE_ROOT` set both times, so both runs measure the same tree. |
| 3 | `attempt-the-build` | not entered — no spec's build was missing. The second-pass row of this step's own `Fails when` table. `spec01`'s footprint was checked with `git status --short` and `git diff` before deciding, not the PRD's as a whole. |
| 4 | `re-run-the-harnesses` | pass. Every baselined count re-taken on the merged tree with the same command line and the same `PEARDE_ROOT`. No count dropped. The one count that rose is the PRD's own probe, 14→24, and it is this unit's — shown by running the whole gate verbatim on the tree without the build, where it exits 1. |
| 5 | `write-the-specs` | pass, applied as the second-pass row describes: the existing block was run the way `collect` runs it (`bash -e -o pipefail`) on a green tree (exit 0), on a tree without the build (exit 1), and under a behavioural mutation of one footprint file (exit 1, restored, `cmp` clean). The stale count in one box was replaced with quoted output, and the wrong footprint repaired. |

### Edits

No edit is owed to `probe-then-spec` or to any atomic. Every failure this run
met was named by a row already in the route: the second-pass shape of steps 3
and 5 (step 3's table), the lane behind the checkout with a sibling's build in
the same file (step 3's `the brief says the probe's code is uncommitted` row
and step 5's rebuild-the-merged-tree row), a box whose count no longer matches
what its command prints (step 5's table), a footprint file that must ride and
is not in `footprint:` (step 4's table), and a repo-wide gate red on an
inherited line outside the footprint (step 2's and step 4's tables). Each was
followed as written and each held.
