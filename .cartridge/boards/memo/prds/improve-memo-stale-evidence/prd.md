---
repo: /Users/feb/dev/cartridge/memo.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: memo
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-memo-stale-evidence
footprint:
- /Users/feb/dev/cartridge/memo.ctg/src/service.rs
- /Users/feb/dev/cartridge/memo.ctg/src/record.rs
- /Users/feb/dev/cartridge/memo.ctg/src/resolver.rs
---

# Distinguish stale source references from current guidance

Discovery reports missing or changed referenced files and explains freshness without rewriting historical decisions or falsely declaring them obsolete.

## Acceptance

- [ ] Rename a referenced source in a temporary repository: discovery labels the stale target and preserves its original reference and revision.
- [ ] A current routine and completed historical work remain separately retrievable; unverified outcomes retain their caller-reported label.

- [ ] Keep the prior response shape available during migration. Roll back presentation/ranking changes without rewriting authored records or evidence journals.

## Proof and recovery

Start at [service.rs](../../../../../../memo.ctg/src/service.rs), [record.rs](../../../../../../memo.ctg/src/record.rs), [resolver.rs](../../../../../../memo.ctg/src/resolver.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test memo` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-memo-stale-evidence`; maximum five rounds.
