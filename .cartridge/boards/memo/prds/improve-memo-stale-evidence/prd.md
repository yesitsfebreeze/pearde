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
canonical-scope: improve-memo-stale-evidence
footprint:
- src/usage.rs
- .cartridge/templates/seeds/type/resource.md
- .cartridge/tests/integration/resolver.rs
commit: "535915d3315ead89b92811cb70e63dd592d705b1"
---

# Distinguish stale source references from current guidance

Discovery reports missing or changed referenced files and explains freshness without rewriting historical decisions or falsely declaring them obsolete.

## Acceptance

- [x] Rename a referenced source in a temporary repository: discovery labels the stale target and preserves its original reference and revision.
- [x] A current routine and completed historical work remain separately retrievable; unverified outcomes retain their caller-reported label.

- [x] Keep the prior response shape available during migration. Roll back presentation/ranking changes without rewriting authored records or evidence journals.

## Proof and recovery

Start at [service.rs](../../../../../../memo.ctg/src/service.rs), [record.rs](../../../../../../memo.ctg/src/record.rs), [resolver.rs](../../../../../../memo.ctg/src/resolver.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test memo` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-memo-stale-evidence`; maximum five rounds.
