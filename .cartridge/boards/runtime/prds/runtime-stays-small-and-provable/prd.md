---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: rollup
review-round: 3
review-status: failed
canonical-scope: runtime-stays-small-and-provable
---

# A small, provable terminal runtime

Coordinate the linked owner outcomes and record their combined evidence; claim a
leaf for implementation. This parent owns the "provable" half: CI, agent-side
diagnosis and a reliable reload test. The "small" half is the 2026-09-14 quality
audit in [the-runtime-reaches-top-tier-quality](../the-runtime-reaches-top-tier-quality/prd.md),
which also needs the CI leaf. That link is context, not a duplicate task.

## Acceptance

- [ ] Each linked leaf passes its own review and observable acceptance.
- [ ] The reload leaf was delivered before the transport rewrite (939e7d1). Its regression is re-proven on the current `Host::replace`/`reconcile` path at the integrated revision (`just test runtime`, cwd `/Users/feb/dev/cartridge`), or reopened.
- [ ] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [Repository CI runs the gates and reports terminal coverage explicitly](../ci-proves-the-supported-terminal-matrix/prd.md)
- [The agent tests and diagnoses its own runtime](../../../agent/prds/debug-mode-correlates-a-terminal-turn/prd.md)
- [the-reload-test-is-not-flaky](../the-reload-test-is-not-flaky/prd.md)

## Review

[Review history](review.md): round 3/5.

## From the retired work memo

Folded 2026-09-15 from `work/runtime-stays-small-and-provable.md` (status open). The PRD state above is authoritative.

> Simplify terminal dependencies and make the runtime reproducibly verifiable

### Outcome

The terminal-native agent has only justified runtime dependencies, a compact
current design record, and reproducible evidence for language boundaries,
agent-driven debugging, cartridge self-extension and context quality. This is the bounded improvement set from
[[runtime-audit-2026-09-12]], not an open-ended rewrite of the core.

P1 is the first implementation group; P2 is follow-up cleanup. Dependencies in
`needs` define ordering; the rows are otherwise independently actionable.

| Priority | Work | Estimate |
| --- | --- | --- |
| P2 | [context-date-needs-no-clock-cartridge](../../../root/prds/context-date-needs-no-clock-cartridge/prd.md) | 4h |
| P1 | [terminal-profile-starts-only-needed-services](../../../root/prds/terminal-profile-starts-only-needed-services/prd.md) | 1d |
| P1 | [rpc-contracts-run-across-rust-lua-and-bun](../../../root/prds/rpc-contracts-run-across-rust-lua-and-bun/prd.md) | 2d |
| P1 | [fresh-checkouts-can-run-the-gates](../../../root/prds/fresh-checkouts-can-run-the-gates/prd.md) | 1d |
| P1 | [ci-proves-the-supported-terminal-matrix](../ci-proves-the-supported-terminal-matrix/prd.md) | 2d |
| P1 | [the-agent-can-discover-its-own-program](../../../root/prds/the-agent-can-discover-its-own-program/prd.md) | 1d |
| P1 | [debug-mode-correlates-a-terminal-turn](../../../agent/prds/debug-mode-correlates-a-terminal-turn/prd.md) | 2d |
| P1 | [the-agent-can-extend-and-verify-a-cartridge](../../../root/prds/the-agent-can-extend-and-verify-a-cartridge/prd.md) | 2d |
| P1 | [rolling-context-retains-decision-evidence](../../../root/prds/rolling-context-retains-decision-evidence/prd.md) | 1d |
| P2 | [the-live-record-matches-the-terminal-contract](../../../root/prds/the-live-record-matches-the-terminal-contract/prd.md) | 1d |
| P1 | [cartridges-prove-themselves-at-registration](../../../root/prds/cartridges-prove-themselves-at-registration/prd.md) | 2d |

Clarification: [[the-agent-can-diagnose-and-extend-its-runtime]] makes program discovery → debugging →
extension a testable agent workflow, with diagnostics as supporting evidence.

### Check

- [ ] Every child has its acceptance evidence and is done.
- [ ] The audit is updated with the resulting dependency graph, gate results,
      debug invocation and remaining explicit limits.
