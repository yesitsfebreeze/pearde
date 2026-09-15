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

# replace `gini_over_access`'s N² double loop with the sorted closed form, so the health surface stops costing 100 million comparisons and 51 seconds on a 10k-entity store

## Do

`gini_over_access` (`src/health/src/lib.rs`, the `for i in 0..n { for j in 0..n }`
double sum) is `N²` in resident entities and runs inside whatever process serves
health ([[health-is-quadratic-in-entity-count]]). Replace the body with the
standard equivalent, which needs one sort and one pass:

```
counts.sort_unstable();
let sum: u64 = counts.iter().sum();
if n == 0 || sum == 0 { return 0.0; }
let weighted: u128 = counts.iter().enumerate()
    .map(|(i, &c)| (i as u128 + 1) * c as u128).sum();
(2.0 * weighted as f64) / (n as f64 * sum as f64) - (n as f64 + 1.0) / n as f64
```

Take the slice by value or clone it — the caller builds `access_counts` fresh at
`graph_health_stats` and nothing else holds it. `gini_over_memory_sizes` is a
one-line wrapper and needs no change; it is the same code at n = 36 and was
never the cost.

Keep the `u128` accumulator. `weighted` is bounded by `n · n · max(count)`, which
overflows `u64` well before the double sum would.

**Done 2026-09-06 — and the `Do`'s diagnosis was wrong, which the fix does not
depend on.** The closed form is in, `gini_over_access` is one sort and one pass,
and the pairwise implementation moved into the tests as the equivalence proof.

But gini was never the 51.3 seconds. Measured on this store before writing the
part up:

```
memory status  0.008s   no graph load
memory list   53.08s    loads the graph, never calls gini
memory health 54.02s    loads the graph, calls gini
```

`list` does not touch `gini_over_access` and pays 53 s regardless: the cost is
the **graph load**. Health is `list` plus 0.94 s, and that 0.94 covers every
stat it computes rather than gini alone. The old loop was not free either — the
retained pairwise form runs 1,000 elements, 1 M iterations, inside a test that
completes in 0.035 s, so 10,038 resident thoughts is 100.8 M iterations and
roughly **3 s** by extrapolation from that measurement. Worth removing, and an
order of magnitude short of what it was blamed for.

51.3 s was measured on `memory health` and attributed to the only quadratic in
sight. [[health-is-quadratic-in-entity-count]] made that attribution and has
been corrected to carry the ~3 s figure and the control that refutes it. What is actually there — every CLI invocation that
loads this store paying ~53 s, against a `config.rs` comment still citing "the
~4.5 s per-CLI-invocation HNSW rebuild" — is a separate finding and not this
item's.

## Acceptance
`gini_over_access_pins_known_distributions` (already in
`src/health/src/lib.rs`) passes unchanged — it pins the empty, uniform,
zero-sum, `[10,0,0] -> 2/3` and `[100,0] -> 1/2` cases, which is the equivalence
proof, and a new case over a random 1,000-element vector agrees with the old
double loop to `1e-12`. The equivalence half holds:
`gini_over_access_pins_known_distributions` passes untouched and
`the_sorted_form_agrees_with_the_pairwise_one_it_replaced` agrees to 1e-12 over
a seeded 1,000-value spread, and again with the input reversed — the sorted form
being the one that could care about order. Suite 1,243 passed.

**The timing half is unreachable and no change to gini could reach it.**
`time memory health` is 54.02 s because the graph load is, as above. A Check can
name a number the item it belongs to has no way to move.
