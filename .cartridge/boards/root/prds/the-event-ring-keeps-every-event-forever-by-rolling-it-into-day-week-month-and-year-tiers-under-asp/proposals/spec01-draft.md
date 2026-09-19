---
complexity: 3
footprint:
  - src/transport/cartridge.rs
  - src/host/socket.rs
  - src/host/mod.rs
  - src/lib.rs
  - src/ring
  - src/asp/ring.rs
  - src/asp/own.rs
  - src/asp/ask.rs
  - src/asp/registry.rs
  - src/asp/expand.rs
  - src/asp/mod.rs
  - src/asp/README.md
  - docs/asp.txt
  - docs/transport.txt
  - .cartridge/help.md
  - .cartridge/tests/unit/src/asp/mod.rs
  - .cartridge/tests/unit/src/asp/ring.rs
  - .cartridge/tests/unit/src/ring
---

# spec01 — the base keeps every published event as an `event:`, folds it into day, week, month and year tiers, and answers all of them through ASP

Spec for `@root/the-event-ring-keeps-every-event-forever-by-rolling-it-into-day-week-month-and-year-tiers-under-asp`.
This is a **pre-draft**. The PRD cannot be claimed yet. It needs
`@runtime/a-listener-subscribes-to-event-types`, which cartridge-cc owns and
has not built.

Base: cartridge.ctg **`d04ab33`**. That was HEAD when this draft was finished.
The analysis started at `445a87f`, and HEAD moved one commit while it was
being written (`d04ab33`, "asp answers agents in compact lines"). That commit
touched `src/asp/expand.rs`, `src/asp/mod.rs` and `docs/asp.txt`. Every
citation below was re-read at `d04ab33`. Line numbers in
`src/transport/cartridge.rs` will move again when cartridge-cc's rows land.
The implementer has to re-take the base and re-read those lines before
cutting the lane.

## Dependency on cartridge-cc (hard; blocks the lane)

1. **`@runtime/a-listener-subscribes-to-event-types` must be collected.** That
   row adds the per-generation epoch to the channel and the envelope, in
   `publish_kind` and `join` (`src/transport/cartridge.rs:474-505` at
   `d04ab33`). This spec keys `event:` on `(channel, epoch, seq)` and reads
   the epoch inside `publish_kind`. The epoch's type and field name are
   cc's decision. This spec treats the epoch as an opaque scalar and renders
   it as a string.
2. **cartridge-cc must say that both of its rows are collected** before any
   edit to `src/transport/cartridge.rs`. This follows the ASP owner
   (cartridge-1f). The one exception is the tap in `publish_kind`, and the
   tap waits for cc as well. This analyst could identify only the first of
   cc's two rows from the board. A search of `prd.ctg` for `cartridge-cc` and
   `coordinator-41b7` finds only filing notes. **The coordinator has to
   confirm the second row by name with cc.**
3. The whole lane is cut after both rows. It is cut from a new base that
   contains them. It is never cut from `d04ab33`.

## Finding that changes the ASP owner's assumption

The owner's guidance places "a tap in `publish_kind`" as if the ring would
see it in process. That is not how the code runs. `publish_kind` runs in the
**publishing node's own process**. Every node constructs its own `Ctx`
(`src/node/mod.rs:114`), and the host's `Ctx` (`src/host/mod.rs:152`) only
carries what the base itself publishes. The base never sees a node's
envelopes unless a client `follow`s the channel (`src/host/socket.rs:500-534`).
`docs/transport.txt` says the same: "A channel belongs to the cartridge that
publishes it. The publisher keeps a bounded replay buffer."

The tap therefore has to **forward** a stripped entry from the node to the
host. The node already holds a host connection for `Ctx::host`
(`src/transport/cartridge.rs:341-352`). The host socket needs one new method,
`ring`, and that puts `src/host/socket.rs` in the footprint. A consequence:
cc's gap envelope is not consumed by the ring, because the ring is not a
subscriber. The ring consumes cc's **epoch** only. Its own lossy step, a full
tap queue in the node, is reported as a `dropped` count (step 6).

A second consequence: `emit`, `bail` and `gather` go node to node and never
reach a channel. The ring keeps only what is **published**, meaning `notify`
and `publish`. That is the event stream. A plain call is not an event.

## Decision: `event:` and `ring:` split

**This row defines both `event:` and `ring:`.** Both schemes are host-owned,
as the ASP rollup's coordinator decision says ("The host owns `event:` and
`ring:`"). The sibling
`every-declared-event-is-an-asp-type-and-every-published-envelope-an-event-entity`
is mostly covered by delivered work or by this row:

- Sibling box 1 (a declared event is an ASP type with its schema) **is
  already delivered.** `types` lists every declared event under `events`,
  with owner and schema (`docs/asp.txt`, "WHAT THE BASE CONTRIBUTES"). The
  proof is the test
  `asp::tests::base::the_base_contributes_every_tool_and_cartridge_and_lists_every_event_as_a_type`,
  landed in `a2c5962`.
- Sibling boxes 2 and 3 (expanding a `file:` returns the `event:` with its
  edge, and the identity survives a publisher restart through the epoch)
  are this spec's boxes 1, 3 and 6. The envelope reaches the host only
  through this row's tap, so no other row can deliver them without the
  same tap.
- Sibling box 4 (docs) is covered by step 9 here.

Recommendation: the coordinator marks the sibling `superseded-by` this row.
The alternative is to reduce it to a docs-only leaf that needs this row.
This is the smallest split: no new row, one row fewer, one tap, one owner of
`event:`. **JEV child 3** (`every-jev-decision-is-an-asp-entity-and-its-recorded-outcome-tunes-the-gate`)
already `needs` this row. It gets what it asks for:

- `jev.outcome` published with `entity: "decision:<id>"` is recorded by the
  tap.
- `expand decision:<id>` returns the ring's rows and `touched` edges about
  that decision, from every tier, through the entity index.

Its `decision:` entities are jev's own ASP scheme and do not need the ring.
Reading outcomes back does.

Optional cut, if the coordinator wants JEV unblocked before the tiers exist.
**Row A** is steps 1–3 and 5–9 with only the day tier: tap, live window, day
log, `event:`, entity index, `touched`, and spec boxes 1, 3, 6 and 8.
**Row B** is step 4: week, month and year roll-ups, the format fixture and
the disk measurement, which are spec boxes 2, 4, 5 and 7. B needs A. Both write
`src/ring/mod.rs` and `src/asp/ring.rs`, so they integrate serially. The
analyst recommends against the cut. B is about 250 lines, and a second
review round costs more than it saves. JEV child 3 also needs cc first
either way.

## Design (answers the brief)

**Where it lives.** It lives per project, never per user: under
`<descriptor>/.state/ring/`, where `<descriptor>` is the project's
`.cartridge` directory (`Host::descriptor`). There is one daemon per project
and the PRD says "under the project's state directory". `.state/` is already
ignored in this repository (`/Users/feb/dev/cartridge/.cartridge/.gitignore`),
and `cartridge setup` writes `/*` into a new project's `.cartridge/.gitignore`
(`src/cli/setup.rs:401-405`), so it is ignored there too. The directory is
created owner-only (0700), and its files are 0600.

**On-disk layout.** The layout uses format 1 and UTC calendar periods:

```
.state/ring/
  day/2026-09-19.jsonl   line 1 {"format":1,"tier":"day","period":"2026-09-19"}
                         then one entry per line, append-only:
                         {"channel","epoch","seq","agent","action","entity","revision","time"}
  week/2026-W38.json     {"format":1,"tier":"week","period":"2026-W38",
                          "folded":["day/2026-09-14",...],"rows":[Row...]}
  month/2026-09.json     same shape, tier "month"
  year/2026.json         same shape, tier "year"
```

A `Row` is `{agent, action, entity, channel, epoch, count, first_seq,
last_seq, first_time, last_time, first_revision, last_revision}`. A row is
keyed by `(agent, action, entity, channel, epoch)`. That is the PRD's
`(agent, action, entity id)` plus the channel and epoch that make a
sequence number meaningful. The index from entity id to rows is built in
memory at load and is never written to disk. It can be derived from the
rows, so a stored index could only ever disagree with them.

**What a ring entry holds.** The node's tap sends
`{channel, epoch, seq, agent?, session?, entity?, revision?, dropped?}`.
Every value is a string of 256 bytes or fewer, and **no `data`**. The host
stamps `time` (its own clock, unix seconds) and the publisher (from the
node's token, never from the node's claim). The channel becomes
`<publisher>.<local>`, the same name `cartridge follow` uses. The fields are
read as follows:

- `agent`: the payload's top-level `agent` if it is `scheme:key`. Otherwise
  `agent:<session>` if the payload has a top-level string `session`.
  Otherwise `cartridge:<publisher>`.
- `action`: the local channel name, meaning the event name for `notify`.
- `entity`: the payload's top-level `entity` if it is `scheme:key`,
  otherwise none.
- `revision`: the payload's top-level `revision` if it is a string of 128
  bytes or fewer in `[A-Za-z0-9._:/+-]`, otherwise none.

This is the convention a publisher follows so its events are indexed.
`docs/transport.txt` states it (step 9).

**Live window.** The host holds the newest 1024 entries in memory
(`VecDeque`, across all channels). It answers an `event:` in the window
exactly. Every entry is also **appended to the day log when it arrives**
(write-ahead). "Folded into the day" is therefore true of every entry from
the moment it is recorded. A restart loses at most a torn last line, which
the reader skips. It never loses the live window. This is stronger than the
PRD's promise and simpler: no batching, and no fold on stop.

**Roll-ups: how and when.** `roll(now)` runs at host start (in `Ring::open`)
and on every `record` whose entry falls on a later day than the newest day
log. It runs no timer. It cascades:

- a day log with `day < today(now)` is folded into its ISO week
- a week whose Sunday is before today is folded into the month of its
  Thursday. That is the ISO rule, so a week is never split. A row keeps its
  exact first and last time, so no answer lies about when.
- a month that has ended is folded into its year
- a year is never folded. It is the final tier.

Folding merges rows by key: `count` is summed, and first and last seq, time
and revision are taken as min and max by seq. The target is written to
`<file>.tmp` and renamed into place. The source is deleted only after the
rename. The target's `folded` list records every source it absorbed, and a
source already listed is deleted without being merged again. That makes a
crash between rename and delete idempotent. A target that cannot be read
(corrupt, or a `format` this build does not know) is **never overwritten**:
its sources stay where they are, and the failure is logged.

**Retention ("forever").** Nothing is deleted except a source whose rows a
readable target already holds. Every `(agent, action, entity, channel,
epoch)` that ever occurred keeps one row per period at its tier, forever.
What changes with age:

- *Kept*: who, what, which entity, the channel and epoch, the count, the
  first and last seq, time and revision.
- *Dropped*: the individual sequence numbers between first and last, the
  individual times, and every intermediate revision.
- *Never stored at all*: the payload.

**Bound on disk and time.**

- Disk: at steady state the ring holds one day log (about 250 bytes per
  event of that day), the current week and month files, and one file per
  year. Period files hold one row per distinct key in the period, at about
  500 bytes each. Total size ≈ Σ over years (distinct keys × 500 B) + today's
  events × 250 B. **It grows with distinct keys and years, never with the
  number of events.** The epoch is part of the key, so frequent publisher
  restarts multiply the rows. Box 6 measures this, and decision D3 is the
  lever.
- Memory: every loaded table is held in memory with its index, so memory
  has the same bound as disk.
- Time: `record` is one line append plus a hash-map row update, which is
  O(1). `roll` is O(rows of the period) and runs once per period boundary. A
  query is an index lookup per loaded table, and the answer is capped at 64
  rows, newest first. It is never a scan.

**Querying through ASP.** The query surface is the existing ASP ops only,
with no new op:

- `types`: `event` and `ring` are listed as schemes owned by `host`.
  `touched`, `records` and `holds` are listed as edges. The `host.*` ring
  attributes are listed as attributes.
- `expand event:<cartridge>.<channel>/<epoch>/<seq>`:
  - while the event is in the live window, the answer is one node
    `event:…` with the row attributes (`host.tier: "live"`, `host.count: 1`,
    first = last), plus `records` event → entity and `touched` agent → entity
  - after the event leaves the window, the answer is every row of the
    finest tier that covers it (same channel and epoch, `first_seq ≤ seq ≤
    last_seq`), each as a node `ring:<tier>/<period>/<rowid>` with the same
    attribute set and the same two edges

  `rowid` is the first 12 hex characters of the SHA-256 of the row key.
  `sha2` is already a dependency. The same row therefore keeps its id as it
  ages from tier to tier.
- `expand ring:<tier>/<period>` (for example `ring:day/2026-09-19` or
  `ring:live`): the period node plus its rows, with `holds` period → row.
  `expand ring:<tier>/<period>/<rowid>`: that row.
- `expand <any entity>` (a `file:`, a `decision:`, and so on): the rows that
  record the entity, from every tier, newest first, capped at 64. Also one
  `touched` edge per agent, agent → entity, with `revision` = the newest
  last revision. The count is on the row nodes (`host.count`). Decision D1
  covers whether it must also sit on the edge.

The attribute set is the same for every node, at every tier:
`host.tier, host.period, host.agent, host.action, host.entity, host.channel,
host.epoch, host.count, host.first_seq, host.last_seq, host.first_time,
host.last_time, host.first_revision, host.last_revision`. The names start
with `host.`, as `Declaration::problem` requires.

For "any entity" to work, the base has to be asked about every scheme. Today
`Registry::expanding` (`src/asp/registry.rs:55`) asks only the providers
that declare the scheme. The change: the base is always asked (a new
`Registry::asked(scheme)`, used at `src/asp/expand.rs:51`), while
`expanding` keeps guarding "no loaded cartridge declares the scheme"
(`src/asp/expand.rs:29`). The base answers in process, so this costs a hash
lookup. The ring's answer about a foreign entity holds only `ring:` and
`event:` nodes, which the base declares, and declared edges. Admission
(`src/asp/admit.rs`) accepts it unchanged.

**Keeping a secret out.** The guarantee is structural, and there is no
filter to maintain:

1. The tap sends only the named id fields (`agent`, `session`, `entity`,
   `revision`), each as a string of 256 bytes or fewer. The payload never
   leaves the publisher's process on the ring's behalf, so it never reaches
   a file.
2. An id that is not `scheme:key` (the scheme being lowercase letters,
   digits and `-`, as in `Declaration::problem`) is dropped. So is a
   revision outside its charset.
3. The files are 0600 in a 0700 directory.
4. Auth's rule ("no event carries a value") is the publisher's obligation,
   and the ring cannot tell an id from a value. A publisher that puts a
   secret into `entity` breaks that rule, and the ring would keep it.
   `jev.decided` omits state by design, and `jev.outcome` carries
   `decision:<id>` and `by`, which are ids.

There is no purge op. Deleting `.state/ring/` is the manual purge (decision
D5).

## Steps

Every step is written in the lane cut after cc's rows. The steps are ordered
so that each one compiles and keeps the existing suite green.

1. **`src/ring/calendar.rs`** (new): converts unix seconds to UTC day, ISO
   week, month and year, and back. It uses Hinnant's days-from-civil and
   civil-from-days in std only (no `chrono`, which is not a dependency). It
   also has "is this period finished at `now`" and "the month of a week (its
   Thursday)". It has unit tests in `.cartridge/tests/unit/src/ring/tests.rs`.
2. **`src/ring/tier.rs`** (new): `Entry`, `Row`, `Table { rows, index,
   folded }`. It aggregates an entry into a table and merges tables. It reads
   format 1: a day log is aggregated on load, a period file is read as it is,
   and any other `format` is refused by name. It writes a period file with
   tmp and rename.
3. **`src/ring/mod.rs`** (new): `Ring::open(dir, now)`, which loads every
   file, logs and keeps unreadable ones, and rolls. Also
   `record(publisher, entry, now)`, the live `VecDeque` of 1024, and the
   queries `event(channel, epoch, seq)`, `about(entity)` and
   `period(tier, period)`. Add `src/ring/README.md`, which says what the ring
   is, where it writes and its bound. Add `pub mod ring;` in `src/lib.rs`.
   Put the tests behind
   `#[cfg(test)] #[path = "../../.cartridge/tests/unit/src/ring/tests.rs"]`.
4. **`src/ring/roll.rs`** (new): `roll(now)`, the cascade, the `folded`
   ledger, and never overwriting an unreadable target.
5. **ASP provider.**
   - `src/asp/ring.rs` (new): `ring_types()`, the schemes, edges and
     attributes above, merged into `own_types()` in `src/asp/own.rs`. Also
     `ring_answer(&Ring, request) -> Value` for `expand`. It answers nothing
     for `search`.
   - `src/asp/ask.rs:20`: the base's answer becomes `own_answer` plus
     `ring_answer`, as concatenated nodes and edges.
   - `src/asp/registry.rs`: add `asked(scheme)` (the providers from
     `expanding`, plus the base).
   - `src/asp/expand.rs:51`: use `asked`.
   - `src/asp/mod.rs`: `mod ring;`.
   - `src/asp/README.md`: one sentence saying the base's ring is the one
     store below ASP.
6. **Host ingest.**
   - `src/host/mod.rs`: `Host` gains `ring: Mutex<Ring>`, opened in
     `Host::new` at `descriptor.join(".state/ring")`. A failure to open it is
     logged, and the host runs with an empty in-memory ring. The ring never
     stops the host.
   - `src/host/socket.rs`: `Caller::Cartridge` carries the id that
     `host.caller(token)` already returns (`:365`). A new method `ring` is
     granted to cartridges (`:438`). It records the entry under the
     authenticated publisher. A node can therefore only write its own
     channels.
7. **The tap** (cc-gated), in `src/transport/cartridge.rs`:
   - `State` gains a bounded `std::sync::mpsc::SyncSender<Value>` of 1024
     and a `dropped: AtomicU64`.
   - `set_directory` starts the pump once, and only when `directory.host` is
     `Some`. The pump runs in async context, forwards each entry with
     `self.host("ring", entry)` in order, and ignores errors.
   - `publish_kind` builds the stripped entry for `kind == "data"` only,
     after the channel lock is released. It calls `try_send`. When the queue
     is full it increments `dropped`, and the next entry carries `dropped`.
   - A `Ctx` without a host address (every transport unit test, and the
     base's own `Ctx`) does nothing.

   No `.await` and no runtime is needed at the call site. This matters
   because `publish` is reached from Lua without entering the runtime
   (`src/node/mod.rs:290-296`).
8. **Tests** (the names are the gate; see Verify):
   - `.cartridge/tests/unit/src/asp/ring.rs` (new, registered in
     `.cartridge/tests/unit/src/asp/mod.rs`). It uses an `emitter` fixture
     cartridge that declares `did` and a `burst` listener. The listener
     `notify`s `did` `n` times with
     `{entity = "file:src/a.rs", revision = "r"..i, token = "s3cret"}`, in
     calls of 100 if the Lua instruction budget refuses more.
   - `.cartridge/tests/unit/src/ring/tests.rs` (new), and the fixture
     `.cartridge/tests/unit/src/ring/fixtures/format-1/year/2025.json`,
     written by hand, frozen, with three rows including
     `event:fixture.did/1/7` in a row's seq range.
   - The test that crosses processes waits by polling
     `expand ring:live` until seq `n` appears (30 s deadline). It never
     sleeps a fixed time.
9. **Docs and help**, in the same change:
   - `docs/asp.txt`: the `event:` and `ring:` schemes, the ring's attributes
     and edges, and "the base is asked about every entity". Replace "ASP keeps
     no store" (`:12`) with "ASP keeps no store of what providers assert; the
     base's event ring is its own store". Leave the RANKING use-count
     sentence (`:139-140`) to the fabric child.
   - `docs/transport.txt`, STREAMS: published envelopes reach the base's
     ring as ids only (`agent`, `session`, `entity`, `revision`), never the
     payload.
   - `.cartridge/help.md`: one line under ASP.
10. **No manifest edit.** This is host code. No `cartridge.json` changes, so
    there is no trust prompt and no reload of a cartridge. Running it live
    needs the new host binary, which means `cartridge daemon --replace`. Per
    the house rule, **the daemon is not replaced without an explicit clear
    from every session**. That is a coordinator step after collect and is
    not part of Verify.

## Acceptance

- [ ] `asp::tests::ring::the_oldest_of_more_than_1024_published_events_is_answered_from_the_day_tier`:
      the emitter publishes 1100 `did` events through a real node. `expand
      event:emitter.did/<epoch>/1` returns a `ring:day/<today>/…` node with
      `host.agent = "cartridge:emitter"`, `host.action = "did"`,
      `host.entity = "file:src/a.rs"`, `host.first_revision = "r1"` and
      `host.first_seq ≤ 1 ≤ host.last_seq`. Seq 1100 is answered as
      `event:…` with `host.tier = "live"`.
- [ ] `asp::tests::ring::a_finished_day_rolls_into_its_week_and_the_week_into_its_month_with_the_same_row_shape`:
      1100 entries are recorded at 2026-09-16T12:00Z through
      `host.ring.record(…, t)`, and then:
      - after `roll(2026-09-17)`, the same `expand event:…/1` answers
        `ring:week/2026-W38/<rowid>`
      - after `roll(2026-09-21)`, it answers `ring:month/2026-09/<rowid>`
      - after `roll(2026-10-01)`, it answers `ring:year/2026/<rowid>`

      The attribute key set is identical each time and equal to the live
      node's, and `rowid` does not change.
- [ ] `asp::tests::ring::a_folded_event_is_still_answered_after_the_host_restarts`:
      publish 1100 events, then `host.stop()`. Then `Host::new` runs on the
      same directory and reconciles. `expand event:…/1` still returns the day
      row with the same `rowid` and count.
- [ ] `asp::tests::ring::a_tier_file_fixed_in_the_tree_at_format_1_answers_in_the_same_shape`:
      the fixture `year/2025.json` is copied into the ring directory before
      boot. `expand ring:year/2025` holds its three rows, and
      `expand event:fixture.did/1/7` answers the covering row with the same
      attribute key set as box 1.
- [ ] `ring::tests::a_tier_file_of_an_unknown_format_is_kept_and_never_overwritten`:
      a `week` file with `format: 99` survives `roll` byte for byte, and its
      day sources are not deleted.
- [ ] `asp::tests::ring::expanding_a_file_returns_the_ring_s_touched_edges_and_counts_beside_the_owner_s_facts`:
      the `files` fixture (owner of `file:`) and `emitter` are loaded, and 5
      events are published about `file:src/a.rs`. `expand file:src/a.rs`
      holds:
      - the `files` node, with `files.bytes`
      - a `touched` edge `cartridge:emitter → file:src/a.rs` with contributor
        `host`
      - a `ring:` row with `host.count = 5`
- [ ] `ring::tests::a_synthetic_year_of_100k_events_stays_within_its_disk_bound`:
      100 000 entries spread over 2025, with 4 agents × 50 entities × 4
      actions and one epoch per month, are recorded and rolled daily, then
      rolled at 2026-01-02. The test:
      - prints `ring: 100000 events, <rows> rows, <bytes> bytes`
      - asserts that only `year/2025.json` remains
      - asserts `bytes ≤ 600 × rows` and `rows ≤ distinct keys`
      - repeats the run with 200 000 events over the same keys and asserts
        that the row count is equal
- [ ] `asp::tests::ring::the_ring_keeps_no_payload_and_drops_what_is_not_an_id`:
      after the emitter publishes `{entity = "file:src/a.rs", token =
      "s3cret", agent = "not an id"}`, no file under the ring directory
      contains `s3cret`, and the row's agent falls back to
      `cartridge:emitter`.
- [ ] The existing ASP, ring and transport suites stay green, including the
      pinned names in the `test` block.

Spec boxes 1–4, 6 and 7 map to PRD boxes 1–6. Box 5 (unknown format) and
box 8 (payload) are this spec's own. They guard the two ways the ring could lose
or leak data, and the brief asks for both.

## Verify and Proof

```sh
rustfmt --edition 2021 --check src/ring/calendar.rs src/ring/tier.rs src/ring/roll.rs src/asp/ring.rs src/asp/own.rs src/asp/ask.rs src/asp/registry.rs src/asp/expand.rs .cartridge/tests/unit/src/asp/ring.rs .cartridge/tests/unit/src/ring/tests.rs
```

`rustfmt` is given leaf files only. `src/ring/mod.rs`, `src/asp/mod.rs`,
`src/host/*.rs` and `src/transport/cartridge.rs` declare child or test
modules, and `rustfmt` on those files would pull in files this change does
not own. The implementer runs `rustfmt` on exactly these files and on the
edited non-leaf files by hand. They never run bare `cargo fmt`.

```sh
test -f .cartridge/tests/unit/src/ring/fixtures/format-1/year/2025.json
if git ls-files --error-unmatch .cartridge/tests/unit/src/ring/fixtures/format-1/year/2025.json >/dev/null 2>&1; then :; else echo "the format-1 fixture is not tracked"; exit 1; fi
```

```test
run: export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/event-ring-verify}"; env -u CARTRIDGE_YOLO cargo test --lib -- --test-threads=1 asp:: ring:: transport::
pass: the_oldest_of_more_than_1024_published_events_is_answered_from_the_day_tier
pass: a_finished_day_rolls_into_its_week_and_the_week_into_its_month_with_the_same_row_shape
pass: a_folded_event_is_still_answered_after_the_host_restarts
pass: a_tier_file_fixed_in_the_tree_at_format_1_answers_in_the_same_shape
pass: a_tier_file_of_an_unknown_format_is_kept_and_never_overwritten
pass: expanding_a_file_returns_the_ring_s_touched_edges_and_counts_beside_the_owner_s_facts
pass: a_synthetic_year_of_100k_events_stays_within_its_disk_bound
pass: the_ring_keeps_no_payload_and_drops_what_is_not_an_id
pass: the_base_contributes_every_tool_and_cartridge_and_lists_every_event_as_a_type
pass: an_undeclared_edge_kind_refuses_the_provider_by_name
pass: a_fact_behind_the_owners_revision_is_marked_stale
pass: a_subscriber_gets_the_replay_and_then_live_events
```

libtest ORs its positional filters. `asp::` selects every ASP test,
including the new `asp::tests::ring::*`. `ring::` also matches
`ring::tests::*`. `transport::` selects the whole transport suite, which the
tap must leave green. The four existing names are pinned on purpose:

- `the_base_contributes_…` proves the base's answer is still correct now
  that it merges the ring.
- `an_undeclared_edge_kind_…` proves admission is unchanged.
- `a_fact_behind_the_owners_revision_…` proves staleness still holds when
  the base is asked about every scheme.
- `a_subscriber_gets_the_replay_…` proves a `Ctx` without a host address is
  unaffected by the tap.

`env -u CARTRIDGE_YOLO` keeps an inherited yolo flag from reddening the
trust tests. The target directory is private, so pass 2 never rebuilds a
live dylib.

Risk: a cold build plus these suites may approach the collect time limit.
The implementer measures the block cold at the lane base. If it runs over,
they record the time and split the `run:` into two `test` blocks, one for
`ring:: asp::tests::ring::` and one for the rest.

Post-integration proof, run by the coordinator from `/Users/feb/dev/cartridge`
and not in Verify, because the lane cannot reach the superproject's
justfile: `just isolation` must report nothing for `runtime`. The owner
gates do not run it. `just test runtime` and `just check runtime` must pass.
All of this runs under a quiet host (no daemon restart during the sweep).

## Evidence (source only; nothing was built or run)

These are read-only probes, with cwd `/Users/feb/dev/cartridge/cartridge.ctg`,
all exit 0:

- `git rev-parse HEAD` returned `445a87f` at the start and `d04ab33` at the
  end. `git diff --stat 445a87f d04ab33` shows 7 files, none of them in
  transport, host or ring.
- `git show d04ab33:src/transport/cartridge.rs`: `HISTORY = 1024` (`:23`),
  `publish_kind` (`:474-486`), `join` (`:488-505`), `Ctx::host`
  (`:341-352`).
- `git show d04ab33:src/node/mod.rs`: `Ctx::new` per node (`:114`), and
  `publish` from Lua without entering the runtime (`:290-296`).
- `git show d04ab33:src/host/socket.rs`: `Caller` (`:346`), the token to
  cartridge lookup that is discarded (`:365`), the grant list (`:438`), and
  `follow` (`:500-534`).
- `git show d04ab33:src/asp/{registry,expand,ask,own,admit,protocol}.rs`:
  scheme-gated asking (`registry.rs:55`, `expand.rs:29,51`), the base's
  in-process answer (`ask.rs:20`), and admission holding nodes, edges and
  attributes against the declaration.
- There is no `chrono` in `Cargo.toml`. `sha2` is present. Edition 2021.
- `.cartridge/.gitignore` ignores `.state/`.
  `git check-ignore .cartridge/ring/x` in the superproject reports nothing,
  which is why the ring goes under `.state/`.

Not verified: the epoch's final shape (cc has not built it). Whether 1100
`notify` calls fit one Lua call's instruction budget. How long the new
tests take.

## Decisions for the coordinator

- **D1: counts on the edge.** PRD box 5 says "touched edges with counts".
  ASP edges carry no attributes today (`Linked` and `Edge` in
  `src/asp/protocol.rs`). This spec puts the count on the ring's row nodes
  next to the `touched` edge, with no protocol change. If the box is read
  literally, edges gain optional `attributes`, held against the declaration
  like node attributes. That touches `protocol.rs`, `admit.rs`, `world.rs`
  and `docs/asp.txt`, which is cartridge-1f's protocol. Recommendation: no
  protocol change. Ask 1f if the reviewer reads the box literally.
- **D2: "older format".** No older format exists at landing. This spec pins
  a frozen format-1 fixture, a reader that dispatches on `format`, and a
  refusal of unknown formats that keeps the file. The test becomes the
  older-format test the day format 2 is written. The alternative, shipping
  format 2 at once so that format 1 is "older", invents history.
  Recommendation: accept the frozen fixture.
- **D3: the epoch in the row key.** Keeping the epoch makes `event:` lookup
  exact at every tier, forever, but rows multiply with publisher restarts.
  The alternative drops the epoch at the year tier, which makes year rows
  unaddressable by `event:`. Recommendation: keep it and read box 6's
  measurement.
- **D4: the sibling.** Mark
  `every-declared-event-is-an-asp-type-and-every-published-envelope-an-event-entity`
  `superseded-by` this row, or reduce it to docs. Recommendation:
  supersede. Its box 1 was delivered in `a2c5962`.
- **D5: purge.** The PRD asks for no forget or purge op, and this spec adds
  none. A secret that a publisher wrongly put into an id field stays until
  someone deletes `.state/ring/` by hand. Decide whether auth wants a
  `ring {op:"forget", entity}` as a follow-up PRD.
- **D6: cc's second row.** Name it with cartridge-cc before the lane is cut.
  Also confirm that the epoch is readable inside `publish_kind`.
- **D7: the cut.** One row (recommended), or Row A / Row B as described
  under "Optional cut".
- **D8: rollout.** After collect, running the ring live needs
  `cartridge daemon --replace`, and that needs an explicit clear from every
  session. There is no manifest edit, trust prompt or cartridge reload.
