---
complexity: simple
footprint:
  - "src"
  - ".cartridge/tests/unit"
  - ".cartridge/help.md"
  - "README.md"
---

# spec01: references carries its context, and clients are keyed by root

Base revision: `31450e163f4885d27df77c0baf683e9a5e4d1575`.

## Change

1. `src/client.rs`: `position_params` builds the params of a position query
   and adds `context: {includeDeclaration: true}` for
   `textDocument/references`. `Client::query` sends what it returns.
2. `src/service.rs`: the client map is keyed by `(server id, workspace root)`.
   A hit refreshes the LRU stamp. Eviction and `status` follow the new key.
3. `src/catalog.rs`: `status_json` reports `roots` per server, and `running`
   is true when that list is not empty.
4. `.cartridge/tests/unit/live.rs` holds the live test. It needs rust-analyzer
   in the install cache and fails, rather than skips, without it.

## Acceptance

- [x] `references_request_carries_include_declaration` passes.
- [x] `references_finds_call_sites_and_each_crate_root_gets_its_own_client`
      passes against the live rust-analyzer.

## Verify

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/lsp-references-verify}"
LOG="$CARGO_TARGET_DIR/suite.log"
mkdir -p "$CARGO_TARGET_DIR"
if ! env -u CARTRIDGE_YOLO cargo test > "$LOG" 2>&1; then
	tail -40 "$LOG" >&2
	echo "the lsp suite does not pass" >&2
	exit 1
fi
for name in references_request_carries_include_declaration references_finds_call_sites_and_each_crate_root_gets_its_own_client; do
	if ! grep -q "::$name \.\.\. ok" "$LOG"; then
		echo "a named test did not run and pass" >&2
		exit 1
	fi
done
```
