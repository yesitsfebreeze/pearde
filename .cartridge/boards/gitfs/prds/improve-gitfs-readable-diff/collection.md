---
commit: 55cc8aae27575ded5950737c46a99aa358b95980
spec-digests: {"spec01.md":"025587dbf8e4a317b00e38016a42f49322b52f591fa9c9504debbe0d5e99ded8"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/gitfs/prds/improve-gitfs-readable-diff/specs/spec01.md: exit 0

Command SHA-256: ec68425ffc44d57a4e22b13b13edd2562085648e338775c55007281f994bed69

```text
   Compiling ring v0.17.14
   Compiling rustls-webpki v0.103.15
   Compiling rustls v0.23.44
   Compiling tokio-rustls v0.26.5
   Compiling hyper-rustls v0.27.9
   Compiling reqwest v0.12.28
   Compiling gitfs v0.1.0 (/Users/feb/dev/cartridge/gitfs.ctg)
    Finished `test` profile [unoptimized] target(s) in 2.93s
     Running unittests src/main.rs (target/tool-result-contract/debug/deps/gitfs-8952c5d566a3c3a9)

running 25 tests
test secrets::tests::template_files_are_skipped_entirely ... ok
test ship::tests::auto_subject_shapes ... ok
test ship::tests::gate_prompt_demands_json_only ... ok
test secrets::tests::context_lines_are_not_scanned ... ok
test secrets::tests::sensitive_filename_is_flagged_even_with_plain_content ... ok
test secrets::tests::has_secret_detects_and_allows_plain ... ok
test ship::tests::secret_subject_is_rejected_and_plain_passes ... ok
test secrets::tests::real_key_on_added_line_finds ... ok
test secrets::tests::placeholder_token_is_ignored ... ok
test secrets::tests::scan_file_matches ... ok
test store::tests::unrelated_overlay_sessions_do_not_share_a_mutation_lock ... ok
test tool_result::tests::inspection_baseline_diff_is_available ... ok
test tool_result::tests::inspection_baseline_read_does_not_create_a_store ... ok
test tool_result::tests::invalid_inputs_do_not_open_the_store ... ok
test tool_result::tests::payloads_are_encoded_once_and_text_stays_literal ... ok
test tool_result::tests::inspection_absence_binary_bounds_and_path_failures_are_explicit ... ok
test store::tests::roundtrip_and_noop ... ok
test service::snapshot_tests::read_failures_report_partial_success_and_preserve_failed_overlay ... ok
test service::snapshot_tests::guarded_edit_still_refuses_stale_content ... ok
test store::tests::ship_trailer_undo_and_no_remote ... ok
test store::tests::materialize_guard ... ok
test store::tests::multi_path_overlay_survives_rewrite ... ok
test service::snapshot_tests::selection_is_exact_empty_is_empty_and_unowned_is_rejected_before_writes ... ok
test store::tests::concurrent_overlay_writes_keep_every_path ... ok
test tool_result::tests::real_consumers_share_the_tool_result_contract ... ok

test result: ok. 25 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 12.52s


```
