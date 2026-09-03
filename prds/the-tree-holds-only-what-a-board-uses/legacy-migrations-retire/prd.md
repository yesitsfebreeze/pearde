---
state: open
origin: requested
priority: 55
complexity: 10
blast-radius:
needs: every-module-finds-its-siblings-by-one-rule
---

# legacy migrations retire

`migrate_legacy_state` (runs on every import of `plan.py`), guard's `LEGACY` handling for the retired machine dir, `shared.RETIRED` and the `pearde/` ↔ `.pearde/` compatibility branches are one-shot migrations from 2026-09-01/02. `pearde upgrade` is the only migration door; each moves there or goes.

## Done means

No module runs a migration at import; grep for `LEGACY`/`RETIRED` returns only `upgrade`.

## Needs

`every-module-finds-its-siblings-by-one-rule`.
