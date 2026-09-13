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
canonical-scope: degrade-corrects-the-retrieval-path-it-names
---

# degrade-corrects-the-retrieval-path-it-names

Define a store-qualified retrieval feedback handle carrying query identity, bounded contributing path IDs and source revision. The engine validates that handle against retained provenance before weakening only the named path. If provenance is unavailable/expired, refuse without guessing from a thought ID.

## Acceptance

- [ ] Known query feedback changes only its recorded reason/path contribution and leaves unrelated incident edges intact.
- [ ] Expired, forged, wrong-store and arbitrary entity IDs cause no mutation and return explicit invalid-handle/provenance-unavailable errors.
- [ ] Repeating the same feedback uses documented idempotency or revision conflict semantics; CLI/adapter documentation and schema agree on the handle type.

## Proof and recovery

Start at [cartridge.rs](../../../../../../memory.ctg/src/cartridge.rs), [main.rs](../../../../../../memory.ctg/src/main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `degrade-corrects-the-retrieval-path-it-names`; maximum five rounds.
