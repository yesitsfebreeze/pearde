---
repo: /Users/feb/dev/cartridge/memory.ctg
state: deferred
deferred-from: blocked
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "30m"
---

# killing a memory daemon mid-boot leaves the HNSW index dirty, and the next cold start re-verifies every vector at 99% CPU before the socket answers — wait out a boot or confirm the old daemon died before spawning the next one

## Do

On 2026-09-08, `memory stop` left the old daemon's lock held, so the next
`memory daemon` exited on the writer lock; the one that finally held the lock
sat at 98% CPU for ten minutes with no socket while `GraphGnn::rebuild_index
→ reconcile_disk → VectorBackend::insert` reprocessed the 26k-entity vector
index (a `sample` showed the stack), and every kill-and-respawn restarted
the rebuild from scratch. The first boot logged `self-heal compacted data.mdb
895 MiB -> 213 MiB`, and a daemon whose boot is interrupted is not a stable
state to relaunch over.

The rule: before spawning a replacement daemon, verify the previous one is
actually dead (`ps -p <pid>` empty, `memory status` says the lock is free) —
a `memory stop` that does not clear the lock is a signal, not a step to skip.
Once a lock-holding daemon is seen rebuilding, leave it alone: `sample` its
stack to confirm progress before deciding it is wedged, and only kill it if
the same frame repeats with no growth.

## Acceptance
`memory stop && memory daemon` boots to `serving` within the time the store's
last index rebuild took, and the daemon.log shows a single compaction line,
not a repeated one.

Blocked 2026-09-08: the `Do` records a rule and names no code change, and the
`Check` cold-boots the shared store — `memory stop && memory daemon` on the daemon
this machine's other sessions are talking to (pid 85840, serving 26408
entities). It unblocks in a window where that daemon may be stopped and made to
pay its rebuild in the open.
