---
complexity: moderate
footprint:
  - "src/asp/mod.rs"
  - "src/host/plan.rs"
  - "src/host/mod.rs"
  - "src/host/socket.rs"
  - "docs/asp.txt"
  - "docs/transport.txt"
  - ".cartridge/tests/unit/src/asp.rs"
  - ".cartridge/tests/unit/src/tests/host.rs"
---

# spec01: the base is a participant that owns tool.asp

Base revision: `7af748a7a59d0daf65d1aa9545aeaa076272a74a`.

## Change

1. `src/host/plan.rs`: `HOST`, `host_plan()`, the glob sees the base's
   listens, and a listener address for `host` is the host socket.
2. `src/host/mod.rs`: `rewire` puts the base's plan first in both plan lists,
   `start_ready` counts the base as active, `bail` answers `tool.asp`, and
   `caller` accepts a token minted for the edge to `host`.
3. `src/host/socket.rs`: serves `event` for `tool.asp`, and refuses `act` to
   a cartridge.
4. `src/asp/mod.rs`: `TOOL` and `Host::asp_tool`, the tool envelope.
5. Two assertions in `tests/host.rs` now expect `tool.asp` among the needs a
   `tool.*` glob yields.

## Acceptance

- [x] `a_cartridge_that_needs_tools_finds_asp_among_them`
- [x] `a_cartridge_cannot_run_an_action_through_asp`
- [x] The whole library suite passes, which holds the two updated glob tests.

## Verify

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/asp-core-verify}"
LOG="$CARGO_TARGET_DIR/tool-asp.log"
mkdir -p "$CARGO_TARGET_DIR"
if ! env -u CARTRIDGE_YOLO cargo test --lib -- --test-threads=4 > "$LOG" 2>&1; then
	tail -40 "$LOG" >&2
	echo "the library suite does not pass" >&2
	exit 1
fi
for name in a_cartridge_that_needs_tools_finds_asp_among_them a_cartridge_cannot_run_an_action_through_asp a_glob_in_needs_names_what_the_others_listen_to; do
	if ! grep -q "::$name \.\.\. ok" "$LOG"; then
		echo "a named test did not run and pass" >&2
		exit 1
	fi
done
```
