---
complexity: moderate
footprint:
  - "src/asp/mod.rs"
  - "docs/asp.txt"
  - ".cartridge/tests/unit/src/asp.rs"
---

# spec01: asp search keeps the edges between its hits

Base revision: `a2c59624f710afb0cef2278534c55ba5199e2a9f`.

## Change

1. `src/asp/mod.rs`: `asp_search` links the admitted edges into the world and returns those whose two ends are both among the hits.

## Acceptance

- [x] `search_ranks_what_the_providers_found_with_the_fabrics_formula`

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
for name in search_ranks_what_the_providers_found_with_the_fabrics_formula; do
	if ! grep -q "::$name \.\.\. ok" "$LOG"; then
		echo "a named test did not run and pass" >&2
		exit 1
	fi
done
```
