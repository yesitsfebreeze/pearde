---
repo: /Users/feb/dev/cartridge/pty.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: pty
work-kind: rollup
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-pty-programme
needs:
- '@pty/improve-pty-shell-identity'
- '@pty/improve-pty-input-ownership'
- '@pty/improve-pty-command-wait'
---

# PTY and shared shell improvement plan

Coordinate the linked owner outcomes and record their combined evidence; claim a leaf for implementation.

## Acceptance

- [ ] Each linked leaf passes its own review and observable acceptance.
- [ ] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [Return explicit shell and working-directory identity](../improve-pty-shell-identity/prd.md)
- [Coordinate human and agent input on the shared terminal](../improve-pty-input-ownership/prd.md)
- [Wait and retrieve output for one terminal command](../improve-pty-command-wait/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-pty-programme`; maximum five rounds.
