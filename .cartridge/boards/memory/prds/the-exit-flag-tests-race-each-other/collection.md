---
commit: a124fd30d59bcd06062b5464810188a0288e461e
spec-digests: {"spec01.md":"a2d6005ecf97de0e6a22197db86fc773e7427a7727afc0eb7a01676c502560d8"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/prds/the-exit-flag-tests-race-each-other/specs/spec01.md: exit 0

Command SHA-256: da8d1c97c3ab894a30569244a26d9fd818dfce9af77b32d8b4fadbd5b806043c

```text
    Finished `test` profile [unoptimized] target(s) in 0.11s
     Running ../../.cartridge/tests/unit/src/commands/tests/exit_status.rs (target/prd-writer-boundary/debug/deps/exit_status-daef9b000cdee1f6)

running 1 test
test a_reported_failure_is_what_the_exit_status_reads ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Compiling store_core v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/store/core)
    Finished `test` profile [unoptimized] target(s) in 0.95s
     Running unittests src/lib.rs (target/prd-writer-boundary/debug/deps/store_core-bdfdd87cbf601c3d)

running 1 test
test lock::lock_tests::inherited_description_requires_the_bounded_retry ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 77 filtered out; finished in 0.00s

    Finished `test` profile [unoptimized] target(s) in 0.12s
     Running unittests src/lib.rs (target/prd-writer-boundary/debug/deps/commands-d1c3310006141ba4)

running 1 test
test commands_serve::watchdog_handover_tests::a_handover_with_no_listener_frees_the_store_and_returns ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 129 filtered out; finished in 0.00s


```
