---
state: open
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/harness.ctg"
footprint: ["src/roster.rs","cartridge.json",".cartridge/tests/unit/roster_tests.rs",".cartridge/tests/integration/roster.test.ts",".cartridge/docs/roster.md"]
needs: ["@harness/roster-without-context-evidence-contract"]
---

# The default roster row limit is accepted by Sessions

## Outcome

Enabling the host-bound roster with actor and credential configuration, without
an explicit row limit, renders the authorized Sessions roster. Harness's
default request must satisfy the existing Sessions contract. This is a separate
compatibility repair after the roster-specific capture cleanup; disabled roster
behavior and Sessions privacy boundaries stay intact.

## Acceptance

- [ ] A real Sessions+Harness fixture enables roster without max_rows and renders authorized rows rather than reporting an invalid-limit source failure.
- [ ] Harness's default, manifest schema and documentation agree with the Sessions request limit of 1 through 100; explicit supported limits still bound selected rows.
- [ ] Disabled roster makes no call, and unsupported configured limits have an explicit tested failure at the appropriate boundary without leaking credentials.

## Evidence and proof

Observed 2026-09-19 at Harness c8305341bb30b058c481bf023ebf977304248dab:
src/roster.rs rows() returns 200 and capture sends config.max_rows unchanged.
Sessions 499191501e7e3cbb1ac1537ea75a5f1906f97f21 src/roster.rs:119 accepts
limit only from 1 through 100. Source inspection proves the incompatible values;
the analyst did not execute a default-enabled real-composition reproduction.
Reproduce that failure before choosing the smallest compatible default/schema
repair. Run the named regression against actual modules, owner unit/integration
gates, audit and isolation. Do not expand Sessions limits or redesign roster
caps without reviewing that separate contract change. Rollback touches only
Harness configuration, validation, tests and documentation, never stored data.
