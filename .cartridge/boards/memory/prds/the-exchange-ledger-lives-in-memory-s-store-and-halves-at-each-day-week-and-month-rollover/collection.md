---
commit: 97af8ff9f2d277313081e160bf69e7f92096ab29
spec-digests: {"spec01.md":"b5649988847b0205f815b2c2284562050a8e41a5be80a53967dba48249b76220"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/prds/the-exchange-ledger-lives-in-memory-s-store-and-halves-at-each-day-week-and-month-rollover/specs/spec01.md: exit 0

Command SHA-256: 3af1bd2bed4f5afaa80aa0954a1d53ff807cd9534878e7d49b3fc8fd949cdb65

```text
   Compiling config v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/config)
   Compiling store_core v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/store/core)
   Compiling gnn v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/gnn)
   Compiling identity v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/identity)
   Compiling graph v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/graph)
   Compiling retrieval-piece v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/retrieval/piece)
   Compiling ingest v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/ingest)
   Compiling tick v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/tick)
   Compiling bootstrap v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/bootstrap)
   Compiling retrieval v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/retrieval)
   Compiling tick_loop v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/tick/loop)
   Compiling store v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/store)
   Compiling health v0.1.0 (/Users/feb/dev/cartridge/memory.ctg/src/health)
   Compiling rpc v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/rpc)
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/rpc-1a8f81ae0987021b.rpc.1afb545ff6f82bda-cgu.00.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/rpc-1a8f81ae0987021b.rpc.1afb545ff6f82bda-cgu.01.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/rpc-1a8f81ae0987021b.rpc.1afb545ff6f82bda-cgu.02.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/rpc-1a8f81ae0987021b.rpc.1afb545ff6f82bda-cgu.03.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/rpc-1a8f81ae0987021b.rpc.1afb545ff6f82bda-cgu.04.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/rpc-1a8f81ae0987021b.rpc.1afb545ff6f82bda-cgu.05.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/rpc-1a8f81ae0987021b.rpc.1afb545ff6f82bda-cgu.06.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/rpc-1a8f81ae0987021b.rpc.1afb545ff6f82bda-cgu.07.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/rpc-1a8f81ae0987021b.rpc.1afb545ff6f82bda-cgu.08.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/rpc-1a8f81ae0987021b.rpc.1afb545ff6f82bda-cgu.09.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/rpc-1a8f81ae0987021b.rpc.1afb545ff6f82bda-cgu.10.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/rpc-1a8f81ae0987021b.rpc.1afb545ff6f82bda-cgu.11.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/rpc-1a8f81ae0987021b.rpc.1afb545ff6f82bda-cgu.12.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/rpc-1a8f81ae0987021b.rpc.1afb545ff6f82bda-cgu.13.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/rpc-1a8f81ae0987021b.rpc.1afb545ff6f82bda-cgu.14.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/rpc-1a8f81ae0987021b.rpc.1afb545ff6f82bda-cgu.15.rcgu.o unable to open object file: No such file or directory
    Finished `test` profile [unoptimized + debuginfo] target(s) in 7.91s
     Running unittests src/lib.rs (target/debug/deps/rpc-1a8f81ae0987021b)

running 13 tests
test ledger::ledger_tests::a_week_across_a_month_boundary_is_two_weeks ... ok
test ledger::ledger_tests::a_tail_too_small_to_halve_rides_along_instead_of_failing_the_unit ... ok
test ledger::ledger_tests::append_refuses_a_timestamp_that_is_not_milliseconds ... ok
test ledger::ledger_tests::a_closed_day_becomes_one_record_at_most_half_its_raw_text ... ok
test ledger::ledger_tests::closing_september_takes_only_the_week_inside_it ... ok
test ledger::ledger_tests::a_late_exchange_for_a_closed_day_is_folded_into_its_record ... ok
test ledger::ledger_tests::days_mirrored_in_earlier_passes_leave_the_graph_when_their_month_and_year_close_at_once ... ok
test ledger::ledger_tests::a_record_the_graph_refuses_for_good_keeps_its_children_and_stops_retrying ... ok
test ledger::ledger_tests::weeks_months_and_years_condense_their_children_and_forget_them_in_the_graph ... ok
test ledger::ledger_tests::a_record_the_graph_refused_is_mirrored_by_a_later_pass ... ok
test ledger::ledger_tests::import_reads_both_historical_row_shapes ... ok
test ledger::ledger_tests::a_failing_model_leaves_every_input_and_a_later_pass_condenses_them ... ok
test ledger::ledger_tests::the_open_day_past_its_cap_condenses_its_oldest_half_into_a_part ... ok

test result: ok. 13 passed; 0 failed; 0 ignored; 0 measured; 96 filtered out; finished in 0.35s


```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/prds/the-exchange-ledger-lives-in-memory-s-store-and-halves-at-each-day-week-and-month-rollover/specs/spec01.md: exit 0

Command SHA-256: 440c75683d620c27ee7b852629f6befae5a9cb8ffeb72a5a7003299db433d704

```text
   Compiling store_core v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/store/core)
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/store_core-f4e55b9170b5df9d.store_core.24fc8622729353d9-cgu.00.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/store_core-f4e55b9170b5df9d.store_core.24fc8622729353d9-cgu.01.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/store_core-f4e55b9170b5df9d.store_core.24fc8622729353d9-cgu.02.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/store_core-f4e55b9170b5df9d.store_core.24fc8622729353d9-cgu.03.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/store_core-f4e55b9170b5df9d.store_core.24fc8622729353d9-cgu.04.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/store_core-f4e55b9170b5df9d.store_core.24fc8622729353d9-cgu.05.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/store_core-f4e55b9170b5df9d.store_core.24fc8622729353d9-cgu.06.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/store_core-f4e55b9170b5df9d.store_core.24fc8622729353d9-cgu.07.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/store_core-f4e55b9170b5df9d.store_core.24fc8622729353d9-cgu.08.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/store_core-f4e55b9170b5df9d.store_core.24fc8622729353d9-cgu.09.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/store_core-f4e55b9170b5df9d.store_core.24fc8622729353d9-cgu.10.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/store_core-f4e55b9170b5df9d.store_core.24fc8622729353d9-cgu.11.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/store_core-f4e55b9170b5df9d.store_core.24fc8622729353d9-cgu.12.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/store_core-f4e55b9170b5df9d.store_core.24fc8622729353d9-cgu.13.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/store_core-f4e55b9170b5df9d.store_core.24fc8622729353d9-cgu.14.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/store_core-f4e55b9170b5df9d.store_core.24fc8622729353d9-cgu.15.rcgu.o unable to open object file: No such file or directory
    Finished `test` profile [unoptimized + debuginfo] target(s) in 1.55s
     Running unittests src/lib.rs (target/debug/deps/store_core-f4e55b9170b5df9d)

running 2 tests
test ledger::ledger_test::ledger_commit_refuses_when_an_input_is_already_gone ... ok
test ledger::ledger_test::ledger_commit_swaps_inputs_for_their_condensate_and_scan_stays_in_prefix ... ok

test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 78 filtered out; finished in 0.03s

   Compiling config v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/config)
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/config-57aecb1278fc1af3.config.ffd9057c0a46b43c-cgu.00.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/config-57aecb1278fc1af3.config.ffd9057c0a46b43c-cgu.01.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/config-57aecb1278fc1af3.config.ffd9057c0a46b43c-cgu.02.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/config-57aecb1278fc1af3.config.ffd9057c0a46b43c-cgu.03.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/config-57aecb1278fc1af3.config.ffd9057c0a46b43c-cgu.04.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/config-57aecb1278fc1af3.config.ffd9057c0a46b43c-cgu.05.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/config-57aecb1278fc1af3.config.ffd9057c0a46b43c-cgu.06.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/config-57aecb1278fc1af3.config.ffd9057c0a46b43c-cgu.07.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/config-57aecb1278fc1af3.config.ffd9057c0a46b43c-cgu.08.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/config-57aecb1278fc1af3.config.ffd9057c0a46b43c-cgu.09.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/config-57aecb1278fc1af3.config.ffd9057c0a46b43c-cgu.10.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/config-57aecb1278fc1af3.config.ffd9057c0a46b43c-cgu.11.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/config-57aecb1278fc1af3.config.ffd9057c0a46b43c-cgu.12.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/config-57aecb1278fc1af3.config.ffd9057c0a46b43c-cgu.13.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/config-57aecb1278fc1af3.config.ffd9057c0a46b43c-cgu.14.rcgu.o unable to open object file: No such file or directory
warning: (arm64) /Users/feb/dev/cartridge/memory.ctg/target/debug/deps/config-57aecb1278fc1af3.config.ffd9057c0a46b43c-cgu.15.rcgu.o unable to open object file: No such file or directory
    Finished `test` profile [unoptimized + debuginfo] target(s) in 1.78s
     Running unittests src/lib.rs (target/debug/deps/config-57aecb1278fc1af3)

running 77 tests
test config::config_tests::gnn_tests::default_arms_disk_spill ... ok
test config::config_tests::gnn_tests::default_bounds_resident_memories_conservatively ... ok
test config::config_tests::embed_tests::default_uses_the_shared_constants ... ok
test config::config_tests::hub_tests::defaults_are_on_with_sane_tunables ... ok
test config::config_tests::hub_tests::validate_rejects_zero_poll_only_when_enabled ... ok
test config::config_tests::graph_tests::default_validates_and_bad_knobs_are_rejected ... ok
test config::config_tests::ingest_tests::default_config_is_valid ... ok
test config::config_tests::graph_tests::an_unknown_review_policy_scheme_is_flagged ... ok
test config::config_tests::ingest_run_config_tests::the_mapping_carries_the_resolved_retention_deadline ... ok
test config::config_tests::ingest_tests::out_of_range_bm25_params_are_flagged ... ok
test config::config_tests::ingest_tests::an_unknown_or_negative_source_trust_key_is_flagged ... ok
test config::config_tests::ingest_tests::retrieval_breaking_values_are_flagged ... ok
test config::config_tests::ingest_tests::weights_not_summing_to_one_are_flagged ... ok
test config::config_tests::io_tests::merge_deep_scalar_in_over_beats_a_table_in_base ... ok
test config::config_tests::io_tests::merge_deep_leaf_and_array_in_over_replace_the_base ... ok
test config::config_tests::io_tests::merge_deep_merges_nested_tables_at_depth ... ok
test config::config_tests::io_tests::merged_value_merges_project_section_over_missing_user ... ok
test config::config_tests::io_tests::merged_value_keeps_sections_present_in_only_one_scope ... ok
test config::config_tests::llm_timeout_tests::the_unconfigured_timeout_is_the_const_it_replaced ... ok
test config::config_tests::preset_tests::every_preset_yields_a_valid_config ... ok
test config::config_tests::io_tests::merged_value_project_field_wins_and_keeps_the_user_fields_it_omits ... ok
test config::config_tests::preset_tests::medium_matches_the_neutral_struct_defaults ... ok
test config::config_tests::preset_tests::relaxed_and_tight_move_the_knobs_in_opposite_directions ... ok
test config::config_tests::preset_tests::the_default_preset_is_relaxed ... ok
test config::config_tests::io_tests::read_value_parses_leading_section_header ... ok
test config::config_tests::io_tests::merged_value_seals_the_key_when_the_project_redirects_the_endpoint ... ok
test config::config_tests::reload_tests::effective_roots_falls_back_to_cwd_when_enabled_and_empty ... ok
test config::config_tests::reload_tests::effective_roots_is_empty_when_disabled ... ok
test config::config_tests::reload_tests::effective_roots_uses_configured_roots_when_present ... ok
test config::config_tests::secrets_tests::a_project_supplying_its_own_key_with_its_own_url_keeps_it ... ok
test config::config_tests::ingest_run_config_tests::every_field_the_mapping_carries_comes_from_the_config_it_was_given ... ok
test config::config_tests::secrets_tests::a_project_that_leaves_the_url_alone_keeps_inheriting_the_key ... ok
test config::config_tests::secrets_tests::a_project_that_redirects_the_url_does_not_inherit_the_users_key ... ok
test config::config_tests::secrets_tests::sealing_is_per_section_not_global ... ok
test config::config_tests::queue_tests::open_private_append_tightens_a_world_readable_file ... ok
test config::config_tests::serve_tests::one_log_file_per_spawn_arg ... ok
test config::config_tests::queue_tests::open_private_append_creates_then_appends_without_truncating ... ok
test config::config_tests::tests::default_in_pins_data_dir_to_the_given_cwd_deterministically ... ok
test config::config_tests::tests::egress_warnings_flags_a_cloud_tag_behind_a_loopback_url ... ok
test config::config_tests::tests::egress_warnings_flags_a_public_embed_url_and_silences_loopback ... ok
test config::config_tests::tests::egress_warnings_name_the_endpoint_without_its_credential ... ok
test config::config_tests::tests::egress_warnings_reports_one_per_non_local_url ... ok
test config::config_tests::tests::a_mixed_retrieval_table_refuses ... ok
test config::config_tests::tests::configless_load_defaults_to_relaxed ... ok
test config::config_tests::serve_tests::an_unopenable_log_is_an_error_the_caller_can_see ... ok
test config::config_tests::tests::embed_config_default_carries_the_native_knob_constants ... ok
test config::config_tests::tests::is_loopback_url_pins_loopback_only ... ok
test config::config_tests::serve_tests::opening_creates_the_dir_and_appends_rather_than_truncating ... ok
test config::config_tests::tests::a_real_memory_toml_can_set_per_source_retention ... ok
test config::config_tests::tests::log_dir_stays_inside_the_data_dir_memory_owns ... ok
test config::config_tests::tests::a_memory_toml_naming_the_absolute_floor_key_fails_loud ... ok
test config::config_tests::tests::load_of_a_foreign_root_pins_data_dir_to_that_root ... ok
test config::config_tests::evaluation_variants_load_through_the_real_config_gate ... ok
test config::config_tests::tests::load_resolves_relative_data_dir_to_cwd ... ok
test config::config_tests::tests::a_real_memory_toml_can_set_review_policy_and_nothing_else_in_ingest ... ok
test config::config_tests::tests::every_other_retrieval_key_still_refuses ... ok
test config::config_tests::tests::memory_dir_env_pins_the_store_base ... ok
test config::config_tests::tests::native_knob_warnings_names_a_tuned_knob_on_a_v1_endpoint ... ok
test config::config_tests::tests::native_knob_warnings_silent_on_a_v1_endpoint_with_default_knobs ... ok
test config::config_tests::tests::native_knob_warnings_silent_on_default_loopback ... ok
test config::config_tests::tests::reason_sampling_is_unset_by_default_and_zero_temperature_is_a_real_setting ... ok
test config::config_tests::tests::resolve_root_detects_git_as_a_file ... ok
test config::config_tests::tests::resolve_root_returns_start_when_no_memory_ancestor ... ok
test config::config_tests::tests::preset_key_applies_its_tier ... ok
test config::config_tests::tests::validate_refuses_an_empty_denied_path ... ok
test config::config_tests::tests::validate_requires_embed_and_surfaces_sub_config_invariants ... ok
test config::config_tests::tests::wsl_loopback_warnings_names_a_loopback_endpoint_under_wsl ... ok
test config::config_tests::tests::wsl_loopback_warnings_silent_off_wsl ... ok
test config::config_tests::tests::project_preset_beats_user_preset ... ok
test config::config_tests::tests::the_three_retrieval_quality_keys_are_settable_from_a_memory_toml ... ok
test config::config_tests::tests::resolve_root_innermost_git_wins ... ok
test config::config_tests::tests::resolve_root_walks_up_to_nearest_memory_dir ... ok
test config::config_tests::tests::resolve_root_prefers_git_root_over_deeper_memory ... ok
test config::config_tests::tests::resolve_root_starts_at_git_root_when_no_memory ... ok
test config::config_tests::tests::unknown_preset_name_refuses_to_load ... ok
test config::config_tests::tests::min_deliver_fraction_range_is_checked ... ok
test config::config_tests::tests::preset_managed_sections_refuse_to_load ... ok

test result: ok. 77 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.02s

   Doc-tests config

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s


```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/prds/the-exchange-ledger-lives-in-memory-s-store-and-halves-at-each-day-week-and-month-rollover/specs/spec01.md: exit 0

Command SHA-256: c0f803c410652f46bd999b85eede3e4aa88697e6e8c14eacd1a1f07c74caae22

```text
    Checking config v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/config)
    Checking store_core v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/store/core)
   Compiling memory_cartridge v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/cartridge)
    Checking gnn v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/gnn)
    Checking identity v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/identity)
    Checking hub v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/hub)
    Checking graph v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/graph)
    Checking retrieval-piece v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/retrieval/piece)
    Checking ingest v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/ingest)
    Checking tick v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/tick)
    Checking bootstrap v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/bootstrap)
    Checking retrieval v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/retrieval)
    Checking tick_loop v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/tick/loop)
    Checking store v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/store)
    Checking health v0.1.0 (/Users/feb/dev/cartridge/memory.ctg/src/health)
    Checking rpc v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/rpc)
    Checking commands v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/commands)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 2.88s

```
