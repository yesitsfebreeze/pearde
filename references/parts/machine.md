# `machine` — every watched board as one ordered frontier

What the whole machine should work on next, as one list, in the order it
should be worked, cut into the waves that could run at once.

```sh
pearde machine              # the frontier, the waves, and the reading behind them
pearde machine boards       # what the daemon watches, and each board's own cap
pearde machine slots        # the concurrency and the numbers that produced it
pearde machine progress     # one progress line over the merged set
pearde machine --json       # the same read, as data
```

It runs from anywhere. There need be no board above the cwd: the watch set is
the live service's, not the directory's, and @resources/board/machine.py is
found through `pearde.py`'s `COMMANDS` discovery rather than a path.

**It moves nothing.** No claim, no transition, no dispatch, no write to any
board, any settings file or any PRD. It reads and it prints. Dispatching the
waves it draws is the PRD `the-machine-frontier-is-dispatched-in-parallel`,
which is a separate unit precisely so that reading the machine and moving it
are never the same command.

## What it merges

- **Every board the daemon watches**, from `/status` — the same set
  @references/parts/all.md renders. Registering a board is the whole of
  joining, and **an unwatched board is not discoverable**: there is no
  persisted registry of boards here and none is written. A board that has
  never been registered is invisible to this command, on the same rule
  @references/parts/all.md states of its own merge — *a member nobody watches
  is not one of them*.
- **A row with no path is skipped**, with its reason printed. The `all` page
  sits in the watch set as exactly such a row; it is a render over the boards,
  never one of them, and it is never counted as a board.
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

## The marks

One column per row, and it agrees with the waves printed below it.

| mark | what it says |
|---|---|
| `ready` | it is in a wave. If the wave is not the first, the note says what pushed it there |
| `held` | `plan.dispatchable` refuses it — a parked child, a stale claim, a `needs:` not done, a footprint held by a `claimed` PRD. The note is that verdict, verbatim |
| `waits` | its state is not dispatchable. Only `open` and `specced` enter a wave; `claimed`, `analyzing`, `question`, `blocked` and `deferred` print `waits` with the reason and appear in none |
| `collect` | it is finished work `pearde collect` closes, not a thing to dispatch |

`claimed` is the one this command reads more strictly than a board does. For a
single board a `claimed` PRD is *in flight* rather than refused; across the
machine it is in somebody's window right now, and offering it is a double-book.

**A question standing on one PRD does not empty its board.** The gate is
scoped to the asker, so every ungated row on that board still reaches the
frontier and still enters a wave.

## The waves

Three gates, in order: the PRD's own `dispatchable` verdict, the slot count,
and a footprint clash with something already in this wave.

A footprint is `realpath`'d against the board's **parent** directory, not
`plan.prd_repo` — a board that is a git worktree of its own code repo stops
the walk at the board itself, and every path would resolve under `.pearde/`
where no such file exists. Real paths are what is compared, so two boards'
`resources/x.py` are different files, and one file reached through two
symlinks is one file. Two PRDs whose footprints resolve to the same path never
share a wave; the later one prints `footprint clash with @<board>/<rel>` and
falls to the next. The clash serialises the pair and nothing else.

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
the floor under it and nothing above it, printed `ceiling ∞`. It is never
printed as a bare `0`, which reads as *no slots* and means the opposite. The
default does not move — an untouched board still gets the measured 12, and
only an explicit `0` lifts the cap, because unlimited is a thing a person
chooses rather than inherits. One case has no obvious answer and so is stated
rather than guessed: a machine that cannot be read at all, on a board with no
ceiling set, holds at the measured 12 and says so — there is no load term to
hold, and no number the person gave to hold instead.

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
reads of `/proc/stat` elsewhere — and if the machine is genuinely free that is
used instead and the reading says `load1 stale`. A quiet machine is already at
the ceiling and needs no confirming, so it spawns nothing. The residual
weakness is stated in the file: a one-second window can read a bursty machine
either way, and the floor of 1 is what makes that safe — the worst reading
still makes progress.

`demand <n> at once, unconstrained` is printed beside the reading: the sum of
every board's `peak`, which is what the boards ask for against what the
machine will give. It is `plan.py`'s own number added up, not a second
schedule.

## What it does not do

- **No write door on `all`.** This command adds nothing to that page and takes
  nothing from it. @references/parts/all.md's *"nobody works it"* stands
  untouched; `machine` is a separate command over the same watch set, and the
  page stays a display.
- **No persisted registry of boards.** The watch set is the whole
  configuration. Nothing here writes a list of boards, and nothing here starts
  a daemon from a directory with no board — a cold daemon watches nothing, so
  that would buy an empty watch set and a stray process.
- **No board's `settings.md` written.** `machine-ceiling` is read, off the
  board at the cwd when there is one. Not written, not defaulted into a file,
  not proposed.
