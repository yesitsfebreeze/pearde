---
commit: 535915d3315ead89b92811cb70e63dd592d705b1
spec-digests: {"spec01.md":"3e140b209ed90be66369e386558ceddc52a565fd962d2d4daecf7c3d248e51a0"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memo/prds/improve-memo-stale-evidence/specs/spec01.md: exit 0

Command SHA-256: bba8a04465d6b12d0ea33bcffe7ef94741d3241228e16cf779512d7633665159

```text
   Compiling memo_cartridge v0.1.0 (/Users/feb/dev/cartridge/memo.ctg)
    Finished `test` profile [unoptimized] target(s) in 0.35s
     Running unittests src/main.rs (/Users/feb/dev/cartridge/cartridge.ctg/.cartridge/workspace/target/debug/deps/memo_cartridge-20d1131e2a690267)

running 48 tests
test record::resolver::tests::journal_paths_refuse_symlinks_and_cancelled_writes_do_not_save ... ok
test service::tests::bootstrap_is_self_describing_and_leaves_other_cartridge_state_alone ... ok
test service::tests::a_refused_write_leaves_the_memo_on_disk_untouched ... ok
test service::tests::cached_memos_track_same_length_edits_replacements_corruption_and_removal ... ok
test record::resolver::tests::tool_observations_land_in_the_journal_beyond_the_record ... ok
test service::tests::cancellation_before_commit_and_repairing_a_malformed_memo ... ok
test service::tests::full_graph_is_native_only_and_requires_the_trusted_host ... ok
test service::tests::a_work_check_that_names_no_command_is_saved_with_a_warning ... ok
test service::tests::landscape_requires_a_live_host_and_preserves_cancellation_and_input_bounds ... ok
test service::tests::cancellation_interrupts_record_lock_waiting ... ok
test record::resolver::tests::retained_window_rotates_and_corrupt_complete_records_fail ... ok
test service::tests::concurrent_record_writers_preserve_revision_conflicts ... ok
test service::tests::declares_types_dynamically_validates_before_save_and_reads_verbatim ... ok
test service::tests::kind_discovery_reads_only_the_selected_declaration_and_keeps_legacy_types ... ok
test service::tests::concurrent_record_observations_preserve_events_and_deduplicate ... ok
test service::tests::existing_dangling_link_blocks_neither_reads_nor_other_writes ... ok
test service::tests::enabled_cartridge_records_merge_read_only ... ok
test service::tests::list_pages_and_yaml_metadata_are_preserved ... ok
test service::tests::namespaced_usages_links_types_and_legacy_records_coexist ... ok
test service::tests::record_readers_share_the_snapshot_lock ... ok
test service::tests::record_coverage_releases_the_snapshot_before_running_git ... ok
test service::tests::rejects_malformed_metadata_paths_and_symlinks ... ok
test record::distill_tests::the_debt_counts_committed_memos_since_the_last_distill_commit ... ok
test service::tests::resolver::an_agent_resolves_reads_acts_and_records_the_outcome ... ok
test service::tests::resolver::a_current_routine_and_completed_work_remain_distinct_discovery_results ... ok
test service::tests::resolver::a_situation_ranks_relevant_over_ambiguous_and_says_so_when_nothing_matches ... ok
test service::tests::resolver::every_outcome_is_recorded_and_none_is_inferred_from_access ... ok
test service::tests::resolver::malformed_resource_baselines_are_refused_without_overwriting_the_record ... ok
test service::tests::resolver::observations_need_context_and_assessments_need_evidence ... ok
test service::tests::resolver::every_result_says_where_it_came_from_and_how_fresh_it_is ... ok
test service::tests::resolver::model_tool_exposes_resolve_and_preserves_host_attribution ... ok
test service::tests::resolver::pagination_rejects_stale_queries_and_bad_fields ... ok
test service::tests::resolver::resolve_is_typed_explained_live_and_read_only ... ok
test service::tests::resolver::resolved_items_carry_their_kind_status_and_authority ... ok
test service::tests::resolver::resolver_attributes_reports_deduplicates_and_recovers_partial_tail ... ok
test service::tests::resolver::resource_freshness_preserves_recorded_identity_when_source_changes_or_moves ... ok
test service::tests::resolver::staleness_is_ordered_labelled_and_called_out ... ok
test service::tests::resolver::usage_validation_scope_cycles_and_revision_conflicts_are_actionable ... ok
test service::tests::yolo_skips_provenance_without_fabricating_events ... ok
test service::tests::same_named_shipped_system_memos_remain_addressable ... ok
test service::tests::resolver::summaries_stay_small_pages_stay_bounded_and_the_cap_is_actionable ... ok
test service::tests::resolver::resource_boundaries_missing_targets_and_coverage ... ok
test service::tests::shipped_supersessions_and_scope_entries_resolve_in_their_own_record ... ok
test service::tests::tool_schema_trust_boundary_and_cancel_before_registration ... ok
test service::tests::record_contention_longer_than_two_seconds_still_completes ... ok
test service::tests::shipped_resources_digest_and_open_their_own_files ... ok
test service::tests::system_composition_is_ordered_filtered_and_live_from_nested_cwd ... ok
test service::tests::transient_record_contention_waits_for_the_current_operation ... ok

test result: ok. 48 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 3.79s


```
