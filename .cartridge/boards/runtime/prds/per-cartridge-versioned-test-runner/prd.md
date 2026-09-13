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
canonical-scope: per-cartridge-versioned-test-runner
---

# per cartridge versioned test runner

Cache verification evidence by source-tree/dirty digest, dependency revisions, test recipe, relevant configuration and toolchain/platform identity. Manifest version is descriptive metadata only. Run operation-owned isolated artifacts and expose stale/missing evidence explicitly.

## Acceptance

- [ ] Changing code without bumping version invalidates the result and reruns the affected contract.
- [ ] A changed dependency or gate command invalidates downstream evidence, while truly unchanged inputs reuse the prior exact result.
- [ ] Two divergent worktrees produce and execute their own binaries; an unavailable build or failed suite cannot overwrite prior evidence as a success.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `per-cartridge-versioned-test-runner`; maximum five rounds.
