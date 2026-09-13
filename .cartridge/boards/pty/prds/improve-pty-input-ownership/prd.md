---
repo: /Users/feb/dev/cartridge/pty.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: pty
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-pty-input-ownership
needs:
- '@pty/improve-pty-shell-identity'
footprint:
- /Users/feb/dev/cartridge/pty.ctg/main.rs
- /Users/feb/dev/cartridge/pty.ctg/tool.rs
- /Users/feb/dev/cartridge/pty.ctg/marks.rs
- /Users/feb/dev/cartridge/pty.ctg/input.rs
- /Users/feb/dev/cartridge/pty.ctg/tests/process.rs
---

# Coordinate human and agent input on the shared terminal

Separate input lease ownership from foreground-program state. Human input may revoke an agent lease immediately, but granting a new agent command requires an observed shell-ready boundary; an active command/editor receives only explicitly intended literal human input. Child execution goes through the owner's lease and carries command/call identity.

## Acceptance

- [ ] Concurrent agents cannot interleave writes; a refused caller sees busy/owner information without gaining a lease.
- [ ] Human preemption during nvim and a long-running command invalidates the old lease, and the next agent command is refused until shell readiness is observed.
- [ ] Expiry/reload/cancellation cannot unlock another invocation's lease or permanently wedge input; the PTY PID and user's editor remain intact.

## Proof and recovery

Start at [main.rs](../../../main.rs), [tool.rs](../../../tool.rs), [marks.rs](../../../marks.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test pty` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-pty-input-ownership`; maximum five rounds.
