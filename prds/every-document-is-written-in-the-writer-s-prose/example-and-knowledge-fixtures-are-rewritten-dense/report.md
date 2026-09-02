# report — example-and-knowledge-fixtures-are-rewritten-dense

Verdict: DONE

17/17 boxes closed, 26/26 probe checks green on the merged tree against main
at `9a98fae`. No file was rewritten this pass: the retry's two owed repairs
had already landed on the lane, and every box the retry doubted was re-run
against a merged tree built from today's main rather than the stale base the
first run used. The pass is a verification pass, and says so.

## What this pass did, and did not

The retry was opened on three counts (`prd.md § History`). All three are
answered on the lane as it stands:

1. **The merge conflict is gone.** `git merge-tree --write-tree main HEAD`
   exits 0 and returns `99d5564…` — a clean merge into `9a98fae`, seven
   commits past the `fc75bcf` the specs were written against and eleven past
   the `d240590` the first `collect` failed on. The lane rebased and picked
   up commit `8757f22 the example fixtures carry the tags the checkers now
   require`, which is what keeps `memos.py check` and `workflows.py check`
   silent against main's newer checkers.

2. **The two red boxes are green.** `8f6ccfa`'s appended "File index"
   paragraphs in `resources/board/knowledge/Dashboard.md` are rewritten dense
   on the lane (`60b8fae the appended File index sections read dense too`),
   with no exclusion carved. On the merged tree:

       $ python3 resources/prose.py check $(find resources/board/example \
           resources/board/knowledge -name '*.md' | sort)
       exit=0

   Twenty-two fixture files, no output, exit 0. That closes spec02 box 1 and
   spec03 box 5 — the two the retry named.

3. **The struck box stays struck.** spec03's `## Struck box, and why` already
   replaced the untracked-board assertion with box 3, `pearde.py init` into an
   empty temp dir then `memos.py check` on the planted board. The probe runs
   it (`spec03.3 a board this generator made checks clean`) and it is green.
   Nothing about the machine-local `pearde/memos/README.md` is load-bearing
   for any box any more.

I rewrote no prose. Every one of the eighteen fixture files was already
written; re-deriving them would produce different words and the identical
green, and the retry said explicitly not to redo them. What was owed was a
run on a tree that is not stale, and that is what this is.

## Box status

All seventeen boxes carry `[x]`. Each maps to one or more of the probe's
twenty-six checks, and every one was re-run this pass on the merged tree.

| spec | boxes | probe checks | result |
| --- | --- | --- | --- |
| spec01 — the example board fixtures read dense | 6/6 | 11 | green |
| spec02 — the knowledge seed reads dense | 6/6 | 10 | green |
| spec03 — the generated memo index reads dense | 5/5 | 5 | green |

## Verify output

    $ bash .pearde/prds/every-document-is-written-in-the-writer-s-prose/\
      example-and-knowledge-fixtures-are-rewritten-dense/probe/verify_merged.sh
    merged tree 99d55648936f8f4e59838c54aa88e50d2828fb28  (main + 8757f22 + uncommitted)
    PASS  spec01.0 prose.py ran over 22 fixture files
    PASS  spec01.1 prose names no example/ file
    PASS  spec01.2 scan prints 8 PRDs, boxes 3/5 and 3/3
    PASS  spec01.2 band order unchanged
    PASS  spec01.3 memos.py check silent
    PASS  spec01.3 workflows.py check silent
    PASS  spec01.3 questions.py check silent
    PASS  spec01.4 13+ example/ files changed and every line is M
    PASS  spec01.5 box text unchanged in prds/building/specs/spec01.md
    PASS  spec01.5 box text unchanged in prds/finished/specs/spec01.md
    PASS  spec01.6 asking/prd.md keeps three answers, one recommended
    PASS  spec02.1 prose names no knowledge/ file
    PASS  spec02.2 WORKFLOW.md frontmatter byte-identical
    PASS  spec02.3 the legacy name is gone
    PASS  spec02.4 all four workflow ids present
    PASS  spec02.4 the Routing table rows are unchanged
    PASS  spec02.5 dataview fences byte-identical in Dashboard.md
    PASS  spec02.5 dataview fences byte-identical in conclusions/_index.md
    PASS  spec02.5 dataview fences byte-identical in sources/_index.md
    PASS  spec02.6 pearde init plants all five knowledge files
    PASS  spec02.6 knowledge.py doctor is clean on the planted vault
    PASS  spec03.1 the generated index reads dense
    PASS  spec03.2 the example fixture equals what render_index() emits
    PASS  spec03.3 a board this generator made checks clean
    PASS  spec03.4 every content line of the index survives
    PASS  spec03.5 prose names no fixture file at all

    boxes 26/26

Run twice, ten minutes apart, with `main` unmoved at `9a98fae` both times.

### The negative control

The set can still go red. `REF=main` runs the same twenty-six checks against
main alone, without the lane:

    $ REF=main bash …/probe/verify_merged.sh
    FAIL  spec03.1 the generated index reads dense (exit 1, wanted 0)
    FAIL  spec03.2 the example fixture equals what render_index() emits (exit 1, wanted 0)
    FAIL  spec03.5 prose names no fixture file at all (exit 0, wanted 1)

    boxes 17/26

Nine red without the lane, twenty-six green with it. The specs predicted six
red against the older main; today's main makes it nine, because more fixture
prose has drifted in since. Either way the control does its job.

## The footprint

The lane's own changes, `git diff --name-status <merge-base> HEAD`, are
twenty files, every line `M`, every path inside a declared footprint:

- fourteen under `resources/board/example/`  (spec01, plus the generated
  `memos/README.md` that belongs to spec03)
- five under `resources/board/knowledge/`  (spec02)
- `resources/memos.py`  (spec03 — one banner string, `` `memo check` fails
  when it is stale `` → `` `memo check` fails on a stale index ``)

No add, no delete, no rename, and nothing outside. `git diff main HEAD` looks
much wider — it names deletions of `resources/board/session.py` and two
invariants, and edits to `index.md`, `references/parts/*`, `collect.py`,
`shared.py`, `specs.py` and `knowledge.py` — but every one of those is main's
own newer work that the lane has not yet merged, read backwards. The merged
tree carries all of it; the lane reverts none of it.

## The landing step is still owed

spec03's `## What is left` names it, and it cannot be run before the merge:

    python3 resources/memos.py index pearde     # from the repo root

Run it in `/Users/feb/dev/infra/pearde` **after** `collect` lands the lane.
The reason is measured, not assumed. Today `resources/memos.py check` at the
repo root exits 0 and prints nothing, because the shared board's
`pearde/memos/README.md` line 4 still reads the old banner and the committed
generator still writes the old banner. The moment the lane's one-line change
lands, that file is stale and the gate goes red. Running `memos.py index` now
would regenerate it with the old banner — a no-op — so it has to wait.

Name the board directory (`pearde`), not the repo root. A bare
`memos.py index <repo root>` writes a stray `memos/README.md` at the root,
because `find_board` matches any directory basename in `BOARD_DIRS` and this
repo is itself named `pearde`.

Every other board on this machine goes stale the same way and is repaired by
its own next `memo add`; `pearde doctor` names the staleness meanwhile.

## The repo gate

`settings.md § Deliverable` names three. Measured in the main checkout at
`9a98fae`, before this lane merges:

| gate | result | mine? |
| --- | --- | --- |
| `python3 resources/memos.py check` | exit 0, silent | yes — green, and the landing step above keeps it green |
| `python3 resources/index.py check` | exit 1, one problem | no — red on main already |
| `bash resources/doctor.sh` | exit 1, two broken rows | no — both red on main already |

Both failures pre-date this lane and neither is in its footprint. They are
written up under `## Defects outside this scope` rather than fixed.

The `index` row's second problem, and the two extra lines `index.py check`
prints inside the lane worktree, are artifacts rather than defects: they name
`@pearde/memos/…` files that live only in the untracked, machine-local board,
which no worktree and no `git archive` carries. They resolve in the main
checkout.

## Defects outside this scope

**1 · `references/language.md` names a persona that is not on disk.** Line 34
reads `From @references/personas/writer.md, Vera Lindqvist.` The directory
holds `designer.md engineer.md INDEX.md mentor.md skeptic.md` — no
`writer.md`. This is the one problem `index.py check` reports in the main
checkout and the `index broken` row in `doctor.sh`. It is red on main without
this lane, it is a sibling PRD's file, and this PRD's footprint does not
include `references/`. Not fixed. It wants either the persona written or the
reference dropped.

**2 · `doctor.sh` reports `origin broken — 33 derived · 1 with no from:`.**
Board metadata, no file of mine, red on main already. Not fixed.

Neither blocks this lane: `collect` merges twenty files under
`resources/board/` and `resources/memos.py`, none of which is what either row
is about.

## What this PRD does not claim

Carried forward from the first run's disclosure, because it is still true and
still worth a reader's attention: the analyst wrote the eighteen fixture
files and then wrote the acceptance boxes for its own work. Every box is
outcome-shaped — checker exit codes, byte-comparisons, a band-order grep — so
who typed the prose has no bearing on whether they go green, and I re-ran all
twenty-six independently. But `prose.py` counts words, sentence length and
waste words. Passing a word counter is not the same claim as "reads dense",
and this PRD has never made the second one. A reader who wants that claim
wants a person's eye, not another run of the probe.

## Health floor

The brief names no file in this footprint under the floor, and none of the
twenty is. Nothing moved, nothing needed to.
