---
complexity: moderate
footprint:
  - "src/asp/mod.rs"
  - "src/asp/render.rs"
  - "src/asp/tool.rs"
  - "src/asp/rank.rs"
  - "src/asp/expand.rs"
  - "docs/asp.txt"
  - ".cartridge/tests/unit/src/asp/doors.rs"
---

# spec01: asp answers agents in compact lines and expands a level at once

Base revision: `445a87fb834c48b6d6d23fc7d1947f202cdd2e43`.

## Change

1. `src/asp/render.rs`: the compact text form.
2. `src/asp/mod.rs`: `format: "text"` on every request.
3. `src/asp/tool.rs`: text and a limit of 20 by default.
4. `src/asp/expand.rs`: each level's subjects asked through a buffered stream of 16.
5. `src/asp/rank.rs`: a node named by every query word ranks first.

## Acceptance

- [x] `a_cartridge_that_needs_tools_finds_asp_among_them`
- [x] `unloading_a_provider_removes_its_types_and_facts_and_keeps_the_rest`
- [x] `a_fact_behind_the_owners_revision_is_marked_stale`

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
for name in a_cartridge_that_needs_tools_finds_asp_among_them unloading_a_provider_removes_its_types_and_facts_and_keeps_the_rest a_fact_behind_the_owners_revision_is_marked_stale; do
	if ! grep -q "::$name \.\.\. ok" "$LOG"; then
		echo "a named test did not run and pass" >&2
		exit 1
	fi
done
```
