---
commit: 75e76e63d8f97954759bf294f4b0d86d78d5643b
spec-digests: {"spec01.md":"e8a3f053f79f2b0c01106e479b4ba9c763d91022dfddb450c6e4202f46cd98a7"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/gitfs/prds/absorb-fs-and-give-file-work-branch-backed-commits/merge-fs-source-into-gitfs-with-no-behavior-change/specs/spec01.md: exit 0

Command SHA-256: e48df62b16eaf17ad5b346381235cd9023ac5c186b7d5b8ace3b1664df29787c

```text
    Finished `dev` profile [unoptimized] target(s) in 0.08s
   Compiling fs v0.1.0 (/Users/feb/dev/cartridge/fs.ctg)
    Finished `test` profile [unoptimized] target(s) in 2.38s
     Running unittests src/lib.rs (target/debug/deps/fs-0d00c14b9791433b)

running 109 tests
test manifest::the_manifest_carries_every_tool_schema ... ok
test context::tests::typed_record_case_aliases_and_directory_identities_are_excluded ... ok
test provenance::tests::context_is_bounded_and_legacy_missing_coordinates_stay_null ... ok
test context::tests::strict_caps_and_unavailable_sources_never_return_partial_text ... ok
test context::tests::exact_bytes_and_source_revisions_preserve_every_newline ... ok
test files::git_mode_tests::local_mode_and_a_workspace_outside_git_write_the_worktree ... ok
test context::tests::pinned_handle_refuses_observed_replacement_and_deadline_drops_response ... ok
test provenance::tests::nonregular_or_alias_preimages_are_rejected_without_waiting_for_a_writer ... ok
test provenance::tests::receipt_validation_rejects_arbitrary_success_or_wrong_publications ... ok
test provenance::tests::locked_overlay_receipts_pin_old_blob_tip_and_first_parent_without_inventing_overlay ... ok
test push::tests::cancelled_command_kills_the_spawned_helper_group ... ok
test overlay::snapshot_tests::read_failures_report_partial_success_and_preserve_failed_overlay ... ok
test push::tests::hook_requires_exactly_one_complete_advertised_update ... ok
test push::tests::receipt_looking_prose_or_conflicting_trailers_do_not_authorize_push ... ok
test provenance::tests::materialize_keeps_exact_applied_evidence_and_reports_failed_deletion_and_ledger ... ok
test push::tests::command_timeout_and_overflow_are_bounded_and_do_not_expose_stderr ... ok
test search::tests::captured_pages_replay_after_tree_changes_and_new_queries_refresh ... ok
test search::tests::cursor_scope_expiry_and_cancellation_are_explicit ... ok
test overlay::snapshot_tests::selected_snapshot_records_only_new_commits_and_retains_partial_evidence ... ok
test search::tests::empty_stages_is_an_empty_set_never_a_sweep ... ok
test search::tests::active_search_cancellation_reaps_the_backend ... ok
test overlay::snapshot_tests::selection_is_exact_empty_is_empty_and_unowned_is_rejected_before_writes ... ok
test search::tests::deadline_covers_child_wait_after_stdout_is_closed ... ok
test search::tests::deadlock_deadline_terminates_and_reaps_child ... ok
test search::tests::incompatible_stages_reject_before_execution ... ok
test provenance::tests::concurrent_same_session_receipts_form_the_actual_locked_commit_chain ... ok
test search::tests::match_set_cannot_be_grepped_without_files_of ... ok
test search::tests::fake_rg_error_exit_is_a_failure ... ok
test search::tests::missing_rg_is_actionable_not_empty ... ok
test search::tests::fake_rg_receives_literal_arguments_no_shell ... ok
test files::git_mode_tests::git_mode_commits_each_change_and_leaves_the_worktree_until_materialize ... ok
test search::tests::page_has_a_continuation_for_the_rest ... ok
test search::tests::pre_cancelled_invocation_spawns_no_process ... ok
test search::tests::real_grep_keeps_over_200_matches_and_empty_chains_do_not_sweep ... ok
test search::tests::snapshot_budget_fails_without_eviction_and_retirement_frees_it ... ok
test search::tests::malformed_backend_output_fails_explicitly ... ok
test secrets::tests::context_lines_are_not_scanned ... ok
test secrets::tests::has_secret_detects_and_allows_plain ... ok
test secrets::tests::placeholder_token_is_ignored ... ok
test secrets::tests::real_key_on_added_line_finds ... ok
test secrets::tests::scan_file_matches ... ok
test secrets::tests::sensitive_filename_is_flagged_even_with_plain_content ... ok
test secrets::tests::template_files_are_skipped_entirely ... ok
test service::tests::cancel_during_spawn_prevents_mutation ... ok
test service::tests::cancellation_after_preparation_leaves_no_mutation_or_temp ... ok
test service::tests::commit_rechecks_symlinks_and_preserves_executable_modes ... ok
test service::tests::competing_sessions_with_one_observed_revision_have_one_winner ... ok
test service::tests::concurrent_creators_preserve_the_winner ... ok
test search::tests::matching_json_backend_produces_typed_items ... ok
test service::tests::describe_names_and_schemas_match_the_three_keys ... ok
test service::tests::create_overwrite_and_edit_variants ... ok
test service::tests::direct_evidence_uses_guarded_bytes_and_unique_publication_identity ... ok
test service::tests::failed_cleanup_after_known_publication_still_records_once ... ok
test service::tests::disappearance_and_creation_at_publication_are_conflicts ... ok
test service::tests::failed_preparation_preserves_bytes_and_permissions ... ok
test service::tests::observation_failure_after_publication_is_explicit_partial_success ... ok
test service::tests::partial_read_establishes_freshness_only ... ok
test service::tests::newer_bytes_at_commit_survive_write_and_edit ... ok
test service::tests::pre_cancelled_call_never_mutates ... ok
test service::tests::path_escapes_and_forged_context_fail_before_mutation ... ok
test service::tests::read_byte_limit_truncates ... ok
test service::tests::receipt_requires_exact_id_publication_digest_and_one_persisted_sequence ... ok
test service::tests::read_offsets_limits_binary_and_missing ... ok
test service::tests::stale_version_fails_until_reread_including_same_size_with_restored_mtime ... ok
test service::tests::touch_failure_reports_partial_success_with_the_file ... ok
test search::tests::output_survives_cancellation_polls ... ok
test service::tests::touch_records_successful_mutations_only ... ok
test service::tests::unread_overwrite_fails_without_changing_bytes ... ok
test service::tests::unseen_edit_fails_without_changing_bytes ... ok
test ship::tests::active_cancellation_is_exact_bounded_and_drop_cancels_the_blocking_work ... ok
test ship::tests::auto_subject_shapes ... ok
test ship::tests::configured_gate_and_author_are_validated_instead_of_defaulting_invalid_types ... ok
test ship::tests::gate_prompt_demands_json_only ... ok
test ship::tests::preview_revision_binds_author_required_gate_timeout_subject_and_force ... ok
test ship::tests::secret_subject_is_rejected_and_plain_passes ... ok
test ship::valid_config_tests::settled_defaults_are_valid ... ok
test source::tests::exact_bytes_empty_text_and_untrusted_native_shape_checks ... ok
test source::tests::nomination_slots_do_not_refill_and_failures_do_not_remove_other_rows ... ok
test source::tests::trusted_allowlist_validates_counts_id_paths_and_typed_namespace_aliases ... ok
test service::tests::whole_read_of_long_file_is_refused_and_establishes_nothing ... ok
test search::tests::oversized_results_report_truncation ... ok
test search::tests::user_config_cannot_change_results ... ok
test store::tests::missing_publication_ack_remains_unknown_after_later_advance_or_failed_readback ... ok
test search::tests::large_real_tree_pages_every_identity_once_and_ref_keeps_the_tail ... ok
test search::tests::floods_and_oversized_items_fail_instead_of_claiming_completeness ... ok
test store::tests::concurrent_reviewed_publications_have_one_winner_and_preserve_worktree_and_index ... ok
test store::tests::materialize_guard ... ok
test store::tests::concurrent_overlay_writes_keep_every_path ... ok
test store::tests::multi_path_overlay_survives_rewrite ... ok
test store::tests::roundtrip_and_noop ... ok
test store::tests::unrelated_overlay_sessions_do_not_share_a_mutation_lock ... ok
test tool_result::tests::inspection_baseline_diff_is_available ... ok
test store::tests::prepared_head_transaction_holds_the_symbolic_branch_until_decision ... ok
test tool_result::tests::inspection_absence_binary_bounds_and_path_failures_are_explicit ... ok
test tool_result::tests::payloads_are_encoded_once_and_text_stays_literal ... ok
test worker::tests::a_failed_or_cancelled_bail_and_a_late_reply_are_refused ... ok
test worker::tests::digest_refuses_more_than_the_worker_budget_and_paths_outside_the_workspace ... ok
test worker::tests::digest_sends_numbered_files_and_returns_the_worker_answer ... ok
test tool_result::tests::invalid_inputs_do_not_open_the_store ... ok
test worker::tests::draft_strips_fences_and_writes_the_target_through_the_guarded_write ... ok
test worker::tests::integration_digests_the_longest_source_file_and_reports_the_saving ... ok
test tool_result::tests::inspection_baseline_ls_does_not_create_a_store ... ok
test store::tests::reviewed_publication_refuses_stale_head_without_deleting_new_unowned_files ... ok
test store::tests::ship_trailer_undo_and_no_remote ... ok
test service::tests::recording_timeout_is_bounded_unknown_and_never_replays_file_publication ... ok
test store::tests::reviewed_publication_binds_index_overlay_branch_and_repository_identity ... ok
test provenance::tests::metadata_caps_and_unreadable_preimage_never_claim_complete_attribution ... ok
test push::tests::durable_attempt_capacity_corruption_and_monotonic_observation ... ok
test provenance::tests::real_bulk_materialization_preserves_effects_after_record_cap_and_late_write_failure ... ok

test result: ok. 109 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 34.34s

     Running unittests src/bin/gitfs-hook.rs (target/debug/deps/gitfs_hook-359055ecb25d296e)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s


```
