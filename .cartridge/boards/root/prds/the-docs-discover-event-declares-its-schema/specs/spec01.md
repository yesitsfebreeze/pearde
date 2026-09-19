---
complexity: small
footprint:
  - cartridge.json
---

# spec01 — docs.discover declares the payload it takes: none

## Premise at HEAD 7e2d752

docs.ctg commit 282aacc (2026-09-17) already added `"schema": {}` to
`docs.discover`, and `just audit` now passes docs.ctg (`18 of 18 cartridges pass
the hard checks`). That covers box 3 only. `{}` accepts every JSON value, so no
call can violate it, and box 2 cannot hold. Box 1 does not hold either: the handler
(`src/lib.rs` `fn announce(_: &Lua, (): ())`) reads no payload, but the schema
does not say so.

Callers send `null` by default: `cartridge call|send|run` default `data` to
`"null"`, and `cartridge verify` sends the `contracts` entry `docs.discover`
with `Value::Null` (`cartridge.ctg/src/host/run.rs` run_contracts). The host checks
each payload in `transport/cartridge.rs` `validate` (jsonschema 0.56.0) before the
handler runs, and refuses a bad one with "`<name>` payload rejected by its schema".

## Change

In `cartridge.json`, change only `events["docs.discover"].schema` to:

```json
"schema": {
  "type": ["null", "object"],
  "additionalProperties": false
}
```

(no payload, or an empty object; the event has no fields, so none are optional).
Leave the description and every other key as they are. Keep the file's 2-space
formatting. For example:
`jq --indent 2 '.events["docs.discover"].schema = {"type":["null","object"],"additionalProperties":false}'`
touches only those lines.

This is deliberately stricter than the house `"schema": {}` that harness, fs and
tools use for their no-payload events. `{}` accepts every value, so PRD box 2 (a
violating call is refused) would be vacuous. Aligning those siblings is out of
scope here.

## Acceptance

- [x] `docs.discover`'s schema accepts `null` and `{}`, and refuses any object
      with a field, a string, a number and an array. The host's own validator
      crate (jsonschema =0.56.0) checks this against `cartridge.json`.
- [x] Every event in `cartridge.json` still carries a `description` and an
      object `schema`, so the audit's `declares no schema` rule stays green.

The PRD's box 2 (the host refuses a violating call against the declaration)
follows from two things. First, block 1 below proves the declaration refuses those
payloads with the host's own crate, version, features and draft detection
(`validator_for`, no `$schema`). Second, the host's existing tests
(cartridge.ctg `src/transport/tests/cartridge.rs`, `rejected by its schema`) show
that `validate` runs before a listener. No docs call is executed, because that
would need the shared daemon.

## Collect hazard and recovery

Changing `docs.ctg/cartridge.json` changes its trusted hash, so the shared daemon
drops docs (tool.docs, docs.available) until it is re-trusted.

Collect only when nothing depends on docs. Consumers that declare it, found as of
2026-09-19 by the command below, are `live.ctg` (a hard `needs: tool.docs`) and
agent sessions that call `tool.docs` through the shared host. Re-check the list
right before collect, excluding docs.ctg's own manifest:

    cd /Users/feb/dev/cartridge && for f in */cartridge.json; do jq -r --arg f "$f" '[(.needs // [])[]?, (.listen // [])[]] | map(select(test("^(tool\\.)?docs"))) | select(length>0) | "\($f): \(join(","))"' "$f"; done

The coordinator then messages every other active session (a live voice session
runs live.ctg) before collect, and collects only once they have agreed.

After collect:

1. Re-trust only the edited cartridge:
   `cartridge trust /Users/feb/dev/cartridge/docs.ctg`. Never trust the
   superproject path. That would silently approve other sessions' uncommitted
   `.lua` and `cartridge.json` edits.
2. `cartridge reload docs`, then `cartridge status`. If docs still is not active,
   stop and report. Never run `cartridge daemon --replace`: it swaps the host that
   every session shares, and is a last resort only when agreed with the other
   sessions.
3. From `docs.ctg`: `env -u CARTRIDGE_YOLO cartridge verify docs.ctg`. It should
   print `1 contracts passed`, which confirms that the `null` contract call is
   still accepted. It uses a private host, not the daemon.

## Verify

Precondition for block 1: it builds offline, so the jsonschema 0.56.0 dependency
tree must be in the local cargo registry. It is there because cartridge.ctg
builds it. A failure that reads "no matching package" or "failed to download" is
environmental, not a verdict on the change. Recover by running
`cargo fetch --manifest-path ../cartridge.ctg/Cargo.toml` outside the block, then
re-run collect.

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/docs-discover-schema-verify}"
probe="$(mktemp -d)"
trap 'rm -rf "$probe"' EXIT
mkdir -p "$probe/src"
cat > "$probe/Cargo.toml" <<'EOF'
[package]
name = "docs-discover-schema-probe"
version = "0.0.0"
edition = "2021"

[dependencies]
jsonschema = { version = "=0.56.0", default-features = false }
serde_json = "1"
EOF
cat > "$probe/src/main.rs" <<'EOF'
use serde_json::{json, Value};
fn main() {
	let path = std::env::args().nth(1).expect("manifest path");
	let manifest: Value = serde_json::from_str(&std::fs::read_to_string(&path).unwrap()).unwrap();
	let schema = manifest["events"]["docs.discover"].get("schema").expect("docs.discover declares a schema");
	let validator = jsonschema::validator_for(schema).expect("the schema compiles as the host compiles it");
	let mut bad = 0;
	for (payload, accept) in [
		(Value::Null, true),
		(json!({}), true),
		(json!({"force": true}), false),
		(json!("again"), false),
		(json!(1), false),
		(json!([]), false),
	] {
		let ok = validator.is_valid(&payload);
		println!("{payload} -> {}", if ok { "accepted" } else { "refused" });
		if ok != accept { eprintln!("expected {payload} to be {}", if accept { "accepted" } else { "refused" }); bad += 1; }
	}
	if bad > 0 { std::process::exit(1); }
}
EOF
cargo run --offline --quiet --manifest-path "$probe/Cargo.toml" -- "$PWD/cartridge.json"
```

```sh
jq -e '[.events[] | select((.description | type) != "string" or (.schema | type) != "object")] | length == 0' cartridge.json
```

## Review notes carried into collect (round 3, clarification only)

- Before the trust step, `git -C /Users/feb/dev/cartridge/docs.ctg status --short` must print nothing;
  otherwise the trust would approve another session's uncommitted docs.ctg edits. Stop and report.
- After `cartridge reload docs`, `cartridge status` must show both `docs` and `live` active (live hard-needs
  `tool.docs`). If live is not active, report it; do not reload live.
- Run the recovery commands with `</dev/null` so no interactive trust prompt (which defaults to Yes under
  YOLO) can approve the whole repository.

