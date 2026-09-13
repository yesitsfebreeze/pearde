---
kind: work
description: "Expose fact provenance freshness and conflicts consistently"
status: open
priority: P1
size: M
uses:
  - usage: "[[read-usage]]"
    when: ["expose fact provenance freshness and conflicts consistently", "implementing memory cartridge improvements"]
---

# Expose fact provenance freshness and conflicts consistently

## Outcome

Query and get responses identify source, observation/update time where known, lifecycle status and conflicting evidence so callers can assess a recalled fact.

## Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
No matching existing owner was identified for this exact outcome during the planning pass.

## Footprint

Memory; one observable outcome. The listed files are starting points and a proposed edit footprint, not permission to make unrelated changes.
All paths below are relative to /Users/feb/dev/cartridge.

- `memory.ctg/src/cartridge.rs`
- `memory.ctg/src/transport/src`
- `memory.ctg/src/commands/src`
- `memory.ctg/tests/cartridge.rs`
- `memory.ctg/CARTRIDGE.md`

Tests/fixtures and owner-local documentation for this outcome may be added beside
these sources. Recheck active claims before changing shared files. Update cartridge.json
only when public services, schema, configuration or verification commands actually change.

## Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] Seed an updated fact with its older conflicting source: query/get preserve both identities and explain status and provenance.
- [ ] A legacy fact lacking dates returns unknown freshness and remains readable; unavailable evidence is not fabricated.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

## Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Inventory existing engine metadata before adding fields. Preserve engine ownership and distinguish unknown freshness from confirmed stale. Reuse stored links/versions for contradictions; never infer contradiction from a missing field.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

## Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test memory --test cartridge
just check memory
just test memory
```

Implementation must use an isolated branch/worktree per memory.ctg/AGENTS.md. Run the memory repository's full required gates before landing; preserve databases, provenance and documents.

## Compatibility and recovery

Keep the current exclusive-writer invariant and existing on-disk formats. On attachment/readiness failure return an explicit error; reverting the adapter must not require rewriting the store. Any schema addition needs a backwards-compatible reader and a tested migration boundary.

## Handoff

Priority P1; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
No hard prerequisite inside this programme; ready for an owner after source/claim checks.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
