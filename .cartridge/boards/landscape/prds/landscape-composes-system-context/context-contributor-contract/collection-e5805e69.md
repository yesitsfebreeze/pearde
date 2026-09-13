---
commit: e5805e6960844af42a32dbc37833304c8208459b
spec-digests: {"spec01.md":"52de38841036f33f4abd377cbcddea7b8f1df5251bc8eda60a9eb368afdfaab3"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/landscape/prds/landscape-composes-system-context/context-contributor-contract/specs/spec01.md: exit 0

Command SHA-256: e6c3734889235d192ec325c56d5652220f6e0db5a7cf75045ab614be27cab874

```text
    Finished `test` profile [unoptimized] target(s) in 0.07s
     Running unittests src/lib.rs (target/tool-result-contract/debug/deps/landscape-790bf2959c895d43)

running 24 tests
test context::tests::duplicate_tasks_and_invalid_limits_fail_before_any_producer ... ok
test surface::tests::cartridge_nodes_carry_their_capability_keys ... ok
test context::tests::late_ready_contribution_cannot_publish_after_deadline ... ok
test context::tests::dropping_collector_drops_pending_producers_without_spawning_work ... ok
test context::tests::availability_is_explicit_and_disabled_producers_never_poll ... ok
test surface::tests::compose_skips_malformed_surface_entries ... ok
test context::tests::hanging_first_source_does_not_starve_siblings_and_is_dropped ... ok
test surface::tests::tool_nodes_carry_the_describe_description ... ok
test surface::tests::memo_nodes_carry_their_kind_and_declared_usage_phrases ... ok
test context::tests::producer_capacity_omissions_remain_explicit_in_prepared_snapshot ... ok
test tests::edges_connect_present_nodes_and_tolerate_ones_to_come ... ok
test tests::journal_counts_weight_stages ... ok
test context::tests::private_content_cannot_change_public_digest_or_capacity ... ok
test tests::graph_search_keeps_the_seed_ranking ... ok
test tests::upsert_grows_the_node_set_in_place ... ok
test tests::observed_use_outranks_equal_match ... ok
test surface::tests::composed_memo_links_respect_cartridge_namespaces ... ok
test tests::search_returns_kinds_with_descriptions ... ok
test context::tests::canonical_order_exact_readback_and_conflicting_sources ... ok
test surface::tests::compose_grows_the_live_surface_and_counts_observations ... ok
test context::tests::exact_serialized_bounds_count_metadata_and_keep_whole_utf8_rows ... ok
test view_tests::cursor_from_another_snapshot_is_stale ... ok
test view_tests::tracked_files_follow_sibling_repository_links ... ok
test view_tests::tracked_files_join_by_scope_and_page_by_id ... ok

test result: ok. 24 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.05s

    Finished `dev` profile [unoptimized] target(s) in 0.06s

```
