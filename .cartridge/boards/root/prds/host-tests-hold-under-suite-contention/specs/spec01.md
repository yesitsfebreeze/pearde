---
complexity: small
footprint:
  - cartridge.ctg/justfile
  - cartridge.ctg/.cartridge/tests/unit/src/tests/settings.rs
  - cartridge.ctg/.cartridge/tests/unit/src/cli/setup.rs
---

# spec01 — One test per process for the runtime gate, and no test reads ambient yolo

Revises the unpublished spec01 drafted against f8a2c00. That draft's subject —
the `host.sock is already served` collision and the two PoisonError cascades —
is fixed at HEAD 655beb6; its remaining live part is folded in here.

## Evidence (2026-09-15, HEAD 655beb6, cwd /Users/feb/dev/cartridge)

- `just check cartridge`: exit 0 (fmt and clippy clean; the rustfmt failure
  named in the PRD landed fixed with f8a2c00/655beb6).
- `just test cartridge`: exit 1, 166 tests, exactly 1 failure:
  `tests::settings::yolo_overrides_the_configured_value_only_where_the_cartridge_declares_it`
  panics at `.cartridge/tests/unit/src/tests/settings.rs:33` — the assertion
  `apply(...)["yolo"] == false` observes `true` because the test process
  inherits the ambient `CARTRIDGE_YOLO=1` that yolo-mode shells on this
  machine export. With the variable unset the full gate is green (verified:
  `env -u CARTRIDGE_YOLO just test cartridge` exits 0).
- The gate runs `cargo test --workspace` (`cartridge.ctg/justfile`): one
  process, parallel threads. The `CARTRIDGE_HOME`-mutating tests
  (`set_var` at `cli/setup.rs:92,197,223`, `cli/trust.rs:7`,
  `tests/mod.rs:20`) are serialized only by the `trust_home()` process-wide
  mutex — process-global mutation, which the PRD's second acceptance box
  forbids, and a panicking test poisons that mutex for the rest of the
  process (the PoisonError cascades of the earlier draft).
- `cargo-nextest` is already a required tool of the composed gates (the
  toolchain line of `.cartridge/justfile`) and runs every test in its own
  process. `cargo nextest run --workspace` at HEAD runs all 166 tests with
  per-test processes: no shared environment, no shared mutex, no poison
  propagation. Cartridge.ctg has no doc tests (`cargo test --workspace --doc`:
  0 run), which nextest would otherwise skip.

## Acceptance

- [x] The runtime gate executes one test per process: `cartridge.ctg/justfile`
      `test` runs `cargo nextest run --workspace`.
- [x] Every `CARTRIDGE_HOME` `set_var` site in the unit tests is thereby per
      test process, never shared across tests.
- [x] The yolo settings test pins the environment it observes: it saves and
      clears `CARTRIDGE_YOLO` before its first assertion and restores the
      saved value after.
- [x] `trust_home()` recovers a poisoned lock instead of propagating
      PoisonError, so one panicking test cannot cascade under a plain
      in-process `cargo test --workspace` run.
- [x] `just check cartridge` exits 0, and `just test cartridge` exits 0 on
      three consecutive runs with the suite in parallel, with and without
      `CARTRIDGE_YOLO=1` in the caller's environment.

## Verify

The PRD's repo is the superproject, so collection runs these blocks with cwd
`/Users/feb/dev/cartridge`. That is a specced leaf collected without a lane.
The engine allows 120 s per block, so each gate run gets its own block.

```sh
test -z "$(git -C cartridge.ctg status --porcelain)"
```

```sh
just check cartridge
```

```sh
CARTRIDGE_YOLO=1 just test cartridge
```

```sh
CARTRIDGE_YOLO=1 just test cartridge
```

```sh
CARTRIDGE_YOLO=1 just test cartridge
```

```sh
env -u CARTRIDGE_YOLO just test cartridge
```

```sh
grep -q 'nextest run --workspace' cartridge.ctg/justfile
```

```sh
cd cartridge.ctg && cargo test --workspace
```

## Proof

Landed as cartridge.ctg `bceb644` ("Isolate host tests: one test per process
and CARTRIDGE_HOME guards"): `justfile`, `.cartridge/tests/unit/src/cli/setup.rs`
and `.cartridge/tests/unit/src/tests/settings.rs`.

Coordinator revision 2026-09-16 (cartridge-c4). The earlier single proof block
chained five suite runs, which is past the 120 s limit for one block, and it did
not fail on a dirty tree. It is split into one block per gate, and the tree must
be clean first. The CARTRIDGE_HOME grep is an inspection step and doesn't need
a block.
