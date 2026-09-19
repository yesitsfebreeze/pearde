---
state: "analyzing"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
claim: "coordinator-codex-17 2026-09-19T19:17:27.265Z"
---

# ASP composes extensible events and the unified calendar-compacted trace

## Outcome

Cartridges extend the running system through declared events, ASP types and tree entry points, and Lua handlers. ASP exposes the composition and its unified trace. The trace records exchanges and runtime activity in the existing durable compaction engine, which rolls closed UTC days into weeks, months and years. The name trace replaces the former activity ledger surface. Existing persisted history remains readable.

## Acceptance

- [x] A Lua cartridge adds a validated ASP type and tree root without host-specific code, and unloading removes its live declarations.
- [x] Declared events are discoverable ASP entities with their schemas and owners.
- [x] Runtime events and exchanges reach one trace store, whose raw records and compacted tiers expand and search through ASP.
- [x] Failed compaction preserves its inputs, retries are safe, and calendar boundaries remain covered by deterministic tests.
- [x] Scope observes trace tiers and compaction cycles through ASP.
- [ ] Relevant tests, cartridge audits and isolation checks pass.

## Verification — 2026-09-19

Implemented and checked in the working tree; not collected or committed. Lua integration proves schema validation, contributed roots, declared event discovery and event activity delivery. Host suite: 213 passed; final ASP-focused run after adding the host cartridge node: 17 passed. Memory RPC: 112 passed; store: 77; memory cartridge: 27; transport owner filters: 19. Proxy: 65 passed. Scope: 24 passed. Cartridge audits for memory, proxy and scope pass hard checks.

Live verification after refreshing host and native modules: asp:root, 70 event declarations, existing trace history (12367 records at the probe), bounded tier previews, exact event and cartridge edges, and a newly generated memo event all resolve. Existing cycle snapshots resolve through ASP.

The earlier composition isolation passed for 20 cartridges. The final rerun is blocked by a concurrent memo-run recipe edit: expected exactly one closed just block. Strict proxy clippy encounters the pre-existing result_large_err warning; it passes with that lint excepted. The Lua integration test also unloads the worker and verifies its event, type and tree root disappear while the trace root remains; that test passes after the final change.

Delivery queues hold 1024 pending records and report overflow. Pending delivery is process-local; persisted records and compaction are transactional. Existing ledger-named database and mirror keys are retained solely for stored-history compatibility.
