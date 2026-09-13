---

kind: work
level: 10
status: done
description: "`ingest` answers `accepted` with an intake id that no read accepts, and the intake it landed in is 2,268 files deep draining at 5.7 a minute — a written fact is unreadable for hours and the caller is told nothing"
read_when: "writing a fact from an agent, or measuring ingest latency"
---

# ingest-says-when-a-fact-lands

## Do

When the drain loop runs, `tool_ingest` writes the job to
`.memory/intake/direct/` and answers `{"status":"accepted","doc_id":...}`
(`src/rpc/src/server.rs:1736`). Two things follow that a caller cannot see.
The `doc_id` is the intake job's id, not a thought's: `query {id: <that>}`
answers `thought not found`. And the intake is a queue — measured 2026-09-06,
2,268 jobs pending, 1,855 drained, 74 of them in the preceding 13 minutes, a
rate of 5.7 a minute and roughly six hours to reach a job written now.

Probed end to end that day: a fact ingested through the tool was still not
retrievable by its own exact token 200 seconds later, in `mode: content`, and
was found sitting in `.memory/intake/direct/` as
`88bec4d8fa9da93b4adc3df4b93c22e75c768c1f691b466d9c8079a750bdd06b.json`. The
synchronous leg above it (`src/rpc/src/server.rs:1696`) returns
`embedded_chunks` and lands immediately — the same tool answers two different
contracts and names neither.

Say which one happened. Done: every leg of the tool names its id's kind
(`id_kind` — `document` for the synchronous leg, `intake_job` for the durable
one, `queue_job` for the RAM fallback), the `accepted` answer carries
`intake_pending` and a `message` saying the id is not in the graph until the
drain commits it, and an id-read that misses looks in the intake before it
answers: `Server::id_miss` names the waiting job's path instead of `thought not
found`. An agent that writes a fact and immediately reads for it is otherwise
measuring a drain rate it was never told about.

The backlog itself is the ingest half of `the-tick-queue-is-permanently-full`
and is not fixed here; only the silence is.

## Check

Against a live daemon with a non-empty intake, `ingest {text: ...}` answers a
field naming the pending depth and marks the returned id as an intake job, and
`query {id: <that id>}` refuses with a message that names where the fact is
instead of `thought not found`. Run: `cargo test --test e2e intake_drain` —
`ingest_names_the_intake_a_fact_landed_in_and_the_id_read_says_where_it_is`
drives both calls over `memory mcp` against a job the drain cannot commit.
