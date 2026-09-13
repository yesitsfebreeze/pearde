---
kind: work
description: "Simplify terminal dependencies and make the runtime reproducibly verifiable"
status: open
level: 9
subwork:
  - "[[@prd/work/root--context-date-needs-no-clock-cartridge.md]]"
  - "[[@prd/work/root--terminal-profile-starts-only-needed-services.md]]"
  - "[[@prd/work/root--rpc-contracts-run-across-rust-lua-and-bun.md]]"
  - "[[@prd/work/root--fresh-checkouts-can-run-the-gates.md]]"
  - "[[@prd/work/root--ci-proves-the-supported-terminal-matrix.md]]"
  - "[[@prd/work/root--the-agent-can-discover-its-own-program.md]]"
  - "[[@prd/work/root--debug-mode-correlates-a-terminal-turn.md]]"
  - "[[@prd/work/root--the-agent-can-extend-and-verify-a-cartridge.md]]"
  - "[[@prd/work/root--rolling-context-retains-decision-evidence.md]]"
  - "[[@prd/work/root--the-live-record-matches-the-terminal-contract.md]]"
  - "[[@prd/work/root--cartridges-prove-themselves-at-registration.md]]"
  - "[[@prd/work/root--lanes-do-not-poison-each-others-builds.md]]"
  - "[[@prd/work/root--the-reload-test-is-not-flaky.md]]"
---

# A small, provable terminal runtime

## Outcome

The terminal-native agent has only justified runtime dependencies, a compact
current design record, and reproducible evidence for language boundaries,
agent-driven debugging, cartridge self-extension and context quality. This is the bounded improvement set from
[[runtime-audit-2026-09-12]], not an open-ended rewrite of the core.

P1 is the first implementation group; P2 is follow-up cleanup. Dependencies in
`needs` define ordering; the rows are otherwise independently actionable.

| Priority | Work | Estimate |
| --- | --- | --- |
| P2 | [[@prd/work/root--context-date-needs-no-clock-cartridge.md]] | 4h |
| P1 | [[@prd/work/root--terminal-profile-starts-only-needed-services.md]] | 1d |
| P1 | [[@prd/work/root--rpc-contracts-run-across-rust-lua-and-bun.md]] | 2d |
| P1 | [[@prd/work/root--fresh-checkouts-can-run-the-gates.md]] | 1d |
| P1 | [[@prd/work/root--ci-proves-the-supported-terminal-matrix.md]] | 2d |
| P1 | [[@prd/work/root--the-agent-can-discover-its-own-program.md]] | 1d |
| P1 | [[@prd/work/root--debug-mode-correlates-a-terminal-turn.md]] | 2d |
| P1 | [[@prd/work/root--the-agent-can-extend-and-verify-a-cartridge.md]] | 2d |
| P1 | [[@prd/work/root--rolling-context-retains-decision-evidence.md]] | 1d |
| P2 | [[@prd/work/root--the-live-record-matches-the-terminal-contract.md]] | 1d |
| P1 | [[@prd/work/root--cartridges-prove-themselves-at-registration.md]] | 2d |

Clarification: [[the-agent-can-diagnose-and-extend-its-runtime]] makes program discovery → debugging →
extension a testable agent workflow, with diagnostics as supporting evidence.

## Check

- [ ] Every child has its acceptance evidence and is done.
- [ ] The audit is updated with the resulting dependency graph, gate results,
      debug invocation and remaining explicit limits.
