---
commit: 3a79023311b1a9b30c383ec8c71cf31c20a69ee7
spec-digests: {"spec01.md":"989a4c774c063cbd1fbc14a7cda17c37b29fadad66268e2067f0dfdceb9b3c68"}
child-contracts: {".cartridge/boards/fs/prds/improve-fs-change-provenance/direct-file-mutations-report-revisions/prd.md":"f537bb0a63e9942094f04c5e9d10a768b59914b1035673d863827cdbf096fa9f"}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/fs/prds/improve-fs-change-provenance/specs/spec01.md: exit 0

Command SHA-256: 8c7c21011d420ce02e3035b7da38e2725aef1d221e42a0346662436fd6084916

```text
{
  "source_commit": "3a79023311b1a9b30c383ec8c71cf31c20a69ee7",
  "records_commit": "da3708c96b26d32240189c68f292478337fefedb",
  "footprint": [
    ".cartridge/docs/change-provenance.md",
    ".cartridge/tests/integration/change-provenance.test.ts",
    ".cartridge/tests/unit/service/tests.rs",
    "Cargo.toml",
    "src/files.rs",
    "src/main.rs",
    "src/service.rs"
  ],
  "dependencies": [
    {
      "ref": "@fs/improve-fs-change-provenance/direct-file-mutations-report-revisions",
      "source_commit": "3a79023311b1a9b30c383ec8c71cf31c20a69ee7",
      "prd_sha256": "874c31414a7d236a4021b8f40661e54ae1d7391cb288c3b53b31533f077bc705",
      "spec_sha256": "7f555535bc670f5f6b81eba76005ef6527b1861aa1bbde12366a336ece545235",
      "review_round": 3,
      "score": 95,
      "review_sha256": "55978d3381f6065e7932d4b634d6def9cbb66da2eb78079fbdd961b5ba605c9e",
      "collection_sha256": "4c8da549485588cf1af071bc902a54cbf8fb89c93f1f9a8c325226ae3b17f0b2"
    },
    {
      "ref": "@fs/improve-fs-revision-guards",
      "source_commit": "3a79023311b1a9b30c383ec8c71cf31c20a69ee7",
      "prd_sha256": "cdacea0193df104b21f7c2e4d7c90c047773e0f704e6054dd6d1884f1b9a5d4f",
      "spec_sha256": "78fe6d4d246cd3242bb1d3350cad68982c04e2fd9ba14fb5e1c9b6b23f5c6692",
      "review_round": 4,
      "score": 95,
      "review_sha256": "9cbf0ed11fed360d61e23ef5f8e569b46b4ae3dffaedc4bf86e8da9cc871adf1",
      "collection_sha256": "7d09eca0a9d3ada87633965f6f06c63fdc8a143b564af7e5bc47e2a2f3a1f131"
    },
    {
      "ref": "@gitfs/improve-gitfs-readable-diff",
      "source_commit": "b8f27c6f1c07888bfc6e5d09f45a8751e8ca7b36",
      "prd_sha256": "e0ec8ea766792e75bd2d52023d32fbcb855811bd682f8f0226a1db0fa804c0dc",
      "spec_sha256": "6ed56a3426a0c5bf5039a2622785a66c6050c7da0b3a3b60aacfd06e437426e7",
      "review_round": 3,
      "score": 94,
      "review_sha256": "e902695dc87b19e2b5e44fc47de8449f7254930647221216911dde9027ba3251",
      "collection_sha256": "34f5f352c4dcd05d7b0845bb24bd95fe57cdf95e645a962a6d0d0c0399485406"
    },
    {
      "ref": "@gitfs/overlay-mutations-report-revisions",
      "source_commit": "b8f27c6f1c07888bfc6e5d09f45a8751e8ca7b36",
      "prd_sha256": "917a66a3cbb21cb3a4cf6b8e3594e6ddd967e23e2aadb9dbabc1b499fa929775",
      "spec_sha256": "05db280989830d7933859d5d87e2796d0513ed4147e3976883604e1536a8963a",
      "review_round": 3,
      "score": 94,
      "review_sha256": "6ff5b446a04451a7deda8d3516938ed4638d4ba667575be2200156b7ccc68df5",
      "collection_sha256": "71666fa28c495ada609941e8cf9a649201eb624c02cdfd96f520bf49a8dc3763"
    },
    {
      "ref": "@gitfs/tool-results-interoperate",
      "source_commit": "b8f27c6f1c07888bfc6e5d09f45a8751e8ca7b36",
      "prd_sha256": "a284102ceabf68ab6000f37992c22585feefd1076891db81c7d56acede6f0af0",
      "spec_sha256": "87b2a12e71d8a7eab761833e18236315866bf8e5cfbe470738c90cc6a3de9cb4",
      "review_round": 3,
      "score": 96,
      "review_sha256": "0e016083c728e357a89a6b6b810b0bdf05949739f4f4aa608afcaeb091fc25e5",
      "collection_sha256": "6518ff6407b4bcc34a1b25781d056d246bc4b81d418be63fe10b36ab72eed922"
    },
    {
      "ref": "@policy/improve-policy-operation-rules",
      "source_commit": "e442bef2c9f07635f9e8b8e1d87a47193841569f",
      "prd_sha256": "ff05aeecfbc1ede7603d452dcb2635af3b4b0032f04df971aba3281eb5e69124",
      "spec_sha256": "4c387100550778313009dff4a94703b2b6232c874fe469f56167f487e05d707d",
      "review_round": 3,
      "score": 97,
      "review_sha256": "ddeebac92d47d82b4c4db0186e24797edc35d789e58fa923a2b9ee5493049296",
      "collection_sha256": "79e27879d6b8a09e58e723a998a188342c8be26e98a736079108af1d1c2f13e8"
    },
    {
      "ref": "@runtime/shipped-gitfs-profiles-grant-change-recording",
      "source_commit": "bd3b5e78d6e3ddd7dc7567b0c357d6fe60bd02df",
      "prd_sha256": "45067b0b6e40bb01f798a71ea07ec8d9118a52cfb18e27d384a82220cc8b1635",
      "spec_sha256": "588cfb528eab818b0851b2f28ef2ad922a553640762b0fbe47907c8e2701ea52",
      "review_round": 3,
      "score": 96,
      "review_sha256": "53d633436c43c4c51c82adc3189f50bd40d83c5c252f89e82e0062d960642c48",
      "collection_sha256": "70b6c3167492efd2970906a90987d0c26a303efff80606260153b5a81e880fa9"
    },
    {
      "ref": "@sessions/file-change-records-retain-reported-revisions",
      "source_commit": "92240c6ba415f53b2d17971aea185536a6f517bc",
      "prd_sha256": "8bc317ff09911541672a00cb358c6aa64837f2da857fef2f9c18d9a6a004936a",
      "spec_sha256": "451e40c25cd45b7985aaf6c54117d26e768313e860ec6b5c0f2a555a5e2cacce",
      "review_round": 3,
      "score": 96,
      "review_sha256": "7b69e2d01c9c7048df611b8b3d608febabc676707bd963f2623d209384445218",
      "collection_sha256": "e430fa9e6415fb5f680dc363a0d6eddd8df2fb469303f416dfa36ddb21cbc540"
    },
    {
      "ref": "@sessions/improve-sessions-client-mapping",
      "source_commit": "92240c6ba415f53b2d17971aea185536a6f517bc",
      "prd_sha256": "a2d7d336d02eac81875c6e2bbec066953e103e885ea72eeb061976190a178e30",
      "spec_sha256": "1932efa0850b4ba5c0457eba108b7d85a5a94dffa41b3e5c9b08a58ddced0a85",
      "review_round": 3,
      "score": 96,
      "review_sha256": "4e4e69a466fdedaa7f85b57d8be6cec826086d8c7605f2b227f1bf34866848ee",
      "collection_sha256": "602c35e8766c15ea0a71f24e1be096fa558665c14f68c0b7d8ee213c60b3192c"
    }
  ],
  "fixtures": {
    "/Users/feb/dev/cartridge/fs.ctg/.cartridge/tests/integration/context.test.ts": "5239eacb5463d1a6e032c0c6cd22ff370458d574621ac3a5ec486de4244b1264",
    "/Users/feb/dev/cartridge/fs.ctg/.cartridge/tests/integration/change-provenance.test.ts": "fd336db0d75f54db3b6a01ca5fb5700437e2d0fd455d4ea1c266163edb7f4173",
    "/Users/feb/dev/cartridge/gitfs.ctg/.cartridge/tests/integration/change-provenance.test.ts": "db018e5ea32233f4ca8c4ff3e1bc0dbab59b5a85c3510f93c1eebc7af9f7e9a5",
    "/Users/feb/dev/cartridge/gitfs.ctg/.cartridge/tests/integration/tool-result.test.ts": "1c7d95e7cb20545b2dd3d67196dfdd096ad67b1fbad281f285ba0ca6e5016033",
    "/Users/feb/dev/cartridge/gitfs.ctg/.cartridge/tests/integration/reviewed-ship.test.ts": "2cd16fcb495650e8266fb5cdf660e868f656b547768e4777dd1e9c996fc806f9",
    "/Users/feb/dev/cartridge/gitfs.ctg/.cartridge/tests/integration/recorded-push.test.ts": "0c6b4e111e2aea72d3736b5df433a6998ced1d076a417179b75e78361da4953a",
    "/Users/feb/dev/cartridge/sessions.ctg/.cartridge/tests/integration/change-records.test.ts": "56611256a47d763dd4ebe014e7b82f122888a483009f182c33df4812a8eaee42"
  }
}

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/fs/prds/improve-fs-change-provenance/specs/spec01.md: exit 0

Command SHA-256: 480eecae37c36634b36e9a215d58cdfcee605bb8bc8ca2e440566a4c0839f9c8

```text
    Finished `test` profile [unoptimized] target(s) in 0.08s
     Running unittests src/main.rs (target/tool-result-contract/debug/deps/fs-0ae3e717031e9602)

running 51 tests
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
test search::tests::deadline_covers_child_wait_after_stdout_is_closed ... ok
test search::tests::deadlock_deadline_terminates_and_reaps_child ... ok
test search::tests::active_search_cancellation_reaps_the_backend ... ok
test search::tests::pre_cancelled_invocation_spawns_no_process ... ok
test search::tests::page_has_a_continuation_for_the_rest ... ok
test search::tests::snapshot_budget_fails_without_eviction_and_retirement_frees_it ... ok
test search::tests::large_real_tree_pages_every_identity_once_and_ref_keeps_the_tail ... ok
test service::tests::cancel_during_spawn_prevents_mutation ... ok
test search::tests::real_grep_keeps_over_200_matches_and_empty_chains_do_not_sweep ... ok
test service::tests::cancellation_after_preparation_leaves_no_mutation_or_temp ... ok
test service::tests::competing_sessions_with_one_observed_revision_have_one_winner ... ok
test service::tests::concurrent_creators_preserve_the_winner ... ok
test service::tests::commit_rechecks_symlinks_and_preserves_executable_modes ... ok
test service::tests::describe_names_and_schemas_match_the_three_keys ... ok
test service::tests::create_overwrite_and_edit_variants ... ok
test service::tests::disappearance_and_creation_at_publication_are_conflicts ... ok
test service::tests::direct_evidence_uses_guarded_bytes_and_unique_publication_identity ... ok
test service::tests::failed_preparation_preserves_bytes_and_permissions ... ok
test service::tests::failed_cleanup_after_known_publication_still_records_once ... ok
test service::tests::observation_failure_after_publication_is_explicit_partial_success ... ok
test service::tests::newer_bytes_at_commit_survive_write_and_edit ... ok
test service::tests::partial_read_establishes_freshness_only ... ok
test service::tests::pre_cancelled_call_never_mutates ... ok
test service::tests::read_byte_limit_truncates ... ok
test service::tests::path_escapes_and_forged_context_fail_before_mutation ... ok
test service::tests::read_offsets_limits_binary_and_missing ... ok
test service::tests::receipt_requires_exact_id_publication_digest_and_one_persisted_sequence ... ok
test service::tests::stale_version_fails_until_reread_including_same_size_with_restored_mtime ... ok
test service::tests::touch_failure_reports_partial_success_with_the_file ... ok
test service::tests::touch_records_successful_mutations_only ... ok
test service::tests::unread_overwrite_fails_without_changing_bytes ... ok
test service::tests::unseen_edit_fails_without_changing_bytes ... ok
test search::tests::fake_rg_error_exit_is_a_failure ... ok
test search::tests::fake_rg_receives_literal_arguments_no_shell ... ok
test search::tests::malformed_backend_output_fails_explicitly ... ok
test search::tests::matching_json_backend_produces_typed_items ... ok
test search::tests::output_survives_cancellation_polls ... ok
test search::tests::oversized_results_report_truncation ... ok
test search::tests::user_config_cannot_change_results ... ok
test search::tests::floods_and_oversized_items_fail_instead_of_claiming_completeness ... ok
test service::tests::recording_timeout_is_bounded_unknown_and_never_replays_file_publication ... ok

test result: ok. 51 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 2.37s

    Checking fs v0.1.0 (/Users/feb/dev/cartridge/fs.ctg)
    Finished `dev` profile [unoptimized] target(s) in 0.62s

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/fs/prds/improve-fs-change-provenance/specs/spec01.md: exit 0

Command SHA-256: 336aacbbec058325d320be94456d112b0173b3cf0bdcf575c30bd719586c4145

```text
    Finished `test` profile [unoptimized] target(s) in 0.12s
     Running unittests src/main.rs (target/tool-result-contract/debug/deps/gitfs-c66fa7605aaad949)

running 47 tests
test provenance::tests::context_is_bounded_and_legacy_missing_coordinates_stay_null ... ok
test push::tests::cancelled_command_kills_the_spawned_helper_group ... ok
test push::tests::hook_requires_exactly_one_complete_advertised_update ... ok
test push::tests::receipt_looking_prose_or_conflicting_trailers_do_not_authorize_push ... ok
test secrets::tests::context_lines_are_not_scanned ... ok
test secrets::tests::has_secret_detects_and_allows_plain ... ok
test secrets::tests::placeholder_token_is_ignored ... ok
test secrets::tests::real_key_on_added_line_finds ... ok
test secrets::tests::scan_file_matches ... ok
test secrets::tests::sensitive_filename_is_flagged_even_with_plain_content ... ok
test secrets::tests::template_files_are_skipped_entirely ... ok
test push::tests::command_timeout_and_overflow_are_bounded_and_do_not_expose_stderr ... ok
test provenance::tests::nonregular_or_alias_preimages_are_rejected_without_waiting_for_a_writer ... ok
test provenance::tests::receipt_validation_rejects_arbitrary_success_or_wrong_publications ... ok
test provenance::tests::locked_overlay_receipts_pin_old_blob_tip_and_first_parent_without_inventing_overlay ... ok
test ship::tests::active_cancellation_is_exact_bounded_and_drop_cancels_the_blocking_work ... ok
test ship::tests::auto_subject_shapes ... ok
test ship::tests::configured_gate_and_author_are_validated_instead_of_defaulting_invalid_types ... ok
test ship::tests::gate_prompt_demands_json_only ... ok
test ship::tests::preview_revision_binds_author_required_gate_timeout_subject_and_force ... ok
test ship::tests::secret_subject_is_rejected_and_plain_passes ... ok
test service::snapshot_tests::guarded_edit_still_refuses_stale_content ... ok
test provenance::tests::metadata_caps_and_unreadable_preimage_never_claim_complete_attribution ... ok
test provenance::tests::materialize_keeps_exact_applied_evidence_and_reports_failed_deletion_and_ledger ... ok
test store::tests::missing_publication_ack_remains_unknown_after_later_advance_or_failed_readback ... ok
test service::snapshot_tests::read_failures_report_partial_success_and_preserve_failed_overlay ... ok
test service::snapshot_tests::selected_snapshot_records_only_new_commits_and_retains_partial_evidence ... ok
test push::tests::durable_attempt_capacity_corruption_and_monotonic_observation ... ok
test provenance::tests::concurrent_same_session_receipts_form_the_actual_locked_commit_chain ... ok
test service::snapshot_tests::selection_is_exact_empty_is_empty_and_unowned_is_rejected_before_writes ... ok
test store::tests::materialize_guard ... ok
test store::tests::prepared_head_transaction_holds_the_symbolic_branch_until_decision ... ok
test store::tests::concurrent_reviewed_publications_have_one_winner_and_preserve_worktree_and_index ... ok
test tool_result::tests::inspection_baseline_diff_is_available ... ok
test store::tests::roundtrip_and_noop ... ok
test tool_result::tests::inspection_baseline_read_does_not_create_a_store ... ok
test tool_result::tests::payloads_are_encoded_once_and_text_stays_literal ... ok
test tool_result::tests::invalid_inputs_do_not_open_the_store ... ok
test store::tests::multi_path_overlay_survives_rewrite ... ok
test store::tests::unrelated_overlay_sessions_do_not_share_a_mutation_lock ... ok
test store::tests::concurrent_overlay_writes_keep_every_path ... ok
test tool_result::tests::inspection_absence_binary_bounds_and_path_failures_are_explicit ... ok
test store::tests::reviewed_publication_refuses_stale_head_without_deleting_new_unowned_files ... ok
test store::tests::ship_trailer_undo_and_no_remote ... ok
test store::tests::reviewed_publication_binds_index_overlay_branch_and_repository_identity ... ok
test provenance::tests::real_bulk_materialization_preserves_effects_after_record_cap_and_late_write_failure ... ok
test tool_result::tests::real_consumers_share_the_tool_result_contract ... ok

test result: ok. 47 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 16.11s

   Compiling ring v0.17.14
    Checking cartridge v0.1.0 (/Users/feb/dev/cartridge/cartridge.ctg)
    Checking sessions v0.1.0 (/Users/feb/dev/cartridge/sessions.ctg)
   Compiling rustls v0.23.44
    Checking rustls-webpki v0.103.15
    Checking tokio-rustls v0.26.5
    Checking hyper-rustls v0.27.9
    Checking reqwest v0.12.28
    Checking gitfs v0.1.0 (/Users/feb/dev/cartridge/gitfs.ctg)
    Finished `dev` profile [unoptimized] target(s) in 3.00s

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/fs/prds/improve-fs-change-provenance/specs/spec01.md: exit 0

Command SHA-256: 9bbd5b7c8458bfa840038369a7dca44a13dc4d889d8dab90b527f537d6b9ad04

```text
    Finished `test` profile [unoptimized] target(s) in 0.07s
     Running unittests src/lib.rs (target/tool-result-contract/debug/deps/sessions-cb520d7f363a0e47)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests src/main.rs (target/tool-result-contract/debug/deps/sessions-64f3546e64d59d81)

running 92 tests
test change_records_tests::random_publication_ids_are_valid_and_do_not_encode_payload ... ok
test change_records_tests::strict_nested_schema_and_revision_coordinates_reject_before_publication ... ok
test change_records_tests::publication_identity_deduplicates_only_same_publication_and_keeps_legacy_projection ... ok
test change_records_tests::publication_faults_keep_old_state_or_expose_uncertainty_without_replay ... ok
test change_records_tests::changed_page_revision_and_corrupt_stored_nested_logs_are_diagnosed ... ok
test channels::cursor_tests::empty_and_oversized_delivery_do_not_write_or_advance_progress ... ok
test channels::cursor_tests::malformed_duplicate_or_out_of_range_cursors_are_preserved ... ok
test channels::cursor_tests::concurrent_reads_have_one_current_receipt_and_do_not_advance_cursor ... ok
test channels::tests::catalogue_reports_unavailable_mailbox_without_fabricated_atomic_snapshot ... ok
test channels::tests::caps_names_and_conflicting_payload_do_not_mutate_store ... ok
test change_records_tests::concurrent_publications_share_session_gate_and_preserve_contiguous_sequence ... ok
test channels::cursor_tests::watches_delivery_and_ack_survive_restart_without_skipping_later_posts ... ok
test channels::tests::changed_target_is_a_conflict_and_corrupt_or_unsafe_sources_are_preserved ... ok
test channels::cursor_tests::unwatch_discards_only_requested_progress_and_rewatch_explicitly_redelivers ... ok
test channels::tests::credentials_scope_sender_and_direct_alias_follow_mailbox_authority ... ok
test channels::cursor_tests::receipts_are_actor_scoped_and_new_reads_supersede_old_deliveries ... ok
test context::tests::context_has_stable_projection_revision_and_no_store_io ... ok
test context::tests::context_rejects_selectors_and_malformed_authority_without_leaking_inputs ... ok
test channels::cursor_tests::legacy_snapshots_and_reader_capacity_keep_accepted_lines_intact ... ok
test channels::tests::simultaneous_first_posts_in_different_scopes_keep_independent_sequences ... ok
test channels::tests::unsafe_directory_and_unknown_line_fields_are_not_repaired ... ok
test mailbox_tests::actor_scope_and_private_child_lineage_reject_metadata_forgery ... ok
test channels::tests::contiguous_reads_and_catalogue_obey_exact_byte_and_row_caps ... ok
test channels::tests::named_order_dedup_and_catalogue_survive_restart ... ok
test mailbox_tests::full_legacy_mailbox_remains_readable_but_rejects_another_append ... ok
test channels::tests::named_publication_faults_preserve_or_reconcile_without_false_notifications ... ok
test mailbox_tests::legacy_parent_and_generic_fields_cannot_forge_trusted_lineage ... ok
test mailbox_tests::old_mailbox_lines_gain_stable_read_identity_without_eager_rewrite ... ok
test mailbox_tests::reserved_mailbox_buffer_mutation_and_invalid_posts_preserve_bytes ... ok
test mailbox_tests::ambiguous_post_failure_is_resolved_by_message_id_without_duplicate_append ... ok
test mapping_tests::durable_reconnect_keeps_transcript_bytes_and_rejects_metadata_authority ... ok
test mapping_tests::damaged_indices_and_targets_are_preserved_without_adoption ... ok
test mailbox_tests::receipt_ack_survives_restart_and_never_skips_later_posts_or_other_actor_cursor ... ok
test mapping_tests::scope_input_bounds_and_explicit_conversation_types_are_checked ... ok
test mailbox_tests::acknowledgement_failure_preserves_unread_or_reports_only_already_delivered_progress ... ok
test mapping_tests::every_missing_scope_component_is_connection_local ... ok
test mapping_tests::stale_revision_and_held_os_lock_never_create_sessions ... ok
test observations::tests::changing_file_during_read_is_an_unstable_best_effort_snapshot ... ok
test observations::tests::descriptor_and_provider_changes_do_not_share_verdict_freshness ... ok
test observations::tests::inconsistent_completion_or_identity_fields_cannot_create_known_success ... ok
test observations::tests::configured_path_cannot_be_overridden_and_reports_do_not_mutate_sessions ... ok
test observations::tests::report_counts_only_observed_completions_and_preserves_legacy_unknowns ... ok
test observations::tests::malformed_partial_and_rotated_evidence_is_bounded_and_explicit ... ok
test observations::tests::report_distinguishes_disabled_missing_empty_and_unavailable_sources ... ok
test observations::tests::verdicts_compare_only_same_source_and_latest_observed_revisions ... ok
test mapping_tests::symlink_target_and_index_are_refused_without_touching_destination ... ok
test recovery::tests::changed_source_at_commit_keeps_newer_snapshot_and_original_backup ... ok
test recovery::tests::recovery_reports_are_distinct_fresh_and_read_only ... ok
test context::tests::native_context_metadata_contract ... ok
test recovery::tests::stale_repair_requests_and_existing_backups_preserve_all_bytes ... ok
test retention_tests::bad_metadata_and_snapshot_bounds_fail_closed ... ok
test repair_tests::explicit_empty_legacy_repair_preserves_backup_and_refuses_conversation_data ... ok
test mailbox_tests::same_message_id_is_idempotent_and_concurrent_posts_have_distinct_positions ... ok
test retention_tests::busy_journal_lock_and_cutoff_or_batch_errors_have_no_deletion_effect ... ok
test mapping_tests::mapping_publication_failures_preserve_index_and_report_orphan ... ok
test observations::tests::source_and_response_caps_never_truncate_json_or_expose_bodies ... ok
test retention_tests::journal_backup_and_job_symlink_or_traversal_never_touch_outside_evidence ... ok
test retention_tests::protection_changes_are_cas_checked_and_leave_transcripts_unchanged ... ok
test retention_tests::partial_backup_or_malformed_journal_blocks_resume_and_preserves_all_evidence ... ok
test roster::tests::bounded_scan_never_claims_a_complete_or_global_scope_count ... ok
test roster::tests::parent_first_cycle_order_and_private_parent_suppression_are_deterministic ... ok
test mailbox_tests::bounded_delivery_and_failed_read_persistence_leave_all_messages_unacknowledged ... ok
test roster::tests::phase_projection_excludes_payloads_and_does_not_invent_duration ... ok
test roster::tests::caps_are_full_response_utf8_bytes_and_digest_binds_returned_projection ... ok
test channels::tests::serialized_storage_cap_refuses_append_without_eviction ... ok
test tests::checkpoint_failure_before_rename_changes_nothing ... ok
test tests::concurrent_expected_revision_writes_have_one_winner ... ok
test tests::corrupt_snapshot_is_preserved_and_diagnosed_without_overwrite ... ok
test tests::deletion_failure_preserves_state_and_uncertain_deletion_matches_disk ... ok
test tests::a_session_round_trips_through_its_file ... ok
test tests::cwd_changes_are_rejected_during_active_runs_and_advance_revision_otherwise ... ok
test tests::first_checkpoint_creates_one_transcript_reused_across_restart ... ok
test tests::generic_mutation_of_the_canonical_transcript_is_rejected ... ok
test tests::incomplete_session_files_are_reported_without_defaults_or_rewriting ... ok
test tests::interrupted_run_state_is_exposed_without_executing_anything ... ok
test retention_tests::preview_counts_records_and_bytes_and_retains_every_authoritative_protection ... ok
test tests::independent_sessions_do_not_wait_for_another_sessions_gate ... ok
test tests::concurrent_session_checkpoints_keep_one_revision_winner_and_unique_buffer_ids ... ok
test tests::malformed_and_oversized_records_fail_without_changing_data ... ok
test tests::malformed_buffer_ownership_is_not_loaded_or_rewritten ... ok
test tests::store_location_is_required_and_invalid_config_is_rejected ... ok
test retention_tests::resume_refuses_new_protection_and_same_id_replacement_even_with_identical_bytes ... ok
test tests::new_nested_store_is_created_and_unicode_changes_survive_restart ... ok
test tests::post_rename_failure_reports_uncertainty_and_reloads_visible_state ... ok
test tests::sessions_and_ordinary_buffers_round_trip ... ok
test tests::sub_agent_session_records_parent_and_mailbox_round_trips_restart ... ok
test tests::every_pre_rename_failure_preserves_all_mutations_and_notifications ... ok
test tests::unattached_buffers_remain_memory_only_and_survive_other_session_commits ... ok
test retention_tests::post_preview_activity_pin_reference_and_revision_changes_refuse_without_transcript_mutation ... ok
test retention_tests::every_durable_interruption_resumes_only_recorded_targets_and_preserves_backups ... ok
test channels::cursor_tests::every_cursor_publication_fault_preserves_lines_and_exposes_visible_progress ... ok
test change_records_tests::bounded_log_and_pages_refuse_stale_or_overflow_without_eviction ... ok

test result: ok. 92 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 18.09s

    Finished `dev` profile [unoptimized] target(s) in 0.08s

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/fs/prds/improve-fs-change-provenance/specs/spec01.md: exit 0

Command SHA-256: 6ac0fc117d6c03ba838dfaf2222ca63c51d618d6e06737bb83ad8af5d2b6d770

```text
    Finished `test` profile [unoptimized] target(s) in 0.06s
     Running unittests src/lib.rs (target/tool-result-contract/debug/deps/cartridge-41093d4bbf807d0f)

running 165 tests
test observation::tests::invalid_host_config_and_poisoned_cache_do_not_create_authority_or_fail_outcomes ... ok
test observation::tests::dropping_live_invocation_records_unknown_without_retry ... ok
test process::tests::an_unterminated_startup_frame_cannot_exceed_its_budget ... ok
test observation::tests::outcomes_never_treat_transport_or_cancellation_as_known_effect_completion ... ok
test observation::tests::intended_service_capture_ignores_nested_services_and_resumes_become_unknown ... ok
test sandbox::tests::an_empty_command_is_refused_before_launch ... ok
test sandbox::tests::a_net_grant_turns_the_network_on_and_an_empty_one_leaves_it_off ... ok
test sandbox::tests::a_write_grant_names_the_canonicalized_path_and_implies_the_read ... ok
test observation::tests::attribution_is_host_configuration_and_discovery_is_distinct ... ok
test sandbox::tests::an_empty_grant_builds_no_allowance_beyond_the_runtime ... ok
test sdk::tests::older_hosts_use_uncached_descriptions_without_an_unknown_wire_request ... ok
test sandbox::tests::an_exec_grant_that_resolves_builds_a_literal_and_one_that_does_not_builds_nothing ... ok
test sdk::tests::reload_registration_dispatches_boolean_values_for_prepare_and_cancel ... ok
test sandbox::tests::a_script_names_its_interpreter ... ok
test service::version_tests::descriptors_invalidate_on_switch_and_recreation ... ok
test observation::tests::actual_descriptor_shapes_are_hashed_and_invalid_oversized_descriptors_are_unknown ... ok
test sdk::tests::slow_stream_handlers_have_bounded_queues_and_receive_a_gap ... ok
test socket::tests::explicit_unsubscribe_removes_idle_pump_once ... ok
test socket::tests::idle_disconnect_unsubscribes_without_a_future_publish ... ok
test tests::bridge::bridge_manifest_rejects_paths_outside_the_cartridge ... ok
test socket::tests::writer_failure_cancels_a_pending_call_and_unsubscribes ... ok
test socket::tests::disconnect_cleans_subscriptions_while_host_owned_reconcile_waits ... ok
test tests::bridge::process_scripts_resolve_relative_to_the_cartridge ... ok
test tests::cartridges::a_changed_file_swaps_the_fiber_and_a_broken_one_keeps_it ... ok
test tests::cartridges::a_glob_injects_every_matching_key_the_other_entries_provide ... ok
test tests::bridge::bridge_status_tracks_active_generations_and_scopes_backend_calls ... ok
test tests::cartridges::config_lua_overrides_entries_and_manifest_resolves_providers ... ok
test tests::cartridges::reconcile_adds_removes_and_revises_by_id ... ok
test tests::cartridges::yields_are_boundaries_and_access_is_enforced ... ok
test tests::cartridges::yolo_overrides_cartridge_config_only_for_automatic_services ... ok
test tests::composition::failed_initial_profile_entry_recovers_with_its_current_handle ... ok
test tests::composition::replacement_has_one_contract_at_root_and_nested_depth ... ok
test tests::contracts::a_broken_integration_check_fails_closed_with_its_error ... ok
test tests::contracts::a_broken_selftest_fails_closed_and_names_the_cartridge ... ok
test tests::contracts::a_cartridge_declaring_nothing_is_never_called ... ok
test tests::contracts::a_clashed_need_stops_the_run_before_it_loads ... ok
test tests::contracts::a_failing_contract_names_the_path_the_obligation_and_the_key ... ok
test tests::contracts::a_need_that_binds_to_nothing_is_named_instead_of_run ... ok
test tests::contracts::a_nested_cartridge_is_verified_by_its_path_from_the_root ... ok
test tests::contracts::an_unknown_cartridge_is_named_rather_than_run ... ok
test tests::contracts::declared_contracts_run_after_apply_and_pass ... ok
test tests::contracts::one_cartridge_is_verified_without_a_profile ... ok
test tests::contracts::one_obligation_may_be_declared_alone ... ok
test tests::contracts::the_providers_a_need_binds_to_are_reached_but_never_graded ... ok
test process::tests::excessive_discovery_output_is_killed_and_reaped ... ok
test tests::folders::folder_manifest_names_the_component_and_reloads_its_entry ... ok
test tests::folders::malformed_manifests_fail_without_evaluating_entries ... ok
test socket::tests::a_write_half_close_still_receives_its_pending_reply ... ok
test tests::foreground::foreground_call_returns_the_service_value_and_disposes_the_profile ... ok
test tests::foreground::foreground_missing_or_failed_service_still_disposes ... ok
test tests::landscape::landscape_distinguishes_provider_states_and_refreshes_committed_generations ... ok
test tests::landscape::landscape_lists_dynamic_children_and_tracked_source_paths ... ok
test tests::ledger::a_child_provide_is_seen_by_its_parent_subtree_and_not_by_the_graph_outside ... ok
test tests::ledger::a_dangling_re_export_is_unread_on_the_ledger_read_too ... ok
test tests::ledger::a_new_cartridge_is_available_and_not_started ... ok
test tests::ledger::a_root_that_does_not_exist_is_an_empty_ledger ... ok
test tests::ledger::a_walk_answers_from_the_asker_subtree_then_steps_outward ... ok
test tests::ledger::a_walk_from_a_nested_scope_steps_outward ... ok
test tests::ledger::an_entry_is_its_path_from_the_root ... ok
test tests::ledger::an_unreadable_document_is_an_entry_with_its_reason ... ok
test tests::ledger::two_entries_of_one_scope_offering_one_key_is_a_clash ... ok
test process::tests::excessive_discovery_stderr_is_also_bounded ... ok
test tests::lifecycle::a_raising_step_fails_the_fiber_with_nothing_installed ... ok
test tests::lifecycle::a_cycle_stays_inactive ... ok
test tests::lifecycle::a_target_change_stops_the_iterator_at_the_boundary ... ok
test tests::lifecycle::a_replaced_provider_reloads_its_dependents ... ok
test tests::lifecycle::access_is_enforced_at_the_point_of_use ... ok
test tests::lifecycle::disposing_a_parent_retires_its_children ... ok
test tests::lifecycle::dependents_are_drained_before_any_provider_inverse ... ok
test tests::lifecycle::disposing_an_effect_that_never_yields_finishes ... ok
test tests::lifecycle::effects_revert_in_lifo_order ... ok
test tests::lifecycle::isolated_realms_bind_independently ... ok
test tests::lifecycle::listeners_fire_in_order_and_bail_stops ... ok
test tests::lifecycle::user_values_and_callbacks_are_dropped_outside_the_registry_lock ... ok
test tests::manifest::a_blank_grant_path_is_refused_like_a_blank_key ... ok
test tests::manifest::a_cartridge_two_levels_down_is_not_offered ... ok
test tests::manifest::a_disabled_cartridge_still_declares_what_it_asked_for ... ok
test tests::manifest::a_grandchild_key_reaches_the_top_only_through_every_level ... ok
test tests::manifest::a_missing_file_the_document_names_does_not_blank_its_declarations ... ok
test tests::manifest::a_parent_passes_an_inner_key_outward_by_naming_it ... ok
test tests::manifest::an_empty_document_requests_nothing ... ok
test tests::manifest::an_export_that_names_nothing_inside_is_refused ... ok
test tests::manifest::an_unreadable_document_asks_for_nothing_knowable_not_for_nothing ... ok
test tests::manifest::documented_commands_are_data_and_keep_the_manifest_strict ... ok
test tests::manifest::malformed_declarations_are_refused_without_evaluating_the_entry ... ok
test tests::manifest::probe_nesting_is_not_discovered ... ok
test tests::manifest::the_capability_request_is_on_the_same_document ... ok
test tests::manifest::the_document_declares_what_it_provides_and_needs ... ok
test tests::manifest::the_document_overrides_what_the_entry_declares ... ok
test tests::manifest::two_subtrees_may_provide_the_same_key ... ok
test tests::lifecycle::disposing_an_apply_that_never_yields_finishes_and_runs_prior_inverses ... ok
test tests::node::the_document_carries_the_cartridges_own_config ... ok
test tests::folders::watcher_reloads_a_folder_when_its_manifest_changes ... ok
test sdk::tests::cancelling_nested_startup_kills_and_reaps_its_child ... ok
test tests::process::closed_links_release_pending_and_reject_new_requests ... ok
test tests::process::disabled_processes_never_run_hello_apply_or_replace ... ok
test sandbox::tests::the_asynchronous_spawn_enforces_the_same_empty_grant ... ok
test tests::process::dropping_a_waiter_ignores_its_late_reply ... ok
test tests::process::invalid_registration_fails_before_changing_loaded_fibers ... ok
test sandbox::tests::the_synchronous_command_enforces_the_empty_grant ... ok
test tests::process::ordinary_lua_composition_can_load_a_process_wrapper ... ok
test tests::process::lua_wrappers_merge_injections_before_start_and_preserve_config ... ok
test tests::process::sdk_eof_and_dispose_release_waiters_before_finalizers ... ok
test tests::process::sdk_child_roundtrip_errors_metadata_and_eof ... ok
test tests::reload::a_composed_handle_reloads_its_node_again_after_the_first_swap ... ok
test tests::reload::a_nested_node_is_swapped_and_its_dependent_follows ... ok
test tests::reload::an_ask_at_a_retired_uid_is_refused_and_the_node_still_reloads ... ok
test tests::reload::an_uncomposed_node_and_an_unknown_uid_refuse_the_ask ... ok
test tests::reload::corrected_code_can_recover_a_failed_initial_generation ... ok
test tests::reload::switching_keeps_consumers_bound_and_rejects_bad_migrations ... ok
test tests::cartridges::wrapped_process_isolation_metadata_and_dependency_restart_compose ... ok
test tests::reload::two_entries_of_one_file_each_get_their_own_switch ... ok
test tests::process::a_process_provides_listens_and_is_disposed ... ok
21658
{"nodes":["db","store","tool"],"socket":"/tmp/cartridge-9db54681c6bb6bb9-feb.sock","up":"tool.run"}
test tests::resolver::a_chain_node_whose_binary_does_not_exist_refuses_the_ask ... ok
test tests::resolver::a_chain_walks_to_its_far_end_before_the_tool_it_names ... ok
test tests::cartridges::local_list_resolves_wrappers_without_starting_a_daemon_or_applying_cartridges ... ok
test tests::resolver::a_clash_is_refused_naming_every_offer ... ok
test tests::resolver::a_cycle_is_refused_not_walked ... ok
test tests::resolver::a_diamond_launches_its_shared_provider_once ... ok
test tests::resolver::a_nested_provider_answers_before_any_outer_one ... ok
test tests::resolver::a_reentry_into_an_uninstalled_node_launches_nothing ... ok
test tests::resolver::an_unbound_key_refuses_the_launch ... ok
test tests::resolver::layered_shared_dependencies_are_completed_once_in_bottom_up_order ... ok
test tests::resolver::the_launch_refuses_a_cycle_the_ledger_holds ... ok
test tests::rpc_contract::rust_sdk_and_lua_share_json_and_bidirectional_contracts ... ok
test tests::rpc_contract::rust_sdk_eof_rejects_another_inflight_call ... ok
test tests::node::a_chain_node_calls_its_dependency_and_serves_its_dependents ... ok
test tests::rpc_contract::rust_sdk_failed_apply_retains_generation_then_reload_and_dispose_work ... ok
test tests::socket::one_turn_id_crosses_the_socket_the_host_a_cartridge_and_lua ... ok
test tests::socket::a_client_round_trips_through_a_cartridge ... ok
test tests::stream::a_failing_listener_publishes_an_error_event_on_its_channel ... ok
test tests::stream::a_full_replay_and_gap_leave_the_subscription_live ... ok
test tests::socket::socket_calls_a_lua_wrapped_sdk_process_with_correlated_errors ... ok
test tests::stream::a_lua_cartridge_publishes_and_a_late_watcher_replays_the_log ... ok
test tests::stream::a_lua_cartridge_watches_a_channel_a_socket_client_publishes_to ... ok
test tests::stream::a_queue_nobody_reads_ends_at_the_next_publish ... ok
test tests::resolver::a_hosted_node_runs_its_lua_component_and_provides_its_keys ... ok
test tests::stream::a_slow_subscriber_gets_a_gap_and_closes_without_blocking_publishers ... ok
test tests::stream::a_subscriber_receives_everything_published_to_its_channel_in_order ... ok
test tests::resolver::a_chain_of_lua_cartridges_is_hosted_and_the_cascade_follows_the_dependency ... ok
test tests::stream::concurrent_publishers_leave_a_gapless_ordered_log ... ok
test tests::stream::history_is_bounded_and_an_old_cursor_receives_a_gap ... ok
test tests::stream::leaving_is_an_event_everyone_still_on_the_channel_sees ... ok
test tests::stream::publishing_without_a_listener_costs_one_append_and_keeps_the_log ... ok
test tests::stream::a_process_cartridge_publishes_and_watches_over_the_wire ... ok
test tests::stream::a_subscriber_that_crashed_and_came_back_ends_up_where_it_was ... ok
test tests::stream::a_repeat_subscribe_spawns_no_second_pump ... ok
test tests::process::disposing_a_child_before_ready_kills_it_without_waiting_for_startup_deadline ... ok
test process::tests::hung_discovery_is_killed_and_reaped ... ok
test tests::resolver::a_chain_comes_up_from_the_bottom_and_teardown_follows_the_dependency ... ok
test tests::wire::a_cartridge_hosts_a_cartridge_over_the_same_wire ... ok
test turn::tests::a_credential_or_a_prompt_body_is_omitted_and_named ... ok
test turn::tests::a_sink_that_cannot_repair_a_failed_write_stops_accepting_records ... ok
test turn::tests::oversized_records_are_valid_json_and_bounded_before_and_after_rotation ... ok
test turn::tests::redaction_reaches_objects_inside_nested_arrays ... ok
test turn::tests::the_sink_stays_bounded_by_rotating_one_generation ... ok
test tests::wire::a_child_key_the_sub_host_never_declared_stays_private ... ok
test tests::wire::a_daemon_reload_carries_down_to_the_child_that_declared_it ... ok
test tests::wire::a_child_that_declared_no_reload_still_answers_null ... ok
test tests::wire::a_nested_bridge_call_resolves_against_the_daemons_profile_grant ... ok
test tests::wire::a_child_that_never_becomes_ready_fails_the_spawn_where_it_failed ... ok
test tests::process::a_child_that_stays_alive_without_ready_times_out_and_is_reaped ... ok
test tests::folders::recorded_memory_layout_uses_the_separate_submodule ... ok
test tests::process::watches_reload_wrappers_binaries_and_new_executable_directories_once ... ok
test tests::wire::stdout_closed_live_children_obey_each_host_deadline_and_are_reaped ... ok

test result: ok. 165 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 14.24s

     Running unittests src/main.rs (target/tool-result-contract/debug/deps/cartridge-bfe1ba4daa6e9908)

running 2 tests
test stdio_tests::mcp_bridge_failure_preserves_request_ids_without_replay ... ok
test stdio_tests::mcp_bridge_keeps_notifications_silent_and_successes_intact ... ok

test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests .cartridge/tests/unit/src/tests/fixtures/chain_fixture.rs (target/tool-result-contract/debug/examples/chain_fixture-352252d61bd6755b)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests .cartridge/tests/unit/src/tests/fixtures/lua_fixture.rs (target/tool-result-contract/debug/examples/lua_fixture-e8ce3e540cfc5bdc)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests .cartridge/tests/unit/src/tests/fixtures/nested_fixture.rs (target/tool-result-contract/debug/examples/nested_fixture-edd2fe45942c6858)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests .cartridge/tests/unit/src/tests/fixtures/rpc_fixture.rs (target/tool-result-contract/debug/examples/rpc_fixture-8e172d8aaafa386c)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

bun test v1.3.14 (0d9b296a)

.cartridge/tests/integration/memo-run.test.ts:
(pass) memo recipes preserve argument boundaries and propagate failure [43.56ms]
(pass) memo runner refuses missing, repeated and unterminated executable blocks [23.77ms]
(pass) nested PRD lanes resolve their own memo owner [13.42ms]
lane-build-evidence [{"lane":"alpha","mode":"safe","temperature":"cold","ms":892.315458,"source":{"commit":"eb81d464fb98d81bd37b2c7e9d648b3bbecbf8a7","tree":"9a08268bb20ac8730ac543ea7d92cc6e8d3bf9f9","digest":"d12a11572ff645ddd6ef8218e56d6a7f0424bb428b02cf77089b7be92751f0f2"},"binary_sha256":"621c63cda4141929dcc27bacc90bf3ef4c9d9819e41b3f3222381c4bdb1e3471","expected":"alpha","observed":"alpha","correct":true,"toolchain":"rustc 1.98.0 (88d9e12ae 2026-08-18) (Homebrew)\nbinary: rustc\ncommit-hash: 88d9e12ae178fab0fb5cc050a94da85685d449ea\ncommit-date: 2026-08-18\nhost: aarch64-apple-darwin\nrelease: 1.98.0\nLLVM version: 22.1.8"},{"lane":"alpha","mode":"safe","temperature":"warm","ms":389.79895799999986,"source":{"commit":"eb81d464fb98d81bd37b2c7e9d648b3bbecbf8a7","tree":"9a08268bb20ac8730ac543ea7d92cc6e8d3bf9f9","digest":"d12a11572ff645ddd6ef8218e56d6a7f0424bb428b02cf77089b7be92751f0f2"},"binary_sha256":"621c63cda4141929dcc27bacc90bf3ef4c9d9819e41b3f3222381c4bdb1e3471","expected":"alpha","observed":"alpha","correct":true,"toolchain":"rustc 1.98.0 (88d9e12ae 2026-08-18) (Homebrew)\nbinary: rustc\ncommit-hash: 88d9e12ae178fab0fb5cc050a94da85685d449ea\ncommit-date: 2026-08-18\nhost: aarch64-apple-darwin\nrelease: 1.98.0\nLLVM version: 22.1.8"},{"lane":"bravo","mode":"safe","temperature":"cold","ms":673.2491669999999,"source":{"commit":"0e1731185d01e9efe83a0cfa7efe09da498f95a0","tree":"f6ae5de5148108d3fb163edb0b16f3b83e9b7e84","digest":"101fc091b5b3c98b8c6c6948f7c20f06809f26890f2ff7a0bd65d1caca571ba9"},"binary_sha256":"febb286887708a068c11f7fead75a49e73f7d2ee84646d9029e7e0109abf4166","expected":"bravo","observed":"bravo","correct":true,"toolchain":"rustc 1.98.0 (88d9e12ae 2026-08-18) (Homebrew)\nbinary: rustc\ncommit-hash: 88d9e12ae178fab0fb5cc050a94da85685d449ea\ncommit-date: 2026-08-18\nhost: aarch64-apple-darwin\nrelease: 1.98.0\nLLVM version: 22.1.8"},{"lane":"bravo","mode":"safe","temperature":"warm","ms":410.8004579999997,"source":{"commit":"0e1731185d01e9efe83a0cfa7efe09da498f95a0","tree":"f6ae5de5148108d3fb163edb0b16f3b83e9b7e84","digest":"101fc091b5b3c98b8c6c6948f7c20f06809f26890f2ff7a0bd65d1caca571ba9"},"binary_sha256":"febb286887708a068c11f7fead75a49e73f7d2ee84646d9029e7e0109abf4166","expected":"bravo","observed":"bravo","correct":true,"toolchain":"rustc 1.98.0 (88d9e12ae 2026-08-18) (Homebrew)\nbinary: rustc\ncommit-hash: 88d9e12ae178fab0fb5cc050a94da85685d449ea\ncommit-date: 2026-08-18\nhost: aarch64-apple-darwin\nrelease: 1.98.0\nLLVM version: 22.1.8"}]
(pass) divergent lanes execute their own cold and warm builds without inherited caches [2542.27ms]

 4 pass
 0 fail
 47 expect() calls
Ran 4 tests across 1 file. [2.63s]
    Finished `dev` profile [unoptimized] target(s) in 0.06s

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/fs/prds/improve-fs-change-provenance/specs/spec01.md: exit 0

Command SHA-256: 5c843ed05309afb21dc30874561bcb9a360d6458db77aa42441322251956e551

```text
    Finished `dev` profile [unoptimized] target(s) in 0.07s
   Compiling ring v0.17.14
   Compiling rustls-webpki v0.103.15
   Compiling rustls v0.23.44
   Compiling tokio-rustls v0.26.5
   Compiling hyper-rustls v0.27.9
   Compiling reqwest v0.12.28
   Compiling gitfs v0.1.0 (/Users/feb/dev/cartridge/gitfs.ctg)
    Finished `dev` profile [unoptimized] target(s) in 3.51s
    Finished `dev` profile [unoptimized] target(s) in 0.07s
    Finished `dev` profile [unoptimized] target(s) in 0.06s

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/fs/prds/improve-fs-change-provenance/specs/spec01.md: exit 0

Command SHA-256: cd9ff1fd0712c60d5ec57c16281716b7a58b395351aee8fb3a1196c1ef112210

```text
bun test v1.3.14 (0d9b296a)

../fs.ctg/.cartridge/tests/integration/context.test.ts:
(pass) native FS snapshots return exact full bytes and preserve legacy tool reads without touches [787.08ms]
(pass) native FS refuses typed aliases, unsafe sources and cap overflow without partial payload [15.30ms]

../fs.ctg/.cartridge/tests/integration/change-provenance.test.ts:
(pass) real Host composes FS and Sessions for exact publication records and restart without GitFS ownership [1064.72ms]
(pass) native malformed refused and timed-out recorders report partial publication without retry [2028.51ms]

../gitfs.ctg/.cartridge/tests/integration/change-provenance.test.ts:
(pass) real Host direct and overlay evidence preserves divergence, operation tags, restart and explicit ownership [844.74ms]
(pass) actual standalone profile omits Sessions and keeps GitFS mutations available with honest unavailable attribution [182.00ms]
(pass) failed grant discovery never silently disables recording and failed recorders preserve committed effects without replay [4519.26ms]

../gitfs.ctg/.cartridge/tests/integration/tool-result.test.ts:
(pass) real SDK, MCP and proxy preserve tool payloads and do not replay failed effects [4789.21ms]
(pass) real MCP inspection obeys operation policy and preserves repository state [3954.84ms]

../gitfs.ctg/.cartridge/tests/integration/reviewed-ship.test.ts:
(pass) native required gate is fail-closed for explicit subjects, body timeout and cancellation; exact success never pushes [2354.78ms]
(pass) native stale reviews preserve external commits, and concurrent commits publish once without a configured model [1061.22ms]
(pass) native force never bypasses a gate and oversized required review never silently truncates [1039.87ms]

../gitfs.ctg/.cartridge/tests/integration/recorded-push.test.ts:
(pass) native recorded push requires reviewed exact binding and never replays operation identities [1792.62ms]
(pass) native push refuses changed remote, nonancestor, ambiguous URLs and rewrite rules [1540.33ms]
(pass) lost response stays durable unknown across restart; old readback cannot permit replay, exact readback confirms [4371.43ms]
(pass) native cancellation and overflow keep bounded unknown evidence and do not leak helper stderr [2095.42ms]
(pass) owned hook refuses an advertised head changed after preview check; durable refusal survives restart [1181.15ms]
(pass) server CAS refuses advance after the validated advertisement without changing local history [1290.26ms]

../sessions.ctg/.cartridge/tests/integration/change-records.test.ts:
(pass) native distinct direct and overlay publications persist with exact read-only pages and legacy metadata [64.46ms]
(pass) native strict DTOs, duplicate conflicts, and atomic invalid batches preserve snapshot [23.15ms]
(pass) native legacy snapshots remain readable and corrupt retained evidence is diagnosed without repair [32.99ms]
(pass) native count capacity and byte-bounded pages keep all retained publication identities [915.81ms]

 22 pass
 0 fail
 1250 expect() calls
Ran 22 tests across 7 files. [36.12s]

```
