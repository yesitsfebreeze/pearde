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
canonical-scope: improve-memory-tool-errors
footprint:
- /Users/feb/dev/cartridge/memory.ctg/src/cartridge.rs
needs:
- "@memory/memory-owns-its-tool/memory-adapter-core"
- "@root/improve-tool-result-contract"
- "@memory/improve-memory-readiness"
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

## From the retired work memo

Folded 2026-09-15 from `work/improve-memory-tool-errors.md` (status open). The PRD state above is authoritative.

> Return actionable memory failures and enforce the tool schema

### Outcome

A failed tool call distinguishes contention, unavailable dependencies, invalid input and committed-versus-uncertain ingestion.

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
- [ ] Inject lock contention, model timeout and invalid input: MCP clients receive distinct codes with concise safe details.
- [ ] Ingestion committed, refused and unknown completion remain distinguishable; invalid arguments cause no engine call.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Define machine-readable error codes and retryability under the shared tool result contract. Translate engine errors once, validate inputs before crossing the service boundary, and never retry a write with uncertain completion automatically.
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

Priority P0; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [improve-tool-result-contract](../../../root/prds/improve-tool-result-contract/prd.md), [improve-memory-readiness](../improve-memory-readiness/prd.md) are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
