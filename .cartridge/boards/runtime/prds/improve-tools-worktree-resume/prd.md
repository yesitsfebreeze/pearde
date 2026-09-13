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
canonical-scope: improve-tools-worktree-resume
needs:
- '@runtime/improve-tools-preflight'
footprint:
- /Users/feb/dev/cartridge/cartridge.ctg/scripts/workspace.py
- /Users/feb/dev/cartridge/cartridge.ctg/repositories.json
---

# Recover interrupted worktree creation safely

Re-running a partially completed worktree operation either resumes its owned work or explains a conflict without deleting another session's files.

## Acceptance

- [ ] Each injected failure can be retried to one correct worktree without duplicate refs or untracked-file loss.
- [ ] A preexisting unrelated path/branch or active lane is refused; cleanup only removes artifacts attributable to that operation.

- [ ] Use temporary roots and preserve existing development commands. Preflight does not authorize or execute. Cleanup is limited to artifacts owned by the operation; no ancestry-only or blanket deletion of lanes.

## Proof and recovery

Start at [workspace.py](../../../scripts/workspace.py), [repositories.json](../../../repositories.json).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-tools-worktree-resume`; maximum five rounds.
