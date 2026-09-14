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
canonical-scope: the-agent-surface-is-usable
needs:
- '@memory/memory-owns-its-tool/memory-adapter-core'
- '@memory/improve-memory-tool-get'
- '@memory/improve-memory-tool-errors'
- '@memory/improve-memory-readiness'
---

# An agent can recall, record, read back and diagnose memory through tool.memory

The old 22-tool `memory mcp` surface is gone. Agents now reach memory through `tool.memory`, which memory.ctg serves from its own cartridge (`src/cartridge.rs`). MCP and agent consumers relay it without any sibling knowledge (decision `a-cartridge-brings-its-own-surface`). This parent tracks the leaves that make that tool sufficient: its adapter, exact readback, actionable failures and readiness.

## Acceptance

- [ ] Each linked leaf is done with its own evidence at a single memory.ctg revision.
- [ ] Integration gate, run as the memory integration test at that revision: one `tool.memory` session calls describe, ingest, query, and get by the returned ID. It also triggers one invalid input and one unavailable embed. Every answer stays under 32,000 characters, and each failure carries its code.
- [ ] A live probe against an identified installed generation (`cartridge call memory`, with pid and build recorded) is kept apart from the isolated test. If the probe fails, record the failure and do not repair the production store.

## Work items

- [Memory serves query and ingest through its own adapter](../memory-owns-its-tool/memory-adapter-core/prd.md)
- [Agents read one recalled fact back by ID through tool.memory](../improve-memory-tool-get/prd.md)
- [tool.memory failures carry a stable code the agent can act on](../improve-memory-tool-errors/prd.md)
- [Report memory readiness separately from registration](../improve-memory-readiness/prd.md)

## Review

[Review history](review.md): rounds 1–2 inherited, round 3 rebased; maximum five.
