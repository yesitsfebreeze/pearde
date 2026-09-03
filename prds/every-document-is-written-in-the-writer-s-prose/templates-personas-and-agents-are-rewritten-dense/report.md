# templates-personas-and-agents-are-rewritten-dense — implementer report

Verdict: DONE

All 31 acceptance boxes across the four specs are ticked, and every
`## Verify and Proof` block exits 0 under `bash -e -o pipefail` — in the lane,
and again on a merged tree built by applying the lane's diff onto `main`.

| spec | boxes | block in the lane | group |
|---|---|---|---|
| `spec01` | 6/6 | **exit 0** | `references/agents/` 1015 → 914, 10.0% off · ceiling 915 |
| `spec02` | 9/9 | **exit 0** | `references/personas/` 3112 → 2870, 7.8% off · ceiling 2872 |
| `spec03` | 8/8 | **exit 0** | the seven `.doc.md` 2495 → 2301, 7.8% off · ceiling 2301 |
| `spec04` | 8/8 | **exit 0** | the nine shapes 4690 → 4646, 0.9% off · ceiling 4646 |

This pass wrote no source file. The previous pass reached the fact-preserving
floor on both groups and reported FAILED against two ceilings written below
that floor; between the two passes the two ceilings were replaced with the
measured floors — `spec03` 2211 → **2301**, `spec04` 4580 → **4646** — which is
exactly the reopen the previous `## Failure` names. Both boxes were then
verified by running their own blocks and ticked. Every other box was re-run
rather than inherited.

The two boxes this pass closed:

- `spec03`: `group: 2495 -> 2301 (7.8% off)`, block exit 0.
- `spec04`: `group: 4690 -> 4646 (0.9% off)`, block exit 0.

## The flip, shown against a tree without the build

The build lives uncommitted in the lane; the orchestrator's checkout does not
hold it. Both blocks were run **verbatim** from the checkout, which is the root
`collect` runs them from, and both fail there on the first line —
`prose.py check` — before they ever reach the ceiling:

```
spec03 in the checkout: exit 1
  references/templates/memo.doc.md: 1 unbound waste word(s) (that)
  references/templates/prd.doc.md: 4 unbound waste word(s) (it)
  references/templates/report.doc.md: 1 unbound waste word(s) (that)
  references/templates/workflow.doc.md: 1 unbound waste word(s) (this)
spec04 in the checkout: exit 1
  references/templates/grammar.md: 4 unbound waste word(s) (it, that)
  references/templates/health.md: 1 unbound waste word(s) (it)
  references/templates/prd.md: 1 unbound waste word(s) (this)
```

The whole gate ran on the pre-build files and went red; it runs green on the
lane. Nothing here is a neighbour's landing.

## The merge is clean, and green

The lane is at `31620bb`; `main` is at `f8968fe`, eleven commits ahead, so
`lanes.merge` needs a rebase. One footprint file overlaps —
`references/templates/grammar.md`, which `main` changed in two table rows
(`plan.py` → `mapfile.py`, `skills/` → `references/skills/`). Proved before the
merge rather than in `collect`: `git clone --shared -b main` to scratch, then
`git apply --3way` of the lane's whole diff — **all nineteen files applied
cleanly, exit 0**, no conflict. The four blocks then run on that merged tree
with `BASE=31620bb`:

```
spec01 exit 0   group: 1015 -> 914 (10.0% off)
spec02 exit 0   group: 3112 -> 2870 (7.8% off)
spec03 exit 0   group: 2495 -> 2301 (7.8% off)
spec04 exit 0   group: 4690 -> 4646 (0.9% off)
```

`main`'s two grammar.md edits are inside backticked code, which `prose.py`
excludes from its count, so the merged counts are the lane's.

## Verify output

`python3 resources/prose.py check references/agents/*.md references/personas/*.md
references/templates/*.md` in the lane — exit 0, silent, over the whole
footprint.

Board harnesses. No harness on this board names a footprint path in a way that
reads it; eight name one in a fixture or an assertion, and one sibling harness
runs `prose.py`. Baselined before the first edit with `PEARDE_ROOT=<lane>`, and
re-run after, same order, same command lines, same root:

| harness | baseline | re-run |
|---|---|---|
| `the-board-runs-itself/brief-is-printed` | 41/104, exit 1 | 41/104, exit 1 |
| `the-board-runs-itself/init-asks-nothing` | 52 pass · 37 fail, exit 1 | 52 pass · 37 fail, exit 1 |
| `the-board-runs-itself/one-command` | 47 passed, 7 failed, exit 1 | 47 passed, 7 failed, exit 1 |
| `the-board-runs-itself/too-big-splits-itself` | 24/60, exit 1 | 24/60, exit 1 |
| `the-board-runs-itself/vision-is-first-class` | 52/52, **exit 0** | 52/52, **exit 0** |
| `the-round-runs-in-a-window-that-ends` | 25 pass · 1 fail, exit 1 | 25 pass · 1 fail, exit 1 |
| `workflows-on-the-board/workflow-attach` | 44/47, exit 1 | 44/47, exit 1 |
| `workflows-on-the-board/workflow-seed` | 65 pass · 7 fail, exit 1 | 65 pass · 7 fail, exit 1 |

Every one of those reds is **before the first edit** and inherited. Seven
failing lines name a footprint path; each was checked against the base revision
`31620bb` and is red there too:

- `too-big-splits-itself`: `references/templates/prd.md lacks: above` `split-above` and
  `lacks: under ## Children`. Neither string is in `git show 31620bb:references/templates/prd.md`.
- `workflow-attach`: `references/templates/prd.md lacks '# workflow:'` and
  `references/templates/spec.md lacks '# workflow:'`. `spec.md` is not modified
  in the lane at all, and neither string is at the base.
- `brief-is-printed`: three `Work as @references/personas/…` rows whose *got*
  side is empty — the lane has no board, so `brief` prints nothing. The persona
  path is the harness's expectation, not a file it reads.

A pre-edit control was taken as well: `git clone --shared <lane> <scratch>/pre`
run with `PEARDE_ROOT=<scratch>/pre`. Seven of the eight are identical to the
built tree. `workflow-seed` scores **worse** in the clone (63 pass · 9 fail) on
two `doctor` rows — the clone has no gitignored board, the known
archive-versus-checkout hazard — so that rise is the missing board, not this
build, and it is not claimed as a flip.

The sibling harness
`every-document-is-written-in-the-writer-s-prose/skills-and-scout-docs-are-rewritten-dense/probe/verify.sh`
is the one harness of 78 that ignores `PEARDE_ROOT`: it `cd`s to a hard-coded
`…/pearde/.lanes/…` path that does not exist and exits 2 before running
anything. Recorded, not repaired — it is that PRD's file. See the findings.

The repo's own gate, both roots, unchanged across the run:

```
lane      index.py check  exit 1
          references/language.md references @references/personas/writer.md — not on disk
          references/parts/commits.md references @pearde/memos/a-board-s-own-file-…md — not on disk
checkout  index.py check  exit 1
          resources/common.py is on disk with no row in references/files.md
          references/files.md lists @resources/board/hotreload-test.js — not on disk
          @@view names @resources/board/hotreload-test.js — not on disk
          references/parts/commits.md references @pearde/memos/a-board-s-own-file-…md — not on disk
```

No line in either root names a path under `references/agents/`,
`references/personas/` or `references/templates/`, which is why every spec's
index check is anchored on its own prefix. The checkout's set has moved since
the previous pass — `main` gained eleven commits — and the lane's
`@pearde/…` line is the lane's missing board by construction.

`bash resources/doctor.sh` in the checkout: `health` (a stale ranking, 29
commits behind, and four dropped files), `knowledge` (graph.json behind on
`260902-4f91`, `260902-aae0`) and `questions` (an `## Answers` with no
`## Questions` in `resources-are-organised-by-responsibility/every-module-finds-its-siblings-by-one-rule`)
broken. All inherited, none names a file in this footprint.

## What stands in the tree

Nineteen files, uncommitted in the lane
`/Users/feb/dev/infra/pearde/.pearde/.lanes/every-document-is-written-in-the-writer-s-prose-templates-personas-and-agents-are-rewritten-dense`,
all from the two earlier passes; this pass added none and changed none:

`references/agents/pearde-analyst.md`, `pearde-implementer.md`,
`pearde-pass.md`; `references/personas/INDEX.md`, `designer.md`, `engineer.md`,
`mentor.md`, `skeptic.md`; `references/templates/atomic.doc.md`,
`memo.doc.md`, `prd.doc.md`, `report.doc.md`, `spec.doc.md`, `vision.doc.md`,
`workflow.doc.md`, `grammar.md`, `health.md`, `prd.md`, `report.md`.

`references/templates/spec.md`, `memo.md`, `workflow.md`, `atomic.md` and
`vision.md` are unchanged and stay unchanged: 36 to 85 words each, every one a
frontmatter key, a heading or an angle-bracketed placeholder that is the
shipped shape.

The checkout is clean. On the board, only this PRD's own directory is
untracked. No health-floor file is in this footprint.

## Findings

The first four are carried forward from the two earlier passes, unfixed and
still standing.

1. **`prose.py` reads frontmatter as prose.** `resources/prose.py` strips fenced
   and inline code and skips headings, table rows, bullets and blockquotes, and
   never strips the `---` block. `references/templates/health.md` is flagged for
   a comment inside a closed, ordered key set that `health.py` writes. Written
   around here by rewording the comment. Owner:
   `a-density-checker-and-the-root-docs-are-rewritten`, `done`.
2. **A restrictive relative clause is flagged as a vague subject.** The rule
   bans `it is`, `this means`, `there are` — a pronoun with no noun. The regex
   also fires on `every one that is ready` and `when there is one`, where `that`
   and `there` are bound. Rewording those buys no density. Same owner.
3. **`references/personas/writer.md` is in no commit.** The parent PRD names it
   as the source of the density rules. `index.py check` still names it in the
   lane; on `main` the line is gone, so `references/language.md` was reworded
   between the passes and no file cites the missing persona any more. The
   persona itself is still not on disk, and
   `the-standard-is-held-to-its-own-standard` is still its obvious home.
4. **A box may carry a ceiling derived from a base its own block does not
   measure, and nothing checks the two agree.** `spec03`'s box still reads
   "fall from 2456 to **2301 or fewer** … 6.3% off" while its own block sums
   the base at **2495** and prints **7.8% off**. Only the ceiling decides the
   exit, so the box passes, but its stated base and rate are wrong by 39 words
   and 1.5 points. `pearde specced` reads a block's presence and `collect`
   re-runs it — neither compares a box's stated base to the block's. Not
   repaired here: correcting the base and the percentage is a spec edit, and
   redefining a spec is not the implementer's. The route edit below is the fix.
5. **New. One board harness of 78 ignores `PEARDE_ROOT` and `cd`s to a path
   that does not exist.**
   `prds/every-document-is-written-in-the-writer-s-prose/skills-and-scout-docs-are-rewritten-dense/probe/verify.sh`
   line 23 `cd`s to `/Users/feb/dev/infra/pearde/pearde/.lanes/…` — the
   pre-`.pearde` board spelling — and exits 2 with
   `cd: … No such file or directory` before running an assertion. It is the
   only harness `grep -L PEARDE_ROOT` names. Left alone: it is that PRD's file,
   and the repair is owed to its owner.

`python3 resources/grammar.py show` defines every word this contract uses. The
route needed no term the file does not hold, and nothing was learned outside
this repo, so `knowledge.py remember` had nothing to take.

## Workflow probe-then-spec

| # | atomic | outcome |
|---|--------|---------|
| 1 | `read-the-contract` | ok — PRD, four specs, both earlier `report.md` reads, `git status --short` in lane, checkout and board recorded before the first command that writes. The PRD body carries a `## Failure` from the previous pass that the reopen left in place; the specs are the contract and both ceilings had moved |
| 2 | `capture-the-harness-baseline` | ok — the eight harnesses naming a footprint path, plus a pre-edit `git clone --shared` control with `PEARDE_ROOT`; `index.py check` in both roots; `doctor.sh` in the checkout. All four blocks run under `bash -e -o pipefail` before the first write: 0, 0, 0, 0 |
| 3 | `attempt-the-build` | entered for no spec — the third pass on this route. Each spec's own footprint was checked with `git status --short` and `git diff` before deciding, and every block already exited 0, so there was nothing to build. The work is claimed as this PRD's, not as a flip of this pass |
| 4 | `re-run-the-harnesses` | ok — same set, same order, same `PEARDE_ROOT=<lane>`. No count fell. The one that rose is the clone's missing board, said so |
| 5 | `write-the-specs` | not entered — implementer pass. The `Fails when` table was applied to the four blocks that already stand; one row fired, finding 4, and the repair is a spec edit outside an implementer's remit |

### Edits

One, carried forward from the previous pass and still unapplied, against step
5's `## Fails when` table in `write-the-specs`. The existing row covers a box
that quotes a count; it does not cover a box that quotes a ceiling computed
from a base the block re-derives at run time. `spec03` in this PRD still holds
a live instance. Proposed row:

| seen | means | do |
|------|-------|----|
| a box states "fall from `<B>` to `<C>` — `<P>`% off" and the block's own base sums something other than `<B>` | the ceiling was computed from a base the block does not measure, so the block enforces a rate nobody chose — `<C>` against the real base, not `<P>`% | print the block's base line before writing the box (`prose.py stat <base> \| grep <the group> \| awk '{b+=$2} END{print b}'`), paste that number into the box, and derive `<C>` from it. Never carry a base measured at a different moment of the pass |

A second row, new, against step 2's `## Fails when` table. Step 2 says
`grep -L PEARDE_ROOT` names the harnesses that ignore it and that their counts
are the checkout's however you invoke them. That is the benign case. The
harness this run met does not measure the checkout either — it `cd`s to a
hard-coded lane path from a previous board layout and exits before its first
assertion, so it contributes a non-zero exit that looks like a red:

| seen | means | do |
|------|-------|----|
| a harness in the baseline set exits 2 on `cd: … No such file or directory` naming a `.lanes/` path that is not yours | the harness hard-codes another PRD's lane, which `collect` removed when that PRD landed — it measures nothing, in any root, and its exit is not a colour | record it as *not run* rather than as red, never compare it across the two runs, and report the hard-coded path to that PRD's owner. `grep -L PEARDE_ROOT` names this class alongside the harnesses that merely default to the checkout; the two are not the same finding |

Nothing else in the route misled the run. Every other `Fails when` row this
pass hit — the second-pass entry rule in step 3, the lane's `@pearde/…`
dangling reference and the clone-versus-checkout hazard in step 2, the adjacent
uncommitted hunk in step 4, the previous report at the report path in step 5 —
read exactly as the run went.
