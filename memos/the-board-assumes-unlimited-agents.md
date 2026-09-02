---
memo: the-board-assumes-unlimited-agents
kind: decision
status: decided
subject: the plan, the pass and the drill assume every dispatchable PRD runs at once; a worker cap is a person's setting, never the plan's clock
date: 2026-09-02
---

# the-board-assumes-unlimited-agents — the dependency structure is the only schedule

The workers are agents. An agent starts the moment its gates clear and costs
nothing while it does not exist, so a staffing number has no place in the
plan. Measured on 2026-09-02 across this machine's boards: `mitosys` printed
a 441-unit wall at `workers=5` against a 386-unit critical path; `model` 329
at `workers=3` against 258. Neither number was the plan — both were a cap
the board had been told to pretend was staffing.

The cap was not the largest serializer. Four mechanisms in the skill held
work back before any plan was drawn, each written for a world of three
workers:

1. **The pass batched.** `transitions-per-pass` counted claims, and a pass
   held its turn until every worker it dispatched was in — so eight PRDs went
   out, the ninth waited for the slowest of the eight, and nothing a return
   unblocked was dispatched until the next window.
2. **The brief entered the pass's window.** Eight kilobytes per dispatch,
   pasted as the worker's prompt, paid for again on every turn of the pass.
   Twenty dispatches cost the window forty thousand tokens it never read.
3. **Two questions stopped the whole board.** `pearde claim` refused every
   PRD with `asking N — drill first`, when a question on one PRD can reshape
   only that PRD, its ancestors, its descendants and what needs them.
4. **Nothing told an analyst that a wide footprint or a chained split is a
   serial board.** One PRD footprinting `src` put eight of fourteen live PRDs
   on `model` behind it; a `## Split` whose children each need the previous
   runs nothing at once.

## Decision

- `workers: 0` and `pipeline: 0` are unlimited, and the default. A number
  is a cap a person sets for a rate limit or a budget. The plan's simulation,
  its `order` and its wall are the unconstrained critical path; `peak` says
  how many agents that path asks for at its widest.
- A worker's prompt is the brief **command**. The worker runs `pearde brief`
  in its own window; the brief never enters the pass's.
- A pass dispatches everything dispatchable every time the board moves.
  `transitions-per-pass` is spent on returns, and `MORE` goes out only when
  the count is spent and nothing is in flight. `next` prints the whole
  actionable set for one turn, not its first line.
- The drill gate is scoped: the asker, its ancestors, its descendants and
  what `needs:` one of them wait; the rest of the board dispatches before
  the pass is put.
- `specced` warns on a footprint directory over `footprint-above` tracked
  files; `refine` warns on a split that is one chain. The analyst's brief and
  the drill's output rule both say: siblings own disjoint files and `needs`
  only where one consumes what another makes.

## Alternatives considered

**Keep the cap and tune it per board** — the header already printed the
peak beside the cap; nobody moved the cap, because the number looked like a
fact about staffing. A default that is right is better than a dial.

**Refuse a wide footprint or a chained split** — a rename across a tree is
legitimately wide and legitimately first. The line says what it costs; the
analyst decides.

**Let workers outlive their pass** — would remove the batch boundary
entirely, but a background agent's life past its parent's return is not
something this harness promises. The pass holds instead, and dispatches on
every return.

## Consequences

- Every worker still edits one working tree. Unlimited analysts probing one
  repo can collide on a file no footprint yet names — the footprint gate
  covers `claimed` PRDs only. The PRD
  `every-worker-runs-in-its-own-worktree` is the fix; until it lands,
  `pipeline` is the knob to set on a board where that happens.
- A board with `workers: 6` written keeps its cap; `pearde settings
  workers=0` lifts it.
