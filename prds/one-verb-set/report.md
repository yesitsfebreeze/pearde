Verdict: DONE

## Summary

Second pass of `probe-then-spec` on this PRD: the specs and the build were
already in the lane from the analyst's pass. Nothing needed building. Every
one of spec01's five acceptance boxes was run against
`.pearde/.lanes/one-verb-set` this session, output quoted below, and the
spec's whole `## Verify and Proof` block exits 0 both as a file and the way
`collect` runs it. No file was edited this pass — lane `git status --short`
is byte-for-byte what it was before my first command.

Correction, after `collect` refused this report once: the acceptance boxes
were first ticked here in the report and left `- [ ]` in
`specs/spec01.md`, which is the file `collect` reads. They are now ticked
in the spec too — `git diff --stat -- prds/one-verb-set/specs/spec01.md` is
`5 insertions(+), 5 deletions(-)`, the five markers and nothing else — and
against the same runs quoted below, with nothing re-run to earn a tick.
The brief's rule is to tick a box in the spec as it closes rather than in a
batch at the end; this pass batched it, and the refusal was the cost.

## Spec01 — box status

- [x] **`scout.sh` with no argument prints one row per verb and exits 0.**
  `bash resources/scout/scout.sh` → exit 0, seven rows:

  ```
  VERB               CONTRACT                                             LANDS IN
  sweep              snapshot every bucket's star counts                  snapshots/<date>.tsv
  delta [days]       what gained the most stars since ~N days ago         snapshots/ (diffed, no new write)
  trending [window]  GitHub's own trending feed, a discovery channel      none kept — pipe to a file to save it
  tool <query>       one-off dependency ranking: stars + what stars hide  none kept — pipe to a file to save it
  find <id> [query]  call one ranking page by id (was route.sh)           routes.md defines it; a settled pick goes in findings.md
  reading            the curated, mechanism-mapped reading list           reading-list.md
  quality            the passive quality gates and their templates        templates/
  ```

- [x] **`resources/scout/check.sh` exits 0.** `bash resources/scout/check.sh`
  → exit 0, silent. Proven able to fail rather than assumed: copied
  `README.md` to scratch outside the repo, changed the Commands table's
  `reading` row to `readng`, re-ran:

  ```
  scout/check: row 6 differs
    scout.sh:   reading	the curated, mechanism-mapped reading list	reading-list.md
    README.md:  readng	the curated, mechanism-mapped reading list	reading-list.md
  check.sh exit=1
  ```

  Restored from the scratch copy, `cmp` clean, re-run exit 0.

- [x] **`toolscout.sh` and `scout.sh tool` are byte-identical.** Run with the
  PRD's own `Done when` query rather than only the block's no-argument case:
  `toolscout.sh 'topic:tui language:rust'` against `scout.sh tool 'topic:tui
  language:rust'` → `exit a=0 b=0`, `stdout identical (2223 bytes)`, `stderr
  identical`. Last line of both:
  `record: none kept — pipe to a file to save this ranking`.

- [x] **`scout.sh delta` over 40 changed rows exits 0 and names the
  snapshots it diffed.** Snapshots backed up, replaced with two 50-row
  fixtures, restored after:

  ```
  delta exit=0  rows=42
  record: …/snapshots/2020-01-01.tsv vs …/snapshots/2020-01-02.tsv — diffed in place, nothing new written to snapshots/
  ```

  `git status --short -- resources/scout/snapshots` empty afterwards.

- [x] **`reading` names `reading-list.md`; `quality` names `templates/`.**

  ```
  record: …/resources/scout/reading-list.md
  record: …/resources/scout/templates — copy these into a tree to wire the gates
  ```

Beyond the boxes: all seven verbs emit a `record:` line (`grep -n 'record:'
resources/scout/scout.sh` → 7 sites, one per verb), and `scout.sh find list`
and `route.sh list` both report 45 rows, so the `find` verb forwards without
holding a list of its own.

## Verify blocks and the repo gate

- Spec01's block as a file: exit 0, prints `ok`.
- Spec01's block the way `collect` runs it —
  `bash -e -o pipefail -c "$(awk '/^```sh/{f=1;next} /^```/{f=0} f' specs/spec01.md)"`
  → exit 0, prints `ok`. It reads no board-wide gate, so its exit is its own
  footprint's.
- `.pearde/prds/one-verb-set/probe/verify.sh` with `LANE=<lane>`: `boxes 8/8`,
  exit 0, at baseline and again at the re-run.
- Repo gate, checkout root: `python3 resources/index.py check` → exit 0 at
  baseline and exit 0 at the end. `bash resources/doctor.sh .pearde` →
  `index ok · 191 files · every anchor resolves`; the `broken` rows
  (`vault`, `origin`, `memos`, `knowledge`, `questions`) were broken before
  the first command and name no scout path.
- Repo gate, lane root: `index.py check` → exit 1 on three lines, identical
  at baseline and at the end, none in my footprint's meaning:
  `resources/common.py is on disk with no row in references/files.md`,
  `references/files.md lists @resources/board/hotreload-test.js — not on disk`,
  `@@view names @resources/board/hotreload-test.js — not on disk`. All three
  are pre-existing at the lane's own `HEAD` (`git show HEAD:references/files.md`
  has the hotreload row and no common.py row) and all three close on the merge
  — the checkout already carries both hunks.

## Harness baseline and re-run

Every harness that greps a footprint path, run with `PEARDE_ROOT=<lane>` (and
`LANE=<lane>`) both times, same command line, same order:

| harness | baseline | re-run |
|---|---|---|
| `one-verb-set/probe` | `boxes 8/8`, exit 0 | `boxes 8/8`, exit 0 |
| `a-check-for-the-reading-list/probe` | exit 2, `ok    active row left alone` | same |
| `the-round-runs-in-a-window-that-ends/probe` | `26 checks · 25 pass · 1 fail` | same |
| `workflows-on-the-board/workflow-skill/probe` | `55 checks · 46 pass · 9 fail` | same |
| `resources-are-organised-by-responsibility/probe` | `probe: 11 passed, 9 failed` | same |
| `…/the-largest-module-is-cut-by-responsibility/probe` | killed (exit 143), no count | `46 checks · 45 pass · 1 fail` (`FAIL C plan.py example writes a board`) |
| `…/skills-and-scout-docs-are-rewritten-dense/probe` | `boxes 9/14` | `boxes 9/14` |
| `the-board-runs-itself/an-example-board/probe` | `37 checks · 36 pass · 1 fail · 1 skipped` | same |

No count moved. The one row with no baseline is the largest-module probe,
whose baseline run was killed by the sweep and which completed on its own at
45/46 — recorded as new, compared to nothing. Every pre-existing failure above
was failing before the first edit.

Lane `git status --short` identical at both ends —
`M references/files.md`, `M resources/scout/README.md`, `M
resources/scout/scout.sh`, `M resources/scout/toolscout.sh`, `??
resources/scout/check.sh` — so nothing this session wrote survives outside
the footprint. The checkout's dirty list grew by `references/parts/doctor.md`,
`index.md`, `resources/doctor.sh`, `resources/board/serve.py` mid-run; a live
sibling, none of them mine.

## Findings

### 1 — the collision on `resources/scout/README.md` (carried forward)

The analyst's pass reported it and it still stands, sharpened. The sibling PRD
`every-document-is-written-in-the-writer-s-prose/skills-and-scout-docs-are-rewritten-dense`
holds a committed harness whose contract requires `resources/scout/README.md`
to keep the exact table-row count of `9889e78` and to shrink in word count —
which this PRD's `Done when` forbids, because it adds a Commands table to that
same README. Pointed at this lane the harness fails five boxes: `spec01.2`,
`spec01.5`, `spec02.4` (README row count), `spec02.5` (`index.py` output),
`spec02.6` (word count). Two facts this pass adds: the count is `boxes 9/14`
at baseline **and** at the re-run, so nothing moved during my session; and the
harness's own default lane
(`…/pearde/.lanes/every-document-is-written-in-the-writer-s-prose-skills-and-scout-docs-are-rewritten-dense`)
no longer exists, so `bash verify.sh` with no `LANE` exits 2 at its `cd` and
the harness has no measurable baseline of its own at all. `spec01.2` and
`spec01.5` read `references/skills/*.md`, which this footprint never touches —
those two are its missing lane, not this build. The sequencing decision the
earlier pass named is unchanged and is still not resolvable from inside this
footprint: land this PRD first and let the densifying PRD densify the merged
README including the new table, or except the table from its row-count check.

### 2 — `lane/one-verb-set` will not merge cleanly, for a reason outside this PRD

`git merge-tree --write-tree --name-only HEAD lane/one-verb-set` conflicts on
`references/files.md`. The conflict is entirely sibling-vs-sibling: `main` adds
manifest rows for `@resources/board/quiet.py` and `@resources/spend.py`, the
lane tip adds a row for `@resources/claims.py`, and the three insertions land
within eight lines of each other. Nothing of scout is in it — my rows are at
line ~245, in the `@@scout` table.

This build's own hunk was proved to merge before the merge rather than
discovered in `collect`: cloned the checkout to scratch, committed the
checkout's uncommitted `references/files.md` there as the neighbour's copy,
`git apply --3way` of the lane's `references/files.md` diff →
`Applied patch to 'references/files.md' cleanly.`, exit 0.

The lane also carries three commits `main` does not have — `1be5d2b`,
`e861cca`, `56f7ce5` — none of them this PRD's, all inherited from the
checkout's HEAD at cut time. `resources/common.py` from `1be5d2b` is already
on `main` by another path; `resources/claims.py` is not on `main` at all.
Reported, not fixed: `attempt-the-build`'s lane row says to rebase when a
conflicting file is inside the footprint, and `references/files.md` is — but
the conflicting *hunks* belong to two other PRDs and a rebase would replay
three foreign commits onto `main`. The board's own ruling is that a conflicted
lane is reported, not stranded, so the orchestrator owns this one.

### 3 — `doctor.sh --harnesses` does not complete on this board

`bash resources/doctor.sh --harnesses .pearde` exits **144** with the report
truncated after the `purge` row — the `harnesses` and `jstests` rows never
print — and ends on:

```
resources/doctor.sh: line 1017: 42418 Terminated: 15          sleep 0.1
```

Line 950 is the sweep's concurrency gate,
`while [ "$(jobs -r … | grep -c .)" -ge "$HCAP" ]; do sleep 0.1; done`, and
something inside the 98-harness sweep SIGTERMs it. Reproduced twice, with
`PEARDE_ROOT=<lane>` set and unset. `resources/doctor.sh` is uncommitted and
modified in the checkout by a live sibling adding the `purge` row immediately
above the harness block, so this may be that session's in-flight state rather
than a standing defect — either way it is outside this footprint and is why
the baseline was taken by invoking the eight footprint harnesses directly.

## Health floor

The brief lists no file in this footprint under the floor, and none was
edited this pass, so nothing moved and nothing needed to.

## Workflow probe-then-spec

| # | step | outcome |
|---|---|---|
| 1 | `read-the-contract` | done. `prd.md` read with no `## Answers`/`## Questions`/`## Failure`; `specs/spec01.md` read whole; the previous pass's `report.md` read and its finding carried forward. `git status --short` recorded in **both** roots before the first command. All five `footprint:` paths exist in the lane; none of the four `resources/scout/*` paths is modified in the checkout, so nothing had to be carried in. The PRD's cited source `docs/content/docs/improvements/scout-one-verb.mdx` is absent from the working tree exactly as the body warns; the body itself carries the argument, so nothing dangled. |
| 2 | `capture-the-harness-baseline` | done, with a fallback. `find .pearde/prds -name verify.sh` → 96 at baseline (98 by doctor's later count); 8 grep a footprint path; 6 of 96 lack `PEARDE_ROOT`, two of them in my set (`a-check-for-the-reading-list`, `skills-and-scout-docs-are-rewritten-dense` — both take `LANE` instead, and both were given it). The atomic's own command for a lane, `PEARDE_ROOT=<lane> bash resources/doctor.sh --harnesses <board>`, does not complete here (Finding 3), so the eight were invoked directly. Repo gate recorded in both roots. |
| 3 | `attempt-the-build` | entered as the route's **second** pass, per the atomic's first `Fails when` row. Spec01's footprint is not clean — all five paths are modified or added in the lane and the behaviour is in the files — so this pass built nothing and re-measured instead. Steps 1, 2 and 4 of the atomic ran; step 3 was correctly not entered. No new code, no fixture left behind, nothing at the repo root. |
| 4 | `re-run-the-harnesses` | done. Same set, same order, same `PEARDE_ROOT`. Every count equal to its baseline; no drop, no rise, so no flip is claimed for this pass and none is available to claim. The one harness with no baseline is named as new. Formatter/linter step is a no-op: no file was edited. |
| 5 | `write-the-specs` | applied as the second pass applies it — its `Fails when` table read against the block that already stands, no spec authored. The block holds no board-wide gate, no `## ` at line start, no `<placeholder>`, no `! <cmd>`, no `<test> && <good news>` shape, and asserts no literal probe total; it exits 0 under `bash -e -o pipefail -c "$(awk …)"`, the way `collect` runs it. The table's report-path row fired: a previous pass's `report.md` was on disk and its `## Findings` is carried forward above as Finding 1. |

### Edits

`capture-the-harness-baseline`, step 1. The step names one command as the way
to measure a lane, and it is the command that does not finish here. Replace:

> Most board harnesses take their root from `PEARDE_ROOT` and fall back to the
> board's own repo, which is always the orchestrator's checkout — so a worker
> building in a lane runs `PEARDE_ROOT=<lane> bash resources/doctor.sh
> --harnesses <board>`, or exports `PEARDE_ROOT=<lane>` before running one by
> hand.

with:

> Most board harnesses take their root from `PEARDE_ROOT` and fall back to the
> board's own repo, which is always the orchestrator's checkout — so a worker
> building in a lane runs `PEARDE_ROOT=<lane> bash resources/doctor.sh
> --harnesses <board>`, or exports `PEARDE_ROOT=<lane>` before running one by
> hand. `--harnesses` runs the whole board's sweep, four at a time, and it can
> die on the sweep rather than on your unit: measured here it exited 144 with
> the `harnesses` and `jstests` rows never printed and `sleep 0.1` at the
> concurrency gate reporting `Terminated: 15`. Check that the `harnesses` row
> is actually in the output before treating the run as a baseline; where it is
> not, invoke the harnesses your footprint names one at a time with the same
> `PEARDE_ROOT`, which is the same measurement and does not depend on 90 other
> PRDs' harnesses staying alive.

`attempt-the-build`, the lane row ending "where it names conflicting files
that are all inside your footprint, rebase the lane onto the checkout's branch
and resolve them". The row decides on the conflicting *file*, and a lane cut
from a dirty checkout carries commits that are nobody's PRD — so a file inside
the footprint can conflict on hunks that are two siblings' and a rebase then
replays foreign commits onto `main`. Append to that row's **do** cell:

> Decide on the conflicting **hunks**, not the file. `git merge-tree
> --write-tree HEAD lane/<slug>` prints the three stage blobs; diff base
> against each side and read whose lines they are. Where every conflicting hunk
> is outside this PRD's meaning — measured here, `references/files.md`
> conflicting on manifest rows for three other PRDs' modules while this
> footprint's rows sat 100 lines away — do not rebase: `git log --oneline
> main..lane/<slug>` will name commits this PRD never made, and replaying them
> lands other people's work. Prove your own hunk instead (clone the checkout,
> commit the neighbour's working copy, `git apply --3way` your diff) and report
> the conflict for the orchestrator.

## Scores

complexity: 12
blast-radius: low
workflow: probe-then-spec
