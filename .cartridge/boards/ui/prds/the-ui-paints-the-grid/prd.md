---
repo: /Users/feb/dev/cartridge/tui.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: ui
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: the-ui-paints-the-grid
---

# the-ui-paints-the-grid

Rebase the painter plan onto current ui.ctg/PTy interfaces and retain one PTY-owned emulator. Measure a reproducible 120x40 continuous-redraw fixture before/after transport changes; require no wrong/missing final cells and no more than 20% median throughput regression over five paired runs. Missed frame generations trigger a full resync, not stale row reuse.

## Acceptance

- [ ] Row, style, palette, cursor and wide-character fixtures render the same final grid as the PTY, including after dropped updates and resize.
- [ ] Real nvim and UI replacement preserve screen/input semantics and the current footer/transcript contract.
- [ ] Performance reports name hardware/toolchain, fixture rate and all samples; unsupported environments remain unmeasured instead of passing a guessed smoothness claim.

## Proof and recovery

Start at [chat.ts](../../../../../../ui.ctg/src/chat.ts), [modules.ts](../../../../../../ui.ctg/src/modules.ts).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test ui` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

External evidence prerequisites: [pty-owns-the-terminal-grid](../../../../memos/work/root--pty-owns-the-terminal-grid.md), [pty-encodes-input](../../../../memos/work/root--pty-encodes-input.md). Resolve their current completion and source revision before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `the-ui-paints-the-grid`; maximum five rounds.
