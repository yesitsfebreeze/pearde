---
kind: work
level: 9
status: open
description: roll [[crates-are-hot-pieces]] across the compute crates — hygiene proven, retrieval and graph next, then the piece benchmark that runs a new dylib against the one it replaced
read_when: "picking the next crate to make hot, or asking how far the piece loop reaches"
---

# every-compute-crate-is-a-piece

## Do

Execute the children in order; each is one lane. A crate qualifies when its
surface is free functions over host-owned types — no generics, no `async` at
the boundary. The async shells are excluded by [[crates-are-hot-pieces]].

subwork: [[hygiene-is-the-first-piece]] [[retrieval-is-a-piece]]

On 2026-09-09, [[graph-is-a-piece]] and [[piece-bench-runs-old-against-new]]
moved to ideas. The existing retrieval claim and completed hygiene evidence
remain unchanged. This development optimization is not a prerequisite for the
first usable core revision.

## Check

The retained children pass their own checks. The original wider acceptance,
serving every compute crate hot and swapping each without a restart, is deferred
with the related ideas; it is not claimed complete.
