---
commit: 1ffca32db1d06364b3e35e6cbca4881a1f814f71
spec-digests: {"spec01.md":"84448715ee4592a6a48bb657563d0763ac86c23e987798fe6e095b89b7f1fa5c"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memo/prds/landscape-file-kernel-context-facade/specs/spec01.md: exit 0

Command SHA-256: bf31a9869d04a323a5e9cab6dde7b65c8597e711c75b0e3c5b0108bbe68584cc

```text
    Blocking waiting for file lock on build directory
    Finished `test` profile [unoptimized] target(s) in 2.49s
     Running unittests src/main.rs (target/tool-result-contract/debug/deps/memo_cartridge-bc0c17505d7b5b6c)

running 77 tests
test board::tests::native_inputs_are_bounded_and_model_tool_cannot_initialize_a_board ... ok
test document::projection::tests::code_and_ordinary_links_are_literal_and_never_open_their_targets ... ok
test board::tests::symlink_ancestors_symlink_files_and_oversized_files_are_distinct_conflicts ... ok
test board::tests::a_racing_creator_is_never_replaced_even_after_the_final_inspection ... ok
test board::tests::conflict_preserves_edits_and_all_unrelated_state_without_partial_install ... ok
test document::projection::tests::native_read_hydrates_only_public_sections_and_binds_a_separate_source_closure ... ok
test document::projection::tests::public_section_diagnostics_are_bound_to_the_observed_source_revision ... ok
test document::projection::tests::private_sources_and_malformed_private_metadata_never_leak_through_any_projection ... ok
test document::projection::tests::exact_qualified_relative_and_named_sections_preserve_owner_boundaries ... ok
test document::projection::tests::repeated_references_reuse_one_snapshot_even_after_bytes_and_aliases_change ... ok
test document::tests::alias_collisions_and_physical_owner_ambiguity_name_both_sources ... ok
test document::tests::frontmatter_cannot_override_ownership_and_unclosed_fences_never_claim_validation ... ok
test document::tests::metadata_only_index_is_additive_and_model_tool_cannot_choose_native_roots ... ok
test document::tests::malformed_versioned_sources_fail_in_read_and_index_instead_of_disappearing ... ok
test document::tests::nested_cwd_has_one_canonical_owner_and_normal_sibling_owners_remain_independent ... ok
test board::tests::partial_install_reports_effects_and_resumes_only_missing_files ... ok
test document::tests::unsafe_paths_symlinks_and_non_regular_sources_refuse_without_opening_them ... ok
test document::validation::tests::dependency_expressions_and_advanced_syntax_never_produce_a_descriptor ... ok
test document::validation::tests::validation_uses_the_already_parsed_bytes_after_source_is_deleted ... ok
test document::validation::tests::frozen_lf_crlf_and_multiple_blocks_select_exact_recipe_and_argument_vector ... ok
test document::tests::native_projections_share_exact_frozen_bytes_with_crlf_and_stale_guards ... ok
test board::tests::dropping_the_awaiting_request_requests_stop_without_claiming_worker_join ... ok
test document::validation::tests::metadata_fences_duplicates_and_parameter_errors_are_source_located ... ok
test board::tests::native_preview_is_read_only_and_install_matches_exact_manifest ... ok
test document::validation::tests::execution_bases_and_capacity_limits_refuse_without_partial_source_payload ... ok
test document::projection::tests::cycles_depth_source_and_visit_limits_are_explicit_and_bounded ... ok
test record::resolver::tests::journal_paths_refuse_symlinks_and_cancelled_writes_do_not_save ... ok
test record::resolver::tests::tool_observations_land_in_the_journal_beyond_the_record ... ok
test service::tests::a_refused_write_leaves_the_memo_on_disk_untouched ... ok
test service::tests::a_merged_view_shadow_preserves_owner_identity_and_refuses_conflicting_writes ... ok
test service::tests::bootstrap_is_self_describing_and_leaves_other_cartridge_state_alone ... ok
test service::tests::a_work_check_that_names_no_command_is_saved_with_a_warning ... ok
test record::resolver::tests::retained_window_rotates_and_corrupt_complete_records_fail ... ok
test service::tests::cancellation_before_commit_and_repairing_a_malformed_memo ... ok
test service::tests::cached_memos_track_same_length_edits_replacements_corruption_and_removal ... ok
test service::tests::cancellation_interrupts_record_lock_waiting ... ok
test service::tests::full_graph_is_native_only_and_requires_the_trusted_host ... ok
test service::tests::landscape_requires_a_live_host_and_preserves_cancellation_and_input_bounds ... ok
test service::tests::concurrent_record_writers_preserve_revision_conflicts ... ok
test service::tests::concurrent_record_observations_preserve_events_and_deduplicate ... ok
test service::tests::declares_types_dynamically_validates_before_save_and_reads_verbatim ... ok
test service::tests::enabled_cartridge_records_merge_read_only ... ok
test service::tests::kind_discovery_reads_only_the_selected_declaration_and_keeps_legacy_types ... ok
test service::tests::list_pages_and_yaml_metadata_are_preserved ... ok
test record::distill_tests::the_debt_counts_committed_memos_since_the_last_distill_commit ... ok
test service::tests::existing_dangling_link_blocks_neither_reads_nor_other_writes ... ok
test service::tests::record_coverage_releases_the_snapshot_before_running_git ... ok
test service::tests::record_readers_share_the_snapshot_lock ... ok
test document::projection::tests::byte_utf8_output_and_diagnostic_limits_do_not_claim_complete_expansion ... ok
test service::tests::rejects_malformed_metadata_paths_and_symlinks ... ok
test service::tests::namespaced_usages_links_types_and_legacy_records_coexist ... ok
test service::tests::resolver::a_situation_ranks_relevant_over_ambiguous_and_says_so_when_nothing_matches ... ok
test service::tests::resolver::a_current_routine_and_completed_work_remain_distinct_discovery_results ... ok
test service::tests::resolver::every_result_says_where_it_came_from_and_how_fresh_it_is ... ok
test service::tests::resolver::an_agent_resolves_reads_acts_and_records_the_outcome ... ok
test service::tests::resolver::every_outcome_is_recorded_and_none_is_inferred_from_access ... ok
test service::tests::resolver::malformed_resource_baselines_are_refused_without_overwriting_the_record ... ok
test service::tests::resolver::model_tool_exposes_resolve_and_preserves_host_attribution ... ok
test service::tests::resolver::observations_need_context_and_assessments_need_evidence ... ok
test service::tests::resolver::pagination_rejects_stale_queries_and_bad_fields ... ok
test service::tests::resolver::resolve_is_typed_explained_live_and_read_only ... ok
test service::tests::resolver::resolved_items_carry_their_kind_status_and_authority ... ok
test service::tests::resolver::resolver_attributes_reports_deduplicates_and_recovers_partial_tail ... ok
test service::tests::resolver::resource_freshness_preserves_recorded_identity_when_source_changes_or_moves ... ok
test service::tests::resolver::staleness_is_ordered_labelled_and_called_out ... ok
test service::tests::resolver::usage_validation_scope_cycles_and_revision_conflicts_are_actionable ... ok
test service::tests::resolver::summaries_stay_small_pages_stay_bounded_and_the_cap_is_actionable ... ok
test service::tests::yolo_skips_provenance_without_fabricating_events ... ok
test service::tests::same_named_shipped_system_memos_remain_addressable ... ok
test service::tests::resolver::resource_boundaries_missing_targets_and_coverage ... ok
test service::tests::shipped_supersessions_and_scope_entries_resolve_in_their_own_record ... ok
test service::tests::record_contention_longer_than_two_seconds_still_completes ... ok
test service::tests::tool_schema_trust_boundary_and_cancel_before_registration ... ok
test service::tests::shipped_resources_digest_and_open_their_own_files ... ok
test service::tests::system_composition_is_ordered_filtered_and_live_from_nested_cwd ... ok
test service::tests::transient_record_contention_waits_for_the_current_operation ... ok
test document::tests::bounded_index_reports_truncation_and_refuses_byte_metadata_depth_and_entry_overflow ... ok

test result: ok. 77 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 5.03s

    Finished `dev` profile [unoptimized] target(s) in 0.23s
bun test v1.3.14 (0d9b296a)

../memo.ctg/.cartridge/tests/integration/file-kernel-context.test.ts:
(pass) actual FS and memo compose exact files, kernel, documents and memory without file observations [1351.36ms]
(pass) optional grant, disabled flags and one deadline preserve independently usable evidence [287.04ms]
(pass) trusted config, physical typed namespace aliases and exact wrapper caps refuse safely [56.34ms]

 3 pass
 0 fail
 91 expect() calls
Ran 3 tests across 1 file. [1.72s]
bun test v1.3.14 (0d9b296a)

../memo.ctg/.cartridge/tests/integration/context.test.ts:
(pass) native shared context and exact readback retain attribution without tool calls or writes [673.90ms]
(pass) optional states and delayed discovery/read use one deadline while retaining other evidence [419.51ms]
(pass) invalid inputs and evidence size caps preserve exact references and legacy tool surface [24.99ms]

 3 pass
 0 fail
 80 expect() calls
Ran 3 tests across 1 file. [1139.00ms]
bun test v1.3.14 (0d9b296a)

../memo.ctg/.cartridge/tests/integration/inventory.test.ts:
{"paths":10000,"summary_bytes":393,"max_page_bytes":11731,"snapshot_calls":3}
(pass) native compact snapshot pages 10000 paths exactly with one discovery and no hidden writes [7485.43ms]
(pass) cache replacement follows newest-started request and failed refresh preserves published snapshot [503.35ms]
(pass) restart, invalid inputs and partial sources are explicit while legacy landscape remains accepted [206.14ms]

 3 pass
 0 fail
 10183 expect() calls
Ran 3 tests across 1 file. [8.21s]
    Finished `dev` profile [unoptimized] target(s) in 0.18s
/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memo/prds/landscape-file-kernel-context-facade/real-host-proof.py: OK
{
  "runtime_binary": "/Users/feb/dev/cartridge/cartridge.ctg/target/tool-result-contract/debug/cartridge",
  "manifest_sha256": "68502209e955e716f485eb2b774e12564915d71676dc17451142163c98ae9202",
  "manifest": {
    "name": "fs",
    "entry": "init.lua",
    "source": "https://github.com/yesitsfebreeze/fs.ctg",
    "provide": [
      "fs.context",
      "tool.read",
      "tool.write",
      "tool.edit",
      "tool.search",
      "tool.glob",
      "tool.grep"
    ],
    "needs": [
      "sessions"
    ],
    "description": "Provides file read, write, edit, search, glob, and grep tools; records touched files through sessions.",
    "commands": {
      "build": {
        "argv": [
          "just",
          "--justfile",
          "../cartridge.ctg/justfile",
          "build",
          "fs"
        ],
        "cwd": "."
      },
      "check": {
        "argv": [
          "just",
          "--justfile",
          "../cartridge.ctg/justfile",
          "check",
          "fs"
        ],
        "cwd": "."
      },
      "test": {
        "argv": [
          "just",
          "--justfile",
          "../cartridge.ctg/justfile",
          "test",
          "fs"
        ],
        "cwd": "."
      },
      "run": {
        "argv": [
          "just",
          "--justfile",
          "../cartridge.ctg/justfile",
          "process",
          "fs"
        ],
        "cwd": ".",
        "description": "Foreground SDK JSON-lines process; use hello to inspect capabilities."
      },
      "hello": {
        "argv": [
          "just",
          "--justfile",
          "../cartridge.ctg/justfile",
          "process",
          "fs",
          "hello"
        ],
        "cwd": "."
      }
    }
  },
  "cases": [
    {
      "present": true,
      "exit": 0,
      "stdout": "{\"complete\":true,\"deadline_exceeded\":false,\"limits\":{\"deadline_ms\":500,\"max_bytes\":16384,\"max_rows\":16},\"revision\":\"1efab06bb106b34cbbe7bdb08424ee6ddfe53f5540006502ce88766e19f63afa\",\"rows\":[{\"reference\":{\"id\":\"@alpha/fixture.txt\",\"kind\":\"file\",\"owner\":\"alpha\",\"revision\":\"9974f5c368e5b474e4ea7aca00768bd5bbf8c78ff347a1a4949beea58a17ac3f\",\"revision_kind\":\"source_bytes\"},\"selection_reason\":\"public file owner/path match; exact source bytes\",\"source\":\"{\\\"owner\\\":\\\"alpha\\\",\\\"path\\\":\\\"fixture.txt\\\"}\",\"text\":\"FULL\\r\\nREAL_HOST\\r\\n\"},{\"reference\":{\"id\":\"@runtime/kernel/alpha\",\"kind\":\"kernel\",\"owner\":\"runtime\",\"revision\":\"26f8caac18d77d98e85abe9205742f7a494e7284f2100dd2c57dafffe465bb20\",\"revision_kind\":\"observed_projection\"},\"selection_reason\":\"kernel owner/capability match; observed public metadata\",\"source\":\"{\\\"generation\\\":2,\\\"id\\\":\\\"alpha\\\",\\\"provide\\\":[\\\"native.fixture\\\"],\\\"state\\\":\\\"Active\\\"}\",\"text\":\"{\\\"generation\\\":2,\\\"id\\\":\\\"alpha\\\",\\\"provide\\\":[\\\"native.fixture\\\"],\\\"state\\\":\\\"Active\\\"}\"}],\"schema\":\"cartridge-context/v1\",\"sources\":[{\"contributor\":\"documents\",\"state\":\"disabled\"},{\"contributor\":\"files\",\"state\":\"available\"},{\"contributor\":\"kernel\",\"state\":\"available\"},{\"contributor\":\"memory\",\"state\":\"disabled\"}],\"truncated\":false}\n",
      "stderr": "",
      "profile": "return {{id=\"memo\",path=\"memo\",inject={\"fs.context\"}},{id=\"alpha\",path=\"alpha\"},{id=\"sessions\",path=\"sessions.lua\"},{id=\"fs\",path=\"fs\"}}"
    },
    {
      "present": false,
      "exit": 0,
      "stdout": "{\"complete\":false,\"deadline_exceeded\":false,\"limits\":{\"deadline_ms\":500,\"max_bytes\":16384,\"max_rows\":16},\"revision\":\"88998e7472c51dde3a625d0fd1eaaa6f978e289786cbabcfc5650ba22c5383f8\",\"rows\":[{\"reference\":{\"id\":\"@runtime/kernel/alpha\",\"kind\":\"kernel\",\"owner\":\"runtime\",\"revision\":\"26f8caac18d77d98e85abe9205742f7a494e7284f2100dd2c57dafffe465bb20\",\"revision_kind\":\"observed_projection\"},\"selection_reason\":\"kernel owner/capability match; observed public metadata\",\"source\":\"{\\\"generation\\\":2,\\\"id\\\":\\\"alpha\\\",\\\"provide\\\":[\\\"native.fixture\\\"],\\\"state\\\":\\\"Active\\\"}\",\"text\":\"{\\\"generation\\\":2,\\\"id\\\":\\\"alpha\\\",\\\"provide\\\":[\\\"native.fixture\\\"],\\\"state\\\":\\\"Active\\\"}\"}],\"schema\":\"cartridge-context/v1\",\"sources\":[{\"contributor\":\"documents\",\"state\":\"disabled\"},{\"contributor\":\"files\",\"state\":\"absent\"},{\"contributor\":\"kernel\",\"state\":\"available\"},{\"contributor\":\"memory\",\"state\":\"disabled\"}],\"truncated\":false}\n",
      "stderr": "",
      "profile": "return {{id=\"memo\",path=\"memo\",inject={}},{id=\"alpha\",path=\"alpha\"}}"
    }
  ],
  "assertions": "Real Host present grant loads FS/Memo and returns exact bytes + kernel; omitted FS/grant keeps Memo loaded with files absent/kernel available; source bytes and directory entries unchanged.",
  "assertion_count": 10
}

```
