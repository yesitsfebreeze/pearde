---
state: claimed
origin: requested
priority: 90
complexity: 15
blast-radius: high
workflow: probe-then-spec
claim: impl-redo-collect-runs 2026-09-03 21:38
---


# collect runs the invariants and red refuses

`collect` runs every `resources/invariants/*.sh` before writing `done`. Any non-zero exit refuses the collect, prints the failing invariant and its output, and leaves state unchanged — the PRD stays exactly where it was.

Absorbs the gate `the-session-rebase-rollback-asks-refuse-before-it-resets` (open, ready) as a sibling gate on the same collect path: that PRD asks `refuse` before a reset, this one asks the invariants before `done`; neither touches the other's text.

## Done means

Plant an invariant that exits 1 → `collect` exits 1, the PRD stays `claimed`, the output names the script; remove it → collect proceeds.

## Needs

No gate. `the-session-rebase-rollback-asks-refuse-before-it-resets` is a sibling gate on collect, named here and left untouched.

## History

**failed, retried 2026-09-03 21:37**

**2026-09-03 21:4x — the claim is dead; the report is the analyst's**

The report on disk is the analyst's SPECCED (mtime earlier than the claim's
`since`), so no implementer ever returned. The worker's session was reaped —
no process on this machine holds it. The claim only reads live because its
footprint names shared files other sessions keep writing
(`silence-measures-the-workers-own-tree` names the artefact). The analyst's
work stands in `specs/`; the next implementer continues from it.
