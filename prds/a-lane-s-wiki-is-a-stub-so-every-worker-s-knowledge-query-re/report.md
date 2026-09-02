# a lane's wiki is a stub so every worker's knowledge query returns nothing — implementer report

Verdict: DONE

Both specs are green. 13 of 13 acceptance boxes ticked, each against output
quoted below. The probe reads `19 checks · 19 pass · 0 fail`, both
`## Verify and Proof` blocks exit 0 under `collect`'s own flags
(`bash -e -o pipefail`), and both exit 1 with the footprint file mutated.

`harvest` was run once against the live board, as spec02 reserved for this
pass: **35 note(s) recovered, 1 already on record, from 27 lane wiki(s)**.
Zero lane wikis remain. The record went from 83 to 88 notes.

The build stands in the lane
`pearde/.lanes/a-lane-s-wiki-is-a-stub-so-every-worker-s-knowledge-query-re`,
uncommitted, one file: `resources/knowledge.py`, +163 −5.

| spec | boxes | verdict |
|---|---|---|
| `specs/spec01.md` — the resolver climbs to the board | 7/7 | green |
| `specs/spec02.md` — `harvest` recovers the stubs | 6/6 | green |

## Workflow probe-then-spec

| # | step | outcome |
|---|------|---------|
| 1 | `read-the-contract` | ok. `prd.md`'s body is the unedited template, so the contract was read from `specs/` and from pass one's `report.md` — the row `## Fails when` names. Every `@` resolved. `git status --short` recorded in three roots before the first command. |
| 2 | `capture-the-harness-baseline` | ok. Six knowledge harnesses plus the repo gate, in the lane and in the checkout. Every one matched the count pass one published, so the inherited baseline is confirmed rather than re-taken by reverting. |
| 3 | `attempt-the-build` | **not entered.** This is the route's second pass: the specs exist and the build is in the tree. The step's first `Fails when` row covers exactly this and says to run 1, 2 and 4 only. No red-to-green on this tree is claimed as this pass's. |
| 4 | `re-run-the-harnesses` | ok. All six unchanged. One harness appeared mid-run with no baseline. |
| 5 | `write-the-specs` | applied as the second pass does — no spec authored. Its `Fails when` table was run over the two blocks that already stood and caught two defects, both repaired below. |

### Edits

No edit is owed to the workflow files. Every failure this run hit was in the
specs, not in an atomic, and every shape was already named in a `Fails when`
row that fired correctly.

## What was run, and what it printed

### spec01 — the resolver

The tree under test is the lane, named in both runs as the atomic requires
(`PEARDE_ROOT=<lane>`).

- **box 1** — `PEARDE_ROOT=<lane> bash pearde/prds/…/probe/verify.sh`, from
  the checkout:

      19 checks · 19 pass · 0 fail
      verify.sh done, fail=0

  Sections A, B, C, D, E, F **and** G all `ok`.

- **box 2** — section D, the negative control, ticked both:

      ok   pre-fix resolver reports 0 notes from a lane — the check can fail
      ok   pre-fix resolver created the stub the PRD names

- **box 3** — the same query, the same second, two cwds:

      lane:     query: 88 hit(s), 3 strong · 88 notes on record
      checkout: query: 88 hit(s), 3 strong · 88 notes on record

  and `ls -a <lane>/pearde` afterwards is `. .. graphify` — no wiki.

- **box 4** — `knowledge.py doctor` from the lane:
  `doctor: clean — 88 notes, graph in sync, pending honest`.

- **box 5** — `bash resources/doctor.sh` from the checkout:
  `knowledge   ok      88 notes on record · graph in sync · pending honest`.
  The row passes `--root` explicitly and was unaffected, as the spec said.

- **box 6** — proved both ways, not just re-run. With the build:

      ok   knowledge.py board wrote 140 PRD note(s), matching disk (140)
      20 checks · 12 pass · 8 fail

  With the two `board_above` lines stripped out of the lane's file (backed up
  to a scratch dir outside the repo, restored, `cmp` clean):

      FAIL knowledge.py board wrote 0 PRD note(s), disk has 140
      20 checks · 11 pass · 9 fail

  One lower with the fix, exactly as the box asks. The other eight failures
  are that PRD's and were not touched.

- **box 7** — `python3 resources/index.py check`. **The box's list is out of
  date and the box still holds.** It names three problems; the tree reports
  neither three nor the same three, and neither reading names
  `resources/knowledge.py`:

  - from the **checkout**: one problem,
    `references/language.md references @references/personas/writer.md` — one of
    the three the box names. The other two (`index.md → @pearde/memos/lanes-share-one-copy-of-what-they-regenerate.md`
    and `resources/board/edit.py → @questions.py`) were **closed by a sibling**
    between pass one and this one: the checkout's HEAD moved from `58c92e6`
    to `1858a35` while this run was in progress. Per the atomic's row on a
    brief's inherited line being absent, my own baseline is the measurement.
  - from the **lane**: five problems — the checkout's one, the box's other
    two, plus `references/skills/pearde-machine.md is on disk with no row in
    references/files.md` and `@@share names @pearde/memos/lanes-share-…`. All
    five are the lane being one commit behind the checkout, not this build.
    Both readings were identical before and after every command this pass ran.

### spec02 — harvest

- **box 1** — section G, all `ok` in the clean-room fixture: `--dry` moved
  nothing, the real run printed
  `harvest: 1 note(s) recovered, 1 already on record, from 1 lane wiki(s)`,
  the stranded finding stood in the board's wiki, the emptied stub was gone,
  the shared graphify symlink and its target survived, and a second run
  printed `no lane holds a wiki of its own — nothing stranded`.

- **box 2** — `harvest --dry` on the live board printed 36 `dry · ` lines and
  the trailing count
  `dry · harvest: 35 note(s) recovered, 1 already on record, from 27 lane wiki(s)`.
  `find pearde/.lanes -path '*/wiki/*.md' | wc -l` was `36` before and `36`
  after. Nothing moved.

- **box 3** — the real run, once:

      harvest: 35 note(s) recovered, 1 already on record, from 27 lane wiki(s)

  Afterwards `find pearde/.lanes -path '*/wiki/*.md'` prints **nothing**, and
  `find pearde/.lanes -maxdepth 3 -type d -name wiki | wc -l` is **0**. Of the
  35, **30 were pending gaps and 5 were sources** — and the record rose by
  exactly five, `83 notes on record` → `88 notes on record`, which is the
  arithmetic the box asks for: `doctor` counts sources and conclusions, not
  pending.

- **box 4** — `doctor: clean — 88 notes, graph in sync, pending honest`. No
  missing frontmatter, no dangling wikilink, in any of the 35 moved notes.

- **box 5** — the shared store is identical before and after:
  `ls .git/pearde-shared/` → `pearde`, `resources` both times, and
  `share status` is **diff-clean end to end**, closing on the same line:
  `233 shared · 0 not yet · 0 refused (git tracks them) · 4 someone else's link`.
  No path went from `linked` to `absent`; 62 `graphify` entries still stand
  under `.lanes`.

- **box 6** — a second `harvest`:
  `harvest: no lane holds a wiki of its own — nothing stranded`, exit 0.

## The harness set

Baseline taken in the lane before the first command, re-run after. Every one
matched pass one's published count, which confirms the inherited baseline
without a window in which the tree is half-reverted — the cheaper confirmation
the atomic prefers to a revert.

| harness | pass one | my baseline | after |
|---|---|---|---|
| `one-definition-of-the-board-not-two` | 12 pass 8 fail | 12 pass 8 fail | 12 pass 8 fail |
| `upgrade-leaves-the-memo-index-stale` | 34 pass 6 fail | 34 pass 6 fail | 34 pass 6 fail |
| `the-doctor-completes-without-a-home` | 9 pass 3 fail | 9 pass 3 fail | 9 pass 3 fail |
| `init-seeds-a-board-doctor-calls-green` | 25 pass 16 fail | 25 pass 16 fail | 25 pass 16 fail |
| `workflow-skill` | 48 pass 7 fail | 48 pass 7 fail | 48 pass 7 fail |
| `every-module-finds-its-siblings-by-one-rule` | 3 pass 20 fail | 3 pass 20 fail | 3 pass 20 fail |

Nothing moved in either direction. The five still-red harnesses were red
against a lane before the first edit of pass one; the family
`every-probe-harness-is-re-aimed-at-the-pearde-layout` and
`two-harnesses-still-name-a-tree-they-do-not-measure` own that.

**A harness appeared mid-run.** `find prds -name verify.sh` counted 72 at
step 2 and 73 at step 4:
`prds/post-report-crashes-a-collect-between-the-done-write-and-the/probe/verify.sh`,
landed by a parallel session. It has no baseline here and is compared to
nothing.

**The checkout's HEAD moved twice under this run** — `58c92e6` at step 1,
`1858a35` at step 4 (`one-copy-per-machine-of-what-every-lane-regenerates`).
Neither commit touched `resources/knowledge.py`, and the lane's base
(`318fbda`) is still an ancestor of HEAD, so the merge is a fast-forward for
this file. See `## The merge` below.

## Two defects in the specs' own verify blocks, repaired

Both were caught by running each block the way `collect` runs it — awked out
of the fence and run under `bash -e -o pipefail` — and both are shapes the
step-5 `Fails when` table names. Neither could have been caught by `specced
--check`, which reads a block's presence and never its exit.

**spec01: `python3 resources/index.py check` exits 1.** It prints a problem
and returns non-zero, so under `-e` the block died on it with every box
already ticked — and the problem it dies on
(`references/language.md → @references/personas/writer.md`) is a file no
footprint of this PRD names. `collect` would have refused the spec with
`spec01 exit 1 — nothing written` for a reason outside the unit. Repaired the
way the table's board-wide-gate row prescribes — capture, refuse a crashed
producer by exit code, then gate only on rows naming this spec's own
footprint path:

```sh
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
if [ -z "$out" ] && [ "$rc" != 0 ]; then echo "index.py check crashed before printing"; exit 1; fi
printf '%s\n' "$out"
if printf '%s\n' "$out" | grep -q 'resources/knowledge\.py'; then exit 1; fi
```

The rows stay visible and stop deciding the exit. Note the `if … then exit 1;
fi` rather than a trailing `&& exit 1`: under `pipefail` the tail of a
`… | grep … && exit 1` line is dead.

**spec02: `pearde share status` — `pearde` is not on this machine's PATH.**
`command -v pearde` finds nothing, so the line was a 127 that `-e` turned
into the block's exit. Repaired to the module the repo actually ships, and
captured, since its output is evidence and not a gate:

```sh
share=$(python3 resources/pearde.py share status 2>&1) && src=0 || src=$?
if [ -z "$share" ]; then echo "share status printed nothing (exit $src)"; exit 1; fi
printf '%s\n' "$share" | tail -1
```

Both blocks now:

    spec01 FINAL EXIT=0 · 19 checks · 19 pass · 0 fail · verify block complete
    spec02 FINAL EXIT=0 · 19 checks · 19 pass · 0 fail · verify block complete

**And both can fail.** The mutation is behavioural, not a renamed string: the
two `memos.board_above` lines were stripped from the lane's
`resources/knowledge.py` — the thing the unit *computes*, the board it
resolves — with the file backed up to a scratch dir outside the repo:

    spec01 MUTATED EXIT=1 · 19 checks · 9 pass · 10 fail
    spec02 MUTATED EXIT=1
    RESTORED cmp clean

`git diff --stat` after the restore is the same `163 insertions(+), 5
deletions(-)` it was before.

Both blocks hard-code `PEARDE_ROOT="$PWD"`, which names the orchestrator's
checkout. They were run once with the lane substituted, as the atomic
directs, and left as written — after `collect` merges, `$PWD` is the tree
that carries the fix and the blocks are correct as they stand.

## The graph index is part of adding a note

`doctor.sh`'s `knowledge` row was **broken before the first edit of this
pass**: `graph.json is behind the files: 260902-2085` — the note pass one
wrote. Harvesting 35 more would have widened it to six ids. This is the same
class as the memo index the step-5 table already names:
`wiki/.graphify/graph.json` is generated, gitignored, and regenerating it is
part of adding a note rather than a separate edit.
`python3 resources/knowledge.py relink` was run after the harvest; it wrote
`88 nodes, 38 edges` and changed **no tracked wiki file**
(`git status --short -- wiki` is 120 lines before and after, diff empty). The
row is `ok` again.

The footprint is wrong on this point in the same way it is wrong for a memo
spec, and the next author of a spec that writes notes should carry the relink
in it.

One artefact of my own was removed: the negative-control window ran the
pre-fix resolver against the live board, which enqueued
`wiki/pending/260902-3dd5.md` — `question: "board"`, a gap the tool invented
because it was reading an empty record. It is an artefact of the control, not
a question of the board's, and was deleted, the same way pass one deleted
`pending/260902-5d10.md`.

## The merge

The lane is one file, `resources/knowledge.py`, uncommitted, cut from
`318fbda`. The checkout is at `1858a35` and **clean**. Since the lane was cut,
one commit touched this file — `72d5afc` *the graph view is coloured by tag,
not by folder* — and its hunks are at lines 318, 550 and 671–691. This lane's
hunks are at 8, 17–31, 1062, 1107 and 1124. **Disjoint**, so the rebase is
clean and no hunk of the sibling's is at risk.

Nothing was carried from the checkout into the lane and nothing was written
into the checkout: `git status --short` in the checkout is empty, and in the
lane it is the single line ` M resources/knowledge.py`.

## Findings — carried forward from pass one, plus this pass's

Pass one's five findings all still stand and none is fixed here. Restated by
name so the board keeps its only copy:

1. **`references/knowledge.md:23,63` calls the wiki gitignored and "machine-local
   data, not source".** Half true in a way that would license deleting the
   record: it is gitignored in the code checkout and **tracked in the board
   worktree**. Owned by
   `every-document-is-written-in-the-writer-s-prose/the-loose-reference-files-are-rewritten-dense`.
2. **`references/skills/pearde-knowledge.md:7-8` says "the default root is
   `.pearde/wiki/`".** After this landing the default root is the board above
   the cwd. Owned by `…/skills-and-scout-docs-are-rewritten-dense`.
3. **`references/files.md`'s row for `@resources/knowledge.py` will not list
   `harvest`.** In six live footprints; a one-line edit into a file being
   rewritten wholesale is a rebase conflict.
4. **`pearde share` does not cover the wiki, and should not** — adding
   `pearde/wiki` to the `SHARED` table would show 24 deletions in the board
   worktree, which `share`'s `invisible()` guard cannot see. Recorded because
   it is the obvious wrong fix.
5. **The grammar defines neither `lane` nor `wiki`,** nor `harvest`, the word
   this build coined. All three were used again this pass.

New this pass:

6. **`resources/index.py check` exits non-zero when it prints a problem, and
   this is not written down anywhere a spec author would look.** Two specs on
   this board put it bare in a `## Verify and Proof` block; both would have
   been refused by `collect` for a reason outside their footprint. It is the
   same trap as `doctor` and a repo-root `git status`, and the step-5 table
   names those two but not `index.py check`. Worth a row.
7. **`pearde` is not on this machine's PATH,** though the skill's own prose
   and at least one verify block spell commands as `pearde <verb>`. Every
   working caller on this board goes through `python3 resources/pearde.py`. A
   spec that writes `pearde …` in a block is a 127 under `-e`.
8. **The board grew a stub wiki mid-run, twice, from my own negative
   controls** — which is the defect working exactly as described, and is the
   cleanest possible demonstration that the fix is load-bearing: the moment
   the two `board_above` lines are gone, `<lane>/pearde/wiki` reappears.
   `harvest` cleaned both, which also incidentally proved it idempotent on
   the live board and not only in the fixture.

## The record

`harvest` moved 35 notes onto the record, so the record now answers questions
27 lanes had been asking into a directory `git worktree remove` deletes. No
fact was learned outside this repo this pass, so nothing new was written with
`knowledge.py remember`; pass one's `[[260902-2085]]` stands and is now in the
graph.

## Scores

complexity: 18
blast-radius: mid
workflow: probe-then-spec
