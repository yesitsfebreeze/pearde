---
commit: "d9161cd2f3a363915c7a7d642a4955e7a3836065"
verification-target: "committed"
original-commit: "d9161cd2f3a363915c7a7d642a4955e7a3836065"
spec-digests: {"implementation.md":"cd151943e922c65d991f1d19ce4ed9b923bf44239ed4ded341fd3e967848ffe5"}
child-contracts: {}
workspace-verified: false
workspace-drift: [{"path":".cartridge/help.md","sha256":"bc741307d5c41d147f591bd487954d56502e18f9995ee954910fa1f6379bd6d5"},{"path":"README.md","sha256":"9c043e9109c2630c5c649af18e818c40d65fa905bd24696c6069ac67b304eb02"},{"path":"src/graph/src/experience/undo.rs","sha256":"9db52f2276b72db23706dc3cb1eaae344e626e1d4c11239af99b58f3cccf6f86"}]
---

# Collection

Verified committed snapshot d9161cd2f3a363915c7a7d642a4955e7a3836065 in /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source.

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/prds/memory-crystallizes-the-systems-activity-by-its-reasons/memory-stands-alone-with-clear-engine-and-integration-boundaries/specs/implementation.md: exit 0

Command SHA-256: 484a7a845d89a1f96039fa6b98f3eab612ce8a8a14ae9ca4bc59d50b72813936

```text
passed: experience_recurrence_and_reason_boundaries, experience_survives_reload_and_undo_restores_indexes, experience_intake_retry_recurrence_restart_and_opposite_outcome, experience_failed_commit_restores_graph_and_retains_input, experience_commit_refuses_older_full_flush_and_migrates_history, experience_receipts_survive_commit_and_expire_without_accepting_old_delivery, experience_read_only_search_never_enqueues_usage_on_fresh_or_cached_queries, experience_reason_space_separates_outcomes_without_rewriting_content
/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/identity)
   Compiling graph v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/graph)
   Compiling retrieval-piece v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/retrieval/piece)
   Compiling tick v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/tick)
   Compiling ingest v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/ingest)
   Compiling bootstrap v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/bootstrap)
   Compiling retrieval v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/retrieval)
   Compiling tick_loop v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/tick/loop)
   Compiling store v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/store)
   Compiling health v0.1.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/health)
   Compiling rpc v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/rpc)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 4.30s
     Running unittests src/lib.rs (/tmp/cartridge-memory-stack-independent-target/debug/deps/graph-26370a2107f51966)

running 5 tests
test experience::tests::experience_retirement_invalidates_shortcut_without_overwriting_history ... ok
test experience::tests::experience_repeat_rehydrates_unloaded_owner_and_preserves_other_indexes ... ok
test experience::tests::experience_survives_reload_and_undo_restores_indexes ... ok
test experience::tests::experience_recurrence_and_reason_boundaries ... ok
test experience::tests::experience_repeat_burst_measurement ... ok

test result: ok. 5 passed; 0 failed; 0 ignored; 0 measured; 179 filtered out; finished in 0.67s

     Running unittests src/lib.rs (/tmp/cartridge-memory-stack-independent-target/debug/deps/rpc-64010245428f3d5b)

running 11 tests
test experience::tests::experience_legacy_decode_preserves_large_preexisting_rows ... ok

running 1 test
test experience::tests::experience_failed_commit_restores_graph_and_retains_input ... ok
test experience::tests::experience_concurrent_passes_commit_each_delivery_once ... ok
test experience::tests::experience_commit_refuses_older_full_flush_and_migrates_history ... ok
test experience::tests::experience_missing_embedder_retains_acknowledged_input ... ok
test experience::tests::experience_external_writer_blocks_without_discarding_ram ... ok
test experience::tests::experience_asp_pages_reasons_and_usage_without_mutation ... ok
test experience::tests::experience_read_only_search_never_enqueues_usage_on_fresh_or_cached_queries ... ok
test experience::tests::experience_intake_retry_recurrence_restart_and_opposite_outcome ... ok
test experience::tests::experience_crash_after_commit_preserves_receipts ... ok
test experience::tests::experience_ordinary_save_and_crystallization_preserve_dirty_work ... ok

test result: ok. 11 passed; 0 failed; 0 ignored; 0 measured; 98 filtered out; finished in 0.28s

     Running unittests src/lib.rs (/tmp/cartridge-memory-stack-independent-target/debug/deps/store_core-8140b5a572fe661c)

running 2 tests
test experience::tests::experience_intake_enforces_delivery_window_and_payload_bound ... ok
test experience::tests::experience_receipts_survive_commit_and_expire_without_accepting_old_delivery ... ok

test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 75 filtered out; finished in 0.03s

     Running unittests src/lib.rs (/tmp/cartridge-memory-stack-independent-target/debug/deps/tick_loop-dad2a3cdca644bdb)

running 1 test
test tick_cluster::tick_cluster_tests::experience_reason_space_separates_outcomes_without_rewriting_content ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 73 filtered out; finished in 0.00s


```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/prds/memory-crystallizes-the-systems-activity-by-its-reasons/memory-stands-alone-with-clear-engine-and-integration-boundaries/specs/implementation.md: exit 0

Command SHA-256: b324e867b764fe5f961ae0f3c31db0828f8144ce208e6fcaacb8cb035f41d90b

```text
passed: a_memory_entity_expands_to_its_node_with_the_observed_projection_revision, search_and_expand_agree_with_context_memory_on_a_real_bank, the_shipped_declaration_is_one_the_host_accepts
til)
   Compiling audit v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/hotreload/audit)
   Compiling memory_transport_macros v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/transport/macros)
   Compiling memory_cartridge v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/cartridge)
   Compiling hotreload v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/hotreload)
   Compiling base v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/base)
   Compiling llm v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/llm)
   Compiling memory_transport v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/transport)
   Compiling ingest_config v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/ingest/config)
   Compiling math v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/math)
   Compiling test_support v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/.cartridge/tests/support)
   Compiling config v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/config)
   Compiling store_core v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/store/core)
   Compiling gnn v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/gnn)
   Compiling identity v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/identity)
   Compiling graph v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/graph)
   Compiling hub v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/hub)
   Compiling retrieval-piece v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/retrieval/piece)
   Compiling tick v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/tick)
   Compiling ingest v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/ingest)
   Compiling bootstrap v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/bootstrap)
   Compiling retrieval v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/retrieval)
   Compiling tick_loop v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/tick/loop)
   Compiling store v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/store)
   Compiling health v0.1.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/health)
   Compiling rpc v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/rpc)
   Compiling commands v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/commands)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 4.62s
     Running unittests src/lib.rs (/tmp/cartridge-memory-stack-independent-target/debug/deps/memory_cartridge-29a9f7cef8e68873)

running 6 tests
test asp::tests::the_shipped_declaration_is_one_the_host_accepts ... ok
test asp::tests::a_memory_entity_expands_to_its_node_with_the_observed_projection_revision ... ok
test asp::tests::search_keeps_the_context_filtering_exactly ... ok
test asp::tests::expand_answers_nothing_for_a_missing_private_expired_or_respelled_key ... ok
test asp::tests::search_delivers_ranked_rows_without_reading_any_back ... ok
test asp::tests::search_and_expand_agree_with_context_memory_on_a_real_bank ... ok

test result: ok. 6 passed; 0 failed; 0 ignored; 0 measured; 21 filtered out; finished in 0.14s


```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/prds/memory-crystallizes-the-systems-activity-by-its-reasons/memory-stands-alone-with-clear-engine-and-integration-boundaries/specs/implementation.md: exit 0

Command SHA-256: ec20757d6692bc3039c7c3fafec9e54c3a5098709e287d1c321122d32eead872

```text
    Checking util v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/util)
    Checking audit v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/hotreload/audit)
    Checking memory_transport v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/transport)
    Checking memory_transport_macros v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/transport/macros)
    Checking hotreload v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/hotreload)
    Checking base v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/base)
    Checking llm v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/llm)
    Checking ingest_config v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/ingest/config)
    Checking math v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/math)
    Checking test_support v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/.cartridge/tests/support)
    Checking config v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/config)
    Checking store_core v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/store/core)
    Checking gnn v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/gnn)
    Checking identity v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/identity)
    Checking graph v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/graph)
    Checking hub v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/hub)
    Checking retrieval-piece v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/retrieval/piece)
    Checking tick v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/tick)
    Checking ingest v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/ingest)
    Checking bootstrap v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/bootstrap)
    Checking retrieval v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/retrieval)
    Checking tick_loop v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/tick/loop)
    Checking store v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/store)
    Checking memory-bench v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/.cartridge/tests/integration/bench)
    Checking health v0.1.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/health)
    Checking rpc v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/rpc)
    Checking commands v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/commands)
    Checking memory v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source)
    Checking memory_cartridge v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-H8DUeh/source/src/cartridge)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 7.16s

```
