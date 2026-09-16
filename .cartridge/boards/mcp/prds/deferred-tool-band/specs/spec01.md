---
complexity: medium
footprint:
  - cartridge.json
  - src/service.rs
  - .cartridge/tests/unit/tests.rs
  - .cartridge/docs/README.md
---

# spec01 — `tools/list` withholds deferred schemas behind a one-line listing and a `tools` restore call

Base: mcp.ctg `6f06acd`. No `needs`. Everything lands in `src/service.rs`; no new file.

## Scope and contract

This PRD owns **the MCP listing only** (`tools/list` of the mcp cartridge). The band's
disposition is the **composition-wide contract**, carried by fields any listing can
read, not by mcp internals:

- descriptor `summary` (string, optional): the one-line listing text. Never
  substituted by `description`.
- descriptor `defer` (bool, optional): `false` opts the tool out of deferral.
- a consumer-side `hot` set (tool names, a setting of each listing surface): names
  always sent with their schema.
- disposition rule: a tool is **hot** if the band is off, `defer == false`, its name is
  in `hot`, an explicit allowlist names it, or it was restored; otherwise **deferred**.

mcp is the first consumer. Its README section `## Deferred tools` is the canonical
statement of the contract, and other boards cite it. No shared doc file is added,
because that would widen the footprint. `@harness/reflex-tool-audit-loop` reads a tool's disposition from the
same descriptor fields (`defer`) and its own `hot` setting, applying the rule above
in `harness.ctg` `convert_tools`; it does not read mcp's `Service`. The proxy
(`proxy.ctg` injected `cartridge__*` tools), agent (`agent.ctg` model loop) and
harness listings are out of scope here (see Remaining).

## Files and steps

1. `cartridge.json` `settings` — add `band` (boolean, default `false`: "Withhold the
   schema of every tool that is not hot; list it by name and summary in the `tools`
   meta-tool") and `hot` (list, default `[]`: "Tool names always sent with their
   schema while the band is on"). Default off, because this transport cannot push
   `notifications/tools/list_changed` (see Remaining): a restore reaches only a client
   that re-lists, and Claude Code does not. `band=false` is the rollback.
2. `src/service.rs` `Config` — add `band: bool`, `hot: Vec<String>`; `validate`
   refuses empty or duplicate `hot` names. `hot` takes tool **names** (`memo`), while
   `tools` takes keys (`tool.memo`). Names that match no descriptor cannot be refused at
   config time: descriptors are discovered at list time, and providers come and go with
   the composition. They are reported in the listing meta instead (step 5). Add `band: false, hot: vec![]` to the three
   full `Config { .. }` literals in `tests.rs`: `fixture`,
   `an_empty_profile_exposes_no_tools_and_an_unknown_one_is_refused`, and
   `diagnostic_inspection_is_optional_scoped_and_cannot_grant_authority`. The literals
   using `..Config::default()` need no change.
3. `describe` — read the optional descriptor fields `summary` and `defer` into
   `Tool`. Nothing else about the listing changes.
4. `Service` — add `restored: Mutex<BTreeSet<String>>`. It lives as long as the
   service: one per host process, **shared by every attached client, never cleared
   until the host restarts**, with no un-restore. Apply the disposition rule from
   Scope; the explicit allowlist is a non-empty `config.tools`.
5. `tools/list` with the band on — return the hot listings plus one meta-tool `tools`
   (`inputSchema {type:object, required:[name], properties:{name:{type:string}}}`).
   Its description is a fixed sentence followed by one line per deferred tool:
   `name — summary`, with the summary whitespace-flattened and clipped to 100 chars,
   or `name` alone when no summary is declared. Add `result._meta["cartridge/band"] =
   {deferred:[names], withheld_bytes, kept_bytes, unknown_hot:[names]}`, where
   `unknown_hot` lists the `hot` names that match no described tool. withheld is the serialized bytes of
   the deferred listings; kept is the bytes of their listing lines. A provider tool
   named `tools` while the band is on hits the existing `duplicate tool name` error,
   which fails the whole `tools/list`. The recovery is to rename the provider tool or
   set `band=false`. With the band off the output is byte-identical to today: no
   meta-tool, no `_meta`.
6. `tools/call` named `tools` (band on only) — handle it before the registry lookup,
   with no policy round. A restore only reveals the schema of a tool that `tools/call`
   already reaches under policy, so it grants no call authority. Every `tools/call` of
   the restored tool still goes through `policy` as today. That makes a host-wide,
   unauthenticated restore acceptable: one client can change another client's listing,
   but never what that client may call. For a known name, insert it into
   `restored` and answer `content(<that tool's listing JSON>, false)`. For an unknown
   name, answer `content(.., true)`. A deferred tool that was never restored stays
   callable through `tools/call` as today, because deferred is not disabled; a call
   therefore does not prove a restore.
7. `.cartridge/tests/unit/tests.rs` — add a `band_fixture(band, hot, tools)` fake with
   four tools:
   - `memo`, summary "Read the record"
   - `plain`, no summary, description `PLAIN-DESCRIPTION-SENTINEL`
   - `pinned`, `defer:false`
   - `hotname`, named in `hot`

   Tests, all prefixed `band_`:
   - `band_withholds_deferred_schemas_and_lists_their_summaries`
   - `band_restores_a_deferred_tool_for_the_rest_of_the_session`
   - `band_lists_a_tool_without_summary_by_name_alone`
   - `band_opt_out_and_allowlist_arrive_with_their_schema`
   - `band_disabled_sends_every_schema`
   - `band_disabled_listing_is_byte_identical`: the serialized `tools/list` result with
     `band:false, hot:[]` equals, byte for byte, both (a) the result from a config built
     through `Config::default()` with only `tools` set, and (b) a pinned
     `json!({"tools":[{name,description,inputSchema}…]})` built from the fixture
     descriptors in name order, which is the shape emitted at `6f06acd`.
   - `band_reports_withheld_and_kept_bytes` (prints `band: withheld N kept M`)
8. `.cartridge/docs/README.md` — add a `## Deferred tools` section covering:
   - the contract (`summary`, `defer`, `hot` and the disposition rule), as read by
     every listing surface
   - the `band`/`hot` settings
   - the `tools` meta-tool and the `cartridge/band` meta
   - the phrase "`hot` takes tool names, `tools` takes keys"
   - the phrase "a provider tool named `tools` fails the listing" with its recovery
   - the phrase "restores are shared by every attached client until the host
     restarts", with the policy rationale from step 6
   - the missing list-change push
   - `band=false` as the rollback

## Acceptance

- [x] With `band=true` and `hot=[hotname, ghost]`, `tools/list` declares exactly the hot set, anything restored, and the `tools` meta-tool: `{pinned, hotname, tools}`. `memo` has no `inputSchema`, the `tools` description contains `memo — Read the record`, and `cartridge/band.unknown_hot` is `["ghost"]` (`band_withholds_deferred_schemas_and_lists_their_summaries`).
- [x] Before any restore, `memo` has no `inputSchema` in `tools/list`. After exactly one `tools/call tools {name:"memo"}`, `memo` has its `inputSchema` in both of the next two `tools/list` results (`band_restores_a_deferred_tool_for_the_rest_of_the_session`).
- [x] `plain` appears as a line equal to `plain`, and `PLAIN-DESCRIPTION-SENTINEL` occurs nowhere in the serialized `tools/list` result (`band_lists_a_tool_without_summary_by_name_alone`).
- [x] `pinned` (`defer:false`) and `hotname` arrive with schemas. With a non-empty `config.tools`, every named tool arrives with its schema and there is no `tools` meta-tool (`band_opt_out_and_allowlist_arrive_with_their_schema`).
- [x] With `band=false`, every tool has its `inputSchema`, there is no `tools` meta-tool and there is no `cartridge/band` meta (`band_disabled_sends_every_schema`).
- [x] With `band=false`, the serialized `tools/list` equals both the `Config::default()` listing and the pinned pre-band JSON for the fixture (`band_disabled_listing_is_byte_identical`).
- [x] `cartridge/band` reports `withheld_bytes` and `kept_bytes` equal to independently computed sums for the fixture, and withheld > kept (`band_reports_withheld_and_kept_bytes`).
- [x] `cartridge.json` declares `band` and `hot`, and the README documents the contract fields, that `hot` takes names, `cartridge/band`, the collision, the restore scope and the rollback.
- [x] fmt is clean and clippy reports no warnings (`-D warnings`) for mcp.ctg.

## Verify

Each block runs from the engine-provided cwd: first the lane worktree root of mcp.ctg,
then the mcp.ctg repo. `cargo test --lib band_` stands in for `just test mcp`, which is
red at base `6f06acd`: 11 passed and 2 failed, the live-fixture tests
`initialized_live_client_inspects_real_policy_without_granting_writes` and
`initialized_live_client_observes_catalog_replacements`, both failing with "Live catalog
did not settle". `just check mcp` is covered by the fmt and clippy blocks.

```sh
cargo fmt --all --check
```

```sh
cargo clippy --all-targets -- -D warnings
```

```sh
out=$(cargo test --lib band_ -- --nocapture 2>&1) || { printf '%s\n' "$out"; exit 1; }
printf '%s\n' "$out" | grep -q 'test result: ok. 7 passed'
printf '%s\n' "$out" | grep -E 'band: withheld [0-9]+ kept [0-9]+'
```

```sh
grep -q '"band"' cartridge.json
grep -q '"hot"' cartridge.json
grep -q 'cartridge/band' .cartridge/docs/README.md
grep -q 'defer' .cartridge/docs/README.md
grep -q 'band=false' .cartridge/docs/README.md
grep -q 'a provider tool named `tools` fails the listing' .cartridge/docs/README.md
grep -q 'restores are shared by every attached client until the host restarts' .cartridge/docs/README.md
grep -q 'hot` takes tool names' .cartridge/docs/README.md
```

## Remaining (not this spec)

- `@root/the-stdio-bridge-pushes-tools-list-changed-so-a-deferred-tool-restore-reaches-every-client`
  (needs this PRD): the stdio bridge in `cartridge.ctg/src/cli/host.rs`
  (one reply per line, no server push today) emits `notifications/tools/list_changed`
  after a `tools` restore, and mcp advertises `tools.listChanged`. Once it lands, flip
  the `band` default to `true`.
- **Other listings apply the same contract:** proxy injected tools (proxy board), agent
  model loop (agent board) and harness `convert_tools` (harness board, via
  `@harness/reflex-tool-audit-loop`). Each reads `summary`/`defer` from descriptors and
  its own `hot` setting.
- **Providers:** add `summary` and, where needed, `defer:false` in their own boards
  (fs, lsp, memo, …).
- `@mcp/the-mcp-live-catalog-tests-settle-at-base`: the 2 live-fixture tests in `just test mcp` fail at base
  with "Live catalog did not settle: starting the host for .cartridge". Triage and
  fix them so the owner gate is green again.
