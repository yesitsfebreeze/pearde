---
kind: work
description: "Display shared terminal ownership and cwd"
status: open
priority: P2
size: M
needs:
  - "[improve-pty-input-ownership](../../../pty/prds/improve-pty-input-ownership/prd.md)"
uses:
  - usage: "[[read-usage]]"
    when: ["display shared terminal ownership and cwd", "implementing ui cartridge improvements"]
---

# Display shared terminal ownership and cwd

## Outcome

The UI shows which actor currently owns input and which working directory commands will use, including human preemption.

## Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
Related existing work (context/coordination, not automatically a hard dependency): [the-sidebar-slides-over-the-shell](../../prds/the-sidebar-slides-over-the-shell/prd.md), [the-palette-and-exit](../../prds/the-palette-and-exit/prd.md), [the-terminal-is-drawn-from-pty](../../prds/the-terminal-is-drawn-from-pty/prd.md).

## Footprint

Terminal UI; one observable outcome. The listed files are starting points and a proposed edit footprint, not permission to make unrelated changes.
All paths below are relative to /Users/feb/dev/cartridge.

- `ui.ctg/ui/index.ts`
- `ui.ctg/ui/palette.tsx`
- `ui.ctg/ui/activity.ts`
- `ui.ctg/src/chat.ts`
- `ui.ctg/tests/transcript.test.tsx`
- `ui.ctg/tests/palette.test.tsx`

Tests/fixtures and owner-local documentation for this outcome may be added beside
these sources. Recheck active claims before changing shared files. Update cartridge.json
only when public services, schema, configuration or verification commands actually change.

## Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] Move the shell cwd and transfer/preempt input ownership: the visible status updates before another command is sent.
- [ ] Stale/disconnected ownership is labelled unknown and cannot appear as a valid grant; UI reload preserves the PTY.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

## Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Consume PTY identity and ownership events in the existing surface, with minimal persistent chrome and accessible status text. Do not infer ownership from the last visible message.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

## Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test ui
just check ui
```


## Compatibility and recovery

Keep session/PTY state in their existing owners. New UI features can be disabled/reverted without closing the PTY or deleting history. Check module replacement, keyboard navigation and supported terminal widths.

## Handoff

Priority P2; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [improve-pty-input-ownership](../../../pty/prds/improve-pty-input-ownership/prd.md) are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
