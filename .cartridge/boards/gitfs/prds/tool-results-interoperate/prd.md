---
repo: /Users/feb/dev/cartridge/gitfs.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: gitfs
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: tool-results-interoperate
footprint:
- /Users/feb/dev/cartridge/gitfs.ctg/service.rs
- /Users/feb/dev/cartridge/gitfs.ctg/ship.rs
- /Users/feb/dev/cartridge/gitfs.ctg/main.rs
- /Users/feb/dev/cartridge/gitfs.ctg/cartridge.json
---

# Every currently exposed tool completes through its real consumers

This PRD owns the immediate interoperability fix; the older improve-tool-result-contract becomes its coverage reference. Keep the current content:string/error:boolean wire. Serialize structured domain payloads exactly once at the producing tool boundary; consumers share fixtures and reject malformed results without guessing a second operation. A later richer negotiated protocol is outside this repair.

## Acceptance

- [ ] Real direct, MCP and proxy GitFS read/ship scan return equivalent decoded payloads; a string that itself contains JSON is not double-normalized.
- [ ] Invalid request input and policy refusal cause zero backend calls. A malformed response discovered after a fixture mutation reports an explicit failed/unknown outcome and causes no retry or follow-on mutation.
- [ ] Native agent resumes after ordinary tool failure, while cancellation and partial effects retain the original invocation identity.

## Proof and recovery

Start at [service.rs](../../../service.rs), [ship.rs](../../../ship.rs), [main.rs](../../../main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test gitfs` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `tool-results-interoperate`, `improve-tool-result-contract`; maximum five rounds.
