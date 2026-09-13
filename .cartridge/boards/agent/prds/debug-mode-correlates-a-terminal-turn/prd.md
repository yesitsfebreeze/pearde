---
repo: /Users/feb/dev/cartridge/agent.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: agent
work-kind: rollup
review-round: 2
review-status: stale-after-migration
canonical-scope: debug-mode-correlates-a-terminal-turn
needs:
- every-enabled-tool-ships-a-contract-probe
- tool-probes-run-and-locate-a-failing-provider
---

# The agent tests and diagnoses its own runtime

Coordinate the linked owner outcomes and record their combined evidence; claim a leaf for implementation.

## Acceptance

- [ ] Each linked leaf passes its own review and observable acceptance.
- [ ] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [Every enabled tool ships a contract probe](../../../root/prds/every-enabled-tool-ships-a-contract-probe/prd.md)
- [Tool probes run and locate a failing provider](../../../root/prds/tool-probes-run-and-locate-a-failing-provider/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `debug-mode-correlates-a-terminal-turn`; maximum five rounds.
