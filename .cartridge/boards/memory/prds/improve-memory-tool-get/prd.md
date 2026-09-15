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
canonical-scope: improve-memory-tool-get
footprint:
- /Users/feb/dev/cartridge/memory.ctg/src/cartridge.rs
needs:
- "@memory/memory-owns-its-tool/memory-adapter-core"
- "@root/improve-tool-result-contract"
- "@memory/improve-memory-provenance"
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

## From the retired work memo

Folded 2026-09-15 from `work/improve-memory-tool-get.md` (status open). The PRD state above is authoritative.

> Retrieve a recalled fact by stable ID

### Outcome

Every returned memory reference can be followed to a bounded get response without guessing another text query.

### Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
No matching existing owner was identified for this exact outcome during the planning pass.

### Footprint

Memory tool adapter; one observable outcome. The listed files are starting points and a proposed edit footprint, not permission to make unrelated changes.
All paths below are relative to /Users/feb/dev/cartridge.

- `memory-tool.ctg/src/main.rs`
- `memory-tool.ctg/cartridge.json`
- `memory.ctg/src/cartridge.rs`
- `policy.ctg/init.lua`

Tests/fixtures and owner-local documentation for this outcome may be added beside
these sources. Recheck active claims before changing shared files. Update cartridge.json
only when public services, schema, configuration or verification commands actually change.

### Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] Query a seeded fact then get its ID through the real MCP bridge; text, ID and provenance agree.
- [ ] Invalid k, oversized text, unknown properties, missing ID and absent fact return defined errors matching the advertised schema.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Extend the adapter to the engine's existing get operation. Use operation-specific input validation, preserving query/ingest defaults and limits; reject unknown fields including undocumented sync unless intentionally added to the schema.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

### Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test memory-tool
just check memory-tool
just test memory --test cartridge
just test policy
```


### Compatibility and recovery

Keep query/ingest compatible during extension. New mutations are opt-in policy operations; reverting the tool adapter must leave engine contents intact. Do not consolidate repositories as part of this leaf.

### Handoff

Priority P1; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [improve-tool-result-contract](../../../root/prds/improve-tool-result-contract/prd.md), [improve-memory-provenance](../improve-memory-provenance/prd.md) are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
