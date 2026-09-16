---
commit: f364f46f77c2f84345fe4cc5850c6182c0754568
spec-digests: {"spec01.md":"60cca74321d5339172563daf8163a9db2c11a64c92e1d9d51f1ebf7950f1c1ba"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently/specs/spec01.md: exit 0

Command SHA-256: f94fba658d2f5241b133490b72c1a230ff88c9b6b145320daca6b1877ff1da43

```text

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently/specs/spec01.md: exit 0

Command SHA-256: d6deee4789080f25caa37b6f9d3e8c297c5263b17da60d29d5c9ba8a37e3d5b1

```text
toolchain: cargo cargo-nextest bun tmux
cargo fmt --all --check
cargo clippy --workspace --all-targets
   Compiling cartridge v0.1.0 (/Users/feb/dev/cartridge/cartridge.ctg)
    Finished `dev` profile [unoptimized] target(s) in 2.13s
check     cartridge  pass

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently/specs/spec01.md: exit 0

Command SHA-256: b0660102351e5641666e0d7024400252249ea3a793661d9f0b7c54913b21e5e3

```text
toolchain: cargo cargo-nextest bun tmux
cargo nextest run --workspace 
   Compiling cartridge v0.1.0 (/Users/feb/dev/cartridge/cartridge.ctg)
    Finished `test` profile [unoptimized] target(s) in 3.28s
────────────
 Nextest run ID 4e98f9bd-4ec7-40ca-a310-aa01326369b5 with nextest profile: default
    Starting 169 tests across 2 binaries
        PASS [   0.031s] (  1/169) cartridge host::socket::tests::an_owner_only_directory_is_created_and_repaired
        PASS [   0.031s] (  2/169) cartridge host::socket::tests::a_run_directory_is_owner_only
        PASS [   0.036s] (  3/169) cartridge lua::tests::a_memory_limit_bounds_what_a_chunk_can_allocate
        PASS [   0.037s] (  4/169) cartridge host::plan::tests::a_listener_accepts_each_declared_sender_for_its_events_only
        PASS [   0.038s] (  5/169) cartridge host::socket::tests::each_run_owns_its_node_directory_and_a_dead_run_is_swept
        PASS [   0.038s] (  6/169) cartridge host::plan::tests::a_cartridge_gets_listeners_only_for_what_it_defines_or_needs
        PASS [   0.038s] (  7/169) cartridge host::plan::tests::every_event_carries_its_deadline
        PASS [   0.038s] (  8/169) cartridge host::socket::tests::a_symlinked_socket_directory_is_refused
        PASS [   0.038s] (  9/169) cartridge host::plan::tests::a_private_host_keeps_its_socket_and_ports_to_itself
        PASS [   0.038s] ( 10/169) cartridge host::plan::tests::no_node_holds_a_token_another_node_accepts_from_someone_else
        PASS [   0.016s] ( 11/169) cartridge lua::tests::the_interpreter_keeps_computation_and_drops_the_machine
        PASS [   0.017s] ( 12/169) cartridge sandbox::tests::a_net_grant_turns_the_network_on_and_an_empty_one_leaves_it_off
        PASS [   0.019s] ( 13/169) cartridge sandbox::tests::a_script_names_its_interpreter
        PASS [   0.023s] ( 14/169) cartridge lua::tests::each_file_is_evaluated_in_a_state_of_its_own
        PASS [   0.031s] ( 15/169) cartridge lua::tests::a_runaway_is_refused_and_the_state_survives
        PASS [   0.024s] ( 16/169) cartridge sandbox::tests::a_write_grant_names_the_canonicalized_path_and_implies_the_read
        PASS [   0.014s] ( 17/169) cartridge sandbox::tests::an_empty_grant_builds_no_allowance_beyond_the_runtime
        PASS [   0.017s] ( 18/169) cartridge sandbox::tests::an_exec_grant_that_resolves_builds_a_literal_and_one_that_does_not_builds_nothing
        PASS [   0.015s] ( 19/169) cartridge sandbox::tests::the_runtime_is_named_canonically
        PASS [   0.016s] ( 20/169) cartridge sandbox::tests::the_prefix_stops_at_a_system_directory
        PASS [   0.014s] ( 21/169) cartridge settings::files::tests::the_listing_reads_each_configuration_file_once
        PASS [   0.054s] ( 22/169) cartridge lua::tests::a_wait_refills_the_budget_and_a_coroutine_does_not
        PASS [   0.015s] ( 23/169) cartridge settings::host::tests::an_undeclared_host_key_leaves_the_declared_defaults_standing
        PASS [   0.062s] ( 24/169) cartridge lua::tests::every_resume_gets_the_budget_back
        PASS [   0.020s] ( 25/169) cartridge tests::host::a_document_refuses_a_bad_schema_or_a_contract_it_does_not_listen_to
        LEAK [   0.217s] ( 26/169) cartridge sandbox::tests::an_empty_command_is_refused_before_launch
        PASS [   0.250s] ( 27/169) cartridge sandbox::tests::an_async_spawn_is_confined_like_the_synchronous_one
        PASS [   0.426s] ( 28/169) cartridge sandbox::tests::the_synchronous_command_enforces_the_empty_grant
        PASS [   0.008s] ( 29/169) cartridge tests::host::a_lifecycle_subscriber_that_falls_behind_is_disconnected
        PASS [   0.524s] ( 30/169) cartridge sandbox::tests::an_interpreter_reaches_its_own_installation
        PASS [   1.105s] ( 31/169) cartridge tests::host::a_missing_listener_waits_and_says_for_what
        PASS [   1.717s] ( 32/169) cartridge tests::host::a_cartridge_asks_the_host_what_only_the_host_knows
        PASS [   1.705s] ( 33/169) cartridge tests::host::a_granted_env_prefix_reaches_the_node_and_nothing_beside_it_does
        PASS [   1.737s] ( 34/169) cartridge tests::host::a_call_that_comes_back_into_its_sender_is_answered
        PASS [   1.744s] ( 35/169) cartridge tests::host::a_cartridge_sends_only_what_it_defines_or_needs
        PASS [   1.819s] ( 36/169) cartridge tests::host::a_hung_listener_times_out_and_its_node_keeps_serving
        PASS [   0.580s] ( 37/169) cartridge tests::host::a_pipe_wakes_the_node_from_outside
        PASS [   0.866s] ( 38/169) cartridge tests::host::a_payload_the_schema_rejects_never_reaches_the_listener
        PASS [   0.896s] ( 39/169) cartridge tests::host::a_node_refuses_to_listen_to_what_it_did_not_declare
        PASS [   2.605s] ( 40/169) cartridge tests::host::a_glob_in_needs_names_what_the_others_listen_to
        PASS [   1.106s] ( 41/169) cartridge tests::host::a_node_presenting_its_own_credential_is_refused_on_the_host_socket
        PASS [   2.479s] ( 42/169) cartridge tests::host::a_helper_asks_the_base_while_answering
        PASS [   2.659s] ( 43/169) cartridge tests::host::a_cartridge_answers_the_events_it_listens_to
        PASS [   2.368s] ( 44/169) cartridge tests::host::a_native_module_reaches_the_base_through_the_global
        PASS [   1.138s] ( 45/169) cartridge tests::host::a_spawned_program_answers_requests_by_id
        PASS [   1.110s] ( 46/169) cartridge tests::host::a_stop_request_ends_a_foreground_run
        PASS [   1.154s] ( 47/169) cartridge tests::host::a_spawn_the_grant_did_not_name_is_denied
        PASS [   0.905s] ( 48/169) cartridge tests::host::a_stopped_cartridge_takes_its_programs_along
        PASS [   1.163s] ( 49/169) cartridge tests::host::a_spawned_helper_sees_only_the_two_named_cartridge_variables_and_a_path
        PASS [   0.021s] ( 50/169) cartridge tests::host::an_untrusted_descriptor_is_refused_where_it_is_enforced
        PASS [   1.251s] ( 51/169) cartridge tests::host::a_schema_only_change_reaches_a_sender_that_already_validated
        PASS [   0.026s] ( 52/169) cartridge tests::host::grant_paths_name_the_project_and_settings
        PASS [   1.307s] ( 53/169) cartridge tests::host::a_restart_keeps_its_dependents_working
        PASS [   0.014s] ( 54/169) cartridge tests::host::solo_entries_sharing_a_socket_name_are_refused
        PASS [   0.289s] ( 55/169) cartridge tests::host::an_undeclared_event_fails_the_cartridge_before_it_starts
        PASS [   1.208s] ( 56/169) cartridge tests::host::gather_and_emit_reach_every_listener
        PASS [   1.254s] ( 57/169) cartridge tests::host::an_event_declared_twice_fails_the_later_entry
        PASS [   1.137s] ( 58/169) cartridge tests::host::one_cartridge_cannot_see_anothers_globals
        PASS [   0.012s] ( 59/169) cartridge tests::ledger::a_root_that_does_not_exist_is_an_empty_ledger
        PASS [   0.012s] ( 60/169) cartridge tests::ledger::an_entry_is_its_path_from_the_root
        PASS [   1.114s] ( 61/169) cartridge tests::host::streams_replay_and_then_deliver_live
        PASS [   0.981s] ( 62/169) cartridge tests::host::the_host_socket_answers_the_command_line
        PASS [   0.015s] ( 63/169) cartridge tests::ledger::an_unreadable_document_is_an_entry_with_its_reason
        PASS [   0.015s] ( 64/169) cartridge tests::ledger::two_entries_of_one_scope_offering_one_key_is_a_clash
        PASS [   0.013s] ( 65/169) cartridge tests::node::the_entry_recheck_refuses_bytes_that_changed
        PASS [   0.011s] ( 66/169) cartridge tests::settings::an_untrusted_project_config_is_refused_at_its_read
        PASS [   0.009s] ( 67/169) cartridge tests::settings::naming_the_table_fills_the_keys_inside_it
        PASS [   0.011s] ( 68/169) cartridge tests::settings::keys_inside_an_absent_optional_table_stay_absent
        PASS [   0.009s] ( 69/169) cartridge tests::settings::yolo_overrides_the_configured_value_only_where_the_cartridge_declares_it
        PASS [   0.011s] ( 70/169) cartridge trace::tests::a_credential_or_a_prompt_body_is_omitted_and_named
        PASS [   0.009s] ( 71/169) cartridge trace::tests::a_full_diagnostics_queue_drops_records_and_says_how_many
        PASS [   0.010s] ( 72/169) cartridge trace::tests::a_sink_that_cannot_repair_a_failed_write_stops_accepting_records
        PASS [   0.011s] ( 73/169) cartridge trace::tests::oversized_records_are_valid_json_and_bounded_before_and_after_rotation
        PASS [   0.012s] ( 74/169) cartridge trace::tests::redaction_reaches_objects_inside_nested_arrays
        PASS [   1.337s] ( 75/169) cartridge tests::host::a_waiting_cartridge_starts_when_the_descriptor_adds_its_listener
        PASS [   0.025s] ( 76/169) cartridge trace::tests::the_sink_stays_bounded_by_rotating_one_generation
        PASS [   0.025s] ( 77/169) cartridge transport::cartridge::tests::a_cartridge_sends_a_declared_event_and_takes_the_answer
        PASS [   0.022s] ( 78/169) cartridge transport::cartridge::tests::a_directory_update_replaces_the_schema_a_node_validates_against
        PASS [   0.026s] ( 79/169) cartridge transport::cartridge::tests::a_listener_checks_what_arrives_whatever_the_sender_checked
        PASS [   0.013s] ( 80/169) cartridge transport::cartridge::tests::a_peer_token_sends_events_and_nothing_else
        PASS [   0.013s] ( 81/169) cartridge transport::cartridge::tests::a_subscriber_gets_the_replay_and_then_live_events
        PASS [   0.078s] ( 82/169) cartridge transport::cartridge::tests::a_connection_runs_at_most_its_in_flight_limit_at_once
        PASS [   0.015s] ( 83/169) cartridge transport::cartridge::tests::an_undeclared_event_or_a_bad_payload_is_refused_before_sending
        PASS [   0.010s] ( 84/169) cartridge transport::cartridge::tests::an_unknown_token_is_refused_and_disconnected
        PASS [   0.010s] ( 85/169) cartridge transport::cartridge::tests::events_reach_listeners_directly
        PASS [   0.008s] ( 86/169) cartridge transport::rpc::tests::a_call_gets_its_result
        PASS [   0.007s] ( 87/169) cartridge transport::rpc::tests::a_request_dropped_unanswered_is_answered_with_an_internal_error
        PASS [   0.007s] ( 88/169) cartridge transport::rpc::tests::an_oversized_frame_closes_a_capped_connection
        PASS [   0.059s] ( 89/169) cartridge transport::rpc::tests::calls_run_concurrently_and_match_by_id
        PASS [   0.018s] ( 90/169) cartridge transport::rpc::tests::closing_fails_waiting_calls
        PASS [   0.006s] ( 91/169) cartridge transport::rpc::tests::dropping_the_last_handle_closes_the_connection
        PASS [   0.007s] ( 92/169) cartridge transport::rpc::tests::errors_cross_as_error_objects
        PASS [   0.007s] ( 93/169) cartridge transport::rpc::tests::notifications_arrive_without_an_id
        PASS [   0.169s] ( 94/169) cartridge transport::cartridge::tests::a_send_reconnects_after_the_listener_restarts
        PASS [   0.008s] ( 95/169) cartridge transport::typed::bind_tests_unix::a_bound_socket_is_owner_only
        PASS [   0.009s] ( 96/169) cartridge transport::typed::bind_tests_unix::a_live_endpoint_served_by_another_uid_refuses_the_bind
        PASS [   0.008s] ( 97/169) cartridge transport::typed::bind_tests_unix::a_live_owner_reports_already_running
        PASS [   0.007s] ( 98/169) cartridge transport::typed::bind_tests_unix::a_rebound_stale_socket_is_also_owner_only
        PASS [   0.009s] ( 99/169) cartridge transport::typed::bind_tests_unix::a_regular_file_squatting_the_name_is_refused_not_removed
        PASS [   0.008s] (100/169) cartridge transport::typed::bind_tests_unix::a_socket_is_owner_only_even_under_a_permissive_umask
        PASS [   0.008s] (101/169) cartridge transport::typed::bind_tests_unix::a_stale_socket_file_is_removed_and_rebound
        PASS [   0.008s] (102/169) cartridge transport::typed::bind_tests_unix::a_symlink_to_a_foreign_target_refuses_the_bind
        PASS [   0.008s] (103/169) cartridge transport::typed::owner_tests_unix::a_dangling_symlink_is_refused
        PASS [   0.007s] (104/169) cartridge transport::typed::owner_tests_unix::a_missing_path_reads_as_absence_not_as_a_squat
        PASS [   0.208s] (105/169) cartridge transport::cartridge::tests::gather_reports_every_listener_outcome
        PASS [   0.007s] (106/169) cartridge transport::typed::owner_tests_unix::a_path_owned_by_another_uid_is_refused
        PASS [   0.007s] (107/169) cartridge transport::typed::owner_tests_unix::a_path_this_user_owns_is_accepted
        PASS [   0.008s] (108/169) cartridge transport::typed::owner_tests_unix::a_regular_file_is_not_an_endpoint
        PASS [   0.007s] (109/169) cartridge transport::typed::owner_tests_unix::connect_accepts_a_socket_this_user_bound
        PASS [   0.011s] (110/169) cartridge transport::typed::owner_tests_unix::a_symlink_to_a_foreign_target_is_refused
        PASS [   0.007s] (111/169) cartridge transport::typed::owner_tests_unix::connect_refuses_a_foreign_endpoint_before_it_connects
        PASS [   0.010s] (112/169) cartridge transport::typed::owner_tests_unix::connect_refuses_when_the_peer_uid_differs
        PASS [   0.008s] (113/169) cartridge transport::typed::owner_tests_unix::the_peer_check_reads_the_server_uid_and_decides_both_ways
        PASS [   0.006s] (114/169) cartridge transport::typed::typed_tests::cwd_tag_tests::path_tag_is_stable_and_nonempty
        PASS [   0.010s] (115/169) cartridge transport::typed::typed_tests::a_root_that_does_not_exist_yet_tags_the_same_from_every_spelling
        PASS [   0.006s] (116/169) cartridge transport::typed::typed_tests::tests::io_error_into_codec_is_a_decode_carrying_the_original_message
        PASS [   0.009s] (117/169) cartridge transport::typed::typed_tests::tests::rpc_error_absorbs_adapter_and_codec_via_from
        PASS [   0.008s] (118/169) cartridge transport::typed::typed_tests::tests::serde_error_into_codec_preserves_the_serde_message
        PASS [   0.007s] (119/169) cartridge transport::typed::typed_tests::tests_2::inproc_reader_drains_leftover_across_small_reads
        PASS [   0.006s] (120/169) cartridge transport::typed::typed_tests::tests_3::json_decodes_multiple_frames_from_one_buffer
        PASS [   0.012s] (121/169) cartridge transport::typed::typed_tests::tests_3::json_many_consecutive_newlines_do_not_overflow
        PASS [   0.009s] (122/169) cartridge transport::typed::typed_tests::tests_3::json_partial_line_yields_none_until_newline
        PASS [   0.006s] (123/169) cartridge transport::typed::typed_tests::tests_3::json_tolerates_crlf_and_skips_blank_lines
        PASS [   0.009s] (124/169) cartridge transport::typed::typed_tests::tests_3::json_roundtrip_single_frame
        PASS [   0.006s] (125/169) cartridge transport::typed::typed_tests::tests_4::recv_returns_none_on_closed_adapter
        PASS [   0.010s] (126/169) cartridge transport::typed::typed_tests::tests_4::channel_roundtrip_json_envelope
        PASS [   0.009s] (127/169) cartridge transport::typed::typed_tests::the_tag_is_the_same_before_and_after_the_root_is_created
        PASS [   0.013s] (128/169) cartridge trust::tests::a_built_native_module_is_a_source_so_its_rebuild_restarts_the_cartridge
        PASS [   0.010s] (129/169) cartridge trust::tests::a_changed_file_stops_being_trusted
        PASS [   0.012s] (130/169) cartridge trust::tests::a_deleted_project_can_still_be_untrusted
        PASS [   0.009s] (131/169) cartridge trust::tests::a_digest_is_the_files_own_sha_256
        PASS [   0.011s] (132/169) cartridge trust::tests::a_file_the_record_does_not_name_is_refused
        PASS [   0.012s] (133/169) cartridge trust::tests::a_file_under_a_skipped_directory_names_the_real_dead_end
        PASS [   0.010s] (134/169) cartridge trust::tests::a_global_config_symlinked_out_of_the_home_still_passes
        PASS [   0.011s] (135/169) cartridge trust::tests::a_nested_record_does_not_shadow_a_fresh_outer_one
        PASS [   0.263s] (136/169) cartridge transport::typed::bind_tests_unix::a_caller_of_another_uid_is_refused_and_the_listener_keeps_serving
        PASS [   0.011s] (137/169) cartridge trust::tests::a_widened_grant_untrusts_its_manifest
        PASS [   0.010s] (138/169) cartridge trust::tests::an_untrusted_bare_lua_entry_is_refused_at_its_resolve
        PASS [   0.009s] (139/169) cartridge trust::tests::an_untrusted_project_is_refused_until_it_is_trusted
        PASS [   0.009s] (140/169) cartridge trust::tests::every_spelling_of_a_directory_is_one_record
        PASS [   0.010s] (141/169) cartridge trust::tests::read_refuses_a_file_that_changed_after_it_was_trusted
        PASS [   3.900s] (142/169) cartridge tests::host::a_node_serves_other_events_while_a_handler_waits
        PASS [   0.011s] (143/169) cartridge trust::tests::the_store_is_private_to_this_user
        PASS [   0.014s] (144/169) cartridge trust::tests::revoking_a_project_takes_its_nested_records
        PASS [   0.009s] (145/169) cartridge trust::tests::the_users_own_home_needs_no_trust
        PASS [   0.011s] (146/169) cartridge trust::tests::the_walk_skips_build_output_and_links
        PASS [   0.113s] (147/169) cartridge::bin/cartridge cli::host::signal_tests::a_terminate_stops_the_host
        PASS [   0.007s] (148/169) cartridge::bin/cartridge cli::host::stdio_tests::mcp_bridge_failure_preserves_request_ids_without_replay
        PASS [   0.007s] (149/169) cartridge::bin/cartridge cli::host::stdio_tests::mcp_bridge_keeps_notifications_silent_and_successes_intact
        PASS [   0.007s] (150/169) cartridge::bin/cartridge cli::listing::tests::the_listing_follows_sends_and_marks_cycles_and_missing_listeners
        PASS [   0.007s] (151/169) cartridge::bin/cartridge cli::manual::tests::addresses_resolve_and_search_lands_in_the_section
        PASS [   0.008s] (152/169) cartridge::bin/cartridge cli::settings::tests::lua_keys_and_values_render_as_lua_source
        PASS [   0.029s] (153/169) cartridge::bin/cartridge cli::setup::tests::a_file_changed_by_the_exchange_is_not_recorded
        PASS [   0.009s] (154/169) cartridge::bin/cartridge cli::setup::tests::a_folder_in_the_way_of_a_link_is_refused
        PASS [   0.009s] (155/169) cartridge::bin/cartridge cli::setup::tests::a_setup_or_doctor_event_the_cartridge_does_not_listen_to_is_refused
        PASS [   0.311s] (156/169) cartridge::bin/cartridge cli::host::signal_tests::an_interrupt_is_ignored_while_a_program_holds_the_terminal
        PASS [   0.011s] (157/169) cartridge::bin/cartridge cli::setup::tests::setup_offers_what_it_finds_and_the_catalog_and_filters_by_subsequence
        PASS [   0.013s] (158/169) cartridge::bin/cartridge cli::setup::tests::setup_trusts_what_it_chose_not_what_the_tree_holds
        PASS [   0.011s] (159/169) cartridge::bin/cartridge cli::trust::tests::an_explicit_path_trusts_a_folder_that_is_neither
        PASS [   0.008s] (160/169) cartridge::bin/cartridge cli::width::tests::fit_and_pad_count_display_cells
        PASS [   0.549s] (161/169) cartridge trust::tests::a_deleted_project_is_untrusted_by_a_relative_path
        PASS [   0.496s] (162/169) cartridge trust::tests::a_relative_or_empty_home_is_refused_rather_than_trust_disabling
        PASS [   1.050s] (163/169) cartridge tests::host::verify_sends_every_declared_contract
        PASS [   0.246s] (164/169) cartridge::bin/cartridge cli::setup::tests::setup_links_the_chosen_writes_a_descriptor_the_host_reads_and_lets_a_cartridge_ask
        PASS [   1.080s] (165/169) cartridge tests::settings::refused_settings_do_not_wedge_the_process_when_diagnostics_are_on
        PASS [   2.854s] (166/169) cartridge tests::host::a_terminated_mcp_exits_with_its_input_still_open
        PASS [   5.669s] (167/169) cartridge tests::host::a_node_that_catches_its_own_refusal_exits
        PASS [   5.752s] (168/169) cartridge tests::host::a_spinning_handler_is_refused_and_its_node_keeps_serving
        PASS [   4.424s] (169/169) cartridge tests::settings::a_configuration_file_that_never_returns_is_refused
────────────
     Summary [   9.550s] 169 tests run: 169 passed (1 leaky), 0 skipped
test      cartridge  pass

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently/specs/spec01.md: exit 0

Command SHA-256: 4313675ec3d75f6bdc574c74c4419203b7fa64308a4389d20216d57d874e4e1b

```text
    Finished `dev` profile [unoptimized] target(s) in 0.05s

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently/specs/spec01.md: exit 0

Command SHA-256: 1a73ca315a24f0c684c0f9f9ef5b67412335996d164f30bf7b0469e0e97bbb7a

```text
toolchain: cargo cargo-nextest bun tmux
bun test v1.3.14 (0d9b296a)

 11 pass
 0 fail
 1455 expect() calls
Ran 11 tests across 1 file. [42.60s]
test      lifecycle  pass

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/prds/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently/specs/spec01.md: exit 0

Command SHA-256: 7f89dcdcda36e194e7721c1a52622c070cd9e6845ae18d6af7e22022ef6688d2

```text

```
