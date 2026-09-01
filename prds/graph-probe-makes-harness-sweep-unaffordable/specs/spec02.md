---
complexity: 5
footprint:
  - .pearde/prds/graph-probe-makes-harness-sweep-unaffordable/probe/verify.sh
---

# spec02 — the sweep's affordability is checked, not assumed

The affordance that let one probe cost minutes inside the sweep was that
nothing measured what a harness costs: the row advertises itself as "the one
row measured in tens of seconds", and no check anywhere fails when a harness
blows past that. This spec stands up the permanent check: a harness of this
PRD's own that (a) reads every `verify.sh` under the board and fails if any
runs `graph.sh extract` against a real corpus that can carry documents —
extract is affordable only code-only or on a run-time fixture — and (b) runs
the graph probe end-to-end with a stopwatch and fails past 60 seconds.

**What already stands (analyst pass one, uncommitted in the tree):** the
harness is written and green — 4 checks, 4 pass, ~2 s. Its checks A and B are
in the file; the census in the gate harness now reads 45 harnesses and this
one is counted.

**What is left:** confirm the two reds this PRD's build must flip are flipped
— the gate harness's census J (was `got: 43 · want: 44`, then `44 · 45` with
this PRD's harness added) and the sweep row's wall-clock (the graph probe's
share drops from unbounded to ~2 s of the ~67 s row).

Note the honest boundary: doctor's sweep row on the committed tree was already
red for reasons this PRD does not own (the tree carries other workers'
uncommitted edits; the census counted the graph probe's non-carrying exit).
Those reds belong to their own PRDs; the affordability contract this spec
closes is that no harness makes the row unaffordable, not that the row is
green.

## Acceptance

- [x] `bash .pearde/prds/graph-probe-makes-harness-sweep-unaffordable/probe/verify.sh` exits 0 and prints a line ending `0 fail`
- [x] its check A fails when a harness is temporarily given a bare `extract "$REPO" --force` line and passes again once it is removed (the check can fail)
- [x] `bash .pearde/prds/the-gate-runs-the-harnesses/probe/verify.sh` reports the census with `got` equal to `want` for the exit-carrying count
- [x] the sweep's `harnesses` row, run with `--harnesses`, completes with the graph probe contributing seconds, not minutes

## Verify and Proof

```sh
bash .pearde/prds/graph-probe-makes-harness-sweep-unaffordable/probe/verify.sh
bash .pearde/prds/the-gate-runs-the-harnesses/probe/verify.sh 2>&1 | grep census
bash resources/doctor.sh --harnesses . 2>&1 | grep -E "harnesses|graph-lands"
```