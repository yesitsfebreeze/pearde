---
repo: /Users/feb/dev/cartridge/pty.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
work-kind: leaf
review-round: 3
review-status: "passed"
canonical-scope: improve-pty-shell-identity
footprint: ["src/main.rs","src/marks.rs","src/tool.rs","src/identity.rs",".cartridge/tests/unit/identity/tests.rs",".cartridge/tests/integration/process.rs",".cartridge/docs/shell-identity.md"]
capability-owner: "pty"
commit: "e8e6b319b03dcc9e1dea66b4fd3a0f6b83ab2d47"
---

# Return explicit shell and working-directory identity

Every shell readback states the shell executable/dialect, cwd, phase and whether command integration is supported.

## Acceptance

- [x] Nushell, Zsh and Bash fixtures return explicit identity/cwd without requiring welcome-text parsing.
- [x] An unsupported shell reports unknown integration while screen/input still work; UI replacement does not replace the PTY.

- [x] Preserve the one shared PTY and literal-input fallback. Feature negotiation/additive fields permit old callers; reverting the UI/client must not terminate the user's shell. Do not interrupt the live terminal for testing.

## Proof and recovery

Start at [main.rs](../../../main.rs), [tool.rs](../../../tool.rs), [marks.rs](../../../marks.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test pty` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-pty-shell-identity`; maximum five rounds.

## From the retired work memo

Folded 2026-09-15 from `work/improve-pty-shell-identity.md` (status open). The PRD state above is authoritative.

### Outcome

Every shell readback states the shell executable/dialect, cwd, phase and whether command integration is supported.

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
- [ ] Nushell, Zsh and Bash fixtures return explicit identity/cwd without requiring welcome-text parsing.
- [ ] An unsupported shell reports unknown integration while screen/input still work; UI replacement does not replace the PTY.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Use the existing environment scan and shell marks; separate configured executable from detected dialect and unknown state. Preserve literal-input fallback for unsupported shells.
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

Priority P1; scope size S (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
No hard prerequisite inside this programme; ready for an owner after source/claim checks.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
