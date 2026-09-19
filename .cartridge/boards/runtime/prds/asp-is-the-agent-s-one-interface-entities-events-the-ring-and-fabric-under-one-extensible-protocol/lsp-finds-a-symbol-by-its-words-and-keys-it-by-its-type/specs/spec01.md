---
complexity: moderate
footprint:
  - "src/asp/outline.rs"
  - "src/asp/search.rs"
  - "src/asp/mod.rs"
  - "README.md"
  - ".cartridge/help.md"
  - ".cartridge/tests/unit/asp.rs"
---

# spec01: lsp finds a symbol by its words and keys it by its type

Base revision: `c5f3f4df58a0e6a7d64b5f1cf881f5a1764cb805`.

## Change

1. `src/asp/outline.rs`: `container()` normalizes a container before it enters a key.
2. `src/asp/search.rs`: whole query plus up to four words, merged by id, exact name first.

## Acceptance

- [x] `a_method_is_found_by_its_words_and_every_key_it_is_given_expands`
- [x] `expanding_a_file_yields_symbols_with_spans_and_signatures_and_contains_edges`
- [x] `the_outline_is_one_compact_line_per_symbol_with_no_raw_lsp`

## Verify

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/lsp-words-verify}"
LOG="$CARGO_TARGET_DIR/lsp-words.log"
mkdir -p "$CARGO_TARGET_DIR"
if ! env -u CARTRIDGE_YOLO cargo test --lib asp_tests > "$LOG" 2>&1; then
	tail -40 "$LOG" >&2
	echo "the suite does not pass" >&2
	exit 1
fi
for name in a_method_is_found_by_its_words_and_every_key_it_is_given_expands expanding_a_file_yields_symbols_with_spans_and_signatures_and_contains_edges the_outline_is_one_compact_line_per_symbol_with_no_raw_lsp; do
	if ! grep -q "::$name \.\.\. ok" "$LOG"; then
		echo "a named test did not run and pass" >&2
		exit 1
	fi
done
```
