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
canonical-scope: improve-memory-tool-get
needs:
- '@memory/memory-owns-its-tool/memory-adapter-core'
footprint:
- /Users/feb/dev/cartridge/memory.ctg/src/cartridge.rs
---

# Agents read one recalled fact back by ID through tool.memory

The memory service already serves exact reads: `{"op":"get","id"}` goes through `operation` in `src/cartridge.rs` to `query_by_id` in `src/rpc/src/server.rs`, and `.cartridge/tests/integration/cartridge.rs` covers it through an attached owner. The agent tool does not. `tool_describe` offers only `query|ingest`, and `tool_call` reads a `sync` field the schema never declares. Outcome, owned by memory: `tool.memory` gains `get`, lists it in `reads`, and validates each operation's arguments in the adapter. MCP and agent consumers relay the descriptor and need no knowledge of memory (decision `a-cartridge-brings-its-own-surface`).

## Acceptance

- [ ] A `tool.memory` query followed by `get` on a returned ID yields the same id, text, status and source. `describe` lists `get` with `id` required and `reads: ["query","get"]`.
- [ ] Each of these returns `error: true` with a distinct message and no engine call: a missing or empty id, `k` outside 1..20, text over 65536 bytes, or an undeclared field (including `sync` on query or get). An unknown ID returns not-found and never falls back to a semantic query.
- [ ] With an attached owner, `get` passes owner read validation. A disconnected owner returns an explicit error, never an empty result.
- [ ] Existing query and ingest calls keep their output shape, and `.cartridge/help.md` documents `get`.

## Proof and recovery

First probe: call `tool.memory` with `{"op":"get","id":…}` at memory.ctg `c25af4d` and record the refusal. Extend `.cartridge/tests/unit/src/cartridge/tests.rs` and the existing `tool.memory` case in `.cartridge/tests/integration/cartridge.rs`. Gates, from /Users/feb/dev/cartridge/memory.ctg: `just check` and `just test`, neither run in planning. Default decision: declare `sync` for ingest only. Rollback: revert the descriptor and `tool_call` arms. The operation only reads, so store bytes stay untouched.

## Dependencies and review

The adapter-core need appears delivered; the coordinator should verify it. Shares its footprint with the errors and correct leaves; land this one first. [Review history](review.md): round 3 of 5.
