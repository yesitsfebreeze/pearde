---
kind: work
level: 10
status: done
description: script ingesting every part as one claim, kind as claim-kind, idempotent
read_when: "executing the dashboard plan"
---

# interim-parts-ingest

From [[working-with-memory]] item 4. Retired by the fold (`memory-seam`).

## Do
One script under `scripts/`: every part under `memos/` except `insights/`
and `dashboards/` (generated) becomes one `memory ingest` claim — the part's
`kind` as claim-kind label, the file path as source. Idempotent by
content-hash id. Add a `just` target.

## Check
Ran twice, `memory report` unchanged between runs;
`memory report --group day --claim_kind decision` shows per-day counts;
`just build && just check && just test` green.
Landed 2026-09-05: `scripts/parts_ingest.sh` plus the `just memos-ingest`
target. Each part becomes one DirectJob in `.memory/intake/direct`, keyed by
`sha256(source_id, text)` — the same id the store derives — with the part's
`kind` carried as `session://<kind>` in the source title, the label
`report --group claim_kind` reads. A drained job moves to `direct/done/`, so
the presence check reads both directories; without that every run re-parked
the whole record. Two consecutive runs left `memory report --group kind`
unchanged at 2 documents / 3488 facts, the third reported none newly parked and 66
already present, and `memory report --group day --claim-kind decision` returns
per-day counts (1 on 2026-08-16, 318 on 2026-09-05).
Retired 2026-09-05 by [[@prd/work/memory--retire-the-parts-ingest-script.md]]: the file watcher
rooted at `memos/` (`the-watcher-watches-parts`) is what carries the record
now.
