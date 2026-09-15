---
state: "analyzing"
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
- "pty.ctg"
- "router.ctg"
- "harness.ctg"
- "mcp.ctg"
needs:
- the-profile-is-the-orchestration-service
- the-gates-run-from-the-root-justfile
claim: "cartridge-ctg-22 2026-09-15T09:06:09.793Z"
---

# pty, router, harness and mcp tests are green

## Outcome

The four spine owners (2026-09-14: pty 2, router 2, harness 1, mcp 1 red) pass repeatably.

## Acceptance

- [ ] `just test pty`, `just test router`, `just test harness`, `just test mcp` exit 0 on three consecutive runs; the counts observed at the start are in Result.

## Result

Dispatchable as of 2026-09-15 and not started: its footprint is held.

pty.ctg, router.ctg, harness.ctg and mcp.ctg carry 9 uncommitted changes that belong to another session. The owner of these changes is not this session and did not announce itself.
Dispatching a worker into those trees would either build on work that is still
moving or overwrite it, and the acceptance here is about whether the suites are
green, which cannot be judged at a revision that does not exist yet.

This clears the moment the owning session commits. Nothing about this item is
otherwise blocked: the composition starts, the gates report per target, and
`just test` already names exactly which of these owners are red.
