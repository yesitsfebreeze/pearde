---
state: open
origin: requested
priority: 90
repo: "/Users/feb/dev/cartridge/jev.ctg"
work-kind: leaf
needs:
  - '@root/jev-decides-every-closed-set-question-over-the-asp-world/jev-pulls-asp-slices-narrows-them-in-two-passes-and-sends-only-allowed-schemes'
  - '@root/the-event-ring-keeps-every-event-forever-by-rolling-it-into-day-week-month-and-year-tiers-under-asp'
footprint:
  - 'src'
  - '.cartridge'
  - 'cartridge.json'
  - 'README.md'
---

# every jev decision is an asp entity and its recorded outcome tunes the gate

## Outcome

jev.ctg is an ASP provider. It owns the scheme `decision:`. Every decision
is an entity with `about` edges to the entities it was made over, and it
carries its point, verdict, confidence and the revision it was computed
against. When the fallback path or the user later decides otherwise, that
outcome is recorded against the decision. A routine reads those outcomes
from the ring and proposes new gates for each judgement.

## Context

TypeSafe's documentation says of thresholds: "Start with conservative
thresholds, test with your own data, and adjust as you observe results."
The ring is that data. Without recorded outcomes a gate is a guess that
nobody revisits.

## Acceptance

- [ ] jev.ctg declares the scheme `decision:` and the edge kind `about` in
      its `cartridge.json`, and ASP `expand` on a file shows the decisions
      made about it, labelled with jev as the contributor.
- [ ] `jev {op:"outcome", decision_id, agreed, by}` publishes
      `jev.outcome`. A named test joins it to its decision through the
      ring's index by entity id.
- [ ] A routine memo computes, for each judgement, the agreement rate in
      each confidence band, and prints the `act` gate that would have kept
      agreement above a stated target. It changes nothing by itself.
- [ ] Unloading jev.ctg removes the `decision:` facts and nothing else.
