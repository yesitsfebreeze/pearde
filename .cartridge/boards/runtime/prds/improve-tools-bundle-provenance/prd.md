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
canonical-scope: improve-tools-bundle-provenance
needs:
- '@runtime/improve-tools-preflight'
footprint:
- /Users/feb/dev/cartridge/cartridge.ctg/scripts/workspace.py
- /Users/feb/dev/cartridge/cartridge.ctg/repositories.json
---

# Ship bundles with source and dependency provenance

Deliver the provenance contract in the runtime-owned development package, preserving this work ID and its fixture when tools.ctg is relocated. Record repository commits/dirty digests, executable checksums, dependency inventory and recipe/toolchain/configuration identities; do not claim reproducible binary bytes solely from reproducible metadata.

## Acceptance

- [ ] Unchanged fixture inputs yield identical metadata; a changed executable, dependency or dirty source changes its corresponding digest.
- [ ] Missing required binaries fail before bundle publication, and credentials/private stores never enter the output.
- [ ] The old command shim and new package produce equivalent manifests during the migration interval.

## Proof and recovery

Start at [workspace.py](../../../scripts/workspace.py), [repositories.json](../../../repositories.json).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-tools-bundle-provenance`; maximum five rounds.
