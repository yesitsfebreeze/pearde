---
complexity: small
footprint:
  - .cartridge/tests/integration/working.rs
---

# Working-memory inspection and assessment remain separately observable

## Implementation and boundary

The implementing worker owns this specification and its subsequent one-file
implementation in the engine lane. Use committed Harness
c8305341bb30b058c481bf023ebf977304248dab, or a newer committed base only after
rechecking this contract and overlap. Change only the named integration test;
product code, fixtures, support.rs, manifest, settings, needs and events stay
outside this receipt. No product behavior or documentation surface changes.

In rolling_memory_refreshes_below_budget_and_survives_reload_and_failure,
replace equality between the inspection projection and the whole model system
context with explicit assertions that the nonempty complete projected string
is the exact system prefix and the remaining suffix contains the advisory JEV
instruction followed by a complete terminal <jev-assessment> block. Parse that
block as JSON and compare it exactly with the response's assessment value;
assert fallback action for this composition without JEV. Preserve the stored
summary assertions and every existing reload, corrected-constraint, compaction
comparison, privacy, failure-mode, appended-tail, hard-budget and recovery check.
Do not substitute a loose substring check for projection preservation.

The committed context handler tries the assessment-reserved budget first and
then the full budget after failure. Correct the later hard-budget failed-refresh
router count to exactly before + 2 and explain those two attempts. Keep exact
saved-summary and original-transcript equality, the explicit provider error,
and successful subsequent recovery. No tolerance range or removed assertion.

## Evidence and overlap

An untouched committed archive fails at the original projection equality.
Correcting only that assertion reaches the later router-count mismatch (16
observed versus 15 expected). Both reproduce against the pinned host below.
Preserve these separate red observations, then run the entire corrected test.
The live working.rs already has foreign prefix/suffix and +2 changes. Do not copy
or commit that dirty file wholesale. Implement independently in the clean engine
lane. Before integration, compare the current live diff and coordinate with its
owner: identical hunks may be recognized as delivered only after explicit
reconciliation; preserve stronger assertions and all unrelated foreign edits.
If ownership remains unresolved, retain the verified lane and report collection
blocked. Do not force checkout, stash, discard or reset foreign work. Recheck
HEAD, file hashes and worktree status before any collection.

## Acceptance

- [x] The named test is red on the unchanged baseline for the recorded equality,
      and green with the bounded correction; the prefix-only intermediate probe
      also records the later count mismatch.
- [x] Exact projection, explicit assessment payload, reload and every original
      failure/data-preservation assertion remain enforced by the complete test.
- [x] Exact two-attempt maintenance accounting, formatting, strict lint and all
      owner Rust tests pass against the identified compatible committed host.

## Verify and Proof

Run each block from the engine lane and subsequently the reconciled integration
checkout with a 120-second outer watchdog per block. Prebuild separately if a
cold compilation approaches that bound; never treat a timeout as success.
Each block supplies an isolated target default; the coordinator may override
CARGO_TARGET_DIR with another private target. Supply a fresh short XDG_RUNTIME_DIR
(such as a mktemp directory beneath /tmp) to all blocks. The test support builds
this lane's actual module and kills/waits its disposable daemon on failure.
Unset CARTRIDGE_YOLO. The host is a build of committed
b4345b6dc5d03d33900ff7fb793f7dd752f5757d, not the dirty live host source or stale
release binary. Its provenance is in roster implementer-codex-3.md. A replacement
host requires explicit committed-source provenance, hash and compatibility proof.

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/working-proof-verify}"
export CARTRIDGE_BIN="${CARTRIDGE_BIN:-/tmp/roster-current-host-target/debug/cartridge}"
printf '%s  %s\n' b081f7d1b9aab6c1130bb61ee4ec356931b65483dcac7e88c998ca283ff6dc75 "$CARTRIDGE_BIN" | shasum -a 256 -c -
env -u CARTRIDGE_YOLO cargo build --locked --workspace
```

```test
run: env -u CARTRIDGE_YOLO CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/working-proof-verify}" CARTRIDGE_BIN="${CARTRIDGE_BIN:-/tmp/roster-current-host-target/debug/cartridge}" RUST_TEST_THREADS=1 cargo test --locked --test working rolling_memory_refreshes_below_budget_and_survives_reload_and_failure -- --exact
pass: rolling_memory_refreshes_below_budget_and_survives_reload_and_failure
```

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/working-proof-verify}"
cargo fmt --all -- --check
env -u CARTRIDGE_YOLO cargo clippy --locked --workspace --all-targets -- -D warnings
```

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/working-proof-verify}"
env -u CARTRIDGE_YOLO CARTRIDGE_BIN="${CARTRIDGE_BIN:-/tmp/roster-current-host-target/debug/cartridge}" RUST_TEST_THREADS=1 cargo test --locked --workspace --all-targets
```

One spec and one test file qualify for the explicit 2026-09-19 fast path in
review-plan.md. The same worker authors this spec and code. No numeric review
score is claimed. An independent verifier reads the full diff, confirms the
baseline reasons and reruns all blocks before acceptance or collection. A
behavioral gap or any failed eligibility condition enters normal review at
round 1. The coordinator owns final audit/isolation and retrying the blocked
roster gates; this test correction does not certify the separate roster change.
