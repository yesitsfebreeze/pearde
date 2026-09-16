---
state: "done"
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge/proxy.ctg"
capability-owner: proxy
needs:
- "@memory/the-exchange-ledger-lives-in-memory-s-store-and-halves-at-each-day-week-and-month-rollover"
workflow: "develop-one-cartridge"
commit: "0bd95016091d7a0998f345fc45759f219f6ada34"
---

# The proxy hands each finished exchange to the memory ledger

## Outcome

With the `ledger` setting naming a memory key (normally `"memory"`), every
exchange `Service::request_for_principal` completes, whether streamed or not,
sends `{op: "ledger", action: "append", ts, wire, user, response}` to that key.
`user` is `wire::last_user_text` of the request, and `response` is the
assistant text of the final response. The send is spawned with a bounded
timeout and never awaited by the request. A refused or failed send is logged
once as `proxy_ledger_degraded` and never changes the response.

The default `ledger` is `""`, which declares no need and sends nothing. The
need is `${config.ledger}`, the same pattern `harness` uses for `memory`. So a
composition without memory keeps working, and one that sets the key waits for
memory like any other need.

## Acceptance

- [x] `cargo test` (46 passed), `cargo fmt --check` and `cargo clippy --all-targets -D warnings` green in the proxy lane.
- [x] With `ledger = "memory"`, a completed chat, responses and anthropic exchange each sends one append carrying the request's newest user text and the response text.
- [x] A `call` that errors or never answers leaves the forwarded response byte-identical and the request's latency unaffected.
- [x] With `ledger = ""`, nothing is sent and `needs` resolves without memory.
