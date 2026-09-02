# the-brief-names-the-verdict-line-collect-requires — implementer report

Verdict: DONE

Pass two on the analyst's uncommitted probe. Both specs confirmed against
their boxes: **13 of 13 ticked**, every one from a check actually run.

- `specs/spec01.md` — 7/7 — the brief names the `Verdict:` line; the rewrap's
  leftover continuation is gone.
- `specs/spec02.md` — 6/6 — two content rules in `brief.check()`, both proven
  able to fail; the `briefs` row stops overstating.

Nothing was committed. The footprint is unchanged from pass one — this pass
edited no source file, only the two spec files' boxes.

**The flip is this PRD's, shown against `HEAD` and not merely re-run.** With
the three footprint files restored from `HEAD` into a scratch copy, the probe
reads `5 ok · 10 FAIL` (exit 1); with them in place, `15 ok · 0 FAIL` (exit 0).
Each of the ten failures names a predicate these hunks satisfy.

**The orchestrator's `brief:every` reading is confirmed and the specs agree
with it.** `brief_prd` appends `blocks["every"]` for both the analyst and the
implementer role; `brief_consult` renders only `blocks["consultant"]`. The
consultant brief carries 0 `Verdict:` lines, the analyst and implementer
exactly 1 each. The line numbers in the PRD and specs have gone stale — see
Findings.

## Verify output

| check | result |
|---|---|
| `probe/verify.sh` | `15 ok · 0 FAIL`, exit 0 — run twice, identical |
| same, footprint reverted to `HEAD` | `5 ok · 10 FAIL`, exit 1 |
| `brief.py --check` | silent, exit 0 |
| `check()` on `HEAD:workers.md` | **2 problems** — both new rules fire on the pre-build file |
| `check()` on the current file | 0 problems — no false positive on any of the five blocks |
| `verdict_of` span vs `HEAD` | `verdict_of unchanged` — byte-identical |
| `git diff HEAD -- references/templates/report.md` | empty |
| `grep -c 'as you would one the PRD already carries'` | `1` |
| consultant brief `Verdict:` count | `0` |
| analyst / implementer brief `Verdict:` count | `1` / `1` |
| `python3 resources/index.py check` | silent, exit 0 |
| `bash resources/doctor.sh` | exit 0 at first measurement, 0 `broken` rows |
| `briefs` row | `ok  5 blocks in references/parts/workers.md · every placeholder named · the verdict line named` |

### The two rules proven able to fail

Defect a — the marker removed from `brief:every`:

    brief:every never names the `Verdict:` line `pearde collect` reads — a
    worker following the brief writes a report the collect refuses

Defect b — the duplicated continuation restored:

    brief:analyst repeats a line ending `…PRD already carries. Then read` — a
    rewrap that left the old continuation behind

Both name their block; defect b quotes the repeated tail. Neither fires on the
real file.

## Sweep for other copies

`grep -rn 'as you would one the PRD already carries' --include='*.md'
--include='*.py' --include='*.sh' .` — **1 hit before, 1 after**:
`references/parts/workers.md:163`, the surviving correct line. The deleted
duplicate is gone tree-wide.

Shape sweep for the claim itself — every site that instructs a verdict:

| site | state |
|---|---|
| `workers.md:171` `> exactly one verdict:` (analyst) | receives `brief:every` — covered |
| `workers.md:328` `Return **DONE**` (implementer) | receives `brief:every` — covered |
| `workers.md:85` | the corrected sentence — the one source |
| `doctor.sh:618` | the checker's comment — in footprint, correct |
| `references/templates/grammar.md:127` | **out of scope** — a sibling's untracked file; already states the rule correctly and agrees with the correction |
| `collect.py:309`, `:349` | out of scope — the tool, which the PRD forbids loosening; unchanged |
| `resources/scout/routes.md:299` | not the claim — an unrelated `## Verdict` heading |

Corrected inside the footprint: 0 further (pass one had already done both).
Named out of scope: 2. Counts add up.

## Harness baseline and re-run

23 harnesses name a footprint path. Each was run twice — once on the tree as
it stands, once on a scratch copy with only the three footprint files restored
from `HEAD` — plus a control copy with nothing reverted.

**No harness went green to red.** Every exit-code move was `1 → 0`, in the
direction of this PRD's hunks. Unchanged pairs: `brief-is-printed` 104,
`workflow-improve` 71, `workflow-seed` 68, `too-big-splits-itself` 60,
`the-loop-is-commands` 58, `vision-is-first-class` 52, `workflow-attach` 47,
`the-skill-tree-is-guarded` 41, `an-analyst-workflow…` 21,
`one-definition-of-the-board-not-two` 20, `the-harness-sweep-is-capped` 16,
`the-view-row-names-a-variable` 6.

One ok-count **dropped** — `the-doctor-completes-without-a-home`, 12 → 11 —
and it is not mine. The diff shows one `ok` became a `skip`:

    skip  the view-row harness could not be run — 8477-8479 are held
          elsewhere (: 8477); not asserted here

Exit 0 and 0 FAIL in both runs. The cause is the live `serve.py run` daemon
(pid 28740) a sibling started during this run, the same cause as doctor's
`view` row below. The rule the harness asserts did not move.

Two harnesses are red in **both** runs — pre-existing, recorded before this
pass changed anything: `upgrade-leaves-the-memo-index-stale` (the analyst's
Obsidian vault-register finding, still standing) and
`workflows-on-the-board/workflow-skill`.

The exit-1 seen in both the baseline **and the control** copy of
`resources/doctor.sh` is a copy artifact, not a regression — that is precisely
what the control copy established.

## Findings — not fixed, not filed

**1 — A sibling wrote inside this PRD's footprint file mid-run.** Three lines
were added to `references/parts/workers.md` at 78-80, *inside the
`brief:every` block this PRD edits*, after the baseline was taken (mtime moved
1788335748 → 1788336591, hunks 9 → 10):

    > Look a word in your contract you do not know up with `python3
    > resources/grammar.py show`, and put a word you needed and it does not
    > define in your report rather than inventing one.

This is the `pearde-grammar` sibling. Every check was re-run afterwards: this
PRD's hunks are intact, and the added lines trip neither new rule — which is
extra evidence for spec02's no-false-positive box. Left exactly as found. The
commit will need staging hunk by hunk in this file.

**2 — The sibling's `round` → `pass` rename and `grammar` row ride along.**
`resources/doctor.sh` hunks moved 13 → 15 and `references/parts/doctor.md`
carries three; doctor's `questions` row now reads `1 PRD carries a pass`, and
a new `grammar ok 170 terms` row appears. Both are the sibling's, both `ok`,
left untouched by design.

**3 — Line numbers in the PRD and both specs have gone stale.** The mechanism
is exactly as written; only the citations moved, as siblings grew the files:

| cited | actual now |
|---|---|
| `brief.py:340` (analyst + implementer get `every`) | `:369` |
| `brief.py:361` (consultant skips it) | `:374` / `:390` |
| `collect.py:258` (`verdict_of`) | `:309` |
| `collect.py:299` (the raise) | `:349` |

spec01's box 4 names `brief.py:361` in its text. The box is closed on the
mechanism, which holds; the number is what drifted.

**4 — The analyst's docstring finding is misattributed, and there is nothing
to fix.** The analyst report says `collect.py:258` "should not say 'bold'
without qualification". The docstring makes **no** decoration claim at all — it
only documents the 40-line window. The overstatement ("generous about
decoration — bold, headings") lives in the **PRD body**, which is the contract
and not editable here. It is already corrected where it matters: the brief now
names the safe shape. No edit to `collect.py` is warranted. The analyst's
underlying measurement stands — `**Verdict:** X`, `*Verdict:* X`, `- Verdict:
X` and `> Verdict: X` are all read as no verdict, and the probe pins all four.

**5 — `knowledge` row flipped `ok` → `broken` mid-run, outside the
footprint.** `graph.json is behind the files: 260902-14d9, 260902-4b7c,
cargo-vendor-is-order-independent-of-the-source-replacement-`. All three notes
under `.pearde/wiki/` were written after this run's baseline. A sibling's
`knowledge.py` write; nothing in this footprint closes it.

**6 — `view` row flipped `off` → `broken` mid-run.** "the service is up but
this board is not registered". A `serve.py run` daemon (pid 28740) came up
during the run. Not restarted or stopped here — the coordinator owns the
service.

**7 — A harness the analyst recorded red is now green, and not by this PRD.**
`workflows-on-the-board/workflow-improve/probe/verify.sh` was reported failing
on a missing "any of the three, plus" row. It now reads exit 0, 71 ok — and
identically so in the reverted-baseline copy, so a sibling closed it between
the analyst's run and this one. Not this PRD's flip.

**8 — Cosmetic, in this PRD's own probe.** The summary prints `15 ok` while 24
`ok` lines appear: the G4 Python sub-block prints its own lines and rolls up
into a single bash-level assertion, so `PASS` undercounts what is displayed.
Honest, but the two numbers invite misreading — the analyst report's "22
assertions" is the same confusion. Not repaired; the probe is pass-one code.

## Workflow correct-a-documented-claim

| # | step | outcome |
|---|---|---|
| 1 | `read-the-contract` | done — PRD, both specs, analyst report read; `git status --short` recorded before the first edit. It listed **more** paths than the brief named (`SKILL.md`, `index.md`, `references/files.md`, `references/parts/handles.md`) and HEAD had moved `bc1c589` → `5f3270a`. Recorded per the step's own fails-when row; the tree is live |
| 2 | `capture-the-harness-baseline` | done — 23 footprint harnesses listed with `find`, each run in a reverted copy and a control copy; mtimes and hunk counts recorded for all nine dirty files. Two pre-existing reds written down before any edit |
| 3 | `edit-inside-the-footprint` | done — **no source file edited this pass**; pass one's hunks confirmed intact after a sibling wrote into the same file. Only the two spec files' boxes changed |
| 4 | `sweep-for-other-copies` | done — 1 hit before, 1 after; 2 sites named out of scope with line numbers |
| 5 | `re-run-the-harnesses` | done — every count ≥ baseline but one, which is explained and attributed; the flip shown against `HEAD` rather than merely re-run |
| 6 | `run-the-repo-gate` | done — `index.py check` silent exit 0; `doctor` exit 0 with 0 `broken` rows at first measurement, two sibling-caused rows red later, both attributed |

No back-edge was taken.

### Edits

Two failures the atomics caused, with replacement text.

**`capture-the-harness-baseline` — the reverted-copy recipe corrupts the
baseline when a sibling's hunks share a file with yours.** The atomic says to
"restore your own footprint files from `HEAD` there — that reverts your build
and keeps every neighbour's". That is only true when no neighbour has hunks in
*your* files. Here `resources/doctor.sh` held this PRD's one hunk **and** a
sibling's rename plus a new `grammar` row; restoring it from `HEAD` reverted
the sibling's work too, leaving a copy whose `doctor.sh` knows nothing of the
untracked `resources/grammar.py` still present. Several doctor-reading
harnesses read artificially red in that copy. Replacement for that bullet:

> restore your own footprint files from `HEAD` there — that reverts your build
> and keeps every neighbour's, **but only where no neighbour has hunks in a
> file of yours. Check first: `git diff -U0 -- <footprint path>` and read the
> hunks. Where a file is shared, restoring it from `HEAD` reverts their work
> as well and the copy is not a baseline for anything that reads it — say so,
> and fall back to comparing the two copies row by row for the rows your own
> hunks touch, which is the comparison the control copy makes honest.**

**`edit-inside-the-footprint` — `## Fails when` has no row for a sibling
writing *inside* your footprint file.** It lists a sibling committing your
lines and a sibling dirtying a path *outside* your footprint, but not the case
met here: a live session adding its own hunks to a file you hold, after your
baseline, while you are measuring it. Row to add:

| seen | means | do |
|------|-------|----|
| a footprint file's mtime or hunk count moves during the run and none of the new hunks are yours | a sibling is writing inside your footprint, not merely beside it — one writer per file has been broken | `git diff -U0 -- <path>` and read every hunk; confirm your own are intact by re-running each check that reads the file, quote the added lines in the report, and leave them. Never revert them and never fold them into your own hunks — the commit is staged hunk by hunk |
