---
complexity: small
footprint:
  - src/host/plan.rs
  - .cartridge/tests/unit/src/host/plan.rs
---

# Optional exact needs do not reject an otherwise runnable cartridge

## Implementation and boundary

Use committed host 8da102215640bedf9b11d4f3325abec34bf639a2 in the engine lane.
The current unmatched() checks optional sends as required declarations; an absent
jev? therefore prevents stock Harness fixtures from loading. Keep optional
needs in send permissions, but exclude them from the missing-provider rejection.
Unmatched listeners and hard needs must retain their existing rejection.

The manifest already documents optional needs as exact names, never globs.
Reject an optional wildcard such as tool.*? during planning with a clear message
naming the need, before expansion can discard optionality. This implements the
PRD's permitted refusal alternative. Preserve ordinary hard wildcard behavior,
existing circular optional dependency startup, and exact optional sends when a
provider exists. No manifest, setting, declared need, event or documentation
surface changes; this restores the documented contract in its existing owner.

The implementing worker validated and owns this final specification against the named base.
Add tests in the existing plan test module. Use the crate's existing test helpers
write/home/built and real disposable Host compositions, explicit trust, and the
newly built candidate node binary. Reuse public Host reconcile/status/bail/stop.
Never restart the shared daemon. Ensure cleanup runs before assertions escape.
Pin actual Active state and a successful declared consumer event with an absent
optional provider, while the otherwise identical hard need is Failed with the
existing message. Also pin unknown listener refusal, exact optional permission,
and clear wildcard rejection with and without matching providers. Existing
hard wildcard and circular dependency tests remain compatibility gates.

## Acceptance

- [x] optional_need_without_provider_loads_and_answers observes a real active
      consumer and successful event without an optional provider; hard needs and
      undeclared listeners still fail.
- [x] optional_glob_is_refused_without_losing_optionality proves both empty and
      populated wildcard compositions fail clearly at planning; exact optional
      permission and existing hard wildcard behavior remain intact.
- [x] Both new regressions fail on the unchanged base and pass on the candidate.
      Formatting, strict lint and the complete workspace tests pass.

## Verify and Proof

Run from owner root in both lane and integrated passes. Prebuild the isolated
candidate before collection. Use a fresh short XDG_RUNTIME_DIR supplied by the
coordinator to avoid old fixture global-environment path accumulation. Unset
CARTRIDGE_YOLO. Do not edit any other path or reuse a stale installed node binary.

```test
run: env -u CARTRIDGE_YOLO RUST_TEST_THREADS=1 CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/optional-needs-verify}" cargo test --locked --lib host::plan::tests
pass: optional_need_without_provider_loads_and_answers
pass: optional_glob_is_refused_without_losing_optionality
```

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/optional-needs-verify}"
cargo fmt --all -- --check
cargo clippy --locked --workspace --all-targets -- -D warnings
```

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/optional-needs-verify}"
env -u CARTRIDGE_YOLO RUST_TEST_THREADS=1 cargo test --locked --workspace --all-targets
```

An independent verifier reads the complete diff and reruns proof before any
acceptance ticks. Coordinator runs composition audit/isolation after integration
and then retries the blocked Harness gates using the verified candidate host.
