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

# Readable projections hydrate bounded linked prose

Derive commands/docs/human views from one document; linked prose has a separate digest closure and depth/byte bounds.

## Acceptance

- [ ] An edited prose dependency changes the hydrated projection digest.
- [ ] Cyclic or excessive expansion reports truncation within the declared bounds.
- [ ] References inside code blocks stay literal and private source bodies remain hidden.

## Proof and recovery

Start at [service.rs](../../../../../../../memo.ctg/src/service.rs), [record.rs](../../../../../../../memo.ctg/src/record.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test memo` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `one-document-serves-every-reader`; maximum five rounds.
