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
canonical-scope: MEMORY-002
---

# Memory counts use consistent public terminology

Clarify stored memory, active memory and loaded/unloaded project daemons in current CLI/status documentation. Existing owner: `codex/memory-terminology`; preserve its reserved worktree and require handoff before claiming this scope. Keep hot/cold exports, history, audit, check/repair and hot reload intact.

## Acceptance

- [ ] CLI and RPC counts name the same entities, thoughts and reasons for one snapshot.
- [ ] Legacy data decodes with unchanged API and store layouts.
- [ ] The owner-reserved worktree and unrelated store contents are preserved.

## Proof and recovery

Start at [cartridge.rs](../../../../../../memory.ctg/src/cartridge.rs), [main.rs](../../../../../../memory.ctg/src/main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `MEMORY-002`; maximum five rounds.
