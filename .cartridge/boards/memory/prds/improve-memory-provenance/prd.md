---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: memory
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-memory-provenance
footprint:
- /Users/feb/dev/cartridge/memory.ctg/src/cartridge.rs
- /Users/feb/dev/cartridge/memory.ctg/src/transport/src
- /Users/feb/dev/cartridge/memory.ctg/src/commands/src
- /Users/feb/dev/cartridge/memory.ctg/tests/cartridge.rs
- /Users/feb/dev/cartridge/memory.ctg/CARTRIDGE.md
---

# Expose fact provenance freshness and conflicts consistently

Query and get responses identify source, observation/update time where known, lifecycle status and conflicting evidence so callers can assess a recalled fact.

## Acceptance

- [ ] Seed an updated fact with its older conflicting source: query/get preserve both identities and explain status and provenance.
- [ ] A legacy fact lacking dates returns unknown freshness and remains readable; unavailable evidence is not fabricated.

- [ ] Keep the current exclusive-writer invariant and existing on-disk formats. On attachment/readiness failure return an explicit error; reverting the adapter must not require rewriting the store. Any schema addition needs a backwards-compatible reader and a tested migration boundary.

## Proof and recovery

Start at [cartridge.rs](../../../../../../memory.ctg/src/cartridge.rs), [cartridge.rs](../../../../../../memory.ctg/tests/cartridge.rs), [CARTRIDGE.md](../../../../../../memory.ctg/CARTRIDGE.md).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-memory-provenance`; maximum five rounds.
