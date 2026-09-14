---
repo: /Users/feb/dev/cartridge/pty.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: pty
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: improve-pty-input-ownership
needs:
- '@pty/improve-pty-shell-identity'
footprint:
- /Users/feb/dev/cartridge/pty.ctg/src/main.rs
- /Users/feb/dev/cartridge/pty.ctg/src/tool.rs
- /Users/feb/dev/cartridge/pty.ctg/.cartridge/tests/integration/process.rs
- /Users/feb/dev/cartridge/pty.ctg/.cartridge/docs/README.md
---

# Coordinate human and agent input on the shared terminal

Delivered baseline (pty cacd7e1, documented in `.cartridge/docs/README.md`): tool writes are
serialized by `tool_gate`; `pty {op:"control"}` hands the terminal to user or agent, and
takeback revokes writes, sends one Ctrl+C and returns the interrupted invocation; stale
cancellation only interrupts the matching context; commands need the prompt phase. Tests:
`shell_serializes_input_and_only_cancels_the_matching_invocation`,
`handoff_blocks_agent_input_and_takeback_interrupts_without_closing_shell`. Remaining gaps:
a refused caller learns no owner, and after takeback the old prompt mark can admit the next
agent command before the shell has answered the interrupt (handoff record in
`../improve-pty-command-wait/`). Keep the documented takeback interrupt.

## Acceptance

- [ ] A refused concurrent call reports busy plus the owning invocation's session/run, without acquiring input.
- [ ] After takeback and hand-back, the next agent command is refused until a new prompt mark arrives after the interrupt.
- [ ] Hand-back, reload or cancellation of one invocation never releases another invocation's ownership, and a lost owner never leaves input permanently refused.
- [ ] The shell PID and a running nvim survive every case above.

## Proof and recovery

First step: run `just test pty` (cwd `/Users/feb/dev/cartridge`) and record the baseline,
including the two known failures in release-status. Extend the two existing integration tests
with the prompt-mark race. Gate: the same command. Rollback: new fields are additive; the
existing control op and its documented behaviour stay compatible.

## Dependencies and review

Ready: shell identity is done. [Review history](review.md); rounds inherited from `improve-pty-input-ownership`; limit five.
