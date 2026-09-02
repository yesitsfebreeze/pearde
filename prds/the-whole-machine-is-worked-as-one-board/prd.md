---
state: open
origin: requested
priority: 80
complexity: 0
blast-radius:
---

# the whole machine is worked as one board

The user's words, 2026-09-02: *"Now we can just work over all the boards like
we are working on it like a master board. Everything that is able to be done in
parallel we can do in parallel. We can look at all the PRDs, we can sort them,
all of that."* — and, from the same conversation, *"when we call it we are just
working on all boards globally, no matter where we start the session from."*

This **replaces** `one-command-works-the-busiest-board-on-the-machine-from-any`,
filed earlier the same day and set `superseded` by this PRD. That contract read
the whole watch set and then worked **one** board — the single most urgent move,
singular, with fan-out named as a future PRD. This is that future PRD, and it
absorbs the earlier one whole rather than sitting beside it: one contract, not
two overlapping ones. Its three settled forks are carried below unchanged,
because they are still the answers.

## What exists when this is done

A `pearde-all` skill (`references/skills/pearde-all.md`, wired into `SKILL.md`
and `index.md` the way every other skill is) and, where the logic does not fit
in a skill body, a script under `resources/board/` it points at — this repo's
own rule from @index.md: *"Anything executed... lives under `resources/`,
whole."*

Run from **any** directory, with or without a `.pearde/` above the cwd, it:

1. ensures the daemon is up — `serve.py ensure`, the same call `pearde view`
   makes, no board argument required outside a board's repo;
2. reads `/status` for every board the daemon watches — name and path;
3. merges their PRDs into **one ordered frontier**: the same qualification
   `all.py` already does for the page (`@<board>/<rel>`, dropping a row that
   already carries a `board`), ordered by the same three axes `plan.py` already
   computes for one board (@references/parts/order.md — dependency, vision
   importance, complexity and blast-radius). One list, not one list per board;
4. **prints that order before it moves anything** — every row, its board, and
   the rung it sits on. "Look at all the PRDs, sort them" is the deliverable,
   visible, not an internal step;
5. dispatches across that frontier **in parallel wherever parallel is legal**,
   and works each dispatch through the existing loop (@references/parts/loop.md)
   unchanged.

It is an **ephemeral master over the watch set**: it plans and dispatches the
way a master does over its members, and nothing on disk declares it. The watch
set is the whole configuration.

## The forks already settled — carried forward, still the answers

1. **Relation to `all` and to master.** `all` (@references/parts/all.md) stays
   exactly what it is: a read-only page, no write door, and its *"nobody works
   it"* line stays true — the page is still not worked; the **boards** are, each
   through its own door. A master (@references/parts/master.md) stays exactly
   what it is: a board with static `members:` and one orchestrator. Neither
   line is to be edited by this PRD. If the analyst finds the contract cannot
   be built without loosening one, that is a REFINE back to the user, not a
   quiet edit.
2. **Board discovery from a cold directory with no daemon up.** No new
   machine-wide registry — `serve.py` calls that settled and gone
   (`daemon_pids()`: *"there is no machine-wide registry to consult"*;
   `cmd_run`: *"there is no machine-wide list to read"*). Discovery is
   `ensure` + `/status`, as above. A board this machine has never watched once
   is not discoverable; that is the accepted shape of "every board this machine
   watches" (@references/parts/all.md: *"a member nobody watches is not one of
   them"*), carried over rather than fixed.
3. **`workers: 5` is scoped to this dispatch.** Every board's own
   `.pearde/settings.md` `workers:` is untouched (3 plain, 6 master, per
   @references/settings.md). Five concurrent slots is an override passed at
   dispatch time, never written back into a board.

## What fan-out adds, and the two things it makes dangerous

**The machine ceiling is an open fork.** Fork 3 fixes five slots *per board*.
Five times however many boards the daemon watches is not a number anyone chose,
and it is the number that decides whether this command is usable. The analyst
settles it from what the board already knows, or asks it as a `## Questions`
fork — it does not pick silently.

**Cross-board footprint overlap is real, and the reason to think it is not is
wrong.** Two boards are usually two repos, so two footprints cannot collide.
Except a board's `.pearde/` sits in a repo that another board's footprint
names, and **this checkout is exactly that case**: the pearde skills installed
on this machine are symlinks into this tree, so a pass on the *dotfiles* board
that edits a skill file is editing this repo. Two sessions spent 2026-08-28/29
on this board attributing precisely those edits to a phantom third writer. So
the overlap check that gates parallel dispatch resolves symlinks and compares
**real paths**, not board names or repo roots. A pair that resolves to one file
is serialised, however far apart the two boards look.

**Claim discipline is unchanged and applies across the set.** One writer per
file; `pearde claim` and the same gates that refuse it; never a second
orchestrator on a board a live session already holds. A board that refuses is
named and skipped with the reason, the way `claim` itself refuses — not
silently dropped.

**One progress line over the merged set**, in the register the board already
uses for one board (@references/parts/progress.md), so a person reading it sees
the machine and not a board.

## Constraints and non-goals

- No write door on `/board/all`; the page stays read-only.
- No persisted machine-wide registry of boards.
- No board's own `settings.md` is written.
- No `members:` file, no board on disk for this set.
- It does not replace master boards, and a master appearing in the watch set is
  worked as the one board it is.
- Not in scope: making an unwatched board reachable.
- The merge and the ordering already exist in `resources/board/all.py` and
  `resources/board/plan.py` (`next`, `scan`, `gantt_payload`). Read both before
  writing new arithmetic — a second implementation of either is the drift
  @references/parts/all.md warns against: *"a second arithmetic here is how the
  two would come to disagree."*

## Pointers

@references/parts/all.md, @references/parts/master.md,
@references/parts/loop.md, @references/parts/order.md,
@references/parts/dispatch.md, @references/parts/workers.md,
@references/parts/pass.md, @references/parts/progress.md,
@references/parts/handles.md, @references/settings.md,
`resources/board/all.py`, `resources/board/plan.py`, `resources/board/serve.py`
(`cmd_status`, `cmd_ensure`, the `/status` route), @index.md's `@@all`,
`@@master` and `@@skills` rows.

## Questions

### Q1: How much runs at once across your projects

You are choosing how many jobs this machine starts in parallel: one fixed
total, or five for every project it watches. It watches ten today, so five
each is fifty at once, competing for the same machine and the same budget?

1. **Five in total** — the machine runs five jobs at once however many projects it watches; the rest wait their turn. (recommended)
2. **Five for each project** — every project gets its own five, so ten watched means fifty running together: fastest, and heaviest.
3. **You set the ceiling** — it asks you for a number the first time and remembers it, and you change it whenever it feels wrong.

<!-- for the board: probe/machine.py waves() slot cap + DISPATCH_WORKERS; fork 3 of this PRD reads 5 as per-board, the probe capped 5 machine-wide -->

## Answers

**Q1** *(answered 2026-09-02 13:24)* — cant we do it dnyamically by load, so we use 80% power of the machine

## Children

| child | contract | needs |
|---|---|---|
| `the-machine-frontier-is-one-ordered-list` | Run from any directory, one command prints every watched board's PRDs as a single dependency-ordered frontier, with the concurrency it would use and the reading that produced it, and moves nothing | — |
| `the-machine-frontier-is-dispatched-in-parallel` | That frontier's waves are dispatched as pass workers across boards, serialised on real-path footprint clashes, claim refusals named and skipped, one progress line over the merged set | the-machine-frontier-is-one-ordered-list |
