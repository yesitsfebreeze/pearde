---
repo: /Users/feb/dev/cartridge/memo.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: memo
work-kind: leaf
review-round: 3
review-status: accepted
canonical-scope: improve-memo-types-drilldown
footprint:
- src/service.rs
- .cartridge/tests/integration/tests.rs
commit: "5ecbf9e4ed34561dd75bcacfb98340ec28ee006a"
---

# Read type declarations individually

A caller discovers compact kind metadata and requests only the declaration needed for the intended write.

## Acceptance

- [x] Discover work and routine kinds, then retrieve their full declarations individually without loading other bodies.
- [x] Existing types clients and validated writes behave unchanged; unknown kinds produce explicit errors.

- [x] Keep the prior response shape available during migration. Roll back presentation/ranking changes without rewriting authored records or evidence journals.

## Proof and recovery

Start at [service.rs](../../../../../../memo.ctg/src/service.rs), [record.rs](../../../../../../memo.ctg/src/record.rs), [resolver.rs](../../../../../../memo.ctg/src/resolver.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test memo` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-memo-types-drilldown`; maximum five rounds.
