---
kind: work
level: 10
status: open
claim: b424ceba 2026-09-09 15:55
estimate: 4h
description: A live daemon exposes bounded startup progress or a terminal failure instead of remaining indefinitely invisible before listening
read_when: a daemon process exists but agent connections cannot reach its endpoint
---

# daemon-startup-cannot-remain-silently-unreachable

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

[[@prd/work/memory--memory-integration-fast-readiness.md]], [[@prd/work/memory--the-daemon-comes-back-after-the-watchdog.md]],
and [[@prd/work/memory--mcp-attachment-recovers-without-replaying-work.md]] already own adjacent
contracts and must not be replaced by another supervision system.
