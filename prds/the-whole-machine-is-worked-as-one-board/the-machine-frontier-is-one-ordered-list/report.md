# the-machine-frontier-is-one-ordered-list — implementer report

Verdict: DONE

41 of 41 acceptance boxes closed and ticked as each was proven — spec01 16/16,
spec02 12/12, spec03 13/13. The probe is now `resources/board/machine.py`,
discovered through `COMMANDS`, and `pearde machine` prints the merged frontier
from any directory and moves nothing.

Built: `resources/board/machine.py`, `references/skills/pearde-machine.md`,
`references/parts/machine.md`. Amended, minimally and only my own rows:
`references/files.md` (3 rows), `index.md` (`@@machine` scope + `@@skills`),
`SKILL.md` (description), `references/settings.md` (one row appended after
`name`). No file held by the concurrent session was written.

`machine-ceiling: 0` now means unlimited, on the coordinator's instruction —
the one thing this build and the peer session's convention did not meet. It is
fixed, guarded and proven; `## The ceiling, and what `0` means` below is the
whole of it.

Gate: `index.py check` — one problem, the one already on record.
`memos.py check` — clean. `doctor.sh` — every row ok but that same `index`
row. `probe/verify.sh` — **18 of 18**, PASS.

## Verify and Proof — what ran

`bash probe/verify.sh` (spec01's harness, `MACHINE_PY=resources/board/machine.py`):

```
ok   runs from / with no board above the cwd
ok   prints a board count over the watch set
ok   prints the slot count and its reading
ok   the reading names the cpu term
ok   the reading names the memory term
ok   every row is addressed @<board>/<rel>
ok   prints at least one wave
ok   a row marked ready is in a wave
ok   no row marked ready carries a non-dispatchable state
ok   the merged progress line is one line
ok   --json parses and carries slots, rows, waves
ok   it moved nothing in this repo
ok   machine-ceiling: 0 lifts the ceiling
ok   an unlimited ceiling prints ∞, never 0
ok   an unlimited ceiling keeps the floor of 1
ok   a set machine-ceiling is honoured
ok   an absent machine-ceiling still gives 12
ok   an unparseable machine-ceiling gives 12
PASS
```

The last six rows are new — the cases that would have caught the `0` clamp.
They run against a throwaway board rather than this repo's own, and read the
count out of `slots()` with the meter held still, because what is being tested
is what `machine-ceiling` *says*, not what this machine happens to be doing.

`python3 resources/pearde.py machine`, run from the repo root:

```
skipped all — no path — the merged page, not a board
1 of 1 board(s) · 7 PRDs on the frontier · 1 wave(s)
demand 5 at once, unconstrained
12 slots (load1 stale, ceiling 12) · cpu 15.62 of 10 loaded, -7.6 cores under 80% → 0
  · mem 18.1 of 32 GiB used, 7.5 GiB under 80% → 74 · busy 42% now (1.5s sample)
```

`pearde help` carries the row — `  pearde machine   every watched board as one
ordered frontier —…` — and `cd / && python3 …/machine.py machine` exits 0.
`pearde machine boards` prints `pearde  …/.pearde  cap ∞`.
`pearde machine progress` is one line, in `@references/parts/progress.md`'s
register: `▸ machine: 1 boards · done 70/76 · 92% · derived 22/23 · open 5/103
· 5% · ready 5 · blocked 0 · collect 1 @5 workers · as engineer`.

`--json` carries `boards, demand, notes, reading, rows, skipped, slots, waves`.

`git status --porcelain` diffed either side of every run: unchanged.

### The boxes that needed a rig rather than a run

Four boxes cannot be proven against a one-board watch set, so they were proven
by calling `frontier()` and `waves()` directly over temporary boards built in
the scratchpad. That is the shipped code path — `frontier` takes its entries as
an argument and never touches the daemon.

- **footprint clash** — two boards, `link/target.txt` and `other/target.txt`,
  both symlinks onto one real file. Both resolved to
  `…/mt/shared/target.txt`; the cut produced two waves, and the later row
  printed `footprint clash with @repoA/alpha`.
- **a master's members are not counted twice** — a master naming both boards
  as members produced `merged rows: ['@repoA/alpha', '@repoB/beta']`, each
  taken from its own board, and `demand 2`, not 4.
- **footprints resolve from the board's parent** — on this board, which *is* a
  git worktree, `leaked-background-services-outlive-their-fixtures` resolved to
  `/Users/feb/dev/infra/pearde/resources/board/serve.py`. `plan.repo_root` on
  the board itself answers `/Users/feb/dev/infra/pearde/.pearde`, under which
  no such file exists — this is defect `[[260902-b1f6]]`, routed around rather
  than patched, as instructed.
- **a board that will not read** — a board whose `prds/` is a file printed
  `repoC: unreadable — no `prds/` directory at …` in `notes`, and the other
  board's rows still printed.

### The meter's boxes

Proven by substituting `_machine` / `_busy_now`, and by reading `vm_stat`
alongside the file:

```
mem: total 32 GiB · `Pages free` alone -> 31.9 GiB used · four counters -> 19.7 GiB used
   machine.py reports: 19.71
stale:      12 | 12 slots (load1 stale, ceiling 12) · … · busy 5% now (1.0s sample)
saturated:   1 | 1 slots (at the floor, ceiling 12) · … · busy 99% now (1.0s sample)
quiet:      12 | 12 slots (at the ceiling, ceiling 12) · …  (0.0 ms, no sampler)
unreadable: 12 | 12 slots · machine unreadable, holding at the ceiling
/proc: cores 10 load1 3.31 total 31 GiB used 18.8 GiB  (no vm_stat, no sysctl)
ceiling: absent -> 12 · `4` -> 4 · `banana` -> 12 · `900` -> 12
```

The linux branch could not be run on linux. `_machine_proc` grew a `root`
argument so the same code reads a fake `proc/loadavg` and `proc/meminfo`; the
parse is proven, and `subprocess.run` was replaced with a raiser for the
duration to prove `vm_stat` and `sysctl` are never reached on that path. The
`None`/`None` fallback to the ceiling is proven too, which is the alternative
spec02 allowed.

## What changed from the probe, and why

Beyond the three edits spec01 named (own-directory import, the `files.md` row,
the `@@machine` scope row) five things moved. Each is inside a spec's scope and
none is a refactor.

1. **`compute_plan(board, workers=0)`, not `workers=nslots`.** The peer session
   landed the memo `the-board-assumes-unlimited-agents` mid-run: `workers: 0`
   is now unlimited and the default, and a cap is a person's setting rather
   than the plan's clock. Passing the slot count into each board's own plan cut
   the list twice — once by a cap that board never had, once here — and hid
   work. Each board's schedule is now drawn unconstrained, so `start` is the
   dependency structure alone, and the slot count is applied exactly once, when
   the merged list is cut into waves.
2. **`demand <n> at once, unconstrained`**, a new header line: the sum of every
   board's `peak`, which `plan.py` now returns. It is the machine's demand with
   no second scheduler — `plan.py`'s own number added up. A master's `peak` is
   skipped, on the same rule that drops its member rows.
3. **The clash reason is printed.** The probe computed
   `footprint clash with <addr>` and then discarded it: `waves()` re-copied the
   row with `why=None` when it was finally admitted, and `text()` never read
   the field. The reason is now kept per address, first-reason-wins, and
   printed as the row's note. The acceptance box asks for it to be *printed*,
   and before this it was not.
4. **A board that will not read is noticed.** `compute_plan` answers `None` for
   two different things — a board with nothing live, and a board it could not
   read — so the probe's `try/except` caught nothing and a broken board went
   silently missing across the whole machine. A missing `prds/` is now a note.
5. **`pearde all:` in the error path became `pearde machine:`**, and the
   `boards` verb prints each board's own cap through `plan.workers_label`, so
   `workers: 0` reads `∞` rather than `0`, which means the opposite.

`probe/verify.sh` also gained two lines: it now resolves a relative
`MACHINE_PY` against `$ROOT` (spec01's own Verify block passes a relative path,
and the harness `cd`s to `/`, so the probe's copy silently tested nothing), and
its "moved nothing" row now diffs `git status` from before the run rather than
grepping it afterwards, which could not tell this build's own new files from a
write the command made.

## The name

Built as `pearde machine`, per spec03 and the orchestrator's instruction — not
`pearde-all`. `all` already names the read-only page whose contract sentence
*"nobody works it"* the parent PRD's fork 1 forbids editing.
`references/parts/machine.md` links that sentence rather than restating it, and
`git diff` on `references/parts/all.md` and `references/parts/master.md` is
empty.

## Findings

### The load meter is a proxy, and the real ceiling is invisible to it

This is the one thing the gated sibling PRD should inherit rather than
rediscover. What actually limits concurrency on this machine is not cpu, memory
or load — it is the model gateway answering 402 or 429. That surfaces as a
**dead worker**, not as load: an async launch is not the same as an agent that
is alive, and a worker killed at the gateway costs nothing measurable locally
while producing nothing. No local meter can see it, and this command dispatches
nothing, so no detection was built. The probe's own measurements already say
the same thing from the other side: 80% of this machine is 25 to 270 workers,
which is the fifty-at-once the user declined, reached silently. The floor of 1
and the ceiling of 12 are what make the number a person would choose; the load
term between them only ever lowers it.

`the-machine-frontier-is-dispatched-in-parallel` is where a launched-but-dead
worker has to be detected, because that is the first command that launches one.

### The ceiling, and what `0` means

`machine-ceiling` is a settings row rather than a buried constant, so it can be
moved. It defaults to the measured composite — floor 1, ceiling 12,
load-derived between — which is this board's recorded answer to Q1
(*"dynamically by load, so we use 80% power of the machine"*).

I first shipped `ceiling()` clamping to `1..64`, so `machine-ceiling: 0` fell
back to 12 instead of lifting the cap, and flagged it as the one place this
build and the peer session's `0 = unlimited` convention did not meet. The
coordinator ruled: make `0` unlimited. Done, and the reading is now:

```
ceiling(): absent -> 12 · `0` -> 0 · `4` -> 4 · `64` -> 64
           `65` -> 12 · `-1` -> 12 · `banana` -> 12
uncapped, quiet:      24 | 24 slots (cpu-bound, ceiling ∞) · cpu 0.20 of 10 loaded …
uncapped, saturated:   1 | 1 slots (at the floor, ceiling ∞) · … busy 99% now
uncapped, unreadable: 12 | 12 slots · machine unreadable, holding at the ceiling
                           — none is set, so the measured 12 stands
ceiling 4, quiet:      4 | 4 slots (at the ceiling, ceiling 4) · …
ceiling 12, quiet:    12 | 12 slots (at the ceiling, ceiling 12) · …
```

The counterfactual, so the new harness rows are not decoration:

```
pre-fix   machine-ceiling: 0 -> ceiling 12, 12 slots, 12 slots (at the ceiling, ceiling 12)
post-fix  machine-ceiling: 0 -> ceiling 0,  24 slots, 24 slots (cpu-bound, ceiling ∞)
```

**The default did not move.** An untouched board still gets the measured 12;
only an explicit `0` lifts the cap, because unlimited is a thing a person
chooses rather than inherits.

**The arithmetic is guarded.** `SLOT_CEILING == 0` through a bare
`min(SLOT_CEILING, n)` would pin every reading to zero and dispatch nothing —
the exact inversion of the setting. Every site now goes through `_clamp()`
(floor always, ceiling only where there is one) or `_ceiling_label()`
(`plan.workers_label`, so it prints `∞` and never a bare `0`, which reads as
*no slots* and means the opposite). `grep -n 'SLOT_CEILING'` shows no
comparison or `min()` left outside those two, and `SLOT_FLOOR` still applies
under an unlimited ceiling — proven by the saturated row above.

One case the instruction did not settle, decided and written down rather than
guessed: **a machine that cannot be read at all, on a board with no ceiling
set.** There is no load term to hold and no number the person gave to hold
instead, so it holds at the measured 12 and the reading says why. Returning an
unbounded count off an unreadable machine would be the worst of both.

### No spec box covers the `0` case, and I did not invent one

Said plainly, because the coordinator asked to be told rather than have the
spec quietly widened. spec02's nearest boxes are *"`1 <= n <= machine-ceiling`
for every reading"* — whose upper bound is vacuous once there is no ceiling —
and *"an absent or unreadable value leaves 12 standing"*, which covers absent
and unparseable but says nothing about `0`. Both are still true and stay
ticked. The `0` behaviour is proven by six new rows in `probe/verify.sh` and by
the block above; it is **not** ticked against any acceptance box, because there
is none to tick. The spec was thin here.

### Where the ceiling is read from, which the spec did not settle

There is no machine-wide settings file, and this command spans every board and
writes to none. `machine-ceiling` is therefore read from the board at the cwd
when there is one, and the measured default stands anywhere else. That is
stated in the settings row and in `references/parts/machine.md`, because it is
the kind of rule that is a bug the second it is undocumented.

### A member nobody watches loses its work

A master's rows are dropped in favour of the member's own. If that member is
not registered with the daemon, its PRDs appear on the frontier nowhere at all.
This is the same rule `@references/parts/all.md` already states of its own
merge, so it is consistent rather than new, and it is written down in
`references/parts/machine.md`. It is worth a person knowing: on this machine,
registering a master is not the same as registering its members.

### A question does not empty its board

Checked against the peer's scoped drill gate: `dispatchable` carries no
question gate, so a board carrying `asking N` still contributes every ungated
row to the frontier. Nothing in the merge drops or zeroes such a board. The
asker itself is held by its own state and prints `waits`, which is right.

## Defects outside scope, not fixed

- **`plan.repo_root` stops at a board that is a git worktree** —
  `[[260902-b1f6]]`. Routed around by `real_feet`, which walks from the board's
  parent. `plan.py` is held by the concurrent session; not touched.
- **`resources/board/edit.py references @questions.py — not on disk`** — the
  one `index.py check` problem, already on record, and the reason `doctor`'s
  `index` row reads `broken`. Outside my footprint.
- **`waves()` reported `no slot free` for a row that was both out of slots and
  clashing** — it now asks for the clash first, so the row is told the thing it
  cannot fix by waiting. Fixed inside spec01's scope; noted because the probe's
  ordering was the other way round.

## Housekeeping

`python3 resources/knowledge.py relink` was run: `graph.json` was behind two
notes, `260902-5c4d` and `260902-b307`, both written by this PRD's own analyst
pass an hour before the claim. That was `doctor`'s `knowledge` row reading
`broken`; it now reads `ok — 40 notes, graph in sync`. Nothing was written to
the notes themselves. No new knowledge note was needed: every number in this
build was measured on this machine, not learned outside the repo.

## Health

`resources/board/machine.py` scores **76** (`lines, branching`) — well over the
floor of 40. No file in the footprint was under the floor before or after, and
nothing was moved on health grounds.
