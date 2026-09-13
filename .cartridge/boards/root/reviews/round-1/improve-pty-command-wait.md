---
kind: work
description: "Wait and retrieve output for one terminal command"
status: open
priority: P1
size: M
needs:
  - "[[@prd/work/root--improve-pty-shell-identity.md]]"
uses:
  - usage: "[[read-usage]]"
    when: ["wait and retrieve output for one terminal command", "implementing pty cartridge improvements"]
---

# Wait and retrieve output for one terminal command

## Outcome

A caller can follow one stable command ID to completion and distinguish timeout, shell exit and truncated output.

## Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
Related existing work (context/coordination, not automatically a hard dependency): [[@prd/work/root--sub-agents-share-the-terminal.md]], [[@prd/work/root--pty-encodes-input.md]].

## Footprint

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

## Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] Wait on command A while B completes later: A's ID, exit and output remain correctly attributed; timeout does not kill A.
- [ ] Output beyond the configured limit is explicitly truncated/pageable; dropped history and unsupported shell integration are reported without false completion.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

## Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Expose the existing command IDs/marks through bounded wait and output cursor operations. Readback timeout must leave the command running; expired history returns an explicit result rather than another command's output.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

## Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test pty
just check pty
```


## Compatibility and recovery

Preserve the one shared PTY and literal-input fallback. Feature negotiation/additive fields permit old callers; reverting the UI/client must not terminate the user's shell. Do not interrupt the live terminal for testing.

## Handoff

Priority P1; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [[@prd/work/root--improve-pty-shell-identity.md]] are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
