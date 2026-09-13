---
state: open
origin: requested
priority: 82
blast-radius: high
workflow: develop-one-cartridge
needs:
  - @runtime/one-runner-executes-documents
footprint:
  - /Users/feb/dev/cartridge/cartridge.ctg/src/process.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/reload.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/stream.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/tests/lifecycle.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/tests/reload.rs
  - /Users/feb/dev/cartridge/pty.ctg/tests/process.rs
---

# Sidecars, event tools, and reload have explicit lifetimes

Justdown sidecars and the accepted event-typed tool direction require owned processes and subscriptions, not detached jobs that survive their cartridge by accident.

## Ownership and scope

Owner: `runtime`. Participating repositories: `cartridge.ctg`, `pty.ctg`, `memo.ctg`. Coordinate from the root master board. Footprints are preliminary checkout-absolute paths so Pearde can detect cross-board overlaps; narrow and rebase them during analysis before claiming in another checkout.

## Implementation plan

1. Extend the shared executor with sidecar readiness, health, stop, and exit reporting. Use the runtime's ownership tree and existing channels.
2. Specify event-triggered tools as a separate extension from justdown invocation mode: exact event type, activation, bounded queue, duplicate handling, and cancellation.
3. Bind a running invocation/subscription to its original document revision. New invocations use the new revision; changing a file alone does not duplicate sidecars or subscriptions.
4. Probe exclusive listeners and memory writers through prepare/reject/dispose, and document when a runtime host restart is required.

## Acceptance contract

- A sidecar becomes ready only after the real endpoint is usable; early exit and readiness timeout are visible failures.
- Disabling the owner terminates only its descendants/subscriptions, leaving sibling processes and PTY intact.
- One event produces the documented number of invocations across reconnect/reload; overflow is bounded and reported rather than silently lost.
- A rejected candidate retains the old service; no duplicate listener, writer, or subscription survives a successful replacement.
- Read/discovery of an event-tool document never activates it.

## Verification to turn into specs

Run from the composed repository root. These are proposed gates, not results. The analyst must probe commands and write executable `specs/specNN.md` gates with source revisions and expected outcomes before implementation.

```sh
just test runtime reload
just test runtime lifecycle
just test runtime stream
just test pty
```

## Failure and recovery

A reload duplicates an event consumer or reports READY before binding. Drive real processes and count subscriptions/endpoints.

Rollback: Disable the new lifecycle modes independently of one-shot recipes. Drain owned work before removing a feature; never kill unrelated processes.

## Prior context

Related existing runtime memo leaf names: `a-tool-is-declared-by-its-memo`. Resolve them under `cartridge.ctg/.cartridge/memos/` and inspect older `.pearde` work before changing scope; link superseded work explicitly. This PRD is the authoritative state for this new slice, not a copy of an older ticket.

## Evidence

No implementation evidence yet. The assessment provides the baseline. All new PRDs begin `open`; Pearde transition commands govern later states. Do not manufacture specifications, approvals, timings, claims, or passing results.
