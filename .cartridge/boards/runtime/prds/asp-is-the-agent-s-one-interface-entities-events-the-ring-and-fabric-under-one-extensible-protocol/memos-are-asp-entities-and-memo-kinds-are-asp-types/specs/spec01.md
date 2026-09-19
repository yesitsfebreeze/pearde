---
complexity: moderate
footprint:
  - ".cartridge/help.md"
  - "README.md"
  - "cartridge.json"
  - "init.lua"
  - "src/lib.rs"
  - "src/record.rs"
  - "src/service.rs"
  - "src/asp.rs"
  - ".cartridge/tests/unit/src/asp.rs"
---

# spec01: memos are asp entities and memo kinds are asp types

Base revision: `dcbeb59b5ec3a72e1b902b1241e1c87dacabfbc9`.

## Change

1. `src/asp.rs` answers `asp.memo` from the record's own rows and graph: `memo:` nodes, `links`, `uses`, `kind` and `mentions` edges, and search.
2. `src/record.rs` caches each memo's path-like words; `src/service.rs` adds `Service::asp`.
3. `cartridge.json` declares `asp.memo` and the `asp` block; `init.lua` listens; README and help describe it.

## Acceptance

- [x] `expanding_a_memo_yields_its_node_revision_situations_and_edges_to_what_it_names`
- [x] `expanding_a_file_yields_a_mentions_edge_from_each_memo_that_names_it`
- [x] `search_returns_the_memo_for_a_phrase_in_its_when_and_respects_the_limit`
- [x] `a_newly_declared_kind_reaches_asp_with_no_manifest_change`
- [x] `the_manifest_declares_one_asp_event_and_prefixes_its_attributes`

## Verify

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/memo-asp-verify}"
LOG="$CARGO_TARGET_DIR/memo-asp.log"
mkdir -p "$CARGO_TARGET_DIR"
if ! env -u CARTRIDGE_YOLO cargo test -- --test-threads=2 > "$LOG" 2>&1; then
	tail -40 "$LOG" >&2
	echo "the suite does not pass" >&2
	exit 1
fi
for name in expanding_a_memo_yields_its_node_revision_situations_and_edges_to_what_it_names expanding_a_file_yields_a_mentions_edge_from_each_memo_that_names_it search_returns_the_memo_for_a_phrase_in_its_when_and_respects_the_limit a_newly_declared_kind_reaches_asp_with_no_manifest_change the_manifest_declares_one_asp_event_and_prefixes_its_attributes; do
	if ! grep -q "::$name \.\.\. ok" "$LOG"; then
		echo "a named test did not run and pass" >&2
		exit 1
	fi
done
```
