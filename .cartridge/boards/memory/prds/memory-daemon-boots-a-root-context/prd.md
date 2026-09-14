---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: memory-daemon-boots-a-root-context
---

# Memory's owner refuses writes while draining and survives a failed replacement

Memory owns its store through two lifecycles: the CLI daemon (`run_server` in `src/commands/src/commands_serve.rs`) and the transport cartridge (`on_dispose` in `src/cartridge.rs`). Three gaps are visible at `c25af4d`:

- While shutdown runs, `invoke` refuses only model-dependent ops (`src/rpc/src/server.rs`). forget, degrade, move, promote, pulse and gc are still admitted while `save_fn` runs.
- A replacement daemon evicts its predecessor (`evict_predecessor`) before it knows it can boot, and continues "anyway" after a timeout.
- `ready` reports pid and draining state but not store state.

Outcome, owned by memory: fix only those three gaps. There is no plugin tree or root Context; memory decision `memory-is-a-plugin-tree` conflicts with the repository scope in `.cartridge/docs/AGENTS.md`.

## Acceptance

- [ ] Once shutdown begins, every mutating op is refused with a draining error. In-flight calls complete and their effects are included in the final save (`lifecycle_test.rs` plus a `server_admin_test.rs` case).
- [ ] A replacement whose config or store-directory validation fails exits without stopping the running owner, which keeps answering `health` with the same pid (`e2e/lifecycle.rs`).
- [ ] `ready` reports store state (opening, ready, draining or unavailable), consistent with cartridge `status`, and the cartridge `on_dispose` path follows the same admission rule.

## Proof and recovery

First probe: reproduce each gap in a disposable store with the existing e2e harness and record what happens. Gates, from /Users/feb/dev/cartridge/memory.ctg: `just check`, `just test`, `just e2e` (not run). Rollback: revert per gap; the writer lock and guarded flush stay the durability boundary.

## Dependencies and review

No hard needs. Shares its lifecycle files with memory-signals-become-events, so land this first. [Review history](review.md): rounds 1–2 inherited, round 3 rebased; maximum five.
