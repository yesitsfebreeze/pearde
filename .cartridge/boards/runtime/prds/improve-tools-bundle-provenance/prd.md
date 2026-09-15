---
repo: /Users/feb/dev/cartridge/tools.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: improve-tools-bundle-provenance
footprint:
- /Users/feb/dev/cartridge/tools.ctg/src/service.rs
- /Users/feb/dev/cartridge/tools.ctg/.cartridge/tests/unit/service/tests.rs
needs:
- "@runtime/improve-tools-preflight"
---

# Ship bundles with source and dependency provenance

`bundle` writes a provenance record into `dist/cartridge`. `bundle` and `package` in [service.rs](../../../../../../tools.ctg/src/service.rs) already stage into a temporary folder, refuse a missing Rust binary before publishing (`packaging_refuses_missing_rust_binaries_but_accepts_lua_only`) and rename into place. They record nothing about what was built. The old `scripts/workspace.py` and `repositories.json` inputs no longer exist.

Record `PROVENANCE.json` inside the staged bundle before the rename. It holds, per repository under the composition root (submodules included), the commit and a SHA-256 of `git diff HEAD` when dirty; the SHA-256 of every copied executable; digests of each `Cargo.lock`/`bun.lock` used; the build profile; and the `rustc`, `cargo` and `bun` versions. This is metadata only and does not claim reproducible binary bytes.

## Acceptance

- [ ] Two bundles of an unchanged fixture produce byte-identical `PROVENANCE.json` (the record has no timestamp).
- [ ] Changing a copied executable, a lockfile or a tracked source file (dirty) changes exactly the corresponding digest.
- [ ] The record contains no environment values, `config.lua` contents, credentials or `.cartridge` store paths. A failing version probe fails the bundle before the rename and keeps the previous `dist/cartridge`.

## Proof and recovery

First extend `package_preserves_entries_binaries_and_notices` in [tests.rs](../../../../../../tools.ctg/.cartridge/tests/unit/service/tests.rs) with a git fixture. Gates, cwd `/Users/feb/dev/cartridge`: `just test tools`, `just check tools`. Not run. Rollback: stop writing the file. Bundles stay loadable without it.

## Dependencies and review

No hard prerequisites. Same file as `improve-tools-preflight`, so coordinate landing. Board placement under @runtime is historical. [Review](review.md): inherits 2 rounds.

## From the retired work memo

Folded 2026-09-15 from `work/improve-tools-bundle-provenance.md` (status open). The PRD state above is authoritative.

### Outcome

A generated bundle identifies exact repository revisions, dirty state, executable checksums and dependency inventory.

### Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
Related existing work (context/coordination, not automatically a hard dependency): [lane-rm-refuses-after-the-gates-run](../../../root/prds/lane-rm-refuses-after-the-gates-run/prd.md), [lanes-do-not-poison-each-others-builds](../../../root/prds/lanes-do-not-poison-each-others-builds/prd.md).

### Footprint

Workspace tools; one observable outcome. The listed files are starting points and a proposed edit footprint, not permission to make unrelated changes.
All paths below are relative to /Users/feb/dev/cartridge.

- `tools.ctg/service.rs`
- `tools.ctg/tests/test_lane.py`
- `cartridge.ctg/scripts/workspace.py`
- `cartridge.ctg/repositories.json`

Tests/fixtures and owner-local documentation for this outcome may be added beside
these sources. Recheck active claims before changing shared files. Update cartridge.json
only when public services, schema, configuration or verification commands actually change.

### Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] Two bundles from unchanged fixtures produce identical provenance metadata; a changed executable/revision changes the appropriate entries.
- [ ] Missing required binaries fail packaging; no provider credentials or live state are included.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Extend existing bundling with a deterministic machine-readable manifest excluding credentials and private stores. Distinguish reproducible metadata from a claim of reproducible binaries; validate required executables before publication.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

### Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test tools
just check tools
just links
```


### Compatibility and recovery

Use temporary roots and preserve existing development commands. Preflight does not authorize or execute. Cleanup is limited to artifacts owned by the operation; no ancestry-only or blanket deletion of lanes.

### Handoff

Priority P2; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [improve-tools-preflight](../improve-tools-preflight/prd.md) are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
