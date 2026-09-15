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
canonical-scope: improve-pty-command-wait
needs:
- '@pty/improve-pty-shell-identity'
footprint:
- /Users/feb/dev/cartridge/pty.ctg/src/main.rs
- /Users/feb/dev/cartridge/pty.ctg/src/tool.rs
- /Users/feb/dev/cartridge/pty.ctg/src/marks.rs
- /Users/feb/dev/cartridge/pty.ctg/.cartridge/tests/integration/process.rs
- /Users/feb/dev/cartridge/pty.ctg/.cartridge/tests/unit/marks/tests.rs
---

# Wait and retrieve output for one terminal command

Baseline (pty 0db055d, transport port): OSC 133 marks give each command an `id`
(`src/marks.rs`); `pty {op:"commands"}` lists bounded history with ids; `Shell::run` waits for
the done mark, never kills on timeout, and marks output past the limit as "truncated; tail
shown" (`src/main.rs`). Gaps: the `tool.shell` command result is text without the id, a caller
cannot wait on an id later, an id evicted from history is indistinguishable from unknown, and
the handoff record beside this PRD shows unresolved delayed-mark correlation. Excluded: input
lease semantics (`@pty/improve-pty-input-ownership`) and the tui.

## Acceptance

- [ ] A `tool.shell` command result carries its command id, exit (or running) and `truncated`, as additive fields.
- [ ] Waiting on command A's id while B later completes returns A's own exit and output; a wait timeout leaves A running.
- [ ] An id evicted from history, or a shell without mark integration, returns an explicit `unavailable` reason, never a false completion.
- [ ] A marker arriving after the wait deadline is attributed to the right id on the next wait (fixture from the handoff context).

## Proof and recovery

First step: run `just test pty` (cwd `/Users/feb/dev/cartridge`) and record the baseline,
including the two known failures in release-status; reproduce the delayed-mark case in
`.cartridge/tests/integration/process.rs` without a live user terminal. Gate: the same command.
Rollback: fields and the wait op are additive; old callers keep text results, and the shared
shell PID is never restarted by this change.

## Dependencies and review

Ready: shell identity is done. [Review history](review.md); rounds inherited from `improve-pty-command-wait`; limit five.

## From the retired work memo

Folded 2026-09-15 from `work/improve-pty-command-wait.md` (status open). The PRD state above is authoritative.

### Outcome

A caller can follow one stable command ID to completion and distinguish timeout, shell exit and truncated output.

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
- [ ] Wait on command A while B completes later: A's ID, exit and output remain correctly attributed; timeout does not kill A.
- [ ] Output beyond the configured limit is explicitly truncated/pageable; dropped history and unsupported shell integration are reported without false completion.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Expose the existing command IDs/marks through bounded wait and output cursor operations. Readback timeout must leave the command running; expired history returns an explicit result rather than another command's output.
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

Priority P1; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [improve-pty-shell-identity](../improve-pty-shell-identity/prd.md) are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
