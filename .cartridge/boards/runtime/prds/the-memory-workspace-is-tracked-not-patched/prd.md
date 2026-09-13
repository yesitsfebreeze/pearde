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
canonical-scope: the-memory-workspace-is-tracked-not-patched
---

# the-memory-workspace-is-tracked-not-patched

Replace the obsolete import plan with verification of the current separate memory submodule. Retain the old vendor/bootstrap rationale as history; do not remove a nested .git, import engine files or rewrite memory's source history. The deliverable is a current reproducible source-layout contract.

## Acceptance

- [ ] A fresh recursive checkout obtains the recorded memory commit and builds using documented sibling SDK dependencies.
- [ ] Runtime manifests/catalog/links point to memory.ctg without obsolete vendor-copy or patch bootstrap requirements.
- [ ] Existing memory worktrees, ignored stores and repository history remain intact; any remaining portability gap becomes a bounded development-tooling requirement.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `the-memory-workspace-is-tracked-not-patched`; maximum five rounds.
