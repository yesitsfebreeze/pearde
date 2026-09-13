---
repo: /Users/feb/dev/cartridge/memo.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memo
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: a-shadowing-write-passes-the-leaf-check
commit: "648b420fd12e38d7d07e934595e57fdaa74ae51b"
---

# a-shadowing-write-passes-the-leaf-check

Apply intentional workspace shadowing before uniqueness validation, retaining distinct owner-qualified source identity. Reject two unrelated workspace definitions with the same leaf and ambiguous shipped collisions. Reconcile this behavior with the canonical document parser contract rather than relaxing duplicate checks globally.

## Acceptance

- [x] A workspace write shadowing the permitted shipped leaf saves with a new revision and is returned by the legacy unqualified read.
- [x] Owner-qualified read still reaches the shipped original; another owner's identical basename is not overwritten or merged.
- [x] Two conflicting local definitions, stale expected revision and an unapproved shipped-file write fail without mutation.

## Proof and recovery

Start at [service.rs](../../../../../../memo.ctg/src/service.rs), [record.rs](../../../../../../memo.ctg/src/record.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test memo` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `a-shadowing-write-passes-the-leaf-check`; maximum five rounds.
