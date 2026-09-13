---

kind: work
level: 10
status: done
description: "`[gnn] min_weight` is the floor of an edge weighting the graph does not implement — `Edge` carries only source and target, `add_edge` takes no weight, and the module doc that promises weighted edges is the third artefact of the same unbuilt design"
read_when: "picking up work, or reading the GNN's config"
---

# the-gnn-edge-weight-floor-has-no-edge-weights

## Do

`min_weight` is declared in `config::GnnConfig` (`src/config/src/config.rs:595`,
default `DEFAULT_MIN_WEIGHT = 0.01` at `:604`), declared again in
`gnn::GnnConfig` (`src/gnn/src/gnn_propagate.rs:28`), and copied from one to the
other at `:217`. Nothing computes with it. Those five lines plus two test
assertions are every mention in the tree.

The name says what it was for. `gnn_graph.rs`'s module doc opens "The
training-side graph view: nodes with feature vectors, weighted edges" — and
`Edge` holds `source` and `target` and nothing else (`:61-64`), `add_edge`
(`:54`) takes two ids and no weight, and the word `weight` appears nowhere else
in the file. There is no weighting for a floor to apply to.

Delete `min_weight` from both configs, its two defaults and the copy, drop the
two assertions in `gnn_propagate_test.rs:151-169`, and correct the module doc
to describe the `Edge` that exists. This is the second dead config key of the
night — `[graph] max_ledger_entries` was the first
([[@prd/work/memory--the-graph-ledger-bound-lost-its-ledger.md]]) — and `[gnn]`, like `[graph]`,
carries no allow-list, so an operator setting it gets no complaint
([[config-rejects-unknown-keys]] covers only the three preset-managed
sections).

Two things kept it alive. Its test asserts that the value survives the copy
from one struct to the other, so the field has coverage that proves only that
it is copied — and the shape of that test is why nobody could see the
difference. `from_maps_every_field_without_drift`
(`src/gnn/src/tests/gnn_propagate_test.rs`, deleted with the two-struct
`From` at `a807a1f0`) set all five fields and
asserts all five round-trip:

```
self_weight: 0.11,   assert_eq!(runtime.self_weight, 0.11);
min_weight:  0.22,   assert_eq!(runtime.min_weight, 0.22);
```

`self_weight` drives the blend at `gnn_propagate.rs:140` and `min_weight`
drives nothing, and those two adjacent lines are indistinguishable, because a
round-trip test never touches what a field *does*. Every field in a config
struct looks equally alive to it. And it survived a sweep built to catch exactly this: the field
census in [[@prd/work/memory--the-gcounter-accessor-has-no-caller.md]] listed `min_weight` among the
seven candidates at one reference, and five others were opened and cleared
while this one was assumed live.

**Done 2026-09-06.** `min_weight` is gone from both config structs, both
defaults, the copy between them and the three test assertions; `rg` over `src`
and `tests` finds it only in the doc line that records its removal. The second
dead config key of the night after `[graph] max_ledger_entries`, and the same
shape: a key whose subsystem was never built rather than one whose subsystem was
deleted ([[@prd/work/memory--the-graph-ledger-bound-lost-its-ledger.md]] is the deletion case).

`gnn_graph.rs`'s module doc now says "unweighted edges" and names what was
removed, rather than quietly dropping the word — an edit that adds, so a reader
meeting `Edge { source, target }` learns the weighting was promised and never
existed instead of wondering whether it was lost.

The observation about the round-trip test is the part worth keeping and it
generalises past this key: `from_maps_every_field_without_drift` sets five
fields and asserts five round-trips, and `self_weight` — which drives the blend
at `gnn_propagate.rs:140` — and `min_weight` — which drove nothing — are
adjacent, identical lines. **A round-trip test cannot distinguish a live field
from a dead one, because it never touches what a field does.** Every field in a
config struct looks equally covered to it. That is why the key survived a census
built to find exactly this: it was listed among the candidates at one reference
and assumed live while five others were opened and cleared.

## Check

`rg min_weight` finds nothing outside `target/`, `gnn_graph.rs`'s module doc
describes an unweighted edge, and `just check` and `just test` are green. All
hold — the single remaining hit is the doc line naming the deletion; suite 1,255
passed.
