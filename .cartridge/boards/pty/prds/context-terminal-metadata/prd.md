---
repo: /Users/feb/dev/cartridge/pty.ctg
state: deferred
deferred-from: specced
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: pty
work-kind: leaf
review-round: 3
review-status: "passed"
canonical-scope: context-terminal-metadata
needs:
- "@pty/improve-pty-shell-identity"
footprint: ["Cargo.toml","src/main.rs","src/context.rs",".cartridge/tests/unit/context/tests.rs",".cartridge/tests/integration/process.rs",".cartridge/docs/context.md"]
---

# Offer terminal lifecycle metadata without screen or command output

One owner-local part of the existing Landscape file/kernel/live context contract. Preserve the historical source scope and two inherited review rounds. This leaf owns its named native or library boundary; other owners remain prerequisites rather than copied implementations.

## Acceptance

- [ ] An already active terminal exposes a bounded readonly shell identity/lifecycle/control-state observation with stable revision.
- [ ] Metadata reads never start a terminal, alter input ownership, advance a screen cursor or return command/output/screen/title payloads.
- [ ] Exit, unavailable or replaced shell is explicit; public owner and native fixtures retain current terminal behavior.

## Proof and recovery

Measure the actual current owner behavior before specs. Independently review the concrete source footprint, authority and failure contract before implementation. Public owner tests/check and native integration must demonstrate the claimed readonly behavior. Preserve source records and existing APIs on failure; no automatic retries or activation.

## Review

Inherits rounds 1–2 from @landscape/landscape-composes-system-context/live-file-context-contributors; maximum five rounds. This split does not claim a new passing implementation review. The preserved original requires file/kernel evidence and separately owned live metadata.
