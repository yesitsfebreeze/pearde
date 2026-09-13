---
kind: work
level: 10
status: done
description: the drain took one parked job at a time against a single-slot embedder, so the run loop now coalesces up to sixteen parked jobs into one chunk-embed round trip
read_when: "touching the intake drain or the tick's embed cost"
---

# the-intake-drain-runs-a-batch

## Do

Measured 2026-09-06: `.memory/intake/direct/` held 2,268 pending jobs, `done/`
1,855, of which 74 landed in the preceding 13 minutes — 5.7 jobs a minute, one
job at a time, roughly six hours to reach a fact written now
([[@prd/work/memory--ingest-says-when-a-fact-lands.md]]).

Concurrency cannot fix it: the embedding server runs one slot and hangs on
parallel requests ([[@prd/work/memory--embeds-go-through-one-lane.md]]). Batching can. One
`/api/embed` call takes many inputs and `embed_batch` already sends them that
way — but the drain called it per job, so a job with two chunks was a two-input
batch and the next job waited for a whole round trip.

Landed: `run_loop` (`src/ingest/src/ingest_worker.rs`) takes one task off the
receiver and then `try_recv`s up to `BATCH_CAP` more, distills each — the
gates, the split, the unchanged-source hit, the document — and spends ONE
`embed_chunks` call on every chunk of all of them, then places and answers per
job, so one job's failure is still exactly one job's failure and its payload
stays for retry. A tombstone closes the run of ingests parked ahead of it
rather than joining a batch that would overtake it, which is the ordering the
one queue exists for. `Worker::start` parks a job and hands back the channel
its `Outcome` arrives on; `drain_direct_once`
(`src/ingest/src/ingest_direct.rs`) parks a whole group that way before it
waits on the first, because a drain that awaited each outcome left the run loop
one job to find. Its per-job archive and its poison and failure handling are
unchanged.

Deliberately left per job: the document embed. `place_document` makes its own
one-text call, so M one-chunk jobs cost M + 1 round trips where they cost 2M
before. Folding the document texts into the same batch means
`place_document` taking a vector it was handed instead of fetching one, which
is `src/ingest/src/ingest_place.rs` and a lane of its own. The tick loop's
half is out of scope for the same reason it was before.

## Check

`cargo test -p ingest` — two tests carry it:

- `a_batch_of_parked_jobs_spends_one_embed_call_on_every_chunk` counts every
  `/api/embed` request's input length behind a worker fed six parked one-chunk
  jobs: exactly one request carries all six chunks, seven requests in all.
  Red-proofed at `BATCH_CAP = 1`, where the same test sees twelve requests of
  one input each and no six-input request at any point.
- `a_seeded_drain_archives_every_job_exactly_once` drains an intake seeded with
  40 payloads — more than `BATCH_CAP`, so the accounting crosses a group
  boundary — and `done/` holds exactly those 40 files with the intake empty.
