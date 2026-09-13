---
kind: work
level: 10
status: done
estimate: 1h
actual: 1h
description: give the ignored scale tier one `just scale` recipe — release, `--run-ignored only`, output uncaptured — because the tier's product is a printed table, not a green tick
read_when: "wiring a runner for the ignored tests, or asking why the scale tier is not a CI job"
---

# the-scale-tier-has-a-runner

Done 2026-09-07: `scale filter=''` in `justfile` beside `e2e`. The list
printed 17 on darwin; `just scale gc_sweep_scale` built release, ran the one
test, printed its `victims=` table (N=100000, 100% victims: sweep 3283 ms)
and exited 0 in 17 s. [[hot-reload-and-the-perf-harness-are-memories-own]]
names it the performance harness.

## Do

[[no-runner-runs-the-ignored-tests]] closes on "what is missing is a runner,
not a repair", and its count still holds: 18 `#[ignore]` attributes on
non-comment lines over 7 files, `rg -n 'ignored|--run-ignored' justfile`
matching nothing, `just test` and CI's `cargo nextest run --workspace
--locked` both taking the default `--run-ignored default`. Add the runner as
one recipe in `justfile`, next to `test` and `e2e`:

```
# the ignored scale/measurement tier: minutes to hours in release, run on a
# cadence, never in CI. --no-capture because these print tables and assert no
# ceiling — a green tick from this tier proves only that the instruments still
# reach the code.
scale filter='':
    cargo nextest run --workspace --release --run-ignored only --no-capture {{filter}}
```

Four measurements shape that line and each is why the obvious alternative is
wrong.

**Uncaptured, because nothing here is a gate.** Reading every assert in the
17 tests `cargo nextest list --workspace --run-ignored only` returns on this
darwin machine: not one asserts a cost bound. `route_fanout::fanout` asserts
`slope > 0.02` and says so in its own comment — "guards the instrument, not a
behaviour"; `gc_scale::cold_spill_per_victim_vs_batched` asserts both paths
landed the same row count "or the comparison is meaningless";
`gnn_scale::tick_head_of_line_delay` asserts the probe landed. Nine of the 17
assert nothing at all — `gnn_train_scale`, `other_tick_tasks_scale`,
`gc_sweep_scale`, `cold_search_scale`, `cold_spill_scale`,
`pulse_cost_per_tick`, `depth_is_an_eviction_bias`, `seed_scale::scale`, and
two of the four PageRank measurements, whose reason string already says
"measurement, not an assertion". So a runner that reports pass/fail reports
nothing; `--no-capture` (which nextest also serializes, matching the `e2e`
recipe's reason) is what makes the recipe's output the product.

**Release, because every reason string prices the escape in release** —
"minutes in release" on 14 of the 18, and `spill_memory`'s header calls debug
"effectively unbounded".

**A cadence and not CI.** CI's test job carries `timeout-minutes: 30` and the
tier does not fit: `seed_scale::scale` took 95 minutes by hand while its own
reason string claims 11, an 8.6x gap that means no per-test budget in this
tree can be trusted from its attribute. Only 4 of the 18 have ever been run.
The first full `just scale` therefore has a second job — nextest prints each
test's wall time, so one run produces the cost table nobody has, and only
after that can anyone say which subset a CI cadence could afford. Land the
recipe, run it once, and let the numbers pick the tier.

**A darwin runner must not claim the eighteenth.** `tests/spill_memory.rs` is
`#![cfg(target_os = "linux")]`, so it compiles to nothing here: the harness
lists 17, not 18. The recipe needs no guard for this, because nextest 0.9.143
exits 4 — "no tests to run" — when a filter matches nothing, so
`just scale spill_memory` fails loudly on darwin instead of passing empty.
Do not add a `--no-tests` flag that would silence it.

The tier asserts no ceilings, so this recipe does not make it a gate and must
not be sold as one — [[gates-are-tests]] still applies, and the parts these
tables feed stay as unreproducible as [[every-published-number-is-unreproducible]]
says until a run writes its numbers down.

## Check

`cargo nextest list --workspace --run-ignored only 2>/dev/null | wc -l` prints
17 on darwin and 18 on linux, and

```
just scale gc_sweep_scale
```

builds release, runs exactly one test, prints its `victims=` table to the
terminal uncaptured, and exits 0.
