---
commit: 21be1528bff2840b00dcef3e87ece41585df3017
spec-digests: {"spec01.md":"589848682581cfbf9c60f31868f4af31b0d16b93b395090a750ddb4902ae9e60"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/gitfs/prds/tool-results-interoperate/specs/spec01.md: exit 0

Command SHA-256: ea8e858aa02e4a15ec4d42d4cdbd699a1efa27d866db146dc8b79bde9fd43132

```text
    Finished `test` profile [unoptimized] target(s) in 0.06s
     Running unittests src/main.rs (/Users/feb/dev/cartridge/cartridge.ctg/.cartridge/workspace/target/debug/deps/gitfs-19fc2b53a8f8f0b9)

running 22 tests
test secrets::tests::template_files_are_skipped_entirely ... ok
test ship::tests::auto_subject_shapes ... ok
test ship::tests::gate_prompt_demands_json_only ... ok
test secrets::tests::context_lines_are_not_scanned ... ok
test secrets::tests::sensitive_filename_is_flagged_even_with_plain_content ... ok
test secrets::tests::has_secret_detects_and_allows_plain ... ok
test ship::tests::secret_subject_is_rejected_and_plain_passes ... ok
test secrets::tests::real_key_on_added_line_finds ... ok
test secrets::tests::scan_file_matches ... ok
test secrets::tests::placeholder_token_is_ignored ... ok
test tool_result::tests::invalid_inputs_do_not_open_the_store ... ok
test tool_result::tests::payloads_are_encoded_once_and_text_stays_literal ... ok
test store::tests::unrelated_overlay_sessions_do_not_share_a_mutation_lock ... ok
test store::tests::roundtrip_and_noop ... ok
test service::snapshot_tests::read_failures_report_partial_success_and_preserve_failed_overlay ... ok
test service::snapshot_tests::guarded_edit_still_refuses_stale_content ... ok
test store::tests::ship_trailer_undo_and_no_remote ... ok
test store::tests::materialize_guard ... ok
test store::tests::multi_path_overlay_survives_rewrite ... ok
test store::tests::concurrent_overlay_writes_keep_every_path ... ok
test service::snapshot_tests::selection_is_exact_empty_is_empty_and_unowned_is_rejected_before_writes ... ok
test tool_result::tests::real_consumers_share_the_tool_result_contract ... ok

test result: ok. 22 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 3.26s


```
