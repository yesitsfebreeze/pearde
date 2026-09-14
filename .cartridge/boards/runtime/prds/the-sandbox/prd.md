---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: runtime
work-kind: rollup
review-round: 3
review-status: passed
canonical-scope: the-sandbox
needs:
- '@runtime/launch-authority'
- '@runtime/linux-policy'
- '@runtime/macos-policy'
---

# The sandbox

Track the linked current outcomes as a finite scope snapshot. On the transport host,
the grant in `cartridge.json` is the only policy input, and `src/sandbox.rs` is
the only wall. macOS builds a `sandbox-exec` profile; networking is all or
nothing, a documented platform limit. Linux refuses all execution
(`src/sandbox_linux.rs`). Historical framework and product proposals remain
source history.

## Acceptance

- [ ] Each included leaf has its own current acceptance and owner.
- [ ] At one pinned cartridge.ctg revision, `just test runtime` passes on macOS and, once linux-policy lands, on its recorded Linux runner. Close this snapshot only against that child evidence; later enhancements get separate work items.

## Work items

- [launch-authority — Every cartridge process starts inside its grant, and nothing it spawns escapes it](../launch-authority/prd.md)
- [linux-policy — Linux commands install Landlock and seccomp before execution, enforce declared capabilities, and refuse unsupported confinement.](../linux-policy/prd.md)
- [macos-policy — macOS commands enforce manifest capabilities through sandbox-exec with verified runtime exceptions and real allowed/denied operation tests.](../macos-policy/prd.md)

Shared footprint: `src/sandbox.rs` and `.cartridge/tests/unit/src/sandbox/tests.rs`; land serially.

## Review

[Review history](review.md): round 3/5.
