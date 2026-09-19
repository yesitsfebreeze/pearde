---
complexity: simple
footprint:
  - "src/asp/mod.rs"
  - "src/asp/rank.rs"
  - "src/host/mod.rs"
  - "src/host/plan.rs"
  - "docs/asp.txt"
  - ".cartridge/tests/unit/src/asp.rs"
---

# spec01: the base's plan declares an asp block and answers in process

Base revision: `804a08b63fd44a3fc1f473ce25d1fc789bedc262`.

## Change

1. `src/asp/mod.rs`: `own_types` is the base's declaration, `own_answer` its
   answer to an expand or a search, and `asp_ask` answers the provider `host`
   in process instead of sending an event. `types` lists every declared event.
2. `src/host/plan.rs`: the base's plan carries `own_types`.
3. `src/host/mod.rs`: `participants` replaces `active_plans` and puts the
   base's plan first.
4. `src/asp/rank.rs`: `matches`, so the base's search returns only what the
   query's words name.

## Acceptance

- [x] `the_base_contributes_every_tool_and_cartridge_and_lists_every_event_as_a_type`

## Verify

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/asp-core-verify}"
LOG="$CARGO_TARGET_DIR/base-contributes.log"
mkdir -p "$CARGO_TARGET_DIR"
if ! env -u CARTRIDGE_YOLO cargo test --lib -- --test-threads=4 > "$LOG" 2>&1; then
	tail -40 "$LOG" >&2
	echo "the library suite does not pass" >&2
	exit 1
fi
if ! grep -q "::the_base_contributes_every_tool_and_cartridge_and_lists_every_event_as_a_type \.\.\. ok" "$LOG"; then
	echo "the named test did not run and pass" >&2
	exit 1
fi
```
