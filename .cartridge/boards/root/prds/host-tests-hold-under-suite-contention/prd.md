---
state: open
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge"
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
wave: 2
date: "2026-09-15"
footprint:
- "cartridge.ctg"
needs:
- the-profile-is-the-orchestration-service
- the-gates-run-from-the-root-justfile
---

# Host tests hold under suite contention

## Outcome

The host's own check and test gates are green when the whole suite runs at once.

## Acceptance

- [ ] `just check cartridge` exits 0 (2026-09-15: rustfmt diff in `.cartridge/tests/unit/src/host/socket.rs`).
- [ ] `just test cartridge` exits 0 on three consecutive runs with the suite in parallel; `$CARTRIDGE_HOME` is set per test, never process-global; the `cli::setup` and `cli::trust` tests pass on macOS CI.

## Folds

Deferred with `superseded-by` pointing here:

- @root/unit-process-tests-time-out-and-redden-under-suite-contention-after-the-settings-refactor-raised-startup-timeout-to-60s
- root memo `prd/the-binary-target-passes-on-a-runner`

## Result

Not started.
