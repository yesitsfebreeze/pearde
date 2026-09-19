---
complexity: moderate
footprint:
  - ".cartridge/help.md"
  - "README.md"
  - "cartridge.json"
  - "init.lua"
  - "src/client.rs"
  - "src/lib.rs"
  - "src/service.rs"
  - "src/asp"
  - ".cartridge/tests/unit/asp.rs"
---

# spec01: lsp contributes symbols usages and calls to asp

Base revision: `c09ab1a92c375b5ef0e5db495ef6b49227d45c78`.

## Change

1. `src/asp/` is the provider: `outline.rs`, `places.rs`, `expand_file.rs`, `expand_symbol.rs`, `search.rs`, and `mod.rs` (the `asp.lsp` entry).
2. `src/client.rs` adds `workspace_symbol`, call hierarchy and the matching client capabilities.
3. `cartridge.json` declares `asp.lsp` and the `asp` block; `init.lua` listens; README and help describe it.

## Acceptance

- [x] `expanding_a_file_yields_symbols_with_spans_and_signatures_and_contains_edges`
- [x] `a_bare_name_resolves_through_search_to_its_symbol_and_calls_walk_two_levels`
- [x] `the_outline_is_one_compact_line_per_symbol_with_no_raw_lsp`

## Verify

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/lsp-asp-verify}"
LOG="$CARGO_TARGET_DIR/lsp-asp.log"
mkdir -p "$CARGO_TARGET_DIR"
if ! env -u CARTRIDGE_YOLO cargo test > "$LOG" 2>&1; then
	tail -40 "$LOG" >&2
	echo "the suite does not pass" >&2
	exit 1
fi
for name in expanding_a_file_yields_symbols_with_spans_and_signatures_and_contains_edges a_bare_name_resolves_through_search_to_its_symbol_and_calls_walk_two_levels the_outline_is_one_compact_line_per_symbol_with_no_raw_lsp; do
	if ! grep -q "::$name \.\.\. ok" "$LOG"; then
		echo "a named test did not run and pass" >&2
		exit 1
	fi
done
```
