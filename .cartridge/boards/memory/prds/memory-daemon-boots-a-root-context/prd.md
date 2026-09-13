---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: memory-daemon-boots-a-root-context
---

# memory-daemon-boots-a-root-context

Audit the current daemon startup/shutdown sequence directly and fix only a demonstrated ownership gap. Drop the obsolete extension root, mine/models plugin and MCP exposure requirements. Record dependencies between admission, in-flight work, persistence and listener ownership using current source paths.

## Acceptance

- [ ] A shutdown fixture stops admitting new writes before draining owned in-flight operations and persisting committed data.
- [ ] Startup failure or rejected replacement preserves the previous owner and releases only candidate-owned resources.
- [ ] Readiness and health report actual store state and no runtime plugin framework or duplicate writer is required to inspect it.

## Proof and recovery

Start at [cartridge.rs](../../../../../../memory.ctg/src/cartridge.rs), [main.rs](../../../../../../memory.ctg/src/main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `memory-daemon-boots-a-root-context`, `memory-boots-as-a-plugin-tree`; maximum five rounds.
