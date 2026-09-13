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
canonical-scope: documents-own-live-processes
needs:
- '@runtime/one-runner-executes-documents/document-command-result'
---

# Event activation resumes from a durable cursor

Use at-least-once notifications and stable dispatch identities; do not promise exactly-once external effects.

## Acceptance

- [ ] Crash after dispatch replays the same identity for deduplication or explicit reconciliation.
- [ ] Reload produces no duplicate subscriptions.
- [ ] Queue overflow reports a gap and recoverable journal cursor.

## Proof and recovery

Start at [runtime.rs](../../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `documents-own-live-processes`; maximum five rounds.
