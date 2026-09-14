---
repo: /Users/feb/dev/cartridge/agent.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: agent
work-kind: rollup
review-round: 3
review-status: failed
canonical-scope: debug-mode-correlates-a-terminal-turn
needs:
- '@root/every-enabled-tool-ships-a-contract-probe'
- '@root/tool-probes-run-and-locate-a-failing-provider'
---

# The agent tests and diagnoses its own runtime

The agent enters debug mode through the visible shell, exercises the enabled cartridges against their declared contracts and locates a failing one. This parent coordinates the children below; it is not implementation work.

## Acceptance

- [ ] Each linked child passes its own review and acceptance, or its tracked memo reaches done with evidence.
- [ ] Integration: in a disposable profile the agent opens debug mode from the shell, runs `cartridge verify` and `cartridge doctor`, attributes a deliberately failing fixture cartridge from their output and the turn's trace ID, and closes debug mode with the user's PTY intact.
- [ ] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [Every enabled tool ships a contract probe](../../../root/prds/every-enabled-tool-ships-a-contract-probe/prd.md)
- [Tool probes run and locate a failing provider](../../../root/prds/tool-probes-run-and-locate-a-failing-provider/prd.md)
- Debug mode opens and closes from the shell — root memo `prd.ctg/.cartridge/memos/work/root--debug-mode-opens-and-closes-from-the-shell.md`, `blocked`, no PRD.
- A turn carries one ID through host, Lua and Bun — root memo `root--a-turn-carries-one-id-through-host-lua-and-bun.md`, `done`.
- Context: the agent can discover its own program — root memo, `done`.

## Integration gate

The host now ships `selftest`/`integration` contracts run by `cartridge verify` and a `doctor` event run by `cartridge doctor` (cartridge `b02b200`, `docs/creating-cartridges.txt` CONTRACTS). Both probe children predate this and must be reconciled onto it before this gate is final. From `/Users/feb/dev/cartridge`: `just verify` and `just test runtime` after the children pass. Not run for this plan.

## Review

[Review history](review.md): round 3 of 5 (rounds 1–2 inherited).
