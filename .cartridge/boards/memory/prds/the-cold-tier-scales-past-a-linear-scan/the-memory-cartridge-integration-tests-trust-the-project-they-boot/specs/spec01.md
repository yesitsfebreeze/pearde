---
complexity: low
footprint:
  - .cartridge/tests/integration/cartridge.rs
---

# spec01 — the cartridge fixture trusts its temp project in a temp CARTRIDGE_HOME

Base: memory.ctg 5097a83; base cartridge.ctg a965d6e (release build of 2026-09-15 or the
current debug build; both probed green). Reusable attempt:
`.state/loop/the-memory-cartridge-integration-tests-trust-the-project-they-boot/attempt-1.patch`
(applies to 5097a83 with `git apply`).

Steps, all in `.cartridge/tests/integration/cartridge.rs`:

1. Add `fn base_command(dir: &Path) -> Command`: `Command::new(base())` with
   `.env("CARTRIDGE_HOME", dir.join(".home"))` and `.current_dir(dir)`. `.home` is inside
   the tempdir (removed with it) and dot-prefixed, so `trust::collect` never hashes it.
2. In `Base::boot`, before spawning `daemon`, run `base_command(&dir).arg("trust").arg(&dir)`
   and assert it succeeded (stderr in the message). Spawn `daemon` via `base_command`.
3. `Base::cli` uses `base_command(&self.dir)`. `Command::new(base())` then appears only in
   `base_command`.
4. `a_bad_configuration_fails_the_cartridge_before_it_listens`: once trust passes, the base
   answers a call to a failed cartridge with `` `memory` is not provided `` (`host/mod.rs:769`:
   failed slots leave the catalogue), not `no active listener`. Assert
   ``error.contains("`memory` is not provided")``.

Not included: `cargo nextest run --workspace` still has one failure outside this
footprint, `memory::spill_transparency a_spilled_graph_answers_the_same_queries_as_one_that_never_spilled`
(recall@10 0.8370 < 0.84, `spill_transparency.rs:146`; the same result on two runs).
The PRD's third box needs its own PRD or has to be dropped.

## Acceptance

- [ ] `cargo nextest run -p memory --test cartridge` exits 0 (3 passed) against `../cartridge.ctg/target/release/cartridge`, or against the debug build when no release build exists.
- [ ] `Command::new(base())` appears exactly once in the fixture, and that spawn sets `CARTRIDGE_HOME`, so trust, daemon and cli all share the temp home.
- [ ] After the run, no record in `$HOME/.cartridge/trust` modified during the run names a project under the resolved `$TMPDIR/.tmp*`.

## Verify

```sh
export CARGO_TARGET_DIR="$PWD/target/trust-verify"
f=.cartridge/tests/integration/cartridge.rs
test "$(grep -c 'Command::new(base())' "$f")" = 1
grep -q 'env("CARTRIDGE_HOME"' "$f"
if [ ! -x ../cartridge.ctg/target/release/cartridge ]; then
  test -x ../cartridge.ctg/target/debug/cartridge
  export CARTRIDGE_BIN="$(cd ../cartridge.ctg/target/debug && pwd -P)/cartridge"
fi
mark="$(mktemp)"
cargo nextest run -p memory --test cartridge
trust="$HOME/.cartridge/trust"
tmp="$(cd "${TMPDIR:-/tmp}" && pwd -P)"
leaked="$( [ -d "$trust" ] && find "$trust" -type f -newer "$mark" -exec grep -l "\"project\": \"$tmp/.tmp" {} + 2>/dev/null || true)"
rm -f "$mark"
test -z "$leaked"
```
