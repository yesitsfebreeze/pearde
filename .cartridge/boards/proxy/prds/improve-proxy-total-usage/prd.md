---
repo: /Users/feb/dev/cartridge/proxy.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: proxy
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: improve-proxy-total-usage
needs:
- '@gitfs/tool-results-interoperate'
footprint:
- src/main.rs
- src/service.rs
- src/streaming.rs
- src/usage.rs
- .cartridge/tests/unit/tests.rs
- .cartridge/docs/usage.md
commit: "9ddcc08807a059579c21227ad9d3523d242ddf86"
---

# Account for every internal model round consistently

JSON and streaming responses provide consistent total usage across internal tool rounds, with final-round usage separately identified.

## Acceptance

- [x] A three-round fixture reports matching cumulative totals for JSON and SSE and no double counting of final events.
- [x] Missing usage, partial stream failure and cancellation preserve known totals and label incomplete accounting.

- [x] Keep native request/response wire semantics and caller-owned conversation history. New telemetry is opt-in/additive and bounded. Reverting continuation changes must report invalid mappings rather than resolve to the wrong provider/client.

## Proof and recovery

Source: `proxy.ctg/src/service.rs`, `src/streaming.rs`, `src/wire.rs` and `src/usage.rs`.

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test proxy` from the composed root with the acceptance fixtures. The public proxy tests/check and GitFS/policy consumer gates now pass; see verification.json.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Review history](review.md): round 3 passed at 96/100; acceptance evidence is separate from the plan score.

Reverify unchanged usage accounting at0c9d4e9 after scoped continuation changes;
prior480a093f receipt retained. Router integration is0a216cb.

Reverify unchanged acceptance after the next integrated owner feature; earlier
0c9d4e9b receipt retained. No contract relaxation.

Reverification: recall integration at9ddcc088 changes shared proxy paths. Bind newly imported context/wire modules and dependency declarations without changing behavior acceptance or executable gates.
