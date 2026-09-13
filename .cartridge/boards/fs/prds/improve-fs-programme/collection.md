---
commit: 3a79023311b1a9b30c383ec8c71cf31c20a69ee7
spec-digests: {"spec01.md":"a3c330c6c0900d2a532f352a8e5e69f24d7bd372130436b2d49bd0fa6fa4a5ba"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/fs/prds/improve-fs-programme/specs/spec01.md: exit 0

Command SHA-256: 8f88e3fc8fdfb02071f9fa38e3ad93b1fe122893c186fc329e72c978ed09175c

```text
{
  "source_commit": "3a79023311b1a9b30c383ec8c71cf31c20a69ee7",
  "records_commit": "dfa0e1ecdbb86b5fbf12268cf2e9d6ed5b4bc9b1",
  "footprint": [
    ".cartridge/docs/change-provenance.md",
    ".cartridge/docs/revision-guards.md",
    ".cartridge/docs/search-pages.md",
    ".cartridge/tests/integration/change-provenance.test.ts",
    ".cartridge/tests/unit/search/tests.rs",
    ".cartridge/tests/unit/service/tests.rs",
    "Cargo.toml",
    "cartridge.json",
    "src/context.rs",
    "src/files.rs",
    "src/main.rs",
    "src/search.rs",
    "src/service.rs"
  ],
  "dependencies": [
    {
      "ref": "@fs/improve-fs-change-provenance",
      "source_commit": "3a79023311b1a9b30c383ec8c71cf31c20a69ee7",
      "prd_sha256": "1c5f48fd2abad4fd4b2d9e472e997b9a6097d44ee9ac29debd07c838e578ba2f",
      "spec_sha256": "0995591014a02ea39caff602ed90e46b6ab9f42c363ad83e982a227b673a7d7a",
      "review_round": 3,
      "score": 95,
      "review_sha256": "cb43f577b8eb382aa9d347e2fba87c92a9ee412d0fe983b9e027db5a2fc01c8b",
      "collection_sha256": "b32b96442546fc8ea3af032d1c307a0602edd2f1a52e34196f1e311767294ce5"
    },
    {
      "ref": "@fs/improve-fs-change-provenance/direct-file-mutations-report-revisions",
      "source_commit": "3a79023311b1a9b30c383ec8c71cf31c20a69ee7",
      "prd_sha256": "874c31414a7d236a4021b8f40661e54ae1d7391cb288c3b53b31533f077bc705",
      "spec_sha256": "7f555535bc670f5f6b81eba76005ef6527b1861aa1bbde12366a336ece545235",
      "review_round": 3,
      "score": 95,
      "review_sha256": "55978d3381f6065e7932d4b634d6def9cbb66da2eb78079fbdd961b5ba605c9e",
      "collection_sha256": "4c8da549485588cf1af071bc902a54cbf8fb89c93f1f9a8c325226ae3b17f0b2"
    },
    {
      "ref": "@fs/improve-fs-revision-guards",
      "source_commit": "3a79023311b1a9b30c383ec8c71cf31c20a69ee7",
      "prd_sha256": "cdacea0193df104b21f7c2e4d7c90c047773e0f704e6054dd6d1884f1b9a5d4f",
      "spec_sha256": "78fe6d4d246cd3242bb1d3350cad68982c04e2fd9ba14fb5e1c9b6b23f5c6692",
      "review_round": 4,
      "score": 95,
      "review_sha256": "9cbf0ed11fed360d61e23ef5f8e569b46b4ae3dffaedc4bf86e8da9cc871adf1",
      "collection_sha256": "7d09eca0a9d3ada87633965f6f06c63fdc8a143b564af7e5bc47e2a2f3a1f131"
    },
    {
      "ref": "@fs/improve-fs-search-pages",
      "source_commit": "3a79023311b1a9b30c383ec8c71cf31c20a69ee7",
      "prd_sha256": "59c4d9e6d08a45a2c9b4d3fd681b0aa8cdd0feb1726e1dc6712161d86c2e15a9",
      "spec_sha256": "8a6cbf888240ed84069b1dd80c8b73e407357fcf01393fc852239c813a7a6d4d",
      "review_round": 3,
      "score": 95,
      "review_sha256": "5bd22b2a31414f269a493c97ad8e698a058ffd2dc2350aa20171794e6d03ff71",
      "collection_sha256": "f317be790cfff8e2863c634474d4d02ba316edc74db4af600c4dea0fcd92fc85"
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
      "ref": "@gitfs/overlay-mutations-report-revisions",
      "source_commit": "b8f27c6f1c07888bfc6e5d09f45a8751e8ca7b36",
      "prd_sha256": "917a66a3cbb21cb3a4cf6b8e3594e6ddd967e23e2aadb9dbabc1b499fa929775",
      "spec_sha256": "05db280989830d7933859d5d87e2796d0513ed4147e3976883604e1536a8963a",
      "review_round": 3,
      "score": 94,
      "review_sha256": "6ff5b446a04451a7deda8d3516938ed4638d4ba667575be2200156b7ccc68df5",
      "collection_sha256": "71666fa28c495ada609941e8cf9a649201eb624c02cdfd96f520bf49a8dc3763"
    },
    {
      "ref": "@gitfs/tool-results-interoperate",
      "source_commit": "b8f27c6f1c07888bfc6e5d09f45a8751e8ca7b36",
      "prd_sha256": "a284102ceabf68ab6000f37992c22585feefd1076891db81c7d56acede6f0af0",
      "spec_sha256": "87b2a12e71d8a7eab761833e18236315866bf8e5cfbe470738c90cc6a3de9cb4",
      "review_round": 3,
      "score": 96,
      "review_sha256": "0e016083c728e357a89a6b6b810b0bdf05949739f4f4aa608afcaeb091fc25e5",
      "collection_sha256": "6518ff6407b4bcc34a1b25781d056d246bc4b81d418be63fe10b36ab72eed922"
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
      "ref": "@runtime/shipped-gitfs-profiles-grant-change-recording",
      "source_commit": "8e514eace6b88d4ef4e55aa5f031e539ab28eb5b",
      "prd_sha256": "39f513d89d0a5f2fda4953bb73224423383d43dd888e71e9840884cd0609eb0a",
      "spec_sha256": "87a0b5ba0c3937ec9552b6d047f357e9d45ab176de2c28cc3940b13a2f7ed885",
      "review_round": 3,
      "score": 96,
      "review_sha256": "b3c8b3aa4dd1fe32707f18e4874dd98879de56901f25e39025ff93ce72b79480",
      "collection_sha256": "87ec8b7c621c7bc5a6e701192a6b91303021a9b1a0aec62e168e72d68cd57b18"
    },
    {
      "ref": "@sessions/file-change-records-retain-reported-revisions",
      "source_commit": "191e2b6cb4291bdcce7a894f98bb2d475361d30f",
      "prd_sha256": "560ec93d79b842097e2abf736a038fa49ac70919f63f76a2952ed35f29a7a578",
      "spec_sha256": "7d0403c1823ba82837ddae2bffc6a8eb6337ff408250e909d9f00984ad707a84",
      "review_round": 3,
      "score": 96,
      "review_sha256": "7b69e2d01c9c7048df611b8b3d608febabc676707bd963f2623d209384445218",
      "collection_sha256": "72afa5e21e3319929b3362f1fd0c6a4b61800489d8bb685d3471f10386b2c1ad"
    },
    {
      "ref": "@sessions/improve-sessions-client-mapping",
      "source_commit": "191e2b6cb4291bdcce7a894f98bb2d475361d30f",
      "prd_sha256": "7ab9e3f5bec5776afc360d81feda9b5b14e976e6a2c4b86838871e3c544b9f3f",
      "spec_sha256": "8bcedb4cf0eed743beb8bff4a5c9d4455e401035671e8787a8dda0700c1db87f",
      "review_round": 3,
      "score": 96,
      "review_sha256": "4e4e69a466fdedaa7f85b57d8be6cec826086d8c7605f2b227f1bf34866848ee",
      "collection_sha256": "84fa7f44b40082d4febff6bf1bb87ac4937ab032043e1d761a4d408ff94f1c27"
    }
  ],
  "fixtures": {
    "/Users/feb/dev/cartridge/fs.ctg/.cartridge/tests/integration/context.test.ts": "5239eacb5463d1a6e032c0c6cd22ff370458d574621ac3a5ec486de4244b1264",
    "/Users/feb/dev/cartridge/fs.ctg/.cartridge/tests/integration/change-provenance.test.ts": "fd336db0d75f54db3b6a01ca5fb5700437e2d0fd455d4ea1c266163edb7f4173",
    "/Users/feb/dev/cartridge/gitfs.ctg/.cartridge/tests/integration/change-provenance.test.ts": "db018e5ea32233f4ca8c4ff3e1bc0dbab59b5a85c3510f93c1eebc7af9f7e9a5",
    "/Users/feb/dev/cartridge/gitfs.ctg/.cartridge/tests/integration/tool-result.test.ts": "1c7d95e7cb20545b2dd3d67196dfdd096ad67b1fbad281f285ba0ca6e5016033",
    "/Users/feb/dev/cartridge/gitfs.ctg/.cartridge/tests/integration/reviewed-ship.test.ts": "2cd16fcb495650e8266fb5cdf660e868f656b547768e4777dd1e9c996fc806f9",
    "/Users/feb/dev/cartridge/gitfs.ctg/.cartridge/tests/integration/recorded-push.test.ts": "0c6b4e111e2aea72d3736b5df433a6998ced1d076a417179b75e78361da4953a",
    "/Users/feb/dev/cartridge/sessions.ctg/.cartridge/tests/integration/change-records.test.ts": "56611256a47d763dd4ebe014e7b82f122888a483009f182c33df4812a8eaee42",
    "/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/fs/prds/improve-fs-change-provenance/rollup-check.ts": "ecaaa4e83b14321a6d4b6c44e2d2b82035c3632d285ab0cf32122379bc54f12f",
    "/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/fs/prds/improve-fs-change-provenance/rollup-bindings.json": "3f64cdb5ae814e57ac6b586902b3bd74b83cd7c3ac99dcbac5f50139fdad5905"
  }
}
    Finished `test` profile [unoptimized] target(s) in 0.11s
     Running unittests src/main.rs (target/tool-result-contract/debug/deps/fs-0ae3e717031e9602)

running 51 tests
test search::tests::empty_stages_is_an_empty_set_never_a_sweep ... ok
test context::tests::typed_record_case_aliases_and_directory_identities_are_excluded ... ok
test context::tests::exact_bytes_and_source_revisions_preserve_every_newline ... ok
test context::tests::strict_caps_and_unavailable_sources_never_return_partial_text ... ok
test search::tests::incompatible_stages_reject_before_execution ... ok
test search::tests::cursor_scope_expiry_and_cancellation_are_explicit ... ok
test search::tests::captured_pages_replay_after_tree_changes_and_new_queries_refresh ... ok
test search::tests::match_set_cannot_be_grepped_without_files_of ... ok
test context::tests::pinned_handle_refuses_observed_replacement_and_deadline_drops_response ... ok
test search::tests::missing_rg_is_actionable_not_empty ... ok
test search::tests::active_search_cancellation_reaps_the_backend ... ok
test search::tests::deadlock_deadline_terminates_and_reaps_child ... ok
test search::tests::deadline_covers_child_wait_after_stdout_is_closed ... ok
test search::tests::pre_cancelled_invocation_spawns_no_process ... ok
test search::tests::page_has_a_continuation_for_the_rest ... ok
test search::tests::fake_rg_error_exit_is_a_failure ... ok
test search::tests::snapshot_budget_fails_without_eviction_and_retirement_frees_it ... ok
test service::tests::cancel_during_spawn_prevents_mutation ... ok
test service::tests::cancellation_after_preparation_leaves_no_mutation_or_temp ... ok
test search::tests::real_grep_keeps_over_200_matches_and_empty_chains_do_not_sweep ... ok
test service::tests::competing_sessions_with_one_observed_revision_have_one_winner ... ok
test service::tests::commit_rechecks_symlinks_and_preserves_executable_modes ... ok
test service::tests::concurrent_creators_preserve_the_winner ... ok
test service::tests::describe_names_and_schemas_match_the_three_keys ... ok
test service::tests::direct_evidence_uses_guarded_bytes_and_unique_publication_identity ... ok
test service::tests::create_overwrite_and_edit_variants ... ok
test service::tests::failed_cleanup_after_known_publication_still_records_once ... ok
test service::tests::failed_preparation_preserves_bytes_and_permissions ... ok
test service::tests::disappearance_and_creation_at_publication_are_conflicts ... ok
test service::tests::observation_failure_after_publication_is_explicit_partial_success ... ok
test service::tests::newer_bytes_at_commit_survive_write_and_edit ... ok
test service::tests::partial_read_establishes_freshness_only ... ok
test service::tests::path_escapes_and_forged_context_fail_before_mutation ... ok
test service::tests::pre_cancelled_call_never_mutates ... ok
test service::tests::read_byte_limit_truncates ... ok
test service::tests::read_offsets_limits_binary_and_missing ... ok
test search::tests::fake_rg_receives_literal_arguments_no_shell ... ok
test service::tests::receipt_requires_exact_id_publication_digest_and_one_persisted_sequence ... ok
test service::tests::touch_failure_reports_partial_success_with_the_file ... ok
test service::tests::stale_version_fails_until_reread_including_same_size_with_restored_mtime ... ok
test service::tests::unread_overwrite_fails_without_changing_bytes ... ok
test service::tests::unseen_edit_fails_without_changing_bytes ... ok
test service::tests::touch_records_successful_mutations_only ... ok
test search::tests::large_real_tree_pages_every_identity_once_and_ref_keeps_the_tail ... ok
test search::tests::malformed_backend_output_fails_explicitly ... ok
test search::tests::matching_json_backend_produces_typed_items ... ok
test search::tests::output_survives_cancellation_polls ... ok
test search::tests::oversized_results_report_truncation ... ok
test search::tests::user_config_cannot_change_results ... ok
test search::tests::floods_and_oversized_items_fail_instead_of_claiming_completeness ... ok
test service::tests::recording_timeout_is_bounded_unknown_and_never_replays_file_publication ... ok

test result: ok. 51 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 2.35s

    Finished `dev` profile [unoptimized] target(s) in 0.09s
    Finished `dev` profile [unoptimized] target(s) in 0.09s
    Finished `dev` profile [unoptimized] target(s) in 0.12s
    Finished `dev` profile [unoptimized] target(s) in 0.09s
    Finished `dev` profile [unoptimized] target(s) in 0.07s
bun test v1.3.14 (0d9b296a)

../fs.ctg/.cartridge/tests/integration/context.test.ts:
(pass) native FS snapshots return exact full bytes and preserve legacy tool reads without touches [452.47ms]
(pass) native FS refuses typed aliases, unsafe sources and cap overflow without partial payload [19.71ms]

../fs.ctg/.cartridge/tests/integration/change-provenance.test.ts:
(pass) real Host composes FS and Sessions for exact publication records and restart without GitFS ownership [1153.69ms]
(pass) native malformed refused and timed-out recorders report partial publication without retry [2032.36ms]

../gitfs.ctg/.cartridge/tests/integration/change-provenance.test.ts:
(pass) real Host direct and overlay evidence preserves divergence, operation tags, restart and explicit ownership [1863.95ms]
(pass) actual standalone profile omits Sessions and keeps GitFS mutations available with honest unavailable attribution [285.99ms]
(pass) failed grant discovery never silently disables recording and failed recorders preserve committed effects without replay [4842.21ms]

../gitfs.ctg/.cartridge/tests/integration/tool-result.test.ts:
(pass) real SDK, MCP and proxy preserve tool payloads and do not replay failed effects [4173.68ms]
(pass) real MCP inspection obeys operation policy and preserves repository state [5369.11ms]

../gitfs.ctg/.cartridge/tests/integration/reviewed-ship.test.ts:
(pass) native required gate is fail-closed for explicit subjects, body timeout and cancellation; exact success never pushes [2754.97ms]
(pass) native stale reviews preserve external commits, and concurrent commits publish once without a configured model [1425.23ms]
(pass) native force never bypasses a gate and oversized required review never silently truncates [1480.18ms]

../gitfs.ctg/.cartridge/tests/integration/recorded-push.test.ts:
(pass) native recorded push requires reviewed exact binding and never replays operation identities [2364.12ms]
(pass) native push refuses changed remote, nonancestor, ambiguous URLs and rewrite rules [1603.91ms]
(pass) lost response stays durable unknown across restart; old readback cannot permit replay, exact readback confirms [3401.01ms]
(pass) native cancellation and overflow keep bounded unknown evidence and do not leak helper stderr [2948.07ms]
(pass) owned hook refuses an advertised head changed after preview check; durable refusal survives restart [1846.28ms]
(pass) server CAS refuses advance after the validated advertisement without changing local history [1691.89ms]

../sessions.ctg/.cartridge/tests/integration/change-records.test.ts:
(pass) native distinct direct and overlay publications persist with exact read-only pages and legacy metadata [63.44ms]
(pass) native strict DTOs, duplicate conflicts, and atomic invalid batches preserve snapshot [28.59ms]
(pass) native legacy snapshots remain readable and corrupt retained evidence is diagnosed without repair [39.97ms]
(pass) native count capacity and byte-bounded pages keep all retained publication identities [1219.95ms]

 22 pass
 0 fail
 1250 expect() calls
Ran 22 tests across 7 files. [41.26s]

```
