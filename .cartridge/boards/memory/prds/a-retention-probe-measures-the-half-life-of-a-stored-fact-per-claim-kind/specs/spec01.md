---
complexity: mid
footprint:
  - /Users/feb/dev/cartridge/memory.ctg/.cartridge/development/memos/routine/develop-memory.md
  - /Users/feb/dev/cartridge/memory.ctg/.cartridge/tests/integration/bench/Cargo.toml
  - /Users/feb/dev/cartridge/memory.ctg/.cartridge/tests/integration/bench/src/main.rs
  - /Users/feb/dev/cartridge/memory.ctg/.cartridge/tests/integration/bench/src/common.rs
  - /Users/feb/dev/cartridge/memory.ctg/.cartridge/tests/integration/bench/src/retention.rs
  - /Users/feb/dev/cartridge/memory.ctg/.cartridge/tests/integration/bench/RESULTS.md
  - /Users/feb/dev/cartridge/memory.ctg/.cartridge/justfile
  - /Users/feb/dev/cartridge/memory.ctg/Cargo.lock
---

# spec01 — Evaluate retention by claim kind on mature memory

## Base and dependencies

- Base repository: `/Users/feb/dev/cartridge/memory.ctg` at source HEAD `1351865eb0e787cf819456aaa201c18eacf74406`.
- The checkout is already dirty for unrelated memory cartridge work; implementation must preserve those changes or use the coordinator-assigned lane.
- The eval reuses the existing `memory-bench` crate and the mature fixture file `.cartridge/tests/integration/bench/mature.json`; it must not require a running daemon.
- The eval must support a real embed provider through the existing cache machinery and must support `--fake-llm` for plumbing checks. Scores from `--fake-llm` are labelled meaningless.
- Every cargo verify command must set an isolated `CARGO_TARGET_DIR` before invoking cargo.

## Acceptance

- [x] `just eval-retention --cache /tmp/memory-retention-vectors.json --report-dir /tmp/memory-retention` runs against `.cartridge/tests/integration/bench/mature.json` and prints one table with rows for `preference`, `decision`, `project`, `fact`, `code-fact`, `reference`, `procedural` and `unlabelled`.
- [x] Every table cell contains `untouched` and `touched` measurements for rank at k=10 and the final tier `hot` or `cold`.
- [x] The run includes both retrieval variants, `full` and `simple_hybrid`, using the same fixture, vectors, spans, unrelated-document count and query labels.
- [x] A second process against the same vector cache returns identical ranks, tiers and report JSON apart from run timestamps and report paths.
- [x] `.cartridge/tests/integration/bench/RESULTS.md` gains a dated `Retention by claim kind` section that states the span grid, unrelated-document count, vector cache identity, source revision and the decision supported by the table.

## Implementation steps

1. Add a `retention` subcommand to `.cartridge/tests/integration/bench/src/main.rs` and implement it in a new `.cartridge/tests/integration/bench/src/retention.rs` module. Keep `common.rs` as shared embedding/report plumbing; do not duplicate the e2e CLI harness.
2. Extend `.cartridge/tests/integration/bench/Cargo.toml` only if the retention runner needs an already-workspace dependency that is not listed. Prefer the dependencies already used by `replay.rs`: `base`, `graph`, `retrieval`, `config`, `store_core`, `tick` and `util`.
3. Add a `eval-retention` recipe to `.cartridge/development/memos/routine/develop-memory.md` and wire `.cartridge/justfile` only if its generic recipe list cannot dispatch it through `memo-run`. The top-level `justfile` must remain an import only.
4. Build the eval in memory-bench, not as a daemon-only CLI path. Load `mature.json`, validate it with retention-specific checks, obtain vectors through the existing cache shape, build an in-memory `GraphGnn` with a bound cold store, and query through `retrieval::query::query` for both variants.
5. Use synthetic probe documents appended to the mature fixture at run time. For each claim kind, create one labelled target entity with deterministic text and `Entity.claim_kind` set to that kind; create the unlabelled default with empty `claim_kind`. Set `EntityKind::Claim` for the labelled and unlabelled probes so automatic GC is allowed to spill them; do not use `EntityKind::Fact`, because automatic removal protects Facts and would not measure the kind-specific heat curve.
6. For each span, choose deterministic ageing by setting the probe entity's `created_at`, `accessed_at`, and `heat_updated_at` to `now - span`. Give the probe initial heat equal to one access deposit. Run the existing GC path through `tick::tick_stigmergy::run_gc` against the root memory after constructing the graph, so the tier result observes the production cold-victim policy rather than a copied predicate.
7. For each span and kind, push the configured unrelated count by inserting deterministic unrelated `EntityKind::Claim` documents with fixed vectors and text into the graph before querying. This must exercise ranking competition without changing the target label or query after observing scores.
8. For the intermediate-touch arm, start with the same aged target, apply exactly one access deposit at the midpoint by using the same heat math production retrieval uses or by querying the target at the midpoint and committing access, then advance the entity clocks to the final span before GC and final query. The report must name which mechanism was implemented.
9. Query with k=10. The result row rank is the one-based index of the target ID in the delivered list, or `>10` when absent. The tier is `cold` if the result's `cold_ids` contains the target or the target is present in the cold store after GC, else `hot`.
10. Write a machine-readable report under the requested report directory using `common::write_report`, print a human table to stdout, and update `.cartridge/tests/integration/bench/RESULTS.md` with a dated section after a real non-fake run.
11. Add focused unit tests in `retention.rs` for claim-kind coverage, stable span ordering, cache refusal/reuse, and repeatability normalization. Reuse the mature fixture smoke assertions already present in `replay.rs` where possible instead of copying the whole fixture builder.

## Verify and Proof

<!--
How collect runs these blocks (engine facts, src/lifecycle.ts collect/verify):
- Each sh/bash/shell block runs as `sh -eu -c`, 120 s limit, empty stdin, the
  collector's environment.
- It runs twice: first with cwd = the lane, a worktree of the PRD's `repo` at
  `prd.ctg/.cartridge/boards/<board>/.lanes/<slug>`; then, after the
  fast-forward, with cwd = `repo` itself. With no lane it runs once, in `repo`.
- Paths are relative to the repo root. Never `cd` to an absolute checkout, or
  pass 1 tests the wrong tree. `../<sibling>.ctg` does not resolve from the
  lane either; name absolute tools (e.g. CARTRIDGE_BIN) with an env default.
- Pass 2 runs in the live checkout. The host hot-restarts a cartridge when its
  target/debug dylib changes, so every cargo block first sets
  `export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/<slug>-verify}"`.
- A block must not write inside the footprint. In the lane pass, collect
  commits such writes; in pass 2 they abort collection with "source footprint
  changed during integrated verification". Write scratch output elsewhere.
-->

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/a-retention-probe-verify}"
cargo test -p memory-bench retention:: --manifest-path Cargo.toml
```

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/a-retention-probe-verify}"
rm -rf /tmp/memory-retention-verify
mkdir -p /tmp/memory-retention-verify
just eval-retention --fake-llm --cache /tmp/memory-retention-verify/vectors.json --report-dir /tmp/memory-retention-verify/run1 > /tmp/memory-retention-verify/run1.out
just eval-retention --fake-llm --cache /tmp/memory-retention-verify/vectors.json --report-dir /tmp/memory-retention-verify/run2 > /tmp/memory-retention-verify/run2.out
if ! grep -q 'preference' /tmp/memory-retention-verify/run1.out; then exit 1; fi
if ! grep -q 'decision' /tmp/memory-retention-verify/run1.out; then exit 1; fi
if ! grep -q 'project' /tmp/memory-retention-verify/run1.out; then exit 1; fi
if ! grep -q 'fact' /tmp/memory-retention-verify/run1.out; then exit 1; fi
if ! grep -q 'code-fact' /tmp/memory-retention-verify/run1.out; then exit 1; fi
if ! grep -q 'reference' /tmp/memory-retention-verify/run1.out; then exit 1; fi
if ! grep -q 'procedural' /tmp/memory-retention-verify/run1.out; then exit 1; fi
if ! grep -q 'unlabelled' /tmp/memory-retention-verify/run1.out; then exit 1; fi
python3 - <<'PY'
import glob, json, sys
reports = []
for d in ['run1', 'run2']:
    paths = sorted(glob.glob(f'/tmp/memory-retention-verify/{d}/retention-*.json'))
    if len(paths) != 1:
        sys.exit(f'expected one retention report for {d}, found {paths}')
    with open(paths[0]) as f:
        data = json.load(f)
    data.pop('generated_at', None)
    data.pop('report_path', None)
    reports.append(data)
if reports[0] != reports[1]:
    sys.exit('retention eval is not repeatable against one cache')
for variant in ['full', 'simple_hybrid']:
    rows = [r for r in reports[0]['results'] if r['variant'] == variant]
    if len(rows) != 8:
        sys.exit(f'{variant} has {len(rows)} rows, expected 8')
    for row in rows:
        if set(row['cells']) != set(reports[0]['spans']):
            sys.exit(f'{row["claim_kind"]} has wrong span cells')
        for cell in row['cells'].values():
            for arm in ['untouched', 'touched']:
                if cell[arm]['tier'] not in ['hot', 'cold']:
                    sys.exit('cell tier must be hot or cold')
                rank = cell[arm]['rank_at_10']
                if not (rank == '>10' or isinstance(rank, int) and 1 <= rank <= 10):
                    sys.exit('rank_at_10 must be 1..10 or >10')
PY
```

```sh
if ! grep -q 'Retention by claim kind' .cartridge/tests/integration/bench/RESULTS.md; then exit 1; fi
if ! grep -q 'just eval-retention' .cartridge/tests/integration/bench/RESULTS.md; then exit 1; fi
```

## Reusable attempt artifacts

- Existing mature fixture: `.cartridge/tests/integration/bench/mature.json`.
- Existing mature fixture smoke test: `replay::tests::the_mature_fixture_carries_read_history_and_trains_where_rows_are_resident`.
- Analyst probe command: `CARGO_TARGET_DIR=/tmp/memory-retention-analyst-target cargo test -p memory-bench the_mature_fixture_carries_read_history_and_trains_where_rows_are_resident --manifest-path /Users/feb/dev/cartridge/memory.ctg/Cargo.toml`.

## Remaining work

The implementation still needs the new `retention.rs` runner, the just recipe, focused tests, a real cached eval run, and the dated `RESULTS.md` section. The spec deliberately does not prescribe the exact span grid or unrelated-document count beyond requiring them to be fixed and reported; the implementer should choose the smallest grid that crosses the default seven-day cold gate and at least one long-retention kind curve.
