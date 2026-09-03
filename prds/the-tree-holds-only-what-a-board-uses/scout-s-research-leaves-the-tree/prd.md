---
state: claimed
origin: requested
priority: 50
complexity: 20
blast-radius: mid
workflow: probe-then-spec
claim: impl-redo-scout-s-rese 2026-09-03 21:38
---


# scout's research leaves the tree

`findings.md`, `reading-list.md`, `snapshots/*.tsv` and `templates/` under `resources/scout` are the author's research for another project (1,900 lines). They move to a separate repo or the board's wiki; `snapshots/` ships empty with a README line; `route.sh`, `scout.sh`, `toolscout.sh` and `buckets.txt` stay.

The user's data — moved, never deleted.

## Done means

`resources/scout` holds only tool files; `files.md` rows updated.

## Needs

No gate.

## History

**failed, retried 2026-09-03 21:37**

**2026-09-03 21:4x — the claim is dead; the report is the analyst's**

The report on disk is the analyst's SPECCED (mtime earlier than the claim's
`since`), so no implementer ever returned. The worker's session was reaped —
no process on this machine holds it. The claim only reads live because its
footprint names shared files other sessions keep writing
(`silence-measures-the-workers-own-tree` names the artefact). The analyst's
work stands in `specs/`; the next implementer continues from it.
