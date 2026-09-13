---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: runtime
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-tools-preflight
footprint:
- /Users/feb/dev/cartridge/cartridge.ctg/scripts/workspace.py
- /Users/feb/dev/cartridge/cartridge.ctg/repositories.json
---

# Preview workspace-tool effects before execution

Own one preview/apply contract in the surviving runtime development package. Preview reports operation ID, canonical repository/path identities, prerequisite tools and planned effects without changing files/refs. Apply revalidates those inputs; preflight is not authorization.

## Acceptance

- [ ] Bundle and worktree previews leave refs/files byte-identical and identify missing prerequisites.
- [ ] A target/repository change invalidates the old preview before any operation-owned creation.
- [ ] Apply performs only the named reviewed operation; compatibility shims call the same implementation and no second generic executor is introduced.

## Proof and recovery

Start at [workspace.py](../../../scripts/workspace.py), [repositories.json](../../../repositories.json).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-tools-preflight`; maximum five rounds.
