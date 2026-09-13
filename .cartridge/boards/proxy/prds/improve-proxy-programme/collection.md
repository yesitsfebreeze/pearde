---
commit: 9ddcc08807a059579c21227ad9d3523d242ddf86
spec-digests: {"spec01.md":"f1b22eba1d31e9beca6a867b9521215efbac60f3bd60ea75110c63c108ada6e9"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/proxy/prds/improve-proxy-programme/specs/spec01.md: exit 0

Command SHA-256: a8451405d6289538635a30de5d4bacc967a88e913487e5fa8f224db6418f00a2

```text
{
  "source_commit": "9ddcc08807a059579c21227ad9d3523d242ddf86",
  "records_commit": "08d12d6ba4ea02db2d4c92fab0c11f7ae1c7b853",
  "footprint": [
    ".cartridge/docs/continuations.md",
    ".cartridge/docs/traces.md",
    ".cartridge/docs/usage.md",
    ".cartridge/tests/unit/tests.rs",
    "Cargo.toml",
    "cartridge.json",
    "src/context.rs",
    "src/continuation.rs",
    "src/main.rs",
    "src/service.rs",
    "src/streaming.rs",
    "src/trace.rs",
    "src/usage.rs",
    "src/wire.rs"
  ],
  "dependencies": [
    {
      "ref": "@proxy/improve-proxy-total-usage",
      "commit": "9ddcc08807a059579c21227ad9d3523d242ddf86",
      "prd_sha256": "d3e9fd43af350df3ae8c9c168b86ad8adf1a30dde5d10e80352d6380d2a05201",
      "spec_sha256": "d352e4dd49e0dc9547cf7bae2f5e9603df2145d4bc50a7fbca2032d2796b73c0",
      "review_round": 3,
      "score": 96,
      "review_sha256": "071c54fd868f3064f9de48e6f976f0b662bf382cbecc4a048fdbc5bfd71c9f08",
      "collection_sha256": "914a87aac051376f7d9f00a4b2a27e8a5b7ab73ef6d22d8de83561b44c5ea3a6"
    },
    {
      "ref": "@proxy/improve-proxy-tool-trace",
      "commit": "9ddcc08807a059579c21227ad9d3523d242ddf86",
      "prd_sha256": "3a97d54f54fb1e70deec5c4d919124a3a9bf73b6c798a9ae36d65f0594593a5d",
      "spec_sha256": "098dcdd949a8e71002438f17bbd0638922934b95cd68b8807a32c6602774ca1e",
      "review_round": 3,
      "score": 96,
      "review_sha256": "e08916174ae6b29c40e23b2d90ee4a1b167cc34e10356e3d1a25c798423b3189",
      "collection_sha256": "09646d7dc82684cde88983e405b9cb223dcf1330f04b9527966188f330d08b5a"
    },
    {
      "ref": "@proxy/improve-proxy-continuation-recovery",
      "commit": "9ddcc08807a059579c21227ad9d3523d242ddf86",
      "prd_sha256": "71790d0a58cb50c53829414d270e026996ecd6b9fdd31b90f27c124f1dc3fb8e",
      "spec_sha256": "e47b432ca4747609f5d62a90decd713ee630747f01f7d9285d0b13af1930e172",
      "review_round": 3,
      "score": 95,
      "review_sha256": "7777217bbcfba396282bf5c2197768dde105bdd1e860f9db24e4f964e57904e1",
      "collection_sha256": "918869f95ec497d67fbdb5b3e0ea5963b8906dbc0fd76b978a4493d428b9a79e"
    }
  ]
}
    Finished `test` profile [unoptimized] target(s) in 0.10s
     Running unittests src/main.rs (target/proxy-trace/debug/deps/proxy-01549d61205db87b)

running 41 tests
test tests::configured_client_keys_are_distinct_and_do_not_use_request_metadata ... ok
test tests::context_tests::inserting_evidence_never_splits_or_rewrites_caller_groups ... ok
test tests::context_tests::cancelled_preparation_and_pre_poll_streams_never_dispatch_model_or_tools ... ok
test tests::context_tests::disabled_recall_and_long_queries_preserve_wire_and_validate_profile_caps ... ok
test tests::an_ask_denial_names_the_operation_and_the_missing_channel ... ok
test tests::collision_budget_and_malformed_calls_fail_before_side_effects ... ok
test tests::continuation_expiry_retention_and_mapping_bounds_are_explicit ... ok
test tests::accounting_is_bounded_and_overflow_cannot_be_a_success ... ok
test tests::caller_tools_are_returned_and_mixed_batches_are_deferred_without_execution ... ok
test tests::cancellation_during_observation_keeps_completed_tool_evidence ... ok
test tests::context_tests::later_round_budget_omits_whole_snapshot_without_requery_or_digest_change ... ok
test tests::exhausted_step_budget_prevents_unreportable_tool_side_effects ... ok
test tests::dropping_stream_body_cancels_active_tool_and_releases_router_lease ... ok
test tests::final_sse_preserves_ids_stop_reasons_and_native_response_items ... ok
test tests::granted_dispatches_land_in_the_observation_journal_with_caller_and_turn ... ok
test tests::context_tests::context_archive_and_inspection_are_scoped_bounded_and_do_not_infer ... ok
test tests::immediately_dropped_stream_has_an_archived_report_without_dispatch ... ok
test tests::context_tests::failed_optional_context_keeps_provider_stream_error_and_terminal_metadata ... ok
test tests::malformed_and_decreasing_snapshots_keep_known_counts_but_flag_uncertainty ... ok
test tests::enabled_http_reports_success_and_error_with_lookup_id ... ok
test tests::disabled_trace_preserves_native_json_and_streams ... ok
test tests::interrupted_stream_reports_error_without_success_replay_or_tools ... ok
test tests::incomplete_streams_retain_observed_usage_and_never_claim_success ... ok
test tests::native_requests_are_injected_and_private_results_return_to_model ... ok
test tests::policy_denials_and_approval_requirements_never_execute ... ok
test tests::missing_invalid_zero_usage_and_json_errors_are_distinct ... ok
test tests::context_tests::sourced_context_is_user_data_once_per_round_in_all_json_and_sse_wires ... ok
test tests::continuation_http_principals_eviction_restart_and_full_input_recovery ... ok
test tests::trace_archive_bounds_active_records_and_does_not_resurrect_them ... ok
test tests::missing_final_route_never_reuses_an_earlier_rounds_provider ... ok
test tests::trace_outcomes_do_not_turn_errors_into_success_or_replay ... ok
test wire::tests::last_user_text_reads_every_wire_and_skips_tool_results ... ok
test tests::http_accepts_original_json_and_authenticates_before_dispatch ... ok
test tests::text_arrives_before_round_completion_and_private_tools_stay_hidden ... ok
test tests::truncated_provider_streams_keep_trace_errors_and_native_framing ... ok
test tests::tool_traces_bind_mixed_calls_and_policy_without_retaining_payloads ... ok
test tests::three_round_json_and_sse_accounting_match_without_duplicate_final_events ... ok
test tests::trace_overflow_does_not_limit_tool_execution ... ok
test tests::context_tests::optional_failures_and_tight_budgets_preserve_original_valid_requests ... ok
test tests::deadline_and_dropped_request_cancel_the_exact_active_tool ... ok
test tests::trace_http_isolation_and_partial_cancellation_use_trusted_identities ... ok

test result: ok. 41 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 1.04s

    Finished `dev` profile [unoptimized] target(s) in 0.09s

```
