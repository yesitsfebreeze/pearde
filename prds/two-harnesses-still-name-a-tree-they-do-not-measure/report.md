# two harnesses still name a tree they do not measure — implementer

Verdict: DONE

One spec, seven boxes, all seven ticked against output quoted into the box and
re-measured this pass. `spec01`'s `## Verify and Proof` block, run the way
`collect` runs it (`bash -e -o pipefail`), exits **0**. This PRD's probe reports
`probe: 16 passed, 0 failed`.

This is the route's **third** pass on the PRD: the analyst built the four
harnesses and wrote the spec, an implementer ticked the boxes, and this pass
re-measured every one against a tree that moved overnight. Steps 3 and 5 were
not entered — the build stood in the board repo before my first command.
**I claim no flip:** every red-to-green on this tree was earned by the pass that
built it, and one count that rose since is a neighbour's landing, named below.
My own edits are box 6's evidence line in `specs/spec01.md` and this file.

## What was run

| | |
|---|---|
| board | `/Users/feb/dev/infra/pearde/pearde` (its own repo; `HEAD e018609` at start, was `0a84af1` at the previous pass) |
| checkout | `/Users/feb/dev/infra/pearde` (`HEAD 31620bb`; ` M references/system.md`, not mine) |
| lane | `.lanes/two-harnesses-still-name-a-tree-they-do-not-measure` — holds `pearde/graphify` and `.pearde/graphify` and **no board**, so no footprint path exists in it at any depth. All work is in the board repo, which is where `spec01`'s block `cd`s. |
| footprint | four of five **untracked** in the board repo; the ledger harness is now **tracked**, committed by its own PRD at `f0a443d` with the preamble intact |
| probe | exit `0`, `probe: 16 passed, 0 failed` |
| verify block | exit `0` under `bash -e -o pipefail` |
| `index.py check` | exit `1`, one row: `references/language.md references @references/personas/writer.md — not on disk`. Outside the footprint, inherited, unchanged since the previous pass. |
| `doctor.sh` | exit `1`: `index broken` (the row above), `origin broken — 33 derived · 1 with no from:`, and **new since the previous pass** `knowledge broken — the research layer does not check out`. All three outside the footprint, all inherited. |
| board dirty-file count | `259` before the runs and `259` after — the block and the probe write nothing under the board |

## Boxes

Each box carries its own quoted output in `specs/spec01.md`. Re-measured here:

1. **board walk** — `grep -cF 'basename "$BOARD"'` prints `1` for each of the four.
2. **`${PEARDE_ROOT:-`** — `1` for each; the line is
   `ROOT="${PEARDE_ROOT:-$(dirname "$BOARD")}"` in all four, still at lines
   16, 21, 22, 28.
3. **no `..` walk, no absolute root** — the four print `0` and `0` for both
   greps. The census's `A3`, which read the fifth footprint file's quoted plant
   as a walk, has been re-anchored by its own PRD — see the findings.
4. **the session harness is red honestly** — from the checkout: exit `10`,
   `verify: 10 FAIL`, five `ModuleNotFoundError: No module named 'sessions'`.
   Under `PEARDE_ROOT=<board>/.lanes/every-run-session-works-in-a-worktree-of-its-own`,
   which does hold `resources/board/sessions.py`: exit `0`, `verify: green`.
   `resources/board/sessions.py` is still absent from the checkout, so the box's
   two trees are still the two trees it names.
5. **each of the four reads the runner's tree** — three print the scratch path
   back in their own header line (`— tree …/impl-two-pass2/fake`); the session
   harness prints no tree line and its evidence is box 4, unchanged.
6. **the three counts** — two unmoved (`probe: 20 passed, 1 failed`,
   `probe: 3 passed, 20 failed`); the ledger's rose. See below.
7. **the probe** — exit `0`, `16 passed, 0 failed`; `C1`–`C4` each name the
   defect they saw and `C5` shows the copied-from file unchanged. The board's
   dirty-file count is identical either side of the run.

Box 5's evidence remains weaker for the session harness than for the other
three, for the reason the previous pass gave: it prints no tree line, so a
scratch tree without `sessions.py` and the board's own repo produce the same
`ModuleNotFoundError`. Its tree-sensitivity is proven by box 4 instead.
Narrowing that is the parent PRD's census work, not this unit's.

## Findings

### The ledger harness went green, and the rise is not this unit's

`prds/every-run-session-works-in-a-worktree-of-its-own/a-session-ledger-names-who-holds-what-and-reaps-what-is-gone/probe/verify.sh`
printed `PROBE RED — 1 failure(s)` at both earlier passes and prints
`PROBE GREEN` — `29 passed, 0 failed` — now. A count that rose is the same
evidence as a count that dropped: the tree moved.

It is the neighbour's, measured two ways. The harness reads
`$ROOT/resources/board/session.py`; that file's last commit in the checkout is
`31620bb` at `2026-09-02 23:45`, and the harness's own file has not been
touched since `22:03`, before the previous pass ran it. A harness unmoved and
an input written after the count was taken puts the difference outside this
unit entirely.

Box 6 is the one edit this pass made to the spec: its quoted output now names
what the block prints, and says which of the three moved and why. Leaving the
old count in the box would have left a number in an acceptance box that its own
command contradicts.

### The census's `A3` has been repaired — the previous pass's finding is closed

The previous pass reported `A3` of
`prds/a-harness-measures-the-tree-its-worker-built-in/probe/verify.sh` red on
this PRD's own probe, because its matcher read a walk carried inside a `sed`
spell as a walk in code, and proposed anchoring it on a root **assignment** the
way `A4` already was. That harness was rewritten at `09:02` today and now reads

```sh
grep -qE '^[[:space:]]*([A-Za-z_]*(ROOT|REPO|CODE|R|BOARD)[A-Za-z_]*=|cd[[:space:]]).*/\.\./\.\./\.\.' "$h"
```

with the reason written above it, citing `nothing-left-open/a-quoted-walk-is-data`.
`A3` no longer names this PRD's probe. Nothing is owed on this finding.

### The population census still cannot close — the harness set is 76 now

`A1`, `A2` and `A3` are red at `got: 75 · want: 76`, `got: 73 · want: 76` and
`got: 2 · want: 0`, naming three files this PRD never touched:
`…/skills-and-scout-docs-are-rewritten-dense/probe/verify.sh`,
`…/board-rel-is-a-third-wrong-board-path-resolution/probe/verify.sh` and
`…/no-destructive-git-runs-in-a-tree-the-session-does-not-own/probe/verify.sh`.
The population was 69 when this PRD's analyst started, 72 at the previous pass
and `76` now (`find prds -name verify.sh | wc -l`). Four harnesses fixed and
seven born unrooted since. The structural finding stands and has now been
confirmed a third time: **there is no way on this board for a harness to be
born rooted.** Routing *a harness is born rooted* — a template plus the prose
pointing at it — as its own contract is the only thing that closes the census,
and it is the orchestrator's call.

### `PEARDE_ROOT` is read in the checkout now, and still set by nothing

Refined from the previous pass. `grep -rn PEARDE_ROOT resources/ references/`
over the checkout no longer returns nothing: two committed invariant scripts
read it (`resources/invariants/a-board-s-own-file-commits-in-the-board-repo.sh:53`
and `…/no-destructive-git-runs-in-a-tree-the-session-does-not-own.sh:40`). But
nothing **sets** it. The harness sweep in `resources/doctor.sh:915` is still

```sh
( PEARDE_HARNESSES=1 bash "$h" </dev/null >"$HTMP/out.$ji" 2>&1; echo $? > "$HTMP/rc.$ji" ) &
```

with no `PEARDE_ROOT` on it, so all 76 rooted harnesses still fall back to the
board's own repo under the sweep, and the mechanism this PRD conformed four
files to is exercised today only when a person types the variable. The runner
that names the tree still lives only in
`a-harness-measures-the-tree-its-worker-built-in`'s lane. That PRD's business,
unchanged.

### One harness was measuring the lane, and pass one took that away

Carried forward unchanged and not re-litigated:
`…/every-module-finds-its-siblings-by-one-rule/probe/verify.sh` preferred `$PWD`
and was the one harness that measured a worker's lane unassisted. Conforming it
to the board's one rule costs that until the runner above lands. It is a
four-line revert if the call was wrong.

### A verify block that plants a defect must plant it on a copy

Carried forward. The probe does the whole experiment on copies under `$TMPDIR`
and asserts it as `C5`; confirmed again this pass by the board's dirty-file
count being identical either side of the run. Nothing to add.

### Four files are untracked and must be staged whole — one has already landed

Of the five footprint files, the ledger harness is now tracked: its own PRD
committed it at `f0a443d`, preamble intact, so this unit's edit to it has
landed inside a neighbour's commit. The other four are still `??` in the board
repo, three of them inside other PRDs' directories whose lanes are live, so
`collect` must stage them whole rather than by hunk. I did not `git add` them:
staging into an index shared by every session on this board risks a neighbour's
commit sweeping them up, and committing is not the implementer's act.

## Knowledge and grammar

Nothing was learned from outside this repo, so nothing was written back with
`knowledge.py remember`. No word in the contract was missing from
`grammar.py show`.

## Workflow probe-then-spec

| # | atomic | verdict | note |
|---|--------|---------|------|
| 1 | `read-the-contract` | ok | `prd.md` is still the placeholder template; the contract is `specs/spec01.md` and the previous pass's `report.md`. Both shapes are now rows in the atomic, added by the previous pass. The lane holds no board — also a row now. |
| 2 | `capture-the-harness-baseline` | ok, with one shape the table does not carry | baseline taken before the first edit: probe, the three counts, `git status --short` in both roots, both HEADs, `index.py check` and `doctor.sh` recorded red **before the first edit**. The shape the table lacks is below. |
| 3 | `attempt-the-build` | not entered | the second-pass row applies verbatim: the specs exist and the build is in the tree. No rebuild, no flip claimed. |
| 4 | `re-run-the-harnesses` | ok | every recorded harness re-run with the same command line. One count rose; attributed to `31620bb` by the harness's mtime against its input's commit date, per the `count went up` row. |
| 5 | `write-the-specs` | not entered | same row: the spec exists; my act on it is one box's evidence line, re-quoted from output I ran. |

### Edits

One shape the atomics do not carry. A replacement row, for the workflow's
owner — I edited no workflow file. The previous pass's three edits are in this
file's history and all three have since landed in the atomic.

**1 — `re-run-the-harnesses`, `## Fails when`: the box, not only the report,
holds the stale count.** The `a count went up` row tells a worker to quote both
counts in the **report** and name the file that explains the rise. On a second
or third pass the number is also sitting inside an already-ticked acceptance
box, where the box's own command now contradicts it, and the row says nothing
about that. Add:

| seen | means | do |
|------|-------|----|
| a count named inside an already-ticked acceptance box is not what the box's own command prints now, and the difference is a neighbour's landing | the box was ticked honestly against the tree of an earlier pass; a number in a box is quoted output, and quoted output that its command contradicts is worse than no number | re-quote the box against what the command prints now and say **inside the box** which count moved and whose landing moved it. Do not untick it — the box's claim is about this unit's work, and that claim still holds; and do not leave the old number standing, because the next reader checks the box by running its command |

## Scores

complexity: 8
blast-radius: mid
workflow: probe-then-spec
