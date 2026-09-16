---
state: open
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge/mcp.ctg"
capability-owner: mcp
work-kind: leaf
---

# The mcp owner gate is green: the live catalog tests settle

## Outcome

At mcp.ctg `6f06acd`, `just test mcp` from `/Users/feb/dev/cartridge` exits 1: 11 tests
pass and 2 live-fixture tests fail,
`initialized_live_client_inspects_real_policy_without_granting_writes` and
`initialized_live_client_observes_catalog_replacements`, both with "Live catalog did not
settle: starting the host for .cartridge". Find out whether the fixture, the host start
or the catalog wait is wrong, and fix it at the root, so the owner gate is green again
and future mcp specs can name `just test mcp` instead of a narrower stand-in.

## Acceptance

- [ ] The failing cause is named with evidence (command, cwd, exit code, the relevant log line) in the spec.
- [ ] `just test mcp` from `/Users/feb/dev/cartridge` exits 0 on two consecutive runs.
- [ ] `just check mcp` exits 0.
- [ ] Neither test is deleted or ignored to get there.

## Proof and recovery

Observed by the analyst of `@mcp/deferred-tool-band`, 2026-09-16
(`.state/loop/deferred-tool-band/analyst-1.md`).
