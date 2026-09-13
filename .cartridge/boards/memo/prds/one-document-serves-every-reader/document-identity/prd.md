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
---

# Readers agree on document identity and revision

Define cartridge-document/v1 identity from canonical owner/path and SHA-256 of exact source bytes; .jd is only an unambiguous alias.

## Acceptance

- [ ] Commands, docs and human projections return the same source digest.
- [ ] Duplicate owner/alias identities refuse with source locations.
- [ ] Body-only words never become metadata matches and existing native memo APIs remain compatible.

## Proof and recovery

Start at [service.rs](../../../../../../../memo.ctg/src/service.rs), [record.rs](../../../../../../../memo.ctg/src/record.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test memo` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `one-document-serves-every-reader`; maximum five rounds.
