---
commit: b8f27c6f1c07888bfc6e5d09f45a8751e8ca7b36
spec-digests: {"spec01.md":"13ce569a3f7d9eb26dd041bd6488743cdda3bb8bcc708b6a73521c1375ef8c31"}
child-contracts: {".cartridge/boards/gitfs/prds/improve-gitfs-reviewable-ship/recorded-push-reconciles-the-exact-remote-head/prd.md":"e4d549434eb68dc231d1397014bf393b852bffc619ff6b5613dad150e6ca5c94",".cartridge/boards/gitfs/prds/improve-gitfs-reviewable-ship/reviewed-owned-tree-commits-locally/prd.md":"688c02d650fe75b4da4a03ca7e04b2d9cd24e00d180e69d0978d30834b7956a7"}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/gitfs/prds/improve-gitfs-reviewable-ship/specs/spec01.md: exit 0

Command SHA-256: 71d387c0fe35b36b42990e3abd46d6fef860603c6dfcc7b5436602b2d06aaa22

```text
{
  "source_commit": "b8f27c6f1c07888bfc6e5d09f45a8751e8ca7b36",
  "records_commit": "a38b23eca920a48f652d0c0a96e2637ef82a4803",
  "footprint": [
    ".cartridge/docs/change-provenance.md",
    ".cartridge/docs/inspection.md",
    ".cartridge/docs/push.md",
    ".cartridge/docs/ship.md",
    ".cartridge/tests/integration/change-provenance.test.ts",
    ".cartridge/tests/integration/recorded-push.test.ts",
    ".cartridge/tests/integration/reviewed-ship.test.ts",
    ".cartridge/tests/integration/tool-result.test.ts",
    ".cartridge/tests/unit/provenance.rs",
    ".cartridge/tests/unit/push/tests.rs",
    ".cartridge/tests/unit/ship/tests.rs",
    ".cartridge/tests/unit/snapshot.rs",
    ".cartridge/tests/unit/store/tests.rs",
    ".cartridge/tests/unit/tool_result.rs",
    "Cargo.toml",
    "init.lua",
    "src/inspection.rs",
    "src/main.rs",
    "src/provenance.rs",
    "src/push.rs",
    "src/service.rs",
    "src/ship.rs",
    "src/store.rs",
    "src/tool_result.rs"
  ],
  "dependencies": [
    {
      "ref": "@policy/ship-push-is-an-explicit-policy-operation",
      "source_commit": "e442bef2c9f07635f9e8b8e1d87a47193841569f",
      "prd_sha256": "b7ac45dab65dc1c5cba9879e544518036409b83c796bb1c7049867056f393c60",
      "spec_sha256": "c313a77d300b54994b0eef60a4474efc57376d6db4882e5e5f9c8175f037e49d",
      "review_round": 3,
      "score": 97,
      "review_sha256": "d057975798a4944f0332cfbeffbc51be8eea7d3029cdddc07a714497d0ae1053",
      "collection_sha256": "1648f9cb145c0baf229f4e53260b56ff4bfdd516ef308551bd405c7d6b3656c1"
    },
    {
      "ref": "@gitfs/improve-gitfs-readable-diff",
      "source_commit": "b8f27c6f1c07888bfc6e5d09f45a8751e8ca7b36",
      "prd_sha256": "e0ec8ea766792e75bd2d52023d32fbcb855811bd682f8f0226a1db0fa804c0dc",
      "spec_sha256": "6ed56a3426a0c5bf5039a2622785a66c6050c7da0b3a3b60aacfd06e437426e7",
      "review_round": 3,
      "score": 94,
      "review_sha256": "e902695dc87b19e2b5e44fc47de8449f7254930647221216911dde9027ba3251",
      "collection_sha256": "34f5f352c4dcd05d7b0845bb24bd95fe57cdf95e645a962a6d0d0c0399485406"
    },
    {
      "ref": "@gitfs/improve-gitfs-snapshot-selection",
      "source_commit": "b8f27c6f1c07888bfc6e5d09f45a8751e8ca7b36",
      "prd_sha256": "0bcf82b09a990ae76494669bb89e1e0054d492c9466ed46d232a231d7b17d188",
      "spec_sha256": "a904623c7d41d7caaaa08a184595fd9fe8ce76c19e146a804193bc5c544c8cb7",
      "review_round": 3,
      "score": 97,
      "review_sha256": "3d82567f6539d411e6369638b96735abd92727b800188bfa8beb07be05d11d3d",
      "collection_sha256": "f4e047332b71b3baf7617aa10bd91dac7a030f4d3893f5f11077afaf1baba4d7"
    },
    {
      "ref": "@policy/improve-policy-operation-rules",
      "source_commit": "e442bef2c9f07635f9e8b8e1d87a47193841569f",
      "prd_sha256": "ff05aeecfbc1ede7603d452dcb2635af3b4b0032f04df971aba3281eb5e69124",
      "spec_sha256": "4c387100550778313009dff4a94703b2b6232c874fe469f56167f487e05d707d",
      "review_round": 3,
      "score": 97,
      "review_sha256": "ddeebac92d47d82b4c4db0186e24797edc35d789e58fa923a2b9ee5493049296",
      "collection_sha256": "79e27879d6b8a09e58e723a998a188342c8be26e98a736079108af1d1c2f13e8"
    },
    {
      "ref": "@gitfs/improve-gitfs-reviewable-ship/reviewed-owned-tree-commits-locally",
      "source_commit": "b8f27c6f1c07888bfc6e5d09f45a8751e8ca7b36",
      "prd_sha256": "c397c6c76f4f334b7eb5515a2a901b98bba02bc1fcaaef114ac17e21f62a3233",
      "spec_sha256": "6b251cdfef881e035a048fd8d6fc8be2b7b15e41431ebe4813a2c7df854c5ddd",
      "review_round": 3,
      "score": 95,
      "review_sha256": "459046648d77e82735a3313e7f0594eaaae26d27fa358fda38c81307af961d0b",
      "collection_sha256": "253d4cab9798ba93ba189ae645dc4dc5fc1215033fce48548b84df0a2e7a31af"
    },
    {
      "ref": "@gitfs/improve-gitfs-reviewable-ship/recorded-push-reconciles-the-exact-remote-head",
      "source_commit": "b8f27c6f1c07888bfc6e5d09f45a8751e8ca7b36",
      "prd_sha256": "f7fb33f8f5d0d3101c0ba516964d06bd893f39e000170efe4541725625e9d380",
      "spec_sha256": "6733e87f3f84226f8070a1c66b494ca4931f4145bc6281ca1517e3c12f153569",
      "review_round": 3,
      "score": 96,
      "review_sha256": "838bc559f5655e3165c2a7458f5da866761ba41af85b65c5ea40986dd7b15116",
      "collection_sha256": "44977c90879b4740183345464d5f809751cf64c2f83bb3d8a31dc0b708a8a7e7"
    }
  ],
  "composition_proof_sha256": "b8845814d7e60b7492ece92f6d4f60c1269e7f73e4f5ec7054004c3031dcc9d2"
}
    Finished `test` profile [unoptimized] target(s) in 0.10s
     Running unittests src/main.rs (target/tool-result-contract/debug/deps/gitfs-c66fa7605aaad949)

running 47 tests
test provenance::tests::context_is_bounded_and_legacy_missing_coordinates_stay_null ... ok
test push::tests::cancelled_command_kills_the_spawned_helper_group ... ok
test push::tests::hook_requires_exactly_one_complete_advertised_update ... ok
test push::tests::receipt_looking_prose_or_conflicting_trailers_do_not_authorize_push ... ok
test secrets::tests::context_lines_are_not_scanned ... ok
test secrets::tests::has_secret_detects_and_allows_plain ... ok
test secrets::tests::placeholder_token_is_ignored ... ok
test secrets::tests::real_key_on_added_line_finds ... ok
test secrets::tests::scan_file_matches ... ok
test secrets::tests::sensitive_filename_is_flagged_even_with_plain_content ... ok
test secrets::tests::template_files_are_skipped_entirely ... ok
test push::tests::command_timeout_and_overflow_are_bounded_and_do_not_expose_stderr ... ok
test provenance::tests::nonregular_or_alias_preimages_are_rejected_without_waiting_for_a_writer ... ok
test provenance::tests::receipt_validation_rejects_arbitrary_success_or_wrong_publications ... ok
test provenance::tests::locked_overlay_receipts_pin_old_blob_tip_and_first_parent_without_inventing_overlay ... ok
test ship::tests::active_cancellation_is_exact_bounded_and_drop_cancels_the_blocking_work ... ok
test ship::tests::auto_subject_shapes ... ok
test ship::tests::configured_gate_and_author_are_validated_instead_of_defaulting_invalid_types ... ok
test ship::tests::gate_prompt_demands_json_only ... ok
test ship::tests::preview_revision_binds_author_required_gate_timeout_subject_and_force ... ok
test ship::tests::secret_subject_is_rejected_and_plain_passes ... ok
test service::snapshot_tests::guarded_edit_still_refuses_stale_content ... ok
test service::snapshot_tests::read_failures_report_partial_success_and_preserve_failed_overlay ... ok
test provenance::tests::metadata_caps_and_unreadable_preimage_never_claim_complete_attribution ... ok
test store::tests::missing_publication_ack_remains_unknown_after_later_advance_or_failed_readback ... ok
test provenance::tests::materialize_keeps_exact_applied_evidence_and_reports_failed_deletion_and_ledger ... ok
test push::tests::durable_attempt_capacity_corruption_and_monotonic_observation ... ok
test service::snapshot_tests::selected_snapshot_records_only_new_commits_and_retains_partial_evidence ... ok
test provenance::tests::concurrent_same_session_receipts_form_the_actual_locked_commit_chain ... ok
test service::snapshot_tests::selection_is_exact_empty_is_empty_and_unowned_is_rejected_before_writes ... ok
test store::tests::materialize_guard ... ok
test store::tests::concurrent_reviewed_publications_have_one_winner_and_preserve_worktree_and_index ... ok
test store::tests::roundtrip_and_noop ... ok
test tool_result::tests::inspection_baseline_diff_is_available ... ok
test tool_result::tests::inspection_baseline_read_does_not_create_a_store ... ok
test store::tests::multi_path_overlay_survives_rewrite ... ok
test store::tests::prepared_head_transaction_holds_the_symbolic_branch_until_decision ... ok
test tool_result::tests::payloads_are_encoded_once_and_text_stays_literal ... ok
test tool_result::tests::invalid_inputs_do_not_open_the_store ... ok
test store::tests::concurrent_overlay_writes_keep_every_path ... ok
test store::tests::unrelated_overlay_sessions_do_not_share_a_mutation_lock ... ok
test tool_result::tests::inspection_absence_binary_bounds_and_path_failures_are_explicit ... ok
test store::tests::reviewed_publication_refuses_stale_head_without_deleting_new_unowned_files ... ok
test store::tests::ship_trailer_undo_and_no_remote ... ok
test store::tests::reviewed_publication_binds_index_overlay_branch_and_repository_identity ... ok
test provenance::tests::real_bulk_materialization_preserves_effects_after_record_cap_and_late_write_failure ... ok
test tool_result::tests::real_consumers_share_the_tool_result_contract ... ok

test result: ok. 47 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 14.24s

   Compiling ring v0.17.14
   Compiling rustls v0.23.44
    Checking rustls-webpki v0.103.15
    Checking tokio-rustls v0.26.5
    Checking hyper-rustls v0.27.9
    Checking reqwest v0.12.28
    Checking gitfs v0.1.0 (/Users/feb/dev/cartridge/gitfs.ctg)
    Finished `dev` profile [unoptimized] target(s) in 2.85s
   Compiling ring v0.17.14
   Compiling rustls-webpki v0.103.15
   Compiling rustls v0.23.44
   Compiling tokio-rustls v0.26.5
   Compiling hyper-rustls v0.27.9
   Compiling reqwest v0.12.28
   Compiling gitfs v0.1.0 (/Users/feb/dev/cartridge/gitfs.ctg)
    Finished `dev` profile [unoptimized] target(s) in 3.29s
    Finished `dev` profile [unoptimized] target(s) in 0.08s
    Finished `dev` profile [unoptimized] target(s) in 0.06s
bun test v1.3.14 (0d9b296a)

../gitfs.ctg/.cartridge/tests/integration/reviewed-ship.test.ts:
(pass) native required gate is fail-closed for explicit subjects, body timeout and cancellation; exact success never pushes [2374.42ms]
(pass) native stale reviews preserve external commits, and concurrent commits publish once without a configured model [983.58ms]
(pass) native force never bypasses a gate and oversized required review never silently truncates [952.23ms]

../gitfs.ctg/.cartridge/tests/integration/recorded-push.test.ts:
(pass) native recorded push requires reviewed exact binding and never replays operation identities [1785.15ms]
(pass) native push refuses changed remote, nonancestor, ambiguous URLs and rewrite rules [1096.97ms]
(pass) lost response stays durable unknown across restart; old readback cannot permit replay, exact readback confirms [3113.01ms]
(pass) native cancellation and overflow keep bounded unknown evidence and do not leak helper stderr [2066.16ms]
(pass) owned hook refuses an advertised head changed after preview check; durable refusal survives restart [1155.81ms]
(pass) server CAS refuses advance after the validated advertisement without changing local history [1209.30ms]

 9 pass
 0 fail
 544 expect() calls
Ran 9 tests across 2 files. [14.89s]
{
  "schema": "gitfs-reviewable-rollup/v1",
  "actual_providers": [
    "GitFS native",
    "MCP native",
    "policy Lua"
  ],
  "session": "reviewable-rollup",
  "base": "4807f6a593c1df1d4d184e460225c4b1a2e0ebdd",
  "local_commit": "d5f80d0166be517765e228e8fb1925a5b11fb540",
  "tree": "6310d0e9f6ae49234a336f0de4117c7f9cd2c967",
  "local_revision": "0533f7957dbfe47e6ffb274a816e620866e661a433017b01ac803744cb6facdd",
  "push_revision": "cfe2c4191b2294ec0e7245cc3efe80bf53c2789037bad80528d5b3b11c7bb44c",
  "push_status": "confirmed",
  "reconcile_status": "confirmed",
  "unrelated_staged_excluded": true,
  "index_unchanged": true,
  "unselected_snapshot_preserved": true,
  "unrelated_remote_ref_unchanged": true,
  "policy_denial_executed": false,
  "binaries": {
    "cartridge": "3c107ead7a60caa07a7aa295cb46c7b2a0663a17ca7aa11fc11b45076b9b08c8",
    "gitfs": "b095286cae2b0162581dd6bead1657c5a7c6ebc4c0a134403ca72859d04dfb8a",
    "mcp": "d1d48482f944205f3d589031fbcbbc7c1699e095fa139792a4ff4c1037a09727"
  }
}

```
