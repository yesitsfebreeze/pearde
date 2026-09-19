---
complexity: moderate
footprint:
  - "src/loader/document.rs"
  - "src/host/socket.rs"
  - "src/host/mod.rs"
  - "src/host/plan.rs"
  - "docs/creating-cartridges.txt"
  - "docs/transport.txt"
  - "docs/asp.txt"
  - ".cartridge/tests/unit/src/loader/document.rs"
  - ".cartridge/tests/unit/src/tests/declarations.rs"
  - ".cartridge/tests/unit/src/tests/mod.rs"
  - ".cartridge/tests/unit/fixtures/manifests"
---

# spec01: an event declaration carries a host-validated frame and a cartridge can read its own declared events

Base revision: `e4821bf5ecad81e542047372b81082faa4e5da0b`.

## Change

1. `src/loader/document.rs`: `Event.frame`, a closed enum `message | data | none`, deserialized per event so a bad value is refused naming `events.<kind>` and the value; an event without a frame serializes exactly as before.
2. `src/host/socket.rs`, `src/host/mod.rs`: the `declarations` host method, granted to cartridges, answering the calling node's own declared events; the command line gets an error.
3. ASP `types` carries each event's frame.
4. Fixtures of all 18 current manifests prove every declared event loads unchanged.

## Acceptance

- [x] `every_current_manifest_loads_its_events_unchanged`
- [x] `each_frame_in_the_closed_set_loads`
- [x] `a_frame_outside_the_closed_set_is_refused_naming_its_kind_and_value`
- [x] `a_declaration_without_a_frame_round_trips_unchanged`
- [x] `a_cartridge_reads_its_own_declared_events_and_no_one_elses`

## Verify

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/frame-verify}"
LOG="$CARGO_TARGET_DIR/frame.log"
mkdir -p "$CARGO_TARGET_DIR"
if ! env -u CARTRIDGE_YOLO cargo test --lib -- --test-threads=4 --skip tests::composed > "$LOG" 2>&1; then
	tail -40 "$LOG" >&2
	echo "the suite does not pass" >&2
	exit 1
fi
for name in every_current_manifest_loads_its_events_unchanged each_frame_in_the_closed_set_loads a_frame_outside_the_closed_set_is_refused_naming_its_kind_and_value a_declaration_without_a_frame_round_trips_unchanged a_cartridge_reads_its_own_declared_events_and_no_one_elses; do
	if ! grep -q "::$name \.\.\. ok" "$LOG"; then
		echo "a named test did not run and pass" >&2
		exit 1
	fi
done
```
