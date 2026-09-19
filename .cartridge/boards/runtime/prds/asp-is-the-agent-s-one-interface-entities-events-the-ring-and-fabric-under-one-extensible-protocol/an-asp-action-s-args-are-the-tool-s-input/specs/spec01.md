---
complexity: moderate
footprint:
  - "src/asp/mod.rs"
  - "src/asp/protocol.rs"
  - "docs/asp.txt"
  - ".cartridge/tests/unit/src/asp.rs"
---

# spec01: an asp action's args are the tool's input

Base revision: `5980c7cfc13f89dfc49ec38ba8e785b42c8a1a61`.

## Change

1. `src/asp/mod.rs`: `act` sends `{op: "call", input: args}` to the tool event.
2. `src/asp/protocol.rs` and `docs/asp.txt` state that `args` is the tool's input.

## Acceptance

- [x] `an_action_runs_through_its_tool_and_a_denial_reaches_the_caller_unchanged`

## Verify

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/asp-core-verify}"
LOG="$CARGO_TARGET_DIR/asp-core.log"
mkdir -p "$CARGO_TARGET_DIR"
if ! env -u CARTRIDGE_YOLO cargo test --lib -- --test-threads=4 > "$LOG" 2>&1; then
	tail -40 "$LOG" >&2
	echo "the suite does not pass" >&2
	exit 1
fi
for name in an_action_runs_through_its_tool_and_a_denial_reaches_the_caller_unchanged; do
	if ! grep -q "::$name \.\.\. ok" "$LOG"; then
		echo "a named test did not run and pass" >&2
		exit 1
	fi
done
```
