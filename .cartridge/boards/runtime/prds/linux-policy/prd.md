---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: runtime
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: linux-policy
---

# linux-policy — Linux commands install Landlock and seccomp before execution, enforce declared capabilities, and refuse unsupported confinement.

Require a real disposable Linux runner as the first analysis prerequisite. The implementation spec must name its kernel and Landlock ABI, record the required filesystem/network/exec guarantees and test unsupported facilities. The macOS workstation can prepare the design but cannot supply Linux enforcement evidence; this availability remains an explicit unresolved gate until a runner is identified.

## Acceptance

- [ ] A real Linux process proves allowed and denied read/write/exec and empty-network TCP/UDP behavior, with inherited descriptors and no-new-privileges covered.
- [ ] Deliberately unsupported ABI/facility and failed policy installation refuse before cartridge instructions execute.
- [ ] Cross compilation is reported separately from runtime enforcement; no supported-Linux completion or release claim is made from compile success alone.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

External evidence prerequisites: [command-adapter](../../../.pearde/prds/the-sandbox/command-adapter/prd.md). Resolve their current completion and source revision before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `linux-policy`; maximum five rounds.
