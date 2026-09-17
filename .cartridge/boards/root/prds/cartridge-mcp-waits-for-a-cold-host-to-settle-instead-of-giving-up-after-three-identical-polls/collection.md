---
commit: ac71b3b6ee892449afb8d8c1b6df00ed80b8488c
spec-digests: {"spec01.md":"2112b30dd2db66934ef2a769f5999e93bbee842e20e7610a0726b4e69b10e0ab"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/cartridge-mcp-waits-for-a-cold-host-to-settle-instead-of-giving-up-after-three-identical-polls/specs/spec01.md: exit 0

Command SHA-256: ec06429054a399df88b388509f3b015c53e4f7f1eaed0325bbe976dea15d6174

```text
source guards ok

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/cartridge-mcp-waits-for-a-cold-host-to-settle-instead-of-giving-up-after-three-identical-polls/specs/spec01.md: exit 0

Command SHA-256: 4760afe0e99095634b80c18cdde760ca5fe44b4ea02c58b27ab4b73079b9d606

```text
    Finished `test` profile [unoptimized] target(s) in 0.05s
     Running unittests src/main.rs (target/cartridge-mcp-waits-verify/debug/deps/cartridge-4cf410bc79e1524b)

running 4 tests
test cli::host::stdio_tests::settled_not_on_an_empty_composition ... ok
test cli::host::stdio_tests::settled_when_the_key_is_active ... ok
test cli::host::stdio_tests::settled_when_nothing_is_left_starting ... ok
test cli::host::stdio_tests::settled_not_while_the_key_is_starting ... ok

test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 16 filtered out; finished in 0.00s

settled unit cases ok

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/cartridge-mcp-waits-for-a-cold-host-to-settle-instead-of-giving-up-after-three-identical-polls/specs/spec01.md: exit 0

Command SHA-256: 97ddbaf19afa303cb18685fbbfec0dc53a048141a611c96d4d5d19540c8f66ca

```text
toolchain: cargo cargo-nextest bun tmux
cargo fmt --all --check
cargo clippy --workspace --all-targets
    Finished `dev` profile [unoptimized] target(s) in 0.08s
check     cartridge  pass

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/cartridge-mcp-waits-for-a-cold-host-to-settle-instead-of-giving-up-after-three-identical-polls/specs/spec01.md: exit 0

Command SHA-256: 7c25c6cea6274aa8b741ddb3c6784e6a699b8328b9c8aa6313518879b9570be9

```text
toolchain: cargo cargo-nextest bun tmux
cargo nextest run --workspace 
    Finished `test` profile [unoptimized] target(s) in 0.05s
────────────
 Nextest run ID 39bfff0e-4637-42e0-905a-bcffb7479a6d with nextest profile: default
    Starting 180 tests across 2 binaries
        PASS [   0.011s] (  1/180) cartridge host::socket::tests::an_owner_only_directory_is_created_and_repaired
        PASS [   0.011s] (  2/180) cartridge lua::tests::a_memory_limit_bounds_what_a_chunk_can_allocate
        PASS [   0.012s] (  3/180) cartridge host::plan::tests::a_listener_accepts_each_declared_sender_for_its_events_only
        PASS [   0.012s] (  4/180) cartridge host::socket::tests::a_symlinked_socket_directory_is_refused
        PASS [   0.012s] (  5/180) cartridge host::socket::tests::a_run_directory_is_owner_only
        PASS [   0.013s] (  6/180) cartridge host::plan::tests::every_event_carries_its_deadline
        PASS [   0.015s] (  7/180) cartridge host::plan::tests::a_private_host_keeps_its_socket_and_ports_to_itself
        PASS [   0.015s] (  8/180) cartridge host::plan::tests::a_cartridge_gets_listeners_only_for_what_it_defines_or_needs
        PASS [   0.016s] (  9/180) cartridge host::plan::tests::no_node_holds_a_token_another_node_accepts_from_someone_else
        PASS [   0.016s] ( 10/180) cartridge host::socket::tests::each_run_owns_its_node_directory_and_a_dead_run_is_swept
        PASS [   0.011s] ( 11/180) cartridge lua::tests::each_file_is_evaluated_in_a_state_of_its_own
        PASS [   0.012s] ( 12/180) cartridge lua::tests::the_interpreter_keeps_computation_and_drops_the_machine
        PASS [   0.010s] ( 13/180) cartridge sandbox::tests::an_empty_command_is_refused_before_launch
        PASS [   0.011s] ( 14/180) cartridge sandbox::tests::a_script_names_its_interpreter
        PASS [   0.012s] ( 15/180) cartridge sandbox::tests::a_write_grant_names_the_canonicalized_path_and_implies_the_read
        PASS [   0.018s] ( 16/180) cartridge lua::tests::a_runaway_is_refused_and_the_state_survives
        PASS [   0.017s] ( 17/180) cartridge sandbox::tests::a_net_grant_turns_the_network_on_and_an_empty_one_leaves_it_off
        PASS [   0.010s] ( 18/180) cartridge sandbox::tests::an_empty_grant_builds_no_allowance_beyond_the_runtime
        PASS [   0.011s] ( 19/180) cartridge sandbox::tests::an_exec_grant_that_resolves_builds_a_literal_and_one_that_does_not_builds_nothing
        PASS [   0.012s] ( 20/180) cartridge sandbox::tests::the_microphone_is_granted_only_when_it_is_asked_for
        PASS [   0.010s] ( 21/180) cartridge sandbox::tests::the_runtime_is_named_canonically
        PASS [   0.014s] ( 22/180) cartridge sandbox::tests::the_prefix_stops_at_a_system_directory
        PASS [   0.010s] ( 23/180) cartridge settings::host::tests::an_undeclared_host_key_leaves_the_declared_defaults_standing
        PASS [   0.014s] ( 24/180) cartridge settings::files::tests::the_listing_reads_each_configuration_file_once
        PASS [   0.037s] ( 25/180) cartridge lua::tests::a_wait_refills_the_budget_and_a_coroutine_does_not
        PASS [   0.042s] ( 26/180) cartridge lua::tests::every_resume_gets_the_budget_back
        PASS [   0.018s] ( 27/180) cartridge tests::host::a_document_refuses_a_bad_schema_or_a_contract_it_does_not_listen_to
        PASS [   0.244s] ( 28/180) cartridge sandbox::tests::an_async_spawn_is_confined_like_the_synchronous_one
        PASS [   0.424s] ( 29/180) cartridge sandbox::tests::an_interpreter_reaches_its_own_installation
        PASS [   0.008s] ( 30/180) cartridge tests::host::a_lifecycle_subscriber_that_falls_behind_is_disconnected
        PASS [   0.080s] ( 31/180) cartridge tests::host::a_missing_listener_waits_and_says_for_what
        PASS [   0.610s] ( 32/180) cartridge sandbox::tests::the_synchronous_command_enforces_the_empty_grant
        PASS [   0.922s] ( 33/180) cartridge tests::host::a_node_presenting_its_own_credential_is_refused_on_the_host_socket
        PASS [   1.547s] ( 34/180) cartridge tests::host::a_call_that_comes_back_into_its_sender_is_answered
        PASS [   1.547s] ( 35/180) cartridge tests::host::a_cartridge_asks_the_host_what_only_the_host_knows
        PASS [   1.558s] ( 36/180) cartridge tests::host::a_cartridge_sends_only_what_it_defines_or_needs
        PASS [   1.557s] ( 37/180) cartridge tests::host::a_granted_env_prefix_reaches_the_node_and_nothing_beside_it_does
        PASS [   1.564s] ( 38/180) cartridge tests::host::a_glob_in_needs_names_what_the_others_listen_to
        PASS [   1.588s] ( 39/180) cartridge tests::host::a_cartridge_answers_the_events_it_listens_to
        PASS [   1.575s] ( 40/180) cartridge tests::host::a_helper_asks_the_base_while_answering
        PASS [   1.313s] ( 41/180) cartridge tests::host::a_native_module_reaches_the_base_through_the_global
        PASS [   1.634s] ( 42/180) cartridge tests::host::a_hung_listener_times_out_and_its_node_keeps_serving
        PASS [   0.801s] ( 43/180) cartridge tests::host::a_spawn_the_grant_did_not_name_is_denied
        PASS [   1.156s] ( 44/180) cartridge tests::host::a_node_refuses_to_listen_to_what_it_did_not_declare
        PASS [   1.107s] ( 45/180) cartridge tests::host::a_pipe_without_fn_answers_on_its_answers_fifo
        PASS [   1.120s] ( 46/180) cartridge tests::host::a_payload_the_schema_rejects_never_reaches_the_listener
        PASS [   1.131s] ( 47/180) cartridge tests::host::a_pipe_wakes_the_node_from_outside
        PASS [   0.915s] ( 48/180) cartridge tests::host::a_schema_only_change_reaches_a_sender_that_already_validated
        PASS [   1.168s] ( 49/180) cartridge tests::host::a_restart_keeps_its_dependents_working
        PASS [   2.134s] ( 50/180) cartridge tests::host::a_stop_request_ends_a_foreground_run
        PASS [   2.144s] ( 51/180) cartridge tests::host::a_spawned_program_answers_requests_by_id
        PASS [   2.185s] ( 52/180) cartridge tests::host::a_spawned_helper_sees_only_the_two_named_cartridge_variables_and_a_path
        PASS [   0.010s] ( 53/180) cartridge tests::host::an_untrusted_descriptor_is_refused_where_it_is_enforced
        PASS [   2.172s] ( 54/180) cartridge tests::host::a_stopped_cartridge_takes_its_programs_along
        PASS [   0.013s] ( 55/180) cartridge tests::host::grant_paths_name_the_project_and_settings
        PASS [   2.151s] ( 56/180) cartridge tests::host::a_waiting_cartridge_starts_when_the_descriptor_adds_its_listener
        PASS [   0.014s] ( 57/180) cartridge tests::host::solo_entries_sharing_a_socket_name_are_refused
        PASS [   0.197s] ( 58/180) cartridge tests::host::an_undeclared_event_fails_the_cartridge_before_it_starts
        PASS [   4.141s] ( 59/180) cartridge tests::host::a_node_serves_other_events_while_a_handler_waits
        PASS [   1.010s] ( 60/180) cartridge tests::host::one_cartridge_cannot_see_anothers_globals
        PASS [   1.084s] ( 61/180) cartridge tests::host::an_event_declared_twice_fails_the_later_entry
        PASS [   1.057s] ( 62/180) cartridge tests::host::gather_and_emit_reach_every_listener
        PASS [   0.010s] ( 63/180) cartridge tests::ledger::a_root_that_does_not_exist_is_an_empty_ledger
        PASS [   0.012s] ( 64/180) cartridge tests::ledger::an_entry_is_its_path_from_the_root
        PASS [   0.012s] ( 65/180) cartridge tests::ledger::an_unreadable_document_is_an_entry_with_its_reason
        PASS [   0.906s] ( 66/180) cartridge tests::host::the_host_socket_answers_the_command_line
        PASS [   0.012s] ( 67/180) cartridge tests::ledger::two_entries_of_one_scope_offering_one_key_is_a_clash
        PASS [   0.010s] ( 68/180) cartridge tests::node::the_entry_recheck_refuses_bytes_that_changed
        PASS [   0.010s] ( 69/180) cartridge tests::settings::keys_inside_an_absent_optional_table_stay_absent
        PASS [   0.012s] ( 70/180) cartridge tests::settings::an_untrusted_project_config_is_refused_at_its_read
        PASS [   0.008s] ( 71/180) cartridge tests::settings::naming_the_table_fills_the_keys_inside_it
        PASS [   0.012s] ( 72/180) cartridge tests::settings::yolo_overrides_the_configured_value_only_where_the_cartridge_declares_it
        PASS [   0.010s] ( 73/180) cartridge trace::tests::a_credential_or_a_prompt_body_is_omitted_and_named
        PASS [   0.011s] ( 74/180) cartridge trace::tests::a_full_diagnostics_queue_drops_records_and_says_how_many
        PASS [   0.013s] ( 75/180) cartridge trace::tests::a_sink_that_cannot_repair_a_failed_write_stops_accepting_records
        PASS [   0.012s] ( 76/180) cartridge trace::tests::oversized_records_are_valid_json_and_bounded_before_and_after_rotation
        PASS [   0.009s] ( 77/180) cartridge trace::tests::redaction_reaches_objects_inside_nested_arrays
        PASS [   0.016s] ( 78/180) cartridge trace::tests::the_sink_stays_bounded_by_rotating_one_generation
        PASS [   0.016s] ( 79/180) cartridge transport::cartridge::tests::a_cartridge_sends_a_declared_event_and_takes_the_answer
        PASS [   0.060s] ( 80/180) cartridge transport::cartridge::tests::a_connection_runs_at_most_its_in_flight_limit_at_once
        PASS [   0.022s] ( 81/180) cartridge transport::cartridge::tests::a_directory_update_replaces_the_schema_a_node_validates_against
        PASS [   0.025s] ( 82/180) cartridge transport::cartridge::tests::a_listener_checks_what_arrives_whatever_the_sender_checked
        PASS [   0.068s] ( 83/180) cartridge transport::cartridge::tests::a_listener_that_does_not_answer_reaches_the_log
        PASS [   0.011s] ( 84/180) cartridge transport::cartridge::tests::a_peer_token_sends_events_and_nothing_else
        PASS [   0.165s] ( 85/180) cartridge transport::cartridge::tests::a_send_reconnects_after_the_listener_restarts
        PASS [   0.011s] ( 86/180) cartridge transport::cartridge::tests::a_subscriber_gets_the_replay_and_then_live_events
        PASS [   0.020s] ( 87/180) cartridge transport::cartridge::tests::an_undeclared_event_or_a_bad_payload_is_refused_before_sending
        PASS [   0.009s] ( 88/180) cartridge transport::cartridge::tests::an_unknown_token_is_refused_and_disconnected
        PASS [   0.010s] ( 89/180) cartridge transport::cartridge::tests::events_reach_listeners_directly
        PASS [   1.572s] ( 90/180) cartridge tests::host::streams_replay_and_then_deliver_live
        PASS [   0.602s] ( 91/180) cartridge tests::host::verify_sends_every_declared_contract
        PASS [   0.017s] ( 92/180) cartridge transport::rpc::tests::a_call_gets_its_result
        PASS [   0.011s] ( 93/180) cartridge transport::rpc::tests::a_request_dropped_unanswered_is_answered_with_an_internal_error
        PASS [   0.833s] ( 94/180) cartridge tests::host::two_cartridges_that_need_each_other_both_start_when_one_asks_with_a_question_mark
        PASS [   0.010s] ( 95/180) cartridge transport::rpc::tests::an_oversized_frame_closes_a_capped_connection
        PASS [   3.804s] ( 96/180) cartridge tests::host::a_terminated_mcp_exits_with_its_input_still_open
        PASS [   0.010s] ( 97/180) cartridge transport::rpc::tests::dropping_the_last_handle_closes_the_connection
        PASS [   0.010s] ( 98/180) cartridge transport::rpc::tests::errors_cross_as_error_objects
        PASS [   0.010s] ( 99/180) cartridge transport::rpc::tests::notifications_arrive_without_an_id
        PASS [   0.598s] (100/180) cartridge tests::settings::refused_settings_do_not_wedge_the_process_when_diagnostics_are_on
        PASS [   0.026s] (101/180) cartridge transport::rpc::tests::closing_fails_waiting_calls
        PASS [   0.011s] (102/180) cartridge transport::typed::bind_tests_unix::a_bound_socket_is_owner_only
        PASS [   0.009s] (103/180) cartridge transport::typed::bind_tests_unix::a_live_endpoint_served_by_another_uid_refuses_the_bind
        PASS [   0.011s] (104/180) cartridge transport::typed::bind_tests_unix::a_live_owner_reports_already_running
        PASS [   0.009s] (105/180) cartridge transport::typed::bind_tests_unix::a_rebound_stale_socket_is_also_owner_only
        PASS [   0.009s] (106/180) cartridge transport::typed::bind_tests_unix::a_regular_file_squatting_the_name_is_refused_not_removed
        PASS [   0.011s] (107/180) cartridge transport::typed::bind_tests_unix::a_socket_is_owner_only_even_under_a_permissive_umask
        PASS [   0.008s] (108/180) cartridge transport::typed::bind_tests_unix::a_stale_socket_file_is_removed_and_rebound
        PASS [   0.009s] (109/180) cartridge transport::typed::bind_tests_unix::a_symlink_to_a_foreign_target_refuses_the_bind
        PASS [   0.009s] (110/180) cartridge transport::typed::owner_tests_unix::a_dangling_symlink_is_refused
        PASS [   0.066s] (111/180) cartridge transport::rpc::tests::calls_run_concurrently_and_match_by_id
        PASS [   0.009s] (112/180) cartridge transport::typed::owner_tests_unix::a_path_owned_by_another_uid_is_refused
        PASS [   0.011s] (113/180) cartridge transport::typed::owner_tests_unix::a_missing_path_reads_as_absence_not_as_a_squat
        PASS [   0.010s] (114/180) cartridge transport::typed::owner_tests_unix::a_path_this_user_owns_is_accepted
        PASS [   0.010s] (115/180) cartridge transport::typed::owner_tests_unix::a_symlink_to_a_foreign_target_is_refused
        PASS [   0.010s] (116/180) cartridge transport::typed::owner_tests_unix::connect_accepts_a_socket_this_user_bound
        PASS [   0.013s] (117/180) cartridge transport::typed::owner_tests_unix::a_regular_file_is_not_an_endpoint
        PASS [   0.010s] (118/180) cartridge transport::typed::owner_tests_unix::connect_refuses_a_foreign_endpoint_before_it_connects
        PASS [   0.009s] (119/180) cartridge transport::typed::owner_tests_unix::connect_refuses_when_the_peer_uid_differs
        PASS [   0.011s] (120/180) cartridge transport::typed::typed_tests::a_root_that_does_not_exist_yet_tags_the_same_from_every_spelling
        PASS [   0.011s] (121/180) cartridge transport::typed::owner_tests_unix::the_peer_check_reads_the_server_uid_and_decides_both_ways
        PASS [   0.009s] (122/180) cartridge transport::typed::typed_tests::cwd_tag_tests::path_tag_is_stable_and_nonempty
        PASS [   0.008s] (123/180) cartridge transport::typed::typed_tests::tests::io_error_into_codec_is_a_decode_carrying_the_original_message
        PASS [   0.009s] (124/180) cartridge transport::typed::typed_tests::tests::serde_error_into_codec_preserves_the_serde_message
        PASS [   0.011s] (125/180) cartridge transport::typed::typed_tests::tests::rpc_error_absorbs_adapter_and_codec_via_from
        PASS [   0.010s] (126/180) cartridge transport::typed::typed_tests::tests_2::inproc_reader_drains_leftover_across_small_reads
        PASS [   0.010s] (127/180) cartridge transport::typed::typed_tests::tests_3::json_decodes_multiple_frames_from_one_buffer
        PASS [   0.010s] (128/180) cartridge transport::typed::typed_tests::tests_3::json_partial_line_yields_none_until_newline
        PASS [   0.014s] (129/180) cartridge transport::typed::typed_tests::tests_3::json_many_consecutive_newlines_do_not_overflow
        PASS [   0.009s] (130/180) cartridge transport::typed::typed_tests::tests_3::json_roundtrip_single_frame
        PASS [   0.011s] (131/180) cartridge transport::typed::typed_tests::tests_3::json_tolerates_crlf_and_skips_blank_lines
        PASS [   0.009s] (132/180) cartridge transport::typed::typed_tests::tests_4::channel_roundtrip_json_envelope
        PASS [   0.008s] (133/180) cartridge transport::typed::typed_tests::tests_4::recv_returns_none_on_closed_adapter
        PASS [   0.009s] (134/180) cartridge transport::typed::typed_tests::the_tag_is_the_same_before_and_after_the_root_is_created
        PASS [   0.011s] (135/180) cartridge trust::tests::a_built_native_module_is_not_a_source_so_a_test_build_keeps_the_cartridge
        PASS [   0.009s] (136/180) cartridge trust::tests::a_deleted_project_can_still_be_untrusted
        PASS [   0.014s] (137/180) cartridge trust::tests::a_changed_file_stops_being_trusted
        PASS [   0.009s] (138/180) cartridge trust::tests::a_digest_is_the_files_own_sha_256
        PASS [   0.010s] (139/180) cartridge trust::tests::a_file_the_record_does_not_name_is_refused
        PASS [   0.010s] (140/180) cartridge trust::tests::a_file_under_a_skipped_directory_names_the_real_dead_end
        PASS [   0.010s] (141/180) cartridge trust::tests::a_global_config_symlinked_out_of_the_home_still_passes
        PASS [   0.012s] (142/180) cartridge trust::tests::a_nested_record_does_not_shadow_a_fresh_outer_one
        PASS [   0.010s] (143/180) cartridge trust::tests::a_widened_grant_untrusts_its_manifest
        PASS [   0.217s] (144/180) cartridge transport::cartridge::tests::gather_reports_every_listener_outcome
        PASS [   0.012s] (145/180) cartridge trust::tests::an_untrusted_bare_lua_entry_is_refused_at_its_resolve
        PASS [   0.012s] (146/180) cartridge trust::tests::an_untrusted_project_is_refused_until_it_is_trusted
        PASS [   0.013s] (147/180) cartridge trust::tests::every_spelling_of_a_directory_is_one_record
        PASS [   0.013s] (148/180) cartridge trust::tests::read_refuses_a_file_that_changed_after_it_was_trusted
        PASS [   0.013s] (149/180) cartridge trust::tests::revoking_a_project_takes_its_nested_records
        PASS [   0.013s] (150/180) cartridge trust::tests::the_store_is_private_to_this_user
        PASS [   0.013s] (151/180) cartridge trust::tests::the_users_own_home_needs_no_trust
        PASS [   0.011s] (152/180) cartridge trust::tests::yolo_trusts_a_file_changed_after_the_record_but_still_lists_it_pending
        PASS [   0.015s] (153/180) cartridge trust::tests::the_walk_skips_build_output_and_links
        PASS [   0.012s] (154/180) cartridge::bin/cartridge cli::host::stdio_tests::mcp_bridge_failure_preserves_request_ids_without_replay
        PASS [   0.015s] (155/180) cartridge::bin/cartridge cli::host::stdio_tests::mcp_bridge_keeps_notifications_silent_and_successes_intact
        PASS [   0.013s] (156/180) cartridge::bin/cartridge cli::host::stdio_tests::only_trust_refusals_prompt_an_attach_reload
        PASS [   0.012s] (157/180) cartridge::bin/cartridge cli::host::stdio_tests::settled_not_on_an_empty_composition
        PASS [   0.013s] (158/180) cartridge::bin/cartridge cli::host::stdio_tests::settled_not_while_the_key_is_starting
        PASS [   0.013s] (159/180) cartridge::bin/cartridge cli::host::stdio_tests::settled_when_nothing_is_left_starting
        PASS [   0.010s] (160/180) cartridge::bin/cartridge cli::host::stdio_tests::settled_when_the_key_is_active
        PASS [   0.009s] (161/180) cartridge::bin/cartridge cli::listing::tests::the_listing_follows_sends_and_marks_cycles_and_missing_listeners
        PASS [   0.263s] (162/180) cartridge transport::typed::bind_tests_unix::a_caller_of_another_uid_is_refused_and_the_listener_keeps_serving
        PASS [   0.009s] (163/180) cartridge::bin/cartridge cli::manual::tests::addresses_resolve_and_search_lands_in_the_section
        PASS [   0.010s] (164/180) cartridge::bin/cartridge cli::settings::tests::lua_keys_and_values_render_as_lua_source
        PASS [   0.115s] (165/180) cartridge::bin/cartridge cli::host::signal_tests::a_terminate_stops_the_host
        PASS [   0.010s] (166/180) cartridge::bin/cartridge cli::setup::tests::a_folder_in_the_way_of_a_link_is_refused
        PASS [   0.013s] (167/180) cartridge::bin/cartridge cli::setup::tests::a_file_changed_by_the_exchange_is_not_recorded
        PASS [   0.013s] (168/180) cartridge::bin/cartridge cli::setup::tests::a_setup_or_doctor_event_the_cartridge_does_not_listen_to_is_refused
        PASS [   0.014s] (169/180) cartridge::bin/cartridge cli::setup::tests::setup_offers_what_it_finds_and_the_catalog_and_filters_by_subsequence
        PASS [   0.018s] (170/180) cartridge::bin/cartridge cli::setup::tests::setup_trusts_what_it_chose_not_what_the_tree_holds
        PASS [   0.015s] (171/180) cartridge::bin/cartridge cli::trust::tests::an_explicit_path_trusts_a_folder_that_is_neither
        PASS [   0.012s] (172/180) cartridge::bin/cartridge cli::width::tests::fit_and_pad_count_display_cells
        PASS [   0.317s] (173/180) cartridge::bin/cartridge cli::host::signal_tests::an_interrupt_is_ignored_while_a_program_holds_the_terminal
        PASS [   5.660s] (174/180) cartridge tests::host::a_node_that_catches_its_own_refusal_exits
        PASS [   0.954s] (175/180) cartridge trust::tests::a_deleted_project_is_untrusted_by_a_relative_path
        PASS [   0.936s] (176/180) cartridge trust::tests::a_relative_or_empty_home_is_refused_rather_than_trust_disabling
        PASS [   0.782s] (177/180) cartridge::bin/cartridge cli::setup::tests::setup_links_the_chosen_writes_a_descriptor_the_host_reads_and_lets_a_cartridge_ask
        PASS [   6.460s] (178/180) cartridge tests::host::a_spinning_handler_is_refused_and_its_node_keeps_serving
        PASS [   4.247s] (179/180) cartridge tests::settings::a_configuration_file_that_never_returns_is_refused
        PASS [   9.404s] (180/180) cartridge tests::host::a_rewritten_native_module_restarts_only_on_reload
────────────
     Summary [  11.045s] 180 tests run: 180 passed, 0 skipped
test      cartridge  pass

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/cartridge-mcp-waits-for-a-cold-host-to-settle-instead-of-giving-up-after-three-identical-polls/specs/spec01.md: exit 0

Command SHA-256: 57b5e4de29be3c697542ca32eaf391144065f2b012a6b03b9bc753d67623507f

```text
starting the host for .cartridge (log: .cartridge/daemon.log)
2026-09-17T11:17:56.693088Z  WARN mcp: `mcp` is not provided
{"error":{"code":-32603,"message":"`mcp` is not provided"},"id":2,"jsonrpc":"2.0"}
the missing mcp listener was named in 1s, inside the 60 s startup deadline

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/cartridge-mcp-waits-for-a-cold-host-to-settle-instead-of-giving-up-after-three-identical-polls/specs/spec01.md: exit 0

Command SHA-256: f1fe98cda1a9212ef7125781e413a3848b2be44ef208de85379194cb3701c386

```text
toolchain: cargo cargo-nextest bun tmux
bun test v1.3.14 (0d9b296a)

 13 pass
 0 fail
 1306 expect() calls
Ran 13 tests across 1 file. [47.07s]
test      lifecycle  pass

```
