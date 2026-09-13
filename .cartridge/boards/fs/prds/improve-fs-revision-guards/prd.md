---
repo: /Users/feb/dev/cartridge/fs.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: fs
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-fs-revision-guards
footprint:
- /Users/feb/dev/cartridge/fs.ctg/service.rs
- /Users/feb/dev/cartridge/fs.ctg/files.rs
- /Users/feb/dev/cartridge/fs.ctg/search.rs
- /Users/feb/dev/cartridge/fs.ctg/service/tests.rs
---

# Use consistent stale-write checks for filesystem mutations

Remove improve-fs-change-provenance from the proposed hard needs: basic stale-write safety must work with current sessions. Reuse existing revision and atomic-write boundaries; attribution additions remain independent. A check-then-write race must be addressed at the actual mutation boundary, not only in request validation.

## Acceptance

- [ ] A deterministic barrier changes the file after validation but before commit; newer bytes survive and the stale writer receives a conflict.
- [ ] Two writers with the same expected revision cannot both overwrite successfully.
- [ ] Direct and overlay APIs preserve executable modes, path validation, cancellation and explicitly reported partial success without importing external ownership.

## Proof and recovery

Start at [service.rs](../../../service.rs), [files.rs](../../../files.rs), [search.rs](../../../search.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test fs` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-fs-revision-guards`; maximum five rounds.
