---
commit: 6a8dec3cc259968a6bcd3aa1b507321268f88b7e
spec-digests: {"spec01.md":"55d24ba0854ba24963ac89b83687aedb0b737e73536d190dd8dbd0d6e99b2fea"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/fs/prds/improve-fs-revision-guards/specs/spec01.md: exit 0

Command SHA-256: 0994189753a784838b736809cf0c31770a308484a7a0616d3c880ddef6a27331

```text
    Finished `test` profile [unoptimized] target(s) in 0.09s
     Running unittests src/main.rs (target/fs-revision/debug/deps/fs-1f8a81b2f9d866bc)

running 43 tests
test search::tests::incompatible_stages_reject_before_execution ... ok
test search::tests::empty_stages_is_an_empty_set_never_a_sweep ... ok
test search::tests::cursor_scope_expiry_and_cancellation_are_explicit ... ok
test search::tests::match_set_cannot_be_grepped_without_files_of ... ok
test search::tests::captured_pages_replay_after_tree_changes_and_new_queries_refresh ... ok
test search::tests::missing_rg_is_actionable_not_empty ... ok
test search::tests::active_search_cancellation_reaps_the_backend ... ok
test search::tests::fake_rg_error_exit_is_a_failure ... ok
test search::tests::deadline_covers_child_wait_after_stdout_is_closed ... ok
test search::tests::deadlock_deadline_terminates_and_reaps_child ... ok
test search::tests::pre_cancelled_invocation_spawns_no_process ... ok
test search::tests::page_has_a_continuation_for_the_rest ... ok
test search::tests::large_real_tree_pages_every_identity_once_and_ref_keeps_the_tail ... ok
test service::tests::cancel_during_spawn_prevents_mutation ... ok
test search::tests::snapshot_budget_fails_without_eviction_and_retirement_frees_it ... ok
test service::tests::cancellation_after_preparation_leaves_no_mutation_or_temp ... ok
test service::tests::competing_sessions_with_one_observed_revision_have_one_winner ... ok
test search::tests::real_grep_keeps_over_200_matches_and_empty_chains_do_not_sweep ... ok
test service::tests::concurrent_creators_preserve_the_winner ... ok
test service::tests::describe_names_and_schemas_match_the_three_keys ... ok
test service::tests::create_overwrite_and_edit_variants ... ok
test service::tests::commit_rechecks_symlinks_and_preserves_executable_modes ... ok
test service::tests::disappearance_and_creation_at_publication_are_conflicts ... ok
test service::tests::failed_preparation_preserves_bytes_and_permissions ... ok
test service::tests::observation_failure_after_publication_is_explicit_partial_success ... ok
test service::tests::partial_read_establishes_freshness_only ... ok
test service::tests::pre_cancelled_call_never_mutates ... ok
test service::tests::path_escapes_and_forged_context_fail_before_mutation ... ok
test service::tests::newer_bytes_at_commit_survive_write_and_edit ... ok
test service::tests::read_byte_limit_truncates ... ok
test service::tests::read_offsets_limits_binary_and_missing ... ok
test service::tests::touch_failure_reports_partial_success_with_the_file ... ok
test service::tests::stale_version_fails_until_reread_including_same_size_with_restored_mtime ... ok
test service::tests::touch_records_successful_mutations_only ... ok
test service::tests::unread_overwrite_fails_without_changing_bytes ... ok
test service::tests::unseen_edit_fails_without_changing_bytes ... ok
test search::tests::fake_rg_receives_literal_arguments_no_shell ... ok
test search::tests::malformed_backend_output_fails_explicitly ... ok
test search::tests::matching_json_backend_produces_typed_items ... ok
test search::tests::output_survives_cancellation_polls ... ok
test search::tests::oversized_results_report_truncation ... ok
test search::tests::user_config_cannot_change_results ... ok
test search::tests::floods_and_oversized_items_fail_instead_of_claiming_completeness ... ok

test result: ok. 43 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 1.09s


```
