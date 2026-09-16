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

## Files and steps

1. `cartridge.json` `settings` — add `band` (boolean, default `false`: "Withhold the
   schema of every tool that is not hot; list it by name and summary in the `tools`
   meta-tool") and `hot` (list, default `[]`: "Tool names always sent with their
   schema while the band is on"). Default off: this transport cannot push
   `notifications/tools/list_changed` (see Remaining), so a restore only reaches a
   client that re-lists.
2. `src/service.rs` `Config` — add `band: bool`, `hot: Vec<String>`; `validate`
   refuses empty or duplicate `hot` names. Update the three `Config { .. }`
   literals in `tests.rs` (`fixture`, `diagnostic_inspection_…`; the third already
   uses `..Config::default()`).
3. `describe` — read two optional descriptor fields into `Tool`: `summary`
   (string) and `defer` (bool; `false` opts out). Nothing else about the listing
   changes.
4. `Service` — add `restored: Mutex<BTreeSet<String>>` (lives as long as the
   service, i.e. the host's mcp instance; shared by every attached client).
   A tool is hot when `!config.band`, or `defer == false`, or its name is in
   `config.hot`, or `config.tools` is non-empty (an explicit allowlist names it,
   which counts as restoring it), or its name is in `restored`.
5. `tools/list` with the band on — return hot listings plus one meta-tool
   `tools` (`inputSchema {type:object, required:[name], properties:{name:{type:string}}}`)
   whose description is a fixed sentence followed by one line per deferred tool:
   `name — summary`, the summary whitespace-flattened and clipped to 100 chars,
   or `name` alone when no summary is declared. The descriptor's `description`
   is never used as a fallback. Add `result._meta["cartridge/band"] =
   {deferred:[names], withheld_bytes, kept_bytes}`: withheld = serialized bytes of
   the deferred listings, kept = bytes of their listing lines. A provider tool
   named `tools` while the band is on hits the existing `duplicate tool name` error.
   Band off: output byte-identical to today (no meta-tool, no `_meta`).
6. `tools/call` name `tools` (band on only) — handled before the registry lookup,
   no policy round (it grants nothing). Known name: insert into `restored`, answer
   `content(<that tool's listing JSON>, false)`. Unknown name: `content(.., true)`.
   A deferred, unrestored tool stays callable through `tools/call` as today
   (deferred is not disabled).
7. `.cartridge/tests/unit/tests.rs` — add a `band_fixture(band, hot, tools)` fake
   with four tools: `memo` (summary "Read the record"), `plain` (no summary,
   description `PLAIN-DESCRIPTION-SENTINEL`), `pinned` (`defer:false`), `hotname`
   (named in `hot`). Tests, all prefixed `band_`:
   - `band_withholds_deferred_schemas_and_lists_their_summaries`
   - `band_restores_a_deferred_tool_for_the_rest_of_the_session`
   - `band_lists_a_tool_without_summary_by_name_alone`
   - `band_opt_out_and_allowlist_arrive_with_their_schema`
   - `band_disabled_sends_every_schema`
   - `band_reports_withheld_and_kept_bytes` (prints `band: withheld N kept M`)
8. `.cartridge/docs/README.md` — a `## Deferred tools` section: settings, the
   `summary`/`defer` descriptor fields, the `tools` meta-tool, `cartridge/band`
   meta, the no-push limit.

## Acceptance

- [ ] With `band=true`, `tools/list` declares exactly `{pinned, hotname, tools}`; `memo` has no `inputSchema` and the `tools` description contains `memo — Read the record` (`band_withholds_deferred_schemas_and_lists_their_summaries`).
- [ ] After one `tools/call tools {name:"memo"}`, two later `tools/list` calls include `memo` with its `inputSchema` and two `tools/call memo` succeed, with exactly one restore call made (`band_restores_a_deferred_tool_for_the_rest_of_the_session`).
- [ ] `plain` appears as a line equal to `plain` and `PLAIN-DESCRIPTION-SENTINEL` occurs nowhere in the serialized `tools/list` result (`band_lists_a_tool_without_summary_by_name_alone`).
- [ ] `pinned` (`defer:false`) and `hotname` arrive with schemas, and with non-empty `config.tools` every named tool arrives with its schema and no `tools` meta-tool (`band_opt_out_and_allowlist_arrive_with_their_schema`).
- [ ] With `band=false` every tool has its `inputSchema`, there is no `tools` meta-tool and no `cartridge/band` meta (`band_disabled_sends_every_schema`).
- [ ] `cartridge/band` reports `withheld_bytes` and `kept_bytes` equal to independently computed sums for the fixture, withheld > kept (`band_reports_withheld_and_kept_bytes`).
- [ ] `cartridge.json` declares `band` and `hot`, and the README documents `cartridge/band`.
- [ ] fmt and clippy are clean for mcp.ctg.

## Verify

```sh
cd /Users/feb/dev/cartridge/mcp.ctg
cargo fmt --all --check
```

```sh
cd /Users/feb/dev/cartridge/mcp.ctg
cargo clippy --all-targets
```

```sh
cd /Users/feb/dev/cartridge/mcp.ctg
out=$(cargo test --lib band_ -- --nocapture 2>&1) || { printf '%s\n' "$out"; exit 1; }
printf '%s\n' "$out" | grep -q 'test result: ok. 6 passed'
printf '%s\n' "$out" | grep -E 'band: withheld [0-9]+ kept [0-9]+'
```

```sh
cd /Users/feb/dev/cartridge/mcp.ctg
grep -q '"band"' cartridge.json && grep -q '"hot"' cartridge.json
grep -q 'cartridge/band' .cartridge/docs/README.md
```

## Remaining (not this spec)

- Push `notifications/tools/list_changed` after a restore needs the stdio bridge in
  `cartridge.ctg/src/cli/host.rs` (one reply per line, no server push today) — a
  cartridge-board PRD; after it lands, flip `band` default to `true`.
- Tool providers declaring `summary`/`defer` belong to their own boards.
