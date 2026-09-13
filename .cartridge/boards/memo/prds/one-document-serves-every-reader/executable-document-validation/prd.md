---
repo: /Users/feb/dev/cartridge/memo.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memo
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: one-document-serves-every-reader
needs:
- '@memo/one-document-serves-every-reader/document-identity'
---

# Invalid executable documents refuse before launch

Require kind, description, recipe, invocation mode and owner-relative execution base. V1 rejects executable imports/includes and filesystem-reading just expressions; probe the actual parser before implementing enforcement.

## Acceptance

- [ ] Duplicate recipes and malformed fences report source locations.
- [ ] Forbidden executable dependency forms cause zero process starts.
- [ ] Valid frozen extraction produces the declared recipe and argv without re-reading mutable source.

## Proof and recovery

Start at [service.rs](../../../../../../../memo.ctg/src/service.rs), [record.rs](../../../../../../../memo.ctg/src/record.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test memo` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `one-document-serves-every-reader`; maximum five rounds.
