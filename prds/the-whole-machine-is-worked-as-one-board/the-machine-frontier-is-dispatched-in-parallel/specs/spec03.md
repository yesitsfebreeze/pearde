---
complexity: 7
footprint:
  - resources/board/dispatch.py
---

# spec03 — the claim gate re-asked at the launch, and every refusal named

`frontier` reads every board once. Between that read and the moment a row is
launched, a session on that board may have claimed it, answered a question, or
opened a second one. So the gate is asked again, per row, against a fresh scan
of that one board, through `transitions.gate_claim` — the same predicate
`pearde claim` uses. A row that refuses is printed with its reason and skipped;
it is never dropped silently and never launched anyway.

## What already stands

`dispatch.refusal` in the probe, and the `refuse` fixture case. Against this
repo's own board it caught a real disagreement on the first `--dry` run:

```
skip @pearde/the-whole-machine-is-worked-as-one-board · leaf: the-whole-machine-is-worked-as-one-board has children not done — the-machine-frontier-is-dispatched-in-parallel
```

`machine` had marked that row `ready` and put it in wave 1. `plan.compute_plan`
only runs `dispatchable` over rows with **no dependency edge left**, so a
container that still has an edge is never examined and reaches the frontier
with `held` empty — while `claim` refuses it. The probe harness carries a row
that fails the moment the dispatcher stops re-asking.

## What is left

Nothing but the move with spec01. The read path is **not** changed here: this
PRD's contract is that refusals are named and skipped, and correcting
`compute_plan`'s hold band is a defect outside this footprint, reported rather
than fixed.

## Design notes

- **`gate_claim`, not `plan.dispatchable`.** `gate_claim` is `dispatchable`
  plus the drill gate, so a board carrying two unanswered questions refuses
  exactly the asker, its ancestors, its descendants and what `needs:` one of
  them — and dispatches everything else. That scoping landed in `3edf110` and
  is consumed here, not re-derived: a board with `asking N` still has a
  dispatchable frontier.
- **No claim is written.** The dispatcher asks the gate and launches; the
  session it launches claims the PRD for itself. Claiming here would leave the
  spawned session refused by its own board.
- **Three refusals, all named the same way**: the row moved state since the
  frontier was read, the row is gone from the board, or the gate refuses it —
  each returned as one sentence and printed as `skip <addr> · <reason>`.
- **The board's own error is a refusal, not a crash.** A board that will not
  scan is skipped by name; the rest of the machine still dispatches.

## Acceptance

- [x] Before every launch the row's board is re-scanned and `transitions.gate_claim` is asked, with `holder=None`
- [x] A refused row prints `skip <addr> · <reason>` where the reason is the gate's own verdict verbatim, with its gate word in front
- [x] A row whose state moved out of `open`/`specced` between the frontier read and the launch is skipped, saying so
- [x] A row that has left the board entirely is skipped, saying so
- [x] A board that raises while scanning is skipped by name and the remaining rows still dispatch
- [x] No row is launched that `pearde claim <rel> <worker>` would refuse at that moment
- [x] The dispatcher writes no `claim:` of its own into any PRD
- [x] Every refusal is in the closing tally's `refused` count, and no row is dropped without a printed reason

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
set -e -o pipefail
python3 .pearde/prds/the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-dispatched-in-parallel/probe/fixture.py refuse
# the gate `claim` asks, asked again per row, with no claim written
grep -q 'trans.gate_claim(row\["path"\], prds, prd)' resources/board/dispatch.py
grep -q 'gone from the board since the frontier was read' resources/board/dispatch.py
grep -q 'board unreadable' resources/board/dispatch.py
n=$({ grep -c 'claim:' resources/board/dispatch.py || true; })
[ "$n" = 0 ]
# against this board: every skip carries its reason, and the tally counts them
d=$(mktemp)
( cd / && python3 /Users/feb/dev/infra/pearde/resources/board/machine.py machine dispatch --dry ) > "$d" 2>&1
[ -s "$d" ]
{ grep -E '^skip @' "$d" || true; } | head -3
r=$({ grep -cE '^skip @[^ ]+ · .+' "$d" || true; })
t=$(sed -n 's/^dispatched [0-9]* · refused \([0-9]*\) · dead [0-9]*$/\1/p' "$d")
[ "$r" = "$t" ]
```
