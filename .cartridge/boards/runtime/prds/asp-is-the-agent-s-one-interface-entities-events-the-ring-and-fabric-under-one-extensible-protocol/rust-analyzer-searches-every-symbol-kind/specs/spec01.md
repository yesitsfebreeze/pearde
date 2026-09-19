---
complexity: moderate
footprint:
  - "src/client.rs"
---

# spec01: rust-analyzer searches every symbol kind

Base revision: `2e0e6edfceee1c605776fd37f14e334bd06160c9`.

## Change

1. `src/client.rs`: `initializationOptions` for rust-analyzer only.

## Acceptance

- [x] `a_method_is_found_by_its_words_and_every_key_it_is_given_expands`

## Verify

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/lsp-kinds-verify}"
LOG="$CARGO_TARGET_DIR/lsp-kinds.log"
mkdir -p "$CARGO_TARGET_DIR"
if ! env -u CARTRIDGE_YOLO cargo test --lib asp_tests > "$LOG" 2>&1; then
	tail -40 "$LOG" >&2
	echo "the suite does not pass" >&2
	exit 1
fi
for name in a_method_is_found_by_its_words_and_every_key_it_is_given_expands; do
	if ! grep -q "::$name \.\.\. ok" "$LOG"; then
		echo "a named test did not run and pass" >&2
		exit 1
	fi
done
```
