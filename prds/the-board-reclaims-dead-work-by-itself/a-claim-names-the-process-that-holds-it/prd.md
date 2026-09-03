---
state: open
origin: requested
priority: 95
complexity: 20
blast-radius: high
workflow: probe-then-spec
---


# a claim names the process that holds it

Today a claim line records a worker **name** — `impl-harness-root` — and
nothing else. A name cannot be resolved to a process, so no tool can ask the
only question that matters: is anyone actually working in this tree?

The liveness rule already exists and is three-valued.
`resources/board/session.py` calls a session **alive** when its pid is running
*and* the `ps lstart=` start time matches the ledger, **dead** when the pid is
gone or the start time differs (the pid-reuse guard), and **unknown**
otherwise; only `dead` reaps. That is exactly the check the user is asking for.

`resources/board/silence.py` `silent_of` is the rule that `scan`, the view and
`sweep` all act on, and it knows none of it: it takes the newest mtime over the
PRD directory and its footprint union and compares that to `claim-ttl`,
default 30m.

When this is done, `pearde claim` records the holder's session id (or pid plus
start time) alongside the worker name, and `silent_of` asks the session ledger
first: **dead** is silent immediately, whatever the mtime says; the mtime rule
survives only for the **unknown** case. A worker that never started — a
concurrency-cap refusal, a 402 — is dead by this rule the moment it is looked
at, not thirty minutes later.

**Constraint.** Faster reclaim means `sweep --apply` reaches a live lane
sooner, and it drops uncommitted lane paths. Committing the lane before the
release belongs in this child, not in a later one.

This is the headline of the container — the other children are cheaper without
it and none of them replaces it.

## History

**failed, retried 2026-09-03 21:03**

swept 2026-09-03 20:59 — claim impl-claim-pid 2026-09-03 17:46, silent 3.2h: no file of this PRD's moved past `claim-ttl`. Read the worker's output before a retry; partial code stands on branch `lane/the-board-reclaims-dead-work-by-itself-a-claim-names-the-process-that-holds-it`, whose worktree this sweep removed — the branch is kept.
