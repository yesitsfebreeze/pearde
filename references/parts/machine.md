# `machine` — every watched board as one ordered frontier

What the whole machine should work on next: one ordered list, cut into the
waves able to run at once.

```sh
pearde machine              # the frontier, the waves, and the reading behind them
pearde machine boards       # what the daemon watches, and each board's own cap
pearde machine slots        # the concurrency and the numbers that produced it
pearde machine progress     # one progress line over the merged set
pearde machine groups       # the labels the watched boards declare, and who holds them
pearde machine --json       # the same read, as data
pearde machine dispatch     # the one verb that moves: run that frontier down

pearde machine work         # the same read over one group of boards
pearde machine work slots   # any verb takes the group, in either order
pearde machine work dispatch
```

Runs from anywhere, with no board above the cwd: the watch set is the live
service's, not the directory's, and @resources/board/machine.py is found
through `pearde.py`'s `COMMANDS` discovery rather than a path.

**The default mode moves nothing.** `pearde machine`, and every verb but one,
make no claim, no transition, no dispatch and no write to any board, settings
file or PRD: they read and print. Moving the machine is a verb you type —
`pearde machine dispatch`, `## Dispatch` below — so no command both reads the
machine and moves it. A person must be able to look at the whole machine
without the looking starting anything.

## What it merges

- **Every board the daemon watches**, from `/status` — the same set
  @references/parts/all.md renders. Registering a board is the whole of
  joining, and **an unwatched board is not discoverable**: no persisted
  registry of boards is kept here or written. An unregistered board is
  invisible to this command, on the same rule @references/parts/all.md states
  of its own merge — *a member nobody watches is not one of them*.
- **A row with no path is skipped**, with its reason printed. The `all` page
  sits in the watch set as exactly such a row — a render over the boards,
  never one of them, and never counted as a board.
- **A row already carrying a `board` is dropped.** A master's payload carries
  its members' PRDs, and those members are watched boards in their own right,
  so each PRD is taken once, from the board that owns it. The same reason a
  master's `peak` is not added to the machine's demand.
- **Each board's own plan, computed by the code that already computes it.**
  `plan.compute_plan(board, workers=0)` per board, and the merged list is its
  `schedule` interleaved by start, priority, board and name. No second
  arithmetic: a scheduler here that disagreed with the board's own would make
  the frontier and the board's page tell a person two different things.

`workers=0` is deliberate. Each board's schedule is drawn **unconstrained**,
so `start` is the dependency structure and nothing else, and `peak` is the
board's honest demand. The slot count is applied once, when the merged list is
cut into waves — cutting it twice would hide work behind a cap the board never
had (`.pearde/memos/the-board-assumes-unlimited-agents.md`).

## Groups

A group is a label a board writes **on itself** — `groups: work infra` in its
own `.pearde/settings.md` (@references/settings.md) — and `pearde machine
<group>` is this same read over the boards carrying it. The frontier, the
waves, the demand, the progress line and `dispatch` are then that group's:
same arithmetic, fewer boards.

**Nothing here keeps the list.** No file names which board is in which group,
on the rule this command already follows for the watch set: the configuration
is distributed to the boards, and a board nobody watches is in no group,
being in nothing. `machine <group>` reads `groups:` off each watched
board's settings as it walks them, and writes nothing — *No board's
`settings.md` written* below stands unchanged, `groups:` included. A person
sets one with `pearde settings groups=work`, standing in that board.

**Labels, not a partition.** A board may carry several and most carry none;
`work` and `private` are two labels among any others, and nothing forces the
set to divide. `machine groups` prints each label with its boards, then the
ungrouped ones on a `—` row.

Two labels are refused, at the board that declares them and named by `machine
groups` rather than silently at the point of use:

| refused | why |
|---|---|
| a verb — `boards`, `slots`, `progress`, `groups`, `dispatch` | `pearde machine slots` has to keep meaning the slot reading. The verb set is closed, so a group is any bare word outside it and the two never compete |
| `all` | `all` is every board by definition, and never a subset of them (@references/parts/all.md) |

A group naming no watched board is a **refusal, not an empty frontier**: an
unwatched board is invisible here, so a silent empty list would read as
*nothing to do* when the truth is *that board was never registered*. The
refusal names the groups that do exist and the line that joins one.

**The page has no group filter.** `all` renders the whole watch set and
nothing else. Grouping is a command-line read; a subset URL would put a second
answer to *what is the set* on a page whose whole rule is that the watch set
is it.

## The marks

One column per row, and it agrees with the waves printed below it.

| mark | what it says |
|---|---|
| `ready` | it is in a wave. If the wave is not the first, the note says what pushed it there |
| `held` | `plan.dispatchable` refuses it — a parked child, a stale claim, a `needs:` not done, a `workflow:` naming nothing. A footprint held by a `claimed` PRD is not among them: each worker works in a lane of its own, so that pair is ordered rather than refused and the merge resolves it. The note is that verdict, verbatim |
| `waits` | its state is not dispatchable. Only `open` and `specced` enter a wave; `claimed`, `analyzing`, `question`, `blocked` and `deferred` print `waits` with the reason and appear in none |
| `collect` | it is finished work `pearde collect` closes, not a thing to dispatch |

`claimed` is the one this command reads more strictly than a board does. For a
single board a `claimed` PRD is *in flight* rather than refused; across the
machine the PRD sits in somebody's window right now, and offering the row
again is a double-book.

**A question standing on one PRD does not empty its board.** The gate is
scoped to the asker, so every ungated row on that board still reaches the
frontier and still enters a wave.

## The waves

Three gates, in order: the PRD's own `dispatchable` verdict, the slot count,
and a footprint clash with something already in this wave.

A footprint is `realpath`'d against the board's **parent** directory, not
`plan.prd_repo` — the walk stops at the board itself for a board kept as a git
worktree of its own code repo, and every path would then resolve under
`.pearde/` where no such file exists. Real paths are what is compared, so two boards'
`resources/x.py` are different files, and one file reached through two
symlinks is one file. Two PRDs whose footprints resolve to the same path never
share a wave; the later one prints `footprint clash with @<board>/<rel>` and
falls to the next. The clash serialises the pair and nothing else.

**The waves are the plan; the pool is the plan run.** `dispatch` does not walk
the waves as barriers: a rolling pool `slots()` wide starts a queued row the
moment a slot is free and nothing **in flight** clashes with its real-path
footprint. The same guarantee holds — never two writers on one real path —
without the barrier: wave 2's first row starts when wave 1's clashing
row is in, not when wave 1's slowest is. The printed cut is still what a person
reads to see the shape of the run.

## The slot count

`slots()` returns the count **and the reading that produced it**, and no
caller prints one without the other: a cap nobody can see is a cap nobody can
debug.

Floor 1, ceiling `machine-ceiling` (@references/settings.md, default 12), and
a load-derived value between. Load only ever lowers the count; the ceiling is
what protects the user. The reading names the cpu term and the memory term
with their raw numbers, so the binding one is visible rather than asserted.

`machine-ceiling: 0` lifts the ceiling, and reads as unlimited the same way
`workers: 0` and `pipeline: 0` already do here: the load-derived count with
the floor under it and nothing above it, printed `ceiling ∞`. The count is
never printed as a bare `0`, which reads as *no slots* and means the opposite. The
default does not move — an untouched board still gets the measured 12, and
only an explicit `0` lifts the cap, because unlimited is a thing a person
chooses rather than inherits. One case has no obvious answer and so is stated
rather than guessed: a machine that cannot be read at all, on a board with no
ceiling set, holds at the measured 12 and says so — with no load term to hold,
and no number the person gave to hold instead.

Two measured gotchas are coded and commented in the file:

- **`vm_stat`'s "Pages free" is not available memory.** Counting it alone read
  31.9 of 32 GiB used on a machine with 19.7 in use, and pinned the meter to
  its floor. Free, inactive, speculative and purgeable are summed. On linux
  the same question is `MemAvailable`, which the kernel answers itself.
- **`load1` lags in both directions.** Measured 2026-09-02: six busy cores
  moved it 2.14 → 3.31 in 20 s, and after a 12-core burn ended it read 20.58
  and stayed high for minutes. So it throttles late and recovers late.

The mitigation is a second opinion asked **only on the throttle path**: when
the load-derived count would fall to the floor and cpu is the binding term, a
one-second instantaneous sample is taken — `top -l 2 -n 0 -s 1` on darwin, two
reads of `/proc/stat` elsewhere — and if the machine is genuinely free the
sample is used instead and the reading says `load1 stale`. A quiet machine is already at
the ceiling and needs no confirming, so it spawns nothing. The residual
weakness is stated in the file: a one-second window can read a bursty machine
either way, and the floor of 1 is what makes that safe — the worst reading
still makes progress.

`demand <n> at once, unconstrained` is printed beside the reading: the sum of
every board's `peak`, which is what the boards ask for against what the
machine will give. The sum is `plan.py`'s own number added up, not a second
schedule.

## Dispatch

`pearde machine dispatch` is the one verb that moves, and
@resources/board/dispatch.py is where it lives — imported lazily, so the read
path never loads it. The order, its waves and the slot reading are printed
**before the first launch**: what is about to happen is on screen before
anything starts.

| flag | what it does |
|---|---|
| `--dry` | prints one `would <addr> · <prompt> in <cwd>` per row it would launch, and starts no process |
| `--once` | fills the pool once, reports, and returns — no waiting for the fill to drain |
| `--workers N` | overrides the load-derived count and says `(override)` in the reading. Without it the count is `slots()` |
| `--adapter <id>` | which adapter to launch. With two or more configured and none named it refuses with the list rather than picking one |
| `--deadline S` | stops **filling** after S seconds and names what is still in flight. It kills nothing |
| `--group <g>` | only the boards declaring `<g>`, applied to the READ before anything is planned — the pool, the waves and the count are that group's, and no board outside it is ever a launch candidate. `machine <group> dispatch` is how it is normally set |

Launching goes through `serve.load_adapters` and `serve.adapter_bin` — the
same adapter set, the same `PEARDE_ADAPTER_BIN` override and the same
`<board>/.state/run-<rel>.log` the view's Start button and the daemon's `/run`
use. One launcher and one trail, not two.

**A launch is not a worker.** The slot meter is a reading of this machine, and
what actually bounds the machine is the model gateway: a 402 or a 429 arrives
as a process that starts, prints an error and exits, so a dispatcher counting
`Popen` returning would give the slot away and report the row as worked. Two
tests separate a launch from a worker, and neither works alone:

- a **launch grace window** (`PEARDE_LAUNCH_GRACE`, default 2 s) — a process
  that exited 0 inside it never worked anything. Only ever consulted on a
  process that has already exited, so a worker that dies at second 30 is not
  caught here;
- a **scan of the run log** for `API Error`, `credit balance`, `insufficient
  quota`, `402`, `429`, `rate limit`. Only consulted on an exited process,
  because a 429 retried and recovered from appears in the log of a perfectly
  live worker.

A dead worker is re-dispatched **once** on the same terms; a second death is
named with the error line quoted, never paraphrased, and the command exits
non-zero when anything died — a run that dispatched nothing living must not
read as success.

**The claim gate is re-asked at the launch.** `frontier` reads every board
once, and between that read and the moment a row starts, a session on that
board may have claimed it or opened a question. So each row's board is
re-scanned and `transitions.gate_claim` — the same predicate `pearde claim`
asks — is put to it again, with no claim of the dispatcher's own written: the
session it launches claims the PRD for itself. A refusal prints
`skip <addr> · <reason>` with the gate's verdict verbatim and the row is
skipped; a board failing to scan is skipped by name and the rest of the
machine still dispatches. Nothing is dropped without a printed reason, and
every refusal is in the closing `dispatched N · refused N · dead N`.

Between them, `machine.progress` is printed at every transition — a worker
coming in, or one finally declared dead — with `· in flight <n> · in <n> ·
skipped <n> · dead <n>` for the run itself on the end of it. A line per poll
would be a log; one line per transition is a state.

**Dispatching changes none of the three things below.** No write door appears
on `all`, no registry of boards is written, and no board's `settings.md` is
touched — a board's own `workers:` is **read** through `plan.plan_workers` and
honoured as a per-board cap under the machine-wide count (`workers: 0` imposes
no cap), and `--workers` is a dispatch-time override that lives on the command
line and nowhere else.

## What it does not do

- **No write door on `all`.** This command adds nothing to that page and takes
  nothing from it. @references/parts/all.md's *"nobody works it"* stands
  untouched; `machine` is a separate command over the same watch set, and the
  page stays a display.
- **No persisted registry of boards, and none of groups.** The watch set is
  the whole configuration and a board's own `groups:` is the whole of its
  membership. Nothing here writes a list of boards, and nothing here starts
  a daemon from a directory with no board — a cold daemon watches nothing, so
  starting one would buy an empty watch set and a stray process.
- **No board's `settings.md` written.** `machine-ceiling` is read, off the
  board at the cwd when one exists, and `groups:` is read off every watched
  board as the walk passes it. Not written, not defaulted into a file,
  not proposed.
