---
repo: /Users/feb/dev/cartridge/tools.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: runtime
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: improve-tools-worktree-resume
footprint:
- /Users/feb/dev/cartridge/tools.ctg/src/service.rs
- /Users/feb/dev/cartridge/tools.ctg/.cartridge/tests/integration/lane.test.ts
---

# Recover interrupted worktree creation safely

Re-running `lane <name>` after a partial creation resumes the operation's own
worktree or refuses with the conflicting path or branch named, never deleting
another session's files. Owner: the `tools` cartridge, function `lane()` in
`tools.ctg/src/service.rs`.

Current behavior, from source reading (not yet reproduced): a registered lane on
`work/<name>` is re-provisioned; an unregistered existing directory is refused.
Two gaps remain. A leftover `work/<name>` branch without a worktree makes
`git worktree add -b` fail with no resume path. Any registered worktree whose
directory is missing makes `canonicalize()?` fail, so every lane operation fails.

## Acceptance

- [ ] After each injected interruption (branch created without worktree; registration whose directory was deleted; provisioning failed after add), re-running `lane` yields one worktree on `work/<name>` with no duplicate branch and no lost commits.
- [ ] A stale registration for another lane no longer blocks `lane`, `land` or `lane-rm`; it is reported, never pruned automatically.
- [ ] An unregistered directory, a branch checked out elsewhere, or a locked lane is refused by name, with files and refs unchanged.

## Proof and recovery

First run `just test tools` from `/Users/feb/dev/cartridge` and record whether
`lane.test.ts` still launches: it names `cartridge.ctg/builtin`, which no longer
exists. If it cannot launch, repairing that fixture is step one. Add the cases
to `lane.test.ts`; gates are `just test tools` and `just check tools`. Rollback
is reverting `lane()`; git refs and worktrees are the only durable state.

## Dependencies and review

No hard prerequisite. Shares `service.rs` with preflight and bundle provenance:
land serially. [Review](review.md): round 3/5.
