---
repo: /Users/feb/dev/cartridge/memory.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "1d"
---

# the `extension` crate — Cordis's context, fiber, effects, services, events, config, loader, scope and inspector in Rust at L0, each a child memo with its own tests

## Do

Build `src/extension` (package `extension`, `//! Layer: L0 · No Memory imports.`,
workspace dependencies only: `tokio`, `parking_lot`, `serde`, `serde_json`,
`thiserror`, `tracing`) as the children below, in this order, each landing
on its own:

subwork: [extension-context-and-fiber](../extension-context-and-fiber/prd.md) [extension-services-provide-and-inject](../extension-services-provide-and-inject/prd.md) [extension-events-four-dispatch-modes](../extension-events-four-dispatch-modes/prd.md) [extension-plugin-config-and-update](../extension-plugin-config-and-update/prd.md) [extension-loader-plugin-tree](../../../runtime/prds/extension-loader-plugin-tree/prd.md) [extension-scope-per-agent-registrations](../extension-scope-per-agent-registrations/prd.md) [extension-inspect](../../../runtime/prds/extension-inspect/prd.md)

The crate's public surface is the Table 2 column of
[[composition-is-a-pillar-of-memory]]; a name not in that table is not added
without a child memo naming it. Nothing in the crate awaits plugin code while
holding a lock: fiber and store state live behind `parking_lot` locks held
for a field read or write, and every `await` on a plugin's future happens
with no lock held ([[rust-harness-foundation]]).

## Acceptance
Every child is done. `cargo nextest run -p extension` is green,
`cargo test --test layer_headers` accepts the crate at L0, and the crate's
`lib.rs` doc comment lists the Table 2 names it exports.
