---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 3
review-status: superseded-recommend-retire
canonical-scope: development-tooling-has-one-home
needs:
- '@memory/memory-owns-its-tool/memory-adapter-core'
- '@memo/one-document-serves-every-reader/document-identity'
---

# Existing development commands run from one package

Move reusable development implementation under runtime ownership with an old-interface shim; retain source history.

## Acceptance

- [ ] Bundle/worktree/preflight entry points retain their interface.
- [ ] Owned-operation recovery survives the relocation.
- [ ] Missing prerequisites fail before packaging or mutation.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `development-tooling-has-one-home`; maximum five rounds.
