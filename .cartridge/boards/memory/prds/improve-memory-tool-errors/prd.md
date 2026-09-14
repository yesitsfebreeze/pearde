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
canonical-scope: improve-memory-tool-errors
needs:
- '@memory/memory-owns-its-tool/memory-adapter-core'
footprint:
- /Users/feb/dev/cartridge/memory.ctg/src/cartridge.rs
---

# tool.memory failures carry a stable code the agent can act on

Today `tool.memory` failures are free prose inside `{content, error:true}` (`tool_failure` in `src/cartridge.rs`). An ingest that did not commit returns the raw engine reply. Engine and transport errors from `memory(...).await?` escape as provider errors, not tool results, so consumers see different failure shapes. Outcome, owned by memory: one translation point in the adapter maps every outcome to a JSON content body `{code, message, call}`. The codes are `invalid_input`, `writer_contended`, `dependency_unavailable`, `ingest_refused` and `ingest_unknown`. The `{content: string, error: bool}` wire stays unchanged.

## Acceptance

- [ ] Invalid arguments return `invalid_input` without opening a store, proven the same way as `invalid_operations_do_not_open_a_store`.
- [ ] A stopped fixture embed server returns `dependency_unavailable`, and so does a disconnected attached owner. A process that finds the store writer held returns `writer_contended`. None of these returns `error:false` with an empty recall.
- [ ] An engine reply whose `status` is not `committed` returns `ingest_refused`. A worker failure after an ingest was dispatched returns `ingest_unknown` with the call ID and advice to verify by query. The adapter never retries.
- [ ] Successful query and ingest content is unchanged in the existing integration case, and `.cartridge/help.md` lists the codes.

## Proof and recovery

First probe: at memory.ctg `c25af4d`, reproduce each failure using the `test_support` fixed-vector HTTP embed and record the content returned today. Tests go in `.cartridge/tests/unit/src/cartridge/tests.rs` and `.cartridge/tests/integration/cartridge.rs`. Gates from /Users/feb/dev/cartridge/memory.ctg: `just check` and `just test`, both not run. Rollback: revert the mapping. No stored state changes.

## Dependencies and review

Adapter-core appears delivered; verify it. Uses the same file as get and correct, so land it after get. [Review history](review.md): round 3 of 5.
