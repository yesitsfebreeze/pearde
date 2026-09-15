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
needs:
- "@memory/extension-services-provide-and-inject"
- "@memory/extension-events-four-dispatch-modes"
estimate: "1d"
---

# the daemon boots a root `Context`, its subsystems become plugins providing services, its cross-crate signals become events, and `[[plugin]]` rows in memory.toml mount through the loader

## Do

Deliver [[memory-is-a-plugin-tree]] as the children below, in order:

subwork: [memory-daemon-boots-a-root-context](../memory-daemon-boots-a-root-context/prd.md) [a-plugins-ingests-unwind-with-it](../../../runtime/prds/a-plugins-ingests-unwind-with-it/prd.md) [memory-signals-become-events](../memory-signals-become-events/prd.md) [plugins-from-memory-toml](../../../runtime/prds/plugins-from-memory-toml/prd.md) [disk-adapters-detach-without-forgetting-memory](../../../runtime/prds/disk-adapters-detach-without-forgetting-memory/prd.md)

The plugins that wrap memory's crates live in `commands` (a composing crate
above the layered set); `extension` itself imports nothing of memory.

## Acceptance
Every child is done. `just test` is green, and `memory plugins` on the
project daemon prints the built-in fibers `Active` with the rows of its
`memory.toml` under the loader.
