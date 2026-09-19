---
complexity: moderate
footprint:
  - "src/asp"
  - ".cartridge/tests/unit/src/asp.rs"
  - ".cartridge/tests/unit/src/asp"
---

# spec01: asp is one file per responsibility

Base revision: `2ea1aae611499b3210b6c363b55d56c2d20853a7`.

## Change

1. Move each responsibility of `src/asp/mod.rs` into its own file; only visibility changes.
2. Move the ASP tests into `.cartridge/tests/unit/src/asp/`, one file per behaviour, with the fixture providers in its `mod.rs`.

## Acceptance

- [x] `unloading_a_provider_removes_its_types_and_facts_and_keeps_the_rest`
- [x] `a_node_two_providers_assert_survives_one_of_them`
- [x] `a_fact_behind_the_owners_revision_is_marked_stale`
- [x] `an_undeclared_edge_kind_refuses_the_provider_by_name`
- [x] `an_action_runs_through_its_tool_and_a_denial_reaches_the_caller_unchanged`
- [x] `search_ranks_what_the_providers_found_with_the_fabrics_formula`
- [x] `a_cartridge_reaches_asp_through_the_host`
- [x] `a_cartridge_that_needs_tools_finds_asp_among_them`
- [x] `a_cartridge_cannot_run_an_action_through_asp`
- [x] `the_base_contributes_every_tool_and_cartridge_and_lists_every_event_as_a_type`
- [x] `a_manifest_refuses_an_asp_block_it_cannot_serve`

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
for name in unloading_a_provider_removes_its_types_and_facts_and_keeps_the_rest a_node_two_providers_assert_survives_one_of_them a_fact_behind_the_owners_revision_is_marked_stale an_undeclared_edge_kind_refuses_the_provider_by_name an_action_runs_through_its_tool_and_a_denial_reaches_the_caller_unchanged search_ranks_what_the_providers_found_with_the_fabrics_formula a_cartridge_reaches_asp_through_the_host a_cartridge_that_needs_tools_finds_asp_among_them a_cartridge_cannot_run_an_action_through_asp the_base_contributes_every_tool_and_cartridge_and_lists_every_event_as_a_type a_manifest_refuses_an_asp_block_it_cannot_serve; do
	if ! grep -q "::$name \.\.\. ok" "$LOG"; then
		echo "a named test did not run and pass" >&2
		exit 1
	fi
done
```
