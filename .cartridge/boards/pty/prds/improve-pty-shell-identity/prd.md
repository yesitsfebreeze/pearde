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
