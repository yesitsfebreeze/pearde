---
complexity: small
footprint: ["src/commands/Cargo.toml","src/store/core/src/lock.rs",".cartridge/tests/unit/src/store/core/src/tests/lock_test.rs","src/store/core/Cargo.toml","Cargo.lock"]
---

# spec01 — Restore isolated exit proof and causally exercise handover locking

Register the existing exit_status.rs as its own commands integration target.
Do not move it back into the shared unit binary or reset the failure flag.
Reuse existing try_lock_patiently's bounded retry. Factor its waiting action
so a deterministic test can release a child-held duplicate only after the
first WouldBlock. A direct attempt must fail while the child holds the open
file description; retry succeeds after release; a genuine holder still fails.
No replacement shutdown/latch protocol or flag reset is added.

## Acceptance

- [x] The exit_status integration target is listed and passes alone; disabling FAILED.store makes that unchanged test fail.
- [x] A child-held duplicate deterministically reproduces the parent-release lock window and the existing bounded retry succeeds; disabling retry makes the new test fail.
- [x] Five unchanged isolated runs pass; full memory formatting/clippy, nextest and documentation gates pass or report any distinct prerequisite failure honestly.

## Verify and Proof

```sh
cargo test -p commands --test exit_status
cargo test -p store_core inherited_description_requires_the_bounded_retry
cargo test -p commands --lib a_handover_with_no_listener_frees_the_store_and_returns
```

Run full `just check` and `just test` in the isolated memory worktree. Compiler
wrappers remain disabled and the lane uses its own target. Preserve historical
exit isolation and 100ms lock patience; these are reused, not reinvented.
