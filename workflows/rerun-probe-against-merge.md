---
atomic: rerun-probe-against-merge
subject: the PRD's own probe is the fastest way to know whether the reconciliation actually preserved every acceptance box, not just whether the merge produced valid syntax
date: 2026-09-03
runs: 0
tags:
  - atomic
---

## Do

1. Run the PRD's `probe/*.py` (or the spec's own `Verify and Proof` block)
   against the merged, uncommitted tree exactly as the prior pass ran it,
   and compare box-for-box against the last recorded run.

## Done when

- Every box that passed before still passes, and a box that fails names
  which side of the merge it is checking against something that moved — not
  a logic regression.

## Fails when
