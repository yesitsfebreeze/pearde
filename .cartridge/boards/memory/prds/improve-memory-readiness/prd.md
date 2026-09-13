---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: memory
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-memory-readiness
needs:
- '@memory/improve-memory-owner-access'
footprint:
- /Users/feb/dev/cartridge/memory.ctg/src/cartridge.rs
- /Users/feb/dev/cartridge/memory.ctg/src/transport/src
- /Users/feb/dev/cartridge/memory.ctg/src/commands/src
- /Users/feb/dev/cartridge/memory.ctg/tests/cartridge.rs
- /Users/feb/dev/cartridge/memory.ctg/CARTRIDGE.md
---

# Report memory readiness separately from registration

A registered memory provider exposes store/model readiness and the reason it cannot currently serve a request.

## Acceptance

- [ ] The contention fixture reports active registration and unavailable query readiness with retryability; it never reports ready from registration alone.
- [ ] Status requests have a deadline, redact credentials, and do not start a writer; after owner recovery status updates without restarting the caller.

- [ ] Keep the current exclusive-writer invariant and existing on-disk formats. On attachment/readiness failure return an explicit error; reverting the adapter must not require rewriting the store. Any schema addition needs a backwards-compatible reader and a tested migration boundary.

## Proof and recovery

Start at [cartridge.rs](../../../../../../memory.ctg/src/cartridge.rs), [cartridge.rs](../../../../../../memory.ctg/tests/cartridge.rs), [CARTRIDGE.md](../../../../../../memory.ctg/CARTRIDGE.md).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-memory-readiness`; maximum five rounds.
