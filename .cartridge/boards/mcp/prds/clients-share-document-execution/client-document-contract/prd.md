---
repo: /Users/feb/dev/cartridge/mcp.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: mcp
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: clients-share-document-execution
needs:
- memory-document-works-end-to-end
---

# Clients share query read and execute contracts

Freeze owner/path/revision, recipe and argv; trusted caller context comes from the host. Legacy names are owner-qualified.

## Acceptance

- [ ] Shared fixtures cover success, tool failure, denial and stale revision.
- [ ] Name collisions are errors rather than last-writer wins.
- [ ] Unsupported sidecar/event modes refuse explicitly.

## Proof and recovery

Start at [service.rs](../../../../service.rs), [tests.rs](../../../../tests.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test mcp` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `clients-share-document-execution`; maximum five rounds.
