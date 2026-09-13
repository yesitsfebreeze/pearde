---
repo: /Users/feb/dev/cartridge/proxy.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: proxy
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: clients-share-document-execution
needs:
- '@mcp/clients-share-document-execution/client-document-contract'
---

# Proxy tool calls retain the shared execution outcome

Use the common runner while preserving client-owned history and native stream semantics.

## Acceptance

- [ ] Success and tool failure agree with the shared fixtures.
- [ ] Cancellation and provider errors retain native stream framing.
- [ ] Headless ask and uncertain completion never trigger hidden retries.

## Proof and recovery

Start at [service.rs](../../../service.rs), [streaming.rs](../../../streaming.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test proxy` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `clients-share-document-execution`; maximum five rounds.
