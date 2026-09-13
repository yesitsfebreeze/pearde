---
state: open
origin: requested
priority: 70
blast-radius: high
workflow: develop-one-cartridge
needs:
  - @memo/memo-board-template
  - @harness/harness-consumes-landscape
  - @mcp/clients-share-document-execution
  - capabilities-live-with-their-owners
  - @runtime/documents-own-live-processes
  - @ui/human-context-is-the-same-document
  - @tools/development-tooling-has-one-home
  - @landscape/context-quality-is-measured
  - @landscape/recursive-development-graph
footprint:
  - /Users/feb/dev/cartridge/.cartridge
  - /Users/feb/dev/cartridge/CARTRIDGE-ASSESSMENT.md
  - /Users/feb/dev/cartridge/.gitmodules
  - /Users/feb/dev/cartridge/cartridge.ctg/repositories.json
  - /Users/feb/dev/cartridge/cartridge.ctg/docs/llms
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge
  - /Users/feb/dev/cartridge/memo.ctg/README.md
  - /Users/feb/dev/cartridge/memory.ctg/CARTRIDGE.md
---

# The composed system passes the complete workflow and retires redundant wrappers

Completion means a clean composed checkout performs the intended work, not a collection of individually green PRs.

## Ownership and scope

Owner: `cartridge-system`. Participating repositories: `root`, `cartridge.ctg`, `all-cartridges`. Coordinate from the root master board. Footprints are preliminary checkout-absolute paths so Pearde can detect cross-board overlaps; narrow and rebase them during analysis before claiming in another checkout.

## Implementation plan

1. Walk the release scenario: initialize board, select work, retrieve context, read one document, execute, inspect, record evidence, edit/reload, and retrieve the improvement from a later session.
2. Run default, MCP, proxy, and source-absent/bundled profiles with local provider fixtures and exact exposure snapshots.
3. Retire wrappers and duplicated authored definitions only after replacement tests pass. Update catalogs, source links, development recipes, ownership/reload docs, and the root submodule pointers coherently.
4. Review every PRD's evidence and remaining limitations. A board transition to done requires observed gates and landed owner commits; plans and templates alone do not prove implementation.

## Acceptance contract

- A fresh checkout completes the full scenario without manual JSON tool envelopes or per-tool client code edits.
- All enabled capabilities have discoverable owner documents and real success/failure probes; all 17 assessed repositories have a recorded disposition.
- No accidental capability expansion occurs in default/MCP/proxy, and corrupt stores/failed reloads preserve previous usable state.
- Changed-repository gates plus the composed build/check/test/smoke gates pass; any environmental skip is named with its unresolved coverage.
- Root board, templates, docs, and evidence agree; no task is marked done solely because its document exists.

## Verification to turn into specs

Run from the composed repository root. These are proposed gates, not results. The analyst must probe commands and write executable `specs/specNN.md` gates with source revisions and expected outcomes before implementation.

```sh
just board-check
just links
just build
just check
just test
just smoke
```

## Failure and recovery

Repository pointers land before their owner commits, leaving a checkout nobody else can build. Verify from the pinned composed checkout.

Rollback: Keep a known-good set of submodule commits/profile configurations and switch code/config together. Preserve all durable stores and records; do not use history rewrites for rollback.

## Prior context

Related existing runtime memo leaf names: `the-agent-can-extend-and-verify-a-cartridge`. Resolve them under `cartridge.ctg/.cartridge/memos/` and inspect older `.pearde` work before changing scope; link superseded work explicitly. This PRD is the authoritative state for this new slice, not a copy of an older ticket.

## Evidence

No implementation evidence yet. The assessment provides the baseline. All new PRDs begin `open`; Pearde transition commands govern later states. Do not manufacture specifications, approvals, timings, claims, or passing results.
