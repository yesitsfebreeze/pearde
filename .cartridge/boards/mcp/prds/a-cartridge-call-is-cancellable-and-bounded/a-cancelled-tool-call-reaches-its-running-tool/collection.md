---
commit: 624afb3ab7bab6f2644e8287981d878c636e3df8
spec-digests: {"spec01.md":"175c41db791189680febebe7493ca28957c0e197f818427d0b6e0c5c4e5657b3"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/mcp/prds/a-cartridge-call-is-cancellable-and-bounded/a-cancelled-tool-call-reaches-its-running-tool/specs/spec01.md: exit 0

Command SHA-256: d9b68547368580ea876a342bd63f9b6b1324e969ed8a98b8850e38a8dc2e0747

```text
   Compiling proc-macro2 v1.0.107
   Compiling unicode-ident v1.0.24
   Compiling quote v1.0.47
   Compiling libc v0.2.189
   Compiling cfg-if v1.0.4
   Compiling serde_core v1.0.229
   Compiling version_check v0.9.5
   Compiling autocfg v1.5.1
   Compiling memchr v2.8.3
   Compiling find-msvc-tools v0.1.12
   Compiling num-traits v0.2.19
   Compiling shlex v2.0.1
   Compiling typenum v1.20.1
   Compiling parking_lot_core v0.9.12
   Compiling pin-project-lite v0.2.17
   Compiling generic-array v0.14.7
   Compiling cc v1.4.6
   Compiling futures-sink v0.3.34
   Compiling scopeguard v1.2.0
   Compiling pkg-config v0.3.34
   Compiling serde v1.0.229
   Compiling smallvec v1.16.1
   Compiling futures-core v0.3.34
   Compiling typeid v1.0.3
   Compiling futures-channel v0.3.34
   Compiling mlua-sys v0.12.0
   Compiling lock_api v0.4.14
   Compiling futures-io v0.3.34
   Compiling futures-task v0.3.34
   Compiling slab v0.4.12
   Compiling zmij v1.0.23
   Compiling erased-serde v0.4.10
   Compiling syn v3.0.5
   Compiling syn v2.0.119
   Compiling serde_derive v1.0.229
   Compiling futures-macro v0.3.34
   Compiling errno v0.3.14
   Compiling futures-util v0.3.34
   Compiling parking_lot v0.12.5
   Compiling ordered-float v2.10.1
   Compiling serde_json v1.0.151
   Compiling signal-hook-registry v1.4.8
   Compiling mio v1.2.3
   Compiling crypto-common v0.1.7
   Compiling block-buffer v0.10.4
   Compiling socket2 v0.6.5
   Compiling cpufeatures v0.2.17
   Compiling digest v0.10.7
   Compiling mlua_derive v0.12.1
   Compiling tokio-macros v2.7.2
   Compiling bstr v1.13.1
   Compiling itoa v1.0.18
   Compiling bytes v1.12.1
   Compiling rustc-hash v2.1.3
   Compiling either v1.18.0
   Compiling mcp v0.1.0 (/Users/feb/dev/cartridge/mcp.ctg)
   Compiling sha2 v0.10.9
   Compiling tokio v1.53.1
   Compiling futures-executor v0.3.34
   Compiling futures v0.3.34
   Compiling serde-value v0.7.0
   Compiling mlua v0.12.1
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 7.71s

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/mcp/prds/a-cartridge-call-is-cancellable-and-bounded/a-cancelled-tool-call-reaches-its-running-tool/specs/spec01.md: exit 0

Command SHA-256: 5a699e1e5a31a372e722968e06aabfb525f0ccbcbc15f48c4d56771903dc5a70

```text

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/mcp/prds/a-cartridge-call-is-cancellable-and-bounded/a-cancelled-tool-call-reaches-its-running-tool/specs/spec01.md: exit 0

Command SHA-256: c9c6c9ade19ea0ddd5fa0645213adb17da0a7c5252b8ac7cdf3fdd345ab6026e

```text
passed: a cancelled tools/call reaches the running tool
bun test v1.3.14 (0d9b296a)

 1 pass
 0 fail
 2 expect() calls
Ran 1 test across 1 file. [3.41s]

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/mcp/prds/a-cartridge-call-is-cancellable-and-bounded/a-cancelled-tool-call-reaches-its-running-tool/specs/spec01.md: exit 0

Command SHA-256: f047ecec51076a6d7c7362d4465079b7cd712ab7a671d9846ad1d49343ce8ee2

```text
passed: cancelling_a_call_reaches_the_tool_under_that_calls_own_identity, two_instances_keep_separate_sessions_and_in_flight_calls, an_empty_tool_list_follows_the_needs_and_is_described_on_every_list, initialized_live_client_inspects_real_policy_without_granting_writes
   Compiling tokio v1.53.1
   Compiling mcp v0.1.0 (/Users/feb/dev/cartridge/mcp.ctg)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 3.83s
     Running unittests src/lib.rs (target/a-cancelled-tool-call-verify/debug/deps/mcp-042c8bdf33b44b24)

running 24 tests
test tests::a_broken_line_and_an_unknown_method_answer_without_dropping_the_connection ... ok
test tests::a_tool_whose_describe_hangs_or_fails_is_left_out_not_the_whole_list ... ok
test tests::an_empty_profile_exposes_no_tools_and_an_unknown_one_is_refused ... ok
test tests::a_denied_call_and_a_failing_tool_are_results_the_client_continues_from ... ok
test tests::a_client_initializes_lists_the_profiles_tools_and_calls_one ... ok
test tests::an_ask_refusal_names_the_operation_and_the_missing_channel ... ok
test tests::an_empty_tool_list_follows_the_needs_and_is_described_on_every_list ... ok
test tests::band_disabled_sends_every_schema ... ok
test tests::band_lists_a_tool_without_summary_by_name_alone ... ok
test tests::band_reports_withheld_and_kept_bytes ... ok
test tests::initialized_live_client_observes_catalog_replacements ... ignored, needs a built host and mcp module; run through `just smoke mcp`
test tests::a_restored_tool_stays_with_the_instance_that_restored_it ... ok
test tests::band_disabled_listing_is_byte_identical ... ok
test tests::cancelling_a_call_reaches_the_tool_under_that_calls_own_identity ... ok
test tests::granted_calls_land_in_the_observation_journal_with_caller_and_turn ... ok
test tests::band_opt_out_and_allowlist_arrive_with_their_schema ... ok
test tests::quiet_defaults_do_not_write_an_automatic_observation_journal ... ok
test tests::diagnostic_inspection_is_optional_scoped_and_cannot_grant_authority ... ok
test tests::the_mcp_event_declares_its_own_bound ... ok
test tests::band_withholds_deferred_schemas_and_lists_their_summaries ... ok
test tests::two_instances_keep_separate_sessions_and_in_flight_calls ... ok
test tests::unavailable_or_changed_explanations_never_replace_refusal_with_allow ... ok
test tests::band_restores_a_deferred_tool_for_the_rest_of_the_session ... ok
bun test v1.3.14 (0d9b296a)

 1 pass
 0 fail
 24 expect() calls
Ran 1 test across 1 file. [4.67s]
test tests::initialized_live_client_inspects_real_policy_without_granting_writes ... ok

test result: ok. 23 passed; 0 failed; 1 ignored; 0 measured; 0 filtered out; finished in 4.73s


```
