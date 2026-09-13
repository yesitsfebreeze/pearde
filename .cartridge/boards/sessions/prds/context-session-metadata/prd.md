---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: sessions
work-kind: leaf
review-round: 3
review-status: "passed"
canonical-scope: context-session-metadata
needs:
- "@sessions/sub-agent-sessions-record-parent-and-mailbox"
footprint: ["src/main.rs","src/context.rs","src/mailbox.rs","src/roster.rs",".cartridge/tests/unit/main/context_tests.rs",".cartridge/tests/unit/main/roster_tests.rs",".cartridge/tests/integration/context.test.ts",".cartridge/docs/context.md","Cargo.toml"]
commit: "92240c6ba415f53b2d17971aea185536a6f517bc"
---

# Offer scoped session metadata without transcript or agent payload

One owner-local part of the existing Landscape file/kernel/live context contract. Preserve the historical source scope and two inherited review rounds. This leaf owns its named native or library boundary; other owners remain prerequisites rather than copied implementations.

## Acceptance

- [x] A trusted session-scoped readonly metadata operation returns stable session/parent/revision/lifecycle identifiers and excludes transcript, mailbox body, agent payload, names/prompts and file lists.
- [x] Unknown or out-of-scope session and inactive source produce explicit bounded absence; reads do not advance cursors or update session state.
- [x] Owner tests and actual native fixtures prove revision changes, strict field allowlists and existing session behavior.

## Proof and recovery

Measure the actual current owner behavior before specs. Independently review the concrete source footprint, authority and failure contract before implementation. Public owner tests/check and native integration must demonstrate the claimed readonly behavior. Preserve source records and existing APIs on failure; no automatic retries or activation.

## Review

Inherits rounds 1–2 from @landscape/landscape-composes-system-context/live-file-context-contributors; maximum five rounds. This split does not claim a new passing implementation review. The preserved original requires file/kernel evidence and separately owned live metadata.
