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
canonical-scope: degrade-corrects-the-retrieval-path-it-names
---

# Degrade weakens only the retrieval paths a query named

Today `degrade` takes a thought ID under the misleading name `query_id` and decays every reason on that thought (`tool_degrade` in `src/rpc/src/server.rs`, `degrade_entity_reasons` in `src/graph/src/graph_ops.rs`, CLI `cmd_degrade` in `src/commands/src/commands_graph_ops.rs`). Memory retains no query provenance. Outcome, owned by memory: the `memory` service accepts a feedback handle `{store, thought, reasons:[{id, score_lamport}]}` (at most 16 reasons) and weakens only those reasons. The default design is stateless: the handle comes from an explained query and is validated against the live graph. There is no new provenance store and no tombstone (memory decision `does-a-removal-need-a-tombstone`).

## Acceptance

- [ ] A fixture query with `explain` yields a handle. Degrading it changes only the named reasons; every other reason on that thought keeps its score and lamport.
- [ ] A reason not attached to the thought, an unknown reason, a wrong store (`replica_id`) or a changed `score_lamport` is refused with a distinct error, and nothing is mutated or saved.
- [ ] Replaying an applied handle is refused as stale, never decayed twice. The legacy `query_id` form keeps its whole-thought behaviour and is documented as such in `.cartridge/help.md`.

## Proof and recovery

First probe, at memory.ctg `c25af4d`: check whether explain output (`retrieval_format_chains` / `retrieval_finalize_explanation` in `src/retrieval/piece/src/lib.rs`) already carries reason IDs and lamports. If not, adding them is step one. Tests belong in `.cartridge/tests/unit/src/rpc/src/tests/` beside the existing graph_ops tests. Gates, from /Users/feb/dev/cartridge/memory.ctg: `just check`, `just test`. Neither was run for this plan. Rollback: revert the handle arm. Refusals write nothing, so store bytes stay unchanged.

## Dependencies and review

No hard needs. Shares `src/rpc/src/server.rs` with the tool leaves; coordinate landing. [Review history](review.md): rounds 1–2 inherited, round 3 rebased; maximum five.
