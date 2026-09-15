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
commit: "a458148fb21f85cabcd9e1ced85c96c581b8e0b2"
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

## From the retired work memo

Folded 2026-09-15 from `work/a-shadowing-write-passes-the-leaf-check.md` (status open). The PRD state above is authoritative.

> A workspace memo that shadows a shipped memo of the same leaf accepts writes; today the write is refused as a duplicate

### Outcome

A write to a workspace memo whose leaf is also shipped by a cartridge (the
shadowing case `type/type.md` documents) validates and saves. Today every
write to such a memo fails with "duplicate memo leaf", so the workspace
checkpoint note cannot be updated through the tool at all while the memory
cartridge ships `dashboards/work-checkpoint.md`.

### Check

- [ ] `zirkle run memo` write to `note/work-checkpoint.md` (leaf shared with
      the shipped `@memory/dashboards/work-checkpoint.md`) saves and returns a
      revision.
- [ ] A workspace memo whose leaf collides with a shipped memo still shadows
      it in reads and listings, per `type/type.md`.

### Context

Found 2026-09-12 from the trunk: `builtin/memo/src/record.rs` (which has
uncommitted edits from another session, not to be touched by the fix's lane
until those land) rejects the union of workspace and shipped memos on a leaf
collision before the shadowing rule applies.
