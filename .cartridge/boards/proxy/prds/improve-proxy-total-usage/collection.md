---
commit: 480a093f5f6e2cbfb74e3a34c222f7f89be7e6b6
spec-digests: {"spec01.md":"96812da0fe910323008b349f169b21112150ee4521bdbf1d45882989ac50536d"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/proxy/prds/improve-proxy-total-usage/specs/spec01.md: exit 0

Command SHA-256: 06cfa1f25a13abefe4f6956832d250edf795a1ceecc927059cb2308460bf5172

```text
   Compiling ring v0.17.14
   Compiling rustls v0.23.44
   Compiling rustls-webpki v0.103.15
   Compiling tokio-rustls v0.26.5
   Compiling hyper-rustls v0.27.9
   Compiling reqwest v0.12.28
   Compiling router v0.1.0 (/Users/feb/dev/cartridge/router.ctg)
   Compiling proxy v0.1.0 (/Users/feb/dev/cartridge/proxy.ctg)
    Finished `test` profile [unoptimized] target(s) in 4.18s
     Running unittests src/main.rs (target/tool-result-contract/debug/deps/proxy-441ab2128063a0ff)

running 21 tests
test tests::exhausted_step_budget_prevents_unreportable_tool_side_effects ... ok
test tests::final_sse_preserves_ids_stop_reasons_and_native_response_items ... ok
test tests::an_ask_denial_names_the_operation_and_the_missing_channel ... ok
test tests::granted_dispatches_land_in_the_observation_journal_with_caller_and_turn ... ok
test tests::collision_budget_and_malformed_calls_fail_before_side_effects ... ok
test tests::immediately_dropped_stream_has_an_archived_report_without_dispatch ... ok
test tests::accounting_is_bounded_and_overflow_cannot_be_a_success ... ok
test tests::malformed_and_decreasing_snapshots_keep_known_counts_but_flag_uncertainty ... ok
test tests::caller_tools_are_returned_and_mixed_batches_are_deferred_without_execution ... ok
test tests::policy_denials_and_approval_requirements_never_execute ... ok
test tests::native_requests_are_injected_and_private_results_return_to_model ... ok
test wire::tests::last_user_text_reads_every_wire_and_skips_tool_results ... ok
test tests::dropping_stream_body_cancels_active_tool_and_releases_router_lease ... ok
test tests::missing_invalid_zero_usage_and_json_errors_are_distinct ... ok
test tests::enabled_http_reports_success_and_error_with_lookup_id ... ok
test tests::interrupted_stream_reports_error_without_success_replay_or_tools ... ok
test tests::incomplete_streams_retain_observed_usage_and_never_claim_success ... ok
test tests::text_arrives_before_round_completion_and_private_tools_stay_hidden ... ok
test tests::http_accepts_original_json_and_authenticates_before_dispatch ... ok
test tests::three_round_json_and_sse_accounting_match_without_duplicate_final_events ... ok
test tests::deadline_and_dropped_request_cancel_the_exact_active_tool ... ok

test result: ok. 21 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 1.01s


```
