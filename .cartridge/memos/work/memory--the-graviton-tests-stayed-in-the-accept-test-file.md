---
kind: work
level: 10
status: done
estimate: 1h
actual: 1h
description: fourteen of accept_test.rs's thirty-eight tests exercise the focus functions and nothing else, and the helper obstacle that held them there is gone — `ent` comes from `test_support` now and `focus_names` is focus-specific and moves with them
read_when: "picking up work, or adding a focus test"
---

# the-graviton-tests-stayed-in-the-accept-test-file

## Do

`src/graph/src/tests/accept_test.rs` keeps fourteen tests that exercise the
focus functions and nothing else. Re-read 2026-09-08, under the names the
2026-09-07 rename gave them ([[focus-grammar]]): `focus_names`,
`add_focus_creates_named_root_child`, `remove_focus_demotes_and_reports`, the
two `promote_skips_when_root_*`, the three `seed_examples_*`,
`mean_pool_normalizes_and_rejects_mismatched_dims`, the two
`promote_unnamed_*`, `add_focus_with_mass_round_trips_and_updates_in_place`,
`add_focus_updates_existing_same_name_instead_of_minting_duplicate` and
`promotes_generic_child_to_root`.

Move them to `src/graph/src/tests/focus_test.rs`. **The obstacle this memo was
written around is gone.** It named the helpers — "`ent` and its siblings are
defined inside accept_test's own `mod tests`, so either they move to a place
both files read or the split copies them". `ent` is now
`test_support::entity_vec` (`accept_test.rs:9`), a dev-dependency both files
can import (`src/graph/Cargo.toml:25`), and `alloc_probe` comes from the same
crate. The one helper still local is `focus_names` (`:808`), which only the
fourteen use, so it moves with them rather than needing a shared home. Nothing
is copied.

The functions themselves are no longer a module of their own: `add_focus`,
`remove_focus` and `focus_rows` live in `src/graph/src/graph_ops.rs` and
`src/graph/src/accept.rs`, reached through `use super::*`, so the new file
needs no import the old one did not have.

Two tests stay behind on purpose: `heavier_focus_wins_at_equal_distance`
(`:925`) and `default_mass_preserves_nearest_focus_routing` (`:940`) only build
a focus as setup and assert on routing, which is the write path's job.

This is the test half of [[the-graviton-api-was-filed-under-the-write-path]].

## Check

`rg -c 'fn (add_focus|remove_focus|focus_names|promote_unnamed|seed_examples|mean_pool)' src/graph/src/tests/accept_test.rs`
returns nothing, `src/graph/src/tests/focus_test.rs` holds the fourteen plus
`focus_names`, `rg -n 'fn heavier_focus|fn default_mass' src/graph/src/tests/accept_test.rs`
still names the two routing tests, and `cargo test -p graph` is green with the
same total test count.

Done 2026-09-08: the thirteen focus tests and `focus_names` moved to
`src/graph/src/tests/focus_test.rs`, declared beside `accept_tests` in
`src/graph/src/accept.rs`; `cargo test -p graph` green, 173 tests, 38 in
accept_test before = 25 after + 13.
