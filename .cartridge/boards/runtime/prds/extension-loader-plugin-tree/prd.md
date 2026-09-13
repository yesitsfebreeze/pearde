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
canonical-scope: extension-loader-plugin-tree
---

# extension-loader-plugin-tree

Reuse the current cartridge loader and transactional replacement semantics. Prepare a candidate before retiring the old active generation; where exclusive resources prevent overlap, require a tested handoff protocol or refuse the update while retaining the old service. The old dispose-then-mount prescription is not an atomic rollback guarantee.

## Acceptance

- [ ] Idempotent apply restarts nothing; add/remove/disable/config/name changes produce the documented minimal transitions.
- [ ] Failed candidate preparation preserves the old active provider and removes only newly owned effects.
- [ ] Nested isolation and owner disposal preserve private keys and sibling resources; no plugin loader or catalog is introduced into memory.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `extension-loader-plugin-tree`; maximum five rounds.
