---
state: open
origin: requested
priority: 91
repo: "/Users/feb/dev/cartridge"
work-kind: leaf
needs:
  - "@memory/memory-experience-becomes-reliable-and-useful/memory-exposes-total-backlog-and-the-reason-progress-stopped"
  - "@memory/memory-experience-becomes-reliable-and-useful/recurrence-cannot-masquerade-as-retrieval-usefulness"
footprint:
  - "scope.ctg/src/sources.py"
  - "scope.ctg/src/state.py"
  - "scope.ctg/src/asp_activity.py"
  - "scope.ctg/src/inspector.py"
  - "scope.ctg/src/graph_tree.py"
  - "scope.ctg/src/test_asp_activity.py"
  - "scope.ctg/src/test_health.py"
  - "scope.ctg/README.md"
  - "scope.ctg/.cartridge/help.md"
---

# Scope distinguishes memory use from stalled processing

Show declared memory progress and labelled use signals in the existing ASP graph and inspector. Keep the minute timeline about observed calls. This is a focused extension to the existing Scope PRD, not a return to the superseded processing-cycle dashboard.

## Evidence

Scope now reads resident recent memory and stored usage. It does not show total historical backlog or a stale crystallization writer. USES currently includes throttled reinforcement; stored heat has mixed origins. Existing minute cells correctly avoid inventing historical events. See [investigation](../../../memory/prds/memory-experience-becomes-reliable-and-useful/investigation.md).

## Acceptance

- [ ] A query-serving but stalled writer shows its backlog, last progress and error next to the same memory graph.
- [ ] Retrieval reinforcement, recurrence and observed calls have distinct labels; loaded/resident totals are not presented as bank-wide totals.
- [ ] Repeated polls and pagination do not add usage, heat or synthetic timestamps; source failure or generation change marks retained values stale until fresh data arrives.
- [ ] The real collector/State path and a terminal snapshot exercise idle, active, backlog and unavailable cases without live-store mutation.

## Proof and recovery

Extend the existing Scope regression and collector/State fixtures in test_health.py. From the composition root run `python3 -m unittest discover -s scope.ctg/src -p 'test_*.py'` and an isolated PTY check; verify the declared ASP attributes before testing the UI.

Consume public ASP only. Preserve selection and bounded polling, and stop background collectors cleanly. Reopen the pane to prove the loaded Python revision. Scope S.

## Dependencies and review

Hard prerequisites are in frontmatter; other related work is indexed in the investigation. All new work remains open and unclaimed. [Review](review.md) must reach 90/100 without blockers before implementation. Update owner README and help together; finish with ./task audit and ./task isolation from the composition root.
