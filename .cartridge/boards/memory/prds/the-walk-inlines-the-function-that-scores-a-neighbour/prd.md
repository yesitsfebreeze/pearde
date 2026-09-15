---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# `score_neighbor` is the extracted form of the four lines the walk computes inline, has no production caller, and cannot be adopted — the walk needs `edge_evidence` separately for traversal credit before the score exists

## Do

Two spellings of one formula in one file.

`expand`'s walk (`src/retrieval/src/retrieval_expand.rs:295`, `:317-322`):

```
let evidence = edge_evidence(query_vec, reason, w, refine_tw, refine_cap);
...
let content_score = if neighbor.has_vector() { cosine(query_vec, &neighbor.vector) } else { 0.0 };
let score = w.content * content_score + evidence;
```

`score_neighbor` (`:385-404`) is the same thing as a function: the identical
`content_score` branch, then `w.content * content_score + edge_evidence(...)`.
It is `pub`, and nothing outside its own tests calls it.

Adopting it is not the fix. The walk uses `evidence` on its own two statements
earlier, for the traversal credit — `credit_weight * item.score * evidence`
(`:304`) — so calling `score_neighbor` would compute `edge_evidence` twice per
neighbour on the hot path. The extraction does not fit the one caller it was
extracted from, which is why it was never used. Delete it; `edge_evidence`
stays, with its two real callers.

They agree today and nothing holds them to that — the same exposure
`tests/removal_policy.rs` was built for after one predicate was written five
times and drifted into three answers.

Found by re-running the caller sweep from [the-gcounter-accessor-has-no-caller](../the-gcounter-accessor-has-no-caller/prd.md)
with its two blind spots closed: excluding `src/<crate>/src/tests/` from the
caller count, which this repo uses for unit tests and the first run counted as
production. That turns one candidate into twelve — three of them legitimate
(`test_support` exists to be called by tests), one a test helper misplaced in
`util` (`shutting_down_for_tests_blocking`), and eight production functions with
no production caller: this one, `build_entity_disk_index`, `l2_normalize`,
`link_prediction_loss`, `percentile_sorted`, `structure_digest`, `sum_all` and
`to_dense`.

**Done 2026-09-06 — and not by deleting it.** The `Do` above is right that
`score_neighbor` as written could not be adopted: the walk computes
`edge_evidence` two statements earlier for the traversal credit, so calling it
would have run `edge_evidence` twice per neighbour on the hot path. That is a
reason to change the signature, not to delete the function.

`score_neighbor(query_vec, neighbor, evidence, w)` takes the evidence rather
than recomputing it, and the walk calls it where the formula sat inline. One
production caller, no double computation, and the duplicate spelling gone —
which was this part's actual complaint. Deleting would have removed the
duplication by removing one copy **and** the only tests covering the formula the
surviving copy still computes.

Two parts disagreed about this symbol while agreeing on every fact:
[[an-uncalled-function-with-a-test-may-be-the-check]] had just been corrected to
list it under "called only by a test about itself", and this one said delete.
That disagreement is the signal the remedy was in neither.

`w: Weights` is kept although only `w.content` is read. The tighter signature
would place `evidence: f64` next to a weight — two adjacent same-typed
parameters with nothing but position to tell them apart, which is the shape that
produced the claim-kind-as-language-hint bug
([the-language-hint-reaches-nothing](../the-language-hint-reaches-nothing/prd.md)). Three unused fields is cheap against
that.

## Acceptance
`score_neighbor` has one production caller and one spelling of the formula,
`edge_evidence` keeps its callers, and `just check` and `just test` are green —
suite 1,254 passed. The Check as written asked for its deletion; the reason it
was not deleted is above.
