---
state: "specced"
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge"
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
wave: 2
date: "2026-09-15"
footprint:
- "sessions.ctg"
- "gitfs.ctg"
needs:
- the-profile-is-the-orchestration-service
- the-gates-run-from-the-root-justfile
---

# Sessions and gitfs tests are green

## Outcome

The two owners with the most red tests (2026-09-14: sessions 8, gitfs 6) pass repeatably.

## Acceptance

- [ ] `just test sessions` and `just test gitfs` exit 0 on three consecutive runs; the count observed at the start is in Result.

## Result

Dispatchable as of 2026-09-15 and not started: its footprint is held.

sessions.ctg and gitfs.ctg carry 13 uncommitted changes that belong to another session. The owner of these changes is not this session and did not announce itself.
Dispatching a worker into those trees would either build on work that is still
moving or overwrite it, and the acceptance here is about whether the suites are
green, which cannot be judged at a revision that does not exist yet.

This clears the moment the owning session commits. Nothing about this item is
otherwise blocked: the composition starts, the gates report per target, and
`just test` already names exactly which of these owners are red.
