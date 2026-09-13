---
commit: 0a216cb100ea40aa0535509d44c38b16a009b9cc
spec-digests: {"spec01.md":"a0b3c29c5806e1fe5175185242774370ef52e6a210cd5689c12b237eec690b6a"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/router/prds/improve-router-cost-latency/specs/spec01.md: exit 0

Command SHA-256: acfe99e25c61c15f89fb04414c5826daf5a4a0818c0457e30e9f9aa2ac5f69af

```text
   Compiling ring v0.17.14
   Compiling rustls v0.23.44
   Compiling rustls-webpki v0.103.15
   Compiling tokio-rustls v0.26.5
   Compiling hyper-rustls v0.27.9
   Compiling reqwest v0.12.28
   Compiling router v0.1.0 (/Users/feb/dev/cartridge/router.ctg)
    Finished `test` profile [unoptimized] target(s) in 4.79s
     Running unittests src/lib.rs (target/tool-result-contract/debug/deps/router-6f442f342fc41340)

running 6 tests
test protocol::tests::chat_to_anthropic_carries_tool_calls_and_tool_results ... ok
test protocol::tests::multi_line_data_frames_join_and_empty_ones_stay_errors ... ok
test protocol::tests::upstream_chat_stream_reencodes_to_anthropic_sse ... ok
test protocol::tests::anthropic_upstream_events_decode_to_tools_text_and_done ... ok
test protocol::tests::anthropic_in_chat_out_and_back_through_the_encoder ... ok
test protocol::tests::responses_output_indices_become_contiguous_chat_tool_indices ... ok

test result: ok. 6 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests src/main.rs (target/tool-result-contract/debug/deps/router-eb1c99d9d562a031)

running 29 tests
test auth::tests::jwt_exp_decodes_the_expiry_claim ... ok
test catalog::capability_tests::semantic_revisions_ignore_object_order_and_credential_rotation ... ok
test catalog::capability_tests::wire_features_require_explicit_support_and_native_preservation ... ok
test catalog::capability_tests::every_preference_obeys_known_capabilities_and_context ... ok
test catalog::capability_tests::oauth_payload_and_headers_do_not_enter_decision_records ... ok
test auth::tests::device_begin_guides_key_providers_to_a_key ... ok
test catalog::capability_tests::detailed_discovery_is_bounded_and_preserves_evidence_distinctions ... ok
test proxy::capability_tests::cancelled_execution_retains_the_started_attempt_without_claiming_selection ... ok
test proxy::capability_tests::fallback_costs_bind_each_attempt_and_preserve_price_history ... ok
test proxy::capability_tests::a_policy_reload_during_fallback_does_not_change_the_attributed_snapshot ... ok
test proxy::capability_tests::buffering_missing_usage_stream_handoff_and_attempt_bounds_remain_explicit ... ok
test settings::tests::storage_paths_are_required_without_implicit_locations ... ok
test sync::tests::a_provider_without_live_inventory_still_contributes_its_known_models ... ok
test sync::tests::an_entry_lands_under_the_alias_then_the_shared_core_then_its_slug ... ok
test sync::tests::incomplete_hops_do_not_inherit_other_providers_or_refresh_expired_evidence ... ok
test sync::tests::subscription_cache_reads_are_not_fresh_remote_observations ... ok
test sync::tests::the_fallback_index_lists_known_models_and_unknown_providers_stay_empty ... ok
test auth::tests::valid_oauth_requests_do_not_wait_for_the_store_writer ... ok
test proxy::capability_tests::explained_execution_distinguishes_rejections_and_binds_actual_fallback ... ok
test proxy::capability_tests::native_anthropic_features_survive_selection_and_request_encoding ... ok
test telemetry::tests::native_usage_partial_fields_survive_and_overflow_cost_is_unknown ... ok
test telemetry::tests::partial_and_omitted_attempts_keep_total_unknown_without_repeating_subtotal ... ok
test telemetry::tests::pricing_and_estimates_keep_missing_and_age_explicit ... ok
test telemetry::tests::snapshots_distinguish_unknown_zero_invalid_and_never_double_count ... ok
test auth::tests::oauth_store_round_trips_and_removes ... ok
test proxy::capability_tests::no_compatible_route_fails_before_network_and_health_rules_cannot_waive_fields ... ok
test proxy::capability_tests::actual_failover_skips_incompatible_routes_and_preserves_required_fields ... ok
test proxy::capability_tests::native_and_stream_explanations_are_optional_and_archival_bounds_are_explicit ... ok
test proxy::reload_tests::preparation_retains_existing_leases_and_defers_new_ones ... ok

test result: ok. 29 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.12s

    Blocking waiting for file lock on build directory
    Checking ring v0.17.14
    Checking rustls-webpki v0.103.15
    Checking rustls v0.23.44
    Checking tokio-rustls v0.26.5
    Checking hyper-rustls v0.27.9
    Checking reqwest v0.12.28
    Checking router v0.1.0 (/Users/feb/dev/cartridge/router.ctg)
    Finished `dev` profile [unoptimized] target(s) in 3.03s

```
