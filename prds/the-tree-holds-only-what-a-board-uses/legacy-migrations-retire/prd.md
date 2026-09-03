---
state: claimed
origin: requested
priority: 55
complexity: 36
blast-radius: high
needs: every-module-finds-its-siblings-by-one-rule
workflow: probe-then-spec
claim: impl-redo-legacy-migra 2026-09-03 21:38
---


# legacy migrations retire

`migrate_legacy_state` (runs on every import of `plan.py`), guard's `LEGACY` handling for the retired machine dir, `shared.RETIRED` and the `pearde/` ↔ `.pearde/` compatibility branches are one-shot migrations from 2026-09-01/02. `pearde upgrade` is the only migration door; each moves there or goes.

## Done means

No module runs a migration at import; grep for `LEGACY`/`RETIRED` returns only `upgrade`.

## Needs

`every-module-finds-its-siblings-by-one-rule`.

## History

**failed, retried 2026-09-03 21:37**

**2026-09-03 21:4x — the claim is dead; the report is the analyst's**

The report on disk is the analyst's SPECCED (mtime earlier than the claim's
`since`), so no implementer ever returned. The worker's session was reaped —
no process on this machine holds it. The claim only reads live because its
footprint names shared files other sessions keep writing
(`silence-measures-the-workers-own-tree` names the artefact). The analyst's
work stands in `specs/`; the next implementer continues from it.
