---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 3
review-status: accepted
canonical-scope: the-memory-workspace-is-tracked-not-patched
commit: "ae989f6a4ab5a27d1c8a31f487b49fbcfaacfd35"
---

# the-memory-workspace-is-tracked-not-patched

Replace the obsolete import plan with verification of the current separate memory submodule. Retain the old vendor/bootstrap rationale as history; do not remove a nested .git, import engine files or rewrite memory's source history. The deliverable is a current reproducible source-layout contract.

## Acceptance

- [x] A fresh recursive checkout obtains the recorded memory commit and builds using documented sibling SDK dependencies.
- [x] Runtime manifests/catalog/links point to memory.ctg without obsolete vendor-copy or patch bootstrap requirements.
- [x] Existing memory worktrees, ignored stores and repository history remain intact; any remaining portability gap becomes a bounded development-tooling requirement.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `the-memory-workspace-is-tracked-not-patched`; maximum five rounds.
