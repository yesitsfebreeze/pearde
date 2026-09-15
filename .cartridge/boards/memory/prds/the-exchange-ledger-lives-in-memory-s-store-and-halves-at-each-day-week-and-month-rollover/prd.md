---
state: "done"
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge/memory.ctg"
capability-owner: memory
workflow: "develop-one-cartridge"
commit: "97af8ff9f2d277313081e160bf69e7f92096ab29"
---

# The exchange ledger lives in memory's store and halves at each day, week and month rollover

## Why

`.memory/ledger.jsonl` reached 21.15 GiB. It was written by `memory proxy`,
the standalone loopback forwarder from before the cartridge port, which appended
one `req`/`resp` row per exchange with the body as a JSON array of byte values
(about 4x the text size). Nothing ever rotated, capped or compacted it. The
port removed the proxy (last write 2026-09-09 16:51), so the file is orphaned
and nothing records exchanges today.

A "memory proxy" no longer makes sense: `proxy.ctg` is the system's proxy and
already calls memory for recall (`memo context prepare`, `proxy.ctg/src/service.rs`).
The ledger should be one more thing the proxy hands to memory, not a second
proxy inside memory.

## Outcome

Every exchange that passes through `proxy.ctg` reaches memory, which keeps it
in its LMDB store as a bounded ledger. There is one condense per unit: when a
unit rolls over, the records inside it are condensed by the reasoning model
into one record for that unit, at most half their combined size, and the inputs
are removed in the same write.

1. **Day.** A closed day condenses its raw exchanges.
2. **Week.** A closed week condenses its day records.
3. **Month.** A closed month condenses its week records.
4. **Year.** A closed year condenses its month records. Year is the top unit:
   year records are kept forever, with no retention cap. Pruning is manual.

Every boundary is UTC: a day closes at 00:00 UTC. Units nest strictly, so each
input belongs to exactly one parent. A week starts Monday and closes at the
next Monday 00:00 UTC **or at the month's end, whichever comes first**; a
calendar week that crosses a month boundary becomes two week records, one in
each month (Sep 28–30 closes with September, Oct 1–4 starts October).

Rollover runs only at the day boundary. At 00:00 UTC the day closes first; if
that midnight also ends a week, month or year, those close next, in that order,
each condensing what the step before it just wrote.

A size cap on the raw tier condenses the oldest raw rows early when the open
day grows past it, so the ledger stays bounded between rollovers. The cap is the
`ledger.raw_cap_bytes` cartridge setting, default 256 MiB.

## Shape

- **Capture.** `memory {op: "ledger", action: "append", ts, wire, user, response}`
  stores one exchange as a raw row. `user` is the newest user text of the
  request and `response` the assistant's output text, both plain strings.
  Full request bodies are not kept: every agent request resends the whole
  conversation, so the old ledger averaged about 1 MB per row (11,400 exchanges
  in four days, 2026-09-06..09) and no model can condense that. The proxy side is
  its own PRD, [@proxy/the-proxy-hands-each-finished-exchange-to-the-memory-ledger](../../../proxy/prds/the-proxy-hands-each-finished-exchange-to-the-memory-ledger/prd.md).
- **Store.** A named `ledger` database next to `memory`, `cold`, `cold_vec` and `meta`
  (`src/store/core/src/ledger.rs`), keyed `raw/<day>/<ts>-<n>`,
  `part/<day>/<ts>`, `day/<YYYY-MM-DD>`, `week/<YYYY-MM-DD>` (the week's first
  day inside its month), `month/<YYYY-MM>`, `year/<YYYY>`. Removing inputs and
  writing their condensate is one LMDB transaction.
- **Rollover.** `rpc::ledger` runs on a one-minute loop the engine spawns
  beside its maintenance tick. Condensing uses the `[reason]` model: inputs are
  packed into prompt-sized chunks, each chunk is condensed to at most half its
  size, and the results are condensed again until one record remains. A model
  answer that is empty or over half its input fails the whole rollover for that
  unit; nothing is written and the next pass retries.
- **Raw cap.** When the open day's raw rows pass `ledger.raw_cap_bytes`
  (cartridge setting, default 256 MiB), the oldest half of them is condensed
  into a `part/` row, which the day rollover takes as input with the rest.
- **Graph.** Each unit record is ingested through the existing synchronous
  ingest path with `source: "agent"` and `object_id: "ledger/<unit>/<key>"`.
  The graph mirrors the ledger: once the parent is ingested, each child's
  object id is removed with `forget_by_source`, so a closed week leaves one week
  in the graph and not seven days beside it. Raw and part rows never enter the
  graph. A record carries `ingested: false` until both steps succeed, and every
  pass retries the ones that have not.
- **Import.** `memory {op: "ledger", action: "import", path}` streams an old
  `ledger.jsonl` once. It accepts both historical row shapes (body as JSON or as
  a byte array; `ts` as Unix milliseconds or RFC 3339), pairs each `req` with the
  `resp` that follows it, extracts the newest user text and the assistant text
  (JSON or SSE), skips a user text identical to the previous exchange's, and
  appends raw rows in the day of their `ts`. It never deletes the source file.
## Acceptance

- [x] Ledger, store and config tests plus fmt and clippy of the touched crates
      green. `cargo nextest run --workspace` in the lane: 1403 passed and 3
      failed. The 3 failures are the base-integration tests in
      `.cartridge/tests/integration/cartridge.rs`, which fail identically on
      `main` at `b39f80b` because the temp project is untrusted.
- [x] With a stub model: closing a day writes one day record no larger than half
      the raw rows' bytes and removes those rows; same for week, month and year.
- [x] A calendar week crossing a month boundary yields two week records, and the
      closing month condenses only the one inside it.
- [x] With a failing stub model: rollover leaves every input row in place and
      a later tick with a working model condenses them.
- [x] A closed day is ingested under `ledger/day/<date>`; after its week closes,
      the week is ingested and the day's object id is forgotten; a failed ingest
      leaves the record marked and a later pass finishes it.
- [x] Crossing the raw cap mid-day condenses the oldest raw rows before the day
      closes.
- [x] Importing a fixture with both historical row shapes lands each exchange in
      the day of its `ts`, with the extracted user and assistant text.
