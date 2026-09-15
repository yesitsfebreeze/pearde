---
kind: work
description: "Simplify terminal dependencies and make the runtime reproducibly verifiable"
status: open
level: 9
subwork:
  - "[context-date-needs-no-clock-cartridge](../../prds/context-date-needs-no-clock-cartridge/prd.md)"
  - "[terminal-profile-starts-only-needed-services](../../prds/terminal-profile-starts-only-needed-services/prd.md)"
  - "[rpc-contracts-run-across-rust-lua-and-bun](../../prds/rpc-contracts-run-across-rust-lua-and-bun/prd.md)"
  - "[fresh-checkouts-can-run-the-gates](../../prds/fresh-checkouts-can-run-the-gates/prd.md)"
  - "[ci-proves-the-supported-terminal-matrix](../../../runtime/prds/ci-proves-the-supported-terminal-matrix/prd.md)"
  - "[the-agent-can-discover-its-own-program](../../prds/the-agent-can-discover-its-own-program/prd.md)"
  - "[debug-mode-correlates-a-terminal-turn](../../../agent/prds/debug-mode-correlates-a-terminal-turn/prd.md)"
  - "[the-agent-can-extend-and-verify-a-cartridge](../../prds/the-agent-can-extend-and-verify-a-cartridge/prd.md)"
  - "[rolling-context-retains-decision-evidence](../../prds/rolling-context-retains-decision-evidence/prd.md)"
  - "[the-live-record-matches-the-terminal-contract](../../prds/the-live-record-matches-the-terminal-contract/prd.md)"
  - "[cartridges-prove-themselves-at-registration](../../prds/cartridges-prove-themselves-at-registration/prd.md)"
  - "[lanes-do-not-poison-each-others-builds](../../prds/lanes-do-not-poison-each-others-builds/prd.md)"
  - "[the-reload-test-is-not-flaky](../../../runtime/prds/the-reload-test-is-not-flaky/prd.md)"
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
| P2 | [context-date-needs-no-clock-cartridge](../../prds/context-date-needs-no-clock-cartridge/prd.md) | 4h |
| P1 | [terminal-profile-starts-only-needed-services](../../prds/terminal-profile-starts-only-needed-services/prd.md) | 1d |
| P1 | [rpc-contracts-run-across-rust-lua-and-bun](../../prds/rpc-contracts-run-across-rust-lua-and-bun/prd.md) | 2d |
| P1 | [fresh-checkouts-can-run-the-gates](../../prds/fresh-checkouts-can-run-the-gates/prd.md) | 1d |
| P1 | [ci-proves-the-supported-terminal-matrix](../../../runtime/prds/ci-proves-the-supported-terminal-matrix/prd.md) | 2d |
| P1 | [the-agent-can-discover-its-own-program](../../prds/the-agent-can-discover-its-own-program/prd.md) | 1d |
| P1 | [debug-mode-correlates-a-terminal-turn](../../../agent/prds/debug-mode-correlates-a-terminal-turn/prd.md) | 2d |
| P1 | [the-agent-can-extend-and-verify-a-cartridge](../../prds/the-agent-can-extend-and-verify-a-cartridge/prd.md) | 2d |
| P1 | [rolling-context-retains-decision-evidence](../../prds/rolling-context-retains-decision-evidence/prd.md) | 1d |
| P2 | [the-live-record-matches-the-terminal-contract](../../prds/the-live-record-matches-the-terminal-contract/prd.md) | 1d |
| P1 | [cartridges-prove-themselves-at-registration](../../prds/cartridges-prove-themselves-at-registration/prd.md) | 2d |

Clarification: [[the-agent-can-diagnose-and-extend-its-runtime]] makes program discovery → debugging →
extension a testable agent workflow, with diagnostics as supporting evidence.

## Check

- [ ] Every child has its acceptance evidence and is done.
- [ ] The audit is updated with the resulting dependency graph, gate results,
      debug invocation and remaining explicit limits.
