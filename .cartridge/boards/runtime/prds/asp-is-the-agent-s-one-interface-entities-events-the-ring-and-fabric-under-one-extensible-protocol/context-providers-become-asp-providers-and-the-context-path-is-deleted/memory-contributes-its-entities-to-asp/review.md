Score: 78/100

# Review of spec01: memory answers ASP as the owner of the `memory:` scheme

Reviewer: an independent agent reviewer, 2026-09-19. Read-only except this file.
Base: `memory.ctg` at `3432b13376017be921d745719e0626d6f0b5463c`; `cartridge.ctg` at `445a87f`.

## What I checked, and what held

- Every `file:line` citation in "What is true today" was read at the base
  revision and is accurate, including these:
  - `source.rs:25-30,38-54,61-105,107-108,125,129,145-181,188,312-314`;
  - `lib.rs:2-3,17,182-190,524-531,576,581-586`;
  - `init.lua:5` and `cartridge.json:92,114`;
  - `id_detail.rs:33-35,120-125,147-156,172-198` and `util.rs:61-66`;
  - `server.rs:499-502,547-566,569-587,692,696,713-723,721,764,1655-1664`;
  - `src/cartridge/Cargo.toml:9-10,12-30`;
  - `cartridge.ctg/src/asp/admit.rs:14-60`, `expand.rs:74-79`,
    `search.rs:17-80` and `protocol.rs:85-128`.
- The ranked and compact text rule holds. `util::truncate` appends `...`
  only when `nth(500)` exists, so `chars > 500` on a 503-character ranked
  text reproduces `text_truncated` exactly (`id_detail.rs:121,125,194`).
- The mount path `../../../../.cartridge/tests/integration/asp.rs`, taken from
  `src/cartridge/src/asp/mod.rs`, resolves to the repository root. `crate::DOCUMENT`
  exists (`lib.rs:17`), so the `fs` precedent's `held_to_the_declaration`
  (`fs.ctg/.cartridge/tests/unit/asp.rs:24-46`) ports as described.
- Footprint versus held claims: of the claimed rows with `repo: memory.ctg`,
  only the heat row is claimed besides this one. None of its 14 paths is in this
  footprint. `health-reports-how-many-entities-carry-a-claim-kind` also lists
  `src/cartridge/src/lib.rs`, but that row is `open` and unclaimed. The
  footprint is complete for the Change as written. The `source.rs` widening,
  which only makes three items `pub(crate)`, is the right call: a second copy of
  `hydrate` would defeat the row's parity purpose.
- The Verify block is sound on the hazards this project has already hit:
  - The only guard is `if ! grep -q ...; then`. It is not a bare `! grep`, and
    there is no AND-OR guard.
  - Every variable has a literal default. `${TMPDIR:-/tmp}` survives an empty
    environment.
  - The target directory is pinned outside the live tree.
  - `rpc` and `retrieval-piece` are never tested, so their load-flaky timing
    tests cannot fail it.
  - The real-engine ASP test runs in its own command, apart from the latch-
    flipping `drain` of the engine tests.
- I measured the second command at base in a `git clone --local`, with a cold
  target directory under `env -u CARTRIDGE_YOLO`: `21 passed; 0 failed`, 56.4 s
  wall and a 0.38 s test phase. All three named existing tests exist
  (`engine_test.rs:54`, `.cartridge/tests/unit/src/cartridge/source.rs:72,304`).
  The first command builds the same test binary, so the whole block is roughly
  60 s cold on this machine. That is inside 120 s, but the spec's figure of
  46.7 s is optimistic.
- Isolation holds: nothing reaches a sibling crate or file.
  `retrieval::id_detail::COMPACT_TEXT` is mirrored with a `ponytail:` comment
  and pinned by the real-bank test, not imported. The four-file `asp/` split
  (`mod`, `node`, `expand`, `search`) is one responsibility per file.

## Blocking findings

1. **The search-is-heatless premise rests on a heat mechanism that has already
   been overruled, and the heat row cannot keep its carve-out without also
   warming ASP search.**
   - The spec justifies its search/expand split by citing the heat spec's
     "Mechanism 6": "the text-query delivery … deposits no heat". The deferred
     README text states it as fact: "so it is a delivery and deposits no heat".
   - The heat row's own `prd.md` rejected that mechanism. Its "Decision …
     after review round 1 failed at 85" says: "Blocking finding 1 stands, and
     the PRD wins … the `tool.memory` `query` path keeps depositing".
   - `tool.memory` sends `{op, text, k?}` (`lib.rs:266-268,277`). ASP search, as
     specified, sends the byte-identical `{op:"query", text, k}`. Both reach the
     same `tool_query` enqueue (`server.rs:721,764`).
   - So once the heat row honours its Outcome, it cannot tell the two apart.
     Every ASP search will then keep depositing access heat on up to `limit`
     memory rows (20 from `tool.asp`, 256 from the CLI).
   - The host sends search to every search provider on every ASP search
     (`cartridge.ctg/src/asp/search.rs:23-29`). An agent searching for a file or
     a tool will therefore warm the memory bank. That is the self-warming loop
     the spec says it avoids, and today, before the heat row, it is already the
     behaviour this row ships.
   - Required: either
     - mark ASP search's request with a field the heat row can key its
       delivery rule on, named in this spec and agreed as a note on the heat
       row, and pin it with the recorded-request assertion in
       `search_delivers_ranked_rows_without_reading_any_back`; or
     - withdraw every heat claim (Outcome, Design decisions, deferred docs)
       and state that search heat is whatever the heat row's text-query rule
       ends up being.

2. **`search_keeps_the_context_filtering_exactly` requires a limit rule that
   contradicts both "exactly" and the Change text.**
   - In `context.memory`, `position` enumerates every non-private row
     (`source.rs:145-149`). A superseded, inactive, id-less or malformed row
     therefore uses up the limit, and only private rows are free.
   - Change step 5 says "the loop stops at `limit` public rows", which is the
     same rule.
   - The named test requires the opposite: "with `limit: 1`, `good` still comes
     back, because every row before it is private or filtered".
   - An implementer who follows step 5, or `context.memory`, fails this test.
     One who passes it has diverged from `context.memory` while a test named
     "exactly" says otherwise.
   - Required: pick one rule, state it once in step 5, and make the test's
     fixture order match it. Counting only emitted nodes is defensible. If you
     keep it, rename the claim, and say how twin detection works past the stop
     point: a conflicting twin after the `limit`-th emitted row is never seen.

3. **A new event ships with no README or help text, and the follow-up has no
   owner.**
   - The standing rule (system `cartridge-readme-stays-current`) is that a
     change to a cartridge's surface updates `README.md` and
     `.cartridge/help.md` in the same change.
   - The spec adds `asp.memory` and defers both files to "whoever collects this
     row after the heat row". No PRD row, `needs` edge or claim carries that
     work.
   - `just audit` will not catch it: `audit-cartridges.md:135-143` only checks
     that the files exist, are long enough and are not empty.
   - As written, the surface lands undocumented and nothing on the board says
     so.
   - Required: either
     - add `needs: @memory/heat-is-deposited-on-read-back-not-on-delivery`,
       put `README.md` and `.cartridge/help.md` into this footprint, and land
       the text in this change; or
     - open a sibling leaf row that owns the text and `needs` both rows, and
       name it in the PRD.

   Whichever you choose, the deferred text must stop asserting the heat
   behaviour of blocking finding 1 until that is settled.

## Non-blocking findings

- **The Verify block names tests but cannot prove they test anything.**
  - A `#[test] fn search_delivers_ranked_rows_without_reading_any_back() {}`
    with an empty body satisfies the `... ok` grep. See the project memos
    `text-gates-lose-pin-an-executed-test` and
    `gate-a-test-by-executing-a-mutant`.
  - The cheapest mutant needs no knowledge of the implementation. Copy the tree
    to `$TMPDIR`, set `edge_limit:1` to `edge_limit:0` in expand's request, or
    add `"ids"` to search's request, and require the named test to fail.
  - If no mutant is attempted, the spec must state the ceiling and name the
    diff reviewer as the check, as `a-verify-block-cannot-prove-why-a-test-died`
    prescribes. It does neither.
- **`the_shipped_declaration_is_one_the_host_accepts` does not prove what its
  name says.**
  - The host parses the block with `deny_unknown_fields` (`protocol.rs:20,38`).
    A stray key such as `"owners"` or a top-level `"description"` makes the host
    refuse the whole manifest, and the listed assertions all still pass.
  - Fix: assert that the `asp` object's keys are a subset of `{schemes, edges,
    attributes, actions, search}`, that each scheme's keys are a subset of
    `{description, owner}`, and that each scheme name is bare
    (`protocol.rs:95-105`). Otherwise rename the test.
- **The Verify block does not run the root repository's structural gates.**
  - The spec adds three new `src/` files and a mounted test file under
    `.cartridge/tests/integration/`, but Verify never runs `cited_paths`,
    `orphan_modules` or `layer_headers` (root `Cargo.toml:144,184,196`).
  - A `//!` header that cites `cartridge.ctg/src/asp/admit.rs` would fail
    `cited_paths` ("A tree the repo does not have is rot") and still collect
    green.
  - Either add `cargo test --test cited_paths --test orphan_modules` (both are
    fast), or tell the implementer not to cite sibling paths in comments.
- **The test file's location breaks both the precedent and this repository's
  layout.**
  - The unit tests of the cartridge crate live at
    `.cartridge/tests/unit/src/cartridge/*.rs` (`lib.rs:582,585`,
    `source.rs:313`). The `fs` and `memo` precedents use
    `.cartridge/tests/unit/…` (`fs.ctg/src/asp/mod.rs:56-58`,
    `memo.ctg/src/asp.rs:140-141`).
  - `.cartridge/tests/integration/` holds the root package's `[[test]]` targets
    (root `Cargo.toml:81-228`, `autotests = false`). A lib-mounted file there
    reads as an unregistered integration target.
  - Suggest `.cartridge/tests/unit/src/cartridge/asp.rs`. That also changes the
    PRD frontmatter.
- **The host re-ranks search results, so "in the engine's order" is not what an
  agent sees.**
  - `rank::rank` (`cartridge.ctg/src/asp/rank.rs:38-80`) orders nodes by lexical
    overlap on `name`, `id`, `tags` and `description`. A semantically found
    fact that shares no word with the query falls below every lexical match
    from `fs`, `lsp` or `memo`.
  - `tags: [source.scheme]` also gives every memory node a weight-2 match for
    any query containing that scheme word.
  - This is not the spec's defect. The Outcome, however, sells ASP search as the
    replacement for prompt recall
    (`the-prompt-recall-and-the-proxy-read-asp-search`), and that row inherits a
    ranking change the spec does not mention. State it.
- **An over-long key answers `Err`, which the host reports as memory being
  `unavailable`** (`admit.rs:67-72`). A 513-byte key can never name an entity.
  `Null` ("nothing here") is the truthful answer, and it matches the handling
  of a respelled prefix. The same applies to a query over 4096 bytes: the host
  already bounds the input, and an `Err` makes one bad query look like a
  provider outage.
- **The engine receives `k: limit`, so private and filtered rows still take up
  engine slots.** A bank dense with private facts answers fewer than `limit`
  nodes. This matches `context.memory` (`source.rs:129`), which is why it is not
  blocking, but "do not count toward the limit" only holds inside the rows the
  engine already returned. Say so.
- **The spec says `source.rs` changes only `private`, `hydrate` and
  `ID_BYTES`, but search also needs twin detection and the malformed-source
  skip.**
  - In `context.memory`, both use the private `source()` and `bounded()`
    (`source.rs:153,161`).
  - They can be rebuilt from `hydrate`'s output: its `Malformed` result, and
    `evidence.source` for comparing twins. The spec should say that search
    compares `evidence.source` after hydrating, or the implementer will widen
    `source.rs` again.
- **No event timeout is declared.** A search embeds the query over HTTP on every
  ASP search, and a caller-side timeout cannot cancel a cartridge call (memo
  `a-caller-cannot-cancel-a-cartridge-call`). `lsp` declares `timeout_ms` on its
  ASP event (`lsp.ctg/cartridge.json:35`). Consider one bound at the embed
  client's own limit.
- **The real-bank test leaves the engine open over a `tempfile` directory that
  is dropped at the end of the test.** It skips `drain` on purpose, and this is
  harmless while `tick.interval_secs` is 0 and the queue is disabled. State that
  both settings are required, so that a later settings change does not turn it
  into a background-thread panic in the shared test process.
- **The deferred README wording does not match the file.** The README's Events
  lines use `**Defines** — …` with an em dash (`README.md:9-10`), not the colon
  form in the spec. This is moot if blocking finding 3 moves the text into the
  change.
- **Timing claim:** the block measured about 60 s cold here, against the stated
  46.7 s. That is still inside 120 s, but give the measured figure and not the
  best case.

## Answers to the five questions

1. **Acceptance tests.** Mostly behavioural. The request assertions on the fake
   `call` would catch a `get`-per-hit search or a `get`-based expand, and the
   test computes the revision itself, without calling `hydrate`. The filtering
   test contradicts the Change (blocking finding 2). The declaration test is
   weaker than its name (non-blocking).
2. **Design decisions.**
   - Expand as a read-back through `ids`, search as a single text query,
     revision parity through the one `hydrate`, and no edges and no actions:
     each is sound and justified with evidence.
   - The heat rationale is not sound, because it rests on an overruled
     mechanism and on a request that cannot be told apart from the carve-out
     path (blocking finding 1).
3. **Footprint.** It is complete and minimal for the Change as written. The
   `source.rs` widening is justified, and it collides with no held claim. It is
   incomplete only if blocking finding 3 is fixed by landing the docs here.
4. **Verify.**
   - It fails at base on `test -f`. It passes only with named tests, but any
     body passes (non-blocking).
   - It runs about 60 s cold and 1 s warm.
   - It is robust to the `rpc` flakes, the empty environment, the `set -e`
     pitfalls and the latch.
5. **One file per responsibility and isolation.** Yes. The only issue is where
   the test file sits (non-blocking).

## Round 2

Score: 88/100

Reviewer: a fresh, independent agent reviewer, 2026-09-19. Read-only except
this file. `memory.ctg` is at the stated base `3432b13` with a clean tree.
`cartridge.ctg` is at `f56c442`; its only ASP change since round 1's `445a87f`
is `d04ab33` (compact lines), which moves line numbers but changes no protocol
fact the spec relies on.

### Round-1 blocking findings: all three are resolved

1. **Heat.** Resolved by withdrawing the claim. PRD `prd.md:38-43` and spec
   `spec01.md:183-205` now say that search deposits what a `tool.memory` query
   deposits, and that expand deposits what a read by id deposits. Both
   statements hold at base:
   - `tool.memory` sends `{op, text, k?}` (`lib.rs:266-268`);
   - ASP search sends `{op, text, k}` into the same `tool_query` enqueue
     (`server.rs:713-723,764`);
   - `query_by_ids` enqueues nothing (`server.rs:547-566`).

   The table says plainly that an ASP search for anything warms up to `limit`
   rows. The Documentation text claims nothing beyond parity with
   `tool.memory`. At base `context.memory`'s own text query (`source.rs:129`)
   deposits through the same path too, so for the prompt recall this is parity
   and not a regression. The spec could say so.
2. **The limit rule.** Resolved.
   - Step 2 of "The filters" (`spec01.md:222-223`) and Change step 5
     (`:343-346`) state one rule: only private rows are free, and every other
     row uses a slot.
   - That rule is `source.rs:145-149` exactly.
   - Reply B (`:452-453`) and Reply C (`:454-456`) pin the rule from both
     sides. Counting only emitted nodes fails C, and counting private rows
     fails B.
3. **Documentation.** Resolved.
   - `README.md` and `.cartridge/help.md` are in both footprints
     (`prd.md:14-15`, `spec01.md:9-10`).
   - The text is given word for word (`spec01.md:499-531`), with the em-dash
     form that `README.md:9-10` uses.
   - The insertion points exist (`README.md:20` `## In this composition`,
     `help.md:12` `## Read next`).
   - The text makes no heat claim beyond parity.

### Blocking findings

1. **The rebase note is not enough. Once this row collects, the heat row's
   README gate passes without the heat row doing anything.**
   - The heat spec's Verify checks that `README.md` has moved off
     `base=3432b13376017be921d745719e0626d6f0b5463c`
     (`heat-is-deposited-on-read-back-not-on-delivery/specs/spec01.md:210-217`).
     That diff is the only gate on that row's Acceptance box 4 for the README
     (`heat …/prd.md:48`).
   - After this row lands its `## ASP` section, `README.md` differs from that
     base whether or not the heat row rewrites the `context.memory` bullet. The
     heat row's README gate then goes inert, and it gives no signal. This is
     the paste-beats-the-text-gate class of
     `text-gates-lose-pin-an-executed-test`, created from outside that row.
   - `spec01.md:46-48,496-497` says only that the heat row's bullet edits
     "apply unchanged". That is textually true: the bullet stays at
     `README.md:17` and `help.md:9`, because Events lines 9-10 are replaced one
     for one. It misses the gate.
   - Required:
     - The rebase note must also tell the heat row to re-pin its Verify
       `base`, or better, to gate the bullet line itself rather than the whole
       file.
     - The coordinator should put the same sentence on the heat row's PRD,
       since this row cannot edit it.
   - Apart from this, the heat row's footprint is untouched. None of its other
     twelve paths (`heat …/prd.md:8-21`) is in this footprint. It is `open`
     and has no `claim:`.

### Non-blocking findings

- **Two citations are wrong.**
  - `spec01.md:140` cites `cartridge.ctg/src/asp/expand.rs:51-56` for the
    owner-revision rule. That rule is at `:56-61` at `445a87f` and at `:74-79`
    at `f56c442`. Neither revision has it at 51-56.
  - `spec01.md:244` cites `id_detail.rs:147-152` for "the id path serves
    superseded rows". Those lines are the comment about serving *expired*
    rows. The claim is still true, for a different reason: `matches_filter`
    (`retrieval_score.rs:213-260`) has no superseded test, and
    `build_query_options` (`server.rs:464-473`) does not consult
    `include_history` for the id path.
- **The test file sits in a directory the repository's own gate assigns to
  the root package.**
  - `declared_dependencies.rs:385-386` collects every `.rs` under
    `.cartridge/tests/integration` as a test of the `memory (workspace root)`
    unit. A `memory_cartridge` test placed there is counted against the wrong
    crate's manifest.
  - That is harmless today, because the gate only flags unused declarations.
    It is still more evidence for round 1's suggestion of
    `.cartridge/tests/unit/src/cartridge/asp.rs`.
  - The reason the spec gives for not moving it (`spec01.md:53-57`, "outside
    the frontmatter footprint") is weak. The coordinator can edit the
    frontmatter.
- **The declaration test still misses one class of refusal.** `Described` is
  `deny_unknown_fields` (`protocol.rs:48-53`), so a stray key inside
  `asp.attributes."memory.source"` makes the host refuse the manifest, and
  `the_shipped_declaration_is_one_the_host_accepts` (`spec01.md:473-488`)
  still passes. Add the check that each attribute's keys are a subset of
  `{description}`.
- **Small test gaps.**
  - The expand test does not cover a reply without a `results` array
    (`spec01.md:325`).
  - The filtering test does not cover twins that share a source, which must
    give one node and not zero (`source.rs:165-171`).
  - Neither gap is load-bearing.
- **The documentation box is gated by its heading only** (`spec01.md:596-601`),
  and "neither file's `context.memory` bullet changes" (`prd.md:65-66`) has no
  gate. The spec hands wording to the reviewer, which is acceptable under
  `a-verify-block-cannot-prove-why-a-test-died`. A base-pinned bullet check
  would false-red if the heat row collected first, so leaving it to the
  reviewer is right. Say that this is the reason.
- **`cited_paths` is covered for `asp/` only** (`spec01.md:298-300`). Extend
  the "no sibling paths in comments" instruction to the test file, which is
  where an implementer is most likely to cite `fs.ctg/.cartridge/tests/unit/asp.rs`.
- **`null` for `valid_until` is not stated.** Change step 5 (`spec01.md:349`)
  computes `expired: valid_until < now`. A ranked row without a deadline
  carries `"valid_until": null` (`id_detail.rs:189`), and that must give
  `false`.
- **The manifest edit untrusts the live cartridge.** Changing
  `cartridge.json` makes the running daemon drop `memory` until it is trusted
  again (memo `editing-a-manifest-untrusts-its-cartridge`). Collect pass 2 runs
  in the live submodule, so the PRD should say that `memory` needs
  re-trusting after collect.

### Answers to the six questions

1. **Would the named tests fail on wrong behaviour?**
   - Yes for the load-bearing behaviour:
     - The whole-JSON request comparison catches an extra field or a by-id
       read in search.
     - The exact expand request catches `get`, `edge_limit:0` or a text
       query.
     - Replies B and C pin the limit rule.
     - The expand revision is computed independently of `hydrate`, so the test
       is not self-referential.
     - The real-bank test pins the 500-character mirror on the real engine.
   - An empty or hollow body passes Verify. The spec states that ceiling and
     names the diff reviewer (`spec01.md:580-590`), as the memo prescribes.
2. **Are the design decisions sound?**
   - Expand through `ids`, one text query for search, and revision parity
     through the one `hydrate` are sound. The widening of `source.rs` for
     visibility only is sound.
   - Null for impossible keys is sound. No edges is sound, because edge ends
     can be private or expired. No actions is sound, because `tool.memory` has
     no read by id.
   - The honest heat table is sound.
3. **Is the footprint complete and minimal?** Yes. Its eight paths cover every
   step of the Change. No held claim collides with it, and it touches none of
   the heat row's paths except README and help.
4. **Does Verify fail at base, pass only with the change, and fit 120 s?**
   - At base it stops at `test -f`. I ran it with `env -i` and it exited 1.
   - The guards are `if ! grep …; then`. There is no bare `! grep` and no
     AND-OR guard.
   - The only variable is `${TMPDIR:-/tmp}`, which has a literal default.
   - The target directory is pinned outside the tree.
   - `rpc` and `retrieval-piece` are never tested.
   - The real-engine test is kept apart from the latch-flipping `drain`.
   - Round 1 measured about 60 s cold. Warm is about 1 s.
5. **One file per responsibility and isolation?** Yes. `asp/` is split into
   `mod` (dispatch), `node`, `expand` and `search`. `COMPACT_TEXT` is mirrored
   with a `ponytail:` comment and pinned by a test instead of imported. Nothing
   reaches a sibling.
6. **Were the round-1 blocking findings resolved?** All three, as described
   above. The new blocking finding is a side effect of resolving finding 3.
