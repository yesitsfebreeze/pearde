---
commit: 698a4dc9555a6b3ad8d46dcc5dd3a14463048e70
spec-digests: {"spec01.md":"94dbdf9bcba065d12476468290147d12b80f3773dcc69ee0e902429aeb7c3099"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/harness/prds/improve-harness-compaction-diff/specs/spec01.md: exit 0

Command SHA-256: d33a9e383d9caf8ed68b81e3a7af770fa6678e7bd060c85b0b9a43152d1f08fc

```text
   Compiling harness v0.1.0 (/Users/feb/dev/cartridge/harness.ctg)
    Finished `test` profile [unoptimized] target(s) in 9.89s
     Running unittests src/main.rs (/Users/feb/dev/cartridge/cartridge.ctg/target/tool-result-contract/debug/deps/harness-33774fb0e835d7ff)

running 38 tests
test prompt::tests::replaces_only_exact_known_placeholders_without_recursion ... ok
test compaction::tests::malformed_legacy_evidence_survives_regeneration_and_unknown_versions_fail ... ok
test inspection::accounting::tests::multilingual_schemas_and_tool_exchanges_keep_byte_enforcement ... ok
test inspection::accounting::tests::historical_usage_keeps_run_and_turn_identity_without_replacing_estimate ... ok
test roster::tests::final_render_is_escaped_after_template_and_accounts_whole_row_omissions ... ok
test compaction::tests::legacy_upgrade_retains_summary_and_labels_missing_evidence ... ok
test compaction::tests::prefix_and_original_tail_are_verified_independently ... ok
test roster::tests::host_binding_rejects_bad_caps_and_never_accepts_request_credentials ... ok
test tests::anchor_names_session_foreground_and_files_without_the_user_naming_them ... ok
test roster::tests::source_adapter_checks_identity_digest_revisions_bounds_and_private_inbox_fields ... ok
test tests::context_and_compaction_use_the_supplied_memo_template ... ok
test tests::canonical_deduplication_keeps_each_source_once ... ok
test tests::descriptors_become_function_tools_and_bad_ones_fail ... ok
test tests::ancestor_tree_orders_instructions_and_leaves_legacy_memos_alone ... ok
test tests::malformed_configuration_is_rejected ... ok
test tests::journal_projects_ordered_messages_without_lifecycle_records ... ok
test tests::malformed_records_and_unresolved_groups_are_refused ... ok
test tests::markdown_system_resolves_session_values_and_optional_context_once ... ok
test tests::native_date_covers_the_utc_day_boundary_and_stays_fresh ... ok
test tests::framing_delimiters_are_escaped_and_multibyte_stays_valid ... ok
test tests::prefix_hash_is_stable_and_distinguishes_prefixes ... ok
test tests::tail_start_keeps_complete_turns_and_never_splits_tool_groups ... ok
test inspection::tests::compaction_can_shrink_retained_turns_without_cutting_current_input ... ok
test tests::telemetry_renders_from_the_journal_and_the_block_is_posted_to_build_system ... ok
test tests::terminal_renders_recent_commands_or_nothing ... ok
test tests::compacted_projection_fits_budget ... ok
test tests::missing_optional_files_are_skipped_and_bad_files_error ... ok
test working::tests::multi_call_groups_are_indivisible_and_open_groups_are_rejected ... ok
test working::tests::message_and_byte_limits_trigger_with_provider_headroom ... ok
test tests::oversized_context_returns_context_over_budget_without_changing_transcript ... ok
test tests::compacted_projection_inserts_summary_and_keeps_tail ... ok
test tests::total_instruction_budget_is_enforced ... ok
test working::tests::compacts_inside_a_tool_loop_and_pins_current_request ... ok
test tests::environment_renders_as_one_block_or_empty ... ok
test working::tests::saved_memory_is_validated_and_refreshes_after_new_messages ... ok
test inspection::tests::oversized_result_no_longer_blocks_the_next_model_turn ... ok
test inspection::tests::long_open_tool_exchange_keeps_all_ids_and_fits_budget ... ok
test working::tests::old_history_is_folded_in_small_complete_batches ... ok

test result: ok. 38 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.82s

     Running .cartridge/tests/integration/process.rs (/Users/feb/dev/cartridge/cartridge.ctg/target/tool-result-contract/debug/deps/process-fc01e1672f04c261)

running 4 tests
test harness_process_fails_on_router_timeout_without_history_loss ... ok
test harness_process_compacts_oversized_context_over_the_real_rpc_path ... ok
test harness_process_fails_safely_on_huge_turns_and_router_failures ... ok
test harness_process_projects_context_over_the_real_rpc_path ... ok

test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.89s

     Running .cartridge/tests/integration/ring.rs (/Users/feb/dev/cartridge/cartridge.ctg/target/tool-result-contract/debug/deps/ring-221a52d7ffd7eb6e)

running 1 test
test the_ring_distills_old_turns_into_memory_and_keeps_the_rest ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.10s

     Running .cartridge/tests/integration/working.rs (/Users/feb/dev/cartridge/cartridge.ctg/target/tool-result-contract/debug/deps/working-ac2d94e89b44326f)

running 1 test
test rolling_memory_refreshes_below_budget_and_survives_reload_and_failure ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 5.84s


```
