---
commit: a124fd30d59bcd06062b5464810188a0288e461e
spec-digests: {"spec01.md":"a7c27f7e8407e2bdb660e32a5e6022c5091b5e4c7dd4e2189e871f6ba485b9cb"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/prds/every-mutation-holds-the-store-writer-boundary/specs/spec01.md: exit 0

Command SHA-256: 7583798968d37cbd60993dc594beb9d74980a4775696834e7f35978ac824f66d

```text
    Finished `test` profile [unoptimized] target(s) in 0.13s
     Running unittests src/lib.rs (target/prd-writer-boundary/debug/deps/commands-d1c3310006141ba4)

running 15 tests
test commands_hub::writer_boundary_tests::writer_boundary_configured_clean_child ... ok
test writer_boundary_tests::writer_boundary_child ... ok
memory ingest: unknown operation: operator_ingest
test commands_serve::entry_point_tests::writer_boundary_stale_flush_preserves_disk_and_unflushed_ram ... ok
test commands_compress::writer_boundary_tests::writer_boundary_compress_reservation_race_publishes_once ... ok
test commands_hub::writer_boundary_tests::writer_boundary_clean_retains_the_owned_inode_and_symlink_targets ... ok
test commands_queue_cmd::commands_queue_cmd_tests::writer_boundary_refused_drain_cannot_archive_queue_bytes ... ok
test writer_boundary_tests::writer_boundary_stale_snapshot_cannot_resurrect_after_owner_crash ... ok
test commands_hub::writer_boundary_tests::writer_boundary_configured_clean_protects_ancestors_equal_nested_and_external_links ... ok
test commands_graph_ops::commands_graph_ops_tests::writer_boundary_link_does_not_reintroduce_deleted_endpoints ... ok
test commands_compress::writer_boundary_tests::writer_boundary_compress_refuses_claims_and_preserves_existing_targets ... ok
test writer_boundary_tests::writer_boundary_killed_process_releases_claim ... ok
memory ingest: invalid daemon outcome: missing field `status`; operation outcome may be unknown; not replayed
memory forget: another memory writer holds this data dir (owner pid 64872)
test writer_boundary_tests::writer_boundary_two_process_barrier_has_one_commit_and_unchanged_loser_bytes ... ok
memory ingest: operation operator_ingest failed on the daemon for root /Users/feb/dev/cartridge/memory.ctg/src/commands at /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/memory-op-d58c6135-0545-4949-96f6-46dad20c9500.sock: rpc adapter: eof; operation outcome may be unknown; not replayed
memory audit: another memory writer holds this data dir (owner pid 64872)
test commands_hub::writer_boundary_tests::writer_boundary_pair_claims_both_stores_and_refuses_each_holder_or_alias ... ok
memory repair: another memory writer holds this data dir (owner pid 64872)
test commands_ingest_cmd::operator_tests::writer_boundary_operator_refused_malformed_and_lost_replies_never_replay_offline ... ok
memory clean: another memory writer holds this data dir (owner pid 64872)
memory ingest: another memory writer holds this data dir (owner pid 64872)
memory link: another memory writer holds this data dir (owner pid 64872)
test writer_boundary_tests::writer_boundary_direct_entries_refuse_before_mutation_and_reads_work ... ok

test result: ok. 15 passed; 0 failed; 0 ignored; 0 measured; 115 filtered out; finished in 0.86s

     Running ../../.cartridge/tests/unit/src/commands/tests/exit_status.rs (target/prd-writer-boundary/debug/deps/exit_status-daef9b000cdee1f6)

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

618b40fb3ae989c08eb2c99b04fd847246cd1912fd22e999c6d5b9d1ada155a7  /tmp/memory-writer-full.lMfGqp

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/prds/every-mutation-holds-the-store-writer-boundary/specs/spec01.md: exit 0

Command SHA-256: 094d2a92b89aeaaff56f8650c4d1b7aaed048513eb47cc2c380119a065b13bb6

```text
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
    Checking memory v2.0.0 (/Users/feb/dev/cartridge/memory.ctg)
    Finished `dev` profile [unoptimized] target(s) in 0.46s

```
