---
complexity: 5
footprint:
  - resources/board/dispatch.py
---

# spec04 — one progress line over the merged set, on every transition

A person watching a machine-wide dispatch must read the machine, not ten
boards. `machine.progress` is already that line; this unit prints it at every
transition — the same moment the board prints one for a single board
(@references/parts/progress.md) — with what this run is holding on the end of
it, and closes with a tally that accounts for every row.

## What already stands

`dispatch.live_progress` and the `tick` hook in the probe. Against this repo:

```
▸ machine: 1 boards · done 71/76 · 94% · derived 22/23 · open 4/103 · 4% · ready 4 · blocked 0 · collect 1 @12 workers · as engineer
dispatched 3 · refused 1 · dead 0
```

## What is left

Nothing but the move with spec01.

## Design notes

- **`machine.progress` is not re-derived.** The dispatch counts are appended to
  the line it returns, so the two sums that must not be recomputed by hand —
  the weight fraction and the derived band — stay in `plan.progress_terms`.
- **A transition, not a tick.** The line is printed when a worker comes back in
  or is finally declared dead, not on every poll: a line per half-second is a
  log, and this is a state.
- **The frontier is re-read for it**, so the counts move as the workers move —
  a board whose PRD went `done` shows it on the next line rather than at the
  end.
- **The closing tally is `dispatched N · refused N · dead N`**, and the three
  plus the rows the frontier never offered account for the whole list.

## Acceptance

- [x] The merged progress line is printed once before the first launch and once after the last worker is in
- [x] It is printed again each time a worker returns in or is declared dead, and not on a poll that changed nothing
- [x] The line matches `@references/parts/progress.md`'s register and is produced by `machine.progress`, not rebuilt
- [x] Each line carries `· in flight <n> · in <n> · skipped <n> · dead <n>` for the run itself
- [x] The line's board counts are re-read from the boards, so they change as workers finish
- [x] The run ends with `dispatched <n> · refused <n> · dead <n>` on its own line
- [x] `--dry` prints the same lines with nothing in flight

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
set -e -o pipefail
d=$(mktemp)
( cd / && python3 /Users/feb/dev/infra/pearde/resources/board/machine.py machine dispatch --dry ) > "$d" 2>&1
[ -s "$d" ]
# machine.progress produces the line; dispatch.py appends this run's counts
grep -q 'mach.progress(entries, rows, wv, nslots)' resources/board/dispatch.py
grep -q 'in flight {len(live)} · in {len(done)}' resources/board/dispatch.py
# printed before the first launch and again at the end
n=$({ grep -cE '^▸ machine: [0-9]+ boards · ' "$d" || true; })
[ "$n" -ge 2 ]
# and the closing tally, on its own line
grep -qE '^dispatched [0-9]+ · refused [0-9]+ · dead [0-9]+$' "$d"
# a transition prints it, a poll does not
python3 .pearde/prds/the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-dispatched-in-parallel/probe/fixture.py alive
```
