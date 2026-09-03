---
state: open
origin: requested
priority: 95
complexity: 0
blast-radius:
---

# the board reclaims dead work by itself

A claim on this board survives its worker. Measured 2026-09-03: eighteen
workers were killed at 11:18:04 when a user interrupt ended the pass window
holding them, and four of their PRDs were still `claimed` at 12:0x — three
quarters of an hour behind workers that had been dead the whole time. Nothing
noticed, because nothing was looking at a process.

The user, verbatim: *"All of this should be automatic. And we shouldn't wait
like 30 minutes for something that got canceled. Can't we just check if an
actual agent is working in that tree, like if there is a session existing and a
process running in that session?"*

The answer is yes, and most of the mechanism is already written — it is simply
not wired to claims. When this container is done, a dead worker's PRD returns
to `open` without a person, a cancelled window costs minutes rather than a
`claim-ttl`, a collected PRD leaves no worktree behind, and a fork reaches the
user when it is written rather than when the pass ends.

**What must not change.** `sweep --apply` drops uncommitted lane paths — 44
were lost that way at 11:10 on 2026-09-03. Every child that makes reclaiming
*faster* makes that loss fire *sooner*, so committing the lane before releasing
a claim is a constraint on this whole tree, not a nicety.

The children are siblings and run at once, except where `needs:` says
otherwise.
