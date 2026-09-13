---
state: open
origin: requested
priority: 76
blast-radius: high
workflow: develop-one-cartridge
needs:
  - @memory/memory-owns-its-tool
  - @memo/one-document-serves-every-reader
footprint:
  - /Users/feb/dev/cartridge/tools.ctg
  - /Users/feb/dev/cartridge/cartridge.ctg/scripts/workspace.py
  - /Users/feb/dev/cartridge/cartridge.ctg/workspace/Cargo.toml
  - /Users/feb/dev/cartridge/cartridge.ctg/repositories.json
  - /Users/feb/dev/cartridge/cartridge.ctg/justfile
  - /Users/feb/dev/cartridge/cartridge.ctg/builtin/tools
  - /Users/feb/dev/cartridge/.gitmodules
  - /Users/feb/dev/cartridge/justfile
---

# Development commands and verification have one owning implementation

The tools cartridge is runtime-specific development infrastructure, and its separate repository obscures rather than improves independence.

## Ownership and scope

Owner: `tools`. Participating repositories: `tools.ctg`, `cartridge.ctg`, `root`. Coordinate from the root master board. Footprints are preliminary checkout-absolute paths so Pearde can detect cross-board overlaps; narrow and rebase them during analysis before claiming in another checkout.

## Implementation plan

1. Move its implementation into a runtime-owned development package while preserving the tools service/commands during migration. Keep development code out of the runtime hot path.
2. Publish build/check/test/bundle/worktree recipes as owner-local documents. Preserve source ownership when committing submodules before updating root pointers.
3. Make selected-module and clean-checkout builds reproducible with explicit SDK/sibling dependencies. Document logical independence separately from standalone distribution; do not promise independent cloning while path dependencies remain.
4. Wire any currently omitted meaningful Python probes/compaction checks into named gates after inspecting their prerequisites. Version test evidence by source/recipe revisions, not merely a mutable version label.
5. Probe a fresh disposable checkout/bundle and isolated worktree workflow before retiring tools.ctg.

## Acceptance contract

- Existing tools operations and just build/test/check selections still work and unknown modules fail explicitly.
- A fresh checkout initialized with required submodules builds and runs the memory vertical slice with documented dependencies.
- A bundle discovers owner documents and resolves execution cwd without source-tree absolute paths.
- Worktree creation/removal never affects unrelated edits or stores; removed wrapper references disappear from catalog, links, workspace, and submodules.
- Test evidence identifies the actual source and command revision; stale results are visibly stale.

## Verification to turn into specs

Run from the composed repository root. These are proposed gates, not results. The analyst must probe commands and write executable `specs/specNN.md` gates with source revisions and expected outcomes before implementation.

```sh
just test tools
just verify tools
just links
just build
just smoke
```

## Failure and recovery

A local cache hides a missing package/path, or a worktree command acts on the parent repo instead of the owner. Require disposable clean-checkout and ownership fixtures.

Rollback: Keep the old tools entry as a compatibility shim until bundle and fresh-checkout gates pass; move source history rather than deleting it prematurely.

## Prior context

Related existing runtime memo leaf names: `per-cartridge-versioned-test-runner`. Resolve them under `cartridge.ctg/.cartridge/memos/` and inspect older `.pearde` work before changing scope; link superseded work explicitly. This PRD is the authoritative state for this new slice, not a copy of an older ticket.

## Evidence

No implementation evidence yet. The assessment provides the baseline. All new PRDs begin `open`; Pearde transition commands govern later states. Do not manufacture specifications, approvals, timings, claims, or passing results.
