---
repo: /Users/feb/dev/cartridge/policy.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: policy
work-kind: leaf
review-round: 3
review-status: needs-decision
canonical-scope: improve-policy-resource-scope
needs:
- '@policy/improve-policy-operation-rules'
footprint:
- /Users/feb/dev/cartridge/policy.ctg/init.lua
- /Users/feb/dev/cartridge/policy.ctg/cartridge.json
---

# Constrain granted file operations to declared resources

Define a supported operation target schema and canonical root identity. The mutating backend must bind the authorized target to its actual open/commit operation using platform-supported handle-relative/no-follow semantics; a string canonicalization followed by an unconstrained open is insufficient. Opaque shell commands require separate permission and make no path-confinement promise.

## Acceptance

- [ ] Traversal, outside symlink and a symlink swapped between preview and open cannot write outside the authorized root.
- [ ] A target revision/root change invalidates the preview before mutation.
- [ ] Unsupported platform/operation binding refuses scoped execution with an explicit reason rather than pretending the generic shell is confined.

## Proof and recovery

Start at [init.lua](../../../../../../policy.ctg/init.lua), [cartridge.json](../../../../../../policy.ctg/cartridge.json).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test policy` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-policy-resource-scope`; maximum five rounds.
