---
state: "analyzing"
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge"
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
wave: 2
date: "2026-09-15"
footprint:
- "cartridge.ctg"
needs:
- the-profile-is-the-orchestration-service
- the-gates-run-from-the-root-justfile
claim: "cartridge-ctg-22 2026-09-15T09:00:19.848Z"
---

# Host tests hold under suite contention

## Outcome

The host's own check and test gates are green when the whole suite runs at once.

## Acceptance

- [ ] `just check cartridge` exits 0 (2026-09-15: rustfmt diff in `.cartridge/tests/unit/src/host/socket.rs`).
- [ ] `just test cartridge` exits 0 on three consecutive runs with the suite in parallel; `$CARTRIDGE_HOME` is set per test, never process-global; the `cli::setup` and `cli::trust` tests pass on macOS CI.

## Folds

Deferred with `superseded-by` pointing here:

- @root/unit-process-tests-time-out-and-redden-under-suite-contention-after-the-settings-refactor-raised-startup-timeout-to-60s
- root memo `prd/the-binary-target-passes-on-a-runner`

## Result

2026-09-15 11:35, pass 3 (cartridge-ctg-22). Claimed, analysed, held.

The analyst probed at cartridge.ctg `f8a2c00`, cwd `/Users/feb/dev/cartridge`:

```
just check cartridge  exit 1  cargo fmt --all --check: unformatted debug block in src/host/socket.rs (uncommitted, another session's)
just test cartridge   exit 1  lib 152/152 ok; main 11/14:
  cli::setup::tests::setup_links_the_chosen_writes_a_descriptor_the_host_reads_and_lets_a_cartridge_ask
    panicked at .cartridge/tests/unit/src/cli/setup.rs:180:46: Err(Remote(".../host.sock is already served"))
  cli::setup::tests::setup_trusts_what_it_chose_not_what_the_tree_holds   PoisonError at setup.rs:7:18
  cli::trust::tests::an_explicit_path_trusts_a_folder_that_is_neither     PoisonError at setup.rs:7:18
```

One real failure: the second `listen()` for the same descriptor in the setup
test finds the first host's socket still served. The two PoisonErrors follow
from it: that test panics holding `trust_home()`'s process-wide mutex.
`CARTRIDGE_HOME` is still process-global in the unit tests
(`std::env::set_var` at `cli/setup.rs:99,213,243`, `cli/trust.rs:10`,
`tests/mod.rs:22`), serialised only by that mutex, which is what this item's
second box forbids. `src/trust/mod.rs:35` reads it from the environment.

Held: from 11:01 another session has been changing the host on exactly this
failure (`src/host/mod.rs` `unpublish` removes the socket synchronously,
`rewire` bounded, socket and transport changes), 51 files uncommitted at 11:35.
It has not answered on the cross-session channel. Building on that tree or
beside it would overwrite moving work. The spec01 draft (keep `set_var`, make
the mutex poison-tolerant) does not meet "never process-global" and is not
published; it is revised against whatever that session commits.
