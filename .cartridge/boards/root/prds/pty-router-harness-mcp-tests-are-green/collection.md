---
commit: 2b038c2d240efb01002324dd686ff2f715523ba8
spec-digests: {"spec01.md":"337ba765fbb71a4704287d426430f4cf4a96e4f5aa7a8d7ef3af9558e1c96233"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/pty-router-harness-mcp-tests-are-green/specs/spec01.md: exit 0

Command SHA-256: dbcec9d64fc7da1bad635f6b78fcc991d1dabbe3553d1c81fdf2474d5e665ff9

```text
toolchain: cargo cargo-nextest bun tmux
    Finished `test` profile [unoptimized] target(s) in 0.03s
     Running unittests src/lib.rs (pty.ctg/target/debug/deps/pty-4d0ca58df4d867b2)

running 24 tests
test grid::tests::resize_rewraps_and_keeps_cursor_line ... ok
test grid::tests::alternate_screen_leaves_primary_and_scrollback ... ok
test grid::tests::cursor_queries_return_terminal_replies_without_a_ui ... ok
test identity::tests::configured_and_observed_identity_remain_distinct ... ok
test input::tests::enter_uses_lf_under_line_feed_newline_mode ... ok
test grid::tests::frame_reports_damage_since_version ... ok
test grid::tests::rows_survive_a_full_scrollback ... ok
test input::tests::focus_is_reported_only_under_focus_mode ... ok
test input::tests::kitty_event_types_append_the_action ... ok
test input::tests::modified_arrow_uses_the_parameter_form ... ok
test grid::tests::scroll_saturates_at_the_grid ... ok
test grid::tests::rows_survive_scrolling ... ok
test input::tests::paste_is_wrapped_only_when_bracketed ... ok
test input::tests::sgr_mouse_reports_cells_after_enabling_and_nothing_before ... ok
test input::tests::up_arrow_respects_application_cursor_keys ... ok
test marks::tests::plain_strips_csi_osc_and_carriage_returns ... ok
test marks::tests::marks_delimit_commands_output_exit_and_cwd ... ok
test identity::tests::restarted_shell_hooks_survive_prior_shell_cleanup ... ok
test tool::tests::whole_reads_of_long_files_are_refused_and_narrowed_reads_pass ... ok
test identity::tests::invalid_or_oversized_metadata_cannot_expand_identity ... ok
test context::tests::held_locks_fail_without_waiting_or_locking_unrelated_state ... ok
test context::tests::projection_excludes_payload_preserves_damage_and_tracks_only_metadata ... ok
test context::tests::strict_request_and_entropy_failure_are_local ... ok
test marks::tests::running_command_exposes_partial_output_and_bounded_tail ... ok

test result: ok. 24 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.07s

     Running .cartridge/tests/integration/process.rs (pty.ctg/target/debug/deps/process-b711a4271fdca4d5)

running 11 tests
test bash_reports_marks_through_the_rcfile_shim ... ok
test nu_reports_marks_through_the_spawn_hook ... ok
test shell_serializes_input_and_only_cancels_the_matching_invocation ... ok
test resize_moves_the_emulator_and_the_shell_together ... ok
test handoff_blocks_agent_input_and_takeback_interrupts_without_closing_shell ... ok
test identity_and_shell_survive_ui_clients_coming_and_going ... ok
test zsh_reports_marks_through_the_zdotdir_shim ... ok
test terminal_tool_runs_in_the_users_shell_and_commands_report_it ... ok
test context_metadata_is_bounded_readonly_and_tracks_restart ... ok
test shell_controls_nvim_and_reads_the_visible_screen ... ok
test identity_is_explicit_for_real_shells_and_unknown_fallback ... ok

test result: ok. 11 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 4.29s

test      pty        pass

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/pty-router-harness-mcp-tests-are-green/specs/spec01.md: exit 0

Command SHA-256: dbcec9d64fc7da1bad635f6b78fcc991d1dabbe3553d1c81fdf2474d5e665ff9

```text
toolchain: cargo cargo-nextest bun tmux
    Finished `test` profile [unoptimized] target(s) in 0.03s
     Running unittests src/lib.rs (pty.ctg/target/debug/deps/pty-4d0ca58df4d867b2)

running 24 tests
test grid::tests::resize_rewraps_and_keeps_cursor_line ... ok
test grid::tests::cursor_queries_return_terminal_replies_without_a_ui ... ok
test grid::tests::alternate_screen_leaves_primary_and_scrollback ... ok
test identity::tests::configured_and_observed_identity_remain_distinct ... ok
test grid::tests::frame_reports_damage_since_version ... ok
test grid::tests::rows_survive_a_full_scrollback ... ok
test input::tests::enter_uses_lf_under_line_feed_newline_mode ... ok
test input::tests::focus_is_reported_only_under_focus_mode ... ok
test input::tests::kitty_event_types_append_the_action ... ok
test input::tests::modified_arrow_uses_the_parameter_form ... ok
test input::tests::paste_is_wrapped_only_when_bracketed ... ok
test input::tests::sgr_mouse_reports_cells_after_enabling_and_nothing_before ... ok
test input::tests::up_arrow_respects_application_cursor_keys ... ok
test marks::tests::plain_strips_csi_osc_and_carriage_returns ... ok
test marks::tests::marks_delimit_commands_output_exit_and_cwd ... ok
test identity::tests::restarted_shell_hooks_survive_prior_shell_cleanup ... ok
test grid::tests::scroll_saturates_at_the_grid ... ok
test grid::tests::rows_survive_scrolling ... ok
test tool::tests::whole_reads_of_long_files_are_refused_and_narrowed_reads_pass ... ok
test identity::tests::invalid_or_oversized_metadata_cannot_expand_identity ... ok
test context::tests::strict_request_and_entropy_failure_are_local ... ok
test context::tests::projection_excludes_payload_preserves_damage_and_tracks_only_metadata ... ok
test context::tests::held_locks_fail_without_waiting_or_locking_unrelated_state ... ok
test marks::tests::running_command_exposes_partial_output_and_bounded_tail ... ok

test result: ok. 24 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.07s

     Running .cartridge/tests/integration/process.rs (pty.ctg/target/debug/deps/process-b711a4271fdca4d5)

running 11 tests
test resize_moves_the_emulator_and_the_shell_together ... ok
test shell_serializes_input_and_only_cancels_the_matching_invocation ... ok
test identity_and_shell_survive_ui_clients_coming_and_going ... ok
test nu_reports_marks_through_the_spawn_hook ... ok
test bash_reports_marks_through_the_rcfile_shim ... ok
test handoff_blocks_agent_input_and_takeback_interrupts_without_closing_shell ... ok
test zsh_reports_marks_through_the_zdotdir_shim ... ok
test terminal_tool_runs_in_the_users_shell_and_commands_report_it ... ok
test shell_controls_nvim_and_reads_the_visible_screen ... ok
test context_metadata_is_bounded_readonly_and_tracks_restart ... ok
test identity_is_explicit_for_real_shells_and_unknown_fallback ... ok

test result: ok. 11 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 3.96s

test      pty        pass

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/pty-router-harness-mcp-tests-are-green/specs/spec01.md: exit 0

Command SHA-256: dbcec9d64fc7da1bad635f6b78fcc991d1dabbe3553d1c81fdf2474d5e665ff9

```text
toolchain: cargo cargo-nextest bun tmux
    Finished `test` profile [unoptimized] target(s) in 0.03s
     Running unittests src/lib.rs (pty.ctg/target/debug/deps/pty-4d0ca58df4d867b2)

running 24 tests
test grid::tests::resize_rewraps_and_keeps_cursor_line ... ok
test grid::tests::cursor_queries_return_terminal_replies_without_a_ui ... ok
test grid::tests::alternate_screen_leaves_primary_and_scrollback ... ok
test identity::tests::configured_and_observed_identity_remain_distinct ... ok
test input::tests::enter_uses_lf_under_line_feed_newline_mode ... ok
test grid::tests::rows_survive_a_full_scrollback ... ok
test input::tests::focus_is_reported_only_under_focus_mode ... ok
test input::tests::kitty_event_types_append_the_action ... ok
test grid::tests::scroll_saturates_at_the_grid ... ok
test input::tests::modified_arrow_uses_the_parameter_form ... ok
test grid::tests::frame_reports_damage_since_version ... ok
test input::tests::paste_is_wrapped_only_when_bracketed ... ok
test input::tests::sgr_mouse_reports_cells_after_enabling_and_nothing_before ... ok
test input::tests::up_arrow_respects_application_cursor_keys ... ok
test marks::tests::plain_strips_csi_osc_and_carriage_returns ... ok
test marks::tests::marks_delimit_commands_output_exit_and_cwd ... ok
test grid::tests::rows_survive_scrolling ... ok
test tool::tests::whole_reads_of_long_files_are_refused_and_narrowed_reads_pass ... ok
test identity::tests::restarted_shell_hooks_survive_prior_shell_cleanup ... ok
test identity::tests::invalid_or_oversized_metadata_cannot_expand_identity ... ok
test context::tests::projection_excludes_payload_preserves_damage_and_tracks_only_metadata ... ok
test context::tests::held_locks_fail_without_waiting_or_locking_unrelated_state ... ok
test context::tests::strict_request_and_entropy_failure_are_local ... ok
test marks::tests::running_command_exposes_partial_output_and_bounded_tail ... ok

test result: ok. 24 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.07s

     Running .cartridge/tests/integration/process.rs (pty.ctg/target/debug/deps/process-b711a4271fdca4d5)

running 11 tests
test resize_moves_the_emulator_and_the_shell_together ... ok
test handoff_blocks_agent_input_and_takeback_interrupts_without_closing_shell ... ok
test nu_reports_marks_through_the_spawn_hook ... ok
test bash_reports_marks_through_the_rcfile_shim ... ok
test shell_serializes_input_and_only_cancels_the_matching_invocation ... ok
test identity_and_shell_survive_ui_clients_coming_and_going ... ok
test zsh_reports_marks_through_the_zdotdir_shim ... ok
test shell_controls_nvim_and_reads_the_visible_screen ... ok
test terminal_tool_runs_in_the_users_shell_and_commands_report_it ... ok
test context_metadata_is_bounded_readonly_and_tracks_restart ... ok
test identity_is_explicit_for_real_shells_and_unknown_fallback ... ok

test result: ok. 11 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 4.20s

test      pty        pass

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/pty-router-harness-mcp-tests-are-green/specs/spec01.md: exit 0

Command SHA-256: 8375a32240a8aebdc243be87bc7a5dc3cb9d05d8316b0a5bae2a5f70fc0f82ac

```text
toolchain: cargo cargo-nextest bun tmux
    Finished `test` profile [unoptimized] target(s) in 0.05s
     Running unittests src/lib.rs (router.ctg/target/debug/deps/router-dc069610eb152864)

running 50 tests
test auth::tests::jwt_exp_decodes_the_expiry_claim ... ok
test frontier::tests::a_board_name_meets_the_id_a_provider_serves ... ok
test catalog::capability_tests::wire_features_require_explicit_support_and_native_preservation ... ok
test auth::tests::device_begin_guides_key_providers_to_a_key ... ok
test frontier::tests::distinct_models_stay_distinct ... ok
test catalog::capability_tests::translated_client_fields_admit_a_foreign_wire_and_leave_the_request ... ok
test frontier::tests::the_best_matching_row_wins_and_borrowed_tasks_read_their_source ... ok
test protocol::tests::chat_to_anthropic_carries_tool_calls_and_tool_results ... ok
test protocol::tests::anthropic_in_chat_out_and_back_through_the_encoder ... ok
test catalog::capability_tests::oauth_payload_and_headers_do_not_enter_decision_records ... ok
test protocol::tests::anthropic_upstream_events_decode_to_tools_text_and_done ... ok
test protocol::tests::multi_line_data_frames_join_and_empty_ones_stay_errors ... ok
test protocol::tests::upstream_chat_stream_reencodes_to_anthropic_sse ... ok
test protocol::tests::responses_output_indices_become_contiguous_chat_tool_indices ... ok
test catalog::capability_tests::semantic_revisions_ignore_object_order_and_credential_rotation ... ok
test catalog::capability_tests::every_preference_obeys_known_capabilities_and_context ... ok
test catalog::capability_tests::detailed_discovery_is_bounded_and_preserves_evidence_distinctions ... ok
test proxy::capability_tests::a_real_pi_turn_is_admitted_rather_than_refused_by_every_route ... ok
test proxy::capability_tests::an_explicit_null_field_reads_as_absent_not_as_a_malformed_request ... ok
test auth::tests::oauth_store_round_trips_and_removes ... ok
test proxy::capability_tests::cancelled_execution_retains_the_started_attempt_without_claiming_selection ... ok
test auth::tests::valid_oauth_requests_do_not_wait_for_the_store_writer ... ok
test proxy::capability_tests::buffering_missing_usage_stream_handoff_and_attempt_bounds_remain_explicit ... ok
test proxy::capability_tests::a_policy_reload_during_fallback_does_not_change_the_attributed_snapshot ... ok
test proxy::capability_tests::every_auto_task_selector_is_listed_as_well_as_routed ... ok
test proxy::capability_tests::cancelled_and_persisted_inflight_recovery_is_not_replayed ... ok
test proxy::capability_tests::actual_failover_skips_incompatible_routes_and_preserves_required_fields ... ok
test proxy::capability_tests::native_anthropic_features_survive_selection_and_request_encoding ... ok
test proxy::capability_tests::fallback_costs_bind_each_attempt_and_preserve_price_history ... ok
test proxy::capability_tests::free_routes_lead_paid_and_yield_only_when_unhealthy_or_disabled ... ok
test proxy::capability_tests::no_compatible_route_fails_before_network_and_health_rules_cannot_waive_fields ... ok
test settings::tests::storage_paths_are_required_without_implicit_locations ... ok
test sync::tests::a_provider_without_live_inventory_still_contributes_its_known_models ... ok
test sync::tests::an_entry_lands_under_the_alias_then_the_shared_core_then_its_slug ... ok
test sync::tests::incomplete_hops_do_not_inherit_other_providers_or_refresh_expired_evidence ... ok
test sync::tests::subscription_cache_reads_are_not_fresh_remote_observations ... ok
test sync::tests::the_fallback_index_lists_known_models_and_unknown_providers_stay_empty ... ok
test telemetry::tests::native_usage_partial_fields_survive_and_overflow_cost_is_unknown ... ok
test telemetry::tests::partial_and_omitted_attempts_keep_total_unknown_without_repeating_subtotal ... ok
test telemetry::tests::pricing_and_estimates_keep_missing_and_age_explicit ... ok
test telemetry::tests::snapshots_distinguish_unknown_zero_invalid_and_never_double_count ... ok
test proxy::capability_tests::explained_execution_distinguishes_rejections_and_binds_actual_fallback ... ok
test proxy::capability_tests::concurrent_sweeps_coalesce_and_obsolete_probe_cannot_clear_newer_failure ... ok
test proxy::capability_tests::native_and_stream_explanations_are_optional_and_archival_bounds_are_explicit ... ok
test proxy::capability_tests::a_turn_without_an_answer_falls_back_and_only_a_broken_route_opens_an_incident ... ok
test proxy::capability_tests::persistence_deadlines_and_missing_authority_fail_without_probe_dispatch ... ok
test proxy::capability_tests::recovery_requires_complete_native_responses_with_valid_tools ... ok
test proxy::capability_tests::terminal_routes_do_not_starve_eligible_recovery_and_legacy_is_explicit ... ok
test proxy::capability_tests::recovery_budget_survives_repeated_failures_and_restart ... ok
test proxy::capability_tests::recovery_bounds_a_stalled_attempt_and_rejects_empty_completion ... ok

test result: ok. 50 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 1.14s

test      router     pass

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/pty-router-harness-mcp-tests-are-green/specs/spec01.md: exit 0

Command SHA-256: 8375a32240a8aebdc243be87bc7a5dc3cb9d05d8316b0a5bae2a5f70fc0f82ac

```text
toolchain: cargo cargo-nextest bun tmux
    Finished `test` profile [unoptimized] target(s) in 0.05s
     Running unittests src/lib.rs (router.ctg/target/debug/deps/router-dc069610eb152864)

running 50 tests
test auth::tests::jwt_exp_decodes_the_expiry_claim ... ok
test frontier::tests::a_board_name_meets_the_id_a_provider_serves ... ok
test auth::tests::device_begin_guides_key_providers_to_a_key ... ok
test frontier::tests::distinct_models_stay_distinct ... ok
test catalog::capability_tests::oauth_payload_and_headers_do_not_enter_decision_records ... ok
test frontier::tests::the_best_matching_row_wins_and_borrowed_tasks_read_their_source ... ok
test catalog::capability_tests::wire_features_require_explicit_support_and_native_preservation ... ok
test catalog::capability_tests::translated_client_fields_admit_a_foreign_wire_and_leave_the_request ... ok
test catalog::capability_tests::semantic_revisions_ignore_object_order_and_credential_rotation ... ok
test protocol::tests::chat_to_anthropic_carries_tool_calls_and_tool_results ... ok
test protocol::tests::anthropic_in_chat_out_and_back_through_the_encoder ... ok
test protocol::tests::anthropic_upstream_events_decode_to_tools_text_and_done ... ok
test protocol::tests::multi_line_data_frames_join_and_empty_ones_stay_errors ... ok
test protocol::tests::responses_output_indices_become_contiguous_chat_tool_indices ... ok
test protocol::tests::upstream_chat_stream_reencodes_to_anthropic_sse ... ok
test catalog::capability_tests::every_preference_obeys_known_capabilities_and_context ... ok
test catalog::capability_tests::detailed_discovery_is_bounded_and_preserves_evidence_distinctions ... ok
test proxy::capability_tests::an_explicit_null_field_reads_as_absent_not_as_a_malformed_request ... ok
test proxy::capability_tests::a_real_pi_turn_is_admitted_rather_than_refused_by_every_route ... ok
test auth::tests::oauth_store_round_trips_and_removes ... ok
test proxy::capability_tests::cancelled_execution_retains_the_started_attempt_without_claiming_selection ... ok
test auth::tests::valid_oauth_requests_do_not_wait_for_the_store_writer ... ok
test proxy::capability_tests::buffering_missing_usage_stream_handoff_and_attempt_bounds_remain_explicit ... ok
test proxy::capability_tests::a_policy_reload_during_fallback_does_not_change_the_attributed_snapshot ... ok
test proxy::capability_tests::every_auto_task_selector_is_listed_as_well_as_routed ... ok
test proxy::capability_tests::actual_failover_skips_incompatible_routes_and_preserves_required_fields ... ok
test proxy::capability_tests::fallback_costs_bind_each_attempt_and_preserve_price_history ... ok
test proxy::capability_tests::cancelled_and_persisted_inflight_recovery_is_not_replayed ... ok
test proxy::capability_tests::native_anthropic_features_survive_selection_and_request_encoding ... ok
test proxy::capability_tests::explained_execution_distinguishes_rejections_and_binds_actual_fallback ... ok
test proxy::capability_tests::free_routes_lead_paid_and_yield_only_when_unhealthy_or_disabled ... ok
test proxy::capability_tests::no_compatible_route_fails_before_network_and_health_rules_cannot_waive_fields ... ok
test settings::tests::storage_paths_are_required_without_implicit_locations ... ok
test sync::tests::an_entry_lands_under_the_alias_then_the_shared_core_then_its_slug ... ok
test sync::tests::a_provider_without_live_inventory_still_contributes_its_known_models ... ok
test sync::tests::subscription_cache_reads_are_not_fresh_remote_observations ... ok
test sync::tests::incomplete_hops_do_not_inherit_other_providers_or_refresh_expired_evidence ... ok
test sync::tests::the_fallback_index_lists_known_models_and_unknown_providers_stay_empty ... ok
test telemetry::tests::partial_and_omitted_attempts_keep_total_unknown_without_repeating_subtotal ... ok
test telemetry::tests::native_usage_partial_fields_survive_and_overflow_cost_is_unknown ... ok
test telemetry::tests::snapshots_distinguish_unknown_zero_invalid_and_never_double_count ... ok
test telemetry::tests::pricing_and_estimates_keep_missing_and_age_explicit ... ok
test proxy::capability_tests::concurrent_sweeps_coalesce_and_obsolete_probe_cannot_clear_newer_failure ... ok
test proxy::capability_tests::native_and_stream_explanations_are_optional_and_archival_bounds_are_explicit ... ok
test proxy::capability_tests::a_turn_without_an_answer_falls_back_and_only_a_broken_route_opens_an_incident ... ok
test proxy::capability_tests::persistence_deadlines_and_missing_authority_fail_without_probe_dispatch ... ok
test proxy::capability_tests::recovery_requires_complete_native_responses_with_valid_tools ... ok
test proxy::capability_tests::terminal_routes_do_not_starve_eligible_recovery_and_legacy_is_explicit ... ok
test proxy::capability_tests::recovery_budget_survives_repeated_failures_and_restart ... ok
test proxy::capability_tests::recovery_bounds_a_stalled_attempt_and_rejects_empty_completion ... ok

test result: ok. 50 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 1.14s

test      router     pass

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/pty-router-harness-mcp-tests-are-green/specs/spec01.md: exit 0

Command SHA-256: 8375a32240a8aebdc243be87bc7a5dc3cb9d05d8316b0a5bae2a5f70fc0f82ac

```text
toolchain: cargo cargo-nextest bun tmux
    Finished `test` profile [unoptimized] target(s) in 0.05s
     Running unittests src/lib.rs (router.ctg/target/debug/deps/router-dc069610eb152864)

running 50 tests
test auth::tests::jwt_exp_decodes_the_expiry_claim ... ok
test catalog::capability_tests::wire_features_require_explicit_support_and_native_preservation ... ok
test auth::tests::device_begin_guides_key_providers_to_a_key ... ok
test frontier::tests::a_board_name_meets_the_id_a_provider_serves ... ok
test catalog::capability_tests::translated_client_fields_admit_a_foreign_wire_and_leave_the_request ... ok
test frontier::tests::the_best_matching_row_wins_and_borrowed_tasks_read_their_source ... ok
test frontier::tests::distinct_models_stay_distinct ... ok
test catalog::capability_tests::oauth_payload_and_headers_do_not_enter_decision_records ... ok
test protocol::tests::chat_to_anthropic_carries_tool_calls_and_tool_results ... ok
test protocol::tests::anthropic_upstream_events_decode_to_tools_text_and_done ... ok
test protocol::tests::anthropic_in_chat_out_and_back_through_the_encoder ... ok
test catalog::capability_tests::semantic_revisions_ignore_object_order_and_credential_rotation ... ok
test protocol::tests::multi_line_data_frames_join_and_empty_ones_stay_errors ... ok
test protocol::tests::upstream_chat_stream_reencodes_to_anthropic_sse ... ok
test protocol::tests::responses_output_indices_become_contiguous_chat_tool_indices ... ok
test catalog::capability_tests::every_preference_obeys_known_capabilities_and_context ... ok
test catalog::capability_tests::detailed_discovery_is_bounded_and_preserves_evidence_distinctions ... ok
test auth::tests::oauth_store_round_trips_and_removes ... ok
test proxy::capability_tests::a_real_pi_turn_is_admitted_rather_than_refused_by_every_route ... ok
test proxy::capability_tests::cancelled_execution_retains_the_started_attempt_without_claiming_selection ... ok
test proxy::capability_tests::an_explicit_null_field_reads_as_absent_not_as_a_malformed_request ... ok
test auth::tests::valid_oauth_requests_do_not_wait_for_the_store_writer ... ok
test proxy::capability_tests::buffering_missing_usage_stream_handoff_and_attempt_bounds_remain_explicit ... ok
test proxy::capability_tests::a_policy_reload_during_fallback_does_not_change_the_attributed_snapshot ... ok
test proxy::capability_tests::every_auto_task_selector_is_listed_as_well_as_routed ... ok
test proxy::capability_tests::cancelled_and_persisted_inflight_recovery_is_not_replayed ... ok
test proxy::capability_tests::native_anthropic_features_survive_selection_and_request_encoding ... ok
test proxy::capability_tests::actual_failover_skips_incompatible_routes_and_preserves_required_fields ... ok
test proxy::capability_tests::fallback_costs_bind_each_attempt_and_preserve_price_history ... ok
test proxy::capability_tests::free_routes_lead_paid_and_yield_only_when_unhealthy_or_disabled ... ok
test proxy::capability_tests::explained_execution_distinguishes_rejections_and_binds_actual_fallback ... ok
test settings::tests::storage_paths_are_required_without_implicit_locations ... ok
test sync::tests::a_provider_without_live_inventory_still_contributes_its_known_models ... ok
test sync::tests::an_entry_lands_under_the_alias_then_the_shared_core_then_its_slug ... ok
test sync::tests::incomplete_hops_do_not_inherit_other_providers_or_refresh_expired_evidence ... ok
test sync::tests::subscription_cache_reads_are_not_fresh_remote_observations ... ok
test sync::tests::the_fallback_index_lists_known_models_and_unknown_providers_stay_empty ... ok
test telemetry::tests::native_usage_partial_fields_survive_and_overflow_cost_is_unknown ... ok
test telemetry::tests::partial_and_omitted_attempts_keep_total_unknown_without_repeating_subtotal ... ok
test telemetry::tests::pricing_and_estimates_keep_missing_and_age_explicit ... ok
test telemetry::tests::snapshots_distinguish_unknown_zero_invalid_and_never_double_count ... ok
test proxy::capability_tests::no_compatible_route_fails_before_network_and_health_rules_cannot_waive_fields ... ok
test proxy::capability_tests::native_and_stream_explanations_are_optional_and_archival_bounds_are_explicit ... ok
test proxy::capability_tests::concurrent_sweeps_coalesce_and_obsolete_probe_cannot_clear_newer_failure ... ok
test proxy::capability_tests::a_turn_without_an_answer_falls_back_and_only_a_broken_route_opens_an_incident ... ok
test proxy::capability_tests::recovery_requires_complete_native_responses_with_valid_tools ... ok
test proxy::capability_tests::persistence_deadlines_and_missing_authority_fail_without_probe_dispatch ... ok
test proxy::capability_tests::terminal_routes_do_not_starve_eligible_recovery_and_legacy_is_explicit ... ok
test proxy::capability_tests::recovery_budget_survives_repeated_failures_and_restart ... ok
test proxy::capability_tests::recovery_bounds_a_stalled_attempt_and_rejects_empty_completion ... ok

test result: ok. 50 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 1.15s

test      router     pass

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/pty-router-harness-mcp-tests-are-green/specs/spec01.md: exit 0

Command SHA-256: 08917e650079d24c9fcff98252dbf064b891952b678aa3b70d005d5a15a32ad6

```text
toolchain: cargo cargo-nextest bun tmux
    Finished `test` profile [unoptimized] target(s) in 0.03s
     Running unittests src/lib.rs (harness.ctg/target/debug/deps/harness-59162cf5dbee3069)

running 39 tests
test prompt::tests::replaces_only_exact_known_placeholders_without_recursion ... ok
test compaction::tests::malformed_legacy_evidence_survives_regeneration_and_unknown_versions_fail ... ok
test roster::tests::host_binding_rejects_bad_caps_and_never_accepts_request_credentials ... ok
test compaction::tests::prefix_and_original_tail_are_verified_independently ... ok
test compaction::tests::legacy_upgrade_retains_summary_and_labels_missing_evidence ... ok
test tests::a_record_that_cannot_compose_still_yields_a_usable_prompt ... ok
test inspection::accounting::tests::historical_usage_keeps_run_and_turn_identity_without_replacing_estimate ... ok
test tests::anchor_names_session_foreground_and_files_without_the_user_naming_them ... ok
test inspection::accounting::tests::multilingual_schemas_and_tool_exchanges_keep_byte_enforcement ... ok
test roster::tests::final_render_is_escaped_after_template_and_accounts_whole_row_omissions ... ok
test tests::descriptors_become_function_tools_and_bad_ones_fail ... ok
test tests::context_and_compaction_use_the_supplied_memo_template ... ok
test tests::canonical_deduplication_keeps_each_source_once ... ok
test tests::journal_projects_ordered_messages_without_lifecycle_records ... ok
test tests::compacted_projection_fits_budget ... ok
test tests::malformed_configuration_is_rejected ... ok
test tests::markdown_system_resolves_session_values_and_optional_context_once ... ok
test tests::malformed_records_and_unresolved_groups_are_refused ... ok
test tests::compacted_projection_inserts_summary_and_keeps_tail ... ok
test tests::native_date_covers_the_utc_day_boundary_and_stays_fresh ... ok
test tests::ancestor_tree_orders_instructions_and_leaves_legacy_memos_alone ... ok
test tests::prefix_hash_is_stable_and_distinguishes_prefixes ... ok
test tests::tail_start_keeps_complete_turns_and_never_splits_tool_groups ... ok
test tests::telemetry_renders_from_the_journal_and_the_block_is_posted_to_build_system ... ok
test tests::framing_delimiters_are_escaped_and_multibyte_stays_valid ... ok
test tests::terminal_renders_recent_commands_or_nothing ... ok
test roster::tests::source_adapter_checks_identity_digest_revisions_bounds_and_private_inbox_fields ... ok
test tests::missing_optional_files_are_skipped_and_bad_files_error ... ok
test working::tests::multi_call_groups_are_indivisible_and_open_groups_are_rejected ... ok
test tests::total_instruction_budget_is_enforced ... ok
test inspection::tests::compaction_can_shrink_retained_turns_without_cutting_current_input ... ok
test tests::oversized_context_returns_context_over_budget_without_changing_transcript ... ok
test working::tests::compacts_inside_a_tool_loop_and_pins_current_request ... ok
test working::tests::message_and_byte_limits_trigger_with_provider_headroom ... ok
test tests::environment_renders_as_one_block_or_empty ... ok
test inspection::tests::oversized_result_no_longer_blocks_the_next_model_turn ... ok
test working::tests::saved_memory_is_validated_and_refreshes_after_new_messages ... ok
test inspection::tests::long_open_tool_exchange_keeps_all_ids_and_fits_budget ... ok
test working::tests::old_history_is_folded_in_small_complete_batches ... ok

test result: ok. 39 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.07s

     Running .cartridge/tests/integration/process.rs (harness.ctg/target/debug/deps/process-2f588e52a3259af6)

running 4 tests
    Finished `dev` profile [unoptimized] target(s) in 0.02s
test harness_projects_context_over_the_real_base ... ok
test harness_fails_safely_on_huge_turns_and_router_failures ... ok
test harness_compacts_oversized_context_over_the_real_base ... ok
test harness_fails_on_router_timeout_without_history_loss ... ok

test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 1.10s

     Running .cartridge/tests/integration/ring.rs (harness.ctg/target/debug/deps/ring-222f580290e3ba20)

running 1 test
    Finished `dev` profile [unoptimized] target(s) in 0.02s
test the_ring_distills_old_turns_into_memory_and_keeps_the_rest ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.44s

     Running .cartridge/tests/integration/working.rs (harness.ctg/target/debug/deps/working-04e382d2515a2baf)

running 1 test
    Finished `dev` profile [unoptimized] target(s) in 0.02s
test rolling_memory_refreshes_below_budget_and_survives_reload_and_failure ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 6.26s

test      harness    pass

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/pty-router-harness-mcp-tests-are-green/specs/spec01.md: exit 0

Command SHA-256: 08917e650079d24c9fcff98252dbf064b891952b678aa3b70d005d5a15a32ad6

```text
toolchain: cargo cargo-nextest bun tmux
    Finished `test` profile [unoptimized] target(s) in 0.03s
     Running unittests src/lib.rs (harness.ctg/target/debug/deps/harness-59162cf5dbee3069)

running 39 tests
test prompt::tests::replaces_only_exact_known_placeholders_without_recursion ... ok
test compaction::tests::malformed_legacy_evidence_survives_regeneration_and_unknown_versions_fail ... ok
test compaction::tests::legacy_upgrade_retains_summary_and_labels_missing_evidence ... ok
test roster::tests::host_binding_rejects_bad_caps_and_never_accepts_request_credentials ... ok
test tests::a_record_that_cannot_compose_still_yields_a_usable_prompt ... ok
test compaction::tests::prefix_and_original_tail_are_verified_independently ... ok
test tests::anchor_names_session_foreground_and_files_without_the_user_naming_them ... ok
test inspection::accounting::tests::historical_usage_keeps_run_and_turn_identity_without_replacing_estimate ... ok
test inspection::accounting::tests::multilingual_schemas_and_tool_exchanges_keep_byte_enforcement ... ok
test roster::tests::final_render_is_escaped_after_template_and_accounts_whole_row_omissions ... ok
test tests::descriptors_become_function_tools_and_bad_ones_fail ... ok
test tests::context_and_compaction_use_the_supplied_memo_template ... ok
test tests::ancestor_tree_orders_instructions_and_leaves_legacy_memos_alone ... ok
test tests::compacted_projection_inserts_summary_and_keeps_tail ... ok
test tests::malformed_configuration_is_rejected ... ok
test tests::canonical_deduplication_keeps_each_source_once ... ok
test tests::journal_projects_ordered_messages_without_lifecycle_records ... ok
test tests::compacted_projection_fits_budget ... ok
test tests::markdown_system_resolves_session_values_and_optional_context_once ... ok
test tests::native_date_covers_the_utc_day_boundary_and_stays_fresh ... ok
test tests::malformed_records_and_unresolved_groups_are_refused ... ok
test tests::prefix_hash_is_stable_and_distinguishes_prefixes ... ok
test tests::telemetry_renders_from_the_journal_and_the_block_is_posted_to_build_system ... ok
test tests::tail_start_keeps_complete_turns_and_never_splits_tool_groups ... ok
test tests::terminal_renders_recent_commands_or_nothing ... ok
test tests::framing_delimiters_are_escaped_and_multibyte_stays_valid ... ok
test tests::missing_optional_files_are_skipped_and_bad_files_error ... ok
test working::tests::multi_call_groups_are_indivisible_and_open_groups_are_rejected ... ok
test tests::oversized_context_returns_context_over_budget_without_changing_transcript ... ok
test roster::tests::source_adapter_checks_identity_digest_revisions_bounds_and_private_inbox_fields ... ok
test tests::total_instruction_budget_is_enforced ... ok
test inspection::tests::compaction_can_shrink_retained_turns_without_cutting_current_input ... ok
test working::tests::compacts_inside_a_tool_loop_and_pins_current_request ... ok
test working::tests::message_and_byte_limits_trigger_with_provider_headroom ... ok
test tests::environment_renders_as_one_block_or_empty ... ok
test inspection::tests::oversized_result_no_longer_blocks_the_next_model_turn ... ok
test working::tests::saved_memory_is_validated_and_refreshes_after_new_messages ... ok
test inspection::tests::long_open_tool_exchange_keeps_all_ids_and_fits_budget ... ok
test working::tests::old_history_is_folded_in_small_complete_batches ... ok

test result: ok. 39 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.07s

     Running .cartridge/tests/integration/process.rs (harness.ctg/target/debug/deps/process-2f588e52a3259af6)

running 4 tests
    Finished `dev` profile [unoptimized] target(s) in 0.02s
test harness_projects_context_over_the_real_base ... ok
test harness_fails_on_router_timeout_without_history_loss ... ok
test harness_compacts_oversized_context_over_the_real_base ... ok
test harness_fails_safely_on_huge_turns_and_router_failures ... ok

test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 1.04s

     Running .cartridge/tests/integration/ring.rs (harness.ctg/target/debug/deps/ring-222f580290e3ba20)

running 1 test
    Finished `dev` profile [unoptimized] target(s) in 0.02s
test the_ring_distills_old_turns_into_memory_and_keeps_the_rest ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.43s

     Running .cartridge/tests/integration/working.rs (harness.ctg/target/debug/deps/working-04e382d2515a2baf)

running 1 test
    Finished `dev` profile [unoptimized] target(s) in 0.02s
test rolling_memory_refreshes_below_budget_and_survives_reload_and_failure ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 6.88s

test      harness    pass

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/pty-router-harness-mcp-tests-are-green/specs/spec01.md: exit 0

Command SHA-256: 08917e650079d24c9fcff98252dbf064b891952b678aa3b70d005d5a15a32ad6

```text
toolchain: cargo cargo-nextest bun tmux
    Finished `test` profile [unoptimized] target(s) in 0.03s
     Running unittests src/lib.rs (harness.ctg/target/debug/deps/harness-59162cf5dbee3069)

running 39 tests
test prompt::tests::replaces_only_exact_known_placeholders_without_recursion ... ok
test compaction::tests::legacy_upgrade_retains_summary_and_labels_missing_evidence ... ok
test compaction::tests::malformed_legacy_evidence_survives_regeneration_and_unknown_versions_fail ... ok
test roster::tests::host_binding_rejects_bad_caps_and_never_accepts_request_credentials ... ok
test tests::a_record_that_cannot_compose_still_yields_a_usable_prompt ... ok
test compaction::tests::prefix_and_original_tail_are_verified_independently ... ok
test inspection::accounting::tests::historical_usage_keeps_run_and_turn_identity_without_replacing_estimate ... ok
test tests::anchor_names_session_foreground_and_files_without_the_user_naming_them ... ok
test roster::tests::final_render_is_escaped_after_template_and_accounts_whole_row_omissions ... ok
test inspection::accounting::tests::multilingual_schemas_and_tool_exchanges_keep_byte_enforcement ... ok
test tests::descriptors_become_function_tools_and_bad_ones_fail ... ok
test tests::context_and_compaction_use_the_supplied_memo_template ... ok
test tests::canonical_deduplication_keeps_each_source_once ... ok
test tests::journal_projects_ordered_messages_without_lifecycle_records ... ok
test tests::ancestor_tree_orders_instructions_and_leaves_legacy_memos_alone ... ok
test tests::malformed_configuration_is_rejected ... ok
test tests::markdown_system_resolves_session_values_and_optional_context_once ... ok
test tests::malformed_records_and_unresolved_groups_are_refused ... ok
test tests::compacted_projection_inserts_summary_and_keeps_tail ... ok
test tests::native_date_covers_the_utc_day_boundary_and_stays_fresh ... ok
test tests::framing_delimiters_are_escaped_and_multibyte_stays_valid ... ok
test tests::prefix_hash_is_stable_and_distinguishes_prefixes ... ok
test tests::telemetry_renders_from_the_journal_and_the_block_is_posted_to_build_system ... ok
test tests::terminal_renders_recent_commands_or_nothing ... ok
test tests::tail_start_keeps_complete_turns_and_never_splits_tool_groups ... ok
test tests::compacted_projection_fits_budget ... ok
test roster::tests::source_adapter_checks_identity_digest_revisions_bounds_and_private_inbox_fields ... ok
test tests::missing_optional_files_are_skipped_and_bad_files_error ... ok
test working::tests::multi_call_groups_are_indivisible_and_open_groups_are_rejected ... ok
test tests::oversized_context_returns_context_over_budget_without_changing_transcript ... ok
test tests::total_instruction_budget_is_enforced ... ok
test inspection::tests::compaction_can_shrink_retained_turns_without_cutting_current_input ... ok
test working::tests::compacts_inside_a_tool_loop_and_pins_current_request ... ok
test working::tests::message_and_byte_limits_trigger_with_provider_headroom ... ok
test tests::environment_renders_as_one_block_or_empty ... ok
test inspection::tests::oversized_result_no_longer_blocks_the_next_model_turn ... ok
test working::tests::saved_memory_is_validated_and_refreshes_after_new_messages ... ok
test inspection::tests::long_open_tool_exchange_keeps_all_ids_and_fits_budget ... ok
test working::tests::old_history_is_folded_in_small_complete_batches ... ok

test result: ok. 39 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.07s

     Running .cartridge/tests/integration/process.rs (harness.ctg/target/debug/deps/process-2f588e52a3259af6)

running 4 tests
    Finished `dev` profile [unoptimized] target(s) in 0.02s
test harness_projects_context_over_the_real_base ... ok
test harness_compacts_oversized_context_over_the_real_base ... ok
test harness_fails_safely_on_huge_turns_and_router_failures ... ok
test harness_fails_on_router_timeout_without_history_loss ... ok

test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.95s

     Running .cartridge/tests/integration/ring.rs (harness.ctg/target/debug/deps/ring-222f580290e3ba20)

running 1 test
    Finished `dev` profile [unoptimized] target(s) in 0.02s
test the_ring_distills_old_turns_into_memory_and_keeps_the_rest ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.44s

     Running .cartridge/tests/integration/working.rs (harness.ctg/target/debug/deps/working-04e382d2515a2baf)

running 1 test
    Finished `dev` profile [unoptimized] target(s) in 0.02s
test rolling_memory_refreshes_below_budget_and_survives_reload_and_failure ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 6.95s

test      harness    pass

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/pty-router-harness-mcp-tests-are-green/specs/spec01.md: exit 0

Command SHA-256: 1cb7eb67aa5868e3009fdd729202acb64ccaef143b7c48b04e921cc10424e595

```text
toolchain: cargo cargo-nextest bun tmux
    Finished `test` profile [unoptimized] target(s) in 0.03s
     Running unittests src/lib.rs (mcp.ctg/target/debug/deps/mcp-b4cac2af4ee00b76)

running 13 tests
test tests::an_empty_profile_exposes_no_tools_and_an_unknown_one_is_refused ... ok
test tests::a_broken_line_and_an_unknown_method_answer_without_dropping_the_connection ... ok
test tests::an_ask_refusal_names_the_operation_and_the_missing_channel ... ok
test tests::an_empty_tool_list_follows_the_needs_and_is_described_on_every_list ... ok
test tests::a_denied_call_and_a_failing_tool_are_results_the_client_continues_from ... ok
test tests::a_client_initializes_lists_the_profiles_tools_and_calls_one ... ok
test tests::cancelling_a_call_reaches_the_tool_under_that_calls_own_identity ... ok
test tests::granted_calls_land_in_the_observation_journal_with_caller_and_turn ... ok
test tests::quiet_defaults_do_not_write_an_automatic_observation_journal ... ok
test tests::diagnostic_inspection_is_optional_scoped_and_cannot_grant_authority ... ok
test tests::unavailable_or_changed_explanations_never_replace_refusal_with_allow ... ok
bun test v1.3.14 (0d9b296a)

 1 pass
 0 fail
 24 expect() calls
Ran 1 test across 1 file. [1.74s]
test tests::initialized_live_client_inspects_real_policy_without_granting_writes ... ok
test tests::initialized_live_client_observes_catalog_replacements ... ok

test result: ok. 13 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 2.90s

test      mcp        pass

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/pty-router-harness-mcp-tests-are-green/specs/spec01.md: exit 0

Command SHA-256: 1cb7eb67aa5868e3009fdd729202acb64ccaef143b7c48b04e921cc10424e595

```text
toolchain: cargo cargo-nextest bun tmux
    Finished `test` profile [unoptimized] target(s) in 0.03s
     Running unittests src/lib.rs (mcp.ctg/target/debug/deps/mcp-b4cac2af4ee00b76)

running 13 tests
test tests::an_empty_profile_exposes_no_tools_and_an_unknown_one_is_refused ... ok
test tests::a_broken_line_and_an_unknown_method_answer_without_dropping_the_connection ... ok
test tests::an_empty_tool_list_follows_the_needs_and_is_described_on_every_list ... ok
test tests::granted_calls_land_in_the_observation_journal_with_caller_and_turn ... ok
test tests::an_ask_refusal_names_the_operation_and_the_missing_channel ... ok
test tests::quiet_defaults_do_not_write_an_automatic_observation_journal ... ok
test tests::a_client_initializes_lists_the_profiles_tools_and_calls_one ... ok
test tests::cancelling_a_call_reaches_the_tool_under_that_calls_own_identity ... ok
test tests::diagnostic_inspection_is_optional_scoped_and_cannot_grant_authority ... ok
test tests::a_denied_call_and_a_failing_tool_are_results_the_client_continues_from ... ok
test tests::unavailable_or_changed_explanations_never_replace_refusal_with_allow ... ok
bun test v1.3.14 (0d9b296a)

 1 pass
 0 fail
 24 expect() calls
Ran 1 test across 1 file. [1434.00ms]
test tests::initialized_live_client_inspects_real_policy_without_granting_writes ... ok
test tests::initialized_live_client_observes_catalog_replacements ... ok

test result: ok. 13 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 2.85s

test      mcp        pass

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/pty-router-harness-mcp-tests-are-green/specs/spec01.md: exit 0

Command SHA-256: 1cb7eb67aa5868e3009fdd729202acb64ccaef143b7c48b04e921cc10424e595

```text
toolchain: cargo cargo-nextest bun tmux
    Finished `test` profile [unoptimized] target(s) in 0.03s
     Running unittests src/lib.rs (mcp.ctg/target/debug/deps/mcp-b4cac2af4ee00b76)

running 13 tests
test tests::an_empty_profile_exposes_no_tools_and_an_unknown_one_is_refused ... ok
test tests::a_broken_line_and_an_unknown_method_answer_without_dropping_the_connection ... ok
test tests::an_ask_refusal_names_the_operation_and_the_missing_channel ... ok
test tests::granted_calls_land_in_the_observation_journal_with_caller_and_turn ... ok
test tests::diagnostic_inspection_is_optional_scoped_and_cannot_grant_authority ... ok
test tests::an_empty_tool_list_follows_the_needs_and_is_described_on_every_list ... ok
test tests::cancelling_a_call_reaches_the_tool_under_that_calls_own_identity ... ok
test tests::a_client_initializes_lists_the_profiles_tools_and_calls_one ... ok
test tests::quiet_defaults_do_not_write_an_automatic_observation_journal ... ok
test tests::a_denied_call_and_a_failing_tool_are_results_the_client_continues_from ... ok
test tests::unavailable_or_changed_explanations_never_replace_refusal_with_allow ... ok
bun test v1.3.14 (0d9b296a)

 1 pass
 0 fail
 24 expect() calls
Ran 1 test across 1 file. [1478.00ms]
test tests::initialized_live_client_inspects_real_policy_without_granting_writes ... ok
test tests::initialized_live_client_observes_catalog_replacements ... ok

test result: ok. 13 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 2.88s

test      mcp        pass

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/pty-router-harness-mcp-tests-are-green/specs/spec01.md: exit 0

Command SHA-256: 84c72610132aab982ccfd0566bd567a723be2d96a027c66a5a52e92581611c3a

```text
toolchain: cargo cargo-nextest bun tmux
    Finished `dev` profile [unoptimized] target(s) in 0.06s
check     pty        pass

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/pty-router-harness-mcp-tests-are-green/specs/spec01.md: exit 0

Command SHA-256: 5b5795edc0dfcd223c27fdac20a2f29f017297ae7f334bd85e3e0d96139fe908

```text
toolchain: cargo cargo-nextest bun tmux
    Finished `dev` profile [unoptimized] target(s) in 0.09s
check     router     pass

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/pty-router-harness-mcp-tests-are-green/specs/spec01.md: exit 0

Command SHA-256: c06e0d396dd799d9f73b417f5353b162cccbb4c7616b77c10deb13cad3dfe336

```text
toolchain: cargo cargo-nextest bun tmux
    Finished `dev` profile [unoptimized] target(s) in 0.06s
check     harness    pass

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/pty-router-harness-mcp-tests-are-green/specs/spec01.md: exit 0

Command SHA-256: d501855be255e9277d15101cb05245967a078df26e5dd61aad8bd09957e2290e

```text
toolchain: cargo cargo-nextest bun tmux
    Finished `dev` profile [unoptimized] target(s) in 0.06s
check     mcp        pass

```
