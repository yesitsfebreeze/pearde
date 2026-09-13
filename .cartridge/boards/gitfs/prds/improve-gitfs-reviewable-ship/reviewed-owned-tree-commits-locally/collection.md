---
commit: b8f27c6f1c07888bfc6e5d09f45a8751e8ca7b36
spec-digests: {"spec01.md":"6b251cdfef881e035a048fd8d6fc8be2b7b15e41431ebe4813a2c7df854c5ddd"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/gitfs/prds/improve-gitfs-reviewable-ship/reviewed-owned-tree-commits-locally/specs/spec01.md: exit 0

Command SHA-256: 6f0e3d9bc757c65437d0967d807645cb3a4b6c459e87d452c298cfebfdd8e130

```text
   Compiling ring v0.17.14
   Compiling rustls v0.23.44
   Compiling rustls-webpki v0.103.15
   Compiling tokio-rustls v0.26.5
   Compiling hyper-rustls v0.27.9
   Compiling reqwest v0.12.28
   Compiling gitfs v0.1.0 (/Users/feb/dev/cartridge/gitfs.ctg)
    Finished `test` profile [unoptimized] target(s) in 3.99s
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
test service::snapshot_tests::read_failures_report_partial_success_and_preserve_failed_overlay ... ok
test store::tests::missing_publication_ack_remains_unknown_after_later_advance_or_failed_readback ... ok
test provenance::tests::materialize_keeps_exact_applied_evidence_and_reports_failed_deletion_and_ledger ... ok
test service::snapshot_tests::selected_snapshot_records_only_new_commits_and_retains_partial_evidence ... ok
test push::tests::durable_attempt_capacity_corruption_and_monotonic_observation ... ok
test provenance::tests::concurrent_same_session_receipts_form_the_actual_locked_commit_chain ... ok
test service::snapshot_tests::selection_is_exact_empty_is_empty_and_unowned_is_rejected_before_writes ... ok
test store::tests::materialize_guard ... ok
test store::tests::concurrent_reviewed_publications_have_one_winner_and_preserve_worktree_and_index ... ok
test store::tests::roundtrip_and_noop ... ok
test tool_result::tests::inspection_baseline_diff_is_available ... ok
test store::tests::multi_path_overlay_survives_rewrite ... ok
test tool_result::tests::inspection_baseline_read_does_not_create_a_store ... ok
test tool_result::tests::payloads_are_encoded_once_and_text_stays_literal ... ok
test store::tests::prepared_head_transaction_holds_the_symbolic_branch_until_decision ... ok
test store::tests::concurrent_overlay_writes_keep_every_path ... ok
test tool_result::tests::invalid_inputs_do_not_open_the_store ... ok
test store::tests::unrelated_overlay_sessions_do_not_share_a_mutation_lock ... ok
test tool_result::tests::inspection_absence_binary_bounds_and_path_failures_are_explicit ... ok
test store::tests::reviewed_publication_refuses_stale_head_without_deleting_new_unowned_files ... ok
test store::tests::ship_trailer_undo_and_no_remote ... ok
test store::tests::reviewed_publication_binds_index_overlay_branch_and_repository_identity ... ok
test provenance::tests::real_bulk_materialization_preserves_effects_after_record_cap_and_late_write_failure ... ok
test tool_result::tests::real_consumers_share_the_tool_result_contract ... ok

test result: ok. 47 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 14.38s

   Compiling ring v0.17.14
   Compiling rustls v0.23.44
    Checking rustls-webpki v0.103.15
    Checking tokio-rustls v0.26.5
    Checking hyper-rustls v0.27.9
    Checking reqwest v0.12.28
    Checking gitfs v0.1.0 (/Users/feb/dev/cartridge/gitfs.ctg)
    Finished `dev` profile [unoptimized] target(s) in 2.86s
   Compiling ring v0.17.14
   Compiling rustls-webpki v0.103.15
   Compiling rustls v0.23.44
   Compiling tokio-rustls v0.26.5
   Compiling hyper-rustls v0.27.9
   Compiling reqwest v0.12.28
   Compiling gitfs v0.1.0 (/Users/feb/dev/cartridge/gitfs.ctg)
    Finished `dev` profile [unoptimized] target(s) in 3.29s
bun test v1.3.14 (0d9b296a)

../gitfs.ctg/.cartridge/tests/integration/reviewed-ship.test.ts:
(pass) native required gate is fail-closed for explicit subjects, body timeout and cancellation; exact success never pushes [2603.33ms]
(pass) native stale reviews preserve external commits, and concurrent commits publish once without a configured model [961.78ms]
(pass) native force never bypasses a gate and oversized required review never silently truncates [943.30ms]

 3 pass
 0 fail
 185 expect() calls
Ran 3 tests across 1 file. [4.59s]

```
