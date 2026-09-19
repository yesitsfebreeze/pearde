---
complexity: moderate
footprint:
  - "src/asp/own.rs"
  - "src/asp/ask.rs"
  - "src/asp/mod.rs"
  - "src/host/mod.rs"
  - "docs/asp.txt"
  - ".cartridge/tests/unit/src/asp/base.rs"
---

# spec01: the host's cartridge entities carry state and generation

Base revision: `324f36e35f1c15aad5e2e4e7e3fa8e9d869d7e33`.

## Change

1. `src/host/mod.rs`: `Host::roster` lists every slot with its state, generation and error.
2. `src/asp/own.rs`: `Member`, `member_node`, the `host.state` and `host.error` attributes, and a `cartridge:` node for every roster member; search matches a cartridge by id.
3. `src/asp/ask.rs` passes the roster to the base's answer.

## Acceptance

- [x] `the_base_contributes_every_tool_and_cartridge_and_lists_every_event_as_a_type`

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
for name in the_base_contributes_every_tool_and_cartridge_and_lists_every_event_as_a_type; do
	if ! grep -q "::$name \.\.\. ok" "$LOG"; then
		echo "a named test did not run and pass" >&2
		exit 1
	fi
done
```
