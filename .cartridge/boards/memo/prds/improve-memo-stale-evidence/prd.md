---
repo: /Users/feb/dev/cartridge/memo.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: memo
work-kind: leaf
review-round: 3
review-status: accepted
canonical-scope: improve-memo-stale-evidence
footprint:
- src/usage.rs
- .cartridge/templates/seeds/type/resource.md
- .cartridge/tests/integration/resolver.rs
commit: "a458148fb21f85cabcd9e1ced85c96c581b8e0b2"
---

# Distinguish stale source references from current guidance

Discovery reports missing or changed referenced files and explains freshness without rewriting historical decisions or falsely declaring them obsolete.

## Acceptance

- [x] Rename a referenced source in a temporary repository: discovery labels the stale target and preserves its original reference and revision.
- [x] A current routine and completed historical work remain separately retrievable; unverified outcomes retain their caller-reported label.

- [x] Keep the prior response shape available during migration. Roll back presentation/ranking changes without rewriting authored records or evidence journals.

## Proof and recovery

Start at [service.rs](../../../../../../memo.ctg/src/service.rs), [record.rs](../../../../../../memo.ctg/src/record.rs), [resolver.rs](../../../../../../memo.ctg/src/resolver.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test memo` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-memo-stale-evidence`; maximum five rounds.

## From the retired work memo

Folded 2026-09-15 from `work/improve-memo-stale-evidence.md` (status open). The PRD state above is authoritative.

### Outcome

Discovery reports missing or changed referenced files and explains freshness without rewriting historical decisions or falsely declaring them obsolete.

### Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
Related existing work (context/coordination, not automatically a hard dependency): [a-search-ranks-current-guidance-over-delivered-history](../../../landscape/prds/a-search-ranks-current-guidance-over-delivered-history/prd.md), [handle-memory-staleness-and-conflicts](../handle-memory-staleness-and-conflicts/prd.md).

### Footprint

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

### Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] Rename a referenced source in a temporary repository: discovery labels the stale target and preserves its original reference and revision.
- [ ] A current routine and completed historical work remain separately retrievable; unverified outcomes retain their caller-reported label.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Reuse existing revision digests and staleness metadata. Add repository-structure checks for resource targets and explicit history/current presentation; extend the existing ranking item's corpus rather than creating a second ranker.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

### Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test memo
just check memo
just test landscape
just check landscape
```


### Compatibility and recovery

Keep the prior response shape available during migration. Roll back presentation/ranking changes without rewriting authored records or evidence journals.

### Handoff

Priority P1; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
No hard prerequisite inside this programme; ready for an owner after source/claim checks.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
