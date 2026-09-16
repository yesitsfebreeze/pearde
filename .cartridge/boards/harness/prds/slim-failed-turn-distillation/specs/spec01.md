---
complexity: medium
footprint:
  - src/lib.rs
  - cartridge.json
  - Cargo.toml
  - .cartridge/tests/integration/slim.rs
---

# spec01 — the ring call distils a named failed tool-using run into one memory line

Spec for the leaf @harness/slim-failed-turn-distillation. Base: harness.ctg 9c144a3. No new dependency. The live trigger (agent naming `session`/`run` on its ring call) is the standalone agent-board PRD, with no `needs` either way: harness ignores unknown ring args today and an unnamed ring stays unchanged, so either lands first.

Lane prerequisites: `../memo.ctg` (path dep `evidence`) resolves via the lane's sibling symlink. The integration test boots the base from `CARTRIDGE_BIN`, else `../cartridge.ctg/target/release/cartridge`, so the Verify block pins `CARTRIDGE_BIN` to the built host.

## Steps

1. `cartridge.json` settings: add `"slim": {"type":"boolean","default":true,"doc":"Distil a failed tool-using run named on the ring call into one memory line; false stores nothing."}`. `src/lib.rs` `Config`: add `slim: bool` (deny_unknown_fields, so it is required; `declared_config()` picks it up).
2. `src/lib.rs`: `fn slim_line(transcript:&str, session:&str, run:&str) -> Option<String>`, pure. Over JSONL records with `run == run`: tools = unique `tool` of `kind:"tool_finished"` (first 8, then `…`); failed = any `result.error == true` or `run_finished.phase == "failed"`; none if no tool or not failed. Closing statement = last assistant `message.content` string of the run, whitespace-flattened, cut at 120 chars; else `failed k/n tool calls`. Line: `slim failed turn {session} {run}: {tools} -> {outcome}`.
3. `ring(host, config, args)`: before the sweep, when `config.slim && !config.memory.is_empty()` and `args.session`/`args.run` are strings, `sessions get` + `read_transcript`, then `slim_line`; on `Some`, ingest `{op:"ingest",text,sync:true}` and require `status == "committed"`. Any error: `eprintln!("harness: slim: {e}")` and put it under reply key `slim` (`{"stored":bool}` or `{"error":..}`); never return `Err`. Dispatch passes `&args` (`lib.rs` ~1570).
4. `.cartridge/tests/integration/slim.rs` + `[[test]] name="slim"` in `Cargo.toml`, modelled on `ring.rs` (fixture sessions/buffers/memo/router/memory/control; `ring_keep` high so the sweep evicts nothing). The fixture memory keeps ingests and answers `{op:"query",text}` by substring. Cases: failed tool run -> exactly one ingest, one line, found by `query "slim"`, naming the tool and closing text; successful tool run -> 0; tool-free failed run -> 0; bank refusal -> reply has `slim.error`, sweep keys present, call is Ok; `slim=false` base -> 0; ring without session -> 0 and reply unchanged.
5. Unit test for `slim_line` (multi-run transcript picks only the named run; truncation) in `.cartridge/tests/unit/main/tests.rs` is optional; add the path to the footprint if used.

## Acceptance

- [ ] `cargo test --test slim` passes: a named failed tool-using run yields exactly one ingested line `slim failed turn <session> <run>: <tools> -> <closing statement>`, returned by the fixture bank's `query`.
- [ ] The same test asserts zero ingests for a successful tool run, a tool-free failed run, `slim = false`, empty `memory`, and a ring call without `session`/`run` (whose reply equals today's).
- [ ] The same test asserts a refused ingest returns an Ok ring reply carrying `slim.error` alongside the sweep keys.
- [ ] `cartridge.json` declares `slim` as a boolean defaulting to true (python check below).
- [ ] `cargo fmt --all -- --check` and `cargo clippy --all-targets -- -D warnings` pass in the lane (what `just check harness` runs via `.cartridge/memos/routine/cartridge-development.md`).
- [ ] Post-integration owner gate, from `/Users/feb/dev/cartridge`: `just check harness` and `just test harness` pass.

## Verify

```sh
cargo fmt --all -- --check
```

```sh
cargo clippy --all-targets -- -D warnings
```

```sh
CARTRIDGE_BIN="${CARTRIDGE_BIN:-/Users/feb/dev/cartridge/cartridge.ctg/target/release/cartridge}" cargo test --test slim
```

```sh
python3 -c 'import json,sys; s=json.load(open("cartridge.json"))["settings"]["slim"]; sys.exit(0 if s["type"]=="boolean" and s["default"] is True else 1)'
```

Measured on base 9c144a3 (scratch worktree, fresh CARGO_TARGET_DIR, kache rustc wrapper): `cargo test --test ring` cold 6 s, after touching `src/lib.rs` 1 s; clippy 2 s; fmt <1 s. `slim` does not exist yet; it mirrors `ring`.
