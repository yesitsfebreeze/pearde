# the-exchange-ledger-lives-in-memory-s-store-and-halves-at-each-day-week-and-month-rollover — review

Canonical PRD: [prd.md](prd.md). Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — independent agent review, 2026-09-15 — FAIL 77/100

| Dimension | /20 |
| --- | ---: |
| Value and scope | 17 |
| Ownership and reuse | 17 |
| Dependencies and slices | 15 |
| Acceptance and baseline | 16 |
| Failure and compatibility | 12 |

Blocking findings:

1. The footprint omitted the store-core test file, so collection would refuse it and `cargo test -p store_core ledger` could pass with zero tests.
2. A late row for a closed unit (a pre-midnight `ts` arriving after the pass, an append between scan and commit, a concurrent or repeated import) would overwrite the unit's record, or close a parent around it.
3. There was no single-flight pass: the loop and an explicit `rollover` could condense the same inputs concurrently.
4. A unit too small to halve (one "hi"/"ok" exchange) would retry a model call every minute forever.

Non-blocking notes:

- Sink success should mean `committed`/`deduped`.
- Records must keep their `children` ids for retries.
- A loop through `invoke` defeats idle detection.
- The engine starts lazily, and the standalone daemon has no loop.
- Re-import should be idempotent.
- Verify cost should be measured against the 120-second block limit.
- `proxy.port` and the docs were out of the contract.
- An operator wipe removes year records.

Response in the spec revision:

1. The footprint gained the store test.
2. The existing record is folded in as an input.
3. `ledger_commit` aborts when an input is already gone.
4. The pass holds a process-wide mutex.
5. Inputs under 1 KiB are kept verbatim.
6. The loop backs off to 15 minutes after any failure.
7. The sink statuses are defined.
8. Records carry `children`.
9. The loop calls `ledger_pass` directly.
10. Raw keys are content digests.
11. The engine and daemon scope is stated.
12. `proxy.port` was dropped from scope.
13. The docs state the wipe.

## Round 2: independent agent review, 2026-09-15. FAIL, 82/100

Scores: value/scope 17, ownership/reuse 18, dependencies/slices 18, acceptance/baseline 17, failure/compatibility 12. Round-1 blockers 1–3 were closed in code; round-1 blocker 4 came back at chunk level.

Blocking findings:

1. Days mirrored in earlier passes leaked in the graph when a month or year consumed an unmirrored week in the same pass. Children were carried only from the target record.
2. A tail chunk under 1 KiB could not be halved. It wedged its day and every tier above it.

Non-blocking notes:

- The model should be `None` when the reason URL is empty.
- Import should hold the pass mutex.
- The re-import acceptance wording overstated idempotence.
- A `rejected` ingest counted as done.
- A cap event is expensive.
- `ts` was unchecked.
- Concurrent legacy request/response pairs are dropped by the single `pending` slot.

Response:

- Children now carry through every consumed unit input.
- Chunks under 1 KiB ride along verbatim, and the final text is checked against the total budget.
- The model is `None` for an empty reason URL.
- Import holds the pass mutex.
- A `rejected` ingest is a retried failure.
- `append` refuses a non-millisecond `ts`.
- The acceptance wording is corrected.

Regression tests were added for the leak, the tail chunk and the `ts` check.

The legacy concurrent-pair limit and the cap cost are accepted as documented limits.

## Round 3: independent agent review, 2026-09-15. PASS, 90/100

Scores:

| Dimension | Score |
| --- | ---: |
| Value/scope | 17 |
| Ownership/reuse | 19 |
| Dependencies/slices | 18 |
| Acceptance/baseline | 18 |
| Failure/compatibility | 18 |

The review checked both round-2 blockers in code and found them closed. There are no blocking findings.

Non-blocking notes:

- A rejected ingest is retried forever, even though the hygiene gate is deterministic.
- A `ts` given in seconds passes `append` and lands in 1970.
- A long import holds `PASS` for its whole run.

Response:

- A rejected ingest is now final. The record is marked ingested, its children stay in the graph, and nothing retries it (test `a_record_the_graph_refuses_for_good_keeps_its_children_and_stops_retrying`).
- `append` refuses a `ts` below 10^12.
- The docs now say that `rollover` waits for a running import.

Rounds used: 3/5.
