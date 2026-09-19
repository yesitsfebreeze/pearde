---
commit: "54749f4309860bb39555570298f3e14957d7dfef"
verification-target: "committed"
original-commit: "54749f4309860bb39555570298f3e14957d7dfef"
spec-digests: {"spec01.md":"916fc29d56e1f3262073dd69bd0a64e948eb2689c5cf7a9e415a913f11b273f1"}
child-contracts: {}
workspace-verified: true
workspace-drift: []
---

# Collection

Verified committed snapshot 54749f4309860bb39555570298f3e14957d7dfef in /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-lf670k/source.

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/the-isolation-gate-reads-the-composition-profile/an-optional-need-with-no-provider-still-loads/specs/spec01.md: exit 0

Command SHA-256: 7d5843248e0247add2525a0ad4cf06339e318b9445567b3d1b3335b0d1db2a57

```text
passed: optional_need_without_provider_loads_and_answers, optional_glob_is_refused_without_losing_optionality
   Compiling cartridge v0.1.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-lf670k/source)
    Finished `test` profile [unoptimized] target(s) in 6.17s
     Running unittests src/lib.rs (/tmp/optional-needs-target/debug/deps/cartridge-84da6c7c4bfbad09)

running 7 tests
test host::plan::tests::a_cartridge_gets_listeners_only_for_what_it_defines_or_needs ... ok
test host::plan::tests::a_listener_accepts_each_declared_sender_for_its_events_only ... ok
test host::plan::tests::a_private_host_keeps_its_socket_and_ports_to_itself ... ok
test host::plan::tests::every_event_carries_its_deadline ... ok
test host::plan::tests::no_node_holds_a_token_another_node_accepts_from_someone_else ... ok
test host::plan::tests::optional_glob_is_refused_without_losing_optionality ... ok
test host::plan::tests::optional_need_without_provider_loads_and_answers ... ok

test result: ok. 7 passed; 0 failed; 0 ignored; 0 measured; 179 filtered out; finished in 4.38s


```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/the-isolation-gate-reads-the-composition-profile/an-optional-need-with-no-provider-still-loads/specs/spec01.md: exit 0

Command SHA-256: f237011b19d8befe0228e65a86604eb843917cac95fd2ea5da0a95d04d1042f0

```text
   Compiling cartridge v0.1.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-lf670k/source)
    Finished `dev` profile [unoptimized] target(s) in 7.96s

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/the-isolation-gate-reads-the-composition-profile/an-optional-need-with-no-provider-still-loads/specs/spec01.md: exit 0

Command SHA-256: b01dba47eeaa7ef8697800baf1060c2835b5d48909a8e66f162675020acf9a3c

```text
   Compiling cartridge v0.1.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-lf670k/source)
    Finished `test` profile [unoptimized] target(s) in 4.90s
     Running unittests src/lib.rs (/tmp/optional-needs-target/debug/deps/cartridge-84da6c7c4bfbad09)

running 186 tests
test asp::tests::actions::a_cartridge_cannot_run_an_action_through_asp ... ok
test asp::tests::actions::an_action_runs_through_its_tool_and_a_denial_reaches_the_caller_unchanged ... ok
test asp::tests::base::the_base_contributes_every_tool_and_cartridge_and_lists_every_event_as_a_type ... ok
test asp::tests::composition::a_node_two_providers_assert_survives_one_of_them ... ok
test asp::tests::composition::unloading_a_provider_removes_its_types_and_facts_and_keeps_the_rest ... ok
test asp::tests::doors::a_cartridge_reaches_asp_through_the_host ... ok
test asp::tests::doors::a_cartridge_that_needs_tools_finds_asp_among_them ... ok
test asp::tests::manifest::a_manifest_refuses_an_asp_block_it_cannot_serve ... ok
test asp::tests::merge::a_fact_behind_the_owners_revision_is_marked_stale ... ok
test asp::tests::merge::an_undeclared_edge_kind_refuses_the_provider_by_name ... ok
test asp::tests::search::search_ranks_what_the_providers_found_with_the_fabrics_formula ... ok
test host::plan::tests::a_cartridge_gets_listeners_only_for_what_it_defines_or_needs ... ok
test host::plan::tests::a_listener_accepts_each_declared_sender_for_its_events_only ... ok
test host::plan::tests::a_private_host_keeps_its_socket_and_ports_to_itself ... ok
test host::plan::tests::every_event_carries_its_deadline ... ok
test host::plan::tests::no_node_holds_a_token_another_node_accepts_from_someone_else ... ok
test host::plan::tests::optional_glob_is_refused_without_losing_optionality ... ok
test host::plan::tests::optional_need_without_provider_loads_and_answers ... ok
test host::socket::tests::a_run_directory_is_owner_only ... ok
test host::socket::tests::a_symlinked_socket_directory_is_refused ... ok
test host::socket::tests::an_owner_only_directory_is_created_and_repaired ... ok
test host::socket::tests::each_run_owns_its_node_directory_and_a_dead_run_is_swept ... ok
test loader::document::tests::a_declaration_without_a_frame_round_trips_unchanged ... ok
test loader::document::tests::a_frame_outside_the_closed_set_is_refused_naming_its_kind_and_value ... ok
test loader::document::tests::each_frame_in_the_closed_set_loads ... ok
test loader::document::tests::every_current_manifest_loads_its_events_unchanged ... ok
test lua::tests::a_memory_limit_bounds_what_a_chunk_can_allocate ... ok
test lua::tests::a_runaway_is_refused_and_the_state_survives ... ok
test lua::tests::a_wait_refills_the_budget_and_a_coroutine_does_not ... ok
test lua::tests::each_file_is_evaluated_in_a_state_of_its_own ... ok
test lua::tests::every_resume_gets_the_budget_back ... ok
test lua::tests::the_interpreter_keeps_computation_and_drops_the_machine ... ok
test sandbox::tests::a_net_grant_turns_the_network_on_and_an_empty_one_leaves_it_off ... ok
test sandbox::tests::a_script_names_its_interpreter ... ok
test sandbox::tests::a_write_grant_names_the_canonicalized_path_and_implies_the_read ... ok
test sandbox::tests::an_async_spawn_is_confined_like_the_synchronous_one ... ok
test sandbox::tests::an_empty_command_is_refused_before_launch ... ok
test sandbox::tests::an_empty_grant_builds_no_allowance_beyond_the_runtime ... ok
test sandbox::tests::an_exec_grant_that_resolves_builds_a_literal_and_one_that_does_not_builds_nothing ... ok
test sandbox::tests::an_interpreter_reaches_its_own_installation ... ok
test sandbox::tests::the_microphone_is_granted_only_when_it_is_asked_for ... ok
test sandbox::tests::the_prefix_stops_at_a_system_directory ... ok
test sandbox::tests::the_runtime_is_named_canonically ... ok
test sandbox::tests::the_synchronous_command_enforces_the_empty_grant ... ok
test settings::files::tests::the_listing_reads_each_configuration_file_once ... ok
test settings::host::tests::an_undeclared_host_key_leaves_the_declared_defaults_standing ... ok
test tests::composed::a_run_against_a_live_daemon_starts_no_node ... ok
test tests::composed::one_instance_writes_what_another_reads_off_one_node ... ok
test tests::composed::two_instances_started_cold_and_concurrently_share_one_daemon ... ok
test tests::composed::two_launches_and_one_mcp_leave_one_daemon_and_one_node_per_cartridge ... ok
test tests::declarations::a_cartridge_reads_its_own_declared_events_and_no_one_elses ... ok
test tests::host::a_call_that_comes_back_into_its_sender_is_answered ... ok
test tests::host::a_cartridge_answers_the_events_it_listens_to ... ok
test tests::host::a_cartridge_asks_the_host_what_only_the_host_knows ... ok
test tests::host::a_cartridge_sends_only_what_it_defines_or_needs ... ok
test tests::host::a_document_refuses_a_bad_schema_or_a_contract_it_does_not_listen_to ... ok
test tests::host::a_glob_in_needs_names_what_the_others_listen_to ... ok
test tests::host::a_granted_env_prefix_reaches_the_node_and_nothing_beside_it_does ... ok
test tests::host::a_helper_asks_the_base_while_answering ... ok
test tests::host::a_hung_listener_times_out_and_its_node_keeps_serving ... ok
test tests::host::a_lifecycle_subscriber_that_falls_behind_is_disconnected ... ok
test tests::host::a_missing_listener_waits_and_says_for_what ... ok
test tests::host::a_native_module_reaches_the_base_through_the_global ... ok
test tests::host::a_node_presenting_its_own_credential_is_refused_on_the_host_socket ... ok
test tests::host::a_node_refuses_to_listen_to_what_it_did_not_declare ... ok
test tests::host::a_node_serves_other_events_while_a_handler_waits ... ok
test tests::host::a_node_that_catches_its_own_refusal_exits ... ok
test tests::host::a_payload_the_schema_rejects_never_reaches_the_listener ... ok
test tests::host::a_pipe_wakes_the_node_from_outside ... ok
test tests::host::a_pipe_without_fn_answers_on_its_answers_fifo ... ok
test tests::host::a_restart_keeps_its_dependents_working ... ok
test tests::host::a_rewritten_native_module_restarts_only_on_reload ... ok
test tests::host::a_schema_only_change_reaches_a_sender_that_already_validated ... ok
test tests::host::a_second_event_runs_while_a_yielding_listener_waits_on_another_cartridge ... ok
test tests::host::a_spawn_the_grant_did_not_name_is_denied ... ok
test tests::host::a_spawned_helper_sees_only_the_two_named_cartridge_variables_and_a_path ... ok
test tests::host::a_spawned_program_answers_requests_by_id ... ok
test tests::host::a_spinning_handler_is_refused_and_its_node_keeps_serving ... ok
test tests::host::a_stop_request_ends_a_foreground_run ... ok
test tests::host::a_stopped_cartridge_takes_its_programs_along ... ok
test tests::host::a_terminated_mcp_exits_with_its_input_still_open ... ok
test tests::host::a_waiting_cartridge_starts_when_the_descriptor_adds_its_listener ... ok
test tests::host::an_event_declared_twice_fails_the_later_entry ... ok
test tests::host::an_undeclared_event_fails_the_cartridge_before_it_starts ... ok
test tests::host::an_untrusted_descriptor_is_refused_where_it_is_enforced ... ok
test tests::host::gather_and_emit_reach_every_listener ... ok
test tests::host::grant_paths_name_the_project_and_settings ... ok
test tests::host::one_cartridge_cannot_see_anothers_globals ... ok
test tests::host::solo_entries_sharing_a_socket_name_are_refused ... ok
test tests::host::streams_replay_and_then_deliver_live ... ok
test tests::host::the_host_socket_answers_the_command_line ... ok
test tests::host::two_cartridges_that_need_each_other_both_start_when_one_asks_with_a_question_mark ... ok
test tests::host::verify_sends_every_declared_contract ... ok
test tests::ledger::a_root_that_does_not_exist_is_an_empty_ledger ... ok
test tests::ledger::an_entry_is_its_path_from_the_root ... ok
test tests::ledger::an_unreadable_document_is_an_entry_with_its_reason ... ok
test tests::ledger::two_entries_of_one_scope_offering_one_key_is_a_clash ... ok
test tests::node::the_entry_recheck_refuses_bytes_that_changed ... ok
test tests::settings::a_configuration_file_that_never_returns_is_refused ... ok
test tests::settings::an_untrusted_project_config_is_refused_at_its_read ... ok
test tests::settings::keys_inside_an_absent_optional_table_stay_absent ... ok
test tests::settings::naming_the_table_fills_the_keys_inside_it ... ok
test tests::settings::refused_settings_do_not_wedge_the_process_when_diagnostics_are_on ... ok
test tests::settings::yolo_overrides_the_configured_value_only_where_the_cartridge_declares_it ... ok
test trace::tests::a_credential_or_a_prompt_body_is_omitted_and_named ... ok
test trace::tests::a_full_diagnostics_queue_drops_records_and_says_how_many ... ok
test trace::tests::a_sink_that_cannot_repair_a_failed_write_stops_accepting_records ... ok
test trace::tests::oversized_records_are_valid_json_and_bounded_before_and_after_rotation ... ok
test trace::tests::redaction_reaches_objects_inside_nested_arrays ... ok
test trace::tests::the_sink_stays_bounded_by_rotating_one_generation ... ok
test transport::cartridge::tests::a_cancelled_call_drops_the_listener_and_frees_its_permit ... ok
test transport::cartridge::tests::a_cancelled_call_stops_a_listener_waiting_on_another_cartridge ... ok
test transport::cartridge::tests::a_cartridge_sends_a_declared_event_and_takes_the_answer ... ok
test transport::cartridge::tests::a_connection_runs_at_most_its_in_flight_limit_at_once ... ok
test transport::cartridge::tests::a_directory_update_replaces_the_schema_a_node_validates_against ... ok
test transport::cartridge::tests::a_listener_checks_what_arrives_whatever_the_sender_checked ... ok
test transport::cartridge::tests::a_listener_that_blocks_does_not_park_the_only_worker ... ok
test transport::cartridge::tests::a_listener_that_does_not_answer_reaches_the_log ... ok
test transport::cartridge::tests::a_peer_token_sends_events_and_nothing_else ... ok
test transport::cartridge::tests::a_send_reconnects_after_the_listener_restarts ... ok
test transport::cartridge::tests::a_subscriber_gets_the_replay_and_then_live_events ... ok
test transport::cartridge::tests::an_undeclared_event_or_a_bad_payload_is_refused_before_sending ... ok
test transport::cartridge::tests::an_unknown_token_is_refused_and_disconnected ... ok
test transport::cartridge::tests::events_reach_listeners_directly ... ok
test transport::cartridge::tests::gather_reports_every_listener_outcome ... ok
test transport::rpc::tests::a_call_gets_its_result ... ok
test transport::rpc::tests::a_request_dropped_unanswered_is_answered_with_an_internal_error ... ok
test transport::rpc::tests::an_oversized_frame_closes_a_capped_connection ... ok
test transport::rpc::tests::calls_run_concurrently_and_match_by_id ... ok
test transport::rpc::tests::closing_fails_waiting_calls ... ok
test transport::rpc::tests::dropping_the_last_handle_closes_the_connection ... ok
test transport::rpc::tests::errors_cross_as_error_objects ... ok
test transport::rpc::tests::notifications_arrive_without_an_id ... ok
test transport::typed::bind_tests_unix::a_bound_socket_is_owner_only ... ok
test transport::typed::bind_tests_unix::a_caller_of_another_uid_is_refused_and_the_listener_keeps_serving ... ok
test transport::typed::bind_tests_unix::a_live_endpoint_served_by_another_uid_refuses_the_bind ... ok
test transport::typed::bind_tests_unix::a_live_owner_reports_already_running ... ok
test transport::typed::bind_tests_unix::a_rebound_stale_socket_is_also_owner_only ... ok
test transport::typed::bind_tests_unix::a_regular_file_squatting_the_name_is_refused_not_removed ... ok
test transport::typed::bind_tests_unix::a_socket_is_owner_only_even_under_a_permissive_umask ... ok
test transport::typed::bind_tests_unix::a_stale_socket_file_is_removed_and_rebound ... ok
test transport::typed::bind_tests_unix::a_symlink_to_a_foreign_target_refuses_the_bind ... ok
test transport::typed::owner_tests_unix::a_dangling_symlink_is_refused ... ok
test transport::typed::owner_tests_unix::a_missing_path_reads_as_absence_not_as_a_squat ... ok
test transport::typed::owner_tests_unix::a_path_owned_by_another_uid_is_refused ... ok
test transport::typed::owner_tests_unix::a_path_this_user_owns_is_accepted ... ok
test transport::typed::owner_tests_unix::a_regular_file_is_not_an_endpoint ... ok
test transport::typed::owner_tests_unix::a_symlink_to_a_foreign_target_is_refused ... ok
test transport::typed::owner_tests_unix::connect_accepts_a_socket_this_user_bound ... ok
test transport::typed::owner_tests_unix::connect_refuses_a_foreign_endpoint_before_it_connects ... ok
test transport::typed::owner_tests_unix::connect_refuses_when_the_peer_uid_differs ... ok
test transport::typed::owner_tests_unix::the_peer_check_reads_the_server_uid_and_decides_both_ways ... ok
test transport::typed::typed_tests::a_root_that_does_not_exist_yet_tags_the_same_from_every_spelling ... ok
test transport::typed::typed_tests::cwd_tag_tests::path_tag_is_stable_and_nonempty ... ok
test transport::typed::typed_tests::tests::io_error_into_codec_is_a_decode_carrying_the_original_message ... ok
test transport::typed::typed_tests::tests::rpc_error_absorbs_adapter_and_codec_via_from ... ok
test transport::typed::typed_tests::tests::serde_error_into_codec_preserves_the_serde_message ... ok
test transport::typed::typed_tests::tests_2::inproc_reader_drains_leftover_across_small_reads ... ok
test transport::typed::typed_tests::tests_3::json_decodes_multiple_frames_from_one_buffer ... ok
test transport::typed::typed_tests::tests_3::json_many_consecutive_newlines_do_not_overflow ... ok
test transport::typed::typed_tests::tests_3::json_partial_line_yields_none_until_newline ... ok
test transport::typed::typed_tests::tests_3::json_roundtrip_single_frame ... ok
test transport::typed::typed_tests::tests_3::json_tolerates_crlf_and_skips_blank_lines ... ok
test transport::typed::typed_tests::tests_4::channel_roundtrip_json_envelope ... ok
test transport::typed::typed_tests::tests_4::recv_returns_none_on_closed_adapter ... ok
test transport::typed::typed_tests::the_tag_is_the_same_before_and_after_the_root_is_created ... ok
test trust::tests::a_built_native_module_is_not_a_source_so_a_test_build_keeps_the_cartridge ... ok
test trust::tests::a_changed_file_stops_being_trusted ... ok
test trust::tests::a_deleted_project_can_still_be_untrusted ... ok
test trust::tests::a_deleted_project_is_untrusted_by_a_relative_path ... ok
test trust::tests::a_digest_is_the_files_own_sha_256 ... ok
test trust::tests::a_file_the_record_does_not_name_is_refused ... ok
test trust::tests::a_file_under_a_skipped_directory_names_the_real_dead_end ... ok
test trust::tests::a_global_config_symlinked_out_of_the_home_still_passes ... ok
test trust::tests::a_nested_record_does_not_shadow_a_fresh_outer_one ... ok
test trust::tests::a_relative_or_empty_home_is_refused_rather_than_trust_disabling ... ok
test trust::tests::a_widened_grant_untrusts_its_manifest ... ok
test trust::tests::an_untrusted_bare_lua_entry_is_refused_at_its_resolve ... ok
test trust::tests::an_untrusted_project_is_refused_until_it_is_trusted ... ok
test trust::tests::every_spelling_of_a_directory_is_one_record ... ok
test trust::tests::read_refuses_a_file_that_changed_after_it_was_trusted ... ok
test trust::tests::revoking_a_project_takes_its_nested_records ... ok
test trust::tests::the_store_is_private_to_this_user ... ok
test trust::tests::the_users_own_home_needs_no_trust ... ok
test trust::tests::the_walk_skips_build_output_and_links ... ok
test trust::tests::yolo_trusts_a_file_changed_after_the_record_but_still_lists_it_pending ... ok

test result: ok. 186 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 61.35s

     Running unittests src/main.rs (/tmp/optional-needs-target/debug/deps/cartridge-c998525886221790)

running 22 tests
test cli::host::signal_tests::a_terminate_stops_the_host ... ok
test cli::host::signal_tests::an_interrupt_is_ignored_while_a_program_holds_the_terminal ... ok
test cli::host::stdio_tests::mcp_bridge_failure_preserves_request_ids_without_replay ... ok
test cli::host::stdio_tests::mcp_bridge_keeps_notifications_silent_and_successes_intact ... ok
test cli::host::stdio_tests::only_trust_refusals_prompt_an_attach_reload ... ok
test cli::host::stdio_tests::settled_not_on_an_empty_composition ... ok
test cli::host::stdio_tests::settled_not_while_the_key_is_starting ... ok
test cli::host::stdio_tests::settled_when_nothing_is_left_starting ... ok
test cli::host::stdio_tests::settled_when_the_key_is_active ... ok
test cli::listing::tests::the_listing_follows_sends_and_marks_cycles_and_missing_listeners ... ok
test cli::manual::tests::addresses_resolve_and_search_lands_in_the_section ... ok
test cli::manual::tests::q_and_escape_exit_the_list_instead_of_being_consumed ... ok
test cli::manual::tests::scripted_keys_drive_the_real_list_loop ... ok
test cli::settings::tests::lua_keys_and_values_render_as_lua_source ... ok
test cli::setup::tests::a_file_changed_by_the_exchange_is_not_recorded ... ok
test cli::setup::tests::a_folder_in_the_way_of_a_link_is_refused ... ok
test cli::setup::tests::a_setup_or_doctor_event_the_cartridge_does_not_listen_to_is_refused ... ok
test cli::setup::tests::setup_links_the_chosen_writes_a_descriptor_the_host_reads_and_lets_a_cartridge_ask ... ok
test cli::setup::tests::setup_offers_what_it_finds_and_the_catalog_and_filters_by_subsequence ... ok
test cli::setup::tests::setup_trusts_what_it_chose_not_what_the_tree_holds ... ok
test cli::trust::tests::an_explicit_path_trusts_a_folder_that_is_neither ... ok
test cli::width::tests::fit_and_pad_count_display_cells ... ok

test result: ok. 22 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 1.70s


```
