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
canonical-scope: retrieval-is-a-piece
---

# retrieval-is-a-piece

Compare the current retrieval/piece exports, stable host-owned types and reload tests to the historical migration list before any refactor. Specify only a remaining observed ABI or replacement gap. Preserve the current hot-reload audit and no-default-switch boundary.

## Acceptance

- [ ] A current daemon query observes an intended scoring change after a valid piece replacement under the same PID.
- [ ] An incompatible layout/symbol candidate is rejected before use and the previous retrieval implementation remains usable.
- [ ] Existing recall/legacy-store tests pass at the same revision and no generic-to-monomorphic rewrite is performed solely because an old memo requested it.

## Proof and recovery

Start at [cartridge.rs](../../../../../../memory.ctg/src/cartridge.rs), [main.rs](../../../../../../memory.ctg/src/main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `retrieval-is-a-piece`, `every-compute-crate-is-a-piece`; maximum five rounds.
