---
state: open
origin: requested
priority: 65
repo: "/Users/feb/dev/cartridge/memory.ctg"
work-kind: leaf
---

# A spilled graph answers the same queries as one that never spilled

## Outcome

`memory::spill_transparency a_spilled_graph_answers_the_same_queries_as_one_that_never_spilled`
fails at memory.ctg 5097a83 with recall@10 0.8370 against a 0.84 floor, on 2 of 2 runs
(observed 2026-09-16 by the trust-fixture analyst). Find out whether this is a regression
from the DiskANN prune change (5097a83, collected today as
`@memory/diskann-builds-keep-every-node-reachable-from-the-entry-point`) or pre-existing at
a9ab81a. Fix the cause without lowering the threshold unless the test's floor is shown to
be wrong.

## Acceptance

- [ ] The test's result at a9ab81a and at 5097a83 is recorded (pass/fail and recall), and the cause is named at file:line.
- [ ] `cargo nextest run -p memory --test spill_transparency` exits 0 on 3 consecutive runs, with the threshold unchanged or its change justified by evidence in the spec.
- [ ] The DiskANN reachability and recall tests still pass.

## Proof and recovery

If this is a regression from 5097a83, revert the prune change in a lane and compare before fixing forward.
