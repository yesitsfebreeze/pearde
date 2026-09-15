---
kind: work
description: "Correct or forget one identified fact through the tool boundary"
status: open
priority: P2
size: L
needs:
  - "[improve-memory-tool-get](../../../memory/prds/improve-memory-tool-get/prd.md)"
  - "[improve-policy-operation-rules](../../../policy/prds/improve-policy-operation-rules/prd.md)"
uses:
  - usage: "[[read-usage]]"
    when: ["correct or forget one identified fact through the tool boundary", "implementing memory-tool cartridge improvements"]
---

# Correct or forget one identified fact through the tool boundary

## Outcome

A caller can explicitly correct or forget a specific memory item with a reviewable target and no accidental bulk changes.

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
- [ ] A stale correction leaves the original fact unchanged; a valid correction returns the new identity/revision and retains provenance.
- [ ] Forgetting one ID affects no unrelated fact, requires the configured mutation grant, and has documented retry semantics.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

## Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. This is a large slice: use that bounded probe to split implementation into smaller child outcomes if more than one independent state transition or migration is required.
2. Map onto existing engine operations; add compare-against-revision or equivalent stale-target protection. If correction requires several writes, define an atomic engine operation before exposing it. Preserve provenance/history as required by engine semantics and require operation-scoped policy.
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

Priority P2; scope size L (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [improve-memory-tool-get](../../../memory/prds/improve-memory-tool-get/prd.md), [improve-policy-operation-rules](../../../policy/prds/improve-policy-operation-rules/prd.md) are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
