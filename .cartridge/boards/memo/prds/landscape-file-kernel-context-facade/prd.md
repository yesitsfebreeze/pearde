---
repo: /Users/feb/dev/cartridge/memo.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memo
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: landscape-file-kernel-context-facade
needs:
- "@landscape/landscape-composes-system-context/live-file-context-contributors/file-kernel-evidence-adapter"
- "@memo/landscape-context-facade"
- "@fs/read-only-context-file-snapshots"
commit: "1ffca32db1d06364b3e35e6cbca4881a1f814f71"
---

# Expose configured file and kernel evidence through native shared context

One owner-local part of the existing Landscape file/kernel/live context contract. Preserve the historical source scope and two inherited review rounds. This leaf owns its named native or library boundary; other owners remain prerequisites rather than copied implementations.

## Acceptance

- [x] A real native composition returns configured file bodies and kernel capability evidence in the same existing Prepared snapshot alongside enabled documents/memory.
- [x] Exact readback detects source edits, removals, owner/config changes and generation changes without requery or substitution; existing context and inventory contracts remain unchanged.
- [x] Optional grants and inactive providers produce named absence/disabled states without activation, source writes, observations or inferred permissions.

## Proof and recovery

Measure the actual current owner behavior before specs. Independently review the concrete source footprint, authority and failure contract before implementation. Public owner tests/check and native integration must demonstrate the claimed readonly behavior. Preserve source records and existing APIs on failure; no automatic retries or activation.

## Review

Inherits rounds 1–2 from @landscape/landscape-composes-system-context/live-file-context-contributors; maximum five rounds. This split does not claim a new passing implementation review. The preserved original requires file/kernel evidence and separately owned live metadata.
