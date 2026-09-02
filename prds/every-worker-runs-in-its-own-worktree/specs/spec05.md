---
complexity: 6
footprint:
  - resources/board/plan.py
  - references/parts/states.md
  - references/parts/loop.md
  - references/parts/machine.md
  - references/parts/progress.md
  - references/parts/order.md
---

# spec05 — the footprint clash is an edge, not a gate

Two PRDs on one file are two branches, not two writers in one tree. The
plan still orders them; `claim` stops refusing them.

**What stands** — the clash loop is out of `dispatchable` in
`resources/board/plan.py`, with the reason in its place, and the gate is
off the docstring's list. The scheduler edge is untouched and was already
separate machinery: `compute_plan` serializes the pair with `after`, and
`cmd_plan` prints `after … (footprint)`.

**What is left** —

- `SKIP` in `resources/board/brief.py` maps `footprint` to `clash`. The
  gate no longer raises it, so the entry is dead — drop it here, in this
  spec, so one dict has one editor.
- `references/parts/states.md` and `references/parts/loop.md` name the
  footprint clash among the gates `claim` runs. Both must say instead that
  the clash orders the pair in the plan and is resolved at the merge.
- `cmd_scan`'s `gated` section partitions on `dispatchable`'s answer. A
  clashing PRD now lands in `ready`, which is the intent — check the count
  lines still read true and that nothing prints an empty `gated` header.
- The claim was the board's only serializer for two PRDs on one file. Now
  the merge is. Say that where a reader meets it: a person who sees two
  PRDs claimed on `src/` should know the second one's collect can come back
  red on a conflict, and that this is the designed outcome, not a break.

## Acceptance

- [x] `pearde claim` takes a PRD whose footprint overlaps a `claimed` PRD's
- [x] `pearde scan` lists that PRD under `ready`, not under `gated`
- [x] `pearde plan` still orders the clashing pair, printing `after … (footprint)`
- [x] no file under `references/` names the footprint clash as a gate on `claim`
- [x] `resources/board/brief.py` no longer maps a `footprint` gate word
- [x] `python3 resources/index.py check` and `python3 resources/memos.py check` both print nothing

## Verify and Proof

```sh
grep -q 'footprint' resources/board/plan.py
if grep -n 'footprint:' resources/board/plan.py | grep -q 'is claimed and holds'; then exit 1; fi
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
printf '%s\n' "$out"
if printf '%s\n' "$out" | grep -E '(^|@)(resources/board/plan\.py|references/parts/(states|loop|machine|progress|order)\.md)([ ,:]|$)'; then exit 1; fi
mout=$(python3 resources/memos.py check 2>&1) && mrc=0 || mrc=$?
printf '%s\n' "$mout"   # board-wide: visible, never the exit
```
