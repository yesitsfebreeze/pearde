# four-stale-self-tests-are-re-aimed-at-the-code-that-moved — implementer report

Verdict: DONE

16 of 16 acceptance boxes closed across four specs, every one re-run against the
tree as it stands and quoted below. This was the route's **second** pass: the
analyst built the re-aims and they were in the tree when I arrived, so
`attempt-the-build` had nothing to build, and every red-to-green flip below was
earned by pass one and is claimed for it, not for me. What this pass added is
proof under the shell `collect` actually uses.

**This report is the second write.** The first was refused at collect —
`spec03 exit 1 — nothing written` — and the refusal was correct. The diagnosis
and the repair are in "Why collect refused" below.

## The five harnesses, run individually, never through a sweep

| harness | this pass | exit |
|---|---|---|
| `one-page-that-says-whats-up` | `31 checks · 31 pass · 0 fail` | 0 |
| `seven-closed-probes-drifted-red/the-fixtures-meet-the-tool` | `35 checks · 31 pass · 4 fail` — **its parse-cache row is ok**; all four reds are neighbours', named in Findings 3 and 8 | 1 |
| `the-board-runs-itself/collect-is-a-command` | `133 checks · 133 pass · 0 fail`, both R rows ok | 0 |
| `the-board-runs-itself/init-asks-nothing` | `89 checks · 89 pass · 0 fail`, both J rows ok | 0 |
| `workflows-on-the-board/workflow-improve` | `71/71 checks pass`, the re-aimed row ok | 0 |
| `the-collect-and-brief-harnesses-are-carried-across-the-layou` (downstream, not edited) | `7 checks · 7 pass · 0 fail` | 0 |

`init-asks-nothing` read **88** on my first pass and reads **89** now. That is
Finding 12: a neighbour added a check to it between the two runs.

Neither `resources/board/render.py`, `resources/board/view.css` nor
`references/parts/workers.md` was touched: `git diff --name-only` names none of
the three as this PRD's change (`view-files-moved=0`, `workers-moved=0`).

## Why collect refused, and what changed

`collect` ran spec03's block and got exit 1 while every harness inside it was
green. The cause was one line of mine:

```
grep -c '^88 checks · 88 pass · 0 fail'      →  init=0
```

Between the run that wrote that number and the collect that read it, another
session added `eq "A settings.md · happiness" …` to
`prds/the-board-runs-itself/init-asks-nothing/probe/verify.sh` — a **shared
board file**, one of this PRD's own footprint paths, edited at 10:50 by a
session working on a `happiness:` setting. The harness went 88 → 89, still
`0 fail`, still exit 0. My block pinned the denominator, so a neighbour adding a
*passing* check reddened this PRD.

That is precisely the disease this PRD exists to cure — a self-test pinned to a
number the code was allowed to move — reproduced inside the PRD that cures it.

**The rule now applied to all four blocks: nothing gates on a count another
session can move.** Each block asserts, in its place:

- **the harness is green as a shape, not as a number** — the tally line is
  parsed and `checks == pass && fail == 0` is required, so a neighbour's added
  passing check cannot redden it and a neighbour's added *failing* check still
  can;
- **this PRD's own re-aimed rows read ok in the output**, by their titles;
- **those rows stand in the harness file itself**, exactly once each — which is
  the "re-aimed in place, not added beside" claim, and it is scoped to a
  footprint file rather than to a board-wide census;
- **the retired needle is gone** from that same file;
- **the non-vacuity mutation**, on scratch text or in a `mktemp -d`, never
  against a real file.

No check was weakened to get there. Every gate was shown to fail on the failing
shape:

```
tally on '35 checks · 31 pass · 4 fail'   -> 35/31 fail=4 red
tally on '133 checks · 133 pass · 0 fail' -> 133/133 fail=0 green
all-pass on 71/71 = 1   on 70/71 = 0
R-rows with both ok = 2   with one FAIL = 0
```

Two portability defects were repaired in the same pass. `grep -oE
'^([0-9]+)/\1 checks pass$'` is an ERE **backreference**: BSD grep here accepts
it, ugrep refuses it outright with `invalid escape`, and POSIX does not have it
— replaced with a `re.match` on the two captured numbers. And spec03's row
counts used `\|`, GNU BRE alternation that BSD BRE does not have — switched to
`grep -cE` with a real `|`.

## Per-spec box status — all re-run under `bash -e -o pipefail`

```
BLOCK01 exit=0   BLOCK02 exit=0   BLOCK03 exit=0   BLOCK04 exit=0
```

each extracted as `awk '/^```sh/{f=1;next} /^```/{f=0} f' <spec>` and run as
`bash -e -o pipefail <that file>`, which is how `collect.py:1057` runs them.

**spec01 — 4/4.**
`tally=31/31 fail=0 green drawer-rows=1 height-rows=1 view-files-moved=0`, and
the mutations on scratch text: `drawer live=True mutated=False | height
live=True mutated=False`. Both checks go red on the mutation.

**spec02 — 3/3.**
`row-ok=1 row-red=0 in-place=1 spent-non-goal=0 ignore-live=1
ignore-without-the-line=0`. The harness prints `exit=1` and four `FAIL` rows
inside this block and the block still exits 0 — **that is asserted, not
survived**. The block gates on this PRD's own row (`row-ok=1`), on no failure
naming it (`row-red=0`), on the re-aim standing once in the harness file
(`in-place=1`), on the spent non-goal being gone (`spent-non-goal=0`) and on
the ignore line reading 1 live and 0 with it stripped. The four reds are
printed for the reader and gate nothing, because all four are board-wide: two
census every harness on the board, one re-runs a neighbouring harness, and one
reads the whole working tree's `git diff` of two files a live session holds.

**spec03 — 5/5.**
`collect=133/133 fail=0 green init=89/89 fail=0 green downstream=7/7 fail=0
green`, `R-rows=2 J-rows=2 in-C=2 in-I=2 dead-path=0,0 downstream-edited=0`,
and the non-vacuity in a `mktemp -d`:
`find 0->1: 0 -> 1 | sentinel: absent -> 2192966820 2`. The silent sibling is
no longer empty-versus-empty: creating the file flips `absent` to a checksum,
which is the failure the check exists to catch.

**spec04 — 4/4.**
`all-pass=1 row-ok=1 in-place=1 dead-needle=0 workers-moved=0 sentence-live=1
sentence-gone=0`. I re-read `references/parts/workers.md` on HEAD before
touching anything: `bca8a0c` rewrote it, and the sentence the check reads —
"…is the belief and the `## Workflow` rows, as above." — still stands, now at
line 339, closing the shared return paragraph under the implementer brief
block. The check needed no re-aim.

## Three acceptance boxes were re-aimed, and why that is not a weakening

Three boxes named a denominator as the thing to check: "31 checks", "88 checks,
88 pass", "71/71". Two of the three are numbers a neighbour may move without
touching anything this PRD owns, and one of them **did** move mid-run. Each was
re-aimed at the shape that still meets the box's own sentence — every check
passing, 0 fail, exit 0, and this PRD's own rows ok — with the observed number
quoted in the box for the reader. spec02's "the harness's own total still reads
35 checks" was re-aimed the same way, to the claim it was actually making: the
re-aim was made **in place** rather than added beside, which is now measured on
the harness file itself.

This is the route's own instruction for a check that reddens on a change the
contract did not make, and it is the PRD's thesis applied to the PRD: a gate
pinned to a number nobody promised to hold is a gate that teaches you to skim
past reds.

## Findings — carried forward and new

1-6 are pass one's, carried by name; 7-11 are this pass's first run; 12-13 are
this run's. None is fixed here.

1. **The PRD cites two paths that do not exist.** `resources/view/render.py:459`
   and `resources/view/view.css:508` — there is no `resources/view/`. The files
   are `resources/board/render.py` and `resources/board/view.css`, and both line
   numbers are correct there. The specs already spell the right paths.
2. **Three more harnesses carry the same dead `REG` path, vacuously green.**
   `seven-closed-probes-drifted-red/init-seeds-a-board-doctor-calls-green:33`,
   `the-tool-keeps-its-word/collect-keeps-its-word:320` and
   `the-board-runs-itself/the-next-line-runs:16`. Not this PRD's contract —
   widening it is REFINE. The fix is spec03's two-line shape, copied.
3. **`the-fixtures-meet-the-tool`'s F row is not isolated from other sessions.**
   It reads the whole working tree's `git diff` of `resources/board/plan.py` and
   `resources/board/init.py`. `init.py` is dirty with 62 added lines —
   `GRAMMAR_PY`, `grammar_file()`, `plant_grammar()` — the grammar session's
   work. Contention; spec02 box 3 says so and the box closes.
4. **The tree moved under this run, hard.** Baseline HEAD `9df1035`, board HEAD
   `17f32ae`, 16 dirty repo paths; by the end 20, with
   `resources/board/collect.py`, `resources/board/serve.py`,
   `resources/doctor.sh`, `resources/scout/routes.md` and an untracked
   `resources/board/ramp.py` added mid-run, plus five new untracked PRDs on the
   board. None is mine.
5. **Nothing was learned outside this repo**, so nothing was written back with
   `knowledge.py remember`.
6. **Trap 2 confirmed, untouched.** `init-seeds-a-board-doctor-calls-green`'s
   `D doctor exits 0` is the port-race at its `probe/verify.sh:35`.
7. **spec04's re-aim was already committed, not uncommitted.** The spec's prose
   says "this analyst's uncommitted pass one", but
   `git -C .pearde log -- prds/workflows-on-the-board/workflow-improve/probe/verify.sh`
   ends at `342ba5e`, the check is byte-identical to that commit, and
   `git diff 342ba5e -- <that file>` is empty. The check is right and green;
   only its provenance is wrong.
8. **One neighbour harness reddens three rows in two others.**
   `.pearde/prds/a-session-start-brings-the-board-up/probe/verify.sh` — an
   untracked PRD another session dropped mid-run — is the only harness on the
   board whose last three lines carry no exit-code-carrying check. It is the
   whole cause of `the-fixtures-meet-the-tool`'s `C every harness on the board
   ends on an exit-code-carrying check` (`got [52] want [53]`), its `C the-gate's
   census row is green`, and its `E …and the-gate fails only the two rows that
   read index.py check` — because `the-gate-runs-the-harnesses` fails exactly
   one row, `J every harness on this board ends on a test that carries its exit
   code — got: 52 · want: 53`, and nothing else (`57 checks · 56 pass · 1 fail`).
   Three reds, one cause, in another session's file.
9. **`python3 resources/index.py check` exits 1 on a file that is not mine.**
   Both lines name `resources/board/ramp.py` — untracked, mtime 10:46, absent
   from my baseline `git status`. `index.py check 2>&1 | grep -cv ramp` is `0`:
   no other line. This PRD's footprint is entirely under `.pearde/prds/`,
   outside the manifest scan.
10. **The downstream harness is flaky under concurrent sessions.** First run
    `7 checks · 6 pass · 1 fail`, the red being `collect-keeps-its-word — got:
    101 checks · 88 pass · 13 fail` **from the code repo root**, while the same
    suite by absolute path from `/` in that same run read `101/101`. Run alone
    immediately after: `101 checks · 101 pass · 0 fail`; downstream re-run:
    `7 checks · 7 pass · 0 fail, exit 0`, and green on every run since. That is
    scheduling, not code. It belongs with the harness-run PRD, beside trap 2's
    port race.
11. **`bash resources/doctor.sh` was not run at baseline or after.**
    `resources/doctor.sh` is another session's uncommitted file this whole run,
    and doctor's own probe writes state under `resources/board/state/guard/`.
    `index.py check` stands as the repo gate, and Finding 9 accounts for it.
    The skip is recorded rather than hidden — the same skip pass one recorded.
12. **A neighbour edited one of this PRD's footprint files mid-run.**
    `prds/the-board-runs-itself/init-asks-nothing/probe/verify.sh` now carries,
    on top of pass one's uncommitted re-aim, a foreign hunk adding
    `eq "A settings.md · happiness" "$(fm a happiness)" "0"` and extending the
    `D every other line byte-identical` fixture with `happiness: 0`. The two
    edits are far apart in the file and disjoint, so nothing merged and nothing
    of pass one's was lost — but that file now holds two sessions' uncommitted
    work and whoever commits it takes both. Named so the orchestrator can split
    the commit rather than discover it.
13. **A shared board file with a pinned denominator is a board-wide race.** The
    census in `the-fixtures-meet-the-tool` and `the-gate-runs-the-harnesses`
    (`52 want 53`), the `35 checks` total, and my own `88 checks` all broke the
    same way: a count over files several sessions write, asserted as a
    constant. Findings 8 and 3 are the same defect in other people's harnesses
    as Finding 12 was in mine. Worth a PRD of its own — a census assertion
    should name what it expects to find, not how many things it expects to
    count — but it is not this contract's, and every one of those harnesses is
    somebody else's file.

## What this pass wrote

Only four files, all inside this PRD:

```
.pearde/prds/four-stale-self-tests-.../specs/spec01.md
.pearde/prds/four-stale-self-tests-.../specs/spec02.md
.pearde/prds/four-stale-self-tests-.../specs/spec03.md
.pearde/prds/four-stale-self-tests-.../specs/spec04.md
```

boxes ticked, three re-aimed, and all four `## Verify and Proof` blocks
rewritten. The five harness files in the footprint carry pass one's uncommitted
hunks — and, in one case, a neighbour's — and not one byte of mine. Nothing was
staged and nothing was committed.

## Workflow probe-then-spec

| # | atomic | ran | outcome |
|---|---|---|---|
| 1 | `read-the-contract` | yes | PRD, four specs and pass one's report read; `git status --short` recorded in both roots before the first command, HEAD `9df1035`, board HEAD `17f32ae`. `references/parts/workers.md` re-read on HEAD after `bca8a0c` — the sentence spec04 aims at still stands |
| 2 | `capture-the-harness-baseline` | yes | all five harnesses plus `the-gate-runs-the-harnesses` and `collect-keeps-its-word` run and saved whole, one file per harness, before the first edit |
| 3 | `attempt-the-build` | **not entered** | the route's own row: second pass, specs exist, build in the tree. Nothing rebuilt, no flip claimed |
| 4 | `re-run-the-harnesses` | yes, twice | every count accounted for. The second re-run caught `init-asks-nothing` moving 88 → 89 under a neighbour's hand, which is Finding 12 and the reason collect refused |
| 5 | `write-the-specs` | **partly** | no spec written. The four `## Verify and Proof` blocks rewritten so they survive `bash -e -o pipefail` and gate on nothing a neighbour can move; three acceptance boxes re-aimed off a pinned denominator onto the shape their own sentence names |

### Edits

None to the workflow files. Every failure this pass hit was already a row in an
atomic's `## Fails when` — the `grep -c` that exits non-zero on its passing
value, the `&&…||` pair that cannot fail, the board-wide command whose exit
becomes the block's, the second-pass row that says not to rebuild, and
`re-run-the-harnesses`'s own row for a check that reddens on a change the
contract did not make. The atomics were right; the specs were wrong.

Two observations for whoever owns the library, neither an edit:

1. `write-the-specs` step 7 ends on `pearde specced <prd> --check`, and that
   gate does not run the blocks. All four blocks here were accepted by the
   analyst's pass and all four would have aborted under `collect`. The
   `## Fails when` row already prescribes the check —
   `bash -c "set -o pipefail; $(awk …)"` — but as a remedy after a refusal
   rather than as a step before the gate, and its recipe uses `set -o pipefail`
   alone where `collect` uses `bash -e -o pipefail`. `-e` is what killed three
   of these four blocks, and the row's own recipe would have passed all three.
2. Nothing in `write-the-specs` says a block must not gate on a number a
   parallel session can move. `re-run-the-harnesses` has four rows about
   reading someone else's count; the specs' own blocks need the same rule, and
   on a board with three live sessions it is the difference between a block
   `collect` can run and one that passes only when nobody else is working.
