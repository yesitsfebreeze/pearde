---
complexity: small
footprint:
  - scope.ctg
  - .cartridge/init.lua
---

# Accurate, independent stats

## Acceptance

- [x] Four regression tests and both existing model self-checks pass.
- [x] Scope is enabled and its live status agrees with the host.

## Steps

Count disabled cartridges separately from enabled ones and preserve active-generation errors. Count ASP schemes and events from their declared collections. Poll host, ledger and ASP in separate workers. Bound the message queue to 5000 entries with shutdown-aware backpressure. Preserve the terminal screen and update both help and README.

## Verify and Proof

```sh
python3 scope.ctg/src/test_health.py
python3 scope.ctg/src/state.py
python3 scope.ctg/src/tree.py
just audit scope
just isolation
```

## Independent verification

The independent verifier ran all four regression tests, both model self-checks and a live five-second observation on 2026-09-19. Direct calls and pane %45 agreed: all 20 components active, eight ASP schemes, 68 events, no clashes. Earlier versions failed the disabled-health, scheme-count and slow-ledger regression tests.
