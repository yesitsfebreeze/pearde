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
estimate: "4h"
---

# A live daemon exposes bounded startup progress or a terminal failure instead of remaining indefinitely invisible before listening

## Do

A daemon that has started reaches a usable endpoint or exposes a bounded,
phase-specific failure. Sessions can distinguish startup progress from a dead
service without spawning duplicate owners of the same store. Existing readiness,
listener inheritance, graceful handover, and store ownership remain authoritative.

On 2026-09-09 a foreground daemon process for this repository had no observed Unix
listener and the conventional endpoint returned ENOENT. Model connection,
predecessor handling, and bootstrap precede listener acquisition in the inspected
implementation, but the blocked phase and a causal relationship to reload were
not established. The work includes identifying that phase before choosing a
repair; process existence alone is neither readiness nor proof of a hang.

[memory-integration-fast-readiness](../memory-integration-fast-readiness/prd.md), [the-daemon-comes-back-after-the-watchdog](../the-daemon-comes-back-after-the-watchdog/prd.md),
and [mcp-attachment-recovers-without-replaying-work](../mcp-attachment-recovers-without-replaying-work/prd.md) already own adjacent
contracts and must not be replaced by another supervision system.
