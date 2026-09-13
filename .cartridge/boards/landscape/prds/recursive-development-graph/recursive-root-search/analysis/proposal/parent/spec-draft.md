---
complexity: low
footprint:
- src/lib.rs
- src/census.rs
- src/source_search.rs
- .cartridge/tests/unit/census.rs
- .cartridge/tests/unit/source_search.rs
- .cartridge/docs/source-census.md
- .cartridge/docs/source-search.md
---
# Prove recursive search through the actual native service

Keep original three acceptance checks verbatim and both inherited review rounds. No new source implementation belongs in this rollup. Require verified current receipts for census, PRD public records, Landscape source search and Memo native facade. Its Landscape footprint is the exact local union; PRD/Memo source contracts and receipt fingerprints are explicit external inputs and require manual rollup revalidation when changed.

Use the collected facade's real native fixture: three board levels each contain the same PRD basename with a unique public fact, plus a configured source-only cartridge with typed public/private docs. Search through actual Memo native version3; all permitted facts appear with distinct structured addresses and callable:false. Read each selected reference through the same actual route, compare exact source bytes/revisions with its owner, and reject swapped owner/path/hash. Confirm inactive init.lua poison remains unexecuted, private markers do not appear, source bytes stay unchanged and no provider is activated by discovery. Run descendant edit/removal probes only as current behavior evidence; recursive-source-refresh remains its separate canonical verification task.

## Acceptance

- [ ] Root search finds distinct facts from all three fixture levels.
- [ ] Inactive documentation never becomes a callable service.
- [ ] Exact reads resolve the selected owner rather than another matching basename.

## Verify

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just test landscape
just check landscape
just test memo
just check memo
cd /Users/feb/dev/cartridge/memo.ctg
bun test ./.cartridge/tests/integration/source-search.test.ts
```

A library-only fixture or checked marker is insufficient. Parent proof records the actual source union, exact external receipts, commands, binary hashes, native request/results and privacy/activation limitations. Root alone changes lifecycle/shared map and collects.
