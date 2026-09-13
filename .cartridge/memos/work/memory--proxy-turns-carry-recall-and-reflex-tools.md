---
kind: work
level: 9
status: open
estimate: 2d
description: proxy turns receive bounded memory context and reflex-prepared tools without nesting an agent or model decision loop
read_when: implementing proxy-first memory attachment rather than recording-only forwarding
---

# proxy-turns-carry-recall-and-reflex-tools

## Do

An ordinary agent routed through memory receives relevant bounded memory context
and reflex-selected tool preparation on its model request through the core
proxy. Context retains provenance and distinguishes retrieved data from trusted
instructions. Client-owned tools, cancellation, streaming and provider errors
keep their contracts. Memory or reflex failure leaves the original request
usable with an observable degraded outcome, not a silent stalled turn.

The proxy does not ask a model what to do and does not nest an agent loop.
Existing recall, reflex, routing and authorization mechanisms are reused;
preparation cannot bypass tool policy or widen access. A recording-only proxy
or MCP initialization alone does not satisfy this terminal of [[vision]].

subwork:
[[@prd/work/memory--agent-turn-recall-is-bounded-and-fail-open.md]],
[[@prd/work/memory--changed-context-preserves-the-stable-prompt.md]]

For the first core revision, Reflex preparation uses bounded guidance while
leaving the authorized tool surface available. Schema hiding and its loader,
recorded in [[reflex-guides-deferred-tool-visibility]], are deferred ideas,
not prerequisites for this terminal. This narrowing does not mark the remaining
proxy preparation or its acceptance complete.
