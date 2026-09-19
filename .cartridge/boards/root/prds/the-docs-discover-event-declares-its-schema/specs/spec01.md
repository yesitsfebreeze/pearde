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

## Acceptance

- [ ] `docs.discover`'s schema accepts `null` and `{}`, and refuses any object
      with a field, a string, a number and an array. The host's own validator
      crate (jsonschema =0.56.0) checks this against `cartridge.json`.
- [ ] Every event in `cartridge.json` still carries a `description` and an
      object `schema`, so the audit's `declares no schema` rule stays green.

## Verify

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/docs-discover-schema-verify}"
probe="$(mktemp -d)"
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
jq -e '.events["docs.discover"].schema | type == "object"' cartridge.json
jq -e '[.events[] | select((.description | type) != "string" or (.schema | type) != "object")] | length == 0' cartridge.json
```
