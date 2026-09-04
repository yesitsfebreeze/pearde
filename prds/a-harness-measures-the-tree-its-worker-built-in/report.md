# a harness measures the tree its worker built in — implementer pass four

Verdict: BLOCKED

Same wall as pass three, re-measured from scratch and not inherited: 30 of
this PRD's 31 acceptance boxes stand, specs 01-04 all exit 0 the way `collect`
runs them, and `spec05` box 8 cannot be closed by any work this PRD is allowed
to do. Pass three put three options to the orchestrator; nothing was answered
and nothing was collected — `.state/transitions.jsonl` still ends at
`claimed 2026-09-02T17:20:37`, so passes two, three and four have all run
against an unanswered question. This pass narrows the three options to **one**
by measurement, and writes out the exact replacement text so the answer is an
approval rather than a decision.

## The wall, unchanged

`prds/a-harness-measures-the-tree-its-worker-built-in/probe/verify.sh` —
`verify: 15 pass, 3 fail, 18 checks`, byte for byte pass three's totals and
pass three's three files. Sections B, C and D are green: they read a fixture
the probe builds and no live file at all.

```
A. every harness on the board takes its root from the runner (76 harnesses)
  FAIL A1 every harness reads ${PEARDE_ROOT:-} prds/every-document-is-written-in-the-writer-s-prose/skills-and-scout-docs-are-rewritten-dense/probe/verify.sh — got: 75 · want: 76
  FAIL A2 every harness walks up to its own .pearde prds/board-rel-is-a-third-wrong-board-path-resolution/probe/verify.sh prds/every-document-is-written-in-the-writer-s-prose/skills-and-scout-docs-are-rewritten-dense/probe/verify.sh prds/every-run-session-works-in-a-worktree-of-its-own/no-destructive-git-runs-in-a-tree-the-session-does-not-own/probe/verify.sh — got: 73 · want: 76
  FAIL A3 no harness counts `..` to reach the repo prds/board-rel-is-a-third-wrong-board-path-resolution/probe/verify.sh prds/every-run-session-works-in-a-worktree-of-its-own/no-destructive-git-runs-in-a-tree-the-session-does-not-own/probe/verify.sh — got: 2 · want: 0
  ok   A4 no harness reaches the repo by an absolute path
verify: 15 pass, 3 fail, 18 checks
```

## What pass four measured that pass three asserted

**1. All three offenders sit in PRDs that are `done`.** This is the fact that
collapses the option set, and it was read off the files rather than assumed:

| offending harness | its PRD's `state:` |
|---|---|
| `every-document-…/skills-and-scout-docs-are-rewritten-dense/probe/verify.sh` | `done` |
| `board-rel-is-a-third-wrong-board-path-resolution/probe/verify.sh` | `done` |
| `every-run-session-…/no-destructive-git-runs-in-a-tree-the-session-does-not-own/probe/verify.sh` | `done` |

Pass three's **option 2** — keep the population assertion and widen this PRD's
footprint by the offenders — is therefore not merely non-convergent. It is
forbidden twice over: "never touch another PRD" in every brief, and
`memos/a-harness-that-reads-the-whole-checkout-is-not-a-harness.md`'s own
`## Alternatives considered`, which rejected editing a closed PRD's file in as
many words. Option 2 is off the table, not merely unattractive.

`two-harnesses-still-name-a-tree-they-do-not-measure` — the PRD the
orchestrator filed to convert pass two's offenders, and which did convert them
— is `claimed`. It was scoped to two files that are now fixed. It does not
cover these three.

**2. The merged-tree verifier is unconvertible, read rather than argued.**
`skills-and-scout-docs-are-rewritten-dense/probe/verify.sh` opens:

```
LANE=${LANE:-/Users/feb/dev/infra/pearde/pearde/.lanes/every-document-…-dense}
MAIN=${MAIN:-9889e78}
cd "$LANE" || exit 2
…
TREE=$(git merge-tree --write-tree "$MAIN" "$REF" 2>/dev/null)
```

It `cd`s to a pinned lane, merges it against a pinned SHA with `git merge-tree
--write-tree`, unpacks the result into `mktemp -d` and measures *that*. There
is no tree for `PEARDE_ROOT` to name: the tree it measures does not exist until
the harness builds it. `A1`'s population holds a member for which the
assertion is not unmet but meaningless. Its `A4` pass is honest, not a miss —
`A4`'s matcher requires the absolute path to be *where a root variable is
assigned*, and line 17 assigns a lane, not a root.

**3. `spec05` box 8 has a second unclosable half, which pass three did not
name.** The box reads:

> `doctor.sh --harnesses` reports this harness among the pinned green ones,
> and its own count of harnesses on the board goes from 59 to 60.

`bash resources/doctor.sh` this pass prints `harnesses  off  76 harnesses`,
and `find pearde/prds -name verify.sh | wc -l` is `76`. The board held 59 when
the spec was written, 69 at pass two, 76 at pass three and 76 now. **Even a
green section A cannot make "from 59 to 60" true**, and no work by anyone can:
the clause pins a census that the board grows past every day. So box 8 is not
one blocked assertion behind one open question — it is two clauses, both
written over a live population, and both dead for the same reason. That is
finding 14 arriving a second time, in the same box, from the other side.

## The one option left, with its text

Pass three's option 3 — a gate refusing a new `probe/verify.sh` with no
preamble — is a real and good PRD, and it does not unblock this one: it stops
the count rising and converts nothing already landed, and the three offenders
are in `done` PRDs that a creation-time gate never sees.

So **option 1 is the only one that converges**, and it is what the board
already decided in a `status: decided` memo:

> A probe's assertions are scoped to files in its own PRD's footprint, or to a
> fixture the probe itself built. **A probe never asserts on the state of the
> live working tree.**
> — `memos/a-harness-that-reads-the-whole-checkout-is-not-a-harness.md`

and what step 5 of this route says in its own words: *no command's exit may be
decided by a file outside the footprint; a repo-wide command may be captured
and printed, and may fail only on the lines of its output naming a footprint
path.*

I may not make the edit — "do not guess, do not redefine the spec" — so here
is the exact text an orchestrator edit would put in `specs/spec05.md`, so the
answer is one approval. Two boxes change; nothing else in the spec moves, and
no check is weakened: sections B, C and D already prove the mechanism on
fixtures the probe builds, and they are green.

Box 2, replacing *"every harness on the board … with no exception list"*:

> It asserts every harness named in the `footprint:` of `spec01`, `spec02` and
> `spec04` reads `${PEARDE_ROOT:-`, walks up to its own board, counts no `..`
> and holds no absolute root — 59 files, the population this PRD converted. It
> **prints** the board-wide census beside that, naming every harness on the
> board that lacks the preamble, and the census decides nothing.

Box 8, replacing *"its own count of harnesses on the board goes from 59 to
60"*:

> `doctor.sh --harnesses` reports this harness among the green ones, and its
> own census line names this harness among the harnesses on the board.

With those two lines the PRD closes on the next pass: section A becomes a
59-file footprint assertion that is green today, the census stays visible as
the finding it is, and box 8 stops pinning a number the board outgrows.

**The question, one line:** may `spec05`'s boxes 2 and 8 be rewritten as
above — a footprint assertion plus a printed census — or must this PRD keep an
acceptance box whose colour is decided by whoever committed to the board last?

## Boxes, by spec — every block re-run this pass

Each block awked out of its fence and run under `bash -e -o pipefail`, the
pair `collect.py` passes to `run`. None of these is inherited from pass three.

| spec | block exit | boxes |
|---|---|---|
| `spec01` | **0** | 6 of 6 |
| `spec02` | **0** | 5 of 5 |
| `spec03` | **0** with the lane's two footprint files substituted; **1** verbatim | 6 of 6 |
| `spec04` | **0** | 6 of 6 |
| `spec05` | **1**, on its first line | 7 of 8 |

- `spec01`: `spec01 census over 32 harnesses: 0 offending`, then
  `root-probe: 6 passed, 0 failed`.
- `spec02`: `spec02 census over 26 harnesses: 0 offending`, and
  `one-definition-of-the-board-not-two` still prints its pinned `20 checks`.
- `spec03`: `spec03: 0 offending`. Its two footprint files are uncommitted in
  the lane, so the block was run twice per step 5 of this route. Verbatim
  against the checkout it exits **1** — that is the red-to-green flip shown
  against the tree that does not hold the build, stronger than `git show
  HEAD:`. Substituted to the lane's `resources/doctor.sh` and
  `references/parts/workers.md` it exits **0**, and its fixture sweep printed
  both halves of the last box:

  ```
  .pearde/prds/one/probe/verify.sh — exit 1 · root=/tmp/named-by-the-runner
  .pearde/prds/one/probe/verify.sh — exit 1 · root=/var/folders/…/tmp.TAp6idjZPt/proj
  ```

  An already-set `PEARDE_ROOT` reaches the harness; with none set the root is
  the board's own repo. The lane's `doctor.sh` carries
  `HROOT="${PEARDE_ROOT:-$(cd "$BOARD/.." && pwd)}"` at line 918 and
  `PEARDE_HARNESSES=1 PEARDE_ROOT="$HROOT" bash "$h"` at line 924. The two
  workflow files this spec also names were committed into the board repo by a
  sibling between pass three and now — the board's `workflows/` is clean and
  the block still finds `PEARDE_ROOT` in both, so this spec's claim on them
  stands and nothing of it is left uncommitted.
- `spec04`: `e14-probe: 5 passed, 0 failed`, `ok E14 no scratch index is left
  behind` while a sibling held `/tmp/pearde-index-sibling-probe`, and the
  harness still prints its pinned `85 checks`.
- `spec05`: the block's first line is this PRD's harness, which exits 1, so
  under `-e` the block ends there.

**Box 7 (the `HCAP=4` / `HCAP=1` sweep pair) was not re-run, and that is now a
finding rather than a saving.** It stands on pass one's four sweeps and pass
two's four more. Re-running it cannot close box 8, costs about seven minutes of
wall clock, and — this is the part worth recording — pass two measured the
board's failure set as *unstable run to run with the doctor held fixed*, two
runs of one command over one tree differing by two harnesses. So box 7 is a
**second** acceptance box on this PRD written over the live population, with
the same defect as box 2 and the same cure. The proposed edit above does not
cover it; whoever answers the question should answer for box 7 in the same
breath.

## The baseline, and the gates

Taken before anything this pass ran. This pass wrote no file but this report.

- `probe/verify.sh` — `verify: 15 pass, 3 fail, 18 checks`.
- `python3 resources/index.py check` — **exit 1, one line**:
  `references/language.md references @references/personas/writer.md — not on
  disk`. Outside every footprint here; inherited, and the same single line
  pass three recorded.
- `bash resources/doctor.sh` — exit 1, three broken rows, all outside this
  footprint and all before the first command of this pass: `index` (the line
  above), `origin` (*33 derived · 1 with no from:*), `knowledge` (*graph.json
  is behind the files: 260902-4f91, 260902-aae0*). `briefs ok`, `workflows
  ok`, `harnesses off · 76 harnesses`, `board ok · 144 PRDs`.
- HEADs, unmoved start to end: checkout `31620bb`, board `e018609`, lane
  `8bbb4c1`. Pass three ran at checkout `ba69efa`; the checkout has taken
  twenty-odd commits since and the wall did not move.
- `git status --short`, start and end alike: checkout ` M
  references/system.md` (finding 16 of pass three — a sibling's, still
  uncommitted and still nobody's here); board `?? prds/a-harness-measures-the-
  tree-its-worker-built-in/` and nothing else of this PRD's, the two workflow
  files having been committed by a sibling; lane ` M
  references/parts/workers.md`, ` M resources/doctor.sh`.
- Health: `none under the floor` — nothing owed on this PRD's footprint.

## Findings

Findings 1, 4, 5, 7, 8, 9, 10, 11, 12, 13 and 15 from the earlier passes stand
unchanged and are not restated. Finding 13's claim is now measured rather than
asserted — see *What pass four measured*, item 2. Finding 14 is confirmed and
extended below.

**14 (extended). The population is a random walk, and every offender lands in
a `done` PRD.** 59 → 69 → 76 → 76 harnesses across four passes. Pass two's two
offenders were routed and fixed; three new ones landed while that was
happening, and all three belong to PRDs already `done`. So each pass of this
PRD faces a fresh set of files it is forbidden to touch, filed by PRDs already
closed. An acceptance box over this population cannot converge by construction,
and no amount of routing helps, because routing is slower than the board grows.

**17. `spec05` box 8 pins a census that the board outgrows.** Detailed above.
The general form: an acceptance box that names a **literal count of a live
population** — "from 59 to 60" — is dead the moment the population moves, and
unlike a red check nobody can tell from the file whether it was ever true. This
is the same class the route's step 5 `## Fails when` already names for a
probe's own total (*a floor is honest; an equality is a wall*), arriving
through a spec's acceptance box instead of through a harness.

**18. `nothing-left-open/the-line-tells-the-truth` widened from 36 failures to
41.** Pass three recorded *36 of 85 checks* failing on the orchestrator's
checkout, all `PEARDE_AS` and `--force`, and named it a sibling's regression.
`spec04`'s block captured it again this pass: `verify: 85 checks · 44 pass · 41
fail`. Five more checks went red between 09:06 and now. It is captured, printed
and does not gate `spec04`, which exits 0 — but somebody's regression is
spreading in the shared checkout and nothing on the board is watching it.

**19. The machine's temporary filesystem filled during this pass.** Four
consecutive commands died with `ENOSPC: no space left on device` writing the
tool's own output file under `/private/tmp`, including one whose only job was
to free space; `df` afterwards read `416Gi used of 460Gi · 100% · 2.7Gi free`.
Every measurement quoted above was taken before that point and none is
affected — the run recovered and the closing `git status` was re-taken. This
PRD's blocks build fixtures under `mktemp -d` with `EXIT` traps and several run
whole `doctor --harnesses` sweeps, so they are plausible contributors alongside
every parallel lane; nothing here identifies the filler. A board running
several lane sessions at once, each sweeping seventy-odd harnesses into
temporary trees, has no accounting for temporary space at all, and a worker
that hits this loses its tools mid-run with no diagnosis available — a contract
for someone.

## Workflow probe-then-spec

| # | step | outcome |
|---|---|---|
| 1 | `read-the-contract` | done — the PRD, five specs, pass three's `report.md` (its `## Fails when` row for a report path that already holds one was obeyed: the findings are carried forward by name), and the decided memo the wall turns on. `git status --short` recorded in all three roots before the first command |
| 2 | `capture-the-harness-baseline` | done — this PRD's harness, `index.py check`, `doctor.sh`, and all three HEADs, before anything ran. Its `## Fails when` row for an inherited red fired twice: `index.py check`'s one line and doctor's three broken rows are all outside the footprint and all named |
| 3 | `attempt-the-build` | **not entered.** Its first `## Fails when` row applies — the specs exist and the build stands. Every spec's footprint was checked with `git status` and `git diff` first; none was clean-but-unbuilt. No flip is claimed that pass one did not earn |
| 4 | `re-run-the-harnesses` | done — every spec's block re-run this pass under `bash -e -o pipefail`, `spec03` both verbatim and substituted. No harness was edited. Its row for a count that *rose* fired on finding 18: `the-line-tells-the-truth` moved 36 → 41 failures on a file nobody here touched, quoted and not chased |
| 5 | `write-the-specs` | **not entered** as authoring. Its `## Fails when` table was applied to the blocks that stand, and it is that table — *no command's exit may be decided by a file outside the footprint* — that produced the wall. Pass three's proposed row for this table stands unchanged and is not repeated |

### Edits

Pass three proposed one row for `write-the-specs`'s `## Fails when`, covering
an acceptance box that contracts an assertion over "every `<thing>` on the
board". That row stands as written and is not repeated here. This pass hit its
sibling — a box pinning a **literal count** of a live population — which the
same row does not cover, because such a box names no population and reads as a
perfectly ordinary before-and-after number. Proposed second row for
`write-the-specs`'s `## Fails when`:

| an acceptance box names a literal count of something the board holds — "the count goes from 59 to 60", "all 32 files", "the set is 6" | the number was true at spec-writing time and the board has grown since; the box is now unclosable, and unlike a red check nobody can tell from the file whether it was ever true | write the box as a **relation** the count cannot outgrow — *this harness appears in the census*, *every file in this spec's `footprint:` carries the preamble* — and put the literal number in the spec's prose, where it dates the writing instead of gating the work. A count in a box is only safe over a population the spec's own `footprint:` closes |

The route otherwise said exactly what to do at every step; nothing else
misfired.

## No word was missing

`grammar.py show` covers every term the contract uses. Nothing was learned
outside this repo, so nothing was written to `knowledge.py`.
