---
state: "done"
origin: requested
priority: 95
repo: "/Users/feb/dev/cartridge"
work-kind: leaf
footprint:
  - scope.ctg
  - .cartridge/init.lua
commit: "7809fc14bef0472938eeddab2285384bf78418e8"
---

# scope reports accurate health without serial polling stalls

## Outcome

The recovered stats pane accurately describes enabled host components, surfaces reload errors, counts ASP schemes and events, and polls each health source independently. Its queue stays bounded while paused. The scope cartridge is declared in the composition and includes its own help and tests.

## Acceptance

- [x] Disabled entries do not produce a failed host, and reload errors remain visible.
- [x] ASP displays declared scheme and event counts.
- [x] A delayed ledger does not block host or ASP polling.
- [x] A full queue waits for space and shutdown releases its producer.
- [x] The live pane matches direct host and ASP responses, and owner audit and isolation pass.
