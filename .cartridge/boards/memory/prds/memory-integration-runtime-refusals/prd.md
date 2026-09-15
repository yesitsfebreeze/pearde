---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "4h"
actual: "1h"
---

# Distinguish absent Tokio runtime from shutdown refusal in RPC errors and stop admitting work while draining.

## Do

Trace the bridge result from `src/llm/src/llm.rs` through `src/rpc/src/server.rs`. Replace the ambiguous `None` path with explicit runtime-absent and process-shutting-down outcomes. Reject new model-dependent work once shutdown begins, while allowing already-admitted work to finish or return a distinct refusal. Preserve existing shutdown counters and add focused tests for both branches and the race between admission and shutdown. Do not hide provider failures behind this classification.

**Landed 2026-09-09.** `llm::BridgeRefusal` names the two faults the blocking
bridge collapsed into one `None`: `NoRuntime`, whose text is still the old
`no tokio runtime`, and `ShuttingDown`. `try_block_on_in_place` carries the
reason and the `Option` forms stay as `.ok()` wrappers, so a caller that only
needs "no answer came back" is unchanged and `SHUTDOWN_REFUSED` still counts
the shutdown half alone. Six RPC sites — four in `server.rs`, the reason
completion in `ask.rs`, and the intake drain — report the refusal they hit;
`ask.rs` had been blaming a reason endpoint that was up. `Server::invoke`
refuses `query`, `search`, `ingest`, `link`, `focus`, `intake_drain` and `ask`
with the shutdown category once the latch is up, so work is turned away at
admission rather than after it has run to the bridge; anything already past
that line is a counted crossing the shutdown waits for, and the abandonment
inside it carries the same category. Provider failures still travel as
themselves.

**The live half of the Check.** A fresh daemon on a scratch root answered
`query` and `ask`. An `ask` parked in the bridge when SIGTERM arrived came back
`memory ask: shutting down: the daemon refused this request, retry against a
fresh one` — the drain-window refusal the memo asks for, in place of
`no tokio runtime`. `cargo test -p llm -p rpc --lib -- --test-threads=4` is
24 + 126 green, and `cargo nextest run --workspace --no-fail-fast` is 1466 of
1467: the one red is `memory::cited_paths`, the lane artefact owned by
[the-plan-crate-cites-an-untracked-file](../the-plan-crate-cites-an-untracked-file/prd.md).

## Acceptance
`cargo test -p llm -p rpc --lib -- --test-threads=4` passes, including tests that assert distinct error text or typed categories for absent runtime and shutdown refusal. A fresh-daemon query and answer smoke test passes before shutdown, and a request during drain returns the shutdown category rather than `no tokio runtime`.
