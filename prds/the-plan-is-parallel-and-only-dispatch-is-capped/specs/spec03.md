---
complexity: 4
footprint:
  - resources/board/mapfile.py
  - references/parts/view.md
---

# spec03 — the view's own wording matches what the plan now claims

`after` stays computed and the map keeps the pairs so the Gantt can still
draw a footprint clash — `spec01`/`spec02` change what the number MEANS,
not whether it exists. The prose that describes it, in the code comment
that builds the payload and in the reference page a person reads, said the
clashing PRD "starts when" the other ends. That is no longer true — the
schedule the view draws is `needs:` alone — and left standing it is a wrong
claim about the tool's own behaviour, the kind `references/files.md` and
`memos.py check` exist to catch when it drifts far enough to be checkable.

**What stands** — `resources/board/mapfile.py`'s `after=` comment no longer
claims the clash orders the two PRDs' `startDay`/`endDay`; it says what is
true instead — `dispatch` will serialise the pair, on the real in-flight
set, and this field is a report of that, not an input to the schedule
above it. `references/parts/view.md`'s footprint-clash bullet says the same
thing for a person reading the Gantt, and names where the other honest
number lives — `pearde plan`'s own text, printed by `spec02` — rather than
promising the HTML view itself draws a ceiling it does not. The
peak-agent-count bullet is corrected the same way: `workers:` is
`dispatch`'s cap, not a fact the drawn calendar uses, and setting it moves
no bar; `plan --workers N` is named as the one place that other, staffed
view exists, and it is the command line, not this page.

**What is left** — `resources/board/view.js`'s rendered tile text (`"at " +
DATA.workers + " workers: " + fmtW(cal)`) still phrases the peak-agents
tile as if the board's `workers:` setting shapes the drawn calendar it sits
beside. It does not any more — the view always calls `compute_plan(board,
None)`, so `cal` is now unconditionally the floor. Fixing the tile's own
wording without misleading the other way (implying the tile now shows a
band, which it does not draw) is a small but real edit to a third file
this spec's footprint does not carry; reported as a finding rather than
folded in here.

## Acceptance

- [x] `resources/board/mapfile.py`'s `after=` comment makes no claim about
      `startDay`/`endDay` moving because of a footprint clash
- [x] `references/parts/view.md`'s footprint-clash bullet does not say a
      clashing PRD "starts when" another ends
- [x] `references/parts/view.md`'s peak-agent-count bullet does not say a
      `workers:` cap changes what the drawn calendar costs
- [x] `python3 resources/index.py check` names neither edited file — the
      correction is prose, not a moved or renamed anchor

## Verify and Proof

```sh
if grep -n 'starts when' resources/board/mapfile.py references/parts/view.md; then
  echo "FAIL: overstated claim still present"; exit 1
fi
if grep -n 'the header shows what the cap costs beside the peak' references/parts/view.md; then
  echo "FAIL: stale peak-agent-count claim still present"; exit 1
fi
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
printf '%s\n' "$out"
if printf '%s\n' "$out" | grep -E '(^|@)(resources/board/mapfile\.py|references/parts/view\.md)([ ,:]|$)'; then
  echo "FAIL: index check now names an edited file"; exit 1
fi
echo "PASS: wording corrected, no new drift"
```
