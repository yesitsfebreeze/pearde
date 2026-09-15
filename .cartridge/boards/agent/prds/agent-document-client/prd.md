---
repo: /Users/feb/dev/cartridge/agent.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: agent
work-kind: leaf
review-round: 3
review-status: superseded-recommend-retire
canonical-scope: clients-share-document-execution
needs:
- '@mcp/clients-share-document-execution/client-document-contract'
---

# The agent executes the selected document revision

Consume the shared contract while preserving interactive ask and cancellation.

## Acceptance

- [ ] A discovered document executes without client source changes.
- [ ] Interactive ask binds to the exact invocation and revision.
- [ ] Uncertain completion after restart is surfaced instead of replayed.

## Proof and recovery

Start at [model_loop.rs](../../../model_loop.rs), [run_state.rs](../../../run_state.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test agent` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `clients-share-document-execution`; maximum five rounds.
