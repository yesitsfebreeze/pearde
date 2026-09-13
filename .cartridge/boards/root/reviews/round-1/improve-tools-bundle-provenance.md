---
kind: work
description: "Ship bundles with source and dependency provenance"
status: open
priority: P2
size: M
needs:
  - "[[@prd/work/root--improve-tools-preflight.md]]"
uses:
  - usage: "[[read-usage]]"
    when: ["ship bundles with source and dependency provenance", "implementing tools cartridge improvements"]
---

# Ship bundles with source and dependency provenance

## Outcome

A generated bundle identifies exact repository revisions, dirty state, executable checksums and dependency inventory.

## Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
Related existing work (context/coordination, not automatically a hard dependency): [[@prd/work/root--lane-rm-refuses-after-the-gates-run.md]], [[@prd/work/root--lanes-do-not-poison-each-others-builds.md]].

## Footprint

Workspace tools; one observable outcome. The listed files are starting points and a proposed edit footprint, not permission to make unrelated changes.
All paths below are relative to /Users/feb/dev/cartridge.

- `tools.ctg/service.rs`
- `tools.ctg/tests/test_lane.py`
- `cartridge.ctg/scripts/workspace.py`
- `cartridge.ctg/repositories.json`

Tests/fixtures and owner-local documentation for this outcome may be added beside
these sources. Recheck active claims before changing shared files. Update cartridge.json
only when public services, schema, configuration or verification commands actually change.

## Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] Two bundles from unchanged fixtures produce identical provenance metadata; a changed executable/revision changes the appropriate entries.
- [ ] Missing required binaries fail packaging; no provider credentials or live state are included.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

## Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Extend existing bundling with a deterministic machine-readable manifest excluding credentials and private stores. Distinguish reproducible metadata from a claim of reproducible binaries; validate required executables before publication.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

## Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test tools
just check tools
just links
```


## Compatibility and recovery

Use temporary roots and preserve existing development commands. Preflight does not authorize or execute. Cleanup is limited to artifacts owned by the operation; no ancestry-only or blanket deletion of lanes.

## Handoff

Priority P2; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [[@prd/work/root--improve-tools-preflight.md]] are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
