---
complexity: moderate
footprint:
  - "src/asp"
  - "src/lib.rs"
  - "src/loader/document.rs"
  - "src/host/plan.rs"
  - "src/host/mod.rs"
  - "src/host/socket.rs"
  - "docs/asp.txt"
  - "docs/transport.txt"
  - "docs/architecture.txt"
  - "docs/creating-cartridges.txt"
  - "llms.txt"
  - ".cartridge/help.md"
  - ".cartridge/tests/unit/src/asp.rs"
  - ".cartridge/tests/unit/src/host/plan.rs"
---

# spec01: the host serves asp from the types its cartridges declare

Base revision: `3be97455cfca893f991fdb08954acf60aa6e70c7`.

## Change

1. `src/asp/protocol.rs` is the wire: the `asp` manifest block
   (`Declaration`), what a provider answers (`Asserted`, `Linked`) and what
   ASP gives back (`Node`, `Edge`, `Assertion`, `Source`, `Bound`).
   `Declaration::problem` states why a block cannot load.
2. `src/loader/document.rs` adds `asp` to `Cartridge` and `Declared`, checks
   it, and refuses `asp` as an event name. `src/host/plan.rs` carries it on
   `Plan`.
3. `src/asp/mod.rs` builds the registry from the active plans on every
   request and implements `Host::asp`: `types`, `expand` (fan-out, admission
   against the declaration, merge, stale marking, depth and limit), `search`,
   `actions` and `act`.
4. `src/asp/rank.rs` is the fabric's ranking formula over ASP nodes.
5. `src/host/mod.rs` answers the `bail` key `asp` and exposes
   `active_plans`. `src/host/socket.rs` serves the `asp` method and grants it
   to cartridges.
6. `docs/asp.txt` is the protocol. The help page, the README, `llms.txt`,
   `transport.txt`, `architecture.txt` and `creating-cartridges.txt` point to it.

## Acceptance

- [x] `unloading_a_provider_removes_its_types_and_facts_and_keeps_the_rest`
- [x] `a_node_two_providers_assert_survives_one_of_them`
- [x] `a_fact_behind_the_owners_revision_is_marked_stale`
- [x] `an_undeclared_edge_kind_refuses_the_provider_by_name`
- [x] `an_action_runs_through_its_tool_and_a_denial_reaches_the_caller_unchanged`
- [x] `search_ranks_what_the_providers_found_with_the_fabrics_formula`
- [x] `a_cartridge_reaches_asp_through_the_host`
- [x] `a_manifest_refuses_an_asp_block_it_cannot_serve`

## Verify

The target directory is shared with the implementer's own runs, so the build
is warm and fits the engine's time limit.

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/asp-core-verify}"
LOG="$CARGO_TARGET_DIR/asp.log"
mkdir -p "$CARGO_TARGET_DIR"
if ! env -u CARTRIDGE_YOLO cargo test --lib asp:: > "$LOG" 2>&1; then
	tail -40 "$LOG" >&2
	echo "the asp tests do not pass" >&2
	exit 1
fi
for name in unloading_a_provider_removes_its_types_and_facts_and_keeps_the_rest a_node_two_providers_assert_survives_one_of_them a_fact_behind_the_owners_revision_is_marked_stale an_undeclared_edge_kind_refuses_the_provider_by_name an_action_runs_through_its_tool_and_a_denial_reaches_the_caller_unchanged search_ranks_what_the_providers_found_with_the_fabrics_formula a_cartridge_reaches_asp_through_the_host a_manifest_refuses_an_asp_block_it_cannot_serve; do
	if ! grep -q "::$name \.\.\. ok" "$LOG"; then
		echo "a named asp test did not run and pass" >&2
		exit 1
	fi
done
```
