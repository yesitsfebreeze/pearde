---
complexity: low
footprint:
  - .cartridge/tests/integration/cartridge.rs
---

# spec01 — no base command the fixture spawns inherits CARTRIDGE_YOLO

Base: memory.ctg 3432b13; base binary `../cartridge.ctg/target/release/cartridge`
(cartridge.ctg 7af748a, release build 2026-09-19 13:12).
Reusable attempt: `.state/loop/integration-trust/attempt-2.patch` (applies to 3432b13
with `git apply`). `attempt-1.patch` is obsolete: it no longer applies.

## State at 3432b13 (re-probed 2026-09-19)

Most of the original outcome has already landed. memory.ctg `f2319c5` gave
`Base::boot` its own `CARTRIDGE_HOME` (`<tempdir>/cartridge-home`), runs
`cartridge trust <dir>` before `daemon`, passes the same home to `cli`, and asserts
`` `memory` is not provided `` (cartridge.ctg `src/error/mod.rs:31`, raised at
`src/host/mod.rs:806`). With `CARTRIDGE_YOLO` unset, `cargo nextest run -p memory
--test cartridge` passes 3 of 3 against the release base, and nothing under
`~/.cartridge` changes.

What is still missing: every run in these sessions exports `CARTRIDGE_YOLO=1`, and
the base then trusts every file (`trust::verify`, cartridge.ctg `src/trust/mod.rs:94`).
Under that variable the trust step could be dropped and the tests would still pass.
Probed with the release base on an untrusted temp project with its own
`CARTRIDGE_HOME`: without YOLO, `daemon` exits with `is in no trusted project`.
With `CARTRIDGE_YOLO=1`, it serves the entry.

## Steps

All steps are in `.cartridge/tests/integration/cartridge.rs`.

1. Add `fn base_command(home: &Path) -> Command`:
   `Command::new(base())` with `.env("CARTRIDGE_HOME", home)` and
   `.env_remove("CARTRIDGE_YOLO")`. The precedent is `src/hub/src/lib.rs:121`
   (`env_remove(identity::TAKEOVER_ENV)`).
2. Have the `trust` and `daemon` spawns in `Base::boot` and the spawn in `Base::cli`
   use `base_command(&home)` / `base_command(&self.home)`, dropping their own
   `.env("CARTRIDGE_HOME", …)`. `Command::new(base())` is then left only in
   `base_command`.
3. Add `#[test] fn an_inherited_yolo_does_not_trust_a_project_the_fixture_never_trusted`:
   - `std::env::set_var("CARTRIDGE_YOLO", "1")`. This is safe on edition 2021, and
     nextest runs each test in its own process.
   - Write a temp project with an empty `.cartridge/init.lua`, never trusted, and a
     `cartridge-home` of its own.
   - Spawn `base_command(&home) … daemon` with stderr going to `daemon.log`, and poll
     `try_wait` for up to 10 s, killing the daemon on timeout.
   - Assert that it exited non-zero and that the log contains `is in no trusted project`.

## Acceptance

- [ ] `an_inherited_yolo_does_not_trust_a_project_the_fixture_never_trusted` passes, and so do the 3 existing `memory::cartridge` tests (the `test` block below). At base, the new test does not exist, so its `pass:` line fails.
- [ ] The new test fails when `.env_remove("CARTRIDGE_YOLO")` is removed from `base_command`: the daemon serves the untrusted project and the test times out at 10 s. Probed; see the analyst report.
- [ ] A run leaves `~/.cartridge` untouched: no file under it is newer than a mark taken before the run.

## Verify and Proof

The base binary must exist. `../cartridge.ctg` resolves from the lane through
`.lanes/cartridge.ctg` → the live checkout.

```sh
test -x "${CARTRIDGE_BIN:-../cartridge.ctg/target/release/cartridge}"
```

```test
run: CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/integration-trust-verify}" cargo nextest run -p memory --test cartridge
pass: an_inherited_yolo_does_not_trust_a_project_the_fixture_never_trusted
pass: status_tool_and_context_answer_without_opening_the_store
pass: a_bad_configuration_fails_the_cartridge_before_it_listens
pass: ingest_query_tool_and_context_reach_one_store_through_the_base
```

Timing: 53 s cold in a fresh target dir, and 4 s warm. Each pass fits in 120 s. The
fixture's `module()` builds `memory_cartridge` into the same isolated
`CARGO_TARGET_DIR`, so pass 2 never writes `target/debug` in the live checkout. The
new test sets YOLO itself, so it does not depend on the collector's environment.
Nothing in the Verify block checks `~/.cartridge` (third box). That box is proved by
the fixture's design, a temp `CARTRIDGE_HOME` on every spawn, and by the probe in the
report. The diff reviewer confirms it.

## Review notes carried into implementation (round 1, clarification only)

- Box 3 is checked as: no trust record under `~/.cartridge` names the run's tempdir or `cartridges/memory`.
  Other concurrent tests on this machine write their own trust records, so "no file newer than a mark"
  gives false alarms. The diff reviewer confirms it; the test may assert it too.
- The new test proves that `base_command` strips `CARTRIDGE_YOLO`. That every spawn goes through
  `base_command` (`Command::new(base())` appears only there) is for the diff reviewer.
- Each collect pass builds from a cold `target/integration-trust-verify` (about 50 s against 120 s). If a
  pass times out under machine load, rerun it alone; never loosen the gate.
- Put a comment on the test's `std::env::set_var`: it is only safe on edition 2021, so an edition bump
  must fail loudly rather than the line being dropped.

