# four-stale-self-tests-are-re-aimed-at-the-code-that-moved — analyst report

**Verdict: SPECCED** — 4 specs, complexity 14, blast-radius mid, workflow
`probe-then-spec`.

The build went all the way through. Every one of the four harnesses was shown
red before and green after, run individually, never through a sweep. Six checks
moved across five files; not one line of product code was touched. The probe
pass is uncommitted in the tree for the implementer to continue.

## What the build did

| harness | before | after |
|---|---|---|
| `one-page-that-says-whats-up` | 31 · 29 pass · **2 fail** | 31 · **31 pass · 0 fail** |
| `seven-closed-probes-drifted-red/the-fixtures-meet-the-tool` | 35 · 34 pass · **1 fail** | 35 · 34 pass · 1 fail — the PRD's row is green; the remaining one is a neighbour's, see Findings |
| `the-board-runs-itself/collect-is-a-command` | 133 · 132 pass · **1 fail** | 133 · **133 pass · 0 fail** |
| `the-board-runs-itself/init-asks-nothing` | 88 · 87 pass · **1 fail** | 88 · **88 pass · 0 fail** |
| `workflows-on-the-board/workflow-improve` | **70/71** | **71/71** |
| `the-collect-and-brief-harnesses-are-carried-across-the-layou` (downstream, not edited) | red via its sibling | **7 · 7 pass · 0 fail, exit 0** |

Baseline and after-runs are saved whole, per run, under
`/private/tmp/claude-501/-Users-feb-dev-infra-pearde/f54db065-9498-4db2-b176-a7f14d5ea4b5/scratchpad/baseline-analyst-4stale/`.
`python3 resources/index.py check` exits 0, unchanged.

## The six re-aims

1. **The vision line.** `eaa11a1` moved `<div id="purpose">` out of the timeline
   section and into `<aside id="state">`. The check now asserts
   `<aside id="state"` < `id="purpose"` < the first `</aside>` after it.
2. **The stage height.** `4ce11ec` re-measured the header and the no-script
   fallback became `calc(100vh - 104px)`. The needle reads `104px`.
   `render.py` and `view.css` were not touched — `git diff --name-only` names
   neither.
3. **The spent non-goal.** `the-fixtures-meet-the-tool:174` pinned
   `grep -c parse-cache .pearde/.gitignore` at **0** — it froze the *absence* of
   a fix, and its own label said "a finding, not a fix". The fix landed. The
   check now asserts the anchored line is present exactly once
   (`^\.state/parse-cache\.json$` = 1). The harness's pinned denominator of 35
   is unchanged, because the check was re-aimed in place rather than added.
4. **and 5. The vanished registry, both harnesses.** `REG` now points at
   `$ROOT/.pearde/.state/serve.json` — the path `serve.py entry_path()`
   actually returns after `every-artifact-lands-inside-the-board`. The silent
   sibling is the important half: it compared an empty string to an empty
   string. Pointing it at the live path is **not enough** — the real board is
   unregistered whenever the view daemon is not watching it, so it would stay
   empty-versus-empty. Both sides now end `|| echo absent`, so a run that
   *creates* the real board's registration flips `absent` to a checksum and the
   check fails. The loud half is re-aimed to the invariant rather than to a
   deleted file's contents: `find "$TOP/srv" -name serve.json` is 0 — the
   copied install is code only. `find` does not follow the symlinks `$TOP/srv`
   holds into the real tree, so it reads only the copy.
6. **The rewritten prose.** `78357ed` replaced the three-way "On return" table
   in `references/parts/workers.md` with prose when `collect --report` took the
   verdict lookup off the orchestrator. The row's claim survived: whichever
   verdict a report carries, its `## Workflow` rows stay the orchestrator's.
   The check reads the sentence that now carries it — "…is the belief and the
   `## Workflow` rows, as above." `workers.md` was not edited.

## Non-vacuity, proven for all six

Every re-aimed check was mutated and shown to go red, each mutation on scratch
text or in a `mktemp -d`, never against a real file:

```
live tree: True                     | purpose out of the drawer: False
height: fails when the rule changes
parse-cache count with the line gone: 0  (want 1)
workers: fails when the sentence goes
find count: 0 with no serve.json    | 1 once one lands
absent sentinel: "absent" -> "2192966820 2" — CATCHES creation
```

## Findings — not fixed, not specced, not new PRDs

1. **The PRD cites two paths that do not exist.** `resources/view/render.py:459`
   and `resources/view/view.css:508` — there is no `resources/view/`. The files
   are `resources/board/render.py` and `resources/board/view.css`, and both line
   numbers are correct there. Cited, not re-established; nothing followed from
   the slip.
2. **Three more harnesses carry the same dead `REG` path, vacuously green.**
   `seven-closed-probes-drifted-red/init-seeds-a-board-doctor-calls-green:33`,
   `the-tool-keeps-its-word/collect-keeps-its-word:320`, and
   `the-board-runs-itself/the-next-line-runs:16` each set
   `REG="$ROOT/resources/board/state/serve.json"` and each compares empty to
   empty at a "the real registry is untouched" row. Same defect as trap 1, three
   harnesses the PRD does not name. Left alone — widening the contract is
   REFINE, and these are green, so nothing is blocked on them. The fix is the
   two-line shape in spec03, copied.
3. **A check in `the-fixtures-meet-the-tool` is not isolated from other
   sessions.** `F no file under resources/ carries any of this` reads
   `git diff --name-only -- resources/board/plan.py resources/board/init.py`
   over the whole working tree. Between this run's baseline and its re-run,
   another session left `resources/board/init.py` dirty (an `index_memos(board,
   verb=...)` change, unrelated to anything here), and the row went red on their
   work. The harness's own contract row is green. A red there does not mean a
   regression, which is exactly what this PRD exists to stop — but it is a
   different check in a different PRD's harness, so it is reported, not fixed.
   spec02's third box makes the implementer account for it explicitly.
4. **The tree moved under this run.** At baseline `git status` was clean; by the
   re-run, neighbours held `references/parts/workers.md`, `resources/board/brief.py`,
   `resources/board/init.py` and `resources/doctor.sh` uncommitted, and had
   modified two other PRDs' `verify.sh` files on the board branch. `workers.md`
   in particular is being edited right now and spec04 reads a sentence in it;
   spec04 says what to do if it has moved again.
5. **The knowledge base has no gap to file.** `knowledge.py query` returned 11
   hits, 11 strong, and enqueued nothing into `.pearde/wiki/pending/`. Nothing
   was learned outside this repo, so nothing was written back.
6. **Trap 2 confirmed, untouched.** `init-seeds-a-board-doctor-calls-green`'s
   `D doctor exits 0` is the port-race at its `probe/verify.sh:35`, belonging to
   the harness-run PRD. Not run, not fixed, not counted here.

## Specs

- `specs/spec01.md` — the page harness follows the two deliberate view changes (complexity 4)
- `specs/spec02.md` — the spent non-goal becomes a guard on the fix that landed (complexity 2)
- `specs/spec03.md` — the vanished registry: four checks in two harnesses, not two (complexity 6)
- `specs/spec04.md` — the rewritten prose keeps its check, on the sentence that carries it (complexity 2)

Union of footprints:

```
.pearde/prds/one-page-that-says-whats-up/probe/verify.sh
.pearde/prds/seven-closed-probes-drifted-red/the-fixtures-meet-the-tool/probe/verify.sh
.pearde/prds/the-board-runs-itself/collect-is-a-command/probe/verify.sh
.pearde/prds/the-board-runs-itself/init-asks-nothing/probe/verify.sh
.pearde/prds/workflows-on-the-board/workflow-improve/probe/verify.sh
```

**complexity 14** — six one-to-few-line check edits, no product code, no new
mechanism. The cost was not the edits but reading what each check had been
written to mean and deciding the honest re-aim; the registry pair needed a
sentinel invented before it measured anything, which is the only real design in
the set.

**blast-radius mid** — nothing outside five harness files changes, and no
shipped behaviour can break. But these are the gates a PRD is called done
against, and a re-aim that is subtly wrong makes a gate lie silently, which is
the failure the PRD was written to end. Contained, but load-bearing.

## Workflow probe-then-spec

| # | atomic | ran | outcome |
|---|---|---|---|
| 1 | `read-the-contract` | yes | the PRD's table named all four sites and both traps; nothing had to be re-established, and no question arose |
| 2 | `capture-the-harness-baseline` | yes | all five recorded red, whole outputs saved under a run-named subdirectory; `git status --short` clean at that moment, which is the only reason finding 4 could be told apart from this run's own work |
| 3 | `attempt-the-build` | yes | six checks re-aimed; the build hit nothing undefined |
| 4 | `re-run-the-harnesses` | yes | every changed count accounted for, including the downstream harness clearing with no edit and the one row that reddened on a neighbour |
| 5 | `write-the-specs` | yes | four specs |

### Edits

None. Every step's `## Do` matched what the run actually needed, and no
`## Done when` was wrong. One note that is the run's fault and not the atomic's:
`capture-the-harness-baseline` step 3 asks for `bash resources/doctor.sh` at
baseline and this run skipped it, because the brief forbade touching
`doctor.sh` and a neighbour held it uncommitted. The footprint is entirely under
`.pearde/prds/`, outside the manifest scan, and `index.py check` exits 0 before
and after — so nothing was lost, but the skip is recorded rather than hidden.

## Scores

complexity: 14
blast-radius: mid
workflow: probe-then-spec
