---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: runtime
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: launch-authority
---

# launch-authority — Every cartridge process starts inside its grant, and nothing it spawns escapes it

The transport host (939e7d1, c9ef10b) collapsed the old discovery, direct,
resolver and nested routes. Manifests are read as data (`src/loader/document.rs`);
the host starts every node through one call, `src/host/process.rs` into
`crate::sandbox::command`; and `cartridge.spawn` (`src/node.rs`) runs a child
from inside the node's wall. What is unproven is that the wall holds for nested
children and that a refused wall spawns nothing. The CLI `launch` branch
(`src/cli/host.rs`) stays out of scope: it is the narrow CLI policy kept by
decision `core-composes-and-the-cli-selects-services`.

## Acceptance

- [ ] On macOS, `cartridge.spawn` of a program the node's grant does not name fails with a denial reaching the listener, while a granted program runs (real child processes, not profile text).
- [ ] When the platform wall cannot be built, start fails naming the cartridge, dependents report it unavailable, and no child process exists. This check runs on the Linux runner named by linux-policy.
- [ ] Stopping or replacing a node leaves no nested child running; its dependents keep working (extend `a_restart_keeps_its_dependents_working`).

## Proof and recovery

Start at `src/host/process.rs`, `src/node.rs` (`spawn`) and `src/sandbox.rs`.
Add fixtures to `.cartridge/tests/unit/src/tests/host.rs`. Gates, from
`/Users/feb/dev/cartridge`: `just test runtime` and `just check runtime`. They
have not run for this plan. A failed fix preserves the current single launch
route. Never add an unconfined fallback.

## Dependencies and review

No hard prerequisite. The Linux case uses the runner from
[linux-policy](../linux-policy/prd.md). [Review](review.md): round 3/5.
