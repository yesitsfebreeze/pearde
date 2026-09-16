---
complexity: medium
footprint:
- src/record.rs
- .cartridge/tests/unit/src/record/distill_tests.rs
- .cartridge/tests/integration/tests.rs
---

# memo types returns compact paged kind instructions

`types` serialized every `kind: type` memo whole — 56 declarations' bodies on
one line, 102,797 bytes — which exceeds the MCP tool-result limit and never
reached the model, while `Input::parse` allowed no arguments for `types` at
all. `index` already returns compact kind metadata; `types` returns the
instructions themselves, compactly.

Rows without `kind` are `{path, type, description}`, ordered by path, paged
with the same `limit+1` probe row as `list`. Naming a kind adds that
declaration's `body`. A compact row omits the `body` key rather than carrying
null, so no caller reads a missing body as an empty one.

## Acceptance

- [x] `types` without `kind`: rows are `{path, type, description}`, no bodies,
  ordered by path, paged with the `limit+1` probe row pattern (`more`,
  `cursor`) like `list`.
- [x] `types` with `kind`: rows carry that kind's declaration `body`, paged
  the same way.
- [x] `Input::parse` allows `kind`, `limit`, `cursor` for `types`; other ops
  unchanged.
- [x] The unfiltered `types` answer is far under the 8 KiB ceiling that
  102,797 bytes broke.
- [x] Unit and integration tests cover both forms and paging.

## Verify and Proof

```sh
set -eu
cd /Users/feb/dev/cartridge/memo.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_INCREMENTAL=0
cargo test -p memo_cartridge --all-targets
```

129 tests pass, including
`record::distill_tests::types_returns_compact_rows_and_pages_like_list` and
`service::tests::kind_discovery_reads_only_the_selected_declaration_and_keeps_legacy_types`.
