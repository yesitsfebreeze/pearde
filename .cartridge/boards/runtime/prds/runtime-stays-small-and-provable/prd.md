---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: rollup
review-round: 3
review-status: failed
canonical-scope: runtime-stays-small-and-provable
needs:
- '@runtime/ci-proves-the-supported-terminal-matrix'
- '@agent/debug-mode-correlates-a-terminal-turn'
- '@runtime/the-reload-test-is-not-flaky'
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
