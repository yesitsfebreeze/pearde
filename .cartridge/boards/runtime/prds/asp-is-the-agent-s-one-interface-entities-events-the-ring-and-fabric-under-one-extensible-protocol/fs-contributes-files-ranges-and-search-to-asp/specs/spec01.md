---
complexity: moderate
footprint:
  - ".cartridge/help.md"
  - "README.md"
  - "cartridge.json"
  - "init.lua"
  - "src/files.rs"
  - "src/lib.rs"
  - "src/search.rs"
  - "src/asp"
  - ".cartridge/tests/unit/asp.rs"
---

# spec01: fs contributes files ranges and search to asp

Base revision: `fc8314ef709d2e2ba663cf2245e486ef907aa8f2`.

## Change

1. `src/asp/` is the provider: `identity.rs` (file and range keys and nodes), `expand.rs`, `find.rs` (search with `matches` edges), `mod.rs` (the `asp.fs` entry).
2. `files::resolve` and `search::grep_paths` become `pub` and are reused as they are.
3. `cartridge.json` declares `asp.fs` and the `asp` block; `init.lua` listens; README and help describe it.

## Acceptance

- [x] `a_file_entity_expands_to_its_node_with_a_sha256_revision`
- [x] `search_answers_matches_edges_to_ranges_with_exact_lines_and_columns`
- [x] `editing_a_file_changes_the_revision_fs_answers`

## Verify

The Verify block runs fs's ASP tests only. fs's whole suite takes about 115 s
on a loaded machine, against the engine's 120 s limit, and one of its search
tests holds a 2 s deadline that load alone can miss. The whole suite passed
under `just test fs` on 2026-09-19 with these changes in the tree.

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/fs-asp-verify}"
LOG="$CARGO_TARGET_DIR/fs-asp.log"
mkdir -p "$CARGO_TARGET_DIR"
if ! env -u CARTRIDGE_YOLO cargo test --lib asp:: > "$LOG" 2>&1; then
	tail -40 "$LOG" >&2
	echo "the suite does not pass" >&2
	exit 1
fi
for name in a_file_entity_expands_to_its_node_with_a_sha256_revision search_answers_matches_edges_to_ranges_with_exact_lines_and_columns editing_a_file_changes_the_revision_fs_answers; do
	if ! grep -q "::$name \.\.\. ok" "$LOG"; then
		echo "a named test did not run and pass" >&2
		exit 1
	fi
done
```
