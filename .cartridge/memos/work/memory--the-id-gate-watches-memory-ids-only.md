---

kind: work
level: 10
status: done
description: "`id_mint_reads_no_clock` pins twelve memory-id functions and none of the four that mint entity and reason ids, though `document_id`'s own contract names export, import and hub merge as resting on the same determinism"
read_when: "adding an id minter, or trusting the id gate"
---

# the-id-gate-watches-memory-ids-only

## Do

`tests/id_mint_reads_no_clock.rs` checks five spellings of a clock read against
the **bodies** of a hand-written list, `WATCHED: [(&str, &str); 12]` — four
functions in `base_types.rs` and eight in `accept.rs`, all of them on the
memory-id path. The design is careful: bodies rather than files, because
`base_types.rs` carries legitimate clock reads; `SystemTime::now` without
parentheses, because `unwrap_or_else(SystemTime::now)` passes the function
itself; and `every_watched_function_still_exists` so a renamed entry cannot go
quiet.

Four id minters are not on it:

```
src/ingest/src/ingest_place.rs:356   document_id
src/ingest/src/ingest_place.rs:365   chunk_id
src/ingest/src/ingest_place.rs:403   chunk_source_id
src/math/src/math.rs:124             reason_id
```

All four are pure today. They carry the same requirement as the memory ids, and
`document_id`'s own doc comment states it: "Deterministic from `(source, text)`
alone, and nothing else — that is what `export`/`import` and `memory hub merge`
rest on." A clock read in any of them would make two stores disagree about the
id of the same document, which is the property the union in `absorb_graph`
depends on ([[a-merge-cannot-check-an-edge-s-endpoints]] is the same function
read from the edge side).

`ingest_place.rs` is also the case the gate's body-level design exists for: it
already reads a clock at `:79` for `created_at`, so a file-level check there
would be useless and a body-level one is exactly right.

Add the four to `WATCHED` and widen the array. The gate's own header makes the
argument for doing it — "a gate that lists only the spelling that caused the
last defect catches only the last defect" — and a hand-listed set of *functions*
has that same shape as a hand-listed set of spellings
([[a-gate-that-walks-cannot-fail-short]]).

**Done 2026-09-06.** `WATCHED` is sixteen: the twelve memory-id functions plus
`document_id`, `chunk_id`, `chunk_source_id` and `reason_id`. The doc comment
above the array now carries the reason the entity ids belong — `document_id`'s
own contract, that export, import and hub merge rest on determinism from
`(source, text)` alone — so the next reader does not have to reconstruct why a
file that legitimately reads a clock at `:79` is on a clock-reading gate.

**Proved red.** Inserting `std::time::SystemTime::now()` into `document_id`
fails with `src/ingest/src/ingest_place.rs::document_id reads SystemTime::now`;
removing it passes. Worth doing because the gate matches against a *body*
extracted by brace-matching, so a fixture that silently extracted nothing would
pass forever — the same failure `the_fixtures_actually_encode_something` guards
in the layout guard, and this gate has no equivalent.

## Check

`WATCHED` names all sixteen functions, `every_watched_function_still_exists`
passes, and inserting `SystemTime::now()` into `document_id` fails the gate.
`just test` green. All hold; suite 1,253 passed.
