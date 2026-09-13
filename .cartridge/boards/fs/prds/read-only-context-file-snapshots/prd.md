---
repo: /Users/feb/dev/cartridge/fs.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: fs
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: read-only-context-file-snapshots
commit: "de1406682a33c5b12cb472787178e2570e5ed0f8"
---

# Read exact bounded file context without tool observations

One owner-local part of the existing Landscape file/kernel/live context contract. Preserve the historical source scope and two inherited review rounds. This leaf owns its named native or library boundary; other owners remain prerequisites rather than copied implementations.

## Acceptance

- [x] A native readonly operation returns full selected UTF-8 bytes and their exact SHA256, preserving CRLF and trailing newline, with no tool observation or session touch.
- [x] Expected revision mismatch, missing/nonregular/symlink/escaping/oversized source, malformed input and deadline return bounded explicit outcomes before any mutation.
- [x] Actual SDK and public FS gates prove the new operation and preserve existing model read/write/search contracts.

## Proof and recovery

Measure the actual current owner behavior before specs. Independently review the concrete source footprint, authority and failure contract before implementation. Public owner tests/check and native integration must demonstrate the claimed readonly behavior. Preserve source records and existing APIs on failure; no automatic retries or activation.

## Review

Inherits rounds 1–2 from @landscape/landscape-composes-system-context/live-file-context-contributors; maximum five rounds. This split does not claim a new passing implementation review. The preserved original requires file/kernel evidence and separately owned live metadata.
