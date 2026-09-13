---
commit: 9ddcc08807a059579c21227ad9d3523d242ddf86
spec-digests: {"spec01.md":"7b347989088f57af48a44b8105bb743a7fb9bf82a0f67cb74e6b525db6943d7a"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/proxy/prds/proxy-turns-carry-recall-and-reflex-tools/specs/spec01.md: exit 0

Command SHA-256: 86fc1a674edb73dfab2ec511689110da73fc452d5ff8423da5a12b919f06653e

```text
   Compiling cartridge v0.1.0 (/Users/feb/dev/cartridge/cartridge.ctg)
   Compiling router v0.1.0 (/Users/feb/dev/cartridge/router.ctg)
   Compiling proxy v0.1.0 (/Users/feb/dev/cartridge/proxy.ctg)
    Finished `test` profile [unoptimized] target(s) in 4.26s
     Running unittests src/main.rs (target/proxy-context/debug/deps/proxy-01549d61205db87b)

running 41 tests
test tests::configured_client_keys_are_distinct_and_do_not_use_request_metadata ... ok
test tests::context_tests::inserting_evidence_never_splits_or_rewrites_caller_groups ... ok
test tests::context_tests::disabled_recall_and_long_queries_preserve_wire_and_validate_profile_caps ... ok
test tests::context_tests::cancelled_preparation_and_pre_poll_streams_never_dispatch_model_or_tools ... ok
test tests::collision_budget_and_malformed_calls_fail_before_side_effects ... ok
test tests::an_ask_denial_names_the_operation_and_the_missing_channel ... ok
test tests::continuation_expiry_retention_and_mapping_bounds_are_explicit ... ok
test tests::accounting_is_bounded_and_overflow_cannot_be_a_success ... ok
test tests::caller_tools_are_returned_and_mixed_batches_are_deferred_without_execution ... ok
test tests::cancellation_during_observation_keeps_completed_tool_evidence ... ok
test tests::context_tests::later_round_budget_omits_whole_snapshot_without_requery_or_digest_change ... ok
test tests::exhausted_step_budget_prevents_unreportable_tool_side_effects ... ok
test tests::dropping_stream_body_cancels_active_tool_and_releases_router_lease ... ok
test tests::final_sse_preserves_ids_stop_reasons_and_native_response_items ... ok
test tests::context_tests::context_archive_and_inspection_are_scoped_bounded_and_do_not_infer ... ok
test tests::granted_dispatches_land_in_the_observation_journal_with_caller_and_turn ... ok
test tests::immediately_dropped_stream_has_an_archived_report_without_dispatch ... ok
test tests::context_tests::failed_optional_context_keeps_provider_stream_error_and_terminal_metadata ... ok
test tests::malformed_and_decreasing_snapshots_keep_known_counts_but_flag_uncertainty ... ok
test tests::enabled_http_reports_success_and_error_with_lookup_id ... ok
test tests::disabled_trace_preserves_native_json_and_streams ... ok
test tests::interrupted_stream_reports_error_without_success_replay_or_tools ... ok
test tests::incomplete_streams_retain_observed_usage_and_never_claim_success ... ok
test tests::policy_denials_and_approval_requirements_never_execute ... ok
test tests::native_requests_are_injected_and_private_results_return_to_model ... ok
test tests::missing_invalid_zero_usage_and_json_errors_are_distinct ... ok
test tests::context_tests::sourced_context_is_user_data_once_per_round_in_all_json_and_sse_wires ... ok
test tests::continuation_http_principals_eviction_restart_and_full_input_recovery ... ok
test tests::trace_outcomes_do_not_turn_errors_into_success_or_replay ... ok
test tests::trace_archive_bounds_active_records_and_does_not_resurrect_them ... ok
test tests::missing_final_route_never_reuses_an_earlier_rounds_provider ... ok
test wire::tests::last_user_text_reads_every_wire_and_skips_tool_results ... ok
test tests::http_accepts_original_json_and_authenticates_before_dispatch ... ok
test tests::truncated_provider_streams_keep_trace_errors_and_native_framing ... ok
test tests::text_arrives_before_round_completion_and_private_tools_stay_hidden ... ok
test tests::tool_traces_bind_mixed_calls_and_policy_without_retaining_payloads ... ok
test tests::three_round_json_and_sse_accounting_match_without_duplicate_final_events ... ok
test tests::trace_overflow_does_not_limit_tool_execution ... ok
test tests::context_tests::optional_failures_and_tight_budgets_preserve_original_valid_requests ... ok
test tests::deadline_and_dropped_request_cancel_the_exact_active_tool ... ok
test tests::trace_http_isolation_and_partial_cancellation_use_trusted_identities ... ok

test result: ok. 41 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 1.05s

    Checking cartridge v0.1.0 (/Users/feb/dev/cartridge/cartridge.ctg)
    Checking router v0.1.0 (/Users/feb/dev/cartridge/router.ctg)
    Checking proxy v0.1.0 (/Users/feb/dev/cartridge/proxy.ctg)
    Finished `dev` profile [unoptimized] target(s) in 2.04s
   Compiling proxy v0.1.0 (/Users/feb/dev/cartridge/proxy.ctg)
    Finished `dev` profile [unoptimized] target(s) in 1.32s
   Compiling cartridge v0.1.0 (/Users/feb/dev/cartridge/cartridge.ctg)
   Compiling memo_cartridge v0.1.0 (/Users/feb/dev/cartridge/memo.ctg)
    Finished `dev` profile [unoptimized] target(s) in 5.90s
bun test v1.3.14 (0d9b296a)

.cartridge/tests/integration/recall.test.ts:
{"fixture":"memory_present","sourceId":"9c0e8179c18f55fca23dbd9c999e7ac1715c0c3241a0868af8b5fa46c512937f","binaries":{"CARTRIDGE_WRAPPER":{"path":"/Users/feb/dev/cartridge/cartridge.ctg/target/debug/cartridge","sha256":"e0a2e43d5c0adf83309ad1a80957947d3dab90963f6ee01b305ba91d931d0f28"},"MEMORY_BINARY":{"path":"/Users/feb/dev/cartridge/cartridge.ctg/target/debug/memory_cartridge","sha256":"d595a4db61c2f71cf2a6413b3f4d2e244f2f7d0da90122d1329829bb568b94b8"},"MEMO_BINARY":{"path":"/Users/feb/dev/cartridge/cartridge.ctg/target/proxy-context/debug/memo_cartridge","sha256":"1178e0326e74d426cb837d661c731f1332a1f162cdb8d3d635a634013b1b993f"},"PROXY_BINARY":{"path":"/Users/feb/dev/cartridge/cartridge.ctg/target/proxy-context/debug/proxy","sha256":"bdd2b695ef4ba6e565f44b9369e46a6c5c82e13eae77990558960bc4564a0652"}}}
(pass) real proxy and memo inject bounded memory as user data [1099.42ms]
{"fixture":"memory_absent","binaries":{"CARTRIDGE_WRAPPER":{"path":"/Users/feb/dev/cartridge/cartridge.ctg/target/debug/cartridge","sha256":"e0a2e43d5c0adf83309ad1a80957947d3dab90963f6ee01b305ba91d931d0f28"},"MEMORY_BINARY":{"path":"/Users/feb/dev/cartridge/cartridge.ctg/target/debug/memory_cartridge","sha256":"d595a4db61c2f71cf2a6413b3f4d2e244f2f7d0da90122d1329829bb568b94b8"},"MEMO_BINARY":{"path":"/Users/feb/dev/cartridge/cartridge.ctg/target/proxy-context/debug/memo_cartridge","sha256":"1178e0326e74d426cb837d661c731f1332a1f162cdb8d3d635a634013b1b993f"},"PROXY_BINARY":{"path":"/Users/feb/dev/cartridge/cartridge.ctg/target/proxy-context/debug/proxy","sha256":"bdd2b695ef4ba6e565f44b9369e46a6c5c82e13eae77990558960bc4564a0652"}}}
(pass) valid composition without Memory starts and forwards the original request [81.70ms]

 2 pass
 0 fail
 19 expect() calls
Ran 2 tests across 1 file. [1196.00ms]

```
