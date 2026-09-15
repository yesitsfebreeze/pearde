---
repo: /Users/feb/dev/cartridge/pty.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
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

## From the retired work memo

Folded 2026-09-15 from `work/improve-pty-input-ownership.md` (status open). The PRD state above is authoritative.

### Outcome

Input is attributed to an owner and cannot silently interleave between an agent invocation and human interaction.

### Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
Related existing work (context/coordination, not automatically a hard dependency): [sub-agents-share-the-terminal](../../../agent/prds/sub-agents-share-the-terminal/prd.md), [pty-encodes-input](../../../root/prds/pty-encodes-input/prd.md).

### Footprint

PTY and shared shell; one observable outcome. The listed files are starting points and a proposed edit footprint, not permission to make unrelated changes.
All paths below are relative to /Users/feb/dev/cartridge.

- `pty.ctg/main.rs`
- `pty.ctg/tool.rs`
- `pty.ctg/marks.rs`
- `pty.ctg/input.rs`
- `pty.ctg/tests/process.rs`

Tests/fixtures and owner-local documentation for this outcome may be added beside
these sources. Recheck active claims before changing shared files. Update cartridge.json
only when public services, schema, configuration or verification commands actually change.

### Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] Two concurrent callers cannot interleave input; the refused caller gets the current owner and a retryable state.
- [ ] Human preemption invalidates the old lease, cancellation affects only its invocation, and expiry/reload does not leave the terminal permanently locked.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. This is a large slice: use that bounded probe to split implementation into smaller child outcomes if more than one independent state transition or migration is required.
2. Reuse existing serialized input and invocation identity. Add a bounded ownership/lease contract and explicit human preemption; child agents request execution through their owner. Coordinate with the active pty-encodes-input work before editing shared input code.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

### Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test pty
just check pty
```


### Compatibility and recovery

Preserve the one shared PTY and literal-input fallback. Feature negotiation/additive fields permit old callers; reverting the UI/client must not terminate the user's shell. Do not interrupt the live terminal for testing.

### Handoff

Priority P1; scope size L (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [improve-pty-shell-identity](../improve-pty-shell-identity/prd.md) are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
