Verdict: DONE

# the-vision-file-s-edges-fold-into-needs — implementer, pass two

Built in the lane `/Users/feb/dev/infra/pearde/.pearde/.lanes/the-vision-file-s-edges-fold-into-needs`.
Four files modified, all inside the footprint, uncommitted for `land_lane`:
`resources/board/vision.py`, `resources/doctor.sh`, `references/parts/order.md`,
`references/templates/vision.doc.md`.

## The probe's code was not in the tree — it was rebuilt

The brief says the tree already holds the probe's uncommitted code. It does
not. `git status --short` in the lane was **empty**, and the orchestrator's
checkout carries no hunk in any of the four files either (`git diff --
resources/board/vision.py references/parts/order.md
references/templates/vision.doc.md` is empty; the checkout's `M
resources/doctor.sh` is a **neighbour's** hunk — the `purge` lifecycle row at
line ~862, not this PRD's vision row at ~552). Only
`prds/the-vision-file-s-edges-fold-into-needs/probe/verify.sh` survived, on the
board. The PRD body's own note — "a concurrent collect parked it" — is the
explanation. So pass two re-implemented the three code hunks from `spec01.md`'s
`## What stands from the probe`, which describes them exactly, and the probe
now passes 11/11 against them.

## What landed

`resources/board/vision.py` — the `edges:` loop no longer calls
`after[ra].add(rb)`. Where both ends resolve and `ra != rb`, it checks `rb not
in after[ra]` (a graph built from `needs:` and a parent's children alone, above
this loop) and appends `f"the vision says {b} needs {a}; {b} does not"` to
`dangling`. The dangling-end (`bad`) branch is untouched. The docstring said
depth is computed over "`needs:` plus `edges:`" and that `dangling` lists only
names that resolve to no PRD — both were false after the change, so both now
read the new contract; one comment on the loop says an edge checks `needs:` and
never adds a hop.

`resources/doctor.sh` — the `vision broken` row said `N name(s) in vision.md
resolve(s) to no PRD`, which is false for the new report (both names *do*
resolve). It now reads `N problem(s) in vision.md`, the `fix` line covers both
causes, and the section comment names both.

`references/parts/order.md` and `references/templates/vision.doc.md` — both
said depth is counted over "`needs:` plus `edges:`". Both now say `needs:`
alone and name `edges:` as a check, with the report's exact wording and the
one-line fix; `vision.doc.md`'s `edges` table row now says the key is never an
input to the plan and stays mostly empty.

## Acceptance — every box run, output quoted

| box | run | output |
|---|---|---|
| 1 probe | `PEARDE_ROOT=<lane> bash .pearde/prds/…/probe/verify.sh` | `verify: 11/11 checks pass`, exit 0, no ` FAIL` line |
| 2 byte-identical plan | probe checks 1–3 | `ok vision output byte-identical…` · `ok vision --json byte-identical…` · `ok --check exits 0 on a fully-declared edge` |
| 3 undeclared edge reported | probe checks 6–9 | `ok --check exits 1 on an undeclared edge` · `ok the pair is named, PRD-named` · `ok doctor's vision row carries the same line` · `ok adding the matching needs: silences the report` |
| 4 dangling end unchanged | probe checks 10–11 | `ok --check exits 1 on a dangling edge end` · `ok the dangling end is still named the old way` |
| 5 no hop from an edge | `grep -c 'after\[ra\]\.add(rb)' resources/board/vision.py` | `0` |

`python3 resources/pearde.py specced … --check` → `ok · complexity 12` (with
the expected `5 of 5 boxes already ticked` warn: this route ticks at spec time
and pass two re-ran every one).

## The spec's own blocks, against `write-the-specs`' `## Fails when`

Step 5 on a second pass applies that table to the blocks that already stand.
Three rows fired, all fixed in `specs/spec01.md`:

1. *"a box or block asserts a literal total of the PRD's own probe"* — box 1
   read `ends 'verify: 11/11 checks pass'`, an equality that walls the harness
   shut. It now asserts the tally **parses**, that no ` FAIL` line printed, and
   a **floor** of 11.
2. *"a board-wide gate decides the block's exit"* — the block ended on a bare
   `python3 resources/index.py check`, which is red today on three inherited
   rows (`resources/common.py` has no `files.md` row;
   `@resources/board/hotreload-test.js` listed and absent, twice). Under `-e`
   that spec could never have passed however green the work was. The gate is
   now captured, its rows printed, its exit refused only on a crash (`rc > 1`),
   and only a line naming one of *this* footprint's files fails the block.
3. *"a block exits non-zero on the result that means it passed"* — `grep -c
   'after\[ra\]\.add(rb)'` prints `0` **and exits 1** on success, killing the
   block at line two. The producer is now guarded (`{ … || true; }`) and the
   assertion written as `if grep -q …; then exit 1; fi`.

Two more corrections in the same block: it spelled `prds/…` where `collect`'s
cwd is the **code repo**, so the path never resolved; and it ran the probe with
no `PEARDE_ROOT`, so the harness measured the orchestrator's checkout whatever
tree collect handed it. The block now walks up for the `.pearde/` that holds
this PRD (a lane sits *inside* the board and has none of its own), refuses an
empty board rather than sweeping it vacuously, and runs the probe with
`PEARDE_ROOT="$PWD"`. No `cd`.

Proved both ways, the way `collect` runs it —
`bash -e -o pipefail -c "$(awk '/^```sh/{f=1;next} /^```/{f=0} f' spec01.md)"`:
**exit 0** from the lane, **exit 1** from the unedited checkout
(`verify: 7/11 checks pass`). The block cannot read green on a tree without the
change.

## Harness baseline and re-run

Set: the thirteen harnesses matching `grep -l vision`, run from the board with
`PEARDE_ROOT=<lane>`. Outputs under
`/private/tmp/claude-501/-Users-feb-dev-infra-pearde/1843477b-581c-4854-af0e-e7aad727b949/scratchpad/vision-edges/{base,after}/`.

| harness | before | after |
|---|---|---|
| this PRD's probe | `7/11` | `11/11` |
| `the-board-runs-itself/vision-is-first-class` | `52/52` | `47/52` — see below |
| `upgrade-leaves-the-memo-index-stale` | `17 pass · 22 fail · 1 skip` | `18 pass · 22 fail · 0 skip` — a **neighbour's**: the skip is "the vault list moved while this ran"; no failing line moved |
| the other ten | — | byte-identical counts |

Gate: `python3 resources/index.py check` in the lane is `diff`-identical to its
baseline (same three inherited rows, exit 1). `bash resources/doctor.sh` with
`PEARDE_ROOT=<lane>`: the `vision` row is unchanged (`ok · 1 terminal · 0 on ·
70 off`) — the live `vision.md` declares no edges, so the new check reports
nothing. The only doctor lines that moved are neighbours': `statusline` counts,
`knowledge` going `broken → ok` (another session relinked the graph), and
`harnesses 99 → 100` (another session landed a probe).

Merge safety: `resources/doctor.sh` is also modified, uncommitted, in the
checkout. The hunks are ~310 lines apart. Proved rather than assumed — cloned
the checkout to scratch, committed the neighbour's working copy there, and
`git apply --3way` of the lane's whole diff: *"Applied patch to
'resources/doctor.sh' cleanly"*, all four files clean.

## Findings

### 1 — a sibling's committed probe encodes the contract this PRD replaces

*(carried forward from pass one's report and pass one's `spec01.md`, and now
measured with exact replacements)*

`prds/the-board-runs-itself/vision-is-first-class/probe/verify.sh` — a
different, already-`done` PRD — asserts the old edges-as-hop semantics
directly. Baseline `52/52`, now `47/52`. It is outside this PRD's footprint and
was **not** edited: one writer per file, and this is the orchestrator's edit on
the transition. The five failures and their exact replacements, each measured
against the built lane:

**a. the fixture's two `edges:` must become the PRDs' own `needs:`.** The
section `## the rules copied from vision.py` relies on `"asking -> landed"` and
`"next -> big/second"` placing `asking`, `next` and `building` on the axis.
Insert immediately **before** the `printf … > "$B/vision.md"` on that section's
second line (the earlier sections have already run, so the fixture may be
rewritten here — this PRD's own probe does the same):

```sh
# `edges:` orders nothing: the hops are the PRDs' own `needs:`, and the two
# edges are kept only to prove a declared edge reports nothing.
printf -- '---\nstate: done\npriority: 50\nneeds:\n  - asking\n---\n\n# landed\n' > "$PRDS/landed/prd.md"
printf -- '---\nstate: open\npriority: 30\nneeds:\n  - next\n---\n\n# big/second\n' > "$PRDS/big/second/prd.md"
```

With that, lines 88, 89, 90 (`asking=0`, `next=2`, `building=3`) and line 93
(`axis: 5 on · 1 off`) pass unchanged. Measured.

**b. line 102 — the doctor row's wording.** As it stands:

```sh
has "doctor: vision broken"          "$DOC" "vision      broken  2 names in vision.md resolve to no PRD"
```

as it should read:

```sh
has "doctor: vision broken"          "$DOC" "vision      broken  2 problems in vision.md"
```

**c. line 105 — a consequence of (a), not of this PRD.** Adding those `needs:`
changes the axis counts that section then asserts. As it stands:

```sh
has "doctor: vision ok"   "$(bash "$ROOT/resources/doctor.sh" "$D" 2>/dev/null)" "vision      ok      1 terminal · 2 on · 4 off"
```

as it should read:

```sh
has "doctor: vision ok"   "$(bash "$ROOT/resources/doctor.sh" "$D" 2>/dev/null)" "vision      ok      1 terminal · 4 on · 2 off · longest chain 3"
```

All five green with those three edits: run in scratch, `verify: 52/52 checks
pass`.

### 2 — the same sibling harness calls `doctor.sh "$D"`, not `"$B"`

*(carried forward from pass one)* Its `## dangling names` section passes the
fixture's **parent** directory where every other call passes the board. A
pre-existing bug, unconnected to `edges:`, in the same out-of-footprint file.
Pass one recorded it flipping two long-standing failures to passing; on this
machine today that harness baselined `52/52`, so the flip did not reproduce —
recorded as measured, either way not this PRD's to fix.

### 3 — the sibling's own prose still states the replaced rule

`prds/the-board-runs-itself/vision-is-first-class/prd.md:54` and
`specs/spec02.md:31` both still say depth is "over `needs:` plus `edges:`".
Another PRD's files; reported, not touched. A swept copy at
`prds/doctor-repairs-the-register-entry/probe/stub-skill/resources/doctor.sh:612`
holds the old `vision broken` wording too — it is that PRD's self-contained
stub fixture, unaffected by this change and out of footprint.

## Workflow probe-then-spec

| # | step | result |
|---|---|---|
| 1 | `read-the-contract` | pass. PRD, `specs/spec01.md`, pass one's `report.md` and the probe read; `git status --short` recorded in **both** roots (lane empty, checkout dirty on a neighbour's files) |
| 2 | `capture-the-harness-baseline` | pass. Thirteen `vision` harnesses plus `index.py check` and `doctor`, all with `PEARDE_ROOT=<lane>`, saved under a run-named scratch subdirectory |
| 3 | `attempt-the-build` | pass, rebuilt rather than continued (see above). Every change is an **edit to an existing footprint file**, so built in place, never staged under `probe/` |
| 4 | `re-run-the-harnesses` | pass. One count up (this PRD's probe), one down on a committed harness outside the footprint (left red, replacements above), one neighbour's flake |
| 5 | `write-the-specs` | second-pass form: no spec authored; the `## Fails when` table applied to the standing boxes and block, three rows fired |

No back-edge was taken.

### Edits

None. Every atomic's commands ran as written, every path resolved, and the two
`Fails when` rows that decided this run — `read-the-contract`'s lane row and
`capture-the-harness-baseline`'s `PEARDE_ROOT` paragraph — were already exact,
including the `PEARDE_ROOT`-instead-of-symlink amendment that appeared in
`read-the-contract` mid-run.

## Health floor

Nothing in the footprint is under the floor; the brief listed none. No file
grew a responsibility: `vision_axis` lost a line and gained one.

## Scores

complexity: 12
blast-radius: low
workflow: probe-then-spec
