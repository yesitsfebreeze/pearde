---
commit: 2a6a863cf1af0876072f8879050274cfa650a785
spec-digests: {"spec01.md":"a0dc9e10e5d14fc2c7ced467bf27afb334c28c7dfe82bc36999af190fa8f1ff3"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/sessions/prds/improve-sessions-programme/specs/spec01.md: exit 0

Command SHA-256: 8d9f72ccbdc91205f6cac203e6db239be83a8715e1dc3daa2df6bcab4212c1bd

```text
{"ref":"@sessions/improve-sessions-client-mapping","state":"done","revision":"223517b6b0ed7dd2f718f5b2a8fb6d0de2453eb2c5c24116bb588d2a2e7ae935","commit":"2a6a863cf1af0876072f8879050274cfa650a785","verified":true,"integrated":true,"reason":null,"evidence":"/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/sessions/prds/improve-sessions-client-mapping/collection.md"}
{"ref":"@sessions/improve-sessions-retention","state":"done","revision":"8feb4d4d9d5edeadec9ba3908ded8082add84224b85475059c6476e245b949c0","commit":"2a6a863cf1af0876072f8879050274cfa650a785","verified":true,"integrated":true,"reason":null,"evidence":"/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/sessions/prds/improve-sessions-retention/collection.md"}
{"ref":"@sessions/improve-sessions-recovery","state":"done","revision":"47f7ed3e4cf0b7d5bc788d29fd5ce41a83f5d7921421f7bce69bf1f5a3b55749","commit":"2a6a863cf1af0876072f8879050274cfa650a785","verified":true,"integrated":true,"reason":null,"evidence":"/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/sessions/prds/improve-sessions-recovery/collection.md"}

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/sessions/prds/improve-sessions-programme/specs/spec01.md: exit 0

Command SHA-256: c7002f90a7077e71ab285aba37505c32f0d8d0b7efbd34775bf28321fda37a05

```text
    Finished `test` profile [unoptimized] target(s) in 0.09s
     Running unittests src/main.rs (target/sessions-mapping/debug/deps/sessions-d3cf3d74a9406804)

running 60 tests
test mailbox_tests::old_mailbox_lines_gain_stable_read_identity_without_eager_rewrite ... ok
test mailbox_tests::reserved_mailbox_buffer_mutation_and_invalid_posts_preserve_bytes ... ok
test mailbox_tests::legacy_parent_and_generic_fields_cannot_forge_trusted_lineage ... ok
test mailbox_tests::actor_scope_and_private_child_lineage_reject_metadata_forgery ... ok
test mailbox_tests::full_legacy_mailbox_remains_readable_but_rejects_another_append ... ok
test mapping_tests::scope_input_bounds_and_explicit_conversation_types_are_checked ... ok
test mapping_tests::durable_reconnect_keeps_transcript_bytes_and_rejects_metadata_authority ... ok
test mapping_tests::every_missing_scope_component_is_connection_local ... ok
test mapping_tests::damaged_indices_and_targets_are_preserved_without_adoption ... ok
test observations::tests::changing_file_during_read_is_an_unstable_best_effort_snapshot ... ok
test observations::tests::descriptor_and_provider_changes_do_not_share_verdict_freshness ... ok
test observations::tests::inconsistent_completion_or_identity_fields_cannot_create_known_success ... ok
test observations::tests::configured_path_cannot_be_overridden_and_reports_do_not_mutate_sessions ... ok
test mapping_tests::stale_revision_and_held_os_lock_never_create_sessions ... ok
test mailbox_tests::receipt_ack_survives_restart_and_never_skips_later_posts_or_other_actor_cursor ... ok
test observations::tests::malformed_partial_and_rotated_evidence_is_bounded_and_explicit ... ok
test observations::tests::verdicts_compare_only_same_source_and_latest_observed_revisions ... ok
test observations::tests::report_counts_only_observed_completions_and_preserves_legacy_unknowns ... ok
test observations::tests::report_distinguishes_disabled_missing_empty_and_unavailable_sources ... ok
test mapping_tests::symlink_target_and_index_are_refused_without_touching_destination ... ok
test recovery::tests::changed_source_at_commit_keeps_newer_snapshot_and_original_backup ... ok
test recovery::tests::stale_repair_requests_and_existing_backups_preserve_all_bytes ... ok
test recovery::tests::recovery_reports_are_distinct_fresh_and_read_only ... ok
test repair_tests::explicit_empty_legacy_repair_preserves_backup_and_refuses_conversation_data ... ok
test retention_tests::bad_metadata_and_snapshot_bounds_fail_closed ... ok
test retention_tests::busy_journal_lock_and_cutoff_or_batch_errors_have_no_deletion_effect ... ok
test observations::tests::source_and_response_caps_never_truncate_json_or_expose_bodies ... ok
test mailbox_tests::ambiguous_post_failure_is_resolved_by_message_id_without_duplicate_append ... ok
test mailbox_tests::same_message_id_is_idempotent_and_concurrent_posts_have_distinct_positions ... ok
test retention_tests::journal_backup_and_job_symlink_or_traversal_never_touch_outside_evidence ... ok
test retention_tests::partial_backup_or_malformed_journal_blocks_resume_and_preserves_all_evidence ... ok
test mapping_tests::mapping_publication_failures_preserve_index_and_report_orphan ... ok
test tests::checkpoint_failure_before_rename_changes_nothing ... ok
test retention_tests::protection_changes_are_cas_checked_and_leave_transcripts_unchanged ... ok
test tests::concurrent_expected_revision_writes_have_one_winner ... ok
test tests::corrupt_snapshot_is_preserved_and_diagnosed_without_overwrite ... ok
test tests::a_session_round_trips_through_its_file ... ok
test tests::deletion_failure_preserves_state_and_uncertain_deletion_matches_disk ... ok
test tests::cwd_changes_are_rejected_during_active_runs_and_advance_revision_otherwise ... ok
test mailbox_tests::acknowledgement_failure_preserves_unread_or_reports_only_already_delivered_progress ... ok
test tests::generic_mutation_of_the_canonical_transcript_is_rejected ... ok
test tests::first_checkpoint_creates_one_transcript_reused_across_restart ... ok
test tests::incomplete_session_files_are_reported_without_defaults_or_rewriting ... ok
test tests::interrupted_run_state_is_exposed_without_executing_anything ... ok
test tests::independent_sessions_do_not_wait_for_another_sessions_gate ... ok
test tests::malformed_and_oversized_records_fail_without_changing_data ... ok
test tests::malformed_buffer_ownership_is_not_loaded_or_rewritten ... ok
test tests::concurrent_session_checkpoints_keep_one_revision_winner_and_unique_buffer_ids ... ok
test tests::store_location_is_required_and_invalid_config_is_rejected ... ok
test tests::post_rename_failure_reports_uncertainty_and_reloads_visible_state ... ok
test tests::new_nested_store_is_created_and_unicode_changes_survive_restart ... ok
test retention_tests::preview_counts_records_and_bytes_and_retains_every_authoritative_protection ... ok
test tests::sub_agent_session_records_parent_and_mailbox_round_trips_restart ... ok
test tests::sessions_and_ordinary_buffers_round_trip ... ok
test tests::unattached_buffers_remain_memory_only_and_survive_other_session_commits ... ok
test retention_tests::resume_refuses_new_protection_and_same_id_replacement_even_with_identical_bytes ... ok
test tests::every_pre_rename_failure_preserves_all_mutations_and_notifications ... ok
test mailbox_tests::bounded_delivery_and_failed_read_persistence_leave_all_messages_unacknowledged ... ok
test retention_tests::post_preview_activity_pin_reference_and_revision_changes_refuse_without_transcript_mutation ... ok
test retention_tests::every_durable_interruption_resumes_only_recorded_targets_and_preserves_backups ... ok

test result: ok. 60 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 2.13s

    Finished `dev` profile [unoptimized] target(s) in 0.09s
    Finished `dev` profile [unoptimized] target(s) in 0.09s
bun test v1.3.14 (0d9b296a)

../sessions.ctg/.cartridge/tests/integration/mapping.test.ts:
(pass) real host configuration survives reconnect and copied call metadata cannot cross scopes [343.29ms]
(pass) missing identity or conversation has one honest connection scope and no reconnect identity [63.95ms]
(pass) concurrent fresh SDK processes cannot publish two mappings against one revision [29.89ms]

../sessions.ctg/.cartridge/tests/integration/retention.test.ts:
(pass) real SDK previews exact bytes/records and preserves protected sessions across apply/restart/resume [92.91ms]
(pass) native late protection and durable client references cannot be bypassed with copied candidates [80.55ms]
(pass) actual harness ring still deletes an unprotected completed turn [1352.51ms]
(pass) actual harness ring preserves a turn becoming active during ingest [1176.01ms]

 7 pass
 0 fail
 83 expect() calls
Ran 7 tests across 2 files. [3.15s]

```
