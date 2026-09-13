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
canonical-scope: improve-pty-command-wait
needs:
- '@pty/improve-pty-shell-identity'
footprint:
- /Users/feb/dev/cartridge/pty.ctg/main.rs
- /Users/feb/dev/cartridge/pty.ctg/tool.rs
- /Users/feb/dev/cartridge/pty.ctg/marks.rs
- /Users/feb/dev/cartridge/pty.ctg/input.rs
- /Users/feb/dev/cartridge/pty.ctg/tests/process.rs
---

# Wait and retrieve output for one terminal command

A caller can follow one stable command ID to completion and distinguish timeout, shell exit and truncated output.

## Acceptance

- [ ] Wait on command A while B completes later: A's ID, exit and output remain correctly attributed; timeout does not kill A.
- [ ] Output beyond the configured limit is explicitly truncated/pageable; dropped history and unsupported shell integration are reported without false completion.

- [ ] Preserve the one shared PTY and literal-input fallback. Feature negotiation/additive fields permit old callers; reverting the UI/client must not terminate the user's shell. Do not interrupt the live terminal for testing.

## Proof and recovery

Start at [main.rs](../../../main.rs), [tool.rs](../../../tool.rs), [marks.rs](../../../marks.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test pty` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-pty-command-wait`; maximum five rounds.
