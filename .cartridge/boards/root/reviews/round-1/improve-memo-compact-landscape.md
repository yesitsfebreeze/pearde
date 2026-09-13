---
kind: work
description: "Bound landscape discovery and offer inventory drilldown"
status: open
priority: P1
size: M
uses:
  - usage: "[[read-usage]]"
    when: ["bound landscape discovery and offer inventory drilldown", "implementing memo cartridge improvements"]
---

# Bound landscape discovery and offer inventory drilldown

## Outcome

A default landscape query returns relevant providers and references within a configurable output budget, without returning every tracked path.

## Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
Related existing work (context/coordination, not automatically a hard dependency): [[@prd/work/root--a-search-ranks-current-guidance-over-delivered-history.md]], [[handle-memory-staleness-and-conflicts]].

## Footprint

Memo; one observable outcome. The listed files are starting points and a proposed edit footprint, not permission to make unrelated changes.
All paths below are relative to /Users/feb/dev/cartridge.

- `memo.ctg/src/service.rs`
- `memo.ctg/src/record.rs`
- `memo.ctg/src/resolver.rs`
- `landscape.ctg/src/lib.rs`
- `landscape.ctg/src/surface.rs`

Tests/fixtures and owner-local documentation for this outcome may be added beside
these sources. Recheck active claims before changing shared files. Update cartridge.json
only when public services, schema, configuration or verification commands actually change.

## Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] A 10,000-path fixture returns a default summary of at most 16 KiB and reports omitted counts; explicit inventory pages reconstruct the permitted paths.
- [ ] Paging detects a replaced host snapshot; contributor failure is identified rather than represented as a complete empty result.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

## Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Capture current response bytes on a fixed many-file fixture. Keep stable IDs, generations, source pointers, counts and partial-data diagnostics in the summary; add explicit inventory detail paging. Preserve compatibility through a versioned/additive request option before changing defaults.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

## Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test memo
just check memo
just test landscape
just check landscape
```


## Compatibility and recovery

Keep the prior response shape available during migration. Roll back presentation/ranking changes without rewriting authored records or evidence journals.

## Handoff

Priority P1; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
No hard prerequisite inside this programme; ready for an owner after source/claim checks.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
