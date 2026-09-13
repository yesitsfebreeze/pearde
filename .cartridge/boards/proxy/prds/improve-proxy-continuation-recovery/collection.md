---
commit: 439594188097e770fb9993aae379ac9906e0824a
spec-digests: {"spec01.md":"be8993e5f72e4e9893ee65b85dc8c44f44684d5e1363bb027b5499bd51a24974"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/proxy/prds/improve-proxy-continuation-recovery/specs/spec01.md: exit 0

Command SHA-256: 27f4413978d40afa50fd8e3aff61268e72c1f933b5ff4963a014d6f286065af9

```text
   Compiling proxy v0.1.0 (/Users/feb/dev/cartridge/proxy.ctg)
    Finished `test` profile [unoptimized] target(s) in 2.07s
     Running unittests src/main.rs (target/proxy-continuation/debug/deps/proxy-a653fea2c16f6427)

running 33 tests
test tests::configured_client_keys_are_distinct_and_do_not_use_request_metadata ... ok
test tests::an_ask_denial_names_the_operation_and_the_missing_channel ... ok
test tests::continuation_expiry_retention_and_mapping_bounds_are_explicit ... ok
test tests::collision_budget_and_malformed_calls_fail_before_side_effects ... ok
test tests::exhausted_step_budget_prevents_unreportable_tool_side_effects ... ok
test tests::final_sse_preserves_ids_stop_reasons_and_native_response_items ... ok
test tests::caller_tools_are_returned_and_mixed_batches_are_deferred_without_execution ... ok
test tests::accounting_is_bounded_and_overflow_cannot_be_a_success ... ok
test tests::immediately_dropped_stream_has_an_archived_report_without_dispatch ... ok
test tests::granted_dispatches_land_in_the_observation_journal_with_caller_and_turn ... ok
test tests::malformed_and_decreasing_snapshots_keep_known_counts_but_flag_uncertainty ... ok
test tests::cancellation_during_observation_keeps_completed_tool_evidence ... ok
test tests::dropping_stream_body_cancels_active_tool_and_releases_router_lease ... ok
test tests::native_requests_are_injected_and_private_results_return_to_model ... ok
test tests::missing_invalid_zero_usage_and_json_errors_are_distinct ... ok
test tests::policy_denials_and_approval_requirements_never_execute ... ok
test tests::interrupted_stream_reports_error_without_success_replay_or_tools ... ok
test tests::enabled_http_reports_success_and_error_with_lookup_id ... ok
test tests::incomplete_streams_retain_observed_usage_and_never_claim_success ... ok
test tests::disabled_trace_preserves_native_json_and_streams ... ok
test tests::trace_outcomes_do_not_turn_errors_into_success_or_replay ... ok
test tests::trace_archive_bounds_active_records_and_does_not_resurrect_them ... ok
test tests::missing_final_route_never_reuses_an_earlier_rounds_provider ... ok
test wire::tests::last_user_text_reads_every_wire_and_skips_tool_results ... ok
test tests::truncated_provider_streams_keep_trace_errors_and_native_framing ... ok
test tests::text_arrives_before_round_completion_and_private_tools_stay_hidden ... ok
test tests::continuation_http_principals_eviction_restart_and_full_input_recovery ... ok
test tests::http_accepts_original_json_and_authenticates_before_dispatch ... ok
test tests::tool_traces_bind_mixed_calls_and_policy_without_retaining_payloads ... ok
test tests::three_round_json_and_sse_accounting_match_without_duplicate_final_events ... ok
test tests::trace_overflow_does_not_limit_tool_execution ... ok
test tests::deadline_and_dropped_request_cancel_the_exact_active_tool ... ok
test tests::trace_http_isolation_and_partial_cancellation_use_trusted_identities ... ok

test result: ok. 33 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 1.04s

    Checking proxy v0.1.0 (/Users/feb/dev/cartridge/proxy.ctg)
    Finished `dev` profile [unoptimized] target(s) in 0.90s

```
