---
kind: work
level: 7
status: open
description: deliver the core extension runtime and daemon lifecycle
read_when: "planning or executing the composition pillar, or asking what the pillar workload is"
---

# build-the-composition-pillar

## Do

Deliver the core extension contracts in [[composition-is-a-pillar-of-memory]]
and the daemon lifecycle in [[memory-is-a-plugin-tree]]. Required proxy and memory
components may use the extension machinery without becoming optional features.

subwork: [[@prd/work/memory--the-extension-crate.md]] [[@prd/work/memory--memory-boots-as-a-plugin-tree.md]]

## Check

Every retained child passes its own checks. The daemon owns required core
startup and shutdown, publishes readiness only for available services, and
unwinds failed extension installation without leaking tasks or registrations.
The existing core proxy and memory path works without a native agent loop or
bundled client. Loader and inspection checks belong to their own retained work.
