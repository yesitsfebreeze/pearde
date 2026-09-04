---
state: superseded
origin: requested
priority: 50
complexity: 0
blast-radius:
---

# one command works the busiest board on the machine from any directory

## Superseded 2026-09-02

Absorbed whole by `the-whole-machine-is-worked-as-one-board`, filed the same
day. That PRD keeps this one's three settled forks verbatim — `all` stays a
read-only page, discovery is `serve.py ensure` + `/status` with no new
registry, and `workers: 5` is a dispatch-time override — and drops the one line
this contract turned on: *"not a simultaneous round over every board."* The user
asked for exactly that simultaneous round, so the two contracts overlap rather
than compose, and one of them had to go.

The user's words, 2026-09-02: *"since we have the all board, what I want to
do is that we can work on that all board from any directory. It doesn't
matter when we run `pearde-all`. We're looking at the `all` board, figure
out what the next best move is, and then work on that. That also means for
the all board we can increase the agents to five per board. And generally
have a much better overview of what we need to do and why over the whole
system."*

Settled in conversation, before this was filed — the three forks that would
otherwise block speccing, each closed by the user's own pick:

1. **Relation to `all` and to master.** `all` (@references/parts/all.md)
   stays exactly what it is today — a read-only page, no write door, nobody's
   orchestrator. A master (@references/parts/master.md) stays exactly what
   it is — one board, static `members:`, one orchestrator working it. This
   PRD adds a **third, new thing** — a `pearde-all` command/skill that reads
   the same merged watch-set `all` renders and *works* it, without touching
   either existing invariant. `all.md`'s "nobody works it" line and
   `master.md`'s "master is not `/board/all`" line are not to be edited by
   this PRD; if the analyst finds this contract cannot be built without
   loosening one of them, that is a REFINE back to the user, not a quiet
   edit.
2. **Board discovery, from a cold directory with no daemon up.** No new
   machine-wide registry. `serve.py`'s own docstring/comments call that
   settled and gone (`resources/board/serve.py` — `daemon_pids()`:
   *"there is no machine-wide registry to consult — that is settled and
   gone"*; `cmd_run`: *"there is no machine-wide list to read"*). `pearde-all`
   discovers boards the same way `pearde view status` already does: it
   ensures the daemon is up (`serve.py ensure`, the same call `pearde view`
   makes — no board argument required when run outside any board's repo)
   and reads `/status`'s `boards: [{name, path, ...}]`. A board this
   session has never opened once via `pearde view`/`pearde-all` is not
   discoverable — that is the existing, accepted shape of "every board this
   machine watches" (@references/parts/all.md: *"a member nobody watches is
   not one of them"*), carried over rather than fixed.
3. **The workers=5 bump is scoped to `pearde-all`'s own dispatch.** Every
   board's own `.pearde/settings.md` `workers:` default is untouched (3
   plain, 6 master, per @references/settings.md and
   @references/parts/master.md). When `pearde-all` picks a board to work and
   dispatches implementers on it, it uses 5 concurrent slots for that
   dispatch — an override passed at dispatch time, not a value written back
   into that board's `settings.md`. A board worked directly (not through
   `pearde-all`) keeps its own configured `workers:`.

**What exists when this is done.**

- A `pearde-all` skill (`skills/pearde-all.md` → `references/skills/pearde-all.md`,
  wired into `SKILL.md`'s and `index.md`'s lists the way every other skill
  is) and, if the analyst finds the logic does not fit in the skill body
  alone, a script under `resources/board/` it points at — the repo's own
  rule from `index.md`: *"Anything executed... lives under `resources/`,
  whole."*
- Run from **any** directory, with or without a `.pearde/` above the cwd:
  `pearde-all` (a) ensures the daemon is up, (b) reads its `/status` for
  every registered board's name and path, (c) for each one computes the same
  single-most-urgent-decision `pearde next` already computes for one board
  (@references/parts/order.md's pressure order — drill, collect, waiting on
  a person, in flight, ready, gated), (d) picks the one action that is most
  urgent **across the whole set**, using that same pressure order as the
  cross-board tie-break (a `collect` waiting anywhere outranks a `ready`
  anywhere; within one rung, `all.py`'s existing dash sort — asks+collect,
  then weight left — orders the boards), and (e) names the board, the PRD,
  the step, and why it won, before doing anything else. This is "figure out
  what the next best move is" made literal and printed, not silent.
- Then it works that one board's next step through the existing loop
  (@references/parts/loop.md), unchanged, with `workers=5` for that
  dispatch only, exactly as decided in fork 3. It is one `pearde-pass`-style
  round over the board that won, not a simultaneous round over every board —
  "the next best move," singular, is the ask; fanning out across every
  board's frontier at once is explicitly not this PRD (a future one, if
  wanted).
- `doctor` grows no new row for this — there is nothing installed to check
  beyond the skill file itself, which the existing skill-tree check already
  covers.

**Constraints and non-goals.**

- Never a second orchestrator on a board another session already holds —
  the existing one-writer-per-file / claim discipline
  (`.pearde/memos/several-sessions-write-one-board.md` if such a memo
  exists on this board, else the mechanism in @references/parts/pass.md and
  `pearde sweep`) applies to a board `pearde-all` reaches exactly as it
  applies to a board opened directly. `pearde-all` claims through the same
  `pearde claim`, refused by the same gates, on the board it picked.
  Concretely: never dispatch on a board another live session already has
  claimed work on if that is visible from the scan — refuse and say why it
  moved to the next board, the same way `claim` itself refuses.
- Not in scope: giving `all` a write door; a persisted cross-session
  registry of boards; changing any board's own `workers:` default; a mode
  that works every board at once rather than picking the single next best
  move.
- The merge math to reuse (qualifying rels `@<board>/<rel>`, dropping a row
  that already carries a `board`, the pressure-order sort) already exists in
  `resources/board/all.py` and `resources/board/plan.py` (`next`) — read
  both before writing new arithmetic; a second implementation of either is
  the kind of drift @references/parts/all.md warns against ("a second
  arithmetic here is how the two would come to disagree").

**Pointers.** @references/parts/all.md, @references/parts/master.md,
@references/parts/loop.md, @references/parts/order.md,
@references/settings.md, `resources/board/all.py`, `resources/board/plan.py`
(`next`, `scan`), `resources/board/serve.py` (`cmd_status`, `cmd_ensure`,
`/status` route — board discovery lives here), @references/parts/handles.md,
@index.md's `@@all` and `@@master` rows.
