---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# script ingesting every part as one claim, kind as claim-kind, idempotent

From [[working-with-memory]] item 4. Retired by the fold (`memory-seam`).

## Do
One script under `scripts/`: every part under `memos/` except `insights/`
and `dashboards/` (generated) becomes one `memory ingest` claim — the part's
`kind` as claim-kind label, the file path as source. Idempotent by
content-hash id. Add a `just` target.

## Acceptance
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
Retired 2026-09-05 by [retire-the-parts-ingest-script](../retire-the-parts-ingest-script/prd.md): the file watcher
rooted at `memos/` (`the-watcher-watches-parts`) is what carries the record
now.
