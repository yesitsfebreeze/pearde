---
complexity: mid
footprint:
  - src/cartridge/src/asp
  - src/cartridge/src/lib.rs
  - src/cartridge/src/source.rs
  - cartridge.json
  - init.lua
  - README.md
  - .cartridge/help.md
  - .cartridge/tests/integration/asp.rs
---

# spec01: memory answers ASP as the owner of the `memory:` scheme

## Base revision

`/Users/feb/dev/cartridge/memory.ctg` at `3432b13376017be921d745719e0626d6f0b5463c`
(clean working tree when this spec was written).

## Footprint notes

- **Widened by one path: `src/cartridge/src/source.rs`, visibility only.**
  The revision this row must share with `context.memory` is computed in
  `source::hydrate` (`source.rs:61-105`), and the private filter is
  `source::private` (`source.rs:25-30`). Search also needs
  `context.memory`'s nomination rules exactly, and those compare the encoded
  `source()` of each row (`source.rs:38-54,161-170`). All of these are private
  to `source`. The change makes `private`, `source`, `hydrate` and `ID_BYTES`
  `pub(crate)` and changes nothing else in the file. The alternative is a second copy of the projection
  rule inside `asp/`. Two copies of the rule could drift apart silently, and
  this row exists so that the two surfaces agree during the migration. When
  `the-context-path-is-deleted` removes `source.rs`, that row moves these
  functions into `asp/`. `source.rs` is not in the heat row's footprint.
- **Narrowed by one path: `src/cartridge/Cargo.toml` does not change.** Every
  crate the change uses is already a dependency: `serde_json`, `sha2` and
  `util`, with `tempfile`, `test_support`, `axum` and `futures` for the tests
  (`src/cartridge/Cargo.toml:12-28`).
- **Widened by `README.md` and `.cartridge/help.md`.** A cartridge's README
  and help page change with its surface, in the same change (system rule
  `cartridge-readme-stays-current`). The heat row also lists both files, but it
  is `open` and unclaimed, so waiting on it has no end. This change adds only
  ASP text: the `asp.memory` name in the README's two Events lists, and a new
  `## ASP` section in each file. It rewrites none of the sentences the heat row
  rewrites, which are the `context.memory` bullet under `## Use` in both files.
  **The heat row must rebase over these two files** once this row is
  collected: its edits to the `context.memory` bullet still apply, and the
  `## ASP` section needs no heat edit (see "Heat" below).
- **None of the heat row's other paths is touched:** `src/rpc/src/server.rs`,
  `src/retrieval/**`, `src/graph/src/heat.rs`, `src/config/src/config.rs`,
  `src/tick/**`, `.cartridge/tests/integration/bench/RESULTS.md` and that
  row's unit tests. This spec only reads them as evidence.
- **The test path is the one the PRD names.** A reviewer suggested
  `.cartridge/tests/unit/src/cartridge/asp.rs`, which matches the crate's
  other `#[path]` tests. That path is outside the frontmatter footprint. The
  file is mounted the same way either way, and moving it is a one-line
  follow-up if the coordinator prefers it.

## What is true today

- **The provider being replaced.** `context.memory` sends one text query,
  `{op:"query", text, k: max_rows}` (`source.rs:129`). It then reads each
  nominee back by id with `{op:"get", id, compact:true, edge_limit:1}`
  (`source.rs:107-108,188`). The `memory` service rewrites `get` to `query`
  with `id` (`lib.rs:182-190`), which is served by `Server::query_by_id`
  (`src/rpc/src/server.rs:569`, reached from `tool_query` at `:696`).
- **Filtering on the query rows** (`source.rs:145-181`):
  - Private rows are dropped before anything else, and they are the only
    rows that do not count toward the limit. `position` enumerates every
    non-private row, and the loop stops when `position >= max_rows`
    (`:145-149`). So a superseded, inactive, id-less or malformed row uses up
    a slot. `private` checks `private`, `visibility`, `source.private` and
    `source.visibility` (`:25-30`).
  - `status:"superseded"` rows are skipped (`:150`).
  - Rows without a bounded id, with a status other than `active`, or with a
    malformed source are skipped (`:153-164`).
  - When one id appears twice with different sources, the id is dropped
    (`:165-170,185`).
- **Filtering on the readback.** `hydrate` refuses private and
  `expired:true` rows (`:62-63`). It refuses an id other than the one asked
  for (`:68-70`). It also refuses a malformed source, text over 8192 bytes, a
  missing `text_truncated` and `compact` other than `true` (`:71-78`).
- **The revision.** It is the SHA-256 of
  `["memory-observed-projection/v1", id, source, text, truncated]`, where
  `source` is the JSON of the four bounded fields `scheme`, `object_id`,
  `section` and `url` (`:38-54,79-83`).
- **The context event is wired** in `lib.rs:524-531` (`context_event`),
  `lib.rs:576` (`module.set("context", ...)`), `init.lua:5` and
  `cartridge.json:92,114`. The manifest has no `asp` block, and no `asp.*`
  event is declared or listened to (`jq '.events|keys' cartridge.json` gives
  `context.memory`, `memory` and `tool.memory`).
- **A ranked row and a compact readback carry the same text and source.**
  - A ranked row's text is `truncate(entity.text(), 500)`, and it carries
    `id`, `source`, `status` and `valid_until` (`id_detail.rs:172-198`).
  - The compact readback's text is `truncate(text, COMPACT_TEXT)` with
    `COMPACT_TEXT = 500`. The code documents this as "so compact and ranked
    agree" (`id_detail.rs:33-35,120-125`).
  - `util::truncate` cuts at 500 characters and appends `...`
    (`src/util/src/util.rs:61-66`). So a truncated text is exactly 503
    characters, and an untruncated one is at most 500. `truncated` is
    therefore `chars > 500` on either path.
  - This was measured on the real engine at base. For a fact of about 930
    characters, the ranked row and the `ids` readback both had 503-character
    texts that compared equal, the sources compared equal, and
    `text_truncated` was `true`.
- **The by-id paths.**
  - `{op:"query", ids:[...]}` is served by `query_by_ids`
    (`server.rs:547-566`, reached at `:692`). It answers
    `{results, missing}` with the same `detail_with` rows as `get`.
  - Measured: `ids:["nope"]` answers `{"missing":["nope"],"results":[]}`.
  - An 8-character prefix resolves to the full id. So a prefix key comes back
    with an id different from the key.
  - `get` on an unknown id is an error string instead (`"thought not found:
    <id>"`, `server.rs:1655-1664`).
- **Heat today.**
  - The text-query path enqueues `task_commit_access` on every id it delivers
    (`server.rs:721` on a cache hit, `:764` otherwise). That stamps order and
    count and deposits access heat.
  - `query_by_id` and `query_by_ids` enqueue nothing.
  - `tool.memory` `query` sends `{op:"query", text, k?}` (`lib.rs:266-268,277`)
    and reaches that same text-query path.
- **Heat under the heat row, as far as it is settled.**
  - `@memory/heat-is-deposited-on-read-back-not-on-delivery` is `open`,
    unclaimed, and has no passing spec. Its PRD Decision after review round 1
    overruled its spec's Mechanism 6: the `tool.memory` `query` path "keeps
    depositing until the agent surface has a read-back of its own".
  - Its Outcome deposits heat when a reference is read back by id.
  - A text query with no distinguishing field cannot be told apart from
    `tool.memory` `query`. So whatever that row decides for `tool.memory`
    `query`, it decides for any other text query too.
- **The ranked path drops expired rows** (`retrieval_query.rs:399`,
  `score::drop_expired`). But the result cache at `server.rs:713-723` is keyed
  on the mutation epoch, not on time. So a cached reply can still carry a row
  whose `valid_until` has passed since it was cached.
- **ASP.**
  - The host sends `{op:"expand", entity}` and `{op:"search", query, limit}`.
  - It refuses a provider's whole answer over an undeclared scheme, attribute
    or edge kind (`cartridge.ctg/src/asp/admit.rs:14-60`).
  - It takes the owner's revision only from a node whose id equals the
    expanded entity exactly (`cartridge.ctg/src/asp/expand.rs:51-56`).
  - Search never calls expand (`cartridge.ctg/src/asp/search.rs:17-80`).
  - The `asp` block needs exactly one `asp.<name>` in `listen`, and each
    attribute must be prefixed with the cartridge name
    (`cartridge.ctg/src/asp/protocol.rs:83-130`).
- **How the tests are wired.**
  - The integration tests under `.cartridge/tests/integration/` are
    `[[test]]` targets of the root `memory` package (`Cargo.toml:64,81-228`,
    `autotests = false`). That package cannot link `memory_cartridge`, which
    is `crate-type = ["cdylib"]` only (`src/cartridge/Cargo.toml:9-10`).
  - The cartridge crate mounts its tests with `#[cfg(test)] #[path = ...]`
    (`source.rs:312-314`, `lib.rs:581-586`).
  - Tests that need a store open the real engine in process over a temporary
    directory, with a fake embedder from `test_support`. They do this because
    the base's sandbox denies the LMDB semaphores
    (`.cartridge/tests/unit/src/cartridge/engine_test.rs:1-4,38-51`).
  - `fs.ctg/src/asp/mod.rs:56-58` mounts its ASP tests the same way, and
    `fs.ctg/.cartridge/tests/unit/asp.rs:24-46` holds every answer against the
    shipped block.

## Design decisions

- **The scheme.** It is `memory`, and memory owns it (`owner: true`). The key
  is the full entity id exactly as the engine prints it. An `id` from
  `tool.memory` or `memory query` is already an ASP key. Memory does not
  respell keys. A prefix answers null, not the full id. The reason is that the
  host takes the owner's revision only from a node whose id equals the
  expanded entity, so a respelled node would carry no canonical revision.
- **What expand calls: the by-id read** `{op:"query", ids:[key], compact:true,
  edge_limit:1}`.
  - Expand is an agent asking about one entity it already holds a reference
    to, so it uses the engine's read by reference.
  - `ids` is used rather than `get` because its `{results, missing}` answer
    separates "no such entity" (null) from an engine failure (an error). That
    needs no matching on the `thought not found:` string. Both requests reach
    the same `detail_with` row, so the revision is the same as with `get`.
  - `edge_limit:1` is `context.memory`'s own value. `0` would mean every edge
    (`server.rs:499-502`).
- **What search calls: the text query** `{op:"query", text, k}`, and nothing
  after it.
  - One engine call per search. A `get` per hit, as `context.memory` does,
    would cost one more call per hit, and it would turn every search into a
    read by reference of every hit.
- **Heat: this row makes no heat claim, and adds no heat marker.** What each
  path deposits is whatever the engine does for that request:

  | Path | Request | Today (base) | Under the heat row's Outcome and Decision |
  |---|---|---|---|
  | search | `{op:"query", text, k}` | `task_commit_access` on every delivered row: order, count and access heat (`server.rs:721,764`) | Whatever the heat row settles for `tool.memory` `query`, which it has said "keeps depositing". The two requests are the same shape, so they deposit the same. |
  | expand | `{op:"query", ids:[key], ...}` | Nothing (`server.rs:547-566`) | The read-back deposit on that one fact, the same as `get` |

  - The host sends every ASP search to every search provider
    (`cartridge.ctg` `src/asp/search.rs:23-29`). So until the heat row
    decides otherwise, **an ASP search for anything warms up to `limit`
    memory rows**, just as a `tool.memory` query does today.
  - A marker field, such as `"delivery":"asp"` on the search request, was
    considered and left out. It is the smaller-looking change, but no code
    reads it. Its meaning would be a contract only the heat row can define,
    in `server.rs`, which is in that row's footprint. An unread field that
    looks like a promise is worse than an honest table.
  - If the heat row wants ASP search to deposit nothing while
    `tool.memory` `query` keeps depositing, that row adds the field to both
    the engine rule and `asp/search.rs`. This row adds no other contract that
    field would have to fit, and the request assertion in
    `search_delivers_ranked_rows_without_reading_any_back` is the one line
    that would change.
- **The revision.** It is the same observed-projection revision on both
  paths, computed by the one function `source::hydrate`.
  - Expand hydrates the compact readback row.
  - Search hydrates the ranked row, completed to the compact shape:
    `compact: true`, `text_truncated: text.chars().count() > 500` and
    `expired: valid_until < now`.
  - This is sound because the ranked and compact texts are the same
    `truncate(_, 500)` (see What is true today). A named test on the real
    engine pins it with a truncated fact.
  - A search node therefore carries the revision that `context.memory` and
    expand compute for the same entity.
- **The filters: search follows `context.memory`'s nomination loop
  (`source.rs:140-185`) step for step, minus the byte cap.** ASP bounds by
  node count, not by bytes.
  1. Walk the reply's `entities` in order, skipping private rows
     (`source::private`). Enumerate the rest as `position`.
  2. At `position >= limit`, stop. Every non-private row uses up a slot,
     filtered or not. Only private rows are free.
  3. Skip `status == "superseded"`, a missing or oversized id,
     `status != "active"`, and a source for which `source::source` fails.
  4. If an id is already nominated, mark it conflicting when the encoded
     source differs, then skip. A twin past the stop point is never seen, as
     in `context.memory`.
  5. After the loop, drop the conflicting nominations. Then hydrate each
     remaining row, completed to the compact shape, with
     `source::hydrate(row, id)`. Any `Err` drops the row, which covers
     private, expired and malformed text.
  - The engine is asked for `k: limit`. So private and filtered rows also
    take engine slots, and a bank dense with private facts answers fewer
    than `limit` nodes. This is the same as `context.memory`
    (`source.rs:129`).
  - The expiry check through `hydrate` is not redundant. A cached ranked
    reply can outlive a row's `valid_until`.
- **Expand keeps `context.memory` `read`'s rules exactly:**
  - a private or expired readback answers null;
  - an id other than the key (a prefix) answers null;
  - a malformed row is an error, so the host reports memory `unavailable`
    rather than "absent".
  - The id path serves superseded rows by design (`id_detail.rs:147-152`), as
    `read` does today. Its compact row carries no status, so expand cannot
    filter them without a change to `src/retrieval/**`.
- **Inputs that can never name anything answer null, not an error.** An
  error is reported as memory being `unavailable`. This covers a key that is
  empty, longer than 512 bytes or contains NUL, a query that is empty after
  trimming, and a query over 4096 bytes or with NUL. The engine is not called
  for any of them.
- **The host re-ranks.** `rank::rank` in `cartridge.ctg` orders the merged
  nodes by word overlap with `name`, `id`, `tags` and `description`. So a
  fact that matched semantically but shares no word with the query falls
  below every lexical hit from other providers. `the-prompt-recall-and-the-proxy-read-asp-search`
  inherits that ranking. This row passes the engine's order through and
  changes nothing about it.
- **What a node carries.**
  - `id`: `memory:<id>`.
  - `revision`: as above.
  - `name`: the first line of the text, cut with `util::truncate` at 80
    characters.
  - `description`: the compact text, cut with `util::truncate` at 500
    characters. This is at most 503 characters. On the engine's own output it
    is a no-op, and it bounds anything an attached owner sends.
  - `tags`: `[source.scheme]`, which is present and non-empty on both paths.
    The entity kind is a label on ranked rows and a `u8` on compact rows, so
    it is left out.
  - `attributes`:
    - `memory.source`: the bounded source object, parsed back from the
      evidence's source JSON;
    - `memory.truncated`: whether the text was cut.
- **No edges.**
  - The compact row's `edges` are reasons. Their ends can be private or
    expired entities.
  - Filtering them needs one by-id read per end. That costs one engine call
    each, and after the heat row it would deposit read-back heat on entities
    nobody asked about.
  - Without that filtering, the ids of private rows would leak.
  - The entity graph does not give edges cheaply, so none are declared.
- **No actions.**
  - `tool.memory`'s input is `{op: query|ingest, text, k, raw}`
    (`cartridge.json`, `events."tool.memory".schema.properties.input`). It has
    no read by id. So no `args` template can name one entity: `${key}` is an
    id, not query text.
  - A by-id op on the tool would change the model's own surface, and its heat
    is the heat row's carve-out.
  - Expand already returns the entity's text.

## Change

1. `src/cartridge/src/source.rs`: `fn private`, `fn source`, `fn hydrate` and
   `const ID_BYTES` become `pub(crate)`. Nothing else in the file changes.
2. `src/cartridge/src/asp/mod.rs` is the `asp.memory` service.
   - Its `//!` header states the scheme, the key and the revision. It says
     that search is one text query and expand is one read by id, and it makes
     no claim about heat.
   - No comment in `asp/` cites a path outside memory.ctg, such as
     `cartridge.ctg/...`. The root `cited_paths` gate treats a tree the
     repository does not have as rot, and Verify does not run that gate.
   - It defines `pub(crate) async fn native<F, Fut>(request: Value, call: F)
     -> Result<Value, String>`, with the same `call` shape as
     `source::native`.
   - The request is `{op, entity?, query?, limit?}`. An unparseable request
     is `Err("invalid asp.memory request")`.
   - `expand` calls `expand::expand`, and `search` calls `search::search`.
     Any other op is `Err("unknown asp.memory op")`.
   - `LIMIT = 256` is the ASP node ceiling. It is the default when `limit`
     is absent, and it caps any larger limit.
   - It ends with `#[cfg(test)] #[path =
     "../../../../.cartridge/tests/integration/asp.rs"] mod tests;`.
3. `src/cartridge/src/asp/node.rs` holds the node.
   - `NAME_CHARS = 80` and `DESCRIPTION_CHARS = 500`.
   - `pub(super) fn node(evidence: &Evidence, scheme: &str, truncated: bool)
     -> Value` builds the node described above from a hydrated `Evidence`.
     The id and revision come from `evidence.reference`, and `memory.source`
     from `serde_json::from_str(&evidence.source)`.
4. `src/cartridge/src/asp/expand.rs` answers an entity.
   - An entity that is not `memory:` answers `Null`.
   - A key that is empty, longer than `ID_BYTES` or contains NUL answers
     `Null` without calling the engine.
   - Otherwise it makes exactly one call:
     `{op:"query", ids:[key], compact:true, edge_limit:1}`.
     - An engine `Err` is passed through as the error.
     - A reply without a `results` array is `Err("malformed memory reply")`.
     - An empty `results` answers `Null`.
   - The row is then checked:
     - `source::private` → `Null`;
     - `hydrate(row, key)` returning `Unavailable` (private or expired) or
       `Changed` (a respelled prefix) → `Null`;
     - `Malformed` → `Err("malformed memory row")`;
     - `Ok(evidence)` → `{"nodes":[node(...)]}`, with `truncated` taken from
       the row's `text_truncated`.
5. `src/cartridge/src/asp/search.rs` answers a query.
   - A query that is empty after trimming, over 4096 bytes or containing NUL
     answers `Null` without a call. 4096 bytes is `contribute`'s bound
     (`source.rs:125`).
   - Otherwise it makes exactly one call: `{op:"query", text: query, k:
     limit}`. The request has exactly these three fields, and no by-id read
     follows.
     - An engine `Err` is passed through.
     - A reply without an `entities` array is `Err("malformed memory reply")`.
   - The rows then go through the five-step nomination loop under "The
     filters" in Design decisions: `context.memory`'s loop, minus the byte
     cap. The loop stops at `position >= limit`, where `position` counts
     every non-private row.
   - Each surviving row is extended with `compact:true`,
     `text_truncated: chars(text) > COMPACT_TEXT` (with `COMPACT_TEXT = 500`)
     and `expired: valid_until` (seconds) `< now`. It is then passed through
     `source::hydrate(row, id)`. Any `Err` drops the row.
   - An empty result answers `Null`. Otherwise it answers `{"nodes": [...]}`
     in nomination order, with no `edges` key.
   - A `ponytail:` comment on `COMPACT_TEXT` says it mirrors the engine's
     compact window of 500 characters, and names
     `search_and_expand_agree_with_context_memory_on_a_real_bank` as the test
     that fails if the two part.
6. `src/cartridge/src/lib.rs`:
   - `mod asp;`.
   - An `asp_event` shaped like `context_event` (`:524-531`), calling
     `asp::native(request, |args| memory(s.cfg.clone(), s.status.clone(),
     args))`.
   - `module.set("asp", lua.create_function(asp_event)?)?`.
   - The `//!` header's list of wired events (`:2-3`) gains `asp.memory`.
7. `init.lua`: add `cartridge.listen("asp.memory", memory.asp)` after the
   `context.memory` line.
8. `cartridge.json`:
   - `listen` gains `"asp.memory"`.
   - `events` gains `"asp.memory"`:
     - Description: `ASP provider for the memory scheme: {op: expand, entity}
       answers one memory:<id> node read back by id with its
       observed-projection revision; {op: search, query, limit} answers the
       memory nodes of one text query. Answers {nodes} or nil.`
     - `"timeout_ms": 30000`. A search embeds its query over HTTP, and a
       caller cannot cancel a cartridge call. This is the attached reader's own
       default bound (`lib.rs:70-73`), and `lsp` declares the same field on its
       ASP event.
     - The schema is the `asp.fs` shape: `type: object`, `required: ["op"]`,
       `op` an enum of `expand` and `search`, `entity` and `query` strings,
       and `limit` an integer of at least 1.
   - A top-level `asp` block:
     ```json
     "asp": {
       "schemes": {
         "memory": {
           "description": "A fact in the memory bank; the key is its full entity id as the engine prints it and the revision the SHA-256 of its observed projection (id, source, compact text, truncated).",
           "owner": true
         }
       },
       "attributes": {
         "memory.source": { "description": "The fact's provenance: scheme, object_id, section and url, each bounded." },
         "memory.truncated": { "description": "Whether the description is the engine's 500-character cut of a longer fact." }
       },
       "search": true
     }
     ```
     It has no `edges` and no `actions`, for the reasons in Design decisions.
9. `README.md` and `.cartridge/help.md` get the text under "Documentation"
   below, word for word, and nothing else.
10. `.cartridge/tests/integration/asp.rs` is new and mounted by step 2.
    - It holds a `held_to_the_declaration(&Value)` helper that parses
      `crate::DOCUMENT` and asserts three things for each answer:
      - every node's scheme is in `asp.schemes`;
      - every attribute is in `asp.attributes`;
      - every edge kind is in `asp.edges`. Since none are declared, any edge
        fails.
    - Every test routes each non-error answer through this helper, the way
      `fs.ctg/.cartridge/tests/unit/asp.rs:24-46` does.
    - A fake `call` records every request and pops scripted replies. This is
      the fixture shape of `.cartridge/tests/unit/src/cartridge/source.rs:19-33`.
    - The tests:
    - `a_memory_entity_expands_to_its_node_with_the_observed_projection_revision`:
      one scripted `ids` reply with a two-line text.
      - The answer equals the exact node JSON.
      - Its revision equals a SHA-256 the test computes itself over
        `["memory-observed-projection/v1", id, source_json, text, false]`.
        It does not call `hydrate` to get it.
      - The recorded requests are exactly
        `[{op:"query", ids:[id], compact:true, edge_limit:1}]`, so there is no
        text query.
      - `name` is the first line.
    - `expand_answers_nothing_for_a_missing_private_expired_or_respelled_key`:
      - `Null`, with one request recorded, for each of:
        - `missing` (an empty `results`);
        - a readback marked `visibility:"private"`;
        - `expired:true`;
        - a row whose id is longer than the prefix key asked for.
      - `Null`, with no request recorded, for:
        - a 513-byte key;
        - a key containing NUL;
        - an entity of another scheme.
      - `Err` for an engine error and for a row without `compact`.
    - `search_delivers_ranked_rows_without_reading_any_back`:
      - Three active rows produce three nodes in the engine's order.
      - The recorded requests are exactly
        `[{"op":"query","text":<query>,"k":<limit>}]`, compared as whole JSON
        values. So an extra field or a by-id read fails the test.
      - `limit: 2` gives two nodes and `k: 2`.
      - An empty query and a 4097-byte query each record no request and
        answer `Null`.
    - `search_keeps_the_context_filtering_exactly`, with three scripted
      replies:
      - Reply A holds, in order:
        - a private row, a `visibility:"private"` row and a
          `source.private:true` row;
        - a `superseded` row and a `pending` row;
        - a row whose `valid_until` is in the past;
        - a row without an id and a row with an empty source scheme;
        - two rows of id `twin` with different sources;
        - one `good` row.

        With `limit: 256`, the only node is `good`.
      - Reply B is three private rows and then `good`. With `limit: 1`,
        `good` comes back, because private rows are free.
      - Reply C is one `superseded` row and then `good`. With `limit: 1`,
        the answer is `Null`, because the superseded row used up the slot,
        as it does in `context.memory` (`source.rs:145-150`).
    - `search_and_expand_agree_with_context_memory_on_a_real_bank`:
      - It opens the real engine in process over a `tempfile` dir with
        `test_support::fixed_vec_embed_app`. The settings JSON is
        `engine_test.rs:38-40`'s, built locally because that helper is
        private to its module.
      - It keeps `tick.interval_secs: 0` and `queue.enabled: false`. The test
        leaves its engine open without `drain`, which is safe only with no
        tick and no queue threads. A comment says so.
      - It ingests one fact of more than 500 characters with `raw:true,
        sync:true`. It is one fact because a fixed vector dedupes a second.
      - It makes three calls through the real `memory` service: ASP
        `search`, ASP `expand` of the id search returned, and
        `source::native({op:"contribute", ...})`.
      - The three revisions are equal.
      - `description` has 503 characters and ends in `...`, and
        `memory.truncated` is `true`.
    - `the_shipped_declaration_is_one_the_host_accepts` checks the shipped
      manifest and `init.lua`:
      - `listen` holds exactly one `asp.*` entry, and it is `asp.memory`.
      - `events."asp.memory"` has a non-empty description,
        `timeout_ms: 30000` and a schema whose `op` enum is
        `["expand","search"]`.
      - The `asp` object's keys are a subset of `{schemes, edges, attributes,
        actions, search}`. The host parses the block with
        `deny_unknown_fields`.
      - Each scheme's keys are a subset of `{description, owner}`, and each
        scheme name is lowercase letters, digits and `-`.
      - `asp.schemes.memory.owner` is `true`.
      - Every attribute key starts with `memory.`.
      - `asp.edges` and `asp.actions` are absent or empty, and `asp.search`
        is `true`.
      - `init.lua` contains `cartridge.listen("asp.memory", memory.asp)`.

## Documentation

The system rule is that a surface change updates `README.md` and
`.cartridge/help.md` in the same change, so this text lands with this row.

It touches no sentence the heat row rewrites, and it makes no heat claim.
**The heat row must rebase over both files** after this row is collected. Its
`context.memory` bullet edits apply unchanged beside the new section.

In `README.md`, under `## Events`, replace lines 9 and 10 (em dashes as in the
file):

```
- **Defines** — `memory`, `tool.memory`, `context.memory`, `asp.memory`
- **Listens to** — `memory`, `tool.memory`, `context.memory`, `asp.memory`
```

In both files, insert this section directly before the next `## ` heading
after `## Use`. In `README.md` that heading is `## In this composition`, and
in `.cartridge/help.md` it is `## Read next`.

```
## ASP

`asp.memory` is memory's answer to ASP. memory owns the `memory:` scheme, and
a key is a fact's full entity id as the engine prints it, so an id from
`tool.memory` is already an entity; a shortened id names nothing.

- `{op:"expand", entity}` reads that one fact back by id and answers its node:
  the first line of the fact as `name`, its compact text (at most 500
  characters, then `...`) as `description`, its source scheme as a tag, and
  the `memory.source` and `memory.truncated` attributes. Its revision is the
  observed-projection revision `context.memory` reports for the same fact.
- `{op:"search", query, limit}` runs one text query, the same request
  `tool.memory` sends, and answers the matching facts as nodes with the same
  revision. It reads nothing back, and the engine records the access exactly
  as it records a `tool.memory` query.
- Private and expired facts never appear. Search also leaves out superseded
  and inactive facts. Expand serves a superseded fact, because an id names one
  fact on purpose.
- No edges and no actions are declared.
```

## Acceptance

- [x] `a_memory_entity_expands_to_its_node_with_the_observed_projection_revision`:
      expand makes one by-id read and answers the node with the projection
      revision.
- [x] `expand_answers_nothing_for_a_missing_private_expired_or_respelled_key`:
      absent, private, expired, prefix and impossible keys answer nothing. The
      impossible keys reach no engine, and engine faults are errors.
- [x] `search_delivers_ranked_rows_without_reading_any_back`: search sends
      exactly one `{op, text, k}` request and never a by-id read.
- [x] `search_keeps_the_context_filtering_exactly`: private, superseded,
      inactive, expired, malformed and conflicting rows never become nodes.
      Only private rows are free of the limit, as in `context.memory`.
- [x] `search_and_expand_agree_with_context_memory_on_a_real_bank`: search,
      expand and `context.memory` report one revision for one truncated fact
      on the real engine.
- [x] `the_shipped_declaration_is_one_the_host_accepts`: the `asp` block has
      only keys the host parses, and the `asp.memory` event and the `init.lua`
      listener are as specified.
- [x] `README.md` and `.cartridge/help.md` carry the Documentation text, and
      neither file's `context.memory` bullet changes.
- [x] The existing cartridge-crate tests still pass, `context.memory`'s among
      them.
- [x] No other path reserved by the heat row is changed. This is held by the
      footprint, which names none of them. A `git status` guard in Verify
      would fail falsely in collect's second pass, whenever another session
      has those paths dirty in the shared checkout.

## Verify

Only `memory_cartridge` is tested, in two separate commands. `rpc` and
`retrieval-piece` are built as dependencies and never tested here. Their
timing tests flake under load, even at base.

The ASP tests run apart from the engine tests. The engine tests' `drain` flips
the process-wide shutdown latch, and a real-engine ASP test running beside it
would be refused.

Timing: 46.7 s cold here, and about 60 s cold as the reviewer measured it.
Both are inside the 120 s limit. It is about 1 s warm. The block fails at base
as it must: first on `test -f`, and with the file present, on the first
missing test name.

Documentation is checked with one fixed-string grep per file, for the
`## ASP` heading. Wording is the reviewer's to check against "Documentation"
above.

**What this block cannot prove.** It checks that each named test ran and
passed, not that the test asserts what its name says. An empty test body
passes it too. No mutant run is added: a mutant is a second full build of the
crate in a copy, which would not fit next to this block in 120 s.

The check is the diff reviewer. They confirm that each named test holds the
assertions listed in Change step 10. The load-bearing ones are:
- the whole-JSON request comparison in
  `search_delivers_ranked_rows_without_reading_any_back`;
- the `edge_limit:1` request in the expand test;
- Reply C in the filtering test.

```sh
export CARGO_TARGET_DIR="${TMPDIR:-/tmp}/memory-asp-verify"
mkdir -p "$CARGO_TARGET_DIR"
test -f .cartridge/tests/integration/asp.rs
for doc in README.md .cartridge/help.md; do
	if ! grep -qF '## ASP' "$doc"; then
		echo "$doc has no ASP section" >&2
		exit 1
	fi
done
log="$CARGO_TARGET_DIR/asp.log"
cargo test -p memory_cartridge --lib asp::tests > "$log" 2>&1 || { cat "$log"; exit 1; }
for name in \
	a_memory_entity_expands_to_its_node_with_the_observed_projection_revision \
	expand_answers_nothing_for_a_missing_private_expired_or_respelled_key \
	search_delivers_ranked_rows_without_reading_any_back \
	search_keeps_the_context_filtering_exactly \
	search_and_expand_agree_with_context_memory_on_a_real_bank \
	the_shipped_declaration_is_one_the_host_accepts
do
	if ! grep -q "asp::tests::$name ... ok" "$log"; then
		echo "asp test did not pass: $name" >&2
		cat "$log"
		exit 1
	fi
done
rest="$CARGO_TARGET_DIR/rest.log"
cargo test -p memory_cartridge --lib -- --skip asp::tests > "$rest" 2>&1 || { cat "$rest"; exit 1; }
for name in \
	engine_tests::ingest_query_tool_and_context_reach_one_engine \
	source::tests::memory_fact_joins_shared_context_and_exact_readback_without_requery \
	source::tests::private_oversized_and_unknown_metadata_cannot_enter_evidence
do
	if ! grep -q "$name ... ok" "$rest"; then
		echo "existing test did not pass: $name" >&2
		cat "$rest"
		exit 1
	fi
done
```
