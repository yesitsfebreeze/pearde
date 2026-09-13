---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: runtime
work-kind: rollup
review-round: 2
review-status: stale-after-migration
canonical-scope: the-sandbox
needs:
- '@runtime/launch-authority'
- '@runtime/linux-policy'
- '@runtime/macos-policy'
---

# The sandbox

Track the linked current outcomes as a finite scope snapshot. Historical framework and product proposals remain source history.

## Acceptance

- [ ] Each included leaf has its own current acceptance and owner.
- [ ] Close this snapshot only against observed child evidence; later enhancements get separate work items.

## Work items

- [launch-authority — Discovery, direct, resolver and nested launches use trusted host-resolved policies while preserving scoped wire behavior and descendant teardown.](../launch-authority/prd.md)
- [linux-policy — Linux commands install Landlock and seccomp before execution, enforce declared capabilities, and refuse unsupported confinement.](../linux-policy/prd.md)
- [macos-policy — macOS commands enforce manifest capabilities through sandbox-exec with verified runtime exceptions and real allowed/denied operation tests.](../macos-policy/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `the-sandbox`; maximum five rounds.
