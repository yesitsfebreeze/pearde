---
complexity: mid
footprint: ["src/store/core/src/lib.rs","src/store/core/src/ledger.rs","src/config/src/config.rs","src/rpc/src/lib.rs","src/rpc/src/server.rs","src/rpc/src/ledger.rs","src/commands/src/memory.rs","src/cartridge/src/lib.rs","cartridge.json",".cartridge/tests/unit/src/rpc/src/ledger_tests.rs",".cartridge/tests/unit/src/store/core/src/ledger_test.rs",".cartridge/docs/ledger.md"]
---

# Memory keeps a bounded exchange ledger that condenses per UTC unit and mirrors into the graph

Baseline at memory.ctg `b39f80b`: no code writes or reads an exchange ledger;
`.memory/ledger.jsonl` (21.15 GiB, rows 2026-09-06..09) is orphaned from the
removed `memory proxy`. The store opens four named LMDB databases
(`MAX_DBS = 4`).

## Contract

- **Store.** `store_core` opens a fifth named database, `ledger`
  (`MAX_DBS = 5`). `ledger.rs` adds `ledger_put`, `ledger_scan(prefix)`,
  `ledger_sizes(prefix)` (keys and value lengths without copying values) and
  `ledger_commit(remove, put)`: one write transaction that aborts, writing
  nothing, when a key to remove is already gone. Values are JSON; the table has
  no format-version byte and graph load, flush and migration never read it.
  The store handle is the graph's own (`GraphGnn::store`), never a second open.
- **Config.** `config::Config.ledger: LedgerConfig { raw_cap_bytes }`, default
  `256 * 1024 * 1024`, declared as the `ledger` table setting in
  `cartridge.json`. Zero is refused by `validate`.
- **Op.** `memory {op: "ledger", action}` is admitted by the cartridge and
  dispatched by `Server::invoke`:
  - `append {ts, wire?, user, response}` stores
    `raw/<day>/<ts:013>-<content digest>`; empty `user` and `response` together
    are refused, and so is a `ts` below `10^12` (seconds) or whose UTC date is not
    a four-digit year. The
    digest makes a re-import a no-op while those rows are still uncondensed.
  - `import {path}` streams an old ledger as described in the PRD under the
    pass mutex (no rollover refolds days mid-import) and answers
    `{exchanges, skipped, days}`.
  - `rollover` runs one pass now; `status` answers rows and bytes per tier.
- **Record.** Unit rows are `{text, children, ingested}`: `children` are the
  graph object ids the record replaces, kept until the mirror succeeds. A unit
  consumed as an input passes on its own object id and every child it had not
  yet forgotten, so a week consumed by its month in the same pass still removes
  its days from the graph.
- **Pass.** `rpc::ledger::pass(store, today, cap, model, sink)` holds a
  process-wide mutex and is pure over its arguments: `model: &dyn Fn(&str) ->
  String` and a sink with `ingest(object_id, title, text)` and
  `forget(object_id)`. In order: cap the open day into `part/`; close every day
  before `today`; close weeks, then months, then years whose end is at or before
  `today`, stopping at the first tier where anything failed; mirror every record
  with `ingested: false`. Week start is `max(monday(d), first_of_month(d))`;
  week end is `min(next monday, first of next month)`. A unit's existing record
  is folded in as an input, so a late row never overwrites it. The condensate
  must be non-empty and at most half the input text bytes (separators between
  inputs excluded), checked per model call and on the final text, or the unit
  is left unchanged. A unit under 1 KiB, and any chunk carrying under 1 KiB of
  input (the tail of a large piece), is kept verbatim and packed into the next
  layer, so a small input cannot make a unit retry forever.
- **Mirror.** Forget the record's own object id, ingest it, forget each child,
  then mark it ingested. The production sink answers `committed` and `deduped`
  as ingested, `rejected` (the deterministic hygiene gate) as refused for good,
  which marks the record ingested and keeps its children in the graph, and
  anything else as a failure the next pass retries.
- **Engine.** `Engine::open` spawns a loop calling `Server::ledger_pass`
  directly (not through `invoke`, so it never counts as activity) every 60
  seconds, or every 900 after a pass with any failure. With an empty
  `reason_url` no model is passed and only pending mirrors run. The engine opens on first use, and the standalone
  daemon's server (`commands_serve`) runs no ledger loop.

## Acceptance

- [x] Day close with a stub model: one `day/` record at most half the raw bytes,
      every raw and part row of that day removed, sink ingests `ledger/day/<d>`.
- [x] Week, month and year close the same way over their children, and the sink
      forgets each child's object id after ingesting the parent, including days
      mirrored in earlier passes when their week, month and year close at once.
- [x] A week spanning Sep 28–Oct 4 yields `week/2026-09-28` and `week/2026-10-01`;
      closing September condenses only the first.
- [x] A model returning empty or over-half text leaves every input row, and a
      later pass with a working model condenses them; a sub-KiB tail chunk does
      not fail its unit.
- [x] A failing sink leaves the record `ingested: false`; the next pass ingests
      it and forgets its children. A rejected record keeps its children and is
      not retried.
- [x] Raw rows past the cap become one `part/` row before the day closes.
- [x] A late exchange for a closed day is folded into that day's record, and a
      commit whose input is already gone writes nothing.
- [x] Import of a fixture holding a byte-array row with millisecond `ts`, a JSON
      row with RFC 3339 `ts`, an SSE response and a repeated user text lands
      the expected raw rows in their days; a second import over uncondensed rows
      adds nothing, and a non-millisecond `ts` is refused.

## Verify

Blocks run in the lane or source tree they verify, against the shared target
directory so each stays inside the 120-second block limit.

```sh
set -eu
export CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target
cargo test -p rpc ledger
```

```sh
set -eu
export CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target
cargo test -p store_core ledger
cargo test -p config
```

```sh
set -eu
export CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target
cargo fmt --all -- --check
cargo clippy -p store_core -p config -p rpc -p commands -p memory_cartridge --all-targets -- -D warnings
```
