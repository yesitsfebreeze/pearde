---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: sessions
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-sessions-client-mapping
footprint:
- /Users/feb/dev/cartridge/sessions.ctg/main.rs
- /Users/feb/dev/cartridge/sessions.ctg/README.md
---

# Map client conversations to cartridge sessions honestly

Only a host-authenticated connection identity plus an explicitly supplied external conversation identifier can create a durable mapping. Treat arbitrary clientInfo/name fields as untrusted description. If authenticated identity or conversation ID is absent, use a clearly labelled connection scope and retain no invented cross-reconnect identity.

## Acceptance

- [ ] The same authenticated client/workspace/external ID resolves its own mapping after reconnect.
- [ ] Another authenticated client, workspace or profile cannot reuse it by copying metadata; missing IDs remain connection-scoped.
- [ ] Legacy session files remain readable and mapping writes use revision-checked atomic persistence without rewriting transcripts.

## Proof and recovery

Start at [main.rs](../../../main.rs), [README.md](../../../README.md).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test sessions` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-sessions-client-mapping`; maximum five rounds.
