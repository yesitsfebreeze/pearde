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
canonical-scope: a-cartridge-installs-from-its-source
---

# a-cartridge-installs-from-its-source

Keep retrieval/pinning in development or installation tooling outside the kernel. Fetch into an operation-owned temporary cache, verify the resolved commit and materialized tree, then atomically publish an immutable content-addressed entry and revision-checked profile lock. Approval binds that exact tree/pin and transitives are approved separately.

## Acceptance

- [ ] Concurrent installs of the same pin converge on one verified cache entry and no partial lockfile; a failed fetch leaves the previous pin usable.
- [ ] A cached tree changed after approval is refused before Lua/hello/apply or demand activation.
- [ ] New upstream commits do not change a loaded pin and unapproved transitive cartridges remain inert; no source repository history is rewritten.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

External evidence prerequisites: [a-cartridge-declares-what-it-needs](../../../../memos/work/root--a-cartridge-declares-what-it-needs.md). Resolve their current completion and source revision before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `a-cartridge-installs-from-its-source`; maximum five rounds.
