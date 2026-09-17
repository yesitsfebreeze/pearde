---
state: open
origin: requested
priority: 82
repo: "/Users/feb/dev/cartridge"
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
wave: 3
date: "2026-09-15"
footprint:
- "live.ctg/src/context.ts"
- "prd.ctg/src/service.ts"
needs:
- the-gates-are-green-at-one-pinned-set-of-shas
---

# The orchestrator knows what is in the works

## Outcome

Every orchestrator turn starts with the board, the workers and the roster in view, bounded.

## Acceptance

- [ ] The orchestrator's system context carries board counts by state, every claimed PRD with worker and age, the ready frontier (`prd next`, top 10), the worker registry, the sessions roster and the record's `system` memos, under one byte bound with the oldest cut first.
- [ ] The role text says orchestrator, not terminal surface; it names the doors (voice, text, MCP) and the worker tools.
- [ ] Test: with one claimed PRD and one running worker, `cartridge call live '{"op":"context",...}'` contains both by id.

## Folds

Deferred with `superseded-by` pointing here:

- @landscape/landscape-composes-system-context
- @harness/harness-consumes-landscape
- @root/context-is-living-not-per-session

## Result

Not started.
