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
canonical-scope: one-runner-executes-documents
needs:
- '@runtime/one-runner-executes-documents/document-command-result'
---

# An artifact result reads only the approved output

Open a successful command's regular artifact beneath its permitted root without following replacement symlinks.

## Acceptance

- [ ] A successful fixture returns the declared file with bounds.
- [ ] Nonzero exit never yields a successful artifact.
- [ ] Traversal, symlink and replacement races expose no outside file and retain the command outcome.

## Proof and recovery

Start at [runtime.rs](../../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `one-runner-executes-documents`; maximum five rounds.
