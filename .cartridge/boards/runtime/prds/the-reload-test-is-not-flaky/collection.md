---
commit: bd3b5e78d6e3ddd7dc7567b0c357d6fe60bd02df
spec-digests: {"spec01.md":"d94b88a3fd3b6badc48e5a2962fcecfdd2c36bde8512bc4da409b0770e8d7f20"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/runtime/prds/the-reload-test-is-not-flaky/specs/spec01.md: exit 0

Command SHA-256: 8635d37de02d89a92c0f29ec8095a35d3b4f5bbbfcf7bbd883d183d4de363b37

```text
   Compiling cartridge v0.1.0 (/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/runtime/.lanes/the-reload-test-is-not-flaky)
    Finished `test` profile [unoptimized] target(s) in 5.05s
     Running unittests src/lib.rs (/Users/feb/dev/cartridge/cartridge.ctg/target/tool-result-contract/debug/deps/cartridge-41093d4bbf807d0f)

running 8 tests
test sdk::tests::reload_registration_dispatches_boolean_values_for_prepare_and_cancel ... ok
test tests::reload::an_uncomposed_node_and_an_unknown_uid_refuse_the_ask ... ok
test tests::reload::corrected_code_can_recover_a_failed_initial_generation ... ok
test tests::reload::two_entries_of_one_file_each_get_their_own_switch ... ok
test tests::reload::switching_keeps_consumers_bound_and_rejects_bad_migrations ... ok
test tests::reload::a_composed_handle_reloads_its_node_again_after_the_first_swap ... ok
test tests::reload::an_ask_at_a_retired_uid_is_refused_and_the_node_still_reloads ... ok
test tests::reload::a_nested_node_is_swapped_and_its_dependent_follows ... ok

test result: ok. 8 passed; 0 failed; 0 ignored; 0 measured; 157 filtered out; finished in 0.07s

     Running unittests src/main.rs (/Users/feb/dev/cartridge/cartridge.ctg/target/tool-result-contract/debug/deps/cartridge-bfe1ba4daa6e9908)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 2 filtered out; finished in 0.00s

     Running unittests .cartridge/tests/unit/src/tests/fixtures/chain_fixture.rs (/Users/feb/dev/cartridge/cartridge.ctg/target/tool-result-contract/debug/examples/chain_fixture-352252d61bd6755b)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests .cartridge/tests/unit/src/tests/fixtures/lua_fixture.rs (/Users/feb/dev/cartridge/cartridge.ctg/target/tool-result-contract/debug/examples/lua_fixture-e8ce3e540cfc5bdc)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests .cartridge/tests/unit/src/tests/fixtures/nested_fixture.rs (/Users/feb/dev/cartridge/cartridge.ctg/target/tool-result-contract/debug/examples/nested_fixture-edd2fe45942c6858)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests .cartridge/tests/unit/src/tests/fixtures/rpc_fixture.rs (/Users/feb/dev/cartridge/cartridge.ctg/target/tool-result-contract/debug/examples/rpc_fixture-8e172d8aaafa386c)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

    Finished `test` profile [unoptimized] target(s) in 0.09s
     Running unittests src/lib.rs (/Users/feb/dev/cartridge/cartridge.ctg/target/tool-result-contract/debug/deps/cartridge-41093d4bbf807d0f)
20 unchanged-binary reload regression runs passed

```
