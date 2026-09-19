---
complexity: moderate
footprint:
  - "src/service.rs"
  - "README.md"
  - ".cartridge/help.md"
  - ".cartridge/docs/README.md"
---

# spec01: live reads the composition from asp

Base revision: `dbd3b0af89549ce152a936f3d127817ab374dacd`.

## Change

1. `src/service.rs`: `composition()` groups ASP `types` events by owner; the `fabric` names become `composition`.
2. README, help and docs README name ASP `types`.

## Acceptance

- [x] `the_voice_session_is_told_what_the_record_says`

## Verify

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/live-fabric-verify}"
LOG="$CARGO_TARGET_DIR/live-fabric.log"
mkdir -p "$CARGO_TARGET_DIR"
if ! env -u CARTRIDGE_YOLO cargo test --lib > "$LOG" 2>&1; then
	tail -40 "$LOG" >&2
	echo "the suite does not pass" >&2
	exit 1
fi
for name in the_voice_session_is_told_what_the_record_says; do
	if ! grep -q "::$name \.\.\. ok" "$LOG"; then
		echo "a named test did not run and pass" >&2
		exit 1
	fi
done
```
