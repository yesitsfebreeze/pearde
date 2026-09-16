---
commit: 424b64fe99933915089ddd9d52afb0218d1f0f78
spec-digests: {"spec01.md":"c742074ce7fd4c51c0c5c198331cab21f94e6ea14b67055783c45be0b7dc60c8"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/host-tests-hold-under-suite-contention/specs/spec01.md: exit 0

Command SHA-256: f94fba658d2f5241b133490b72c1a230ff88c9b6b145320daca6b1877ff1da43

```text

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/host-tests-hold-under-suite-contention/specs/spec01.md: exit 0

Command SHA-256: d6deee4789080f25caa37b6f9d3e8c297c5263b17da60d29d5c9ba8a37e3d5b1

```text
toolchain: cargo cargo-nextest bun tmux
cargo fmt --all --check
cargo clippy --workspace --all-targets
    Finished `dev` profile [unoptimized] target(s) in 0.08s
check     cartridge  pass

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/host-tests-hold-under-suite-contention/specs/spec01.md: exit 0

Command SHA-256: 866a59ce40d4e150e2e1fea51d96c2296d14e66bfaef66a7e3efb830b1e49983

```text
toolchain: cargo cargo-nextest bun tmux
cargo nextest run --workspace 
    Finished `test` profile [unoptimized] target(s) in 0.05s
────────────
 Nextest run ID 13f98a03-1b79-49c2-b433-2d336d4491c7 with nextest profile: default
    Starting 168 tests across 2 binaries
        PASS [   0.014s] (  1/168) cartridge host::plan::tests::no_node_holds_a_token_another_node_accepts_from_someone_else
        PASS [   0.014s] (  2/168) cartridge host::plan::tests::every_event_carries_its_deadline
        PASS [   0.014s] (  3/168) cartridge host::plan::tests::a_listener_accepts_each_declared_sender_for_its_events_only
        PASS [   0.014s] (  4/168) cartridge lua::tests::a_memory_limit_bounds_what_a_chunk_can_allocate
        PASS [   0.015s] (  5/168) cartridge host::socket::tests::each_run_owns_its_node_directory_and_a_dead_run_is_swept
        PASS [   0.015s] (  6/168) cartridge host::plan::tests::a_private_host_keeps_its_socket_and_ports_to_itself
        PASS [   0.015s] (  7/168) cartridge host::socket::tests::an_owner_only_directory_is_created_and_repaired
        PASS [   0.015s] (  8/168) cartridge host::plan::tests::a_cartridge_gets_listeners_only_for_what_it_defines_or_needs
        PASS [   0.015s] (  9/168) cartridge host::socket::tests::a_symlinked_socket_directory_is_refused
        PASS [   0.015s] ( 10/168) cartridge host::socket::tests::a_run_directory_is_owner_only
        PASS [   0.013s] ( 11/168) cartridge sandbox::tests::a_write_grant_names_the_canonicalized_path_and_implies_the_read
        PASS [   0.013s] ( 12/168) cartridge sandbox::tests::a_script_names_its_interpreter
        PASS [   0.014s] ( 13/168) cartridge sandbox::tests::an_empty_command_is_refused_before_launch
        PASS [   0.014s] ( 14/168) cartridge lua::tests::the_interpreter_keeps_computation_and_drops_the_machine
        PASS [   0.015s] ( 15/168) cartridge sandbox::tests::a_net_grant_turns_the_network_on_and_an_empty_one_leaves_it_off
        PASS [   0.020s] ( 16/168) cartridge lua::tests::each_file_is_evaluated_in_a_state_of_its_own
        PASS [   0.022s] ( 17/168) cartridge lua::tests::a_runaway_is_refused_and_the_state_survives
        PASS [   0.011s] ( 18/168) cartridge sandbox::tests::the_runtime_is_named_canonically
        PASS [   0.014s] ( 19/168) cartridge sandbox::tests::an_exec_grant_that_resolves_builds_a_literal_and_one_that_does_not_builds_nothing
        PASS [   0.015s] ( 20/168) cartridge sandbox::tests::an_empty_grant_builds_no_allowance_beyond_the_runtime
        PASS [   0.017s] ( 21/168) cartridge sandbox::tests::the_prefix_stops_at_a_system_directory
        PASS [   0.015s] ( 22/168) cartridge settings::files::tests::the_listing_reads_each_configuration_file_once
        PASS [   0.015s] ( 23/168) cartridge settings::host::tests::an_undeclared_host_key_leaves_the_declared_defaults_standing
        PASS [   0.046s] ( 24/168) cartridge lua::tests::a_wait_refills_the_budget_and_a_coroutine_does_not
        PASS [   0.052s] ( 25/168) cartridge lua::tests::every_resume_gets_the_budget_back
        PASS [   0.021s] ( 26/168) cartridge tests::host::a_document_refuses_a_bad_schema_or_a_contract_it_does_not_listen_to
        PASS [   0.255s] ( 27/168) cartridge sandbox::tests::an_async_spawn_is_confined_like_the_synchronous_one
        PASS [   0.339s] ( 28/168) cartridge sandbox::tests::an_interpreter_reaches_its_own_installation
        PASS [   0.008s] ( 29/168) cartridge tests::host::a_lifecycle_subscriber_that_falls_behind_is_disconnected
        PASS [   0.113s] ( 30/168) cartridge tests::host::a_missing_listener_waits_and_says_for_what
        PASS [   0.536s] ( 31/168) cartridge sandbox::tests::the_synchronous_command_enforces_the_empty_grant
        PASS [   0.859s] ( 32/168) cartridge tests::host::a_node_presenting_its_own_credential_is_refused_on_the_host_socket
        PASS [   1.427s] ( 33/168) cartridge tests::host::a_call_that_comes_back_into_its_sender_is_answered
        PASS [   1.425s] ( 34/168) cartridge tests::host::a_cartridge_asks_the_host_what_only_the_host_knows
        PASS [   1.410s] ( 35/168) cartridge tests::host::a_granted_env_prefix_reaches_the_node_and_nothing_beside_it_does
        PASS [   1.443s] ( 36/168) cartridge tests::host::a_cartridge_sends_only_what_it_defines_or_needs
        PASS [   1.435s] ( 37/168) cartridge tests::host::a_glob_in_needs_names_what_the_others_listen_to
        PASS [   1.480s] ( 38/168) cartridge tests::host::a_cartridge_answers_the_events_it_listens_to
        PASS [   1.456s] ( 39/168) cartridge tests::host::a_helper_asks_the_base_while_answering
        PASS [   1.143s] ( 40/168) cartridge tests::host::a_native_module_reaches_the_base_through_the_global
        PASS [   1.508s] ( 41/168) cartridge tests::host::a_hung_listener_times_out_and_its_node_keeps_serving
        PASS [   1.099s] ( 42/168) cartridge tests::host::a_node_refuses_to_listen_to_what_it_did_not_declare
        PASS [   0.996s] ( 43/168) cartridge tests::host::a_spawn_the_grant_did_not_name_is_denied
        PASS [   1.057s] ( 44/168) cartridge tests::host::a_payload_the_schema_rejects_never_reaches_the_listener
        PASS [   0.759s] ( 45/168) cartridge tests::host::a_spawned_program_answers_requests_by_id
        PASS [   0.909s] ( 46/168) cartridge tests::host::a_spawned_helper_sees_only_the_two_named_cartridge_variables_and_a_path
        PASS [   1.069s] ( 47/168) cartridge tests::host::a_pipe_wakes_the_node_from_outside
        PASS [   1.068s] ( 48/168) cartridge tests::host::a_schema_only_change_reaches_a_sender_that_already_validated
        PASS [   1.102s] ( 49/168) cartridge tests::host::a_restart_keeps_its_dependents_working
        PASS [   0.011s] ( 50/168) cartridge tests::host::an_untrusted_descriptor_is_refused_where_it_is_enforced
        PASS [   0.751s] ( 51/168) cartridge tests::host::an_undeclared_event_fails_the_cartridge_before_it_starts
        PASS [   0.014s] ( 52/168) cartridge tests::host::grant_paths_name_the_project_and_settings
        PASS [   1.184s] ( 53/168) cartridge tests::host::an_event_declared_twice_fails_the_later_entry
        PASS [   1.151s] ( 54/168) cartridge tests::host::gather_and_emit_reach_every_listener
        PASS [   0.015s] ( 55/168) cartridge tests::host::solo_entries_sharing_a_socket_name_are_refused
        PASS [   1.267s] ( 56/168) cartridge tests::host::a_stop_request_ends_a_foreground_run
        PASS [   1.271s] ( 57/168) cartridge tests::host::a_stopped_cartridge_takes_its_programs_along
        PASS [   0.011s] ( 58/168) cartridge tests::ledger::a_root_that_does_not_exist_is_an_empty_ledger
        PASS [   0.012s] ( 59/168) cartridge tests::ledger::an_entry_is_its_path_from_the_root
        PASS [   0.011s] ( 60/168) cartridge tests::ledger::an_unreadable_document_is_an_entry_with_its_reason
        PASS [   0.010s] ( 61/168) cartridge tests::ledger::two_entries_of_one_scope_offering_one_key_is_a_clash
        PASS [   0.009s] ( 62/168) cartridge tests::node::the_entry_recheck_refuses_bytes_that_changed
        PASS [   0.708s] ( 63/168) cartridge tests::host::one_cartridge_cannot_see_anothers_globals
        PASS [   0.011s] ( 64/168) cartridge tests::settings::an_untrusted_project_config_is_refused_at_its_read
        PASS [   0.007s] ( 65/168) cartridge tests::settings::keys_inside_an_absent_optional_table_stay_absent
        PASS [   0.009s] ( 66/168) cartridge tests::settings::naming_the_table_fills_the_keys_inside_it
        PASS [   1.061s] ( 67/168) cartridge tests::host::verify_sends_every_declared_contract
        PASS [   1.098s] ( 68/168) cartridge tests::host::the_host_socket_answers_the_command_line
        PASS [   0.011s] ( 69/168) cartridge trace::tests::a_credential_or_a_prompt_body_is_omitted_and_named
        PASS [   0.013s] ( 70/168) cartridge tests::settings::yolo_overrides_the_configured_value_only_where_the_cartridge_declares_it
        PASS [   1.117s] ( 71/168) cartridge tests::host::streams_replay_and_then_deliver_live
        PASS [   0.014s] ( 72/168) cartridge trace::tests::a_full_diagnostics_queue_drops_records_and_says_how_many
        PASS [   0.014s] ( 73/168) cartridge trace::tests::a_sink_that_cannot_repair_a_failed_write_stops_accepting_records
        PASS [   0.795s] ( 74/168) cartridge tests::settings::refused_settings_do_not_wedge_the_process_when_diagnostics_are_on
        PASS [   0.012s] ( 75/168) cartridge trace::tests::oversized_records_are_valid_json_and_bounded_before_and_after_rotation
        PASS [   0.015s] ( 76/168) cartridge trace::tests::redaction_reaches_objects_inside_nested_arrays
        PASS [   2.366s] ( 77/168) cartridge tests::host::a_waiting_cartridge_starts_when_the_descriptor_adds_its_listener
        PASS [   0.027s] ( 78/168) cartridge trace::tests::the_sink_stays_bounded_by_rotating_one_generation
        PASS [   0.028s] ( 79/168) cartridge transport::cartridge::tests::a_cartridge_sends_a_declared_event_and_takes_the_answer
        PASS [   0.019s] ( 80/168) cartridge transport::cartridge::tests::a_listener_checks_what_arrives_whatever_the_sender_checked
        PASS [   0.014s] ( 81/168) cartridge transport::cartridge::tests::a_peer_token_sends_events_and_nothing_else
        PASS [   0.035s] ( 82/168) cartridge transport::cartridge::tests::a_directory_update_replaces_the_schema_a_node_validates_against
        PASS [   0.012s] ( 83/168) cartridge transport::cartridge::tests::a_subscriber_gets_the_replay_and_then_live_events
        PASS [   0.012s] ( 84/168) cartridge transport::cartridge::tests::an_unknown_token_is_refused_and_disconnected
        PASS [   0.021s] ( 85/168) cartridge transport::cartridge::tests::an_undeclared_event_or_a_bad_payload_is_refused_before_sending
        PASS [   0.015s] ( 86/168) cartridge transport::cartridge::tests::events_reach_listeners_directly
        PASS [   0.015s] ( 87/168) cartridge transport::rpc::tests::a_call_gets_its_result
        PASS [   0.010s] ( 88/168) cartridge transport::rpc::tests::a_request_dropped_unanswered_is_answered_with_an_internal_error
        PASS [   0.077s] ( 89/168) cartridge transport::cartridge::tests::a_connection_runs_at_most_its_in_flight_limit_at_once
        PASS [   0.015s] ( 90/168) cartridge transport::rpc::tests::an_oversized_frame_closes_a_capped_connection
        PASS [   0.024s] ( 91/168) cartridge transport::rpc::tests::closing_fails_waiting_calls
        PASS [   0.012s] ( 92/168) cartridge transport::rpc::tests::dropping_the_last_handle_closes_the_connection
        PASS [   0.013s] ( 93/168) cartridge transport::rpc::tests::errors_cross_as_error_objects
        PASS [   0.015s] ( 94/168) cartridge transport::rpc::tests::notifications_arrive_without_an_id
        PASS [   0.013s] ( 95/168) cartridge transport::typed::bind_tests_unix::a_bound_socket_is_owner_only
        PASS [   0.012s] ( 96/168) cartridge transport::typed::bind_tests_unix::a_live_endpoint_served_by_another_uid_refuses_the_bind
        PASS [   0.067s] ( 97/168) cartridge transport::rpc::tests::calls_run_concurrently_and_match_by_id
        PASS [   0.011s] ( 98/168) cartridge transport::typed::bind_tests_unix::a_live_owner_reports_already_running
        PASS [   0.011s] ( 99/168) cartridge transport::typed::bind_tests_unix::a_rebound_stale_socket_is_also_owner_only
        PASS [   0.010s] (100/168) cartridge transport::typed::bind_tests_unix::a_regular_file_squatting_the_name_is_refused_not_removed
        PASS [   0.009s] (101/168) cartridge transport::typed::bind_tests_unix::a_socket_is_owner_only_even_under_a_permissive_umask
        PASS [   0.012s] (102/168) cartridge transport::typed::bind_tests_unix::a_stale_socket_file_is_removed_and_rebound
        PASS [   0.009s] (103/168) cartridge transport::typed::bind_tests_unix::a_symlink_to_a_foreign_target_refuses_the_bind
        PASS [   0.010s] (104/168) cartridge transport::typed::owner_tests_unix::a_missing_path_reads_as_absence_not_as_a_squat
        PASS [   0.011s] (105/168) cartridge transport::typed::owner_tests_unix::a_dangling_symlink_is_refused
        PASS [   0.163s] (106/168) cartridge transport::cartridge::tests::a_send_reconnects_after_the_listener_restarts
        PASS [   0.012s] (107/168) cartridge transport::typed::owner_tests_unix::a_path_owned_by_another_uid_is_refused
        PASS [   0.013s] (108/168) cartridge transport::typed::owner_tests_unix::a_path_this_user_owns_is_accepted
        PASS [   0.012s] (109/168) cartridge transport::typed::owner_tests_unix::a_regular_file_is_not_an_endpoint
        PASS [   0.012s] (110/168) cartridge transport::typed::owner_tests_unix::a_symlink_to_a_foreign_target_is_refused
        PASS [   0.010s] (111/168) cartridge transport::typed::owner_tests_unix::connect_accepts_a_socket_this_user_bound
        PASS [   0.010s] (112/168) cartridge transport::typed::owner_tests_unix::connect_refuses_a_foreign_endpoint_before_it_connects
        PASS [   0.010s] (113/168) cartridge transport::typed::owner_tests_unix::the_peer_check_reads_the_server_uid_and_decides_both_ways
        PASS [   0.013s] (114/168) cartridge transport::typed::owner_tests_unix::connect_refuses_when_the_peer_uid_differs
        PASS [   0.010s] (115/168) cartridge transport::typed::typed_tests::a_root_that_does_not_exist_yet_tags_the_same_from_every_spelling
        PASS [   0.012s] (116/168) cartridge transport::typed::typed_tests::cwd_tag_tests::path_tag_is_stable_and_nonempty
        PASS [   0.011s] (117/168) cartridge transport::typed::typed_tests::tests::io_error_into_codec_is_a_decode_carrying_the_original_message
        PASS [   0.010s] (118/168) cartridge transport::typed::typed_tests::tests::rpc_error_absorbs_adapter_and_codec_via_from
        PASS [   0.010s] (119/168) cartridge transport::typed::typed_tests::tests::serde_error_into_codec_preserves_the_serde_message
        PASS [   0.011s] (120/168) cartridge transport::typed::typed_tests::tests_2::inproc_reader_drains_leftover_across_small_reads
        PASS [   0.009s] (121/168) cartridge transport::typed::typed_tests::tests_3::json_decodes_multiple_frames_from_one_buffer
        PASS [   0.010s] (122/168) cartridge transport::typed::typed_tests::tests_3::json_partial_line_yields_none_until_newline
        PASS [   0.014s] (123/168) cartridge transport::typed::typed_tests::tests_3::json_many_consecutive_newlines_do_not_overflow
        PASS [   0.010s] (124/168) cartridge transport::typed::typed_tests::tests_3::json_roundtrip_single_frame
        PASS [   0.009s] (125/168) cartridge transport::typed::typed_tests::tests_4::channel_roundtrip_json_envelope
        PASS [   0.011s] (126/168) cartridge transport::typed::typed_tests::tests_3::json_tolerates_crlf_and_skips_blank_lines
        PASS [   0.009s] (127/168) cartridge transport::typed::typed_tests::tests_4::recv_returns_none_on_closed_adapter
        PASS [   0.013s] (128/168) cartridge transport::typed::typed_tests::the_tag_is_the_same_before_and_after_the_root_is_created
        PASS [   0.012s] (129/168) cartridge trust::tests::a_changed_file_stops_being_trusted
        PASS [   0.216s] (130/168) cartridge transport::cartridge::tests::gather_reports_every_listener_outcome
        PASS [   0.017s] (131/168) cartridge trust::tests::a_deleted_project_can_still_be_untrusted
        PASS [   0.013s] (132/168) cartridge trust::tests::a_file_the_record_does_not_name_is_refused
        PASS [   0.013s] (133/168) cartridge trust::tests::a_digest_is_the_files_own_sha_256
        PASS [   0.017s] (134/168) cartridge trust::tests::a_file_under_a_skipped_directory_names_the_real_dead_end
        PASS [   0.014s] (135/168) cartridge trust::tests::a_nested_record_does_not_shadow_a_fresh_outer_one
        PASS [   0.016s] (136/168) cartridge trust::tests::a_global_config_symlinked_out_of_the_home_still_passes
        PASS [   0.014s] (137/168) cartridge trust::tests::a_widened_grant_untrusts_its_manifest
        PASS [   0.016s] (138/168) cartridge trust::tests::an_untrusted_bare_lua_entry_is_refused_at_its_resolve
        PASS [   0.017s] (139/168) cartridge trust::tests::every_spelling_of_a_directory_is_one_record
        PASS [   0.023s] (140/168) cartridge trust::tests::an_untrusted_project_is_refused_until_it_is_trusted
        PASS [   0.014s] (141/168) cartridge trust::tests::read_refuses_a_file_that_changed_after_it_was_trusted
        PASS [   0.017s] (142/168) cartridge trust::tests::revoking_a_project_takes_its_nested_records
        PASS [   0.018s] (143/168) cartridge trust::tests::the_store_is_private_to_this_user
        PASS [   0.014s] (144/168) cartridge trust::tests::the_users_own_home_needs_no_trust
        PASS [   0.266s] (145/168) cartridge transport::typed::bind_tests_unix::a_caller_of_another_uid_is_refused_and_the_listener_keeps_serving
        PASS [   0.017s] (146/168) cartridge trust::tests::the_walk_skips_build_output_and_links
        PASS [   0.011s] (147/168) cartridge::bin/cartridge cli::host::stdio_tests::mcp_bridge_failure_preserves_request_ids_without_replay
        PASS [   0.019s] (148/168) cartridge::bin/cartridge cli::host::stdio_tests::mcp_bridge_keeps_notifications_silent_and_successes_intact
        PASS [   0.018s] (149/168) cartridge::bin/cartridge cli::listing::tests::the_listing_follows_sends_and_marks_cycles_and_missing_listeners
        PASS [   0.014s] (150/168) cartridge::bin/cartridge cli::manual::tests::addresses_resolve_and_search_lands_in_the_section
        PASS [   0.020s] (151/168) cartridge::bin/cartridge cli::settings::tests::lua_keys_and_values_render_as_lua_source
        PASS [   0.115s] (152/168) cartridge::bin/cartridge cli::host::signal_tests::a_terminate_stops_the_host
        PASS [   0.020s] (153/168) cartridge::bin/cartridge cli::setup::tests::a_file_changed_by_the_exchange_is_not_recorded
        PASS [   0.012s] (154/168) cartridge::bin/cartridge cli::setup::tests::a_folder_in_the_way_of_a_link_is_refused
        PASS [   0.015s] (155/168) cartridge::bin/cartridge cli::setup::tests::a_setup_or_doctor_event_the_cartridge_does_not_listen_to_is_refused
        PASS [   0.015s] (156/168) cartridge::bin/cartridge cli::setup::tests::setup_offers_what_it_finds_and_the_catalog_and_filters_by_subsequence
        PASS [   0.022s] (157/168) cartridge::bin/cartridge cli::setup::tests::setup_trusts_what_it_chose_not_what_the_tree_holds
        PASS [   0.016s] (158/168) cartridge::bin/cartridge cli::trust::tests::an_explicit_path_trusts_a_folder_that_is_neither
        PASS [   0.013s] (159/168) cartridge::bin/cartridge cli::width::tests::fit_and_pad_count_display_cells
        PASS [   4.067s] (160/168) cartridge tests::host::a_node_serves_other_events_while_a_handler_waits
        PASS [   0.319s] (161/168) cartridge::bin/cartridge cli::host::signal_tests::an_interrupt_is_ignored_while_a_program_holds_the_terminal
        PASS [   1.745s] (162/168) cartridge trust::tests::a_deleted_project_is_untrusted_by_a_relative_path
        PASS [   1.735s] (163/168) cartridge trust::tests::a_relative_or_empty_home_is_refused_rather_than_trust_disabling
        PASS [   1.560s] (164/168) cartridge::bin/cartridge cli::setup::tests::setup_links_the_chosen_writes_a_descriptor_the_host_reads_and_lets_a_cartridge_ask
        PASS [   4.459s] (165/168) cartridge tests::host::a_terminated_mcp_exits_with_its_input_still_open
        PASS [   7.126s] (166/168) cartridge tests::host::a_node_that_catches_its_own_refusal_exits
        PASS [   7.070s] (167/168) cartridge tests::host::a_spinning_handler_is_refused_and_its_node_keeps_serving
        PASS [   5.882s] (168/168) cartridge tests::settings::a_configuration_file_that_never_returns_is_refused
────────────
     Summary [   9.741s] 168 tests run: 168 passed, 0 skipped
test      cartridge  pass

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/host-tests-hold-under-suite-contention/specs/spec01.md: exit 0

Command SHA-256: 866a59ce40d4e150e2e1fea51d96c2296d14e66bfaef66a7e3efb830b1e49983

```text
toolchain: cargo cargo-nextest bun tmux
cargo nextest run --workspace 
    Finished `test` profile [unoptimized] target(s) in 0.05s
────────────
 Nextest run ID 65db55b3-dcb3-4eaf-89af-d94890e845d1 with nextest profile: default
    Starting 168 tests across 2 binaries
        PASS [   0.010s] (  1/168) cartridge host::plan::tests::a_listener_accepts_each_declared_sender_for_its_events_only
        PASS [   0.011s] (  2/168) cartridge host::socket::tests::a_symlinked_socket_directory_is_refused
        PASS [   0.013s] (  3/168) cartridge host::plan::tests::a_cartridge_gets_listeners_only_for_what_it_defines_or_needs
        PASS [   0.013s] (  4/168) cartridge lua::tests::a_memory_limit_bounds_what_a_chunk_can_allocate
        PASS [   0.013s] (  5/168) cartridge host::socket::tests::a_run_directory_is_owner_only
        PASS [   0.013s] (  6/168) cartridge host::plan::tests::a_private_host_keeps_its_socket_and_ports_to_itself
        PASS [   0.014s] (  7/168) cartridge host::plan::tests::no_node_holds_a_token_another_node_accepts_from_someone_else
        PASS [   0.014s] (  8/168) cartridge host::socket::tests::an_owner_only_directory_is_created_and_repaired
        PASS [   0.014s] (  9/168) cartridge host::plan::tests::every_event_carries_its_deadline
        PASS [   0.014s] ( 10/168) cartridge host::socket::tests::each_run_owns_its_node_directory_and_a_dead_run_is_swept
        PASS [   0.010s] ( 11/168) cartridge lua::tests::the_interpreter_keeps_computation_and_drops_the_machine
        PASS [   0.011s] ( 12/168) cartridge sandbox::tests::a_script_names_its_interpreter
        PASS [   0.011s] ( 13/168) cartridge sandbox::tests::a_write_grant_names_the_canonicalized_path_and_implies_the_read
        PASS [   0.012s] ( 14/168) cartridge sandbox::tests::an_empty_command_is_refused_before_launch
        PASS [   0.013s] ( 15/168) cartridge sandbox::tests::a_net_grant_turns_the_network_on_and_an_empty_one_leaves_it_off
        PASS [   0.018s] ( 16/168) cartridge lua::tests::each_file_is_evaluated_in_a_state_of_its_own
        PASS [   0.022s] ( 17/168) cartridge lua::tests::a_runaway_is_refused_and_the_state_survives
        PASS [   0.012s] ( 18/168) cartridge sandbox::tests::an_empty_grant_builds_no_allowance_beyond_the_runtime
        PASS [   0.014s] ( 19/168) cartridge sandbox::tests::an_exec_grant_that_resolves_builds_a_literal_and_one_that_does_not_builds_nothing
        PASS [   0.015s] ( 20/168) cartridge sandbox::tests::the_prefix_stops_at_a_system_directory
        PASS [   0.015s] ( 21/168) cartridge sandbox::tests::the_runtime_is_named_canonically
        PASS [   0.016s] ( 22/168) cartridge settings::files::tests::the_listing_reads_each_configuration_file_once
        PASS [   0.038s] ( 23/168) cartridge lua::tests::a_wait_refills_the_budget_and_a_coroutine_does_not
        PASS [   0.014s] ( 24/168) cartridge settings::host::tests::an_undeclared_host_key_leaves_the_declared_defaults_standing
        PASS [   0.022s] ( 25/168) cartridge tests::host::a_document_refuses_a_bad_schema_or_a_contract_it_does_not_listen_to
        PASS [   0.061s] ( 26/168) cartridge lua::tests::every_resume_gets_the_budget_back
        PASS [   0.244s] ( 27/168) cartridge sandbox::tests::an_async_spawn_is_confined_like_the_synchronous_one
        PASS [   0.333s] ( 28/168) cartridge sandbox::tests::an_interpreter_reaches_its_own_installation
        PASS [   0.009s] ( 29/168) cartridge tests::host::a_lifecycle_subscriber_that_falls_behind_is_disconnected
        PASS [   0.183s] ( 30/168) cartridge tests::host::a_missing_listener_waits_and_says_for_what
        PASS [   0.532s] ( 31/168) cartridge sandbox::tests::the_synchronous_command_enforces_the_empty_grant
        PASS [   0.833s] ( 32/168) cartridge tests::host::a_node_presenting_its_own_credential_is_refused_on_the_host_socket
        PASS [   1.398s] ( 33/168) cartridge tests::host::a_call_that_comes_back_into_its_sender_is_answered
        PASS [   1.400s] ( 34/168) cartridge tests::host::a_cartridge_asks_the_host_what_only_the_host_knows
        PASS [   1.373s] ( 35/168) cartridge tests::host::a_granted_env_prefix_reaches_the_node_and_nothing_beside_it_does
        PASS [   1.407s] ( 36/168) cartridge tests::host::a_cartridge_sends_only_what_it_defines_or_needs
        PASS [   1.417s] ( 37/168) cartridge tests::host::a_glob_in_needs_names_what_the_others_listen_to
        PASS [   1.448s] ( 38/168) cartridge tests::host::a_cartridge_answers_the_events_it_listens_to
        PASS [   1.420s] ( 39/168) cartridge tests::host::a_helper_asks_the_base_while_answering
        PASS [   1.063s] ( 40/168) cartridge tests::host::a_native_module_reaches_the_base_through_the_global
        PASS [   1.486s] ( 41/168) cartridge tests::host::a_hung_listener_times_out_and_its_node_keeps_serving
        PASS [   1.125s] ( 42/168) cartridge tests::host::a_payload_the_schema_rejects_never_reaches_the_listener
        PASS [   1.183s] ( 43/168) cartridge tests::host::a_node_refuses_to_listen_to_what_it_did_not_declare
        PASS [   0.836s] ( 44/168) cartridge tests::host::a_spawned_program_answers_requests_by_id
        PASS [   1.085s] ( 45/168) cartridge tests::host::a_spawn_the_grant_did_not_name_is_denied
        PASS [   1.132s] ( 46/168) cartridge tests::host::a_pipe_wakes_the_node_from_outside
        PASS [   1.102s] ( 47/168) cartridge tests::host::a_schema_only_change_reaches_a_sender_that_already_validated
        PASS [   0.981s] ( 48/168) cartridge tests::host::a_spawned_helper_sees_only_the_two_named_cartridge_variables_and_a_path
        PASS [   1.191s] ( 49/168) cartridge tests::host::a_restart_keeps_its_dependents_working
        PASS [   0.014s] ( 50/168) cartridge tests::host::an_untrusted_descriptor_is_refused_where_it_is_enforced
        PASS [   0.825s] ( 51/168) cartridge tests::host::an_undeclared_event_fails_the_cartridge_before_it_starts
        PASS [   0.020s] ( 52/168) cartridge tests::host::grant_paths_name_the_project_and_settings
        PASS [   1.228s] ( 53/168) cartridge tests::host::a_stop_request_ends_a_foreground_run
        PASS [   1.138s] ( 54/168) cartridge tests::host::gather_and_emit_reach_every_listener
        PASS [   0.376s] ( 55/168) cartridge tests::host::one_cartridge_cannot_see_anothers_globals
        PASS [   1.227s] ( 56/168) cartridge tests::host::an_event_declared_twice_fails_the_later_entry
        PASS [   0.015s] ( 57/168) cartridge tests::host::solo_entries_sharing_a_socket_name_are_refused
        PASS [   0.011s] ( 58/168) cartridge tests::ledger::a_root_that_does_not_exist_is_an_empty_ledger
        PASS [   0.012s] ( 59/168) cartridge tests::ledger::an_entry_is_its_path_from_the_root
        PASS [   0.010s] ( 60/168) cartridge tests::ledger::an_unreadable_document_is_an_entry_with_its_reason
        PASS [   1.287s] ( 61/168) cartridge tests::host::a_stopped_cartridge_takes_its_programs_along
        PASS [   0.012s] ( 62/168) cartridge tests::ledger::two_entries_of_one_scope_offering_one_key_is_a_clash
        PASS [   0.010s] ( 63/168) cartridge tests::node::the_entry_recheck_refuses_bytes_that_changed
        PASS [   1.299s] ( 64/168) cartridge tests::host::a_waiting_cartridge_starts_when_the_descriptor_adds_its_listener
        PASS [   0.011s] ( 65/168) cartridge tests::settings::an_untrusted_project_config_is_refused_at_its_read
        PASS [   0.011s] ( 66/168) cartridge tests::settings::naming_the_table_fills_the_keys_inside_it
        PASS [   0.012s] ( 67/168) cartridge tests::settings::keys_inside_an_absent_optional_table_stay_absent
        PASS [   0.011s] ( 68/168) cartridge tests::settings::yolo_overrides_the_configured_value_only_where_the_cartridge_declares_it
        PASS [   0.011s] ( 69/168) cartridge trace::tests::a_credential_or_a_prompt_body_is_omitted_and_named
        PASS [   0.012s] ( 70/168) cartridge trace::tests::a_full_diagnostics_queue_drops_records_and_says_how_many
        PASS [   0.013s] ( 71/168) cartridge trace::tests::a_sink_that_cannot_repair_a_failed_write_stops_accepting_records
        PASS [   0.013s] ( 72/168) cartridge trace::tests::oversized_records_are_valid_json_and_bounded_before_and_after_rotation
        PASS [   0.012s] ( 73/168) cartridge trace::tests::redaction_reaches_objects_inside_nested_arrays
        PASS [   0.030s] ( 74/168) cartridge trace::tests::the_sink_stays_bounded_by_rotating_one_generation
        PASS [   0.021s] ( 75/168) cartridge transport::cartridge::tests::a_cartridge_sends_a_declared_event_and_takes_the_answer
        PASS [   0.066s] ( 76/168) cartridge transport::cartridge::tests::a_connection_runs_at_most_its_in_flight_limit_at_once
        PASS [   0.021s] ( 77/168) cartridge transport::cartridge::tests::a_directory_update_replaces_the_schema_a_node_validates_against
        PASS [   0.021s] ( 78/168) cartridge transport::cartridge::tests::a_listener_checks_what_arrives_whatever_the_sender_checked
        PASS [   0.015s] ( 79/168) cartridge transport::cartridge::tests::a_peer_token_sends_events_and_nothing_else
        PASS [   0.166s] ( 80/168) cartridge transport::cartridge::tests::a_send_reconnects_after_the_listener_restarts
        PASS [   0.011s] ( 81/168) cartridge transport::cartridge::tests::a_subscriber_gets_the_replay_and_then_live_events
        PASS [   0.014s] ( 82/168) cartridge transport::cartridge::tests::an_undeclared_event_or_a_bad_payload_is_refused_before_sending
        PASS [   0.013s] ( 83/168) cartridge transport::cartridge::tests::an_unknown_token_is_refused_and_disconnected
        PASS [   0.013s] ( 84/168) cartridge transport::cartridge::tests::events_reach_listeners_directly
        PASS [   0.210s] ( 85/168) cartridge transport::cartridge::tests::gather_reports_every_listener_outcome
        PASS [   0.012s] ( 86/168) cartridge transport::rpc::tests::a_call_gets_its_result
        PASS [   0.010s] ( 87/168) cartridge transport::rpc::tests::a_request_dropped_unanswered_is_answered_with_an_internal_error
        PASS [   0.010s] ( 88/168) cartridge transport::rpc::tests::an_oversized_frame_closes_a_capped_connection
        PASS [   0.061s] ( 89/168) cartridge transport::rpc::tests::calls_run_concurrently_and_match_by_id
        PASS [   0.022s] ( 90/168) cartridge transport::rpc::tests::closing_fails_waiting_calls
        PASS [   0.010s] ( 91/168) cartridge transport::rpc::tests::dropping_the_last_handle_closes_the_connection
        PASS [   0.010s] ( 92/168) cartridge transport::rpc::tests::errors_cross_as_error_objects
        PASS [   0.009s] ( 93/168) cartridge transport::rpc::tests::notifications_arrive_without_an_id
        PASS [   0.010s] ( 94/168) cartridge transport::typed::bind_tests_unix::a_bound_socket_is_owner_only
        PASS [   1.113s] ( 95/168) cartridge tests::host::verify_sends_every_declared_contract
        PASS [   0.011s] ( 96/168) cartridge transport::typed::bind_tests_unix::a_live_endpoint_served_by_another_uid_refuses_the_bind
        PASS [   0.012s] ( 97/168) cartridge transport::typed::bind_tests_unix::a_live_owner_reports_already_running
        PASS [   1.143s] ( 98/168) cartridge tests::host::the_host_socket_answers_the_command_line
        PASS [   0.013s] ( 99/168) cartridge transport::typed::bind_tests_unix::a_rebound_stale_socket_is_also_owner_only
        PASS [   0.013s] (100/168) cartridge transport::typed::bind_tests_unix::a_regular_file_squatting_the_name_is_refused_not_removed
        PASS [   1.166s] (101/168) cartridge tests::host::streams_replay_and_then_deliver_live
        PASS [   0.013s] (102/168) cartridge transport::typed::bind_tests_unix::a_socket_is_owner_only_even_under_a_permissive_umask
        PASS [   0.010s] (103/168) cartridge transport::typed::bind_tests_unix::a_stale_socket_file_is_removed_and_rebound
        PASS [   1.084s] (104/168) cartridge tests::settings::refused_settings_do_not_wedge_the_process_when_diagnostics_are_on
        PASS [   0.010s] (105/168) cartridge transport::typed::bind_tests_unix::a_symlink_to_a_foreign_target_refuses_the_bind
        PASS [   0.263s] (106/168) cartridge transport::typed::bind_tests_unix::a_caller_of_another_uid_is_refused_and_the_listener_keeps_serving
        PASS [   0.011s] (107/168) cartridge transport::typed::owner_tests_unix::a_missing_path_reads_as_absence_not_as_a_squat
        PASS [   0.013s] (108/168) cartridge transport::typed::owner_tests_unix::a_dangling_symlink_is_refused
        PASS [   0.012s] (109/168) cartridge transport::typed::owner_tests_unix::a_path_owned_by_another_uid_is_refused
        PASS [   0.011s] (110/168) cartridge transport::typed::owner_tests_unix::a_path_this_user_owns_is_accepted
        PASS [   0.010s] (111/168) cartridge transport::typed::owner_tests_unix::connect_accepts_a_socket_this_user_bound
        PASS [   0.013s] (112/168) cartridge transport::typed::owner_tests_unix::a_symlink_to_a_foreign_target_is_refused
        PASS [   0.010s] (113/168) cartridge transport::typed::owner_tests_unix::connect_refuses_a_foreign_endpoint_before_it_connects
        PASS [   0.015s] (114/168) cartridge transport::typed::owner_tests_unix::a_regular_file_is_not_an_endpoint
        PASS [   0.011s] (115/168) cartridge transport::typed::owner_tests_unix::connect_refuses_when_the_peer_uid_differs
        PASS [   0.011s] (116/168) cartridge transport::typed::typed_tests::cwd_tag_tests::path_tag_is_stable_and_nonempty
        PASS [   0.011s] (117/168) cartridge transport::typed::typed_tests::tests::io_error_into_codec_is_a_decode_carrying_the_original_message
        PASS [   0.011s] (118/168) cartridge transport::typed::typed_tests::a_root_that_does_not_exist_yet_tags_the_same_from_every_spelling
        PASS [   0.013s] (119/168) cartridge transport::typed::owner_tests_unix::the_peer_check_reads_the_server_uid_and_decides_both_ways
        PASS [   0.011s] (120/168) cartridge transport::typed::typed_tests::tests::rpc_error_absorbs_adapter_and_codec_via_from
        PASS [   0.008s] (121/168) cartridge transport::typed::typed_tests::tests_2::inproc_reader_drains_leftover_across_small_reads
        PASS [   0.010s] (122/168) cartridge transport::typed::typed_tests::tests_3::json_decodes_multiple_frames_from_one_buffer
        PASS [   0.012s] (123/168) cartridge transport::typed::typed_tests::tests::serde_error_into_codec_preserves_the_serde_message
        PASS [   0.009s] (124/168) cartridge transport::typed::typed_tests::tests_3::json_partial_line_yields_none_until_newline
        PASS [   0.015s] (125/168) cartridge transport::typed::typed_tests::tests_3::json_many_consecutive_newlines_do_not_overflow
        PASS [   0.007s] (126/168) cartridge transport::typed::typed_tests::tests_3::json_roundtrip_single_frame
        PASS [   0.009s] (127/168) cartridge transport::typed::typed_tests::tests_3::json_tolerates_crlf_and_skips_blank_lines
        PASS [   0.008s] (128/168) cartridge transport::typed::typed_tests::tests_4::channel_roundtrip_json_envelope
        PASS [   0.008s] (129/168) cartridge transport::typed::typed_tests::tests_4::recv_returns_none_on_closed_adapter
        PASS [   0.009s] (130/168) cartridge trust::tests::a_changed_file_stops_being_trusted
        PASS [   0.010s] (131/168) cartridge transport::typed::typed_tests::the_tag_is_the_same_before_and_after_the_root_is_created
        PASS [   0.012s] (132/168) cartridge trust::tests::a_digest_is_the_files_own_sha_256
        PASS [   0.014s] (133/168) cartridge trust::tests::a_deleted_project_can_still_be_untrusted
        PASS [   0.014s] (134/168) cartridge trust::tests::a_file_the_record_does_not_name_is_refused
        PASS [   0.014s] (135/168) cartridge trust::tests::a_file_under_a_skipped_directory_names_the_real_dead_end
        PASS [   0.015s] (136/168) cartridge trust::tests::a_global_config_symlinked_out_of_the_home_still_passes
        PASS [   0.017s] (137/168) cartridge trust::tests::a_nested_record_does_not_shadow_a_fresh_outer_one
        PASS [   0.017s] (138/168) cartridge trust::tests::a_widened_grant_untrusts_its_manifest
        PASS [   0.016s] (139/168) cartridge trust::tests::an_untrusted_bare_lua_entry_is_refused_at_its_resolve
        PASS [   0.016s] (140/168) cartridge trust::tests::an_untrusted_project_is_refused_until_it_is_trusted
        PASS [   0.014s] (141/168) cartridge trust::tests::every_spelling_of_a_directory_is_one_record
        PASS [   0.018s] (142/168) cartridge trust::tests::read_refuses_a_file_that_changed_after_it_was_trusted
        PASS [   0.019s] (143/168) cartridge trust::tests::revoking_a_project_takes_its_nested_records
        PASS [   0.016s] (144/168) cartridge trust::tests::the_store_is_private_to_this_user
        PASS [   0.015s] (145/168) cartridge trust::tests::the_users_own_home_needs_no_trust
        PASS [   0.016s] (146/168) cartridge trust::tests::the_walk_skips_build_output_and_links
        PASS [   0.011s] (147/168) cartridge::bin/cartridge cli::host::stdio_tests::mcp_bridge_failure_preserves_request_ids_without_replay
        PASS [   0.011s] (148/168) cartridge::bin/cartridge cli::host::stdio_tests::mcp_bridge_keeps_notifications_silent_and_successes_intact
        PASS [   0.011s] (149/168) cartridge::bin/cartridge cli::listing::tests::the_listing_follows_sends_and_marks_cycles_and_missing_listeners
        PASS [   0.011s] (150/168) cartridge::bin/cartridge cli::manual::tests::addresses_resolve_and_search_lands_in_the_section
        PASS [   0.011s] (151/168) cartridge::bin/cartridge cli::settings::tests::lua_keys_and_values_render_as_lua_source
        PASS [   0.017s] (152/168) cartridge::bin/cartridge cli::setup::tests::a_file_changed_by_the_exchange_is_not_recorded
        PASS [   0.016s] (153/168) cartridge::bin/cartridge cli::setup::tests::a_folder_in_the_way_of_a_link_is_refused
        PASS [   0.113s] (154/168) cartridge::bin/cartridge cli::host::signal_tests::a_terminate_stops_the_host
        PASS [   0.014s] (155/168) cartridge::bin/cartridge cli::setup::tests::a_setup_or_doctor_event_the_cartridge_does_not_listen_to_is_refused
        PASS [   0.016s] (156/168) cartridge::bin/cartridge cli::setup::tests::setup_offers_what_it_finds_and_the_catalog_and_filters_by_subsequence
        PASS [   0.015s] (157/168) cartridge::bin/cartridge cli::setup::tests::setup_trusts_what_it_chose_not_what_the_tree_holds
        PASS [   0.019s] (158/168) cartridge::bin/cartridge cli::trust::tests::an_explicit_path_trusts_a_folder_that_is_neither
        PASS [   0.012s] (159/168) cartridge::bin/cartridge cli::width::tests::fit_and_pad_count_display_cells
        PASS [   0.319s] (160/168) cartridge::bin/cartridge cli::host::signal_tests::an_interrupt_is_ignored_while_a_program_holds_the_terminal
        PASS [   4.137s] (161/168) cartridge tests::host::a_node_serves_other_events_while_a_handler_waits
        PASS [   1.173s] (162/168) cartridge trust::tests::a_deleted_project_is_untrusted_by_a_relative_path
        PASS [   1.160s] (163/168) cartridge trust::tests::a_relative_or_empty_home_is_refused_rather_than_trust_disabling
        PASS [   1.025s] (164/168) cartridge::bin/cartridge cli::setup::tests::setup_links_the_chosen_writes_a_descriptor_the_host_reads_and_lets_a_cartridge_ask
        PASS [   3.741s] (165/168) cartridge tests::host::a_terminated_mcp_exits_with_its_input_still_open
        PASS [   6.855s] (166/168) cartridge tests::host::a_node_that_catches_its_own_refusal_exits
        PASS [   5.665s] (167/168) cartridge tests::settings::a_configuration_file_that_never_returns_is_refused
        PASS [   7.006s] (168/168) cartridge tests::host::a_spinning_handler_is_refused_and_its_node_keeps_serving
────────────
     Summary [   9.574s] 168 tests run: 168 passed, 0 skipped
test      cartridge  pass

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/host-tests-hold-under-suite-contention/specs/spec01.md: exit 0

Command SHA-256: 866a59ce40d4e150e2e1fea51d96c2296d14e66bfaef66a7e3efb830b1e49983

```text
toolchain: cargo cargo-nextest bun tmux
cargo nextest run --workspace 
    Finished `test` profile [unoptimized] target(s) in 0.06s
────────────
 Nextest run ID e59718b5-20e7-42ac-80e4-918223fcbe78 with nextest profile: default
    Starting 168 tests across 2 binaries
        PASS [   0.010s] (  1/168) cartridge host::socket::tests::an_owner_only_directory_is_created_and_repaired
        PASS [   0.013s] (  2/168) cartridge host::socket::tests::a_symlinked_socket_directory_is_refused
        PASS [   0.013s] (  3/168) cartridge lua::tests::a_memory_limit_bounds_what_a_chunk_can_allocate
        PASS [   0.013s] (  4/168) cartridge host::plan::tests::a_listener_accepts_each_declared_sender_for_its_events_only
        PASS [   0.013s] (  5/168) cartridge host::plan::tests::every_event_carries_its_deadline
        PASS [   0.017s] (  6/168) cartridge host::plan::tests::a_private_host_keeps_its_socket_and_ports_to_itself
        PASS [   0.017s] (  7/168) cartridge host::socket::tests::each_run_owns_its_node_directory_and_a_dead_run_is_swept
        PASS [   0.018s] (  8/168) cartridge host::plan::tests::no_node_holds_a_token_another_node_accepts_from_someone_else
        PASS [   0.019s] (  9/168) cartridge host::socket::tests::a_run_directory_is_owner_only
        PASS [   0.019s] ( 10/168) cartridge host::plan::tests::a_cartridge_gets_listeners_only_for_what_it_defines_or_needs
        PASS [   0.013s] ( 11/168) cartridge lua::tests::the_interpreter_keeps_computation_and_drops_the_machine
        PASS [   0.018s] ( 12/168) cartridge lua::tests::each_file_is_evaluated_in_a_state_of_its_own
        PASS [   0.013s] ( 13/168) cartridge sandbox::tests::a_write_grant_names_the_canonicalized_path_and_implies_the_read
        PASS [   0.013s] ( 14/168) cartridge sandbox::tests::an_empty_command_is_refused_before_launch
        PASS [   0.023s] ( 15/168) cartridge lua::tests::a_runaway_is_refused_and_the_state_survives
        PASS [   0.017s] ( 16/168) cartridge sandbox::tests::a_script_names_its_interpreter
        PASS [   0.018s] ( 17/168) cartridge sandbox::tests::a_net_grant_turns_the_network_on_and_an_empty_one_leaves_it_off
        PASS [   0.016s] ( 18/168) cartridge sandbox::tests::an_empty_grant_builds_no_allowance_beyond_the_runtime
        PASS [   0.010s] ( 19/168) cartridge sandbox::tests::the_runtime_is_named_canonically
        PASS [   0.016s] ( 20/168) cartridge sandbox::tests::an_exec_grant_that_resolves_builds_a_literal_and_one_that_does_not_builds_nothing
        PASS [   0.016s] ( 21/168) cartridge settings::files::tests::the_listing_reads_each_configuration_file_once
        PASS [   0.022s] ( 22/168) cartridge sandbox::tests::the_prefix_stops_at_a_system_directory
        PASS [   0.014s] ( 23/168) cartridge settings::host::tests::an_undeclared_host_key_leaves_the_declared_defaults_standing
        PASS [   0.053s] ( 24/168) cartridge lua::tests::every_resume_gets_the_budget_back
        PASS [   0.055s] ( 25/168) cartridge lua::tests::a_wait_refills_the_budget_and_a_coroutine_does_not
        PASS [   0.022s] ( 26/168) cartridge tests::host::a_document_refuses_a_bad_schema_or_a_contract_it_does_not_listen_to
        PASS [   0.267s] ( 27/168) cartridge sandbox::tests::an_async_spawn_is_confined_like_the_synchronous_one
        PASS [   0.355s] ( 28/168) cartridge sandbox::tests::an_interpreter_reaches_its_own_installation
        PASS [   0.009s] ( 29/168) cartridge tests::host::a_lifecycle_subscriber_that_falls_behind_is_disconnected
        PASS [   0.559s] ( 30/168) cartridge sandbox::tests::the_synchronous_command_enforces_the_empty_grant
        PASS [   0.217s] ( 31/168) cartridge tests::host::a_missing_listener_waits_and_says_for_what
        PASS [   0.812s] ( 32/168) cartridge tests::host::a_node_presenting_its_own_credential_is_refused_on_the_host_socket
        PASS [   1.405s] ( 33/168) cartridge tests::host::a_cartridge_asks_the_host_what_only_the_host_knows
        PASS [   1.414s] ( 34/168) cartridge tests::host::a_call_that_comes_back_into_its_sender_is_answered
        PASS [   1.420s] ( 35/168) cartridge tests::host::a_cartridge_sends_only_what_it_defines_or_needs
        PASS [   1.419s] ( 36/168) cartridge tests::host::a_glob_in_needs_names_what_the_others_listen_to
        PASS [   1.422s] ( 37/168) cartridge tests::host::a_granted_env_prefix_reaches_the_node_and_nothing_beside_it_does
        PASS [   1.459s] ( 38/168) cartridge tests::host::a_cartridge_answers_the_events_it_listens_to
        PASS [   1.438s] ( 39/168) cartridge tests::host::a_helper_asks_the_base_while_answering
        PASS [   1.039s] ( 40/168) cartridge tests::host::a_native_module_reaches_the_base_through_the_global
        PASS [   1.476s] ( 41/168) cartridge tests::host::a_hung_listener_times_out_and_its_node_keeps_serving
        PASS [   0.949s] ( 42/168) cartridge tests::host::a_spawned_helper_sees_only_the_two_named_cartridge_variables_and_a_path
        PASS [   1.167s] ( 43/168) cartridge tests::host::a_node_refuses_to_listen_to_what_it_did_not_declare
        PASS [   1.077s] ( 44/168) cartridge tests::host::a_spawn_the_grant_did_not_name_is_denied
        PASS [   0.838s] ( 45/168) cartridge tests::host::a_spawned_program_answers_requests_by_id
        PASS [   1.128s] ( 46/168) cartridge tests::host::a_payload_the_schema_rejects_never_reaches_the_listener
        PASS [   1.144s] ( 47/168) cartridge tests::host::a_pipe_wakes_the_node_from_outside
        PASS [   1.156s] ( 48/168) cartridge tests::host::a_schema_only_change_reaches_a_sender_that_already_validated
        PASS [   1.196s] ( 49/168) cartridge tests::host::a_restart_keeps_its_dependents_working
        PASS [   0.013s] ( 50/168) cartridge tests::host::an_untrusted_descriptor_is_refused_where_it_is_enforced
        PASS [   0.784s] ( 51/168) cartridge tests::host::an_undeclared_event_fails_the_cartridge_before_it_starts
        PASS [   0.016s] ( 52/168) cartridge tests::host::grant_paths_name_the_project_and_settings
        PASS [   1.192s] ( 53/168) cartridge tests::host::an_event_declared_twice_fails_the_later_entry
        PASS [   1.122s] ( 54/168) cartridge tests::host::gather_and_emit_reach_every_listener
        PASS [   1.230s] ( 55/168) cartridge tests::host::a_stop_request_ends_a_foreground_run
        PASS [   0.364s] ( 56/168) cartridge tests::host::one_cartridge_cannot_see_anothers_globals
        PASS [   0.022s] ( 57/168) cartridge tests::host::solo_entries_sharing_a_socket_name_are_refused
        PASS [   0.013s] ( 58/168) cartridge tests::ledger::a_root_that_does_not_exist_is_an_empty_ledger
        PASS [   0.016s] ( 59/168) cartridge tests::ledger::an_entry_is_its_path_from_the_root
        PASS [   1.283s] ( 60/168) cartridge tests::host::a_stopped_cartridge_takes_its_programs_along
        PASS [   0.012s] ( 61/168) cartridge tests::ledger::an_unreadable_document_is_an_entry_with_its_reason
        PASS [   0.013s] ( 62/168) cartridge tests::ledger::two_entries_of_one_scope_offering_one_key_is_a_clash
        PASS [   0.012s] ( 63/168) cartridge tests::node::the_entry_recheck_refuses_bytes_that_changed
        PASS [   0.009s] ( 64/168) cartridge tests::settings::an_untrusted_project_config_is_refused_at_its_read
        PASS [   1.310s] ( 65/168) cartridge tests::host::a_waiting_cartridge_starts_when_the_descriptor_adds_its_listener
        PASS [   0.010s] ( 66/168) cartridge tests::settings::keys_inside_an_absent_optional_table_stay_absent
        PASS [   0.010s] ( 67/168) cartridge tests::settings::naming_the_table_fills_the_keys_inside_it
        PASS [   0.011s] ( 68/168) cartridge tests::settings::yolo_overrides_the_configured_value_only_where_the_cartridge_declares_it
        PASS [   0.011s] ( 69/168) cartridge trace::tests::a_credential_or_a_prompt_body_is_omitted_and_named
        PASS [   0.009s] ( 70/168) cartridge trace::tests::a_full_diagnostics_queue_drops_records_and_says_how_many
        PASS [   0.011s] ( 71/168) cartridge trace::tests::a_sink_that_cannot_repair_a_failed_write_stops_accepting_records
        PASS [   0.011s] ( 72/168) cartridge trace::tests::oversized_records_are_valid_json_and_bounded_before_and_after_rotation
        PASS [   0.011s] ( 73/168) cartridge trace::tests::redaction_reaches_objects_inside_nested_arrays
        PASS [   0.025s] ( 74/168) cartridge trace::tests::the_sink_stays_bounded_by_rotating_one_generation
        PASS [   0.025s] ( 75/168) cartridge transport::cartridge::tests::a_cartridge_sends_a_declared_event_and_takes_the_answer
        PASS [   0.063s] ( 76/168) cartridge transport::cartridge::tests::a_connection_runs_at_most_its_in_flight_limit_at_once
        PASS [   0.020s] ( 77/168) cartridge transport::cartridge::tests::a_directory_update_replaces_the_schema_a_node_validates_against
        PASS [   0.016s] ( 78/168) cartridge transport::cartridge::tests::a_listener_checks_what_arrives_whatever_the_sender_checked
        PASS [   0.013s] ( 79/168) cartridge transport::cartridge::tests::a_peer_token_sends_events_and_nothing_else
        PASS [   0.171s] ( 80/168) cartridge transport::cartridge::tests::a_send_reconnects_after_the_listener_restarts
        PASS [   0.013s] ( 81/168) cartridge transport::cartridge::tests::a_subscriber_gets_the_replay_and_then_live_events
        PASS [   0.023s] ( 82/168) cartridge transport::cartridge::tests::an_undeclared_event_or_a_bad_payload_is_refused_before_sending
        PASS [   0.014s] ( 83/168) cartridge transport::cartridge::tests::an_unknown_token_is_refused_and_disconnected
        PASS [   0.015s] ( 84/168) cartridge transport::cartridge::tests::events_reach_listeners_directly
        PASS [   0.209s] ( 85/168) cartridge transport::cartridge::tests::gather_reports_every_listener_outcome
        PASS [   0.012s] ( 86/168) cartridge transport::rpc::tests::a_call_gets_its_result
        PASS [   0.010s] ( 87/168) cartridge transport::rpc::tests::a_request_dropped_unanswered_is_answered_with_an_internal_error
        PASS [   0.010s] ( 88/168) cartridge transport::rpc::tests::an_oversized_frame_closes_a_capped_connection
        PASS [   0.062s] ( 89/168) cartridge transport::rpc::tests::calls_run_concurrently_and_match_by_id
        PASS [   0.024s] ( 90/168) cartridge transport::rpc::tests::closing_fails_waiting_calls
        PASS [   0.010s] ( 91/168) cartridge transport::rpc::tests::dropping_the_last_handle_closes_the_connection
        PASS [   0.010s] ( 92/168) cartridge transport::rpc::tests::errors_cross_as_error_objects
        PASS [   0.010s] ( 93/168) cartridge transport::rpc::tests::notifications_arrive_without_an_id
        PASS [   0.010s] ( 94/168) cartridge transport::typed::bind_tests_unix::a_bound_socket_is_owner_only
        PASS [   1.160s] ( 95/168) cartridge tests::host::verify_sends_every_declared_contract
        PASS [   0.013s] ( 96/168) cartridge transport::typed::bind_tests_unix::a_live_endpoint_served_by_another_uid_refuses_the_bind
        PASS [   1.177s] ( 97/168) cartridge tests::host::the_host_socket_answers_the_command_line
        PASS [   0.010s] ( 98/168) cartridge transport::typed::bind_tests_unix::a_rebound_stale_socket_is_also_owner_only
        PASS [   0.012s] ( 99/168) cartridge transport::typed::bind_tests_unix::a_live_owner_reports_already_running
        PASS [   0.263s] (100/168) cartridge transport::typed::bind_tests_unix::a_caller_of_another_uid_is_refused_and_the_listener_keeps_serving
        PASS [   0.011s] (101/168) cartridge transport::typed::bind_tests_unix::a_regular_file_squatting_the_name_is_refused_not_removed
        PASS [   1.202s] (102/168) cartridge tests::host::streams_replay_and_then_deliver_live
        PASS [   0.014s] (103/168) cartridge transport::typed::bind_tests_unix::a_socket_is_owner_only_even_under_a_permissive_umask
        PASS [   0.012s] (104/168) cartridge transport::typed::bind_tests_unix::a_stale_socket_file_is_removed_and_rebound
        PASS [   1.118s] (105/168) cartridge tests::settings::refused_settings_do_not_wedge_the_process_when_diagnostics_are_on
        PASS [   0.013s] (106/168) cartridge transport::typed::owner_tests_unix::a_dangling_symlink_is_refused
        PASS [   0.011s] (107/168) cartridge transport::typed::owner_tests_unix::a_missing_path_reads_as_absence_not_as_a_squat
        PASS [   0.016s] (108/168) cartridge transport::typed::bind_tests_unix::a_symlink_to_a_foreign_target_refuses_the_bind
        PASS [   0.008s] (109/168) cartridge transport::typed::owner_tests_unix::a_path_owned_by_another_uid_is_refused
        PASS [   0.010s] (110/168) cartridge transport::typed::owner_tests_unix::a_path_this_user_owns_is_accepted
        PASS [   0.007s] (111/168) cartridge transport::typed::owner_tests_unix::connect_refuses_a_foreign_endpoint_before_it_connects
        PASS [   0.012s] (112/168) cartridge transport::typed::owner_tests_unix::a_regular_file_is_not_an_endpoint
        PASS [   0.013s] (113/168) cartridge transport::typed::owner_tests_unix::a_symlink_to_a_foreign_target_is_refused
        PASS [   0.013s] (114/168) cartridge transport::typed::owner_tests_unix::connect_accepts_a_socket_this_user_bound
        PASS [   0.009s] (115/168) cartridge transport::typed::owner_tests_unix::connect_refuses_when_the_peer_uid_differs
        PASS [   0.011s] (116/168) cartridge transport::typed::owner_tests_unix::the_peer_check_reads_the_server_uid_and_decides_both_ways
        PASS [   0.013s] (117/168) cartridge transport::typed::typed_tests::a_root_that_does_not_exist_yet_tags_the_same_from_every_spelling
        PASS [   0.011s] (118/168) cartridge transport::typed::typed_tests::tests::io_error_into_codec_is_a_decode_carrying_the_original_message
        PASS [   0.012s] (119/168) cartridge transport::typed::typed_tests::cwd_tag_tests::path_tag_is_stable_and_nonempty
        PASS [   0.014s] (120/168) cartridge transport::typed::typed_tests::tests::rpc_error_absorbs_adapter_and_codec_via_from
        PASS [   0.012s] (121/168) cartridge transport::typed::typed_tests::tests::serde_error_into_codec_preserves_the_serde_message
        PASS [   0.010s] (122/168) cartridge transport::typed::typed_tests::tests_3::json_decodes_multiple_frames_from_one_buffer
        PASS [   0.012s] (123/168) cartridge transport::typed::typed_tests::tests_2::inproc_reader_drains_leftover_across_small_reads
        PASS [   0.015s] (124/168) cartridge transport::typed::typed_tests::tests_3::json_many_consecutive_newlines_do_not_overflow
        PASS [   0.011s] (125/168) cartridge transport::typed::typed_tests::tests_3::json_roundtrip_single_frame
        PASS [   0.011s] (126/168) cartridge transport::typed::typed_tests::tests_3::json_partial_line_yields_none_until_newline
        PASS [   0.011s] (127/168) cartridge transport::typed::typed_tests::tests_3::json_tolerates_crlf_and_skips_blank_lines
        PASS [   0.010s] (128/168) cartridge transport::typed::typed_tests::tests_4::channel_roundtrip_json_envelope
        PASS [   0.012s] (129/168) cartridge transport::typed::typed_tests::tests_4::recv_returns_none_on_closed_adapter
        PASS [   0.014s] (130/168) cartridge trust::tests::a_changed_file_stops_being_trusted
        PASS [   0.015s] (131/168) cartridge transport::typed::typed_tests::the_tag_is_the_same_before_and_after_the_root_is_created
        PASS [   0.016s] (132/168) cartridge trust::tests::a_deleted_project_can_still_be_untrusted
        PASS [   0.010s] (133/168) cartridge trust::tests::a_digest_is_the_files_own_sha_256
        PASS [   0.013s] (134/168) cartridge trust::tests::a_file_the_record_does_not_name_is_refused
        PASS [   0.014s] (135/168) cartridge trust::tests::a_file_under_a_skipped_directory_names_the_real_dead_end
        PASS [   0.014s] (136/168) cartridge trust::tests::a_global_config_symlinked_out_of_the_home_still_passes
        PASS [   0.016s] (137/168) cartridge trust::tests::a_nested_record_does_not_shadow_a_fresh_outer_one
        PASS [   0.014s] (138/168) cartridge trust::tests::a_widened_grant_untrusts_its_manifest
        PASS [   0.013s] (139/168) cartridge trust::tests::an_untrusted_bare_lua_entry_is_refused_at_its_resolve
        PASS [   0.014s] (140/168) cartridge trust::tests::an_untrusted_project_is_refused_until_it_is_trusted
        PASS [   0.017s] (141/168) cartridge trust::tests::every_spelling_of_a_directory_is_one_record
        PASS [   0.013s] (142/168) cartridge trust::tests::read_refuses_a_file_that_changed_after_it_was_trusted
        PASS [   0.015s] (143/168) cartridge trust::tests::revoking_a_project_takes_its_nested_records
        PASS [   0.010s] (144/168) cartridge trust::tests::the_users_own_home_needs_no_trust
        PASS [   0.013s] (145/168) cartridge trust::tests::the_store_is_private_to_this_user
        PASS [   0.016s] (146/168) cartridge trust::tests::the_walk_skips_build_output_and_links
        PASS [   0.010s] (147/168) cartridge::bin/cartridge cli::host::stdio_tests::mcp_bridge_failure_preserves_request_ids_without_replay
        PASS [   0.011s] (148/168) cartridge::bin/cartridge cli::host::stdio_tests::mcp_bridge_keeps_notifications_silent_and_successes_intact
        PASS [   0.010s] (149/168) cartridge::bin/cartridge cli::listing::tests::the_listing_follows_sends_and_marks_cycles_and_missing_listeners
        PASS [   0.013s] (150/168) cartridge::bin/cartridge cli::manual::tests::addresses_resolve_and_search_lands_in_the_section
        PASS [   0.012s] (151/168) cartridge::bin/cartridge cli::settings::tests::lua_keys_and_values_render_as_lua_source
        PASS [   0.017s] (152/168) cartridge::bin/cartridge cli::setup::tests::a_file_changed_by_the_exchange_is_not_recorded
        PASS [   0.015s] (153/168) cartridge::bin/cartridge cli::setup::tests::a_folder_in_the_way_of_a_link_is_refused
        PASS [   0.015s] (154/168) cartridge::bin/cartridge cli::setup::tests::a_setup_or_doctor_event_the_cartridge_does_not_listen_to_is_refused
        PASS [   0.115s] (155/168) cartridge::bin/cartridge cli::host::signal_tests::a_terminate_stops_the_host
        PASS [   0.017s] (156/168) cartridge::bin/cartridge cli::setup::tests::setup_offers_what_it_finds_and_the_catalog_and_filters_by_subsequence
        PASS [   0.019s] (157/168) cartridge::bin/cartridge cli::setup::tests::setup_trusts_what_it_chose_not_what_the_tree_holds
        PASS [   0.013s] (158/168) cartridge::bin/cartridge cli::trust::tests::an_explicit_path_trusts_a_folder_that_is_neither
        PASS [   0.013s] (159/168) cartridge::bin/cartridge cli::width::tests::fit_and_pad_count_display_cells
        PASS [   0.317s] (160/168) cartridge::bin/cartridge cli::host::signal_tests::an_interrupt_is_ignored_while_a_program_holds_the_terminal
        PASS [   4.148s] (161/168) cartridge tests::host::a_node_serves_other_events_while_a_handler_waits
        PASS [   1.158s] (162/168) cartridge trust::tests::a_deleted_project_is_untrusted_by_a_relative_path
        PASS [   1.148s] (163/168) cartridge trust::tests::a_relative_or_empty_home_is_refused_rather_than_trust_disabling
        PASS [   1.008s] (164/168) cartridge::bin/cartridge cli::setup::tests::setup_links_the_chosen_writes_a_descriptor_the_host_reads_and_lets_a_cartridge_ask
        PASS [   3.731s] (165/168) cartridge tests::host::a_terminated_mcp_exits_with_its_input_still_open
        PASS [   6.683s] (166/168) cartridge tests::host::a_node_that_catches_its_own_refusal_exits
        PASS [   6.640s] (167/168) cartridge tests::host::a_spinning_handler_is_refused_and_its_node_keeps_serving
        PASS [   5.388s] (168/168) cartridge tests::settings::a_configuration_file_that_never_returns_is_refused
────────────
     Summary [   9.278s] 168 tests run: 168 passed, 0 skipped
test      cartridge  pass

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/host-tests-hold-under-suite-contention/specs/spec01.md: exit 0

Command SHA-256: 3241eaf7c2c12cc8e9cbfab601e47775b20242d2e7fd0bd2da8ef215f99e6ed6

```text
toolchain: cargo cargo-nextest bun tmux
cargo nextest run --workspace 
    Finished `test` profile [unoptimized] target(s) in 0.06s
────────────
 Nextest run ID 7a674dad-47f2-4267-99c5-379ca03cc8f4 with nextest profile: default
    Starting 168 tests across 2 binaries
        PASS [   0.012s] (  1/168) cartridge host::socket::tests::a_symlinked_socket_directory_is_refused
        PASS [   0.014s] (  2/168) cartridge lua::tests::a_memory_limit_bounds_what_a_chunk_can_allocate
        PASS [   0.015s] (  3/168) cartridge host::socket::tests::an_owner_only_directory_is_created_and_repaired
        PASS [   0.015s] (  4/168) cartridge host::plan::tests::a_listener_accepts_each_declared_sender_for_its_events_only
        PASS [   0.016s] (  5/168) cartridge host::plan::tests::every_event_carries_its_deadline
        PASS [   0.016s] (  6/168) cartridge host::socket::tests::a_run_directory_is_owner_only
        PASS [   0.016s] (  7/168) cartridge host::plan::tests::no_node_holds_a_token_another_node_accepts_from_someone_else
        PASS [   0.016s] (  8/168) cartridge host::plan::tests::a_private_host_keeps_its_socket_and_ports_to_itself
        PASS [   0.017s] (  9/168) cartridge host::plan::tests::a_cartridge_gets_listeners_only_for_what_it_defines_or_needs
        PASS [   0.021s] ( 10/168) cartridge host::socket::tests::each_run_owns_its_node_directory_and_a_dead_run_is_swept
        PASS [   0.013s] ( 11/168) cartridge sandbox::tests::a_write_grant_names_the_canonicalized_path_and_implies_the_read
        PASS [   0.014s] ( 12/168) cartridge sandbox::tests::a_net_grant_turns_the_network_on_and_an_empty_one_leaves_it_off
        PASS [   0.016s] ( 13/168) cartridge lua::tests::each_file_is_evaluated_in_a_state_of_its_own
        PASS [   0.011s] ( 14/168) cartridge sandbox::tests::an_empty_command_is_refused_before_launch
        PASS [   0.021s] ( 15/168) cartridge lua::tests::the_interpreter_keeps_computation_and_drops_the_machine
        PASS [   0.029s] ( 16/168) cartridge lua::tests::a_runaway_is_refused_and_the_state_survives
        PASS [   0.025s] ( 17/168) cartridge sandbox::tests::a_script_names_its_interpreter
        PASS [   0.015s] ( 18/168) cartridge sandbox::tests::an_exec_grant_that_resolves_builds_a_literal_and_one_that_does_not_builds_nothing
        PASS [   0.017s] ( 19/168) cartridge sandbox::tests::the_prefix_stops_at_a_system_directory
        PASS [   0.019s] ( 20/168) cartridge sandbox::tests::an_empty_grant_builds_no_allowance_beyond_the_runtime
        PASS [   0.015s] ( 21/168) cartridge sandbox::tests::the_runtime_is_named_canonically
        PASS [   0.016s] ( 22/168) cartridge settings::files::tests::the_listing_reads_each_configuration_file_once
        PASS [   0.017s] ( 23/168) cartridge settings::host::tests::an_undeclared_host_key_leaves_the_declared_defaults_standing
        PASS [   0.049s] ( 24/168) cartridge lua::tests::a_wait_refills_the_budget_and_a_coroutine_does_not
        PASS [   0.060s] ( 25/168) cartridge lua::tests::every_resume_gets_the_budget_back
        PASS [   0.022s] ( 26/168) cartridge tests::host::a_document_refuses_a_bad_schema_or_a_contract_it_does_not_listen_to
        PASS [   0.273s] ( 27/168) cartridge sandbox::tests::an_async_spawn_is_confined_like_the_synchronous_one
        PASS [   0.359s] ( 28/168) cartridge sandbox::tests::an_interpreter_reaches_its_own_installation
        PASS [   0.011s] ( 29/168) cartridge tests::host::a_lifecycle_subscriber_that_falls_behind_is_disconnected
        PASS [   0.185s] ( 30/168) cartridge tests::host::a_missing_listener_waits_and_says_for_what
        PASS [   0.566s] ( 31/168) cartridge sandbox::tests::the_synchronous_command_enforces_the_empty_grant
        PASS [   1.401s] ( 32/168) cartridge tests::host::a_granted_env_prefix_reaches_the_node_and_nothing_beside_it_does
        PASS [   1.427s] ( 33/168) cartridge tests::host::a_call_that_comes_back_into_its_sender_is_answered
        PASS [   0.873s] ( 34/168) cartridge tests::host::a_node_presenting_its_own_credential_is_refused_on_the_host_socket
        PASS [   1.437s] ( 35/168) cartridge tests::host::a_cartridge_asks_the_host_what_only_the_host_knows
        PASS [   1.440s] ( 36/168) cartridge tests::host::a_glob_in_needs_names_what_the_others_listen_to
        PASS [   1.451s] ( 37/168) cartridge tests::host::a_cartridge_sends_only_what_it_defines_or_needs
        PASS [   1.482s] ( 38/168) cartridge tests::host::a_cartridge_answers_the_events_it_listens_to
        PASS [   1.471s] ( 39/168) cartridge tests::host::a_helper_asks_the_base_while_answering
        PASS [   1.025s] ( 40/168) cartridge tests::host::a_native_module_reaches_the_base_through_the_global
        PASS [   1.493s] ( 41/168) cartridge tests::host::a_hung_listener_times_out_and_its_node_keeps_serving
        PASS [   0.877s] ( 42/168) cartridge tests::host::a_spawned_program_answers_requests_by_id
        PASS [   1.079s] ( 43/168) cartridge tests::host::a_spawned_helper_sees_only_the_two_named_cartridge_variables_and_a_path
        PASS [   1.213s] ( 44/168) cartridge tests::host::a_node_refuses_to_listen_to_what_it_did_not_declare
        PASS [   1.134s] ( 45/168) cartridge tests::host::a_spawn_the_grant_did_not_name_is_denied
        PASS [   1.208s] ( 46/168) cartridge tests::host::a_payload_the_schema_rejects_never_reaches_the_listener
        PASS [   1.217s] ( 47/168) cartridge tests::host::a_pipe_wakes_the_node_from_outside
        PASS [   1.216s] ( 48/168) cartridge tests::host::a_schema_only_change_reaches_a_sender_that_already_validated
        PASS [   1.273s] ( 49/168) cartridge tests::host::a_restart_keeps_its_dependents_working
        PASS [   0.012s] ( 50/168) cartridge tests::host::an_untrusted_descriptor_is_refused_where_it_is_enforced
        PASS [   0.680s] ( 51/168) cartridge tests::host::an_undeclared_event_fails_the_cartridge_before_it_starts
        PASS [   0.018s] ( 52/168) cartridge tests::host::grant_paths_name_the_project_and_settings
        PASS [   1.018s] ( 53/168) cartridge tests::host::gather_and_emit_reach_every_listener
        PASS [   0.014s] ( 54/168) cartridge tests::host::solo_entries_sharing_a_socket_name_are_refused
        PASS [   1.138s] ( 55/168) cartridge tests::host::a_stop_request_ends_a_foreground_run
        PASS [   1.116s] ( 56/168) cartridge tests::host::an_event_declared_twice_fails_the_later_entry
        PASS [   0.400s] ( 57/168) cartridge tests::host::one_cartridge_cannot_see_anothers_globals
        PASS [   0.010s] ( 58/168) cartridge tests::ledger::a_root_that_does_not_exist_is_an_empty_ledger
        PASS [   0.013s] ( 59/168) cartridge tests::ledger::an_entry_is_its_path_from_the_root
        PASS [   0.011s] ( 60/168) cartridge tests::ledger::an_unreadable_document_is_an_entry_with_its_reason
        PASS [   1.197s] ( 61/168) cartridge tests::host::a_stopped_cartridge_takes_its_programs_along
        PASS [   0.014s] ( 62/168) cartridge tests::ledger::two_entries_of_one_scope_offering_one_key_is_a_clash
        PASS [   0.011s] ( 63/168) cartridge tests::node::the_entry_recheck_refuses_bytes_that_changed
        PASS [   0.011s] ( 64/168) cartridge tests::settings::an_untrusted_project_config_is_refused_at_its_read
        PASS [   1.214s] ( 65/168) cartridge tests::host::a_waiting_cartridge_starts_when_the_descriptor_adds_its_listener
        PASS [   0.009s] ( 66/168) cartridge tests::settings::naming_the_table_fills_the_keys_inside_it
        PASS [   0.012s] ( 67/168) cartridge tests::settings::keys_inside_an_absent_optional_table_stay_absent
        PASS [   0.011s] ( 68/168) cartridge tests::settings::yolo_overrides_the_configured_value_only_where_the_cartridge_declares_it
        PASS [   0.011s] ( 69/168) cartridge trace::tests::a_credential_or_a_prompt_body_is_omitted_and_named
        PASS [   0.012s] ( 70/168) cartridge trace::tests::a_full_diagnostics_queue_drops_records_and_says_how_many
        PASS [   0.012s] ( 71/168) cartridge trace::tests::a_sink_that_cannot_repair_a_failed_write_stops_accepting_records
        PASS [   0.014s] ( 72/168) cartridge trace::tests::oversized_records_are_valid_json_and_bounded_before_and_after_rotation
        PASS [   0.013s] ( 73/168) cartridge trace::tests::redaction_reaches_objects_inside_nested_arrays
        PASS [   0.023s] ( 74/168) cartridge trace::tests::the_sink_stays_bounded_by_rotating_one_generation
        PASS [   0.026s] ( 75/168) cartridge transport::cartridge::tests::a_cartridge_sends_a_declared_event_and_takes_the_answer
        PASS [   0.071s] ( 76/168) cartridge transport::cartridge::tests::a_connection_runs_at_most_its_in_flight_limit_at_once
        PASS [   0.020s] ( 77/168) cartridge transport::cartridge::tests::a_directory_update_replaces_the_schema_a_node_validates_against
        PASS [   0.015s] ( 78/168) cartridge transport::cartridge::tests::a_listener_checks_what_arrives_whatever_the_sender_checked
        PASS [   0.011s] ( 79/168) cartridge transport::cartridge::tests::a_peer_token_sends_events_and_nothing_else
        PASS [   0.161s] ( 80/168) cartridge transport::cartridge::tests::a_send_reconnects_after_the_listener_restarts
        PASS [   0.015s] ( 81/168) cartridge transport::cartridge::tests::a_subscriber_gets_the_replay_and_then_live_events
        PASS [   0.018s] ( 82/168) cartridge transport::cartridge::tests::an_undeclared_event_or_a_bad_payload_is_refused_before_sending
        PASS [   0.011s] ( 83/168) cartridge transport::cartridge::tests::an_unknown_token_is_refused_and_disconnected
        PASS [   0.011s] ( 84/168) cartridge transport::cartridge::tests::events_reach_listeners_directly
        PASS [   0.208s] ( 85/168) cartridge transport::cartridge::tests::gather_reports_every_listener_outcome
        PASS [   0.011s] ( 86/168) cartridge transport::rpc::tests::a_call_gets_its_result
        PASS [   0.011s] ( 87/168) cartridge transport::rpc::tests::a_request_dropped_unanswered_is_answered_with_an_internal_error
        PASS [   0.010s] ( 88/168) cartridge transport::rpc::tests::an_oversized_frame_closes_a_capped_connection
        PASS [   0.064s] ( 89/168) cartridge transport::rpc::tests::calls_run_concurrently_and_match_by_id
        PASS [   0.023s] ( 90/168) cartridge transport::rpc::tests::closing_fails_waiting_calls
        PASS [   0.010s] ( 91/168) cartridge transport::rpc::tests::dropping_the_last_handle_closes_the_connection
        PASS [   0.011s] ( 92/168) cartridge transport::rpc::tests::errors_cross_as_error_objects
        PASS [   0.009s] ( 93/168) cartridge transport::rpc::tests::notifications_arrive_without_an_id
        PASS [   0.011s] ( 94/168) cartridge transport::typed::bind_tests_unix::a_bound_socket_is_owner_only
        PASS [   1.121s] ( 95/168) cartridge tests::host::verify_sends_every_declared_contract
        PASS [   0.012s] ( 96/168) cartridge transport::typed::bind_tests_unix::a_live_endpoint_served_by_another_uid_refuses_the_bind
        PASS [   1.148s] ( 97/168) cartridge tests::host::the_host_socket_answers_the_command_line
        PASS [   0.012s] ( 98/168) cartridge transport::typed::bind_tests_unix::a_live_owner_reports_already_running
        PASS [   0.013s] ( 99/168) cartridge transport::typed::bind_tests_unix::a_rebound_stale_socket_is_also_owner_only
        PASS [   1.070s] (100/168) cartridge tests::settings::refused_settings_do_not_wedge_the_process_when_diagnostics_are_on
        PASS [   1.168s] (101/168) cartridge tests::host::streams_replay_and_then_deliver_live
        PASS [   0.012s] (102/168) cartridge transport::typed::bind_tests_unix::a_regular_file_squatting_the_name_is_refused_not_removed
        PASS [   0.012s] (103/168) cartridge transport::typed::bind_tests_unix::a_socket_is_owner_only_even_under_a_permissive_umask
        PASS [   0.010s] (104/168) cartridge transport::typed::bind_tests_unix::a_symlink_to_a_foreign_target_refuses_the_bind
        PASS [   0.013s] (105/168) cartridge transport::typed::bind_tests_unix::a_stale_socket_file_is_removed_and_rebound
        PASS [   0.011s] (106/168) cartridge transport::typed::owner_tests_unix::a_dangling_symlink_is_refused
        PASS [   0.264s] (107/168) cartridge transport::typed::bind_tests_unix::a_caller_of_another_uid_is_refused_and_the_listener_keeps_serving
        PASS [   0.013s] (108/168) cartridge transport::typed::owner_tests_unix::a_missing_path_reads_as_absence_not_as_a_squat
        PASS [   0.013s] (109/168) cartridge transport::typed::owner_tests_unix::a_path_owned_by_another_uid_is_refused
        PASS [   0.011s] (110/168) cartridge transport::typed::owner_tests_unix::a_regular_file_is_not_an_endpoint
        PASS [   0.013s] (111/168) cartridge transport::typed::owner_tests_unix::a_path_this_user_owns_is_accepted
        PASS [   0.011s] (112/168) cartridge transport::typed::owner_tests_unix::a_symlink_to_a_foreign_target_is_refused
        PASS [   0.010s] (113/168) cartridge transport::typed::owner_tests_unix::the_peer_check_reads_the_server_uid_and_decides_both_ways
        PASS [   0.012s] (114/168) cartridge transport::typed::owner_tests_unix::connect_refuses_when_the_peer_uid_differs
        PASS [   0.013s] (115/168) cartridge transport::typed::owner_tests_unix::connect_accepts_a_socket_this_user_bound
        PASS [   0.013s] (116/168) cartridge transport::typed::owner_tests_unix::connect_refuses_a_foreign_endpoint_before_it_connects
        PASS [   0.013s] (117/168) cartridge transport::typed::typed_tests::a_root_that_does_not_exist_yet_tags_the_same_from_every_spelling
        PASS [   0.011s] (118/168) cartridge transport::typed::typed_tests::cwd_tag_tests::path_tag_is_stable_and_nonempty
        PASS [   0.012s] (119/168) cartridge transport::typed::typed_tests::tests::io_error_into_codec_is_a_decode_carrying_the_original_message
        PASS [   0.012s] (120/168) cartridge transport::typed::typed_tests::tests::serde_error_into_codec_preserves_the_serde_message
        PASS [   0.013s] (121/168) cartridge transport::typed::typed_tests::tests::rpc_error_absorbs_adapter_and_codec_via_from
        PASS [   0.011s] (122/168) cartridge transport::typed::typed_tests::tests_2::inproc_reader_drains_leftover_across_small_reads
        PASS [   0.009s] (123/168) cartridge transport::typed::typed_tests::tests_3::json_decodes_multiple_frames_from_one_buffer
        PASS [   0.009s] (124/168) cartridge transport::typed::typed_tests::tests_3::json_partial_line_yields_none_until_newline
        PASS [   0.011s] (125/168) cartridge transport::typed::typed_tests::tests_3::json_roundtrip_single_frame
        PASS [   0.008s] (126/168) cartridge transport::typed::typed_tests::tests_3::json_tolerates_crlf_and_skips_blank_lines
        PASS [   0.016s] (127/168) cartridge transport::typed::typed_tests::tests_3::json_many_consecutive_newlines_do_not_overflow
        PASS [   0.010s] (128/168) cartridge transport::typed::typed_tests::tests_4::channel_roundtrip_json_envelope
        PASS [   0.011s] (129/168) cartridge transport::typed::typed_tests::tests_4::recv_returns_none_on_closed_adapter
        PASS [   0.014s] (130/168) cartridge transport::typed::typed_tests::the_tag_is_the_same_before_and_after_the_root_is_created
        PASS [   0.014s] (131/168) cartridge trust::tests::a_changed_file_stops_being_trusted
        PASS [   0.010s] (132/168) cartridge trust::tests::a_digest_is_the_files_own_sha_256
        PASS [   0.015s] (133/168) cartridge trust::tests::a_deleted_project_can_still_be_untrusted
        PASS [   0.015s] (134/168) cartridge trust::tests::a_file_the_record_does_not_name_is_refused
        PASS [   0.015s] (135/168) cartridge trust::tests::a_file_under_a_skipped_directory_names_the_real_dead_end
        PASS [   0.014s] (136/168) cartridge trust::tests::a_nested_record_does_not_shadow_a_fresh_outer_one
        PASS [   0.014s] (137/168) cartridge trust::tests::a_global_config_symlinked_out_of_the_home_still_passes
        PASS [   0.016s] (138/168) cartridge trust::tests::a_widened_grant_untrusts_its_manifest
        PASS [   0.015s] (139/168) cartridge trust::tests::an_untrusted_bare_lua_entry_is_refused_at_its_resolve
        PASS [   0.016s] (140/168) cartridge trust::tests::an_untrusted_project_is_refused_until_it_is_trusted
        PASS [   0.014s] (141/168) cartridge trust::tests::every_spelling_of_a_directory_is_one_record
        PASS [   0.016s] (142/168) cartridge trust::tests::read_refuses_a_file_that_changed_after_it_was_trusted
        PASS [   0.015s] (143/168) cartridge trust::tests::revoking_a_project_takes_its_nested_records
        PASS [   0.013s] (144/168) cartridge trust::tests::the_store_is_private_to_this_user
        PASS [   0.010s] (145/168) cartridge trust::tests::the_users_own_home_needs_no_trust
        PASS [   0.014s] (146/168) cartridge trust::tests::the_walk_skips_build_output_and_links
        PASS [   0.013s] (147/168) cartridge::bin/cartridge cli::host::stdio_tests::mcp_bridge_failure_preserves_request_ids_without_replay
        PASS [   0.011s] (148/168) cartridge::bin/cartridge cli::host::stdio_tests::mcp_bridge_keeps_notifications_silent_and_successes_intact
        PASS [   0.011s] (149/168) cartridge::bin/cartridge cli::listing::tests::the_listing_follows_sends_and_marks_cycles_and_missing_listeners
        PASS [   0.013s] (150/168) cartridge::bin/cartridge cli::manual::tests::addresses_resolve_and_search_lands_in_the_section
        PASS [   0.011s] (151/168) cartridge::bin/cartridge cli::settings::tests::lua_keys_and_values_render_as_lua_source
        PASS [   0.017s] (152/168) cartridge::bin/cartridge cli::setup::tests::a_file_changed_by_the_exchange_is_not_recorded
        PASS [   0.013s] (153/168) cartridge::bin/cartridge cli::setup::tests::a_folder_in_the_way_of_a_link_is_refused
        PASS [   0.015s] (154/168) cartridge::bin/cartridge cli::setup::tests::a_setup_or_doctor_event_the_cartridge_does_not_listen_to_is_refused
        PASS [   0.114s] (155/168) cartridge::bin/cartridge cli::host::signal_tests::a_terminate_stops_the_host
        PASS [   0.015s] (156/168) cartridge::bin/cartridge cli::setup::tests::setup_offers_what_it_finds_and_the_catalog_and_filters_by_subsequence
        PASS [   0.015s] (157/168) cartridge::bin/cartridge cli::setup::tests::setup_trusts_what_it_chose_not_what_the_tree_holds
        PASS [   0.013s] (158/168) cartridge::bin/cartridge cli::trust::tests::an_explicit_path_trusts_a_folder_that_is_neither
        PASS [   0.008s] (159/168) cartridge::bin/cartridge cli::width::tests::fit_and_pad_count_display_cells
        PASS [   0.315s] (160/168) cartridge::bin/cartridge cli::host::signal_tests::an_interrupt_is_ignored_while_a_program_holds_the_terminal
        PASS [   4.210s] (161/168) cartridge tests::host::a_node_serves_other_events_while_a_handler_waits
        PASS [   1.074s] (162/168) cartridge trust::tests::a_deleted_project_is_untrusted_by_a_relative_path
        PASS [   1.065s] (163/168) cartridge trust::tests::a_relative_or_empty_home_is_refused_rather_than_trust_disabling
        PASS [   0.926s] (164/168) cartridge::bin/cartridge cli::setup::tests::setup_links_the_chosen_writes_a_descriptor_the_host_reads_and_lets_a_cartridge_ask
        PASS [   3.504s] (165/168) cartridge tests::host::a_terminated_mcp_exits_with_its_input_still_open
        PASS [   7.233s] (166/168) cartridge tests::host::a_node_that_catches_its_own_refusal_exits
        PASS [   6.558s] (167/168) cartridge tests::host::a_spinning_handler_is_refused_and_its_node_keeps_serving
        PASS [   5.511s] (168/168) cartridge tests::settings::a_configuration_file_that_never_returns_is_refused
────────────
     Summary [   9.405s] 168 tests run: 168 passed, 0 skipped
test      cartridge  pass

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/host-tests-hold-under-suite-contention/specs/spec01.md: exit 0

Command SHA-256: 9bf309cfdeb310dcb38e572d70ef92043b89a95ada0ef228fd65469903ab7155

```text

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/host-tests-hold-under-suite-contention/specs/spec01.md: exit 0

Command SHA-256: 0798710a90b09c9938761b6084753296de08301ebc32018e52e896d958ffc96d

```text

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/host-tests-hold-under-suite-contention/specs/spec01.md: exit 0

Command SHA-256: 4cacfac87ed95568e2332bd3bf5204a8df619c4dd77dbfd829309df248c8d4a4

```text
    Finished `test` profile [unoptimized] target(s) in 0.05s
     Running unittests src/lib.rs (target/debug/deps/cartridge-e31ef922f87b2f0b)

running 153 tests
test host::socket::tests::a_symlinked_socket_directory_is_refused ... ok
test host::socket::tests::an_owner_only_directory_is_created_and_repaired ... ok
test host::plan::tests::a_cartridge_gets_listeners_only_for_what_it_defines_or_needs ... ok
test lua::tests::a_memory_limit_bounds_what_a_chunk_can_allocate ... ok
test host::socket::tests::a_run_directory_is_owner_only ... ok
test host::plan::tests::every_event_carries_its_deadline ... ok
test host::plan::tests::no_node_holds_a_token_another_node_accepts_from_someone_else ... ok
test lua::tests::the_interpreter_keeps_computation_and_drops_the_machine ... ok
test host::plan::tests::a_private_host_keeps_its_socket_and_ports_to_itself ... ok
test host::plan::tests::a_listener_accepts_each_declared_sender_for_its_events_only ... ok
test sandbox::tests::a_write_grant_names_the_canonicalized_path_and_implies_the_read ... ok
test sandbox::tests::a_net_grant_turns_the_network_on_and_an_empty_one_leaves_it_off ... ok
test sandbox::tests::a_script_names_its_interpreter ... ok
test lua::tests::each_file_is_evaluated_in_a_state_of_its_own ... ok
test host::socket::tests::each_run_owns_its_node_directory_and_a_dead_run_is_swept ... ok
test sandbox::tests::an_empty_command_is_refused_before_launch ... ok
test sandbox::tests::an_empty_grant_builds_no_allowance_beyond_the_runtime ... ok
test sandbox::tests::an_exec_grant_that_resolves_builds_a_literal_and_one_that_does_not_builds_nothing ... ok
test sandbox::tests::the_runtime_is_named_canonically ... ok
test sandbox::tests::the_prefix_stops_at_a_system_directory ... ok
test settings::host::tests::an_undeclared_host_key_leaves_the_declared_defaults_standing ... ok
test settings::files::tests::the_listing_reads_each_configuration_file_once ... ok
test lua::tests::a_runaway_is_refused_and_the_state_survives ... ok
test tests::host::a_document_refuses_a_bad_schema_or_a_contract_it_does_not_listen_to ... ok
test lua::tests::a_wait_refills_the_budget_and_a_coroutine_does_not ... ok
test lua::tests::every_resume_gets_the_budget_back ... ok
test sandbox::tests::the_synchronous_command_enforces_the_empty_grant ... ok
test sandbox::tests::an_async_spawn_is_confined_like_the_synchronous_one ... ok
test tests::host::a_lifecycle_subscriber_that_falls_behind_is_disconnected ... ok
test tests::host::a_missing_listener_waits_and_says_for_what ... ok
test sandbox::tests::an_interpreter_reaches_its_own_installation ... ok
test tests::host::a_call_that_comes_back_into_its_sender_is_answered ... ok
test tests::host::a_cartridge_asks_the_host_what_only_the_host_knows ... ok
test tests::host::a_node_presenting_its_own_credential_is_refused_on_the_host_socket ... ok
test tests::host::a_cartridge_sends_only_what_it_defines_or_needs ... ok
test tests::host::a_granted_env_prefix_reaches_the_node_and_nothing_beside_it_does ... ok
test tests::host::a_glob_in_needs_names_what_the_others_listen_to ... ok
test tests::host::a_cartridge_answers_the_events_it_listens_to ... ok
test tests::host::a_node_refuses_to_listen_to_what_it_did_not_declare ... ok
test tests::host::a_helper_asks_the_base_while_answering ... ok
test tests::host::a_payload_the_schema_rejects_never_reaches_the_listener ... ok
test tests::host::a_spawn_the_grant_did_not_name_is_denied ... ok
test tests::host::a_pipe_wakes_the_node_from_outside ... ok
test tests::host::a_spawned_program_answers_requests_by_id ... ok
test tests::host::a_spawned_helper_sees_only_the_two_named_cartridge_variables_and_a_path ... ok
test tests::host::a_schema_only_change_reaches_a_sender_that_already_validated ... ok
test tests::host::a_stop_request_ends_a_foreground_run ... ok
test tests::host::a_restart_keeps_its_dependents_working ... ok
test tests::host::an_undeclared_event_fails_the_cartridge_before_it_starts ... ok
test tests::host::an_untrusted_descriptor_is_refused_where_it_is_enforced ... ok
test tests::host::a_stopped_cartridge_takes_its_programs_along ... ok
test tests::host::grant_paths_name_the_project_and_settings ... ok
test tests::host::a_native_module_reaches_the_base_through_the_global ... ok
test tests::host::solo_entries_sharing_a_socket_name_are_refused ... ok
test tests::host::an_event_declared_twice_fails_the_later_entry ... ok
test tests::host::one_cartridge_cannot_see_anothers_globals ... ok
test tests::host::a_waiting_cartridge_starts_when_the_descriptor_adds_its_listener ... ok
test tests::ledger::a_root_that_does_not_exist_is_an_empty_ledger ... ok
test tests::ledger::an_entry_is_its_path_from_the_root ... ok
test tests::host::gather_and_emit_reach_every_listener ... ok
test tests::ledger::an_unreadable_document_is_an_entry_with_its_reason ... ok
test tests::host::the_host_socket_answers_the_command_line ... ok
test tests::node::the_entry_recheck_refuses_bytes_that_changed ... ok
test tests::ledger::two_entries_of_one_scope_offering_one_key_is_a_clash ... ok
test tests::settings::an_untrusted_project_config_is_refused_at_its_read ... ok
test tests::settings::keys_inside_an_absent_optional_table_stay_absent ... ok
test tests::settings::naming_the_table_fills_the_keys_inside_it ... ok
test tests::settings::yolo_overrides_the_configured_value_only_where_the_cartridge_declares_it ... ok
test trace::tests::a_credential_or_a_prompt_body_is_omitted_and_named ... ok
test trace::tests::a_full_diagnostics_queue_drops_records_and_says_how_many ... ok
test trace::tests::a_sink_that_cannot_repair_a_failed_write_stops_accepting_records ... ok
test trace::tests::oversized_records_are_valid_json_and_bounded_before_and_after_rotation ... ok
test trace::tests::redaction_reaches_objects_inside_nested_arrays ... ok
test trace::tests::the_sink_stays_bounded_by_rotating_one_generation ... ok
test transport::cartridge::tests::a_cartridge_sends_a_declared_event_and_takes_the_answer ... ok
test transport::cartridge::tests::a_connection_runs_at_most_its_in_flight_limit_at_once ... ok
test transport::cartridge::tests::a_directory_update_replaces_the_schema_a_node_validates_against ... ok
test transport::cartridge::tests::a_listener_checks_what_arrives_whatever_the_sender_checked ... ok
test transport::cartridge::tests::a_peer_token_sends_events_and_nothing_else ... ok
test tests::host::a_hung_listener_times_out_and_its_node_keeps_serving ... ok
test transport::cartridge::tests::a_subscriber_gets_the_replay_and_then_live_events ... ok
test transport::cartridge::tests::an_undeclared_event_or_a_bad_payload_is_refused_before_sending ... ok
test transport::cartridge::tests::an_unknown_token_is_refused_and_disconnected ... ok
test transport::cartridge::tests::events_reach_listeners_directly ... ok
test transport::cartridge::tests::a_send_reconnects_after_the_listener_restarts ... ok
test transport::rpc::tests::a_call_gets_its_result ... ok
test transport::rpc::tests::a_request_dropped_unanswered_is_answered_with_an_internal_error ... ok
test transport::rpc::tests::an_oversized_frame_closes_a_capped_connection ... ok
test transport::rpc::tests::calls_run_concurrently_and_match_by_id ... ok
test transport::rpc::tests::closing_fails_waiting_calls ... ok
test transport::rpc::tests::dropping_the_last_handle_closes_the_connection ... ok
test transport::rpc::tests::errors_cross_as_error_objects ... ok
test transport::rpc::tests::notifications_arrive_without_an_id ... ok
test transport::typed::bind_tests_unix::a_bound_socket_is_owner_only ... ok
test transport::cartridge::tests::gather_reports_every_listener_outcome ... ok
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
test trust::tests::a_changed_file_stops_being_trusted ... ok
test trust::tests::a_deleted_project_can_still_be_untrusted ... ok
test transport::typed::bind_tests_unix::a_caller_of_another_uid_is_refused_and_the_listener_keeps_serving ... ok
test trust::tests::a_digest_is_the_files_own_sha_256 ... ok
test trust::tests::a_file_the_record_does_not_name_is_refused ... ok
test trust::tests::a_file_under_a_skipped_directory_names_the_real_dead_end ... ok
test trust::tests::a_global_config_symlinked_out_of_the_home_still_passes ... ok
test trust::tests::a_nested_record_does_not_shadow_a_fresh_outer_one ... ok
test trust::tests::a_deleted_project_is_untrusted_by_a_relative_path ... ok
test trust::tests::a_widened_grant_untrusts_its_manifest ... ok
test trust::tests::an_untrusted_bare_lua_entry_is_refused_at_its_resolve ... ok
test trust::tests::an_untrusted_project_is_refused_until_it_is_trusted ... ok
test trust::tests::every_spelling_of_a_directory_is_one_record ... ok
test trust::tests::read_refuses_a_file_that_changed_after_it_was_trusted ... ok
test trust::tests::revoking_a_project_takes_its_nested_records ... ok
test trust::tests::the_store_is_private_to_this_user ... ok
test trust::tests::the_users_own_home_needs_no_trust ... ok
test trust::tests::the_walk_skips_build_output_and_links ... ok
test trust::tests::a_relative_or_empty_home_is_refused_rather_than_trust_disabling ... ok
test tests::host::verify_sends_every_declared_contract ... ok
test tests::host::streams_replay_and_then_deliver_live ... ok
test tests::settings::refused_settings_do_not_wedge_the_process_when_diagnostics_are_on ... ok
test tests::host::a_terminated_mcp_exits_with_its_input_still_open ... ok
test tests::host::a_node_serves_other_events_while_a_handler_waits ... ok
test tests::host::a_node_that_catches_its_own_refusal_exits ... ok
test tests::host::a_spinning_handler_is_refused_and_its_node_keeps_serving ... ok
test tests::settings::a_configuration_file_that_never_returns_is_refused ... ok

test result: ok. 153 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 7.15s

     Running unittests src/main.rs (target/debug/deps/cartridge-4cf410bc79e1524b)

running 15 tests
test cli::settings::tests::lua_keys_and_values_render_as_lua_source ... ok
test cli::listing::tests::the_listing_follows_sends_and_marks_cycles_and_missing_listeners ... ok
test cli::host::stdio_tests::mcp_bridge_failure_preserves_request_ids_without_replay ... ok
test cli::host::stdio_tests::mcp_bridge_keeps_notifications_silent_and_successes_intact ... ok
test cli::manual::tests::addresses_resolve_and_search_lands_in_the_section ... ok
test cli::width::tests::fit_and_pad_count_display_cells ... ok
test cli::setup::tests::a_setup_or_doctor_event_the_cartridge_does_not_listen_to_is_refused ... ok
test cli::setup::tests::a_folder_in_the_way_of_a_link_is_refused ... ok
test cli::setup::tests::setup_offers_what_it_finds_and_the_catalog_and_filters_by_subsequence ... ok
test cli::setup::tests::a_file_changed_by_the_exchange_is_not_recorded ... ok
test cli::host::signal_tests::a_terminate_stops_the_host ... ok
test cli::host::signal_tests::an_interrupt_is_ignored_while_a_program_holds_the_terminal ... ok
test cli::setup::tests::setup_links_the_chosen_writes_a_descriptor_the_host_reads_and_lets_a_cartridge_ask ... ok
test cli::setup::tests::setup_trusts_what_it_chose_not_what_the_tree_holds ... ok
test cli::trust::tests::an_explicit_path_trusts_a_folder_that_is_neither ... ok

test result: ok. 15 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.95s

   Doc-tests cartridge

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s


```
