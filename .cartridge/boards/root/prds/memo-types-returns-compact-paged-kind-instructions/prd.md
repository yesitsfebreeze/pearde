---
state: "done"
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge/memo.ctg"
commit: "9fce5267768d4ddeee42fac97eb8eac89512bca3"
---

# memo types returns compact paged kind instructions

## Outcome

`tool.memo` `types` answers fit inside a model tool result without truncation: without `kind` it returns compact rows for every type declaration; with `kind` it returns that kind's instruction bodies. Both forms page with `limit` and `cursor` like `list` does.

## Reason

`record.rs:935-937` serializes every `kind: type` memo as full JSON — 56 type memos' bodies on one line, 102,797 bytes (observed 2026-09-16), which exceeds the MCP tool-result limit and never reaches the model, while `Input::parse` (`record.rs:289-298`) allows no arguments for `types` at all, so a caller cannot narrow it. The advertised contract (`memo.ctg/cartridge.json` tool description) is "index and types for a kind's instructions"; `index` already returns compact kind metadata, `types` should return the instructions themselves, compactly.

## Acceptance

- [x] `types` without `kind`: rows are `{path, type, description}` for each `kind: type` memo, no bodies, ordered by path, paged with the `limit+1` probe row pattern (`more`, `cursor`) exactly like `list` (`record.rs:1026-1041`).
- [x] `types` with `kind`: rows are `{path, body}` for that kind's declaration memos, paged the same way.
- [x] `Input::parse` allows `kind`, `limit`, `cursor` for `types`; other ops unchanged. The service `describe` schema lists `kind`/`limit`/`cursor` for the `types` op like `list` does.
- [x] The unfiltered `types` answer from this workspace (1309 memos, 56 type declarations) is under 8 KiB.
- [x] `memo.ctg` unit tests cover both forms and paging.
