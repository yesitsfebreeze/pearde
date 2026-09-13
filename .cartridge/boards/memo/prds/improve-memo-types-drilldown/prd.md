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
commit: "0976a3b0035c67bbb828063a1def17a1f5297d14"
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

## Reverification after merged shadowing proof

The shared integration test file gained the shadowing fixture at 648b420. The
types/index/read contract is unchanged. Re-run the public memo gate and retain
the previous receipt in collection-5ecbf9e4.md.

Reverify unchanged drilldown contract after owner board installation at0976a3b;
prior648b420f receipt retained. No acceptance scope change.
