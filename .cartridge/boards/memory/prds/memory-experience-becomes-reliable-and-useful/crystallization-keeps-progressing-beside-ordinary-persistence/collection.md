---
commit: "d9161cd2f3a363915c7a7d642a4955e7a3836065"
verification-target: "committed"
original-commit: "d9161cd2f3a363915c7a7d642a4955e7a3836065"
spec-digests: {"implementation.md":"29ebecfc4e5bf3e38c6b2de09d3d2bd9c7982c6f8a4d9743b8aba524782096e5"}
child-contracts: {}
workspace-verified: false
workspace-drift: [{"path":".cartridge/help.md","sha256":"bc741307d5c41d147f591bd487954d56502e18f9995ee954910fa1f6379bd6d5"},{"path":"README.md","sha256":"9c043e9109c2630c5c649af18e818c40d65fa905bd24696c6069ac67b304eb02"}]
---

# Collection

Verified committed snapshot d9161cd2f3a363915c7a7d642a4955e7a3836065 in /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source.

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/prds/memory-experience-becomes-reliable-and-useful/crystallization-keeps-progressing-beside-ordinary-persistence/specs/implementation.md: exit 0

Command SHA-256: c0599b0c84622aa0e7c1cc48079b312902c2b0df0c83bc33e13ed54ce72f874d

```text
passed: writer_publication_is_coordinated_without_holding_graph_lock, writer_gates_are_independent_between_stores, writer_reconciliation_waits_for_publication_and_preserves_dirty_ram, writer_external_advance_never_automatically_replaces_ram
   Compiling util v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/util)
   Compiling audit v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/hotreload/audit)
   Compiling base v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/base)
   Compiling llm v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/llm)
   Compiling hotreload v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/hotreload)
   Compiling ingest_config v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/ingest/config)
   Compiling math v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/math)
   Compiling config v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/config)
   Compiling store_core v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/store/core)
   Compiling graph v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/graph)
   Compiling bootstrap v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/bootstrap)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 3.02s
     Running unittests src/lib.rs (/tmp/cartridge-memory-stack-baseline-target/debug/deps/bootstrap-d0bfd9d3839c0d6e)

running 4 tests
test writer_tests::writer_external_advance_never_automatically_replaces_ram ... ok
test writer_tests::writer_gates_are_independent_between_stores ... ok
test writer_tests::writer_reconciliation_waits_for_publication_and_preserves_dirty_ram ... ok
test writer_tests::writer_publication_is_coordinated_without_holding_graph_lock ... ok

test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.10s


```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/prds/memory-experience-becomes-reliable-and-useful/crystallization-keeps-progressing-beside-ordinary-persistence/specs/implementation.md: exit 0

Command SHA-256: ecef3d7345f797ac8c1f241303d424f092fb7144aa1d5632291807b404f2b780

```text
passed: experience_ordinary_save_and_crystallization_preserve_dirty_work, experience_external_writer_blocks_without_discarding_ram, experience_concurrent_passes_commit_each_delivery_once, experience_crash_after_commit_preserves_receipts, experience_commit_refuses_older_full_flush_and_migrates_history, experience_failed_commit_restores_graph_and_retains_input
t)
   Compiling memory_transport_macros v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/transport/macros)
   Compiling hotreload v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/hotreload)
   Compiling base v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/base)
   Compiling llm v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/llm)
   Compiling memory_transport v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/transport)
   Compiling ingest_config v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/ingest/config)
   Compiling math v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/math)
   Compiling test_support v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/.cartridge/tests/support)
   Compiling store_core v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/store/core)
   Compiling config v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/config)
   Compiling gnn v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/gnn)
   Compiling identity v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/identity)
   Compiling graph v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/graph)
   Compiling retrieval-piece v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/retrieval/piece)
   Compiling tick v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/tick)
   Compiling ingest v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/ingest)
   Compiling bootstrap v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/bootstrap)
   Compiling retrieval v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/retrieval)
   Compiling tick_loop v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/tick/loop)
   Compiling store v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/store)
   Compiling health v0.1.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/health)
   Compiling rpc v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/rpc)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 8.20s
     Running unittests src/lib.rs (/tmp/cartridge-memory-stack-baseline-target/debug/deps/rpc-64010245428f3d5b)

running 11 tests
test experience::tests::experience_legacy_decode_preserves_large_preexisting_rows ... ok
test experience::tests::experience_asp_pages_reasons_and_usage_without_mutation ... ok
test experience::tests::experience_failed_commit_restores_graph_and_retains_input ... ok

running 1 test
test experience::tests::experience_external_writer_blocks_without_discarding_ram ... ok
test experience::tests::experience_commit_refuses_older_full_flush_and_migrates_history ... ok
test experience::tests::experience_missing_embedder_retains_acknowledged_input ... ok
test experience::tests::experience_concurrent_passes_commit_each_delivery_once ... ok
test experience::tests::experience_read_only_search_never_enqueues_usage_on_fresh_or_cached_queries ... ok
test experience::tests::experience_intake_retry_recurrence_restart_and_opposite_outcome ... ok
test experience::tests::experience_crash_after_commit_preserves_receipts ... ok
test experience::tests::experience_ordinary_save_and_crystallization_preserve_dirty_work ... ok

test result: ok. 11 passed; 0 failed; 0 ignored; 0 measured; 98 filtered out; finished in 0.39s


```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/prds/memory-experience-becomes-reliable-and-useful/crystallization-keeps-progressing-beside-ordinary-persistence/specs/implementation.md: exit 0

Command SHA-256: 800e8db5a2fd8ca7cfd9e9ec3a393673b1b3b51e7a494be8783fe2563447b30d

```text
passed: writer_epoch_corruption_is_not_ready_or_writable
   Compiling util v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/util)
   Compiling base v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/base)
   Compiling math v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/math)
   Compiling store_core v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/store/core)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 4.30s
     Running unittests src/lib.rs (/tmp/cartridge-memory-stack-baseline-target/debug/deps/store_core-0092ab9c0269b990)

running 1 test
test tests::writer_epoch_corruption_is_not_ready_or_writable ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 76 filtered out; finished in 0.05s


```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/prds/memory-experience-becomes-reliable-and-useful/crystallization-keeps-progressing-beside-ordinary-persistence/specs/implementation.md: exit 0

Command SHA-256: 99bad454e73d1f63e0c8d5a132b76f3f13a5096b0dc8e324c9ecb20830198a43

```text
passed: reconcile_if_stale_preserves_ram_when_the_store_advanced
   Compiling hub v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/hub)
   Compiling rpc v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/rpc)
   Compiling commands v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/commands)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 3.30s
     Running unittests src/lib.rs (/tmp/cartridge-memory-stack-baseline-target/debug/deps/commands-8c9813afb1aa9a91)

running 1 test
test commands_serve::entry_point_tests::reconcile_if_stale_preserves_ram_when_the_store_advanced ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 129 filtered out; finished in 0.06s


```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/prds/memory-experience-becomes-reliable-and-useful/crystallization-keeps-progressing-beside-ordinary-persistence/specs/implementation.md: exit 0

Command SHA-256: a42d7e060616df8fe181a603ae8db20509a52b997b48316afaaf0e9e77d5afb9

```text
    Checking util v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/util)
    Checking audit v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/hotreload/audit)
    Checking memory_transport v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/transport)
    Checking hotreload v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/hotreload)
    Checking base v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/base)
    Checking llm v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/llm)
    Checking ingest_config v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/ingest/config)
    Checking math v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/math)
    Checking config v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/config)
    Checking store_core v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/store/core)
    Checking graph v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/graph)
    Checking gnn v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/gnn)
    Checking identity v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/identity)
    Checking retrieval-piece v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/retrieval/piece)
    Checking tick v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/tick)
    Checking ingest v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/ingest)
    Checking bootstrap v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/bootstrap)
    Checking retrieval v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/retrieval)
    Checking tick_loop v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/tick/loop)
    Checking store v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/store)
    Checking health v0.1.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/health)
    Checking rpc v2.0.0 (/private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-YRqRP9/source/src/rpc)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 4.13s

```
