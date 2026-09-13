---
commit: 191e2b6cb4291bdcce7a894f98bb2d475361d30f
spec-digests: {"spec01.md":"6ab4480f4eb78676a6f40257f14e5ca9c3a0c54742c977229a46b6ee6cca34fc"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/sessions/prds/improve-sessions-recovery/specs/spec01.md: exit 0

Command SHA-256: c46f15d9000f32ebae07cb376823a92f04e72bfb25972c59218bd4673b029be4

```text
    Finished `test` profile [unoptimized] target(s) in 0.12s
     Running unittests src/lib.rs (/Users/feb/dev/cartridge/cartridge.ctg/target/tool-result-contract/debug/deps/sessions-cb520d7f363a0e47)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests src/main.rs (/Users/feb/dev/cartridge/cartridge.ctg/target/tool-result-contract/debug/deps/sessions-64f3546e64d59d81)

running 89 tests
test change_records_tests::random_publication_ids_are_valid_and_do_not_encode_payload ... ok
test change_records_tests::strict_nested_schema_and_revision_coordinates_reject_before_publication ... ok
test change_records_tests::publication_identity_deduplicates_only_same_publication_and_keeps_legacy_projection ... ok
test change_records_tests::changed_page_revision_and_corrupt_stored_nested_logs_are_diagnosed ... ok
test change_records_tests::publication_faults_keep_old_state_or_expose_uncertainty_without_replay ... ok
test channels::cursor_tests::empty_and_oversized_delivery_do_not_write_or_advance_progress ... ok
test channels::cursor_tests::malformed_duplicate_or_out_of_range_cursors_are_preserved ... ok
test channels::cursor_tests::concurrent_reads_have_one_current_receipt_and_do_not_advance_cursor ... ok
test channels::tests::catalogue_reports_unavailable_mailbox_without_fabricated_atomic_snapshot ... ok
test channels::tests::caps_names_and_conflicting_payload_do_not_mutate_store ... ok
test channels::cursor_tests::unwatch_discards_only_requested_progress_and_rewatch_explicitly_redelivers ... ok
test channels::cursor_tests::watches_delivery_and_ack_survive_restart_without_skipping_later_posts ... ok
test channels::tests::changed_target_is_a_conflict_and_corrupt_or_unsafe_sources_are_preserved ... ok
test change_records_tests::concurrent_publications_share_session_gate_and_preserve_contiguous_sequence ... ok
test channels::cursor_tests::receipts_are_actor_scoped_and_new_reads_supersede_old_deliveries ... ok
test channels::tests::credentials_scope_sender_and_direct_alias_follow_mailbox_authority ... ok
test channels::cursor_tests::legacy_snapshots_and_reader_capacity_keep_accepted_lines_intact ... ok
test channels::tests::simultaneous_first_posts_in_different_scopes_keep_independent_sequences ... ok
test channels::tests::unsafe_directory_and_unknown_line_fields_are_not_repaired ... ok
test mailbox_tests::actor_scope_and_private_child_lineage_reject_metadata_forgery ... ok
test channels::tests::contiguous_reads_and_catalogue_obey_exact_byte_and_row_caps ... ok
test mailbox_tests::full_legacy_mailbox_remains_readable_but_rejects_another_append ... ok
test channels::tests::named_order_dedup_and_catalogue_survive_restart ... ok
test mailbox_tests::legacy_parent_and_generic_fields_cannot_forge_trusted_lineage ... ok
test mailbox_tests::old_mailbox_lines_gain_stable_read_identity_without_eager_rewrite ... ok
test channels::tests::named_publication_faults_preserve_or_reconcile_without_false_notifications ... ok
test mailbox_tests::reserved_mailbox_buffer_mutation_and_invalid_posts_preserve_bytes ... ok
test mailbox_tests::ambiguous_post_failure_is_resolved_by_message_id_without_duplicate_append ... ok
test mailbox_tests::receipt_ack_survives_restart_and_never_skips_later_posts_or_other_actor_cursor ... ok
test mapping_tests::durable_reconnect_keeps_transcript_bytes_and_rejects_metadata_authority ... ok
test mapping_tests::scope_input_bounds_and_explicit_conversation_types_are_checked ... ok
test mapping_tests::damaged_indices_and_targets_are_preserved_without_adoption ... ok
test mapping_tests::every_missing_scope_component_is_connection_local ... ok
test observations::tests::changing_file_during_read_is_an_unstable_best_effort_snapshot ... ok
test mapping_tests::stale_revision_and_held_os_lock_never_create_sessions ... ok
test observations::tests::descriptor_and_provider_changes_do_not_share_verdict_freshness ... ok
test observations::tests::inconsistent_completion_or_identity_fields_cannot_create_known_success ... ok
test observations::tests::configured_path_cannot_be_overridden_and_reports_do_not_mutate_sessions ... ok
test observations::tests::report_counts_only_observed_completions_and_preserves_legacy_unknowns ... ok
test observations::tests::malformed_partial_and_rotated_evidence_is_bounded_and_explicit ... ok
test mapping_tests::symlink_target_and_index_are_refused_without_touching_destination ... ok
test observations::tests::verdicts_compare_only_same_source_and_latest_observed_revisions ... ok
test observations::tests::report_distinguishes_disabled_missing_empty_and_unavailable_sources ... ok
test mailbox_tests::acknowledgement_failure_preserves_unread_or_reports_only_already_delivered_progress ... ok
test recovery::tests::changed_source_at_commit_keeps_newer_snapshot_and_original_backup ... ok
test recovery::tests::recovery_reports_are_distinct_fresh_and_read_only ... ok
test recovery::tests::stale_repair_requests_and_existing_backups_preserve_all_bytes ... ok
test repair_tests::explicit_empty_legacy_repair_preserves_backup_and_refuses_conversation_data ... ok
test retention_tests::bad_metadata_and_snapshot_bounds_fail_closed ... ok
test retention_tests::busy_journal_lock_and_cutoff_or_batch_errors_have_no_deletion_effect ... ok
test observations::tests::source_and_response_caps_never_truncate_json_or_expose_bodies ... ok
test mailbox_tests::same_message_id_is_idempotent_and_concurrent_posts_have_distinct_positions ... ok
test mapping_tests::mapping_publication_failures_preserve_index_and_report_orphan ... ok
test retention_tests::journal_backup_and_job_symlink_or_traversal_never_touch_outside_evidence ... ok
test retention_tests::partial_backup_or_malformed_journal_blocks_resume_and_preserves_all_evidence ... ok
test retention_tests::protection_changes_are_cas_checked_and_leave_transcripts_unchanged ... ok
test mailbox_tests::bounded_delivery_and_failed_read_persistence_leave_all_messages_unacknowledged ... ok
test roster::tests::parent_first_cycle_order_and_private_parent_suppression_are_deterministic ... ok
test roster::tests::bounded_scan_never_claims_a_complete_or_global_scope_count ... ok
test roster::tests::caps_are_full_response_utf8_bytes_and_digest_binds_returned_projection ... ok
test roster::tests::phase_projection_excludes_payloads_and_does_not_invent_duration ... ok
test tests::checkpoint_failure_before_rename_changes_nothing ... ok
test tests::concurrent_expected_revision_writes_have_one_winner ... ok
test tests::corrupt_snapshot_is_preserved_and_diagnosed_without_overwrite ... ok
test tests::a_session_round_trips_through_its_file ... ok
test tests::deletion_failure_preserves_state_and_uncertain_deletion_matches_disk ... ok
test tests::cwd_changes_are_rejected_during_active_runs_and_advance_revision_otherwise ... ok
test retention_tests::preview_counts_records_and_bytes_and_retains_every_authoritative_protection ... ok
test tests::first_checkpoint_creates_one_transcript_reused_across_restart ... ok
test channels::tests::serialized_storage_cap_refuses_append_without_eviction ... ok
test tests::incomplete_session_files_are_reported_without_defaults_or_rewriting ... ok
test tests::generic_mutation_of_the_canonical_transcript_is_rejected ... ok
test tests::concurrent_session_checkpoints_keep_one_revision_winner_and_unique_buffer_ids ... ok
test tests::interrupted_run_state_is_exposed_without_executing_anything ... ok
test retention_tests::resume_refuses_new_protection_and_same_id_replacement_even_with_identical_bytes ... ok
test tests::malformed_and_oversized_records_fail_without_changing_data ... ok
test tests::independent_sessions_do_not_wait_for_another_sessions_gate ... ok
test tests::store_location_is_required_and_invalid_config_is_rejected ... ok
test tests::malformed_buffer_ownership_is_not_loaded_or_rewritten ... ok
test tests::post_rename_failure_reports_uncertainty_and_reloads_visible_state ... ok
test tests::new_nested_store_is_created_and_unicode_changes_survive_restart ... ok
test tests::unattached_buffers_remain_memory_only_and_survive_other_session_commits ... ok
test tests::sub_agent_session_records_parent_and_mailbox_round_trips_restart ... ok
test tests::sessions_and_ordinary_buffers_round_trip ... ok
test retention_tests::post_preview_activity_pin_reference_and_revision_changes_refuse_without_transcript_mutation ... ok
test tests::every_pre_rename_failure_preserves_all_mutations_and_notifications ... ok
test retention_tests::every_durable_interruption_resumes_only_recorded_targets_and_preserves_backups ... ok
test channels::cursor_tests::every_cursor_publication_fault_preserves_lines_and_exposes_visible_progress ... ok
test change_records_tests::bounded_log_and_pages_refuse_stale_or_overflow_without_eviction ... ok

test result: ok. 89 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 17.86s

   Doc-tests sessions

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s


```
