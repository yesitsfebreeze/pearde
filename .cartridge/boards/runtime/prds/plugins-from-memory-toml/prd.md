---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: plugins-from-memory-toml
---

# plugins-from-memory-toml

Reconcile the old plugin configuration proposal with current cartridge profile/manifest ownership. Only database/endpoint settings stay in memory configuration; optional external adapters are composed by runtime. Preserve the old proposal as history rather than adding memory plugins reload back.

## Acceptance

- [ ] Every old plugin row requirement maps to current owner/profile semantics or an explicit obsolete field.
- [ ] Duplicate IDs, unknown providers and invalid candidate configuration fail before replacing a usable composition.
- [ ] Disabled external adapters stop only their effects, while standalone memory ingest/recall and store configuration remain compatible.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `plugins-from-memory-toml`; maximum five rounds.
