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
canonical-scope: improve-memory-tool-correct
needs:
- '@memory/memory-owns-its-tool/memory-adapter-core'
- '@memory/improve-memory-tool-get'
footprint:
- /Users/feb/dev/cartridge/memory.ctg/src/cartridge.rs
- /Users/feb/dev/cartridge/memory.ctg/src/rpc/src/server.rs
- /Users/feb/dev/cartridge/memory.ctg/cartridge.json
---

# Agents correct or forget one identified fact through tool.memory

The service already has a hard single-row `forget` (`tool_forget` → `graph_ops::forget_entity` with `Removal::Explicit{force:false}`) and supersede chains (`Supersedes` reasons, walked by history in `src/rpc/src/server.rs`). `tool.memory` exposes neither, and no operation supersedes a named fact with new text. Outcome, owned by memory: two opt-in tool operations, both refused unless the memory setting `tool_writes` is true (default false). `forget {id}` removes exactly that row under the existing refusal policy. `correct {id, text}` commits a new row that supersedes `id` at the same source, as one engine operation under the store writer. Removal stays hard, with no tombstones (memory decision `does-a-removal-need-a-tombstone`). Neither operation is listed in `reads`, so composition policy treats both as writes.

## Acceptance

- [ ] `correct` returns the new ID, and `get` shows its text and source. The old ID is reachable only as superseded history. Exactly one save happens.
- [ ] `correct` on an unknown or already superseded ID, or `forget` on an unknown or policy-refused ID, returns a distinct error and changes no store bytes.
- [ ] `forget` removes only the named row and its own edges, and the tool cannot reach any by-source or bulk deletion. With `tool_writes` false, both operations are refused before any engine call.
- [ ] If a worker fails after dispatch, the tool reports an unknown outcome with the ID to check via get. The adapter never repeats the mutation.

## Proof and recovery

Land the `forget` exposure and `correct` as separate specs and commits. First probe: confirm whether an ingest with an explicit source and section already supersedes a row, and reuse that path. Tests go in `.cartridge/tests/unit/src/rpc/src/tests/` and `.cartridge/tests/integration/cartridge.rs`. Gates, from /Users/feb/dev/cartridge/memory.ctg: `just check`, `just test` (not run). Rollback: set `tool_writes` false. Superseded history is preserved.

## Dependencies and review

[Review history](review.md): round 3 of 5.
