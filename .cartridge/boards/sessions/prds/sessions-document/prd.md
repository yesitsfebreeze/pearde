---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: sessions
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: capabilities-live-with-their-owners
needs:
- '@mcp/clients-share-document-execution'
---

# A document reads bounded session history

Expose existing read-only session inspection through an owner-local executable document.

## Acceptance

- [ ] Selected session results retain exact IDs and bounded continuation.
- [ ] Missing, corrupt and inaccessible sessions are distinct outcomes.
- [ ] Inspection changes no journal or foreground terminal state.

## Proof and recovery

Start at [main.rs](../../../main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test sessions` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `capabilities-live-with-their-owners`; maximum five rounds.
