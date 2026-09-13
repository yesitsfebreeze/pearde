---
commit: de1406682a33c5b12cb472787178e2570e5ed0f8
spec-digests: {"spec01.md":"829e2fe6b1eff2bf1f47fbeb22fb84703a5284dd85284a5c58e299cd014fa94d"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/fs/prds/improve-fs-revision-guards/specs/spec01.md: exit 0

Command SHA-256: d7f6c923c6d32c4efc3c792e69c7fca9ff1a1cff4dcd07c3d5c264fac6f39610

```text
    Finished `test` profile [unoptimized] target(s) in 0.07s
     Running unittests src/main.rs (target/tool-result-contract/debug/deps/fs-54056baceabd5b7a)

running 47 tests
test search::tests::empty_stages_is_an_empty_set_never_a_sweep ... ok
test context::tests::typed_record_case_aliases_and_directory_identities_are_excluded ... ok
test context::tests::exact_bytes_and_source_revisions_preserve_every_newline ... ok
test context::tests::strict_caps_and_unavailable_sources_never_return_partial_text ... ok
test search::tests::incompatible_stages_reject_before_execution ... ok
test search::tests::cursor_scope_expiry_and_cancellation_are_explicit ... ok
test search::tests::captured_pages_replay_after_tree_changes_and_new_queries_refresh ... ok
test search::tests::match_set_cannot_be_grepped_without_files_of ... ok
test context::tests::pinned_handle_refuses_observed_replacement_and_deadline_drops_response ... ok
test search::tests::missing_rg_is_actionable_not_empty ... ok
test search::tests::active_search_cancellation_reaps_the_backend ... ok
test search::tests::deadline_covers_child_wait_after_stdout_is_closed ... ok
test search::tests::deadlock_deadline_terminates_and_reaps_child ... ok
test search::tests::pre_cancelled_invocation_spawns_no_process ... ok
test search::tests::large_real_tree_pages_every_identity_once_and_ref_keeps_the_tail ... ok
test search::tests::page_has_a_continuation_for_the_rest ... ok
test search::tests::snapshot_budget_fails_without_eviction_and_retirement_frees_it ... ok
test service::tests::cancel_during_spawn_prevents_mutation ... ok
test service::tests::cancellation_after_preparation_leaves_no_mutation_or_temp ... ok
test search::tests::real_grep_keeps_over_200_matches_and_empty_chains_do_not_sweep ... ok
test service::tests::competing_sessions_with_one_observed_revision_have_one_winner ... ok
test service::tests::concurrent_creators_preserve_the_winner ... ok
test service::tests::commit_rechecks_symlinks_and_preserves_executable_modes ... ok
test service::tests::describe_names_and_schemas_match_the_three_keys ... ok
test service::tests::create_overwrite_and_edit_variants ... ok
test service::tests::failed_preparation_preserves_bytes_and_permissions ... ok
test service::tests::disappearance_and_creation_at_publication_are_conflicts ... ok
test service::tests::newer_bytes_at_commit_survive_write_and_edit ... ok
test service::tests::observation_failure_after_publication_is_explicit_partial_success ... ok
test service::tests::partial_read_establishes_freshness_only ... ok
test service::tests::pre_cancelled_call_never_mutates ... ok
test service::tests::path_escapes_and_forged_context_fail_before_mutation ... ok
test service::tests::read_byte_limit_truncates ... ok
test service::tests::read_offsets_limits_binary_and_missing ... ok
test service::tests::stale_version_fails_until_reread_including_same_size_with_restored_mtime ... ok
test service::tests::touch_failure_reports_partial_success_with_the_file ... ok
test service::tests::unread_overwrite_fails_without_changing_bytes ... ok
test service::tests::touch_records_successful_mutations_only ... ok
test service::tests::unseen_edit_fails_without_changing_bytes ... ok
test search::tests::fake_rg_error_exit_is_a_failure ... ok
test search::tests::fake_rg_receives_literal_arguments_no_shell ... ok
test search::tests::malformed_backend_output_fails_explicitly ... ok
test search::tests::matching_json_backend_produces_typed_items ... ok
test search::tests::output_survives_cancellation_polls ... ok
test search::tests::oversized_results_report_truncation ... ok
test search::tests::user_config_cannot_change_results ... ok
test search::tests::floods_and_oversized_items_fail_instead_of_claiming_completeness ... ok

test result: ok. 47 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 1.22s


```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/fs/prds/improve-fs-revision-guards/specs/spec01.md: exit 0

Command SHA-256: 24fefe87c4309d2ebf7c7d7c514681d94cbec8b884bc37b93bd249fd18253bb4

```text
    Finished `dev` profile [unoptimized] target(s) in 0.07s
    Finished `test` profile [unoptimized] target(s) in 0.13s
     Running unittests src/main.rs (target/tool-result-contract/debug/deps/gitfs-4eb57900a7770a88)

running 38 tests
test push::tests::receipt_looking_prose_or_conflicting_trailers_do_not_authorize_push ... ok
test push::tests::hook_requires_exactly_one_complete_advertised_update ... ok
test secrets::tests::template_files_are_skipped_entirely ... ok
test secrets::tests::sensitive_filename_is_flagged_even_with_plain_content ... ok
test secrets::tests::has_secret_detects_and_allows_plain ... ok
test secrets::tests::context_lines_are_not_scanned ... ok
test secrets::tests::real_key_on_added_line_finds ... ok
test ship::tests::auto_subject_shapes ... ok
test ship::tests::active_cancellation_is_exact_bounded_and_drop_cancels_the_blocking_work ... ok
test ship::tests::configured_gate_and_author_are_validated_instead_of_defaulting_invalid_types ... ok
test ship::tests::gate_prompt_demands_json_only ... ok
test ship::tests::preview_revision_binds_author_required_gate_timeout_subject_and_force ... ok
test ship::tests::secret_subject_is_rejected_and_plain_passes ... ok
test secrets::tests::placeholder_token_is_ignored ... ok
test secrets::tests::scan_file_matches ... ok
test store::tests::missing_publication_ack_remains_unknown_after_later_advance_or_failed_readback ... ok
test push::tests::cancelled_command_kills_the_spawned_helper_group ... ok
test push::tests::command_timeout_and_overflow_are_bounded_and_do_not_expose_stderr ... ok
test service::snapshot_tests::read_failures_report_partial_success_and_preserve_failed_overlay ... ok
test service::snapshot_tests::guarded_edit_still_refuses_stale_content ... ok
test store::tests::materialize_guard ... ok
test store::tests::concurrent_reviewed_publications_have_one_winner_and_preserve_worktree_and_index ... ok
test store::tests::prepared_head_transaction_holds_the_symbolic_branch_until_decision ... ok
test store::tests::multi_path_overlay_survives_rewrite ... ok
test tool_result::tests::inspection_baseline_diff_is_available ... ok
test tool_result::tests::inspection_baseline_read_does_not_create_a_store ... ok
test service::snapshot_tests::selection_is_exact_empty_is_empty_and_unowned_is_rejected_before_writes ... ok
test tool_result::tests::invalid_inputs_do_not_open_the_store ... ok
test tool_result::tests::payloads_are_encoded_once_and_text_stays_literal ... ok
test push::tests::durable_attempt_capacity_corruption_and_monotonic_observation ... ok
test store::tests::roundtrip_and_noop ... ok
test store::tests::concurrent_overlay_writes_keep_every_path ... ok
test store::tests::unrelated_overlay_sessions_do_not_share_a_mutation_lock ... ok
test tool_result::tests::inspection_absence_binary_bounds_and_path_failures_are_explicit ... ok
test store::tests::ship_trailer_undo_and_no_remote ... ok
test store::tests::reviewed_publication_refuses_stale_head_without_deleting_new_unowned_files ... ok
test store::tests::reviewed_publication_binds_index_overlay_branch_and_repository_identity ... ok
test tool_result::tests::real_consumers_share_the_tool_result_contract ... ok

test result: ok. 38 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 14.68s


```
