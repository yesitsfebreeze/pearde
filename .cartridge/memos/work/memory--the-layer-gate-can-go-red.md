---

kind: work
level: 10
status: done
description: "`layer_headers` is the last rule gate with no proof it can fail — extract a `check(root)` seam and pin a fixture that violates the layer contract"
read_when: "trusting the layer contract"
---

# the-layer-gate-can-go-red

## Do

Every other rule gate demonstrates its own failure against a fixture:
`one_dispatch`, `memos_index`, `declared_dependencies`, `cited_paths`,
`orphan_modules`, `wire_tolerant_decode`, and — since `cfec6b07` — `vocabulary`
and `tracked_artifacts`. `layer_headers` does not. Its second test,
`the_header_parser_reads_a_wrapped_line_and_reads_nothing_as_nothing`, proves
the *parser*; nothing proves the gate, so nothing shows that a crate importing
above its declared layer would actually fail it.

The obstacle is shape, not difficulty. `every_layer_line_names_its_imports_and_nothing_above_it`
is a ninety-line body that walks `crates(&root)`, reads each `lib.rs` header and
each manifest, and accumulates a `violations` vec inline. Extract
`check(root) -> Result<(), String>` the way the others carry it, leaving the
live test as the two lines that call it against `CARGO_MANIFEST_DIR`.

Then a fixture, and it needs three cases because the gate makes three distinct
claims: a crate whose header omits a dependency it declares, a crate importing
one above its own layer, and a crate with no `//! Layer:` line that is not named
in `COMPOSING`. A red-proof covering only the first would leave the other two in
the state this item exists to end.

## Check

`cargo test --test layer_headers` runs a `the_gate_can_go_red` that fails the
check on each of the three violations and passes a clean fixture, and the live
test is a call into the same `check`.

Done 2026-09-06. `inversions` became a parameter rather than a read of the
const: the stale-entry sweep names crates literally, so against a fixture tree
every real entry reads as stale and a const there fails any fixture for the
wrong reason. The proof covers a fourth case the item did not ask for — both
directions of the INVERSIONS hatch, which the gate offers in its own failure
message and nothing showed was real.
