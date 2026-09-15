---
repo: /Users/feb/dev/cartridge/memory.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: MEMORY-002
---

# CLI and RPC name the same memory counts

Memory counts are reported in two vocabularies. RPC `health` returns `entities`, `reasons` and `memories` (`health_stats` in `src/rpc/src/server.rs`), while `memory health` prints the same numbers as `thoughts:` (`src/commands/src/commands_health.rs`). The hub list mixes `loaded`/`cold` project daemons with counts of resident rows only (`src/commands/src/commands_hub.rs`), and no term separates stored rows (hot plus cold) from the resident working set. Outcome, owned by memory: one documented vocabulary for stored versus resident rows and loaded versus unloaded daemons, applied to CLI labels and help, with RPC wire keys unchanged.

## Acceptance

- [ ] For one fixture snapshot, `memory health` and RPC `health` report equal numbers, and each label maps to one term documented in `.cartridge/help.md` and `.cartridge/docs/README.md`.
- [ ] On a half-cold fixture, stored and resident counts differ and carry distinct labels; hub status labels daemon loading separately from row counts.
- [ ] RPC keys, store layout and legacy decoders are unchanged, and the existing legacy-store and health e2e tests pass at the same revision.

## Proof and recovery

First probe: build a half-cold fixture at memory.ctg `c25af4d` and record both the CLI output and the RPC JSON. Add a CLI/RPC comparison test beside `.cartridge/tests/integration/e2e/health_surface.rs`. Gates, run from /Users/feb/dev/cartridge/memory.ctg: `just check`, `just test`, then `just all`; none has run yet. `.cartridge/docs/WORK_ITEMS.md` names an owner branch `codex/memory-terminology` and commits `0d3ce338`/`15862820`, but on 2026-09-14 none exists in memory.ctg and no `~/dev/memory-worktree-archives` exists. Before claiming, confirm with the user that the reservation lapsed; use any recovered wording only as reference. Rollback: revert the labels; no data changes.

## Dependencies and review

No hard needs. [Review history](review.md): rounds 1–2 inherited, round 3 rebased; maximum five.
