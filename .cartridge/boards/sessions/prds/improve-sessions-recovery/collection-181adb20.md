---
commit: 181adb20248c6fdb718823919438939de55bdefc
spec-digests: {"spec01.md":"c97be5210ffc7d55180dca02e74d6cc021d9df4892d07ab84fb8e3c6e180ea9b"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/sessions/prds/improve-sessions-recovery/specs/spec01.md: exit 0

Command SHA-256: c46f15d9000f32ebae07cb376823a92f04e72bfb25972c59218bd4673b029be4

```text
   Compiling sessions v0.1.0 (/Users/feb/dev/cartridge/sessions.ctg)
    Finished `test` profile [unoptimized] target(s) in 0.78s
     Running unittests src/main.rs (/Users/feb/dev/cartridge/cartridge.ctg/.cartridge/workspace/target/debug/deps/sessions-8ab7b4cedbc26499)

running 32 tests
test mapping_tests::scope_input_bounds_and_explicit_conversation_types_are_checked ... ok
test recovery::tests::stale_repair_requests_and_existing_backups_preserve_all_bytes ... ok
test recovery::tests::recovery_reports_are_distinct_fresh_and_read_only ... ok
test recovery::tests::changed_source_at_commit_keeps_newer_snapshot_and_original_backup ... ok
test mapping_tests::stale_revision_and_held_os_lock_never_create_sessions ... ok
test tests::checkpoint_failure_before_rename_changes_nothing ... ok
test mapping_tests::symlink_target_and_index_are_refused_without_touching_destination ... ok
test repair_tests::explicit_empty_legacy_repair_preserves_backup_and_refuses_conversation_data ... ok
test mapping_tests::durable_reconnect_keeps_transcript_bytes_and_rejects_metadata_authority ... ok
test mapping_tests::every_missing_scope_component_is_connection_local ... ok
test tests::concurrent_expected_revision_writes_have_one_winner ... ok
test tests::corrupt_snapshot_is_preserved_and_diagnosed_without_overwrite ... ok
test tests::deletion_failure_preserves_state_and_uncertain_deletion_matches_disk ... ok
test tests::incomplete_session_files_are_reported_without_defaults_or_rewriting ... ok
test tests::generic_mutation_of_the_canonical_transcript_is_rejected ... ok
test tests::a_session_round_trips_through_its_file ... ok
test tests::first_checkpoint_creates_one_transcript_reused_across_restart ... ok
test tests::cwd_changes_are_rejected_during_active_runs_and_advance_revision_otherwise ... ok
test mapping_tests::damaged_indices_and_targets_are_preserved_without_adoption ... ok
test tests::interrupted_run_state_is_exposed_without_executing_anything ... ok
test tests::store_location_is_required_and_invalid_config_is_rejected ... ok
test tests::malformed_and_oversized_records_fail_without_changing_data ... ok
test tests::malformed_buffer_ownership_is_not_loaded_or_rewritten ... ok
test tests::independent_sessions_do_not_wait_for_another_sessions_gate ... ok
test tests::post_rename_failure_reports_uncertainty_and_reloads_visible_state ... ok
test tests::sessions_and_ordinary_buffers_round_trip ... ok
test tests::unattached_buffers_remain_memory_only_and_survive_other_session_commits ... ok
test tests::new_nested_store_is_created_and_unicode_changes_survive_restart ... ok
test tests::sub_agent_session_records_parent_and_mailbox_round_trips_restart ... ok
test tests::concurrent_session_checkpoints_keep_one_revision_winner_and_unique_buffer_ids ... ok
test mapping_tests::mapping_publication_failures_preserve_index_and_report_orphan ... ok
test tests::every_pre_rename_failure_preserves_all_mutations_and_notifications ... ok

test result: ok. 32 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.70s


```
