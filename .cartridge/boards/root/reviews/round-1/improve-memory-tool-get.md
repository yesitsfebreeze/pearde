---
kind: work
description: "Retrieve a recalled fact by stable ID"
status: open
priority: P1
size: M
needs:
  - "[[@prd/work/root--improve-tool-result-contract.md]]"
  - "[[@prd/work/root--improve-memory-provenance.md]]"
uses:
  - usage: "[[read-usage]]"
    when: ["retrieve a recalled fact by stable id", "implementing memory-tool cartridge improvements"]
---

# Retrieve a recalled fact by stable ID

## Outcome

Every returned memory reference can be followed to a bounded get response without guessing another text query.

## Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
No matching existing owner was identified for this exact outcome during the planning pass.

## Footprint

Memory tool adapter; one observable outcome. The listed files are starting points and a proposed edit footprint, not permission to make unrelated changes.
All paths below are relative to /Users/feb/dev/cartridge.

- `memory-tool.ctg/src/main.rs`
- `memory-tool.ctg/cartridge.json`
- `memory.ctg/src/cartridge.rs`
- `policy.ctg/init.lua`

Tests/fixtures and owner-local documentation for this outcome may be added beside
these sources. Recheck active claims before changing shared files. Update cartridge.json
only when public services, schema, configuration or verification commands actually change.

## Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] Query a seeded fact then get its ID through the real MCP bridge; text, ID and provenance agree.
- [ ] Invalid k, oversized text, unknown properties, missing ID and absent fact return defined errors matching the advertised schema.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

## Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Extend the adapter to the engine's existing get operation. Use operation-specific input validation, preserving query/ingest defaults and limits; reject unknown fields including undocumented sync unless intentionally added to the schema.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

## Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test memory-tool
just check memory-tool
just test memory --test cartridge
just test policy
```


## Compatibility and recovery

Keep query/ingest compatible during extension. New mutations are opt-in policy operations; reverting the tool adapter must leave engine contents intact. Do not consolidate repositories as part of this leaf.

## Handoff

Priority P1; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [[@prd/work/root--improve-tool-result-contract.md]], [[@prd/work/root--improve-memory-provenance.md]] are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
