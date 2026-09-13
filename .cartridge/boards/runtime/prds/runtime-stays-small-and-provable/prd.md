---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: rollup
review-round: 2
review-status: stale-after-migration
canonical-scope: runtime-stays-small-and-provable
needs:
- '@runtime/ci-proves-the-supported-terminal-matrix'
- '@agent/debug-mode-correlates-a-terminal-turn'
- '@runtime/the-reload-test-is-not-flaky'
---

# A small, provable terminal runtime

Coordinate the linked owner outcomes and record their combined evidence; claim a leaf for implementation.

## Acceptance

- [ ] Each linked leaf passes its own review and observable acceptance.
- [ ] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [Repository CI runs the gates and reports terminal coverage explicitly](../ci-proves-the-supported-terminal-matrix/prd.md)
- [The agent tests and diagnoses its own runtime](../../../agent/prds/debug-mode-correlates-a-terminal-turn/prd.md)
- [the-reload-test-is-not-flaky](../the-reload-test-is-not-flaky/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `runtime-stays-small-and-provable`; maximum five rounds.
