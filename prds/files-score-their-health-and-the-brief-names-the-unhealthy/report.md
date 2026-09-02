# Report — files-score-their-health-and-the-brief-names-the-unhealthy

Verdict: DONE

Implementer pass, `probe-then-spec`, as engineer, worker `impl-health`. This is
the route's **second** pass: the analyst probed, specced and left the build
standing (committed). Per the route's own step-3 row for that case, steps 3 and
5 were not entered as build-and-spec work — no code was written and no spec was
authored. What this pass did is run every check, tick every box against quoted
output, and repair three verify blocks that could not have failed.

All 16 acceptance boxes across `spec01`, `spec02`, `spec03` are `[x]`, none
open. `specced --check` → `ok · complexity 14`.

## Per-spec box status

| spec | boxes | all ticked | block exit under `pipefail` |
|---|---|---|---|
| `spec01` — every tracked file carries a score | 6/6 | yes | 0 · `spec01 failures: 0` |
| `spec02` — the brief names the unhealthy files | 4/4 | yes | 0 · `spec02 failures: 0` |
| `spec03` — health is a registered part | 6/6 | yes | 0 · `spec03 failures: 0` |

## Verify output

- Probe: `bash probe/verify.sh` → **`37 checks · 37 pass · 0 fail`**, exit 0.
  Run twice, unchanged, matching the analyst's published count.
- `health.py score` → `153 scored · 153 on the ranking · 18 skipped · 5 under
  40 · graph 954b906` (151 at the analyst pass, 152 then 153 during this one —
  see Findings; `5 under 40` never moved).
- `health.py list --under 40` → `4 resources/board/view.css`, `19
  resources/board/plan.py`, `28 resources/board/serve.py`, `31
  resources/board/collect.py`, `39 resources/board/view.js`. The three files
  the contract's first box names are all under the floor.
- `health.py check` → exit 0, silent.
- Gates: `memos.py check` 0, `grammar.py check` 0, `brief.py --check` 0, all
  silent. `index.py check` was **0 and silent at baseline** and is now 1 — see
  Findings, it is a sibling's file.
- `doctor.sh` rows in footprint: `health ok 153 files · 5 under 40` ·
  `grammar ok 177 terms` · `skills ok 18 well-formed` (lists `pearde-health`) ·
  `briefs ok 5 blocks in references/parts/workers.md · every placeholder named
  · the verdict line named`.
- Registration spot-checks all on their stated lines: `resources/pearde.py:85`,
  `references/settings.md:43-44`, `resources/board/init.py:85`,
  `references/templates/grammar.md:258,261,262,289,290`,
  `references/parts/workers.md:118,352`, `resources/board/brief.py:246,383`.
  `git check-ignore -v .pearde/health/ranking.md` → `.gitignore:16:.pearde/`.

## Baseline, taken before the first write

`git status --short` at 14:43, HEAD `954b906`: 8 paths modified and 1
untracked, **all of them the in-flight machine PRD's**; every one of this
PRD's 14 footprint paths clean and committed. `find .pearde/prds -name
verify.sh` → 58. Gates all exit 0 and silent, including `index.py check`.
`doctor.sh` exit 1 with `knowledge broken`, recorded as failing **before the
first edit** and outside this footprint. **Correction:** the tree carries
**two** broken doctor rows now, not one — `index broken 1 problem` joined it
mid-pass off a sibling's `lanes.py`. Both are outside this footprint and
neither flips a box, but the earlier "one broken row" count was wrong.

No file outside this PRD's own directory was written by this pass. `git status
--short` at the end is byte-identical to the baseline for every path this pass
touched; the paths that changed under it are named in Findings and are a live
sibling's.

## Verify blocks repaired — three blocks that could not fail

This is the pass's only real work, and it is the route's own step-5
`Fails when` shapes, found by running each block the way `collect` will
(`awk` the fence out, `bash -c 'set -o pipefail; …'`).

**`spec02` and `spec03` exited 1 on a green tree.** Both ended on
`bash resources/doctor.sh 2>&1 | grep -E '…'`. `doctor.sh` exits 1 on the
`knowledge` row — another PRD's — and under `pipefail` that exit became the
block's. `collect` would have refused both with `specNN exit 1 — nothing
written`, making this unit's pass conditional on every other PRD on the board.
Repaired the documented way: `out=$(bash resources/doctor.sh 2>&1 || true)`,
guarded with `[ -n "$out" ]`, then grep the rows. The rows stay visible and
stop deciding the exit.

**`spec01`'s `echo` shape — this diagnosis was wrong, and is corrected here.**
The first version of this report said every assertion ending
`; echo "… exit=$?"` could not fail because an `echo` always exits 0. That
holds only without `-e`. `resources/board/collect.py:1242` runs each block as
`bash -e -o pipefail`, and under `-e` a failing `cmd` in `cmd; echo "…"`
aborts the script at `cmd` before the `echo` runs. So the original `spec01`
and `spec03` gates **were** able to fail under the real runner. The counter
rewrite is still the better shape — it reports *how many* checks failed and
which, instead of stopping at the first — but it did not close a hole, and the
claim that it did was incorrect. The `pipefail` diagnosis for `spec02` and
`spec03` below is unaffected and stands: under `-e` a failing `doctor.sh` in a
pipeline aborts the block even more surely than it did without it.

**All three rewritten to the counter shape**: each check is
`<cmd> || N=$((N+1))`, and the block ends bare on `echo "specNN failures: $N"`
then `[ "$N" = 0 ]`.

**`spec03`'s `index.py check` was gating on a file outside the footprint.**
The route's rule is that no command's exit may be decided by a file outside
the footprint, and `index.py check` reads the whole checkout. It is now
captured, printed in full, and fails the block **only** on output lines
matching this spec's own footprint paths. That change is what keeps the block
honest under the sibling landing described below, rather than what hides it —
the failing line is still printed on every run.

**`spec01`'s block no longer asserts a literal file total.** It asserted
`^151 scored · 151 on the ranking`; a live checkout moves that number for
reasons that have nothing to do with this unit (it moved to 152 mid-pass). It
now asserts the summary's *shape* and the contract's actual claim, that
`plan.py`, `collect.py` and `view.js` are each on `list --under 40`. A floor is
honest; an equality on a moving total is a wall.

### Negative controls — each block proved able to fail

Each footprint file was copied to a scratch dir **outside the repo**, mutated,
the block re-run, the file restored by `cp` and the restore proved with `cmp`.

| spec | mutation | block on mutation | after restore | `cmp` |
|---|---|---|---|---|
| `spec01` | `resources/health.py`: summary wording ` on the ranking · ` → `  on the RANKING · ` | exit 1 · `spec01 failures: 1` | exit 0 · `failures: 0` | clean |
| `spec02` | `resources/board/brief.py`: `def health_of(` → `def healthXof(` | exit 1 · `spec02 failures: 2` | exit 0 · `failures: 0` | clean |
| `spec03` | `resources/board/init.py`: `"health/"` → `"heXlth/"` | exit 1 · `spec03 failures: 1` | exit 0 · `failures: 0` | clean |

## No flip is claimed

Every red-to-green on this tree was earned by the pass that built it. This
pass claims exactly one state change it caused, and it is not a code flip:
`doctor`'s `health` row read `ok 151 files · 5 under 40 · stale, pearde health
score refreshes it` at baseline and reads `ok 152 files · 5 under 40` after,
because this pass ran `health score` — which `spec01`'s own block calls. A
`diff` of `doctor.sh` output before and after, with the `statusline` row
excluded, is that one line and nothing else.

## Findings

Carried forward from the analyst pass by name, with this pass's status:

- **The contract's stated default weights are stale.** *(analyst, standing)*
  The PRD body says `lines=20 branching=25 longest=20 fan_out=10 fan_in=10
  links=15`; the code and `references/settings.md:44` both say `lines=25
  branching=30 longest=20 fan_out=5 fan_in=10 links=10`. Re-confirmed on this
  pass. Not fixed — the contract paragraph is not the implementer's to edit.
- **The earlier report's verdict word was not one any block names.**
  *(analyst, closed)* That was the analyst pass's reason to exist; this
  report's verdict line is one word an implementer block names.
- **Three decisions the earlier report called memo-worthy were never
  written.** *(analyst, standing)* The `links` axis reading, the size-heavy
  weights, and the knobs being flat rather than nested. Still unwritten — no
  memo on this board mentions health. Outside this contract, so still a
  finding.
- **`doctor` has one broken row outside this footprint.** *(analyst, standing)*
  `knowledge broken — the research layer does not check out`. Recorded red
  **before the first edit** of this pass and red after; unchanged. Its exit
  code is what broke two of the three verify blocks, which is now repaired.
- **Acceptance box one is ambiguously worded.** *(analyst, standing)* "the
  bottom of the ranking" against a worst-first file. `spec01` restates it as
  "all under the floor" and the repaired block reads `list --under 40`, which
  is order-free.
- **Three shared files deliberately out of the footprint.** *(analyst,
  standing)* `SKILL.md`, `index.md`, `references/files.md` — the machine PRD's
  working set. Confirmed on this pass: all three are still dirty in that
  session's hands, and claiming them would have blocked it.
- **Knowledge gap, auto-enqueued.** *(analyst, standing)* Nothing was learned
  outside this repo on this pass either, so there is nothing to `remember`
  back.
- **`probe-then-spec` fits a case its `## Use when` does not yet name.**
  *(analyst, extended)* See `## Workflow probe-then-spec` below — this pass hit
  the same gap from the implementer's side.

New on this pass:

- **A live sibling session is writing `resources/board/brief.py`, which is in
  this PRD's `spec02` footprint.** At baseline `brief.py` was clean; it is now
  ` M` with 11 insertions / 3 deletions — an `import lanes as laneslib` and a
  rewrite of `repo_of()` to return a worker's lane worktree. mtime 14:48:06,
  after the 14:43 baseline. **None of it is this pass's**: `cmp` against the
  copy taken before the negative control is clean, and `health_of` (lines
  246-270) is untouched. `resources/board/plan.py` (14:47:43) and
  `resources/board/transitions.py` moved the same way. This is a real
  footprint overlap between this PRD and the in-flight lanes/machine work —
  reported, not fixed, and not mine to resolve. `spec02`'s checks were re-run
  after the sibling's change and are green: `brief.py --check` exit 0, probe
  `J1 J2 J3` all `ok`, `doctor`'s `briefs` row green.
- **`index.py check` went from green to red mid-pass on a file outside this
  footprint.** `resources/board/lanes.py is on disk with no row in
  references/files.md` — the sibling's new file, written at 14:45:40, two
  minutes after this pass's baseline recorded `index ok 149 files · 36
  keywords · every anchor resolves`. `references/files.md` is one of the three
  files `spec03` deliberately left out of the footprint. Per the route's row
  for a harness that reads the whole checkout, the harness is left alone, the
  line is quoted, and the repair is owed to that harness's own PRD. Same shape
  as `.pearde/memos/a-harness-that-reads-the-whole-checkout-is-not-a-harness.md`.
- **The file total in the health summary is not a stable number to assert.**
  It moved 151 → 152 within four minutes of a normal working board, purely
  from a neighbour adding a file. Any future spec or harness that pins it will
  go red on somebody else's landing. Recorded here because the fix is
  generalisable: assert the summary's shape and the named files, never the
  count.
- **`graph.json` was rebuilt between the analyst pass and this one.**
  `built_at_commit` moved `f986510` → `954b906` (mtime 14:28). The three graph
  axes and every score are unchanged; only the summary's `graph <hash>` suffix
  differs from what the analyst quoted. Noted so the difference is not read as
  a regression.

No health floor work was owed: the brief's `<health>` block read `none under
the floor`, and `health list --under 40` confirms none of this PRD's 14
footprint files is under 40 — the five that are all belong to other PRDs.

No word in the contract was undefined; `grammar.py check` is clean on 177
terms and `health`, `unhealthy`, `floor` and `complexity` all carry rows.

## Workflow probe-then-spec

| # | step | outcome |
|---|---|---|
| 1 | `read-the-contract` | pass. `prd.md`, all three specs, the analyst's `report.md` and the probe read. All 14 `footprint:` paths exist and were opened. `git status --short` recorded before the first write. Board root is the repo's own `.pearde`, its own git toplevel. |
| 2 | `capture-the-harness-baseline` | pass. 58 board harnesses located by `find`, not a glob. The four gates and `doctor.sh` baselined with exits and full output saved under a run-specific scratch subdirectory. `knowledge broken` recorded as failing **before the first edit**. |
| 3 | `attempt-the-build` | **not entered as build work** — the route's own `Fails when` row for a second pass on a PRD whose specs and build already stand. Steps 1, 2 and 4 run; no code written, no flip claimed. |
| 4 | `re-run-the-harnesses` | pass, with two findings. The probe held at `37 checks · 37 pass · 0 fail` across two runs. `index.py check` dropped green → red on a sibling's file; quoted, attributed by mtime and `git status`, harness left alone. No count in this footprint moved. |
| 5 | `write-the-specs` | **not entered as authoring work** — the specs stood. Its `Fails when` table was still applied to the existing blocks and caught three defects, repaired above; its rule that a previous pass's `## Findings` are carried forward by name was applied to this report. |

### Edits

Two edits to the route's own text, both from shapes this pass hit that the
files do not yet name. Neither was made by me — the route's files are not the
worker's to edit.

**1 — `probe-then-spec`, `## Use when`.** The route's `Fails when` table in
step 3 already handles a second pass on a PRD whose specs and build stand, but
`## Use when` still opens on "A PRD is `open` and needs specs before anyone can
be sent at it", which reads as excluding the case. The analyst hit this from
one side and this pass hit it from the other. Replacement text, as a bullet
after "Not when the specs already exist":

> - Also when the specs **do** exist and an implementer is dispatched on this
>   same route — the second pass. Steps 3 and 5 are then not build-and-spec
>   work: step 3 re-measures and step 5 applies its `Fails when` table to the
>   blocks that already stand, without authoring a spec. Step 3's `Fails when`
>   table says so; this list should not read as excluding the case that table
>   handles.

**2 — step 5, `Do`, item 4.** The step tells the author to keep a block's exit
off files outside the footprint, and its `Fails when` table names the
`pipefail` shape and the `&&`/`echo` shapes separately. What it never says is
that a block should be *run the way collect runs it* before the spec is
considered written — which is the single action that found all three defects
here. Replacement text, appended to item 4:

> Before the spec is done, run the block the way `collect` will and confirm the
> exit. Awk the fenced block out of the spec and run it under
> `bash -c "set -o pipefail; …"`: it must exit 0 on a green tree, and must exit
> **non-zero** with one footprint file mutated. A block that has only ever been
> run line by line has never been tested; a block that has never been run
> against a broken tree cannot fail.

## Second round — review defects, fixed

A reviewing session found two defects in the first DONE. Both were real, both
are fixed, and both were spec-text repairs of the same kind as the first round.
No product code was written.

### 1 — `spec03` box 6 asserted more than its block tested

The box read "`index.py check`, `memos.py check`, `grammar.py check` and
`brief.py --check` all exit 0", but the repaired block had stopped requiring
`index.py check` to exit 0 — it only required that its output name no path in
the footprint. The box was not updated when its test was narrowed, and it
quoted `index ok 149 files · 36 keywords · every anchor resolves`, a **14:43
baseline capture presented as current evidence** while `index.py check` exits 1
today. A box may not quote a stale green.

The narrowing itself is correct and is kept: `index.py check` reads the whole
checkout, and the route forbids a block whose exit is decided by a file outside
its footprint. So the box is rewritten to state exactly what the block tests,
its exit is named as deliberately unasserted with the reason, and the proof is
replaced with today's real output including `index.py check` **exit 1** and its
failing line.

The filter's blind spots, measured against the reviewer's four inputs:

| input | `$FP` | crash guard |
|---|---|---|
| `resources/health.py is on disk with no row in references/files.md` | **trips** | — |
| `references/files.md is on disk with no row in index.md` | ignored | — |
| `SKILL.md is on disk with no row in references/files.md` | ignored | — |
| `resources/board/lanes.py is on disk with no row in references/files.md` | ignored | — |
| `Traceback (most recent call last):` | ignored | **trips** |

The two ignored registration cases are the three shared files `spec03`
deliberately leaves out of its footprint (`SKILL.md`, `index.md`,
`references/files.md`) — the in-flight machine PRD's working set. Asserting
them here would couple this unit's colour to that PRD, which is the coupling
the route forbids; the box now says so instead of implying coverage. The
traceback case was a genuine hole — `index.py` could have died and the block
would have read that as a pass — and it is now closed by an explicit crash
guard on both the exit code and a `Traceback` line.

### 2 — `git check-ignore` could not fail for the reason its box implied

Box 4 offered `git check-ignore -v .pearde/health/ranking.md` →
`.gitignore:16:.pearde/` as proof that `init.py` registers `health/`. It is not
proof of that: line 16 ignores the whole `.pearde/` directory, so the check
passes whatever `init.py` contains. **Measured:** with `"health/"` mutated to
`"heXlth/"` in `init.py`, `git check-ignore -q` still exits **0**. It tested
this repo's own `.gitignore`, never the registration — exactly the shape of the
memo this report cites, surviving a pass whose stated purpose was removing that
shape.

Removed from the block as redundant, and the box now cites the two things that
do test it: `grep -q '"health/"' resources/board/init.py`, and probe `A10`,
which builds a board with `init.py` under `mktemp -d` and reads the
`.gitignore` it actually wrote (`probe/verify.sh:69`).

### A third defect, found while fixing the first two

The `-e` correction above has a consequence I had to test for rather than
reason about. The line I first wrote to capture the index exit was
`idx=$(python3 resources/index.py check 2>&1); irc=$?`. Under `bash -e`, an
assignment from a command substitution carries the substitution's exit status,
so that line **aborts the whole block** whenever `index.py check` is red —
which is exactly the case it was written to survive. Confirmed directly:
`bash -e -o pipefail -c 'x=$(… exit 1); echo REACHED'` prints nothing, exit 1.
Rewritten `-e`-safe as `idx=$(…) && irc=0 || irc=$?`, which reaches the next
line, and all three blocks were then re-run under the runner's real flags.

**All three blocks now verified under `bash -e -o pipefail`, not just
`pipefail`** — the flags `collect.py:1242` actually uses:
`spec01 exit=0`, `spec02 exit=0`, `spec03 exit=0`. The first round tested only
`set -o pipefail`, which is why the `-e` trap above got written at all.

### The first round's negative controls were weak — stated plainly

The reviewer is right and the first report overclaimed. Those three controls
**showed the counter is wired, not that the block detects a regression.** Each
mutation was aimed at the single grep most obviously sensitive to it — summary
wording at `spec01`'s shape-regex, `def health_of(` at `spec02`'s grep,
`"health/"` at `spec03`'s grep. **None of them mutated behaviour**: no score,
no weight, no axis and no fallback was broken, so none of them tested whether
the block would catch a real regression in what `health.py` computes.

Separately, "these blocks could not fail" is **unproven, not proven**: the
pre-rewrite spec text exists nowhere on disk — `.pearde/` is gitignored and the
claim snapshot lists names, not content — so no independent reader can confirm
what the blocks looked like before. That claim rests on this report alone, and
it should be read that way. (It is also the claim the `-e` correction above
partly retracts.)

One genuine behavioural control was run this round, to answer that:

| mutation | effect | block |
|---|---|---|
| `resources/health.py:681` `s = max(1, min(100, round(100 * (1 - bad))))` → `… (1 - 0.0)`, so every file scores 100 | `score` summary goes `5 under 40` → **`0 under 40`**; no file can be unhealthy | `spec01` **exit 1 · `spec01 failures: 4`** |
| restored by `cp` from a scratch dir outside the repo | `5 under 40` returns | `spec01` exit 0 · `failures: 0`, `cmp` clean |

That is a break in what the tool computes, not in a string a grep reads, and
`spec01` caught it on four separate checks. `spec02` and `spec03` have had no
equivalent behavioural control and are still only wiring-proven — said here
rather than left implied.

### Not touched, on the reviewer's instruction

`resources/board/brief.py` — the discrepancy this report records at 14:51 was
accurate, and the reviewer reverted that file at 14:55 to keep a sibling's
uncommitted lanes probe out of this commit. `probe/verify.sh` — honest, and
green at 37/37 on an independent run.

### Standing after this round

All 16 boxes `[x]`, none open. `specced --check` → `ok · complexity 14`.
Every footprint file clean and committed; the dirty paths under `references/`
and `resources/board/` are the machine and lanes PRDs'. `health.py score` →
`153 scored · … · 5 under 40`. Two broken `doctor` rows, `index` and
`knowledge`, both outside this footprint.
