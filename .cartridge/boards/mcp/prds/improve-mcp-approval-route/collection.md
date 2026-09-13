---
commit: f5a740517bc2668b50cf4f61fe81a1e37bb4cfad
spec-digests: {"spec01.md":"8cfc4f5b4829850e5c3d36055025f5cf7480da69e451d9b07eed6ed2697456f3"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/mcp/prds/improve-mcp-approval-route/specs/spec01.md: exit 0

Command SHA-256: a75434df38c0a7a09579d748f18876dd83f07d67cdde32e24ef62d852b5602cf

```text
    Finished `test` profile [unoptimized] target(s) in 0.08s
     Running unittests src/main.rs (target/tool-result-contract/debug/deps/mcp-907608fff523f450)

running 15 tests
test tests::an_empty_profile_exposes_no_tools_and_an_unknown_one_is_refused ... ok
test tests::a_broken_line_and_an_unknown_method_answer_without_dropping_the_connection ... ok
test tests::a_client_initializes_lists_the_profiles_tools_and_calls_one ... ok
test tests::an_ask_refusal_names_the_operation_and_the_missing_channel ... ok
test tests::discovery_does_not_publish_mixed_generations ... ok
test tests::descriptors_are_cached_until_the_service_version_changes ... ok
test tests::granted_calls_land_in_the_observation_journal_with_caller_and_turn ... ok
test tests::cancelling_a_call_reaches_the_tool_under_that_calls_own_identity ... ok
test tests::diagnostic_inspection_is_optional_scoped_and_cannot_grant_authority ... ok
test tests::quiet_defaults_do_not_write_an_automatic_observation_journal ... ok
test tests::a_denied_call_and_a_failing_tool_are_results_the_client_continues_from ... ok
test tests::persistent_discovery_churn_is_bounded_and_stable_errors_keep_old_cache_for_rollback ... ok
test tests::unavailable_or_changed_explanations_never_replace_refusal_with_allow ... ok
bun test v1.3.14 (0d9b296a)

.cartridge/tests/integration/approval.test.ts:
(pass) a real headless profile explains operation rules and ignores forged approval [1860.09ms]

 1 pass
 0 fail
 27 expect() calls
Ran 1 test across 1 file. [1.87s]
test tests::initialized_live_client_inspects_real_policy_without_granting_writes ... ok
test tests::initialized_live_client_observes_catalog_replacements ... ok

test result: ok. 15 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 3.15s


```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/mcp/prds/improve-mcp-approval-route/specs/spec01.md: exit 0

Command SHA-256: 7a1d05311b3e80c4b7fa8af1d09735ce737d3f57566ddc91fcefa0a3fd2eef61

```text
bun test v1.3.14 (0d9b296a)

.cartridge/tests/integration/approval.test.ts:
(pass) a real headless profile explains operation rules and ignores forged approval [5397.70ms]

 1 pass
 0 fail
 27 expect() calls
Ran 1 test across 1 file. [5.41s]

```
