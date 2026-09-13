---
commit: 29b20b27b352ccb8df04cbc2ad9e4eefa20e7369
spec-digests: {"spec01.md":"9b4207fcc0f3e3b8b2da9b0ce73118fe3d58fa99e527b831c6e71299f2256a55"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/mcp/prds/improve-mcp-refresh-catalog/specs/spec01.md: exit 0

Command SHA-256: a75434df38c0a7a09579d748f18876dd83f07d67cdde32e24ef62d852b5602cf

```text
    Finished `test` profile [unoptimized] target(s) in 0.06s
     Running unittests src/main.rs (target/tool-result-contract/debug/deps/mcp-907608fff523f450)

running 12 tests
test tests::an_empty_profile_exposes_no_tools_and_an_unknown_one_is_refused ... ok
test tests::a_broken_line_and_an_unknown_method_answer_without_dropping_the_connection ... ok
test tests::an_ask_refusal_names_the_operation_and_the_missing_channel ... ok
test tests::discovery_does_not_publish_mixed_generations ... ok
test tests::descriptors_are_cached_until_the_service_version_changes ... ok
test tests::quiet_defaults_do_not_write_an_automatic_observation_journal ... ok
test tests::persistent_discovery_churn_is_bounded_and_stable_errors_keep_old_cache_for_rollback ... ok
test tests::granted_calls_land_in_the_observation_journal_with_caller_and_turn ... ok
test tests::cancelling_a_call_reaches_the_tool_under_that_calls_own_identity ... ok
test tests::a_client_initializes_lists_the_profiles_tools_and_calls_one ... ok
test tests::a_denied_call_and_a_failing_tool_are_results_the_client_continues_from ... ok
test tests::initialized_live_client_observes_catalog_replacements ... ok

test result: ok. 12 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 3.19s


```
