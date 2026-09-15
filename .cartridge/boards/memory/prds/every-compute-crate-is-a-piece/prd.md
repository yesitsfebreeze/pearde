---
repo: /Users/feb/dev/cartridge/memory.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# roll [[crates-are-hot-pieces]] across the compute crates — hygiene proven, retrieval and graph next, then the piece benchmark that runs a new dylib against the one it replaced

## Do

Execute the children in order; each is one lane. A crate qualifies when its
surface is free functions over host-owned types — no generics, no `async` at
the boundary. The async shells are excluded by [[crates-are-hot-pieces]].

subwork: [hygiene-is-the-first-piece](../hygiene-is-the-first-piece/prd.md) [retrieval-is-a-piece](../retrieval-is-a-piece/prd.md)

On 2026-09-09, [[graph-is-a-piece]] and [[piece-bench-runs-old-against-new]]
moved to ideas. The existing retrieval claim and completed hygiene evidence
remain unchanged. This development optimization is not a prerequisite for the
first usable core revision.

## Acceptance
The retained children pass their own checks. The original wider acceptance,
serving every compute crate hot and swapping each without a restart, is deferred
with the related ideas; it is not claimed complete.
