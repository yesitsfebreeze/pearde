---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: a-lanes-build-can-hand-back-a-siblings-binary
---

# a lane's build can hand back a sibling's binary

Retain the measured cache-contamination evidence and move the executable outcome to runtime development tooling. Give each operation an isolated target and a wrapper cache key that distinguishes source revisions; if the wrapper cannot prove that property, disable it for isolated builds and measure the cost. Memory consumes correctly built artifacts but owns no host lane automation.

## Acceptance

- [ ] Two worktrees change the same crate differently and executing each resulting binary proves its own behavior.
- [ ] Repeating with the wrapper enabled/disabled identifies whether target isolation alone is sufficient; a wrong artifact fails the gate, not a manual strings warning.
- [ ] The report preserves cold/warm timing, actual binary digests and source identities without changing unrelated worktrees or global cache configuration.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `a-lanes-build-can-hand-back-a-siblings-binary`; maximum five rounds.
