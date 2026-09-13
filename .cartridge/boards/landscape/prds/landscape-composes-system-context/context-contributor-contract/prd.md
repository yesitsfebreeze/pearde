---
repo: /Users/feb/dev/cartridge/landscape.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: landscape
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: landscape-composes-system-context
footprint:
  - src/lib.rs
  - src/context.rs
  - Cargo.toml
  - .cartridge/tests/unit/context.rs
  - .cartridge/docs/context.md
needs:
- '@memo/one-document-serves-every-reader/document-identity'
commit: "c705d648830582e5cf2b4ded267b3c1da4f1eac4"
---

# Contributors return bounded attributable context rows

Define owner/kind/ID/revision/availability/selection reason and an overall deadline in the existing library. The linked memo-owned facade provides native integration before the parent programme can finish.

## Acceptance

- [x] Identical snapshots order identically and exact references read back from the frozen result.
- [x] Disabled, absent, unavailable and empty are distinct.
- [x] Timeout yields a named partial result and private sources leak neither bodies nor callable metadata.

## Proof and recovery

Start at [lib.rs](../../../../../../../landscape.ctg/src/lib.rs), [surface.rs](../../../../../../../landscape.ctg/src/surface.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test landscape` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `landscape-composes-system-context`; maximum five rounds.

Reverification after Memory contributor c705d648: public context contract unchanged; shared lib.rs registration changed.
