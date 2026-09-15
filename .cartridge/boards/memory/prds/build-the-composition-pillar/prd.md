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
---

# deliver the core extension runtime and daemon lifecycle

## Do

Deliver the core extension contracts in [[composition-is-a-pillar-of-memory]]
and the daemon lifecycle in [[memory-is-a-plugin-tree]]. Required proxy and memory
components may use the extension machinery without becoming optional features.

subwork: [the-extension-crate](../the-extension-crate/prd.md) [memory-boots-as-a-plugin-tree](../memory-boots-as-a-plugin-tree/prd.md)

## Acceptance
Every retained child passes its own checks. The daemon owns required core
startup and shutdown, publishes readiness only for available services, and
unwinds failed extension installation without leaking tasks or registrations.
The existing core proxy and memory path works without a native agent loop or
bundled client. Loader and inspection checks belong to their own retained work.
