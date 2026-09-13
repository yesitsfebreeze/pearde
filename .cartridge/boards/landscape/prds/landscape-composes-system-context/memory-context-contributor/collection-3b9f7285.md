---
commit: 3b9f72854c39ddd90128a48bfce2667e387c3fba
spec-digests: {"spec01.md":"bbe1370ecf091f343d24447ad028ec65dfb10422979658869ef505f47e2eaf15"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/landscape/prds/landscape-composes-system-context/memory-context-contributor/specs/spec01.md: exit 0

Command SHA-256: c495a9cf024a4a1ff6aa68bf68fde50e1a830c1d3232d7fa354917e030610863

```text
   Compiling tokio v1.53.1
   Compiling landscape v0.1.0 (/Users/feb/dev/cartridge/landscape.ctg)
    Finished `test` profile [unoptimized] target(s) in 2.14s
     Running unittests src/lib.rs (target/landscape-memory/debug/deps/landscape-1841d9637182d43e)

running 40 tests
test context::tests::duplicate_tasks_and_invalid_limits_fail_before_any_producer ... ok
test context::tests::dropping_collector_drops_pending_producers_without_spawning_work ... ok
test context::tests::late_ready_contribution_cannot_publish_after_deadline ... ok
test context::tests::hanging_first_source_does_not_starve_siblings_and_is_dropped ... ok
test context::tests::producer_capacity_omissions_remain_explicit_in_prepared_snapshot ... ok
test context::tests::availability_is_explicit_and_disabled_producers_never_poll ... ok
test context::tests::private_content_cannot_change_public_digest_or_capacity ... ok
test context::tests::canonical_order_exact_readback_and_conflicting_sources ... ok
test memory::tests::conflicting_duplicate_expiry_and_malformed_bounds_refuse_without_substitution ... ok
test memory::tests::count_bytes_source_mismatch_and_compact_truncation_are_explicit ... ok
test context::tests::exact_serialized_bounds_count_metadata_and_keep_whole_utf8_rows ... ok
test memory::tests::exact_missing_changed_prefix_and_invalid_references_never_requery ... ok
test memory::tests::memory_fact_joins_shared_context_and_exact_readback_without_requery ... ok
test memory::tests::private_only_results_have_the_same_public_snapshot_as_empty_memory ... ok
test memory::tests::private_oversized_and_unknown_metadata_cannot_enter_evidence ... ok
test memory::tests::unavailable_malformed_empty_and_inactive_memory_preserve_other_sources ... ok
test surface::tests::cartridge_nodes_carry_their_capability_keys ... ok
test surface::tests::compose_grows_the_live_surface_and_counts_observations ... ok
test surface::tests::compose_skips_malformed_surface_entries ... ok
test surface::tests::composed_memo_links_respect_cartridge_namespaces ... ok
test surface::tests::memo_nodes_carry_their_kind_and_declared_usage_phrases ... ok
test surface::tests::tool_nodes_carry_the_describe_description ... ok
test tests::edges_connect_present_nodes_and_tolerate_ones_to_come ... ok
test tests::graph_search_keeps_the_seed_ranking ... ok
test tests::journal_counts_weight_stages ... ok
test tests::observed_use_outranks_equal_match ... ok
test tests::search_returns_kinds_with_descriptions ... ok
test tests::upsert_grows_the_node_set_in_place ... ok
test memory::tests::deadline_drops_pending_read_without_starting_later_hydration ... ok
test view_tests::cursor_from_another_snapshot_is_stale ... ok
test inventory::tests::subprocess_output_deadline_and_exit_failures_are_bounded ... ok
test view_tests::tracked_files_follow_sibling_repository_links ... ok
test inventory::tests::named_failures_preserve_usable_owners_and_disable_reads ... ok
test inventory::tests::escaped_rows_force_byte_paging_without_losing_progress ... ok
test inventory::tests::nested_shared_roots_newline_names_and_frozen_refresh ... ok
test view_tests::tracked_files_join_by_scope_and_page_by_id ... ok
test inventory::tests::structural_and_response_limits_are_explicit ... ok
test inventory::tests::git_output_is_strict_and_paths_always_fit_serialized_pages ... ok
test inventory::tests::retained_byte_cap_refuses_whole_owner_before_count_cap ... ok
test inventory::tests::ten_thousand_names_fit_summary_and_exact_bounded_pages ... ok

test result: ok. 40 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 3.32s

    Checking libc v0.2.189
    Checking bytes v1.12.1
    Checking errno v0.3.14
    Checking cpufeatures v0.2.17
    Checking mio v1.2.3
    Checking getrandom v0.4.3
    Checking sha2 v0.10.9
    Checking signal-hook-registry v1.4.8
    Checking rustix v1.1.4
    Checking tokio v1.53.1
    Checking tempfile v3.27.0
    Checking landscape v0.1.0 (/Users/feb/dev/cartridge/landscape.ctg)
    Finished `dev` profile [unoptimized] target(s) in 1.68s
   Compiling landscape v0.1.0 (/Users/feb/dev/cartridge/landscape.ctg)
   Compiling cartridge v0.1.0 (/Users/feb/dev/cartridge/cartridge.ctg)
   Compiling memo_cartridge v0.1.0 (/Users/feb/dev/cartridge/memo.ctg)
    Finished `test` profile [unoptimized] target(s) in 4.13s
     Running unittests src/main.rs (target/landscape-memory/debug/deps/memo_cartridge-bc0c17505d7b5b6c)

running 77 tests
test board::tests::native_inputs_are_bounded_and_model_tool_cannot_initialize_a_board ... ok
test document::projection::tests::code_and_ordinary_links_are_literal_and_never_open_their_targets ... ok
test board::tests::conflict_preserves_edits_and_all_unrelated_state_without_partial_install ... ok
test board::tests::symlink_ancestors_symlink_files_and_oversized_files_are_distinct_conflicts ... ok
test board::tests::a_racing_creator_is_never_replaced_even_after_the_final_inspection ... ok
test document::projection::tests::private_sources_and_malformed_private_metadata_never_leak_through_any_projection ... ok
test document::projection::tests::native_read_hydrates_only_public_sections_and_binds_a_separate_source_closure ... ok
test document::projection::tests::public_section_diagnostics_are_bound_to_the_observed_source_revision ... ok
test document::projection::tests::repeated_references_reuse_one_snapshot_even_after_bytes_and_aliases_change ... ok
test document::projection::tests::exact_qualified_relative_and_named_sections_preserve_owner_boundaries ... ok
test document::tests::frontmatter_cannot_override_ownership_and_unclosed_fences_never_claim_validation ... ok
test document::tests::alias_collisions_and_physical_owner_ambiguity_name_both_sources ... ok
test document::tests::metadata_only_index_is_additive_and_model_tool_cannot_choose_native_roots ... ok
test document::tests::malformed_versioned_sources_fail_in_read_and_index_instead_of_disappearing ... ok
test document::tests::unsafe_paths_symlinks_and_non_regular_sources_refuse_without_opening_them ... ok
test document::tests::nested_cwd_has_one_canonical_owner_and_normal_sibling_owners_remain_independent ... ok
test board::tests::partial_install_reports_effects_and_resumes_only_missing_files ... ok
test board::tests::dropping_the_awaiting_request_requests_stop_without_claiming_worker_join ... ok
test document::validation::tests::frozen_lf_crlf_and_multiple_blocks_select_exact_recipe_and_argument_vector ... ok
test document::validation::tests::validation_uses_the_already_parsed_bytes_after_source_is_deleted ... ok
test document::validation::tests::dependency_expressions_and_advanced_syntax_never_produce_a_descriptor ... ok
test document::validation::tests::metadata_fences_duplicates_and_parameter_errors_are_source_located ... ok
test document::tests::native_projections_share_exact_frozen_bytes_with_crlf_and_stale_guards ... ok
test document::validation::tests::execution_bases_and_capacity_limits_refuse_without_partial_source_payload ... ok
test board::tests::native_preview_is_read_only_and_install_matches_exact_manifest ... ok
test document::projection::tests::cycles_depth_source_and_visit_limits_are_explicit_and_bounded ... ok
test record::resolver::tests::journal_paths_refuse_symlinks_and_cancelled_writes_do_not_save ... ok
test record::resolver::tests::tool_observations_land_in_the_journal_beyond_the_record ... ok
test service::tests::a_refused_write_leaves_the_memo_on_disk_untouched ... ok
test service::tests::a_merged_view_shadow_preserves_owner_identity_and_refuses_conflicting_writes ... ok
test service::tests::a_work_check_that_names_no_command_is_saved_with_a_warning ... ok
test record::resolver::tests::retained_window_rotates_and_corrupt_complete_records_fail ... ok
test service::tests::bootstrap_is_self_describing_and_leaves_other_cartridge_state_alone ... ok
test document::projection::tests::byte_utf8_output_and_diagnostic_limits_do_not_claim_complete_expansion ... ok
test service::tests::cached_memos_track_same_length_edits_replacements_corruption_and_removal ... ok
test service::tests::cancellation_interrupts_record_lock_waiting ... ok
test service::tests::full_graph_is_native_only_and_requires_the_trusted_host ... ok
test service::tests::cancellation_before_commit_and_repairing_a_malformed_memo ... ok
test service::tests::landscape_requires_a_live_host_and_preserves_cancellation_and_input_bounds ... ok
test service::tests::concurrent_record_writers_preserve_revision_conflicts ... ok
test service::tests::declares_types_dynamically_validates_before_save_and_reads_verbatim ... ok
test service::tests::concurrent_record_observations_preserve_events_and_deduplicate ... ok
test service::tests::existing_dangling_link_blocks_neither_reads_nor_other_writes ... ok
test service::tests::enabled_cartridge_records_merge_read_only ... ok
test service::tests::kind_discovery_reads_only_the_selected_declaration_and_keeps_legacy_types ... ok
test service::tests::list_pages_and_yaml_metadata_are_preserved ... ok
test record::distill_tests::the_debt_counts_committed_memos_since_the_last_distill_commit ... ok
test service::tests::record_coverage_releases_the_snapshot_before_running_git ... ok
test service::tests::record_readers_share_the_snapshot_lock ... ok
test service::tests::rejects_malformed_metadata_paths_and_symlinks ... ok
test service::tests::resolver::a_current_routine_and_completed_work_remain_distinct_discovery_results ... ok
test service::tests::namespaced_usages_links_types_and_legacy_records_coexist ... ok
test service::tests::resolver::a_situation_ranks_relevant_over_ambiguous_and_says_so_when_nothing_matches ... ok
test service::tests::resolver::an_agent_resolves_reads_acts_and_records_the_outcome ... ok
test service::tests::resolver::malformed_resource_baselines_are_refused_without_overwriting_the_record ... ok
test service::tests::resolver::every_result_says_where_it_came_from_and_how_fresh_it_is ... ok
test service::tests::resolver::every_outcome_is_recorded_and_none_is_inferred_from_access ... ok
test service::tests::resolver::model_tool_exposes_resolve_and_preserves_host_attribution ... ok
test service::tests::resolver::pagination_rejects_stale_queries_and_bad_fields ... ok
test service::tests::resolver::observations_need_context_and_assessments_need_evidence ... ok
test service::tests::resolver::resolve_is_typed_explained_live_and_read_only ... ok
test service::tests::resolver::resolved_items_carry_their_kind_status_and_authority ... ok
test service::tests::resolver::resource_freshness_preserves_recorded_identity_when_source_changes_or_moves ... ok
test service::tests::resolver::resolver_attributes_reports_deduplicates_and_recovers_partial_tail ... ok
test service::tests::resolver::staleness_is_ordered_labelled_and_called_out ... ok
test service::tests::resolver::usage_validation_scope_cycles_and_revision_conflicts_are_actionable ... ok
test service::tests::resolver::summaries_stay_small_pages_stay_bounded_and_the_cap_is_actionable ... ok
test service::tests::yolo_skips_provenance_without_fabricating_events ... ok
test service::tests::same_named_shipped_system_memos_remain_addressable ... ok
test service::tests::resolver::resource_boundaries_missing_targets_and_coverage ... ok
test service::tests::shipped_supersessions_and_scope_entries_resolve_in_their_own_record ... ok
test service::tests::tool_schema_trust_boundary_and_cancel_before_registration ... ok
test service::tests::shipped_resources_digest_and_open_their_own_files ... ok
test service::tests::system_composition_is_ordered_filtered_and_live_from_nested_cwd ... ok
test service::tests::transient_record_contention_waits_for_the_current_operation ... ok
test document::tests::bounded_index_reports_truncation_and_refuses_byte_metadata_depth_and_entry_overflow ... ok
test service::tests::record_contention_longer_than_two_seconds_still_completes ... ok

test result: ok. 77 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 4.21s


```
