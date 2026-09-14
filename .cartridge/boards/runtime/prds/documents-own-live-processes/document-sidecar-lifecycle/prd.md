---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: documents-own-live-processes
footprint:
- /Users/feb/dev/cartridge/cartridge.ctg/src/node.rs
- /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/tests/host.rs
---

# A helper program belongs to one node generation and its exit is visible

A cartridge starts a helper with `cartridge.spawn` (`src/node.rs` `spawn`, `Spawned`, reader task, on ws/cartridge.ctg branch `transport-design` `ba198f4`). auth, live, tui and prd each run as one. When a helper exits, its reader task ends silently: pending requests fail, but `cartridge status` keeps the node `active`, so a dead helper looks like a working cartridge. From source; not reproduced yet.

## Acceptance

- [ ] After a helper exits, pending and later `:request` or `:send` calls fail at once with "the program exited", without waiting for `timeout_ms`.
- [ ] While its node runs, an unexpected helper exit shows in `cartridge status` for that cartridge: exit code or signal and the last stderr lines. An explicit `:kill()` is not reported as a failure.
- [ ] Stopping or replacing generation N never ends a helper of generation N+1 or of a sibling node, which keeps answering. `@runtime/launch-authority` proves that N's own helpers end.

## Proof and recovery

First add failing tests next to `a_spawned_program_answers_requests_by_id` and `a_restart_keeps_its_dependents_working` in `.cartridge/tests/unit/src/tests/host.rs`, using a fixture helper that exits after one answer. Gates, cwd `/Users/feb/dev/cartridge`: `just test runtime`, `just check runtime`. They have not run, and they need the transport branch on main. The status field is additive. Rollback: remove the exit report. No restart policy is added.

## Dependencies and review

No hard prerequisite. Shared footprint: `src/node.rs` with `@runtime/launch-authority`. Replacement ordering belongs to `@runtime/extension-loader-plugin-tree`. [Review](review.md): rounds 1–2 inherited; round 3 rebased.
