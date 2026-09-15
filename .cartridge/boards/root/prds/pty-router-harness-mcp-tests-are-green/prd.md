---
state: open
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
---

# pty, router, harness and mcp tests are green

## Outcome

The four spine owners (2026-09-14: pty 2, router 2, harness 1, mcp 1 red) pass repeatably.

## Acceptance

- [ ] `just test pty`, `just test router`, `just test harness`, `just test mcp` exit 0 on three consecutive runs; the counts observed at the start are in Result.

## Result

Not started.
