---
atomic: update-stale-specs-and-probe
subject: a spec or a probe check that named the machinery the sibling moved is now testing something that no longer exists; the spec is rewritten to match the tree that exists, not re-derived from scratch
date: 2026-09-03
runs: 0
tags:
  - atomic
---

## Do

1. Grep each existing spec's body and `Verify and Proof` block for anything
   naming the file or function the blocking branch moved logic out of.
2. Reword the spec's "what already stands" narrative and its verify
   commands to the new location, and fix the probe's own check the same
   way — never leave a spec or a probe asserting a fact the merge just made
   false.

## Done when

- No spec and no probe check reads a fact through the file the blocking
  branch emptied out; `pearde specced`'s complexity/count sums are
  unchanged (this is a rewrite, not new specs).

## Fails when
