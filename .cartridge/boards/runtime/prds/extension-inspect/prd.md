---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 3
review-status: delivered-pending-verification
canonical-scope: extension-inspect
needs:
- '@runtime/extension-loader-plugin-tree'
---

# extension-inspect

Map the obsolete extension Inspect proposal onto current runtime inspection and Landscape. Retain a read-only, bounded snapshot of owner identity, phase, provided/injected keys, missing dependencies and owned effects without calling plugin code. No removed extension crate is rebuilt inside memory.

## Acceptance

- [ ] A provider, dependent and pending fixture yield correct owner/generation and missing-key evidence.
- [ ] Snapshot collection does not await arbitrary user callbacks while holding registry locks and respects output limits.
- [ ] Scoped/private providers do not leak; unavailable fields are labelled unknown and existing runtime status callers remain compatible.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `extension-inspect`; maximum five rounds.
