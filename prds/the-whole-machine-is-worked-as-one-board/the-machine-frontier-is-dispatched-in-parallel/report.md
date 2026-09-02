# the-machine-frontier-is-dispatched-in-parallel — implementer report

Verdict: DONE

Pass two on this PRD. The analyst's pass built the dispatcher under `probe/`
and wrote the five specs; this pass **moved it into the footprint** and made
the command real. `pearde machine dispatch` now exists, runs from a directory
with no board above the cwd, and dispatches across eleven boards.

- 43 of 43 acceptance boxes ticked, across `specs/spec01.md` … `specs/spec05.md`
- `probe/verify.sh` **18 of 18 · PASS** (13 fixture cases + 5 rows against this repo)
- every spec's `## Verify and Proof` block exits **0** under `bash -e -o
  pipefail`, and each carries `set -e -o pipefail` of its own so it cannot be
  run any weaker way
- `doctor` rows identical to the pre-edit baseline; `health` 61 for the new
  file, nothing in the footprint under the floor

## What landed

| file | what |
|---|---|
| `resources/board/dispatch.py` | **new**, 364 lines — the probe, moved, with the `PEARDE_ROOT`-rooted `sys.path` bootstrap replaced by the file's own directory the way `machine.py` does it, and `import board.transitions` flattened to `import transitions as trans`, the convention every other file in `resources/board/` uses |
| `resources/board/machine.py` | the verb: three lines in `main`, hoisted above `boards()` so `dispatch` does not pay for a discovery pass it repeats, and `import dispatch as dispatchlib` **lazy** so the read path never loads it. Its module docstring's *"Dispatch is the sibling PRD … not this file"* corrected — see "One edit spec01 did not name" |
| `references/parts/machine.md` | `## Dispatch` added; the unqualified *"It moves nothing"* re-aimed onto the default mode; `## The waves` now says what the pool does with the cut |
| `references/skills/pearde-all.md` | the verb, and the same correction — **note the rename below** |
| `references/files.md` | a row for `@resources/board/dispatch.py` |
| `index.md` | `@@machine` names `@resources/board/dispatch.py` |

`resources/board/dispatch.py` defines no second copy of `clash`, `frontier`,
`slots` or `progress` — `grep -cE '^def (clash|frontier|slots|progress)\('`
is `0`, asserted in spec01's block.

## The footprint moved under the specs — `pearde-machine.md` → `pearde-all.md`

spec05's footprint named `references/skills/pearde-machine.md`. That file is
`D` in `git status` and `references/skills/pearde-all.md` is `??`: a
concurrent session renamed the skill between the specs being written and this
dispatch. Both spellings are the same file — the body is the machine skill
verbatim. I took the file that exists, wrote the correction there, and updated
spec05's `footprint:` to the live spelling so `collect` commits a path that is
on disk. Both spellings are named here so the rename is not silent.

My hunks in that file are two and disjoint from the rename: the tail of the
`description:` line, and the `**This command reads. It does not move.**`
paragraph. If that session rewrites the file whole, these are the two hunks to
re-apply.

## One edit spec01 did not name

spec01 says *"Nothing else in `machine.py` changes."* One thing else did: the
module docstring said **"Read-only: it prints and moves nothing. Dispatch is
the sibling PRD `the-machine-frontier-is-dispatched-in-parallel`, not this
file."** Leaving that above a `dispatch` verb is exactly the drift spec05
exists to close, one file away. It now says the *default mode* is read-only
and names `@resources/board/dispatch.py`. No behaviour moved.

## Two checks re-aimed, and why the rule did not move

Both were whole-workspace checks — the shape
`.pearde/memos/a-harness-that-reads-the-whole-checkout-is-not-a-harness.md`
names. Neither was weakened; each was pointed at what it claims to measure.

**1. `probe/verify.sh`'s row `--dry moved nothing in this repo`** compared
`git status --porcelain` at the repo root before and after. `.pearde/` is
git-ignored, so that comparison **cannot see a board write at all** — the only
thing it can ever report is a neighbouring session's edit to `resources/`,
which is precisely what it did:

```
FAIL --dry moved nothing in this repo
7d6
<  M resources/board/brief.py     ← a sibling committed brief.py mid-block
```

Replaced by two rows that measure the thing:

- a new fixture case **`dry`**, which owns two boards under `mktemp -d`, runs
  the dispatcher with `dry=True`, and compares **every file on both boards
  byte for byte** — plus asserts the stand-in adapter's stamp file was never
  created and no `run-*.log` was opened. Race-free: no other session can touch
  a board this case made. `parse-cache.json` is excluded and the reason is in
  the code — `plan.scan` rebuilds it on any read, the read path included, and
  the board git-ignores it for that reason.
- against this repo, `--dry opened no run log on this board`, narrowed from
  the whole checkout to `$ROOT/.pearde/.state/run-*.log`.

The `dry` case was proved able to fail: `dry=True` → `dry=False` in a scratch
copy gives `FAIL dry --dry started the adapter`; restored and `cmp`-identical,
it is `PASS dry 2 would · nothing on disk moved`.

**2. every spec's verify block.** As written they let a file **outside the
footprint** decide the exit — spec01 and spec05 ended on
`python3 resources/index.py check` (currently red on a *sibling's*
`resources/board/lanes.py`), spec01 on a repo-root `git status` diff, spec03
on `git status --porcelain | grep '^ M .pearde/prds'` (which can never fire —
the board is git-ignored), and spec04 on two `… && echo "ok"` chains, which
exit 0 whatever they find. Under `collect`'s `pipefail` the first two would
have failed this PRD on a neighbour's work, and the last two could not have
failed at all. Every block now **captures** the repo-wide command, prints it,
and gates only on the lines naming its own footprint. `pearde specced … --check
--as engineer` returns `ok`, with no `cannot fail` verdict on any of the five.

## The probe moved, so the fixtures moved with it

`probe/dispatch.py` is **deleted** — that is what "move it to
`resources/board/dispatch.py`" means, and two copies would drift within the
day. `probe/fixture.py` and `probe/verify.sh` now import and invoke the
**shipped** file, so every case is evidence about what runs rather than about
a copy. `verify.sh` calls `machine.py machine dispatch --dry`, the real verb,
not a script path.

Five fixture cases were added for spec01 boxes the analyst's set did not
reach directly — `cap`, `adapters`, `once`, `deadline`, `workers`:

```
PASS dry      2 would · nothing on disk moved
PASS clash    serialised · gap 0.02s
PASS noclash  overlapped by 0.61s
PASS adapter  claude · argv ['--print', '--dangerously-skip-permissions', '/pearde run one']
PASS dead     dead: API Error: 402 {"error":"credit balance"}
PASS instant  dead: exited 0 after 0.05s — under the 0.25s launch grace, so it never worked
PASS refuse   refused [('@alpha/two', 'needs: one is `question`, not done')]
PASS alive    both in · 4 lines
PASS cap      workers: 1 serialised · workers: 0 overlapped
PASS adapters name one with --adapter (a, b)
PASS once     1 out, returned in 0.01s
PASS deadline stop · deadline reached with 1 in flight
PASS workers  load-derived 12 · --workers labels its override
```

`cap` carries its own control — `workers: 1` serialises two unrelated rows
under four machine-wide slots, and `workers: 0` overlaps them, so a per-board
cap that capped everything would fail. It also reads the board's
`settings.md` before and after and asserts the bytes are unchanged: the
dispatcher **reads** a board's `workers:` and never writes it.

`--workers N` against this repo, quoted:

```
3 slots (override) · 12 slots (at the ceiling, ceiling 12) · cpu 3.09 of 10
loaded, 4.9 cores under 80% → 15 · mem 18.9 of 32 GiB used, 6.7 GiB under 80% → 65
```

The whole command against this machine:

```
▸ machine: 11 boards · done 575/694 · 77% · derived 213/241 · open 84/949 · 9%
  · ready 52 · blocked 4 · collect 1 @8 workers · as engineer
dispatched 22 · refused 30 · dead 0
```

## Second pass on spec05 — a false red, and three checks that could not fail

`collect` refused this unit on spec05, and the refusal was right. The line

```sh
[ "$(git diff --stat -- references/settings.md | wc -l | tr -d ' ')" = 0 ]
```

returned `2`, because a **third** session has an uncommitted `groups:` row in
`references/settings.md` for `pearde machine <group>`. That edit is neither
mine nor the neighbour's I already reported, and no schedule of mine ends it.

The line was wrong in **shape**, not merely unlucky. It asserted the whole
tree is clean at that path; the box is entitled only to *this unit did not
touch it*. Those two come apart the moment anyone else is working, which on
this board is most of the time. It is redundant besides: `references/settings.md`
is in no spec's `footprint:` here, so `collect` scopes it out of the commit by
construction and cannot sweep it in whether it is dirty or not.

Replaced with the structural claim, which is the one that holds: the five
specs' `footprint:` blocks are read and asserted **not** to name
`references/settings.md` — and asserted to be non-empty and to name
`resources/board/dispatch.py`, so an empty read cannot pass it for the wrong
reason. The box now states what is tested rather than what was hoped.

**The first repair had that exact defect and was caught before reporting.** It
was written `grep -A9 '^footprint:' specs/spec0*.md`, and the block runs from
the repo root, where `specs/` does not exist: the glob matched nothing, grep
exited 2, and the `if` was false — green for the wrong reason, permanently.
Every path in it is now spelled literally, the way the route requires.

### The `-e` audit

The blocks were written to be run under `pipefail` alone, and two shapes in
them are invisible until `-e` is added:

- **`! <cmd>` mid-block cannot fail a block run with `set -e`.** Bash exempts
  an inverted command from `-e`, so a red one is swallowed unless it happens
  to be the last line. spec01 had one and spec05 had three. All are now
  `if <cmd>; then echo "FAIL …"; exit 1; fi`, which fails in every mode.
- **`grep … | head -3`** in spec03 is two traps at once: `grep` exits 1 on no
  match, and `head` closing the pipe SIGPIPEs it to 141. The producer is now
  guarded — `{ grep … || true; } | head -3`.

The other shapes the sibling warned of are not present: no block uses
`out=$(cmd); rc=$?`, and every repo-wide capture is `$(… || true)` followed by
a separate `[ -n "$out" ]` fallback, not `||` on the assignment itself.

### Each repaired check proved able to fail

Mutated, run, restored, `cmp`-identical — none of the mutations was left behind:

| mutation | block | restored |
|---|---|---|
| `references/settings.md` added to spec02's `footprint:` | `FAIL a spec footprint claims references/settings.md`, rc=1 | `cmp` identical, rc=0 |
| `**It moves nothing.**` appended to `references/parts/machine.md` | `FAIL the unqualified claim still stands`, rc=1 | `cmp` identical, rc=0 |
| `This command reads. It does not move.` appended to `references/skills/pearde-all.md` | `FAIL the skill still makes the unqualified claim`, rc=1 | `cmp` identical, rc=0 |

Final state, every block run the way the refusal asked for
(`bash -e -o pipefail`):

```
spec01 rc=0   spec02 rc=0   spec03 rc=0   spec04 rc=0   spec05 rc=0
probe/verify.sh — PASS
specced --check --as engineer — ok · complexity 38
43 of 43 boxes ticked · 0 open
```

## Finding 8 — a third session is editing `references/settings.md`, and another edited this PRD's own probe

Two collisions, neither of them mine, both recorded so nothing here reads as
silent drift:

1. `references/settings.md` carries an uncommitted `groups:` row for
   `pearde machine <group>`. Not in any footprint of mine; not touched.
2. `probe/verify.sh` was edited **at 15:16**, after my last write to it, by
   another worker: its sibling-harness row moved from `18/18` to `33/33` with
   the comment *"18 read-path rows + 15 group rows"*. The sibling's read-only
   harness genuinely grew to 33 as that `groups:` work landed, so the row is
   honest and it is green; my own re-aimed rows (`the verb is machine's`,
   `--dry opened no run log on this board`, the `machine dispatch --dry`
   invocation) all survived intact. Flagged only because this PRD's own probe
   directory is not supposed to have two writers.

## Workflow probe-then-spec

| # | step | outcome |
|---|---|---|
| 1 | `read-the-contract` | ok — PRD, 5 specs, prior report read; `git status --short` and HEAD `954b906` recorded before the first edit. One footprint path absent (`references/skills/pearde-machine.md`) and resolved to the sibling's rename, above |
| 2 | `capture-the-harness-baseline` | ok — 19 harnesses (9 naming a footprint path, 14 running a repo-root `git status`/`git diff`), `index.py check` and `doctor.sh`, all recorded **before the first edit**. 5 of 19 already red, and `index.py check` already red on `resources/board/lanes.py` |
| 3 | `attempt-the-build` | ok — the move, the verb, the four reference files. The build is an edit **in place** to footprint files, not a staged `probe/` drop: the probe was already written and this pass moved it |
| 4 | `re-run-the-harnesses` | ok — no back-edge. Three counts dropped and all three are the neighbour's; see below |
| 5 | `write-the-specs` | **not entered as authoring** — the specs exist. Its `Fails when` rows were used as a checklist over the inherited blocks, and caught all four defects above. This is the route's second pass, the implementer's: the analyst probed and specced, and steps 3 and 5 have no rebuild to do. Boxes were ticked against the tree, and the only spec edits were the two footprint/verify repairs above |

### Edits

Nothing in the workflow files was wrong for this run, and I edited none of
them. One row that earned its place: step 4's *"a count dropped and every
failing line names a file outside your footprint that `git status` shows a
live sibling modified after your baseline"* fired three times, exactly as
written, and *"the route's steps 3 and 5 have nothing to do"* described this
pass precisely — except that step 3 **did** have work, because the probe still
had to be moved into the footprint. A sharper spelling for that row's
condition would be *"the build is already in the tree **and already at its
footprint paths**"*; on this run it was in the tree and under `probe/`.

## Harness counts, baseline → final

| # | harness | before the first edit | after | whose |
|---|---|---|---|---|
| 01 | `an-unknown-flag-refuses` | `196 checks · 196 pass · 0 fail` | `196 · 195 · 1 fail` | **the neighbour's** |
| 05 | `seven-closed-probes-drifted-red/the-fixtures-meet-the-tool` | `35 · 31 · 4 fail` | `35 · 29 · 6 fail` | **the neighbour's** |
| 12 | `the-board-runs-itself/transitions-are-commands` | `74 · 73 · 1 fail` | `74 · 67 · 7 fail` | **the neighbour's** |
| 16 | this PRD's probe | `FAIL` (transient — see below) | **`PASS`, 18 of 18** | mine |
| 17 | `the-machine-frontier-is-one-ordered-list` | `PASS`, 18 ok | `PASS`, 18 ok | unchanged |
| — | the other 14 | unchanged | unchanged | — |
| — | `index.py check` | red on `resources/board/lanes.py` | same line, unchanged | **the neighbour's** |
| — | `doctor.sh` | `index broken`, `knowledge broken` | same two rows, same colours | **the neighbour's** |

**I claim no red-to-green flip.** Harness 16 read `FAIL` in my baseline sweep
and `PASS` at the end, and the flip is **not** attributable to this pass: the
two rows that were red are `--dry moved nothing in this repo` and `the sibling
read-only harness is still 18/18`, both of which read a repo-root `git status`
that a live session was moving under the sweep. I re-ran the same harness three
times **before my first edit** and it was `PASS|PASS|PASS`. The baseline was
transient, and it is recorded here as transient rather than banked.

## Finding 6 — three harnesses went red on a sibling's landing, not on this unit

Between my baseline (14:44) and my re-run, a concurrent session landed a
"lanes" feature: `resources/board/lanes.py` created 14:45:40 (untracked),
`resources/board/transitions.py` 14:47:26, and new hunks in `collect.py`,
`brief.py`, `plan.py` and `edit.py` — 135 lines across five files that were
not modified when I took the baseline.

Proof it is not mine: **none of the three harnesses names a single path in my
footprint** —
`grep -cE 'machine\.py|dispatch\.py|parts/machine\.md|skills/pearde-(machine|all)\.md'`
is `0` on all three. They entered my baseline set only because they run a
repo-root `git status`/`git diff`. Every failing line names the neighbour's
work:

```
01  FAIL D …the real sweep prints the line the dry run said
    got: sweep: big/second lane removed · branch lane/big-second kept
12  FAIL git diff empty after every refusal
     M .pearde/prds/clash/prd.md   ?? .pearde/.claims/   ?? .pearde/.lanes/
12  FAIL .transitions.jsonl has one row per state move (13) → 14
05  FAIL F no file under resources/ carries any of this
    ← reads `git diff --name-only -- resources/board/plan.py resources/board/init.py`
```

Left alone, per the route: there is nothing in my footprint that closes them.
They are owed to the lanes PRD, not to this one.

## Finding 7 — `index.py check` is red on a sibling's unmanifested file

`resources/board/lanes.py is on disk with no row in references/files.md`, red
**before my first edit**. `references/files.md` is in my footprint, so I could
have closed it with one row — and did not: writing a manifest row for a file I
did not write, whose description I would be inventing, is a fix outside scope.
Its owner will add it with the rest of the feature. It is the reason
`doctor`'s `index` row is `broken` at both ends of this run.

## Findings carried forward from the analyst's pass

Named, not restated — the earlier report is the record and none of these were
closed by this pass.

- **Finding 1 — the load meter is a proxy, and the bound is a dead worker.**
  Still the substantive part. It shipped as `Job.poll` in
  `resources/board/dispatch.py` and is spec02's whole unit; the `dead` and
  `instant` fixtures still prove it against the shipped file. `[[260902-b296]]`.
- **Finding 2 — `machine` marks a row `ready` that `pearde claim` refuses.**
  **Still open, still reproducible.** `plan.compute_plan` computes the `held`
  band only over rows with no dependency edge left, so a container with an edge
  reaches the frontier with `held` empty while `claim` refuses it. `--dry`
  against this machine right now:
  `skip @mitosys/plugins-visible · leaf: plugins-visible has children not done`.
  Not fixed here — `plan.py` is outside this footprint and is being written by
  the concurrent session. It costs this contract nothing, because re-asking the
  gate at the launch **is** this PRD's requirement, and the `refuse` fixture
  fails the moment the dispatcher stops re-asking. Worth its own PRD on the
  read path.
- **Finding 3 — the worktree defect `[[260902-b1f6]]` did not block this
  build.** Still true; `real_feet` walks from the board's parent and the
  dispatcher writes no commit.
- **Finding 4 — three settled forks held without loosening.** Held, and now
  written down where the verb is described: `/board/all` gains no write door,
  discovery is still `ensure` + `/status` with no registry, and no board's
  `settings.md` is written — the `cap` fixture asserts the last one on the
  bytes. `references/settings.md` was not edited; spec05's block asserts it.
- **Finding 5 — `probe-then-spec` fit unchanged.** Still true on the second
  pass, with the one sharpening noted under `### Edits`.

## Notes

- No word was missing from `python3 resources/grammar.py show`.
- Nothing was learned outside this repo, so nothing was written to
  `knowledge.py`.
- Files touched outside my footprint: **none**. `probe/` and `specs/` are
  inside this PRD's own directory.

## Scores

complexity: 38
blast-radius: high
workflow: probe-then-spec
