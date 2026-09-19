---
complexity: moderate
footprint:
  - "src/cli/client.rs"
  - "docs/transport.txt"
---

# spec01: cartridge call prints a text answer as text

Base revision: `f56c442b19ba31672e8b66aff58f25a090b750a4`.

## Change

1. `src/cli/client.rs`: `ask` prints `Value::String` raw.

## Acceptance

- [x] The `cartridge` binary builds with the change.

## Verify

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/cli-text-verify}"
LOG="$CARGO_TARGET_DIR/cli-text.log"
mkdir -p "$CARGO_TARGET_DIR"
if ! env -u CARTRIDGE_YOLO cargo build --bin cartridge > "$LOG" 2>&1; then
	tail -40 "$LOG" >&2
	echo "the suite does not pass" >&2
	exit 1
fi
for name in ; do
	if ! grep -q "::$name \.\.\. ok" "$LOG"; then
		echo "a named test did not run and pass" >&2
		exit 1
	fi
done
```
