---
repo: /Users/feb/dev/cartridge/tools.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
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
needs:
- "@runtime/improve-tools-preflight"
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

## From the retired work memo

Folded 2026-09-15 from `work/improve-tools-worktree-resume.md` (status open). The PRD state above is authoritative.

### Outcome

Re-running a partially completed worktree operation either resumes its owned work or explains a conflict without deleting another session's files.

### Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
Related existing work (context/coordination, not automatically a hard dependency): [lane-rm-refuses-after-the-gates-run](../../../root/prds/lane-rm-refuses-after-the-gates-run/prd.md), [lanes-do-not-poison-each-others-builds](../../../root/prds/lanes-do-not-poison-each-others-builds/prd.md).

### Footprint

Workspace tools; one observable outcome. The listed files are starting points and a proposed edit footprint, not permission to make unrelated changes.
All paths below are relative to /Users/feb/dev/cartridge.

- `tools.ctg/service.rs`
- `tools.ctg/tests/test_lane.py`
- `cartridge.ctg/scripts/workspace.py`
- `cartridge.ctg/repositories.json`

Tests/fixtures and owner-local documentation for this outcome may be added beside
these sources. Recheck active claims before changing shared files. Update cartridge.json
only when public services, schema, configuration or verification commands actually change.

### Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] Each injected failure can be retried to one correct worktree without duplicate refs or untracked-file loss.
- [ ] A preexisting unrelated path/branch or active lane is refused; cleanup only removes artifacts attributable to that operation.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Inject failures after ref, directory, worktree registration and build setup. Record ownership and operation identity; preserve active lane claims and refuse ancestry-only cleanup decisions.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

### Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test tools
just check tools
just links
```


### Compatibility and recovery

Use temporary roots and preserve existing development commands. Preflight does not authorize or execute. Cleanup is limited to artifacts owned by the operation; no ancestry-only or blanket deletion of lanes.

### Handoff

Priority P1; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [improve-tools-preflight](../improve-tools-preflight/prd.md) are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
