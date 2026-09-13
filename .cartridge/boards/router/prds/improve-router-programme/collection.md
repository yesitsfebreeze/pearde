---
commit: 4ad9cd35dc862ecfe0786612d39913612d93fc45
spec-digests: {"spec01.md":"3f38e5229e9b5dec89cf07f63145285be0676375dd389190cfb8f1c7d4e1e097"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/router/prds/improve-router-programme/specs/spec01.md: exit 0

Command SHA-256: fcae24083541a7d44c6348fad8837a84c6f757f652d13accff30e8539a330811

```text
{
  "source_commit": "4ad9cd35dc862ecfe0786612d39913612d93fc45",
  "records_commit": "91a1a559ab36f9da42dcead2bfda96e25122e0da",
  "footprint": [
    ".cartridge/docs/capabilities.md",
    ".cartridge/docs/cost-latency.md",
    ".cartridge/docs/decisions.md",
    ".cartridge/tests/unit/catalog/capabilities.rs",
    ".cartridge/tests/unit/proxy/capabilities.rs",
    ".cartridge/tests/unit/sync/tests.rs",
    ".cartridge/tests/unit/telemetry.rs",
    "Cargo.toml",
    "src/catalog.rs",
    "src/decision.rs",
    "src/main.rs",
    "src/proxy.rs",
    "src/requirements.rs",
    "src/sync.rs",
    "src/telemetry.rs"
  ],
  "dependencies": [
    {
      "ref": "@router/improve-router-route-explanation",
      "commit": "4ad9cd35dc862ecfe0786612d39913612d93fc45",
      "prd_sha256": "28f78dd0f0072401f68eb8417f277f1e683c96ef90aa4e55ae7c47a35f3acda8",
      "spec_sha256": "3d2578f2a869363880c15e05b90530ce52f7e4d0c7c29e8264fa2aa3d99d8571",
      "review_round": 3,
      "score": 96,
      "review_sha256": "f90f7798141409d2c6e6e08dc8eec318044425590063edcb097f7fa639031e69",
      "collection_sha256": "5be71224876c202d8f0f3cae90c9c7cd64aa44505d2a35ceb809374740599a92"
    },
    {
      "ref": "@router/improve-router-capability-routing",
      "commit": "4ad9cd35dc862ecfe0786612d39913612d93fc45",
      "prd_sha256": "e156eec7043d84a2a9917030fd6b24d2a5593a0fcbcf7763667dcffa513c49e3",
      "spec_sha256": "aeada460bce0000ca8ff3c31f07f988c9aed27208518552c18521e3322e39044",
      "review_round": 3,
      "score": 95,
      "review_sha256": "7fc1a213fdf48b41445d3e78250a1be37ce044024db51240ae68858b3148fb83",
      "collection_sha256": "0dee489cf9e408d33e657c155c09034f58a93b625b4ae7618818427b615fc610"
    },
    {
      "ref": "@router/improve-router-cost-latency",
      "commit": "4ad9cd35dc862ecfe0786612d39913612d93fc45",
      "prd_sha256": "db4bdf575b19a73be75a77de830be12c87deb95b1508ede5fbf4d732d11efc8b",
      "spec_sha256": "a0b3c29c5806e1fe5175185242774370ef52e6a210cd5689c12b237eec690b6a",
      "review_round": 3,
      "score": 96,
      "review_sha256": "912d180eb672d05256f044530dd3eec33a324cf02637ba7754eba176a8b519db",
      "collection_sha256": "8081c061f300af7a9adad259e82aa9043d919479ee80b255b694bf2751fb5b88"
    }
  ]
}
    Finished `test` profile [unoptimized] target(s) in 0.10s
     Running unittests src/lib.rs (target/tool-result-contract/debug/deps/router-6f442f342fc41340)

running 6 tests
test protocol::tests::multi_line_data_frames_join_and_empty_ones_stay_errors ... ok
test protocol::tests::chat_to_anthropic_carries_tool_calls_and_tool_results ... ok
test protocol::tests::upstream_chat_stream_reencodes_to_anthropic_sse ... ok
test protocol::tests::anthropic_upstream_events_decode_to_tools_text_and_done ... ok
test protocol::tests::anthropic_in_chat_out_and_back_through_the_encoder ... ok
test protocol::tests::responses_output_indices_become_contiguous_chat_tool_indices ... ok

test result: ok. 6 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests src/main.rs (target/tool-result-contract/debug/deps/router-eb1c99d9d562a031)

running 36 tests
test auth::tests::jwt_exp_decodes_the_expiry_claim ... ok
test catalog::capability_tests::wire_features_require_explicit_support_and_native_preservation ... ok
test auth::tests::device_begin_guides_key_providers_to_a_key ... ok
test catalog::capability_tests::semantic_revisions_ignore_object_order_and_credential_rotation ... ok
test catalog::capability_tests::oauth_payload_and_headers_do_not_enter_decision_records ... ok
test catalog::capability_tests::every_preference_obeys_known_capabilities_and_context ... ok
test catalog::capability_tests::detailed_discovery_is_bounded_and_preserves_evidence_distinctions ... ok
test proxy::capability_tests::cancelled_execution_retains_the_started_attempt_without_claiming_selection ... ok
test proxy::capability_tests::buffering_missing_usage_stream_handoff_and_attempt_bounds_remain_explicit ... ok
test auth::tests::oauth_store_round_trips_and_removes ... ok
test proxy::capability_tests::a_policy_reload_during_fallback_does_not_change_the_attributed_snapshot ... ok
test auth::tests::valid_oauth_requests_do_not_wait_for_the_store_writer ... ok
test proxy::capability_tests::fallback_costs_bind_each_attempt_and_preserve_price_history ... ok
test proxy::capability_tests::explained_execution_distinguishes_rejections_and_binds_actual_fallback ... ok
test proxy::capability_tests::cancelled_and_persisted_inflight_recovery_is_not_replayed ... ok
test proxy::capability_tests::actual_failover_skips_incompatible_routes_and_preserves_required_fields ... ok
test proxy::capability_tests::native_anthropic_features_survive_selection_and_request_encoding ... ok
test settings::tests::storage_paths_are_required_without_implicit_locations ... ok
test sync::tests::a_provider_without_live_inventory_still_contributes_its_known_models ... ok
test sync::tests::an_entry_lands_under_the_alias_then_the_shared_core_then_its_slug ... ok
test proxy::capability_tests::no_compatible_route_fails_before_network_and_health_rules_cannot_waive_fields ... ok
test sync::tests::subscription_cache_reads_are_not_fresh_remote_observations ... ok
test sync::tests::incomplete_hops_do_not_inherit_other_providers_or_refresh_expired_evidence ... ok
test sync::tests::the_fallback_index_lists_known_models_and_unknown_providers_stay_empty ... ok
test telemetry::tests::partial_and_omitted_attempts_keep_total_unknown_without_repeating_subtotal ... ok
test telemetry::tests::native_usage_partial_fields_survive_and_overflow_cost_is_unknown ... ok
test telemetry::tests::pricing_and_estimates_keep_missing_and_age_explicit ... ok
test telemetry::tests::snapshots_distinguish_unknown_zero_invalid_and_never_double_count ... ok
test proxy::capability_tests::concurrent_sweeps_coalesce_and_obsolete_probe_cannot_clear_newer_failure ... ok
test proxy::capability_tests::native_and_stream_explanations_are_optional_and_archival_bounds_are_explicit ... ok
test proxy::reload_tests::preparation_retains_existing_leases_and_defers_new_ones ... ok
test proxy::capability_tests::persistence_deadlines_and_missing_authority_fail_without_probe_dispatch ... ok
test proxy::capability_tests::recovery_budget_survives_repeated_failures_and_restart ... ok
test proxy::capability_tests::recovery_requires_complete_native_responses_with_valid_tools ... ok
test proxy::capability_tests::terminal_routes_do_not_starve_eligible_recovery_and_legacy_is_explicit ... ok
test proxy::capability_tests::recovery_bounds_a_stalled_attempt_and_rejects_empty_completion ... ok

test result: ok. 36 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 1.13s

    Finished `dev` profile [unoptimized] target(s) in 0.10s

```
