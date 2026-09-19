---
state: open
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge"
---

# Redesign Scope around completed ledger processing cycles

## Outcome

A live terminal overview grouped by ASP category, with measured activity and connections, real minute timeline cells, clear system health and a separate interactive plan. Serves ranking row 19 (Scope), directly requested by the user. The latest correction supersedes the original processing-cycle interpretation; no Ticks view or cycle header.

## Acceptance

- [x] ASP activity and graph data work against the running host.
- [x] Retained events populate on startup; replay does not invent timestamps.
- [x] Rounded sections and header focus support keyboard navigation.
- [x] Live minute cells use ░▒▓ intensity; no processing-cycle UI.
- [x] Interactive Gantt uses actual task states and recorded steps.
- [x] Final integration, terminal inspection and required checks pass.
- [x] Keyboard/mouse trails shrink directionally through eighth-block widths at paced 60 FPS.
- [x] Selected entries stay centered, including during rapid input and ranking changes.
