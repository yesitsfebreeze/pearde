---
state: specced
origin: requested
priority: 90
complexity: 15
blast-radius: high
workflow: probe-then-spec
---

# collect runs the invariants and red refuses

`collect` runs every `resources/invariants/*.sh` before writing `done`. Any non-zero exit refuses the collect, prints the failing invariant and its output, and leaves state unchanged — the PRD stays exactly where it was.

Absorbs the gate `the-session-rebase-rollback-asks-refuse-before-it-resets` (open, ready) as a sibling gate on the same collect path: that PRD asks `refuse` before a reset, this one asks the invariants before `done`; neither touches the other's text.

## Done means

Plant an invariant that exits 1 → `collect` exits 1, the PRD stays `claimed`, the output names the script; remove it → collect proceeds.

## Needs

No gate. `the-session-rebase-rollback-asks-refuse-before-it-resets` is a sibling gate on collect, named here and left untouched.
