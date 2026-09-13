---
commit: 439bea56749d6a7361d6c1afb7d1a43bb46c7e9f
spec-digests: {"spec01.md":"75d70b01714f4cbe5b223c2ba9d84fb1c48cd6b295860d8f2dee7abeb22768a1"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/prds/every-mutation-holds-the-store-writer-boundary/specs/spec01.md: exit 0

Command SHA-256: 7583798968d37cbd60993dc594beb9d74980a4775696834e7f35978ac824f66d

```text
   Compiling store_core v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/store/core)
   Compiling graph v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/graph)
   Compiling retrieval-piece v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/retrieval/piece)
   Compiling ingest v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/ingest)
   Compiling tick v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/tick)
   Compiling bootstrap v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/bootstrap)
   Compiling retrieval v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/retrieval)
   Compiling tick_loop v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/tick/loop)
   Compiling store v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/store)
   Compiling health v0.1.0 (/Users/feb/dev/cartridge/memory.ctg/src/health)
   Compiling rpc v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/rpc)
   Compiling commands v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/commands)
    Finished `test` profile [unoptimized] target(s) in 4.12s
     Running unittests src/lib.rs (target/prd-writer-boundary/debug/deps/commands-0b246b2b6a4d9b46)

running 15 tests
test commands_hub::writer_boundary_tests::writer_boundary_configured_clean_child ... ok
test writer_boundary_tests::writer_boundary_child ... ok
memory ingest: unknown operation: operator_ingest
test commands_serve::entry_point_tests::writer_boundary_stale_flush_preserves_disk_and_unflushed_ram ... ok
test commands_compress::writer_boundary_tests::writer_boundary_compress_reservation_race_publishes_once ... ok
test commands_queue_cmd::commands_queue_cmd_tests::writer_boundary_refused_drain_cannot_archive_queue_bytes ... ok
test commands_hub::writer_boundary_tests::writer_boundary_clean_retains_the_owned_inode_and_symlink_targets ... ok
test writer_boundary_tests::writer_boundary_stale_snapshot_cannot_resurrect_after_owner_crash ... ok
memory ingest: invalid daemon outcome: missing field `status`; operation outcome may be unknown; not replayed
test commands_hub::writer_boundary_tests::writer_boundary_configured_clean_protects_ancestors_equal_nested_and_external_links ... ok
test commands_graph_ops::commands_graph_ops_tests::writer_boundary_link_does_not_reintroduce_deleted_endpoints ... ok
test commands_compress::writer_boundary_tests::writer_boundary_compress_refuses_claims_and_preserves_existing_targets ... ok
test writer_boundary_tests::writer_boundary_killed_process_releases_claim ... ok
test writer_boundary_tests::writer_boundary_two_process_barrier_has_one_commit_and_unchanged_loser_bytes ... ok
memory forget: another memory writer holds this data dir (owner pid 43529)
memory ingest: operation operator_ingest failed on the daemon for root /Users/feb/dev/cartridge/memory.ctg/src/commands at /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/memory-op-4693b3e6-1bf9-484a-b8b4-9367e13af17e.sock: rpc adapter: eof; operation outcome may be unknown; not replayed
memory audit: another memory writer holds this data dir (owner pid 43529)
test commands_hub::writer_boundary_tests::writer_boundary_pair_claims_both_stores_and_refuses_each_holder_or_alias ... ok
test commands_ingest_cmd::operator_tests::writer_boundary_operator_refused_malformed_and_lost_replies_never_replay_offline ... ok
memory repair: another memory writer holds this data dir (owner pid 43529)
memory clean: another memory writer holds this data dir (owner pid 43529)
memory ingest: another memory writer holds this data dir (owner pid 43529)
memory link: another memory writer holds this data dir (owner pid 43529)
test writer_boundary_tests::writer_boundary_direct_entries_refuse_before_mutation_and_reads_work ... ok

test result: ok. 15 passed; 0 failed; 0 ignored; 0 measured; 115 filtered out; finished in 0.89s

     Running ../../.cartridge/tests/unit/src/commands/tests/exit_status.rs (target/prd-writer-boundary/debug/deps/exit_status-b2a44cc2997c160d)

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

787d6a4b9ddd149656ea3746a8f0e3a8980b2181405ca869dabba8b4c8bbbaf4  /tmp/memory-writer-full.MJ2JyL

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/prds/every-mutation-holds-the-store-writer-boundary/specs/spec01.md: exit 0

Command SHA-256: 094d2a92b89aeaaff56f8650c4d1b7aaed048513eb47cc2c380119a065b13bb6

```text
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
    Checking store_core v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/store/core)
    Checking cartridge v0.1.0 (/Users/feb/dev/cartridge/cartridge.ctg)
    Checking graph v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/graph)
    Checking retrieval-piece v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/retrieval/piece)
    Checking ingest v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/ingest)
    Checking tick v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/tick)
    Checking bootstrap v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/bootstrap)
    Checking retrieval v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/retrieval)
    Checking tick_loop v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/tick/loop)
    Checking store v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/store)
    Checking memory-bench v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/.cartridge/tests/integration/bench)
    Checking health v0.1.0 (/Users/feb/dev/cartridge/memory.ctg/src/health)
    Checking rpc v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/rpc)
    Checking commands v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/commands)
    Checking memory v2.0.0 (/Users/feb/dev/cartridge/memory.ctg)
    Finished `dev` profile [unoptimized] target(s) in 3.07s

```
