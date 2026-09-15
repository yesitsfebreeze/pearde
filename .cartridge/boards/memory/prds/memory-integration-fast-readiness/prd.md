---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "1d"
---

# A bounded `ready` operation answers daemon generation, build identity, uptime, lifecycle state and endpoint readiness without the graph read lock `health` waits on.

Most of the facts this memo asked for were already on the wire when it came up
for work. `HealthRes` had grown them append-only over four days: `build_id`,
`build_stamp` and `config_id` are the build identity, `uptime_ms` the uptime,
`watchdog_restarts` the replacement state, and `llm_complete_failed`,
`last_llm_complete_failure` and `llm_embed_wedges` the two endpoints. What was
missing was not another counter. It was that every one of them was behind
`Server::health_stats`, which opens with `self.graph.read()` and walks every
resident entity — so the answer to "which build is this and is it draining"
waits on whatever holds the graph, at exactly the moment the question becomes
urgent.

Two facts were genuinely absent. **Generation identity**: `build_id` is equal
for two daemons running one binary and `watchdog_restarts` reads 0 for both,
so neither separates two generations; the pid does, and only the daemon can
report its own. **Lifecycle state**: `invoke` had been refusing model-dependent
work on `util::lifecycle::is_shutting_down()` since the drain landed, but
nothing published the latch, so a caller learned the daemon was leaving from a
failure rather than from a field.

## Do

`Server::readiness_stats` answers from process-global atomics, this process's
environment, its config and its LLM client, and touches no graph at all.
`invoke("ready")` reaches it, so no RPC method was added and the reply still
carries `HealthRes`'s field names — the same wire contract asked a narrower
question. `pid` and `draining` are new on the wire, `serde(default)` like every
field before them; the typed `health()` sets both too, so the detailed view is
never poorer than the fast one. The crossing gauge and its worker denominator
are read through the same `util::lifecycle` accessors
[the-number-that-names-the-stall-is-computed-and-unread](../the-number-that-names-the-stall-is-computed-and-unread/prd.md) minted, not
duplicated. `memory ready` prints the block and its own latency, and is an MCP
tool because every dispatch arm has to be one. Neither poll touches `idle_ms`
or the reflex ledger: a monitor asking whether a daemon is alive must not keep
it looking permanently busy.

The CLI-side half of the cost is not touched here and is not this memo's:
`cmd_health` still calls `load_graph` before it asks the daemon anything, which
is [memory-health-loads-its-own-graph-beside-the-daemon](../memory-health-loads-its-own-graph-beside-the-daemon/prd.md). `memory ready` simply
never opens the store, so it is unaffected either way.

## Acceptance
Done 2026-09-09. Measured:

| reading | number |
|---|---|
| `readiness_stats` under a graph write held 800 ms | answered, deadline 200 ms |
| the same call with `graph.read()` put back (red-proof) | 803 ms — the test fails |
| `memory ready` against a live daemon, whole process | 12 ms wall, `answered: 1 ms` |
| `memory ready` on an unserved store, whole process | 13 ms, opens nothing |
| `memory health` on the record store, for contrast | 85 s, and that is the CLI's own `load_graph` |
| the two-generation e2e, two daemons and a `memory stop` | 5.3 s |

`readiness_answers_while_a_write_holds_the_graph` carries its own control: a
second thread calls `health_stats` and is provably still parked when readiness
has already answered, then completes once the write lets go — so a fast reply
cannot pass by the lock having been free.
`readiness_names_this_process_and_this_build` pins the pid to this process and
the stamp to this binary; `readiness_shows_draining_before_requests_start_failing`
raises the latch and asserts readiness says `draining` while it still answers
and `query` is already refused.
`ready_tells_two_daemon_generations_apart_and_names_the_build` does it for
real — two daemons over one store through the binary — and asserts `memory
health` still prints the counts that need the store.
