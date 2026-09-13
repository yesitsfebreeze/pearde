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
canonical-scope: development-tooling-has-one-home
needs:
- '@runtime/runtime-development-package'
- '@runtime/improve-tools-bundle-provenance'
- '@runtime/improve-tools-preflight'
- '@runtime/improve-tools-worktree-resume'
---

# Development documents work from a clean checkout

Verify installed and source-absent bundle discovery using the canonical development package.

## Acceptance

- [ ] A recursively initialized checkout uses correct owner paths and cwd.
- [ ] A source-absent bundle runs without developer-home references.
- [ ] The shim is retired only after interface and recovery parity.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `development-tooling-has-one-home`; maximum five rounds.
