---
commit: 17e27b74f7126165a93ff46b531b5e78481bcd31
spec-digests: {"spec01.md":"e0df9c2705285ec51787caf85c4742c0cf1ba906887525ccc6fe468a9ca30684"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/agent/prds/a-denied-tool-call-journals-its-error-flag/specs/spec01.md: exit 0

Command SHA-256: 122b724ebf897369afb5f6f426c060aea41970ada6948b45fef0d6663704173f

```text
   Compiling ring v0.17.14
   Compiling rustls v0.23.44
   Compiling rustls-webpki v0.103.15
   Compiling tokio-rustls v0.26.5
   Compiling hyper-rustls v0.27.9
   Compiling reqwest v0.12.28
   Compiling agent v0.1.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/agent/.lanes/a-denied-tool-call-journals-its-error-flag)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 4.17s
     Running .cartridge/tests/integration/loop.rs (target/harness-yolo-verify/debug/deps/loop-9a8e2d656df0559e)

running 13 tests
   Compiling ring v0.17.14
   Compiling rustls v0.23.44
   Compiling rustls-webpki v0.103.15
   Compiling tokio-rustls v0.26.5
   Compiling hyper-rustls v0.27.9
   Compiling reqwest v0.12.28
   Compiling agent v0.1.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/agent/.lanes/a-denied-tool-call-journals-its-error-flag)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 2.01s
test scripted_tool_call_then_final_answer_is_ordered_and_preserves_id ... ok
test a_tool_error_is_visible_to_the_next_model_request ... ok
test harness_system_inserted_once_and_descriptor_schema_reaches_chat_unchanged ... ok
test streaming_credentials_never_reach_journal_events_or_request_records ... ok
test a_dispatch_and_its_outcome_are_recorded_observations ... ok
test multiple_tool_calls_execute_and_persist_in_response_order ... ok
test streaming_malformed_stream_executes_no_tool_and_persists_no_message ... ok
test streaming_cancel_mid_stream_releases_once_without_append ... ok
test configured_keys_only_unknown_tool_is_a_recorded_error ... ok
test recovery_closes_unresolved_calls_then_a_new_turn_can_proceed ... ok
test streaming_post_delta_disconnect_emits_stream_error_without_replay ... ok
test streaming_pre_visible_disconnect_retries_once ... ok
test transport_failure_and_tool_limit_terminate_once ... ok

test result: ok. 13 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 8.66s


```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/agent/prds/a-denied-tool-call-journals-its-error-flag/specs/spec01.md: exit 0

Command SHA-256: 293af0962b7a254bccfebbc9c70bd437b028edcc30e5c1442d60740ef21654b9

```text
passed: multiple_tool_calls_execute_and_persist_in_response_order
   Compiling ring v0.17.14
   Compiling rustls v0.23.44
   Compiling rustls-webpki v0.103.15
   Compiling tokio-rustls v0.26.5
   Compiling hyper-rustls v0.27.9
   Compiling reqwest v0.12.28
   Compiling agent v0.1.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/agent/.lanes/a-denied-tool-call-journals-its-error-flag)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 1.94s
     Running .cartridge/tests/integration/loop.rs (target/harness-yolo-verify/debug/deps/loop-9a8e2d656df0559e)

running 13 tests
   Compiling ring v0.17.14
   Compiling rustls v0.23.44
   Compiling rustls-webpki v0.103.15
   Compiling tokio-rustls v0.26.5
   Compiling hyper-rustls v0.27.9
   Compiling reqwest v0.12.28
   Compiling agent v0.1.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/agent/.lanes/a-denied-tool-call-journals-its-error-flag)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 1.82s
test streaming_cancel_mid_stream_releases_once_without_append ... ok
test recovery_closes_unresolved_calls_then_a_new_turn_can_proceed ... ok
test streaming_malformed_stream_executes_no_tool_and_persists_no_message ... ok
test configured_keys_only_unknown_tool_is_a_recorded_error ... ok
test multiple_tool_calls_execute_and_persist_in_response_order ... ok
test harness_system_inserted_once_and_descriptor_schema_reaches_chat_unchanged ... ok
test streaming_credentials_never_reach_journal_events_or_request_records ... ok
test a_dispatch_and_its_outcome_are_recorded_observations ... ok
test scripted_tool_call_then_final_answer_is_ordered_and_preserves_id ... ok
test a_tool_error_is_visible_to_the_next_model_request ... ok
test streaming_post_delta_disconnect_emits_stream_error_without_replay ... ok
test streaming_pre_visible_disconnect_retries_once ... ok
test transport_failure_and_tool_limit_terminate_once ... ok

test result: ok. 13 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 13.47s


```
