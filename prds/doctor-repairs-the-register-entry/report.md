Verdict: DONE

# doctor-repairs-the-register-entry — implementer report (pass two)

Route `probe-then-spec`, second pass. Pass one (analyst) built the repair in
the lane and wrote `spec01`; this pass took its own pre-edit baseline, proved
the build against it, made the spec's verify block runnable, and ticked the
six boxes against commands run this session. The build itself was not
touched: `git -C <lane> diff` is byte-identical to what pass one left
(`cmp` on the two diffs, clean).

Lane `/Users/feb/dev/infra/pearde/.pearde/.lanes/doctor-repairs-the-register-entry`,
`M references/obsidian.md`, `M resources/doctor.sh`, +52 lines, 0 removed.

## spec01 — all six boxes closed

The verify block, run the way `collect` runs it
(the fenced block awk'd out of `spec01.md` and fed to
`bash -e -o pipefail -c`, cwd the lane) — **exit 0**:

```
14 ok · 0 fail
index.py check:
resources/common.py is on disk with no row in references/files.md
references/files.md lists @resources/board/hotreload-test.js — not on disk
@@view names @resources/board/hotreload-test.js — not on disk
memos.py check: 43 lines
```

Watched it fail first. With `resources/doctor.sh` put back to the lane's
`HEAD` and nothing else changed, the same block is **exit 1** on `8 ok · 6
fail`; restored from a scratch backup and proved with `cmp` (identical). The
flip is 8 ok/6 fail → 14 ok/0 fail, and it is this hunk's.

| box | check | evidence |
|---|---|---|
| 1 | `--fix` reaches the writer, prints `vault repaired` | probe B `ok   B prints the literal repaired line` |
| 2 | Obsidian up → refusal, nothing written | probe C, 3 ok — `refused — Obsidian is running`, register still `{"vaults":{}}` |
| 3 | two realpath-equal entries → names both, writes nothing | probe D, 5 ok — both ids present, `already carries more than one entry`, register untouched |
| 4 | no `--fix` → unchanged | probe E, 3 ok — `broken` row, no repair line, no refusal note |
| 5 | the row's earlier branches untouched | ran both doctor.sh versions on one fixture set, `$SKILL_ROOT` normalised — see below |
| 6 | `bash -n` + the board's gate carry no new failure | `bash -n resources/doctor.sh` silent; `index.py check` 3 lines, `memos.py check` 43 lines, both identical to the pre-edit baseline |

Box 5, pre-edit `doctor.sh` against built, same fixtures, with and without
`--fix`:

```
── branch 1 · ok, registered ──          same  no flag / same  --fix
── branch 2 · ok, no Obsidian config ──  same  no flag / same  --fix
── branch 3 · off, no .obsidian/ ──      same  no flag / same  --fix
── branch 5 · broken, dot-segment board (this repo) ──  same  no flag
```

The `broken` no-home branch is not reachable on a fixture — doctor resolves
the home from passwd, by design — so it is covered by the harness that owns
it, `seven-closed-probes-drifted-red/the-doctor-completes-without-a-home`,
unmoved at `12 checks · 9 pass · 3 fail · 0 skip` on both trees. Whole-tree
confirmation: the built `doctor.sh` and HEAD's print **91 identical rows**
on this repo, `statusline` excluded (that row carries the dirty-file count
and every live session moves it).

## Baseline and re-run — every number, both trees

Taken on the lane with the footprint reverted to `HEAD`, before this pass's
first edit; re-taken on the built lane. `PEARDE_ROOT=<lane>` on every run.

| harness / gate | before the first edit | after | moved |
|---|---|---|---|
| this PRD's `probe/verify.sh` | 8 ok · 6 fail | **14 ok · 0 fail** | this hunk's flip |
| `a-session-start-brings-the-board-up` | 46 checks · 40 pass · 6 fail · 0 skip | same | no |
| `…/the-doctor-completes-without-a-home` | 12 checks · 9 pass · 3 fail · 0 skip | same | no |
| `…/init-seeds-a-board-doctor-calls-green` | 41 checks · 26 pass · 15 fail · 0 skip | same | no |
| `the-board-runs-itself/one-command` | 53 passed, 1 failed | same | no |
| `upgrade-leaves-the-memo-index-stale` | 40 checks · 17 pass · 22 fail · 1 skip | same | no |
| `index.py check` (lane) | 3 lines, exit 1 | same | no |
| `index.py check` (checkout) | 0 lines, exit 0 | — | — |
| `memos.py check` (lane and checkout) | 43 lines, exit 1 | same | no |
| `bash -n resources/doctor.sh` | silent, exit 0 | same | no |
| `doctor` rows on this repo | 91 rows | 91 identical rows | no |

Every one of those harnesses was red **before the first edit**. None is
mine and none moved.

`index.py check` is red in the lane and green in the checkout — the lane is
behind the checkout's uncommitted `references/files.md` / `index.md` work
(`resources/common.py` landed as a commit the lane holds, its index rows
only as a neighbour's working copy). Those three lines close on the merge.
Nothing was added in the lane to silence them.

**Not run, and why.** `bash resources/doctor.sh --harnesses <board>` was
started and killed at ten minutes with the `harnesses` row still unprinted —
94 harnesses at load average 33–43. The set was narrowed to the harnesses
whose text names a footprint path (22) and then to those that also assert on
`vault` or `--fix` (8). Of those, `the-gate-runs-the-harnesses` runs the
whole sweep and is the same cost, so it was not run;
`the-tree-holds-only-what-a-board-uses/the-documented-board-matches-the-code`
carries no `PEARDE_ROOT` and measures the orchestrator's checkout however it
is invoked, so no count from it could be this lane's. Both are named rather
than counted.

## What this pass changed outside the build

**`specs/spec01.md` — the verify block could not run.** As written it began
`PEARDE_ROOT=<repo root under test> bash .pearde/prds/…/probe/verify.sh`, and
`collect` runs the block: `bash -e -o pipefail -c` on it dies immediately
with `bash: repo: No such file or directory` — the angle brackets parse as a
redirect — with all six boxes ticked. Its last two lines were
`python3 resources/index.py check` and `python3 resources/memos.py check`,
board-wide gates already red on lines outside this footprint, so under `-e`
the spec could never have passed however green its own unit was. Rewritten:
the tree under test is `$PWD` (which is what `collect` sets, and
`resources/board/specs.py` now refuses a block that `cd`s to a literal repo
root), the board is walked to rather than named — `pearde/` or `.pearde/` at
or above the repo — and both gates are captured and printed instead of
gating. `specced --check` reads `ok · complexity 16 · footprint
references/obsidian.md, resources/doctor.sh`. The acceptance text was not
touched.

**The six boxes were unticked and re-ticked.** They arrived `[x]` from pass
one; `specced --check` warns `6 of 6 boxes already ticked before an
implementer ran them`. Each was unticked and ticked again as this pass
closed it against a command run here. The warning still prints — it reads
the file, not who ticked, so it cannot tell an analyst's pre-tick from an
implementer's honest one.

**`probe/verify.sh` — the fixture leaked boards into the live daemon.** The
probe runs `doctor --fix` on a fixture project that holds a board, so
doctor's own `board registered` row registered the temp dir with the running
view daemon, which outlived it. `serve.py status` held two dead fixture
boards from pass one:

```
  proj             synced 217s ago · …/scratchpad/vaultfix.ejSF/proj/pearde
  proj-2           synced never · /var/folders/…/tmp.lWseTnoPJz/proj/pearde
```

Both removed after testing the path first (`[ -d "$p" ] || serve.py forget`),
and `PEARDE_PORT=1` added to the probe's two `env -i` invocations so the
repair cannot connect and registers nothing. `serve.py status` after every
subsequent run: `pearde` alone, `master of 1`.

## Finding — `pearde vault` refuses unconditionally today, unrelated to this PRD

Carried forward from pass one, unchanged and still standing.
`resources/board/init.py`'s `cmd_vault` calls `unhide_board(d,
args.opt.get("dir"))` on every non-dry run with no `--dir`; `unhide_board`'s
`name` defaults to `planlib.BOARD_DIR`, which `resources/board/boards.py`
sets to `.pearde` while `LEGACY_BOARD_DIR = "pearde"` — the reverse of the
pair `doctor.sh`'s comments and the in-flight
`the-board-is-a-real-directory-at-pearde-never-a-symlink` family assume.
`unhide_board` refuses any name starting with `.`, so **every** `pearde vault
<dir>` with no explicit `--dir` refuses before reaching the register. That is
why the probe's check A asserts the refusal surfaces rather than a write, and
why check B stubs the writer. Owner: `resources/board/init.py` /
`resources/board/boards.py`, outside this PRD's footprint by its own
`## What stays out`.

## Finding — a neighbour's `serve.py reap` kills this session's measurements

Three long runs of mine died on **exit 144** mid-harness. The killer is a
peer worker's `…/scratchpad/impl-vault-run/pre/resources/board/serve.py reap`,
which reaps machine-wide rather than scoping to what it started. Every count
in the table above was re-taken in the foreground afterwards and is whole,
but no background measurement on this board is trustworthy while that
process runs. Owner: whoever holds `serve.py reap`'s scoping.

## Finding — `resources/doctor.sh` is under the health floor

`python3 resources/health.py score resources/doctor.sh` in the checkout reads
`28  resources/doctor.sh  branching, lines` against a floor of 40 — pre-edit,
before this hunk lands. The brief's health block said `none under the floor`
and is stale against `health.py score`. Nothing inside this spec's scope
moves it: the score is `branching, lines` on a 60 KB shell script and the
only repair is a split, which is a defect outside scope — reported, not done.
The hunk is purely additive (45 lines added, 0 removed) and adds one branch
under `--fix` in one row.

## Workflow probe-then-spec

| # | step | outcome |
|---|------|---------|
| 1 | `read-the-contract` | ok — `prd.md` (no `## Answers`/`## Questions`/`## Failure`), `specs/spec01.md`, the cited `docs/content/docs/improvements/obsidian-register-repair.mdx` (present, untracked in the checkout), `git status --short` recorded in both roots, both footprint paths present in the lane and clean in the checkout |
| 2 | `capture-the-harness-baseline` | ok — footprint reverted to lane `HEAD` and every number above taken before the first edit; the full `--harnesses` sweep abandoned at ten minutes, set narrowed and the exclusions named |
| 3 | `attempt-the-build` | **not entered** — its first `Fails when` row: this is the route's second pass, `git status --short` and `git diff` show spec01's whole footprint already built, so no spec was entered. Its fixture/daemon row fired and was applied (`PEARDE_PORT=1`, `serve.py forget`) |
| 4 | `re-run-the-harnesses` | ok — every count re-taken on the built lane, all equal to baseline except this PRD's own probe. Its "red in the lane, green in the checkout" row fired on `index.py check` and was applied |
| 5 | `write-the-specs` | second pass — no spec authored. Its `Fails when` table applied to the block that already stood: the placeholder-argument row and the board-wide-gate row both fired, and the previous pass's `## Finding` is carried forward by name as its report-overwrite row requires |

### Edits

**`read-the-contract`, last row of `## Fails when`** — its `do` column ends
"…**and read the next row before you baseline anything**", and it is the
last row in the table. There is no next row. Replace that clause with the
atomic it actually points at:

> symlink the live board in at `<lane>/pearde` (both `/pearde` and
> `/.pearde` are gitignored) — **or, where every harness in the set honours
> `PEARDE_ROOT`, skip the symlink and run each from the board with
> `PEARDE_ROOT=<lane>`, which is cheaper and cannot be resolved back by
> `pwd -P`. Read `capture-the-harness-baseline`'s `## Fails when` before you
> baseline anything either way.**

**`capture-the-harness-baseline`, `## Fails when`** — no row covers a
footprint that most of the board's harnesses read. Measured here: 22 of 94
harnesses name `resources/doctor.sh`, and `doctor.sh --harnesses` did not
reach its own row in ten minutes at load 33–43. Add:

> | the harness set that names a footprint path is a large fraction of the board, and a full sweep does not finish | the footprint is a file the board reads about itself — `doctor.sh`, `plan.py`, a reference page — so "every harness that touches it" is the board | narrow in two named steps and record both: the harnesses whose text spells a footprint path, then those that also assert on the *row or verb* the unit changes. Run that set twice. Name every harness dropped and why — one that enumerates the board costs the same as the sweep, one with no `PEARDE_ROOT` measures another tree — and never report a narrowed set as the set |

**`re-run-the-harnesses`, `## Fails when`** — its guard row is about the
*worker* standing a guard down; nothing covers a neighbour reaping the
worker. Add:

> | a long harness run dies on **exit 144** with no failing line of its own | 144 is 128+16, a signal from outside: another session's `serve.py reap` (or any machine-wide reaper) is killing processes it did not start | `pgrep -fl reap` names the owner and the tree it runs from. Re-take every affected count in the **foreground**; a backgrounded measurement on a board with a live reaper is not evidence. Report the reaper's scoping as a finding against its owner — do not narrow your own set to fit inside its window |

## Scores

complexity: 16
blast-radius: low
workflow: probe-then-spec
