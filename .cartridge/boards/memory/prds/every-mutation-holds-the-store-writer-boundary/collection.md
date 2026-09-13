---
commit: 0a8736c5126781b90b842a5b818f083458b2f740
spec-digests: {"spec01.md":"424cab22073f7164087e58b87db6c010e07847093954847995e650e457a8a7d8"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/prds/every-mutation-holds-the-store-writer-boundary/specs/spec01.md: exit 0

Command SHA-256: 7583798968d37cbd60993dc594beb9d74980a4775696834e7f35978ac824f66d

```text
   Compiling config v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/config)
   Compiling transport v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/transport)
   Compiling store_core v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/store/core)
   Compiling gnn v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/gnn)
   Compiling identity v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/identity)
   Compiling hub v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/hub)
   Compiling graph v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/graph)
   Compiling retrieval-piece v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/retrieval/piece)
   Compiling tick v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/tick)
   Compiling ingest v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/ingest)
   Compiling bootstrap v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/bootstrap)
   Compiling retrieval v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/retrieval)
   Compiling tick_loop v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/tick/loop)
   Compiling store v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/store)
   Compiling health v0.1.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/health)
   Compiling rpc v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/rpc)
   Compiling commands v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/commands)
    Finished `test` profile [unoptimized] target(s) in 5.80s
     Running unittests src/lib.rs (/Users/feb/dev/cartridge/memory.ctg/target/prd-writer-boundary/debug/deps/commands-2670e4508d800227)

running 15 tests
test commands_hub::writer_boundary_tests::writer_boundary_configured_clean_child ... ok
test writer_boundary_tests::writer_boundary_child ... ok
memory ingest: unknown operation: operator_ingest
test commands_serve::entry_point_tests::writer_boundary_stale_flush_preserves_disk_and_unflushed_ram ... ok
test commands_compress::writer_boundary_tests::writer_boundary_compress_reservation_race_publishes_once ... ok
test commands_queue_cmd::commands_queue_cmd_tests::writer_boundary_refused_drain_cannot_archive_queue_bytes ... ok
test commands_hub::writer_boundary_tests::writer_boundary_clean_retains_the_owned_inode_and_symlink_targets ... ok
test writer_boundary_tests::writer_boundary_stale_snapshot_cannot_resurrect_after_owner_crash ... ok
test commands_compress::writer_boundary_tests::writer_boundary_compress_refuses_claims_and_preserves_existing_targets ... ok
test writer_boundary_tests::writer_boundary_killed_process_releases_claim ... ok
memory ingest: invalid daemon outcome: missing field `status`; operation outcome may be unknown; not replayed
test commands_graph_ops::commands_graph_ops_tests::writer_boundary_link_does_not_reintroduce_deleted_endpoints ... ok
test commands_hub::writer_boundary_tests::writer_boundary_configured_clean_protects_ancestors_equal_nested_and_external_links ... ok
memory forget: another memory writer holds this data dir (owner pid 23600)
test writer_boundary_tests::writer_boundary_two_process_barrier_has_one_commit_and_unchanged_loser_bytes ... ok
memory ingest: operation operator_ingest failed on the daemon for root /Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/commands at /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/memory-op-e276a471-a1b9-45ea-b2a5-3eeb8f081041.sock: rpc adapter: eof; operation outcome may be unknown; not replayed
memory audit: another memory writer holds this data dir (owner pid 23600)
test commands_hub::writer_boundary_tests::writer_boundary_pair_claims_both_stores_and_refuses_each_holder_or_alias ... ok
memory repair: another memory writer holds this data dir (owner pid 23600)
test commands_ingest_cmd::operator_tests::writer_boundary_operator_refused_malformed_and_lost_replies_never_replay_offline ... ok
memory clean: another memory writer holds this data dir (owner pid 23600)
memory ingest: another memory writer holds this data dir (owner pid 23600)
memory link: another memory writer holds this data dir (owner pid 23600)
test writer_boundary_tests::writer_boundary_direct_entries_refuse_before_mutation_and_reads_work ... ok

test result: ok. 15 passed; 0 failed; 0 ignored; 0 measured; 110 filtered out; finished in 0.86s

     Running ../../.cartridge/tests/unit/src/commands/tests/exit_status.rs (/Users/feb/dev/cartridge/memory.ctg/target/prd-writer-boundary/debug/deps/exit_status-4d5bd56d5ffed1a4)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 1 filtered out; finished in 0.00s


```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/prds/every-mutation-holds-the-store-writer-boundary/specs/spec01.md: exit 0

Command SHA-256: de94232fc4f64d9eddd9067f374d6cbc2427b68cf0c12e299d9d04c19068cfb5

```text

   Doc-tests tick_loop

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests transport

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests transport_macros

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests util

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

5628059831893107562bae65e90c34891d3eb23b66404183913df43279b3b351  /tmp/memory-writer-full.ZbZccY

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/prds/every-mutation-holds-the-store-writer-boundary/specs/spec01.md: exit 0

Command SHA-256: 094d2a92b89aeaaff56f8650c4d1b7aaed048513eb47cc2c380119a065b13bb6

```text
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
    Checking config v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/config)
    Checking store_core v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/store/core)
    Checking transport v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/transport)
    Checking gnn v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/gnn)
    Checking identity v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/identity)
    Checking hub v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/hub)
    Checking graph v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/graph)
    Checking retrieval-piece v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/retrieval/piece)
    Checking tick v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/tick)
    Checking ingest v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/ingest)
    Checking bootstrap v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/bootstrap)
    Checking retrieval v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/retrieval)
    Checking tick_loop v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/tick/loop)
    Checking store v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/store)
    Checking memory-bench v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/.cartridge/tests/integration/bench)
    Checking health v0.1.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/health)
    Checking rpc v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/rpc)
    Checking commands v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary/src/commands)
    Checking memory v2.0.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/.lanes/every-mutation-holds-the-store-writer-boundary)
    Finished `dev` profile [unoptimized] target(s) in 4.16s

```
