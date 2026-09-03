---
state: open
origin: requested
priority: 80
complexity: 35
blast-radius:
needs: the-doctor-refuses-drift
---

# the board is read once per process

`scan()` returns one board record — prds, settings, plan, bands, workflow marks — and `compute_plan`, `progress_line`, `cut_lane`, `snapshot`, `gantt_payload` and `dispatchable` take it instead of re-walking. The three "ready" definitions (`pressure_bands`, `plan_frontier`, `transitions.sections`) become one.

## Done means

`pearde scan` walks the tree once (count `os.walk` calls under a probe); `pearde plan` and `pearde scan` list the same PRDs as ready on a board with an `after:` edge.

## Needs

`one-primitive-one-definition` and `every-documented-command-exists` — both children of `the-doctor-refuses-drift`; the frontmatter `needs:` names that container, which is done exactly when both are.
