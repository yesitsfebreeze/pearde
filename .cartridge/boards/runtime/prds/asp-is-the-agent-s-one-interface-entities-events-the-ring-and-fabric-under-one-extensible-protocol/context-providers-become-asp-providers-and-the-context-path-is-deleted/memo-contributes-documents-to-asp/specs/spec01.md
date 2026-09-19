---
complexity: moderate
footprint:
  - "src/asp_documents.rs"
  - "src/asp.rs"
  - "src/document.rs"
  - "src/lib.rs"
  - "cartridge.json"
  - "README.md"
  - ".cartridge/help.md"
  - ".cartridge/tests/unit/src/asp_documents.rs"
---

# spec01: memo contributes documents to asp

Base revision: `4f8903d56e191cc4bed192813cfa245e49de99f6`.

## Change

1. `src/asp_documents.rs`: the `document:` scheme, keyed by the projection identity `@<owner>/.cartridge/documents/...md`, revision = projection revision, bounded content, private documents never entities; expand and search.
2. `src/asp.rs` routes `document:` and merges document hits into search.
3. `cartridge.json` declares memo the owner of `document:`; README and help describe it.

## Acceptance

- [x] `the_manifest_declares_memo_the_owner_of_the_document_scheme`
- [x] `expanding_a_document_yields_its_projection_revision_and_bounded_content`
- [x] `a_private_or_absent_document_is_never_an_entity`
- [x] `search_ranks_documents_alongside_memos_and_skips_private_ones`

## Verify

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/memo-docs-verify}"
LOG="$CARGO_TARGET_DIR/memo-docs.log"
mkdir -p "$CARGO_TARGET_DIR"
if ! env -u CARTRIDGE_YOLO cargo test --lib -- --test-threads=2 > "$LOG" 2>&1; then
	tail -40 "$LOG" >&2
	echo "the suite does not pass" >&2
	exit 1
fi
for name in the_manifest_declares_memo_the_owner_of_the_document_scheme expanding_a_document_yields_its_projection_revision_and_bounded_content a_private_or_absent_document_is_never_an_entity search_ranks_documents_alongside_memos_and_skips_private_ones; do
	if ! grep -q "::$name \.\.\. ok" "$LOG"; then
		echo "a named test did not run and pass" >&2
		exit 1
	fi
done
```
