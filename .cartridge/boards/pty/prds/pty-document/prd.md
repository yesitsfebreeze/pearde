---
repo: /Users/feb/dev/cartridge/pty.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: pty
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: capabilities-live-with-their-owners
needs:
- '@mcp/clients-share-document-execution/client-document-contract'
- '@pty/improve-pty-input-ownership'
- '@pty/improve-pty-command-wait'
footprint:
- /Users/feb/dev/cartridge/pty.ctg/src/tool.rs
- /Users/feb/dev/cartridge/pty.ctg/.cartridge/tests/integration/process.rs
- /Users/feb/dev/cartridge/pty.ctg/.cartridge/help.md
---

# A shell document uses the owned persistent terminal

Under `the-tool-contract-is-a-memo` a recipe document runs through the shared document runner
(contract leaf, still open). Today `tool.shell` (`pty.ctg/src/tool.rs`) is pty's only
execution surface, so a shell recipe selected from a document must reach the user's visible
shell through that same call, never a hidden subprocess. This leaf adapts the frozen contract's
one-shot invocation to `tool.shell`; busy refusal, ownership and command ids are owned by the
two pty needs and only reused here. Per `a-cartridge-brings-its-own-surface`, pty depends on the
contract's declared key only and learns nothing about memo, agent, mcp or proxy.

## Acceptance

- [ ] A shell recipe invoked through the contract runs in the existing shell PID and returns the contract result with its command id.
- [ ] While a program or user owns input, the invocation refuses with the contract's denial shape and writes nothing.
- [ ] Cancelling the invocation interrupts only its own command and reports completion as uncertain when no done mark arrives.

## Proof and recovery

First step: once the contract leaf publishes its fixtures, run `just test pty` (cwd
`/Users/feb/dev/cartridge`) to record the baseline, then add a contract-shaped fixture to
`.cartridge/tests/integration/process.rs`. Gate: the same command. Rollback: direct
`tool.shell` calls stay unchanged; removing the adapter removes only document invocation.

## Dependencies and review

Blocked on three open needs. [Review history](review.md); rounds inherited from `capabilities-live-with-their-owners`; limit five.
