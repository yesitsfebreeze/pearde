# the-largest-module-is-cut-by-responsibility — implementer

Verdict: DONE

17 of 17 boxes ticked, across three specs. This is the route's **fourth** pass.
The third reported DONE with the lane green and the merge proved clean against
`1880990`; `collect` then ran, `land_lane` committed the lane as `932563b`,
and the rebase onto a checkout that had moved four commits further conflicted
in `plan.py`. It wrote nothing and left the PRD `claimed`, the work committed
on `lane/<slug>` and the checkout untouched — the exact shape step 3's
`Fails when` names. Nothing on the board said so.

The work of this pass is that rebase, twice, and one guard that stops the
third from being needed blind.

| spec | boxes | block, run as collect runs it | mutated |
|---|---|---|---|
| `spec01` | 6/6 | exit 0 | exit 1 |
| `spec02` | 6/6 | exit 0 | exit 1 |
| `spec03` | 5/5 | exit 0 | exit 1 |

`probe/verify.sh` is **46 checks · 46 pass · 0 fail** (42 before; four checks
added, named below). The lane is `8d212a7` on top of the checkout's `3b4114d`,
`git merge-base --is-ancestor HEAD lane/<slug>` answers **yes**, and
`git merge-tree --write-tree --name-only HEAD lane/<slug>` names **no
conflicting file**. `lanes.merge`'s `--ff-only` will take it as it stands.

## The lane could not land, and now can

`merge-tree HEAD lane/<slug>` at the start of this pass:

```
resources/board/plan.py

Auto-merging references/files.md
Auto-merging resources/board/plan.py
CONFLICT (content): Merge conflict in resources/board/plan.py
```

One file, inside spec01's footprint. `39c0cab..31620bb` had put 43 lines into
`plan.py` — `NotABoard`, `state_dir`'s husk guard, `session_tree` — and the
cut is a table of **line numbers** over the file, so it was addressing a
revision that no longer existed. The resolution is a re-cut, not a merge.

Every boundary was mapped through a `difflib` diff of `probe/plan.py.orig`
against the new file rather than shifted by hand. All four hunks land whole
inside a single range — `NotABoard` and the husk guard in `boards`,
`session_tree` in `silence`, the `__main__` wrapper in `plan` — so no range
crossed a module boundary. `plan.py.orig` was refreshed to `31620bb`'s
3242-line file (`cmp`-identical to `HEAD:resources/board/plan.py`, still so at
`3b4114d`), and `cut.py`'s own `uncovered` guard proves the table still covers
every non-blank line.

```
boards       470 lines      (449 before this pass)
prdfile      537 lines
repos        134 lines
registry     260 lines
silence      163 lines      (148)
needs        140 lines
vision       215 lines
schedule     519 lines
mapfile      488 lines
plan         644 lines      (637)
```

151 top-level names in the pre-cut file now (149 before — `NotABoard` and
`session_tree` are the two), 148 reachable as `plan.<name>` by value and the
three rebound parse-cache globals through `plan.prdfile`.

The rebase was then run twice: once onto `31620bb`, resolving `plan.py` with
the re-cut, and once more onto `3b4114d` after `every-link-resolves` landed
mid-verification. The second applied cleanly — that sibling touched
`index.md`, `references/files.md` and `references/templates/grammar.md`, all
three in this footprint, and all three three-way merged with no conflict.

## `cut.py` now refuses an input it must not cut

The previous pass reported, as a finding it did not fix, that re-running the
generator on its own output silently destroys the tree: the second run cuts
the already-cut 644-line `plan.py` into ten stubs and every count collapses,
with nothing in the harness saying so. It cost that pass a run. It is one
`if` and it is now in `cut.py`, beside a named base revision:

```
BASE = "31620bb"
BASE_LINES = 3242
```

Proved: a second consecutive run of `cut.py` against the same tree now stops
with `resources/board/plan.py is 644 lines; the table addresses 31620bb, which
is 3242. Restore the input from plan.py.orig beside this script …`, and writes
nothing. The `uncovered` guard catches a file that grew; this one catches a
file that is the wrong file altogether.

## A traceback that is a sibling's, and how the block says so

`probe` section E asserted `raises no exception` on all four harnesses. After
the rebase, `one-predicate-for-dispatchable` raised one. It is not this unit's:

| tree | one-predicate-for-dispatchable |
|---|---|
| checkout `1880990`, no cut | 33 FAIL · **0** traceback |
| checkout `39c0cab`, no cut | 33 FAIL · **1** traceback |
| checkout `31620bb`, no cut | 33 FAIL · 1 traceback |
| lane, with the cut | 29 FAIL · 1 traceback |

Bisected to `39c0cab` — *the daemon must not write into a board path it no
longer owns*. `state_dir` there stopped calling `die()` and started raising
`NotABoard`. That is right for the daemon and right for the CLI, which catches
it at `__main__`; it is wrong for every caller that is neither, and a harness
calling in through `python3 -c` is one. `one-predicate-for-dispatchable`'s
fixture hands it a path carrying no board, so what used to be a one-line
refusal is now an uncaught traceback and `compute_plan` returns `None`.

The cut moves that code verbatim into `boards.py`; it does not author it, and
nothing in this footprint closes it. A blanket "no Traceback" in spec03's
block would therefore be a file outside the footprint deciding the block's
exit — the thing step 5 forbids. Both the probe and spec03's block now carry a
**per-row traceback baseline** beside the per-row FAIL baseline they already
had, measured on a tree with no cut in it. A traceback the cut adds, on this
row or any other, still fails the block; the sibling's does not.

The weaker half of spec03's box 2 went with it. It read *"none of them names
`dispatchable`, `compute_plan` or `plan_frontier`"*, and one of the 29 always
did — `compute_plan holds the container in its collect list`, a behavioural
FAIL of that harness's own, red at `1880990` with no cut in the tree. A word
match on a FAIL label was never the thing the box meant. It now names the four
assertions spec03 actually re-points, and **the block and the probe assert
them by name** — four checks that did not exist before:

```
  ok   E re-pointed: schedule.py defines dispatchable once
  ok   E re-pointed: cmd_scan calls it on the free set
  ok   E re-pointed: compute_plan holds what it refuses
  ok   E re-pointed: plan_frontier reads the hold
```

A FAIL count that merely does not rise would pass with one of those broken and
another closed by a fixture. This is strictly more than the box asserted
before, not less.

## Workflow probe-then-spec

| # | step | verdict | note |
|---|------|---------|------|
| 1 | `read-the-contract` | pass | PRD, three specs, `probe/`, the previous pass's `report.md`; `git status --short` in lane (clean — the row that says a sibling or `land_lane` committed), checkout (`M references/system.md`) and board (259 dirty, none mine) before the first edit |
| 2 | `capture-the-harness-baseline` | pass | probe 42/42 in the lane; `index.py check` 2 lines lane / 1 checkout; the four harnesses at 1/29/0/0; each also measured on the **checkout with no cut** at 7/33/6/0, which is the control the flip is claimed against |
| 3 | `attempt-the-build` | **re-entered** for spec01 | the build was in the tree and green, against a `plan.py` that had moved — indistinguishable from done to every harness in the lane, and refused by `collect`. Re-cut; spec02 and spec03 were not entered |
| 4 | `re-run-the-harnesses` | pass | probe 46/46; every count at or under baseline; every flip shown against a tree without the build |
| 5 | `write-the-specs` | applied, not authored | three `Fails when` rows fired: a stale line-number table, a check whose exit a file outside the footprint decided, and a box whose words did not match the shape it meant |

### Edits

Two shapes, neither in the atomics. No workflow file was touched.

| atomic | seen | means | do |
|---|---|---|----|
| `attempt-the-build` | the previous pass proved the merge clean and reported DONE, and the merge conflicts anyway | a merge proved against the checkout's HEAD is proved against a **moment**, not against a state. `collect` may run minutes or a day later, and `land_lane` **commits the lane first**: a conflict then leaves the work committed on `lane/<slug>`, the checkout untouched, the PRD `claimed`, and nothing on the board recording the attempt. The next worker's `git status --short` in the lane is clean, which reads as "nothing built" | on any pass whose lane is clean and whose brief says the code is uncommitted, `git log -1 <lane>` before concluding anything, then `merge-base --is-ancestor HEAD lane/<slug>` and `merge-tree --write-tree --name-only`. Re-prove the merge **last**, after every other check, and quote the HEAD it was proved against — a proof taken before the verification run is already stale by the length of the run |
| `re-run-the-harnesses` | a harness the contract does not touch raises a traceback that was not there at the baseline, and the count of FAILs is unchanged | an exception is not a FAIL and no count catches it; a landed sibling can add one to a harness in your footprint without moving a single number you baselined | baseline the **traceback count** per harness beside the FAIL count, and take both on a tree that does not hold your build. Then bisect it: `git clone --shared` the checkout at each commit since the lane's base and run the harness there. A traceback present with and without your build is the sibling's, and belongs in the block as a baseline, never as a wall |

## The boxes, and what each was measured with

Every box was re-measured on the rebased lane. Nothing is inherited.

### spec01 — 6/6

- ten modules, none over 700: the table above, `wc -l` in the block and
  probe section A, twelve checks green.
- every name reachable as `plan.<name>`: probe section B, `MISSING=0`, read
  with `ast` against `probe/plan.py.orig` so a name spelled twice cannot pass
  it. 151 names, 148 by value, three through `plan.prdfile`.
- `python3 resources/pearde.py help` exits 0 with no `failed to import`.
- probe section C: `scan`, `plan`, `status`, `members`, `calibrate`,
  `reconcile`, `vision --check` and `example` all exit 0, and `example` names
  `plan.py` and not the file the code moved into.
- `pearde calibrate` prints `hard-coded in mapfile.py`;
  `grep -rn 'hard-coded in plan.py' resources/board/plan.py` returns nothing.
- the order is a DAG: `import plan` from `resources/board` raises no
  partially-initialized-module error.

### spec02 — 6/6

- `index.py check` names no module of the cut and no file this spec edits.
  In the checkout, with neither the modules nor the rows: **0 problems, exit
  0**. In the lane, with both: **1**, and it is
  `references/parts/commits.md references @pearde/memos/… — not on disk`,
  the lane's missing board dangling by construction, which closes on the
  merge. `doctor`'s `index` row is `ok  160 files · 38 keywords · every anchor
  resolves` in the checkout and that one problem in the lane; every other
  doctor row is byte-identical between the two roots.
- `references/files.md` holds exactly one row per module — nine `= 1`.
- all five `@@` scopes name a module the code moved into:
  `@@board → boards, prdfile · @@order → schedule, vision · @@view → mapfile ·
  @@pass → mapfile · @@machine → schedule`. Re-checked after
  `every-link-resolves` rewrote `index.md` under the run.
- no file under `references/` says `silent_of`, `_scan_one`, `TUNE` or `1.618`
  on a line with `plan.py`.
- `pearde calibrate` names `mapfile.py`.
- the count is printed beside the exit and no number is asserted. It moved
  from 3 to 2 to 1 to 0 in the checkout over four passes, which is the whole
  argument for not asserting it.

### spec03 — 5/5

```
the-board-runs-itself/one-command:                      1 FAIL (was 1), 0 traceback (was 0), harness exit 1
the-tool-keeps-its-word/one-predicate-for-dispatchable: 29 FAIL (was 29), 1 traceback (was 1), harness exit 1
complexity-is-guarded-like-priority:                    0 FAIL (was 0), 0 traceback (was 0), harness exit 0
scan-parses-the-board-once-and-caches-it-by-mtime:      0 FAIL (was 0), 0 traceback (was 0), harness exit 0
```

Each flip is shown against the checkout at `31620bb`, which holds none of this
build — the whole gate run on the old file, which is stronger than
`git show HEAD:`:

| harness | checkout, no cut | lane, with the cut |
|---|---|---|
| `one-command` | 7 FAIL | 1 FAIL |
| `one-predicate-for-dispatchable` | 33 FAIL · 1 tb | 29 FAIL · 1 tb |
| `complexity-is-guarded-like-priority` | 6 FAIL · 1 tb | 0 FAIL · 0 tb |
| `scan-parses-…` | 0 FAIL · **1 tb** | 0 FAIL · **0 tb** |

The last row is the parse-cache one: without the cut, `planlib.prdfile._PCACHE`
does not exist and the harness raises. Box 4's "no `Traceback`" is this unit's
flip, and it is the reason a blanket traceback guard could not simply be
dropped — one row's zero is earned.

Box 5 — no expectation deleted or weakened — re-measured against the board's
own `HEAD` for all four. Seven `eq`/`has`/`check` lines are removed and seven
re-pointed ones replace them, each keeping its expectation: four in
`one-predicate-for-dispatchable` (`$PLAN` → `$SCHED`) and three in
`complexity-is-guarded-like-priority` (`$PLAN` → `$PRDF`, `$SCHED`, and
`float() CALLS remaining` still `3`, now summed over `prdfile.py` and
`silence.py` because the three functions it counts split across two files).
The rest of each diff is a live sibling's — see the findings.

## Each block proved red under a mutation

Backed up outside the repo, restored with `cp`, proved with `cmp`.

| spec | mutation | kind | green | mutated | restored |
|---|---|---|---|---|---|
| `spec01` | `SILENT_STATES` dropped from `plan.py`'s re-export of `silence` | behavioural — the name is genuinely unreachable as `plan.SILENT_STATES` | 0 | 1 (`FAIL B … want [0] got [1]`) | 0 |
| `spec02` | `boards.py`'s row deleted from `references/files.md` | behavioural — `index.py check` *computes* an extra problem naming a footprint file | 0 | 1 | 0 |
| `spec03` | `dispatchable` renamed in `schedule.py` | behavioural — `one-command` goes 1 → **11** FAIL and 0 → **1** traceback, because `plan.py` can no longer import it; the FAIL guard and the new traceback guard both fire | 0 | 1 | 0 |

All three are behavioural. Each block was run as `collect` runs it,
`bash -e -o pipefail -c "$(awk …)"`, from the root the merge produces.

## Findings

Carried forward by name, with what this pass adds.

- **A harness pinned to the absence of a diff.** *(analyst's, then two
  implementers'; re-measured, still open.)*
  `seven-closed-probes-drifted-red/the-fixtures-meet-the-tool` check F asserts
  `git diff --name-only -- resources/board/plan.py resources/board/init.py`
  counts zero. This PRD's contract is a diff to `resources/board/plan.py`, so
  check F is red for this build by construction. The repair is owed to that
  harness's own PRD —
  `.pearde/memos/a-harness-that-reads-the-whole-checkout-is-not-a-harness.md`.
- **The sibling's rule will not know about these nine files.** *(analyst's;
  unchanged and still true.)* `every-module-finds-its-siblings-by-one-rule`
  asserts *"no module imports a sibling without the rule (plan.py excepted)"*,
  and the nine carry the hand-rolled `sys.path` preamble `plan.py` had when
  the cut was taken. Whichever lands second adopts the other's rule. The
  preamble is copied by `cut.py`, so adopting it is one edit to `cut.py` and a
  re-cut, not nine edits.
- **The four harnesses carry a live sibling's hunks.** *(last implementer's;
  re-measured, still true and now visible in every diff.)*
  `a-harness-measures-the-tree-its-worker-built-in` has uncommitted hunks in
  all four of spec03's footprint files — the `BOARD`-walking `PEARDE_ROOT`
  preamble, and in `scan-parses-…` a whole rewrite from a millisecond bench to
  a work census. The board is one copy shared by every lane
  (`<lane>/.pearde` is a symlink to it), so the two footprints overlap with no
  worktree between them. Whichever collects second inherits the other's text
  under its own boxes. Worth an explicit merge order rather than luck. The
  board also still shows
  `D prds/scan-parses-…/probe/__pycache__/parsecache.cpython-314.pyc`, a
  tracked build artifact deleted with that sibling's rewrite, not mine.
- **`index.py check`'s inherited set.** *(analyst's, as a count; superseded
  twice.)* 3 → 2 → 1 → **0** in the checkout across four passes. Nothing
  asserts a number any more, which is why this pass did not have to touch it.
- **The board moved under the run.** *(analyst's, and every pass since; it
  moved twice during this one.)* `every-link-resolves` landed two commits
  between the first rebase and the verification run, and `references/system.md`
  went from dirty to committed under me. Nothing on the board tells a worker
  its lane has gone stale, and every harness in the lane stays green while it
  does. The step-3 edit above is the case for it.
- **The machine ran out of disk mid-run.** *(last implementer's; **reproduced
  this pass.**)* `ENOSPC` from the tool harness itself while five
  `git clone --shared` trees were on disk for the traceback bisect;
  `/System/Volumes/Data` reached 100% with 138Mi free. Removing the clones
  recovered it and the bisect was finished from the saved outputs. A worker
  that clones the checkout per commit to bisect is one of the heavier things
  this board asks for, and there is no headroom for it.
- **The knowledge record had no gap to enqueue.** *(analyst's; still true —
  nothing this pass learned came from outside this repo.)*

New this pass:

- **`land_lane` commits before it merges, and a conflict leaves no trace.**
  This is the finding that cost the board a whole pass. The third pass ended
  DONE with the merge proved clean; `collect` ran, committed the lane, hit the
  conflict, wrote nothing, and left the PRD `claimed` with no `## Failure`, no
  transition row, and a lane whose `git status` is clean. The next worker's
  first honest reading of that tree is "the build is not here". Two cheap
  repairs, neither in this footprint: `land_lane` could write the conflicting
  paths into the PRD on `Stop`, and `collect` could re-prove the merge itself
  rather than trusting a report's claim about a HEAD that has moved.
- **A worker cannot prove a merge that has not happened yet.** Every merge
  proof in this report was true when taken and one of them was false eleven
  minutes later. The only durable statement a worker can make is *the lane is
  a fast-forward of `<sha>`*, and the orchestrator has to re-check it at the
  moment it merges. Worth `collect` running `merge-base --is-ancestor` before
  it commits anything, and rebasing rather than refusing where the conflict
  set is inside the PRD's own footprint.
- **`state_dir`'s refusal is a traceback for every caller but two.**
  `39c0cab` traded `die()` for `raise NotABoard`, correctly for the daemon and
  for the CLI, which catches it at `__main__`. Nothing else does. A `python3
  -c` importing `plan` — which is how a good many harnesses on this board
  reach the code — now gets a traceback where it got a one-line refusal, and
  `compute_plan` comes back `None`. Measured: `one-predicate-for-dispatchable`
  0 tracebacks at `1880990`, 1 at `39c0cab`, unchanged since. It is a defect
  in that PRD's landing, not in this one's cut, and the fix is a `NotABoard`
  handler at the library boundary rather than only at the process one.

## What I did not do

- I did not commit new work. The lane's single commit is `land_lane`'s, from
  the failed `collect`; this pass rebased it twice and resolved `plan.py` into
  it. Nothing else was committed and nothing was pushed.
- I did not touch a workflow or atomic file. The two edits owed are in the
  table above.
- I did not repair `the-fixtures-meet-the-tool`, the sibling's overlapping
  hunks in the four harnesses, the missing sibling rule, or
  `one-predicate-for-dispatchable`'s fixture. All four are outside this
  contract and named as findings. In particular I did not repair that
  fixture even though the file is in this footprint: spec03's own box 5
  promises the diff changes only file paths and module prefixes, and a fixture
  repair would break that promise to hide a sibling's regression.
- I did not restart the view service or write to another PRD's files. The
  three files mutated for the can-it-fail proofs were restored in the same
  command and proved by `cmp`.

## Grammar

No word in the contract was undefined. Nothing to add.

## Scores

complexity: 29
blast-radius: high
workflow: probe-then-spec
