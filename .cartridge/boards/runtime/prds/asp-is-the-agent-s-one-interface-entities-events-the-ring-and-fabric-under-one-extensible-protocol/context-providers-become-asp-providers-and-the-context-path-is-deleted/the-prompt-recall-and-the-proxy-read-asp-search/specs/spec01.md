---
complexity: moderate
footprint:
  - ".cartridge/docs/README.md"
  - ".cartridge/docs/context.md"
  - ".cartridge/help.md"
  - ".cartridge/tests/unit/context.rs"
  - ".cartridge/tests/unit/tests.rs"
  - "README.md"
  - "cartridge.json"
  - "src/context.rs"
  - "src/evidence.rs"
  - "src/lib.rs"
  - "src/service.rs"
---

# spec01: the prompt recall and the proxy read asp search

Base revision: `b85828947c5ad28fc841826e07f972045cdd4cac`.

## Change

1. Proxy's recall asks the host's `asp` service `{op:"search", query, limit: context_limits.max_rows}` through `cartridge.host` instead of `memo {op:"context",action:"prepare"}`, and injects the ranked hits as whole `id | name | description` lines within `max_rows` and `max_bytes`; nothing is injected when ASP answers nothing.
2. The `cartridge-context/v1` snapshot validation and proxy's copy of the evidence contract are deleted.
3. `context_limits.max_rows` is bounded at 256, ASP's cap. The prompt-recall hook moves to ASP search in cartridge.ctg under its own record.

## Acceptance

- [x] `recall_keeps_ranked_hits_as_whole_lines_within_rows_and_bytes`
- [x] `an_empty_asp_search_injects_nothing`
- [x] `later_round_budget_omits_whole_recall_without_requery`
- [x] `sourced_context_is_user_data_once_per_round_in_all_json_and_sse_wires`
- [x] `optional_failures_and_tight_budgets_preserve_original_valid_requests`

## Verify

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/proxy-asp-verify}"
LOG="$CARGO_TARGET_DIR/proxy-asp.log"
mkdir -p "$CARGO_TARGET_DIR"
if ! env -u CARTRIDGE_YOLO cargo test > "$LOG" 2>&1; then
	tail -40 "$LOG" >&2
	echo "the suite does not pass" >&2
	exit 1
fi
for name in recall_keeps_ranked_hits_as_whole_lines_within_rows_and_bytes an_empty_asp_search_injects_nothing later_round_budget_omits_whole_recall_without_requery sourced_context_is_user_data_once_per_round_in_all_json_and_sse_wires optional_failures_and_tight_budgets_preserve_original_valid_requests; do
	if ! grep -q "::$name \.\.\. ok" "$LOG"; then
		echo "a named test did not run and pass" >&2
		exit 1
	fi
done
```
