---
repo: /Users/feb/dev/cartridge/policy.ctg
state: "done"
origin: requested
priority: 50
blast-radius: small
workflow: develop-one-cartridge
capability-owner: policy
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: improve-gitfs-reviewable-ship
needs:
- '@policy/improve-policy-operation-rules'
- '@gitfs/improve-gitfs-reviewable-ship/recorded-push-reconciles-the-exact-remote-head'
commit: "e442bef2c9f07635f9e8b8e1d87a47193841569f"
---

# Recorded ship pushes have an explicit policy operation

Recognize GitFS's separate ship.push operation through the existing policy rules.
Preserve explicit deny precedence and configured fallback behavior. A push remains
a separately evaluated call; recognizing it does not grant it permission or change
remote mutation semantics. The existing default is ask, not an implicit allow.

## Acceptance

- [x] Real policy accepts ship.push configuration and applies tool deny, operation allow/deny/ask and configured fallback consistently through policy and policy.explain.
- [x] Actual MCP enforces allow and deny for push; denied requests execute zero producer calls and permitted requests execute once. Other operations retain their existing behavior.
- [x] Semantic evaluator revision changes with the operation catalog; no external push, credentials or new containment behavior is part of policy validation.

## Lineage

Owner split from [GitFS reviewable shipping](../../../gitfs/prds/improve-gitfs-reviewable-ship/prd.md), preserving inherited rounds1–2 and maximum5. Root coordinates parent prerequisite and map updates. Concrete measured baseline/spec and independent round3 review precede implementation.
