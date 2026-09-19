---
complexity: low
footprint:
  - /Users/feb/dev/cartridge/cartridge.ctg/src/trace
  - /Users/feb/dev/cartridge/cartridge.ctg/src/log
  - /Users/feb/dev/cartridge/cartridge.ctg/src/lib.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/cli/mod.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/host/process.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/trace
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/log
  - /Users/feb/dev/cartridge/cartridge.ctg/docs/architecture.txt
---

# spec01 — split src/trace into the correlation id (trace) and the diagnostics sink (log)

Base: cartridge.ctg `324f36e`. This is a move and a path rewrite. Behaviour does not change.
- Live HEAD is now `445a87f`. `git diff --stat 324f36e 445a87f` shows no change in any footprint path; the only change is in `.cartridge/tests/unit/src/asp/base.rs`.
- A probe of exactly this change passed every block below. Its diff covers every step, including `docs/architecture.txt`:
  `prd.ctg/.cartridge/boards/runtime/.state/loop/the-correlation-id-and-the-diagnostics-sink-are-two-folders/analyst-1-probe.patch` (sha256 `325c22f6…134c`).
- `git apply --check` of the patch against the live tree (445a87f plus the dirty files) exits 0.

## Callers (complete at 324f36e)

Searches:
- `git grep 'trace::' 324f36e` in cartridge.ctg.
- `rg 'cartridge::trace|trace::(flush|subscribe|diagnostic|Layer)' --type rust` over every other `*.ctg`. It found no hit. Only memory.ctg depends on the crate, and it uses none of these names.

| Where | Today | After |
|---|---|---|
| `src/cli/mod.rs:38` | `cartridge::trace::flush()` | `cartridge::log::flush()` |
| `src/cli/mod.rs:50` | `cartridge::trace::subscribe()` | `cartridge::log::subscribe()` |
| `src/host/process.rs:173` | `crate::trace::diagnostic_line` | `crate::log::diagnostic_line` |
| `.cartridge/tests/unit/src/trace/tests.rs` | the sink's six tests (there is no `src/trace/tests`) | moves to `.cartridge/tests/unit/src/log/tests.rs` |
| `docs/architecture.txt:25` | `src/trace/  trace ids and the diagnostics sink` | two lines, one per folder |

`Layer::delivering` has no caller and moves unchanged. `diagnostics_enabled` is `pub(crate)` and only the sink uses it.

## Steps

1. `src/trace/mod.rs` keeps lines 1-54 of the base file: `TURN`, `current`, `mint`, `of`, `stamp`, `scope` and `carry`.
   - Its imports shrink to `Json`, `Future`, `AtomicU64`, `Ordering` and `Arc`.
   - The `#[cfg(test)] mod tests` item is deleted.
2. Create `src/log/` with one file per responsibility. Code moves verbatim; only visibility changes.
   - `redact.rs`: `OMIT`, `sensitive`, and `redact` as `pub(super)`.
   - `sink.rs`: `Sink`, `Out` and `impl Sink`. These become `pub(super)`: both types, the fields `out`, `cap` and `written`, and the methods `file`, `from_env` and `write`.
   - `layer.rs`: `Deliver`, `Layer`, `Fields`, both trait impls and `subscribe`. It adds `use super::diagnostic;`.
   - `mod.rs`:
     - It declares `mod layer; mod redact; mod sink;`, re-exports `pub use layer::{subscribe, Layer};` and imports `use crate::trace::current;`.
     - It holds `diagnostics_enabled`, `Note`, `DROPPED`, `OUT`, `drain`, `out`, `now_ms`, `flush`, `diagnostic` and `diagnostic_line`.
     - For the tests it adds `#[cfg(test)] use sink::Out;` and `#[cfg(test)] #[path = "../../.cartridge/tests/unit/src/log/tests.rs"] mod tests;`.
3. Run `git mv .cartridge/tests/unit/src/trace/tests.rs .cartridge/tests/unit/src/log/tests.rs`. The only edit in that file: `mint()` becomes `crate::trace::mint()`.
4. `src/lib.rs`: add `pub mod log;` after `pub mod loader;`. Nothing re-exports a sink name from `trace`.
5. Rewrite the three code callers in the table above. In `docs/architecture.txt`, replace line 25 with:
   ```
     src/trace/      the correlation id one unit of work carries
     src/log/        the diagnostics sink: redaction, bounded queue, capped file
   ```
6. Replace `src/trace/README.md` and add `src/log/README.md` in the parent's README shape: the five headings, in order, 25 lines or fewer. These are the texts the probe used; `Talks to` matches the real `use` edges:
   ```
   # trace
   Does:      Gives one unit of work an id and carries it across tasks, messages and processes.
   Why:       Without it the lines one request leaves in the host, a node and a provider cannot be joined.
   Owns:      the task-local id, `mint`, `current`, `of`, `stamp`, `scope`, `carry`
   Talks to:  calls nothing in the crate; `log` calls it
   Start at:  `carry`
   ```
   ```
   # log
   Does:      Writes diagnostics as redacted JSON lines to stderr or a capped file, from a thread of its own.
   Why:       Without it a secret reaches the log, a slow disk stalls the runtime, or the file grows without bound.
   Owns:      `Sink`, `Out`, `Layer`, `diagnostic`, `flush`, `subscribe`
   Talks to:  calls `trace` and `settings`; `cli` and `host` call it
   Start at:  `diagnostic`
   ```
7. Format only the touched Rust files with `rustfmt --edition 2021`. Never run bare `cargo fmt`.

## Landing (collect precondition, not a Verify block)

The live `src/cli/mod.rs` has another session's uncommitted `Command::Launch { passthrough }` hunk (around line 101).
- That hunk needs that session's uncommitted `src/cli/args.rs` and `src/cli/host.rs` edits, which are outside this footprint.
- Collect commits every dirty path inside the footprint. A collect now would therefore commit the hunk without the edits it needs, and the collected sha would not build (review round 1: E0026 and E0061 in `src/cli/mod.rs`).

**Precondition.** Collect only when this exits 0:
- from the superproject: `git -C cartridge.ctg diff --quiet -- src/cli/mod.rs`
- inside cartridge.ctg: `git diff --quiet -- src/cli/mod.rs`

A zero exit means that session's edit has landed or been withdrawn. Until then the coordinator waits. If HEAD has moved, it rebases the lane first.

**Why not a Verify block.** Blocks also run in the lane, where this change edits `src/cli/mod.rs` itself, so a `diff --quiet` block would fail on this PRD's own edit. The pass-2 blocks also cannot see the bad receipt: the live tree still holds `args.rs` and `host.rs` and builds.

**Recovery.** If a receipt swept a foreign hunk anyway, check the collected sha before anything else lands:
1. Make a throwaway worktree: `git -C cartridge.ctg worktree add --detach "$(mktemp -d)/wt" <sha>`.
2. Run `cargo check --lib --bins` there with an isolated `CARGO_TARGET_DIR`.
3. If it fails, either revert the foreign hunk from `src/cli/mod.rs` in a follow-up commit, or land the owner's `args.rs` and `host.rs` with the owning session's agreement. Then re-check.

## Acceptance

- [ ] `src/trace` holds only `mod.rs` and `README.md`, and `mod.rs` holds only the correlation id. `src/log` holds the sink, the layer and `subscribe`. (census and probe blocks)
- [ ] A probe crate proves the old paths are gone and the new ones work. (probe block)
  - Importing any of the 19 sink names from `cartridge::trace`, public or private, fails as unresolved (E0432), not as private.
  - The `cartridge::log::` paths and `cartridge::trace::{mint, current}` compile.
- [ ] `src/trace/mod.rs` compiles, with warnings denied, as the whole of a crate that has only `serde_json` and `tokio`. This proves it holds only the correlation id and calls nothing in the crate. (probe block)
- [ ] The six sink tests keep their leaf names and now run under `log::tests::`. No test runs under `trace::`. `.cartridge/tests/unit/src/trace` holds no file. A build failure prints cargo's error. (census block)
- [ ] `src/trace/README.md` and `src/log/README.md` have the five headings, in order, in 25 lines or fewer. (census block) The trace README's `Talks to` line reads "calls nothing in the crate; `log` calls it". The probe block's stand-alone crate proves the "calls nothing" half; the diff reviewer checks the text.
- [ ] `docs/architecture.txt` lists `src/log/` and no longer puts the sink in `src/trace/`. (census block)
- [ ] The Landing precondition held when collect ran.
- [ ] The six sink tests pass, the touched files are rustfmt-clean, and clippy with `-D warnings` is clean. (test and lint blocks)
- [ ] After collect, the coordinator runs `just test runtime` and `just check runtime` from `/Users/feb/dev/cartridge`.

## Verify and Proof

Measured in revision 1 on the patched tree, run as `env -u CARTRIDGE_YOLO` with the kache wrapper on:

| Block | Time |
|---|---|
| census | 7 s warm, 19 s cold |
| probe | 13 s |
| lint | 9 s |
| test | 6 passed, 168 filtered out |

Every block is well under 120 s. Each gate was run against these mutants, all in copies of the patched tree:

| Mutant | Block | Result |
|---|---|---|
| unpatched base | census | exit 1, "log::tests::a_credential_or_a_prompt_body_is_omitted_and_named is not in the census" |
| unpatched base | probe | exit 101, E0433 in the positive control |
| `pub use crate::log::{…}` added to trace | probe | exit 1, "cartridge::trace::subscribe still resolves" |
| the whole old sink left in `trace/mod.rs` | probe | exit 1, "cartridge::trace::subscribe still resolves" |
| review's private `struct Sink; fn redact() {}` in trace | probe | exit 101, the crate's own dead-code lint |
| the same items marked `#[allow(dead_code)]` | probe | exit 1, "cartridge::trace::Sink still exists" (E0603, not E0432) |
| renamed sink code in trace (`pub fn cap()` reading `crate::settings`) | probe | exit 1, "src/trace/mod.rs does not stand alone as the correlation id" |
| syntax error in `log/mod.rs` | census | exit 1, cargo's "unclosed delimiter" error printed |
| `docs/architecture.txt` left unchanged | census | exit 1, "docs/architecture.txt still puts the sink in src/trace" |

The unmutated copy passed both blocks (exit 0).

Census and structure:

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/prd-trace-log-split-verify}"
list="$(mktemp)"
err="$(mktemp)"
if ! cargo test --lib -- --list > "$list.all" 2> "$err"; then
	cat "$err" >&2
	exit 1
fi
grep ': test$' "$list.all" > "$list"
for t in a_credential_or_a_prompt_body_is_omitted_and_named the_sink_stays_bounded_by_rotating_one_generation redaction_reaches_objects_inside_nested_arrays oversized_records_are_valid_json_and_bounded_before_and_after_rotation a_sink_that_cannot_repair_a_failed_write_stops_accepting_records a_full_diagnostics_queue_drops_records_and_says_how_many; do
	if ! grep -qx "log::tests::$t: test" "$list"; then
		echo "log::tests::$t is not in the census" >&2
		exit 1
	fi
done
n=$(grep -c '^log::tests::' "$list")
test "$n" -eq 6
if grep -q '^trace::' "$list"; then
	grep '^trace::' "$list" >&2
	exit 1
fi
rm -f "$list" "$list.all" "$err"
if [ -n "$(find .cartridge/tests/unit/src/trace -type f 2>/dev/null)" ]; then
	echo ".cartridge/tests/unit/src/trace still exists" >&2
	exit 1
fi
if ls src/trace | grep -vqxE 'mod\.rs|README\.md'; then
	ls src/trace >&2
	exit 1
fi
for d in src/trace src/log; do
	r="$d/README.md"
	lines=$(wc -l < "$r")
	test "$lines" -le 25
	got=$(grep -oE '^(Does|Why|Owns|Talks to|Start at):' "$r" | tr '\n' ' ')
	if [ "$got" != "Does: Why: Owns: Talks to: Start at: " ]; then
		echo "$r: headings are '$got'" >&2
		exit 1
	fi
done
if grep -rnE '(crate|cartridge)::trace::(subscribe|flush|diagnostic|Layer)' src; then
	exit 1
fi
if grep -q 'trace ids and the diagnostics sink' docs/architecture.txt; then
	echo "docs/architecture.txt still puts the sink in src/trace" >&2
	exit 1
fi
if ! grep -qE '^ +src/log/ ' docs/architecture.txt; then
	echo "docs/architecture.txt does not list src/log" >&2
	exit 1
fi
echo census ok
```

Old paths are gone, new paths compile, and trace stands alone:

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/prd-trace-log-split-verify}"
repo="$PWD"
probe="$(mktemp -d)"
mkdir -p "$probe/src"
cat > "$probe/Cargo.toml" <<TOML
[package]
name = "trace-log-probe"
version = "0.0.0"
edition = "2021"
publish = false
[workspace]
[dependencies]
cartridge = { path = "$repo" }
serde_json = "1"
TOML
# Positive control: the new paths and the kept correlation id resolve.
cat > "$probe/src/main.rs" <<'RS'
fn main() {
	cartridge::log::subscribe();
	cartridge::log::flush();
	cartridge::log::diagnostic_line("probe", "{}");
	cartridge::log::diagnostic("probe", "m", serde_json::Value::Null);
	let _ = cartridge::log::Layer::default();
	let _ = cartridge::trace::mint();
	let _ = cartridge::trace::current();
}
RS
cargo check --quiet --offline --manifest-path "$probe/Cargo.toml"
# No sink name exists under the old path, public or private: each import must
# fail as unresolved (E0432), not as private (E0603).
for name in subscribe flush diagnostic diagnostic_line diagnostics_enabled Layer Fields Deliver Sink Out Note drain out now_ms redact sensitive OMIT DROPPED OUT; do
	printf 'use cartridge::trace::%s as _;\nfn main() {}\n' "$name" > "$probe/src/main.rs"
	if cargo check --quiet --offline --manifest-path "$probe/Cargo.toml" >"$probe/out" 2>&1; then
		echo "cartridge::trace::$name still resolves" >&2
		exit 1
	fi
	if ! grep -q 'error\[E0432\]' "$probe/out"; then
		cat "$probe/out" >&2
		echo "cartridge::trace::$name still exists" >&2
		exit 1
	fi
done
# trace/mod.rs alone, as the whole of a crate that has only serde_json and
# tokio, with warnings denied: any sink code left in it either names a crate
# module or dependency it cannot reach, or is a private item nothing uses.
mkdir -p "$probe/alone/src"
cat > "$probe/alone/Cargo.toml" <<TOML
[package]
name = "trace-alone-probe"
version = "0.0.0"
edition = "2021"
publish = false
[workspace]
[dependencies]
serde_json = "1"
tokio = { version = "1", features = ["full"] }
TOML
printf '#![deny(warnings)]\n#[path = "%s/src/trace/mod.rs"]\npub mod trace;\n' "$repo" > "$probe/alone/src/lib.rs"
if ! cargo check --quiet --offline --manifest-path "$probe/alone/Cargo.toml" >"$probe/out" 2>&1; then
	cat "$probe/out" >&2
	echo "src/trace/mod.rs does not stand alone as the correlation id" >&2
	exit 1
fi
rm -r "$probe"
echo "trace is only the correlation id; log exports every sink name"
```

Format and lint:

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/prd-trace-log-split-verify}"
rustfmt --check --edition 2021 src/trace/mod.rs src/log/mod.rs src/log/redact.rs src/log/sink.rs src/log/layer.rs src/cli/mod.rs src/host/process.rs .cartridge/tests/unit/src/log/tests.rs
cargo clippy --workspace --all-targets --quiet -- -D warnings
```

```test
run: sh -c 'CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/prd-trace-log-split-verify}" cargo test --lib log::tests::'
pass: log::tests::a_credential_or_a_prompt_body_is_omitted_and_named
pass: log::tests::the_sink_stays_bounded_by_rotating_one_generation
pass: log::tests::redaction_reaches_objects_inside_nested_arrays
pass: log::tests::oversized_records_are_valid_json_and_bounded_before_and_after_rotation
pass: log::tests::a_sink_that_cannot_repair_a_failed_write_stops_accepting_records
pass: log::tests::a_full_diagnostics_queue_drops_records_and_says_how_many
```
