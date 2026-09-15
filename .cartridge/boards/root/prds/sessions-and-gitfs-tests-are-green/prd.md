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

Not started.
