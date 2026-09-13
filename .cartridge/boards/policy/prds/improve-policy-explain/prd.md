---
repo: /Users/feb/dev/cartridge/policy.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: policy
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: improve-policy-explain
needs:
- '@policy/improve-policy-operation-rules'
footprint:
- /Users/feb/dev/cartridge/policy.ctg/init.lua
- /Users/feb/dev/cartridge/policy.ctg/cartridge.json
commit: "a3f5cffface2b7b2bc9ed26d9e55da0ee0f4be2d"
---

# Explain the effective policy without executing a tool

A read-only explanation returns the rule, operation, decision and available authorization route for a trusted caller.

## Acceptance

- [x] For every allow/ask/deny fixture, explanation and dispatch decisions agree at the same policy revision.
- [x] Explain never invokes the target or creates an approval; unknown and malformed requests return explicit diagnostics.

- [x] Parse old profiles unchanged and make new rules opt-in except explicit tested read-only defaults. Reject invalid configuration atomically and retain the prior valid policy. Policy remains separate from runtime sandbox containment.

## Proof and recovery

Start at [init.lua](../../../../../../policy.ctg/init.lua), [cartridge.json](../../../../../../policy.ctg/cartridge.json).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test policy` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-policy-explain`; maximum five rounds.
