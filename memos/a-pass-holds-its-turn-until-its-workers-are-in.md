---
memo: a-pass-holds-its-turn-until-its-workers-are-in
kind: invariant
status: decided
tags:
  - memo
  - kind/invariant
  - status/decided
subject: a background worker does not outlive the pass window that dispatched it, so a pass returns only once every worker it dispatched is in or measurably dead
date: 2026-09-03
verify: bash resources/invariants/a-pass-holds-its-turn-until-its-workers-are-in.sh
prds:
  - a-pass-holds-its-turn-until-its-workers-are-in
---

# a-pass-holds-its-turn-until-its-workers-are-in — a return is also a kill

## Decision

A `pearde-pass` worker holds its turn until every worker it dispatched has
returned or is measurably dead. Returning any verdict with children in flight
kills them, so it is not a return the pass may make. The hold is active: each
report is collected as it lands and whatever it unblocks is dispatched in the
same turn.

Nothing about the ceiling moves. A pass at `context-budget` still writes its
pass file and hands back `MORE` — after its workers are in, not instead of
waiting for them. Nothing about liveness moves either: the transcript check
tells a dead worker from a live one, and a dead one leaves flight the same way
a returned one does.

The rule is stated in @references/parts/loop.md, in
@references/parts/dispatch.md, in @references/parts/workers.md's liveness
paragraph and in @references/agents/pearde-pass.md's verdict table, and
`verify:` fails the moment any of the four loses it — seven phrase assertions,
each proved able to go red.

## Why

Measured 2026-09-03 on this repo. The pass that ended 09:59 dispatched six
workers in its last turn and returned. Their subagent transcripts stop between
10:02 and 10:10, hold no `API Error`, and no process of theirs survived; five
wrote no specs. The next pass found five PRDs `analyzing` over empty `specs/`
directories, and `sweep --apply` dropped 44 uncommitted paths across their four
lanes — what the dead workers had built before they died. Seventy-five minutes
and five analysts bought nothing, and the board read the corpses as live work
for a full `claim-ttl`.

The liveness check had passed. It verifies a worker is alive *before the turn
ends*, which is what a pass does one line before ending the turn that kills it,
so the check alone certifies the workers it is about to burn.

## Alternatives considered

**Let workers outlive their pass** — decided against in
`the-board-assumes-unlimited-agents`, and the reason has not changed: a
background agent's life past its parent's return is not something this harness
promises. Building on it would make every dispatch a bet on an undocumented
behaviour of the runtime.

**Keep the liveness check as the whole rule** — it is what shipped, and it is
what failed. A check for death is not a rule about waiting.

**Return a status while workers run, and let the dispatcher poll** — the
dispatcher holds no board state and opens no file but its own; a status line
is not a verdict, and @references/parts/dispatch.md already names it the one
lie a run can tell in the user's voice.

## Consequences

- A pass window lives as long as its slowest worker. That is the cost, and it
  is smaller than re-dispatching the whole set: the alternative was measured at
  seventy-five minutes for nothing.
- A worker whose infrastructure kills it still ends the hold — dead is in, and
  `MORE` goes out with the PRD swept or resumed per the loop.
- It does not stop a pass from dispatching while it holds. The hold is on the
  return, never on the board.
