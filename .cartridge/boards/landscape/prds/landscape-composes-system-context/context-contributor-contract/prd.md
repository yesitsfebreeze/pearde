---
repo: /Users/feb/dev/cartridge/landscape.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: landscape
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: landscape-composes-system-context
needs:
- '@memo/one-document-serves-every-reader/document-identity'
---

# Contributors return bounded attributable context rows

Define owner/kind/ID/revision/availability/selection reason and an overall deadline in the existing library and memo facade.

## Acceptance

- [ ] Identical snapshots order identically and exact references read back.
- [ ] Disabled, absent, unavailable and empty are distinct.
- [ ] Timeout yields a named partial result and private sources leak neither bodies nor callable metadata.

## Proof and recovery

Start at [lib.rs](../../../../../../../landscape.ctg/src/lib.rs), [surface.rs](../../../../../../../landscape.ctg/src/surface.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test landscape` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `landscape-composes-system-context`; maximum five rounds.
