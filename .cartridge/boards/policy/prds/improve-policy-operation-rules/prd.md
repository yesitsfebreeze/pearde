---
repo: /Users/feb/dev/cartridge/policy.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: policy
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-policy-operation-rules
footprint:
- /Users/feb/dev/cartridge/policy.ctg/init.lua
- /Users/feb/dev/cartridge/policy.ctg/cartridge.json
---

# Authorize individual operations with stable precedence

A profile can allow gitfs read/list while retaining ask/deny for writes, and can independently govern each memory mutation.

## Acceptance

- [ ] Table-driven fixtures cover tool and operation rules, defaults, unknown operations and deny precedence, including read-only gitfs access.
- [ ] MCP, proxy and native agent produce the same decision for equivalent trusted requests; a denied call causes zero backend mutation.

- [ ] Parse old profiles unchanged and make new rules opt-in except explicit tested read-only defaults. Reject invalid configuration atomically and retain the prior valid policy. Policy remains separate from runtime sandbox containment.

## Proof and recovery

Start at [init.lua](../../../../../../policy.ctg/init.lua), [cartridge.json](../../../../../../policy.ctg/cartridge.json).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test policy` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-policy-operation-rules`; maximum five rounds.
