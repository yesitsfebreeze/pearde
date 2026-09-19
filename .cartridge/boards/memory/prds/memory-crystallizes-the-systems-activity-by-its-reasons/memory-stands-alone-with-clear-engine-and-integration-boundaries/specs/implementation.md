---
footprint:
  - src/graph/src/experience
  - src/config
  - README.md
  - .cartridge/docs/architecture.md
  - .cartridge/docs/experience.md
  - .cartridge/help.md
---

# Standalone structural verification contract

This revision replaces the underspecified verification commands while preserving the reviewed outcome and round history. The existing implementation is the baseline, not a new competing engine. The authorized baseline commit includes the existing feature wiring across original feature leaves; this leaf verifies only the declared structural outcome. It does not collect their behavior or the reliability follow-ups.

## Migration and recovery

No new schema, migration, ranking rule or public API is introduced here. Appended enum discriminants and occurrence fields retain their existing layout. Existing intake/receipt migration and stale-snapshot refusal remain in place. A failed verification leaves source and intake unchanged; no loaded cartridge is rebuilt or activated. The tested baseline excludes unrelated task migration, Scope detail, and full-body readback work, which remain preserved in the integration working tree.

## Acceptance

- [x] Experience modules separate metadata, matching, mutation and undo and follow rustfmt.
- [x] The baseline builds from a standalone source snapshot with no sibling crates.
- [x] Cargo dependency metadata confirms graph has no external host source dependency.
- [x] Retired calendar/ledger source and configuration are absent.
- [x] README, help and architecture describe existing boundaries, recovery and representative fidelity.
- [x] Named domain, durable receipt, rollback, restart, observational search and reason partition tests pass.

## Verify

```test
run: export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-/tmp/cartridge-memory-stack-baseline-target}"; cargo test --locked -p graph -p rpc -p store_core -p tick_loop experience --lib
pass: experience_recurrence_and_reason_boundaries
pass: experience_survives_reload_and_undo_restores_indexes
pass: experience_intake_retry_recurrence_restart_and_opposite_outcome
pass: experience_failed_commit_restores_graph_and_retains_input
pass: experience_commit_refuses_older_full_flush_and_migrates_history
pass: experience_receipts_survive_commit_and_expire_without_accepting_old_delivery
pass: experience_read_only_search_never_enqueues_usage_on_fresh_or_cached_queries
pass: experience_reason_space_separates_outcomes_without_rewriting_content
```

```test
run: export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-/tmp/cartridge-memory-stack-baseline-target}"; cargo test --locked -p memory_cartridge asp
pass: a_memory_entity_expands_to_its_node_with_the_observed_projection_revision
pass: search_and_expand_agree_with_context_memory_on_a_real_bank
pass: the_shipped_declaration_is_one_the_host_accepts
```

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-/tmp/cartridge-memory-stack-baseline-target}"
cargo check --workspace --locked
cargo fmt --all -- --check
test ! -e src/rpc/src/ledger.rs
test ! -e src/store/core/src/ledger.rs
python3 - <<'CHECK'
import json, pathlib, subprocess
root=pathlib.Path.cwd().resolve()
metadata=json.loads(subprocess.check_output(['cargo','metadata','--locked','--no-deps','--format-version','1']))
for package in metadata['packages']:
    for dependency in package['dependencies']:
        if dependency.get('path'):
            target=pathlib.Path(dependency['path']).resolve()
            assert root == target or root in target.parents, str(target)
assert 'LedgerConfig' not in pathlib.Path('src/config/src/config.rs').read_text()
CHECK
```
