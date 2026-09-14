---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: rollup
review-round: 3
review-status: passed
canonical-scope: improve-memory-tool-programme
needs:
- '@memory/improve-memory-tool-get'
- '@memory/improve-memory-tool-correct'
- '@memory/improve-memory-tool-errors'
---

# tool.memory covers exact readback, correction and actionable failures

The memory-tool wrapper was dropped on 2026-09-14 (root commit `9e4cde8`), and memory.ctg now serves `tool.memory` itself from `src/cartridge.rs`. This parent tracks the three remaining improvements to that tool. To implement, claim one of the leaves; the parent carries no implementation of its own.

## Acceptance

- [ ] Each linked leaf passes its own review and acceptance at one memory.ctg revision.
- [ ] Integration gate: at that revision, `just test` passes from /Users/feb/dev/cartridge/memory.ctg, and one integration case drives `tool.memory` through query → get → correct → get → forget → get, with each failure code observed where its leaf specifies.
- [ ] Any leaf limitation, such as `tool_writes` staying off by default, is recorded here rather than closed silently.

## Work items

- [Agents read one recalled fact back by ID through tool.memory](../improve-memory-tool-get/prd.md)
- [Agents correct or forget one identified fact through tool.memory](../improve-memory-tool-correct/prd.md)
- [tool.memory failures carry a stable code the agent can act on](../improve-memory-tool-errors/prd.md)

## Review

[Review history](review.md): rounds 1–2 inherited, round 3 rebased; maximum five.
