---
commit: 5097a83cc0cece79bc4b0f804819a718a7bc976d
spec-digests: {"spec01.md":"dc35168f44b6ba8ea03020913372a19505fc2c269cacd50f9cafccdd9557fe7c"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memory/prds/diskann-builds-keep-every-node-reachable-from-the-entry-point/specs/spec01.md: exit 0

Command SHA-256: 83619cff28dabbdd690efad961068a305f87b94d7ba6abeaa8eb33cccc72f50d

```text
   Compiling graph v2.0.0 (/Users/feb/dev/cartridge/memory.ctg/src/graph)
    Finished `release` profile [optimized] target(s) in 4.81s
     Running unittests src/lib.rs (target/release/deps/graph-d28fc7ea6a4d8cbc)

running 15 tests
test diskann::diskann_tests::tests::diskann_clustered_10k_measure ... ignored, measurement: 10k clustered build, run with --release --ignored --nocapture
test diskann::diskann_tests::tests::no_neighbour_list_outgrows_r_and_a_lone_item_gets_none ... ok
test diskann::diskann_tests::tests::corrupt_index_is_rejected ... ok
test diskann::diskann_tests::tests::out_of_range_neighbor_is_rejected ... ok
test diskann::diskann_tests::tests::corrupt_meta_is_rejected ... ok
test diskann::diskann_tests::tests::search_hits_filtered_returns_cosine_similarity_nearest_first ... ok
test diskann::diskann_tests::tests::rebuild_over_an_existing_index_swaps_and_leaves_no_staging ... ok
test diskann::diskann_tests::tests::empty_and_single ... ok
test diskann::diskann_tests::tests::build_open_search_roundtrip ... ok
test diskann::diskann_tests::tests::truncated_graph_is_rejected ... ok
test diskann::diskann_tests::tests::search_hits_filtered_returns_only_matching_and_is_a_subset ... ok
test diskann::diskann_tests::tests::recall_at_10_is_high_vs_brute_force ... ok
test diskann::diskann_tests::tests::the_same_corpus_builds_a_byte_identical_index ... ok
test diskann::diskann_tests::tests::diskann_build_reaches_every_node_on_clustered_corpus ... ok
test diskann::diskann_tests::tests::diskann_recall_on_clustered_corpus ... ok

test result: ok. 14 passed; 0 failed; 1 ignored; 0 measured; 164 filtered out; finished in 9.28s


```
