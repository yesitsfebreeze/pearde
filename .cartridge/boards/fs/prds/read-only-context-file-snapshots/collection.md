---
commit: 3a79023311b1a9b30c383ec8c71cf31c20a69ee7
spec-digests: {"spec01.md":"8c625d4f701015800f452d5c98c4669027cba1fee2a91b46c211148ee8180618"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/fs/prds/read-only-context-file-snapshots/specs/spec01.md: exit 0

Command SHA-256: 01a58d6701ec70b4fa0c36d85207a8ea58481baa5dd5becab23b1251cb1f7f04

```text
    Finished `test` profile [unoptimized] target(s) in 0.14s
     Running unittests src/main.rs (target/tool-result-contract/debug/deps/fs-0ae3e717031e9602)

running 51 tests
test search::tests::empty_stages_is_an_empty_set_never_a_sweep ... ok
test context::tests::typed_record_case_aliases_and_directory_identities_are_excluded ... ok
test context::tests::strict_caps_and_unavailable_sources_never_return_partial_text ... ok
test context::tests::exact_bytes_and_source_revisions_preserve_every_newline ... ok
test search::tests::incompatible_stages_reject_before_execution ... ok
test search::tests::cursor_scope_expiry_and_cancellation_are_explicit ... ok
test search::tests::captured_pages_replay_after_tree_changes_and_new_queries_refresh ... ok
test search::tests::match_set_cannot_be_grepped_without_files_of ... ok
test context::tests::pinned_handle_refuses_observed_replacement_and_deadline_drops_response ... ok
test search::tests::missing_rg_is_actionable_not_empty ... ok
test search::tests::deadline_covers_child_wait_after_stdout_is_closed ... ok
test search::tests::deadlock_deadline_terminates_and_reaps_child ... ok
test search::tests::page_has_a_continuation_for_the_rest ... ok
test search::tests::pre_cancelled_invocation_spawns_no_process ... ok
test search::tests::real_grep_keeps_over_200_matches_and_empty_chains_do_not_sweep ... ok
test search::tests::active_search_cancellation_reaps_the_backend ... ok
test search::tests::snapshot_budget_fails_without_eviction_and_retirement_frees_it ... ok
test service::tests::cancel_during_spawn_prevents_mutation ... ok
test search::tests::fake_rg_error_exit_is_a_failure ... ok
test service::tests::cancellation_after_preparation_leaves_no_mutation_or_temp ... ok
test service::tests::competing_sessions_with_one_observed_revision_have_one_winner ... ok
test service::tests::concurrent_creators_preserve_the_winner ... ok
test service::tests::create_overwrite_and_edit_variants ... ok
test service::tests::describe_names_and_schemas_match_the_three_keys ... ok
test service::tests::commit_rechecks_symlinks_and_preserves_executable_modes ... ok
test service::tests::direct_evidence_uses_guarded_bytes_and_unique_publication_identity ... ok
test service::tests::disappearance_and_creation_at_publication_are_conflicts ... ok
test search::tests::fake_rg_receives_literal_arguments_no_shell ... ok
test service::tests::failed_preparation_preserves_bytes_and_permissions ... ok
test service::tests::failed_cleanup_after_known_publication_still_records_once ... ok
test service::tests::observation_failure_after_publication_is_explicit_partial_success ... ok
test service::tests::partial_read_establishes_freshness_only ... ok
test service::tests::pre_cancelled_call_never_mutates ... ok
test service::tests::read_byte_limit_truncates ... ok
test service::tests::newer_bytes_at_commit_survive_write_and_edit ... ok
test service::tests::path_escapes_and_forged_context_fail_before_mutation ... ok
test service::tests::read_offsets_limits_binary_and_missing ... ok
test service::tests::receipt_requires_exact_id_publication_digest_and_one_persisted_sequence ... ok
test service::tests::touch_failure_reports_partial_success_with_the_file ... ok
test service::tests::stale_version_fails_until_reread_including_same_size_with_restored_mtime ... ok
test service::tests::unread_overwrite_fails_without_changing_bytes ... ok
test service::tests::unseen_edit_fails_without_changing_bytes ... ok
test service::tests::touch_records_successful_mutations_only ... ok
test search::tests::large_real_tree_pages_every_identity_once_and_ref_keeps_the_tail ... ok
test search::tests::malformed_backend_output_fails_explicitly ... ok
test search::tests::matching_json_backend_produces_typed_items ... ok
test search::tests::output_survives_cancellation_polls ... ok
test search::tests::oversized_results_report_truncation ... ok
test search::tests::user_config_cannot_change_results ... ok
test search::tests::floods_and_oversized_items_fail_instead_of_claiming_completeness ... ok
test service::tests::recording_timeout_is_bounded_unknown_and_never_replays_file_publication ... ok

test result: ok. 51 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 2.56s

    Finished `dev` profile [unoptimized] target(s) in 0.08s
bun test v1.3.14 (0d9b296a)

../fs.ctg/.cartridge/tests/integration/context.test.ts:
(pass) native FS snapshots return exact full bytes and preserve legacy tool reads without touches [557.93ms]
(pass) native FS refuses typed aliases, unsafe sources and cap overflow without partial payload [11.44ms]

 2 pass
 0 fail
 56 expect() calls
Ran 2 tests across 1 file. [579.00ms]

```
