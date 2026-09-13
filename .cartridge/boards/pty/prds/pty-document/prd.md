---
repo: /Users/feb/dev/cartridge/pty.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: pty
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: capabilities-live-with-their-owners
needs:
- '@mcp/clients-share-document-execution'
- '@pty/improve-pty-input-ownership'
---

# A shell document uses the owned persistent terminal

Route shell invocation through PTY ownership and command identity, preserving the shell PID.

## Acceptance

- [ ] Busy foreground input refuses a new agent command.
- [ ] An allowed command runs in the existing shell and returns its command ID.
- [ ] Cancellation affects only the owned command and reports uncertain completion honestly.

## Proof and recovery

Start at [tool.rs](../../../tool.rs), [input.rs](../../../input.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test pty` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `capabilities-live-with-their-owners`; maximum five rounds.
