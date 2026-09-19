---
complexity: moderate
footprint:
  - ".cartridge/docs/README.md"
  - ".cartridge/docs/context.md"
  - ".cartridge/docs/inventory.md"
  - ".cartridge/docs/source-search.md"
  - ".cartridge/help.md"
  - ".cartridge/memos/note/program-cartridge-contracts.md"
  - ".cartridge/memos/note/program-checks.md"
  - ".cartridge/memos/note/program-map.md"
  - ".cartridge/memos/system/program-entry.md"
  - ".cartridge/tests/integration/inventory.test.ts"
  - ".cartridge/tests/integration/source-search.test.ts"
  - ".cartridge/tests/integration/tests.rs"
  - ".cartridge/tests/unit/source_search.rs"
  - ".cartridge/tests/unit/src/fabric_graph.rs"
  - ".cartridge/tests/unit/src/graph.rs"
  - ".cartridge/tests/unit/src/rank.rs"
  - ".cartridge/tests/unit/src/sources/census.rs"
  - ".cartridge/tests/unit/src/sources/inventory.rs"
  - ".cartridge/tests/unit/src/sources/search.rs"
  - ".cartridge/tests/unit/src/view.rs"
  - "README.md"
  - "cartridge.json"
  - "src/asp.rs"
  - "src/document.rs"
  - "src/fabric_graph.rs"
  - "src/graph.rs"
  - "src/host.rs"
  - "src/inventory.rs"
  - "src/lib.rs"
  - "src/limits.rs"
  - "src/rank.rs"
  - "src/record.rs"
  - "src/service.rs"
  - "src/settings.rs"
  - "src/source_search.rs"
  - "src/sources/census.rs"
  - "src/sources/inventory.rs"
  - "src/sources/limits.rs"
  - "src/sources/mod.rs"
  - "src/sources/search.rs"
  - "src/view.rs"
---

# spec01: memo's fabric is deleted and every caller reads asp

Base revision: `3155a06a194c2dd761a36d12f48de34b58c9c4e6`.

## Change

1. Delete the fabric op, `view.rs`, `inventory.rs`, `source_search.rs`, `sources/{inventory,search,census,limits}.rs`, `fabric_graph.rs` and their tests and docs.
2. `src/rank.rs` holds the journal-weighted record match; `src/graph.rs` holds only the record as a graph.
3. `cartridge.json`: drop `graph.announce`, the `tool.*` and `source.*` needs and the fabric's settings; `src/settings.rs` needs no retired-settings list after that.

## Acceptance

- [x] `the_composition_graph_is_asps_and_memo_answers_no_fabric`
- [x] `search_returns_only_the_nodes_whose_words_match`
- [x] `observed_use_outranks_equal_match`
- [x] `expanding_a_memo_yields_its_node_revision_situations_and_edges_to_what_it_names`

## Verify

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/memo-fabric-verify}"
LOG="$CARGO_TARGET_DIR/memo-fabric.log"
mkdir -p "$CARGO_TARGET_DIR"
if ! env -u CARTRIDGE_YOLO cargo test --lib -- --test-threads=2 > "$LOG" 2>&1; then
	tail -40 "$LOG" >&2
	echo "the suite does not pass" >&2
	exit 1
fi
for name in the_composition_graph_is_asps_and_memo_answers_no_fabric search_returns_only_the_nodes_whose_words_match observed_use_outranks_equal_match expanding_a_memo_yields_its_node_revision_situations_and_edges_to_what_it_names; do
	if ! grep -q "::$name \.\.\. ok" "$LOG"; then
		echo "a named test did not run and pass" >&2
		exit 1
	fi
done
```
