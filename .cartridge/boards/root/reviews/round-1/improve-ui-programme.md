---
kind: work
description: "Deliver the three Terminal UI improvements with explicit risk coverage"
status: open
subwork:
  - "[improve-ui-run-history](../../../ui/prds/improve-ui-run-history/prd.md)"
  - "[improve-ui-terminal-owner](../../../ui/prds/improve-ui-terminal-owner/prd.md)"
  - "[improve-ui-tool-availability](../../../ui/prds/improve-ui-tool-availability/prd.md)"
uses:
  - usage: "[[read-usage]]"
    when: ["planning ui improvements", "reviewing ui cartridge readiness"]
---

# Terminal UI improvement plan

## Outcome

Deliver the three improvements requested for Terminal UI, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

## Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Reopen completed run evidence after closing the panel | [improve-ui-run-history](../../../ui/prds/improve-ui-run-history/prd.md) |
| 2. Display shared terminal ownership and cwd | [improve-ui-terminal-owner](../../../ui/prds/improve-ui-terminal-owner/prd.md) |
| 3. Explain tool readiness and policy in the palette | [improve-ui-tool-availability](../../../ui/prds/improve-ui-tool-availability/prd.md) |

## Downside coverage

1. Terminal compatibility requires coverage: verify narrow screens, alternate screens and supported shells.
2. Closed panels hide evidence: offer session-backed transcript access.
3. UI adds state/lifecycle complexity: preserve PTY ownership and test module replacement.

These mitigations do not claim to eliminate inherent costs or make this component
independent of all other services. Retained limitations must be stated in Result.

## Order and coordination

Start with children whose needs are satisfied. Child dependencies are authoritative;
the table is a coverage view, not a second backlog. Claim one executable child at
a time and coordinate shared files before work begins. Scope sizes are not time estimates.

Existing records to reconcile before implementation: [the-sidebar-slides-over-the-shell](../../prds/the-sidebar-slides-over-the-shell/prd.md), [the-palette-and-exit](../../prds/the-palette-and-exit/prd.md), [the-terminal-is-drawn-from-pty](../../prds/the-terminal-is-drawn-from-pty/prd.md). Their current source, status and owner take precedence over a stale assessment.

## Check

- [ ] Each child in subwork is done, with its exact commands and observed outcomes in Result.
- [ ] Each of the three downsides above has a tested mitigation or a clearly documented
      retained limitation tied to the child evidence.
- [ ] The integrated Terminal UI behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

## Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test ui
just check ui
```

## Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
