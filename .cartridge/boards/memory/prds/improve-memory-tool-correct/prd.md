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
canonical-scope: improve-memory-tool-correct
footprint:
- /Users/feb/dev/cartridge/memory.ctg/src/cartridge.rs
- /Users/feb/dev/cartridge/memory.ctg/src/rpc/src/server.rs
- /Users/feb/dev/cartridge/memory.ctg/cartridge.json
needs:
- "@memory/memory-owns-its-tool/memory-adapter-core"
- "@memory/improve-memory-tool-get"
- "@policy/improve-policy-operation-rules"
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

## From the retired work memo

Folded 2026-09-15 from `work/improve-memory-tool-correct.md` (status open). The PRD state above is authoritative.

> Correct or forget one identified fact through the tool boundary

### Outcome

A caller can explicitly correct or forget a specific memory item with a reviewable target and no accidental bulk changes.

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
- [ ] A stale correction leaves the original fact unchanged; a valid correction returns the new identity/revision and retains provenance.
- [ ] Forgetting one ID affects no unrelated fact, requires the configured mutation grant, and has documented retry semantics.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. This is a large slice: use that bounded probe to split implementation into smaller child outcomes if more than one independent state transition or migration is required.
2. Map onto existing engine operations; add compare-against-revision or equivalent stale-target protection. If correction requires several writes, define an atomic engine operation before exposing it. Preserve provenance/history as required by engine semantics and require operation-scoped policy.
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

Priority P2; scope size L (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [improve-memory-tool-get](../improve-memory-tool-get/prd.md), [improve-policy-operation-rules](../../../policy/prds/improve-policy-operation-rules/prd.md) are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
