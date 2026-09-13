---
kind: work
level: 10
status: open
estimate: 1d
description: all graph mutations route to the daemon or retain the writer lock from load through commit
read_when: closing removal resurrection from stale whole-map writers
---

# every-mutation-holds-the-store-writer-boundary

## Do

Every graph mutation has exactly one store writer: the serving daemon, or a
local caller retaining writer ownership before load until commit. A competing
mutation refuses without writing; a holder check alone is not ownership.
A stale unrelated mutation cannot resurrect a removed row. Existing daemon
routing and lock primitives remain the boundary, without a new tombstone set,
base-image merge or per-process removed-ID workaround.

This implements [[does-a-removal-need-a-tombstone]] for
[[@prd/work/memory--the-graph-converges.md]]. Bitemporal claim retirement remains distinct from
physical cleanup.
