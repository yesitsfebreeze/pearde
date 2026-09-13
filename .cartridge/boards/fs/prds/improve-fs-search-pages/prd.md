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
canonical-scope: improve-fs-search-pages
footprint:
- /Users/feb/dev/cartridge/fs.ctg/service.rs
- /Users/feb/dev/cartridge/fs.ctg/files.rs
- /Users/feb/dev/cartridge/fs.ctg/search.rs
- /Users/feb/dev/cartridge/fs.ctg/service/tests.rs
---

# Bound and continue file search without losing result identity

Large filesystem searches return bounded results with stable continuation behavior and explicit truncation/change diagnostics.

## Acceptance

- [ ] A large fixture paginates all matching paths without duplicates or silent omissions under the documented consistency model.
- [ ] Tree changes, invalid/expired cursors and cancellation produce explicit outcomes; a bounded result never masquerades as complete.

- [ ] Preserve direct filesystem semantics and keep GitFS overlay ownership distinct. New attribution is additive; never auto-import external edits into a session. Retain guarded write behavior and explicit partial failures.

## Proof and recovery

Start at [service.rs](../../../service.rs), [files.rs](../../../files.rs), [search.rs](../../../search.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test fs` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-fs-search-pages`; maximum five rounds.
