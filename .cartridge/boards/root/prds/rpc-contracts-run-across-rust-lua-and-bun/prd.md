---
repo: /Users/feb/dev/cartridge
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
review-round: 1
review-status: superseded-recommend-retire
rehomed-to: '@runtime/rpc-contracts-run-across-rust-lua-and-bun'
canonical-scope: rpc-contracts-run-across-rust-lua-and-bun
footprint:
- /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/fixtures/transport/cases.json
- /Users/feb/dev/cartridge/cartridge.ctg/src/transport/tests/rpc.rs
- /Users/feb/dev/cartridge/.cartridge/tests/integration/transport-conformance.test.ts
- /Users/feb/dev/cartridge/.cartridge/memos/routine/cartridge-development.md
---

# Rust, Lua and TypeScript peers pass one set of transport cases

The cartridge protocol (`cartridge.ctg/docs/transport.txt`) has three speakers: the Rust peer (`src/transport/rpc.rs`), Lua listeners bridged by `src/node.rs`, and `src/wire.ts`, copied byte-identically into tui, live, auth and prd. Only Rust has behavioral tests; the shared `fixtures/rpc/cases.json` was deleted in cartridge.ctg `939e7d1`. Root owns one executable case set so a drifting speaker fails a gate.

## Acceptance

- [ ] One committed `cases.json` (null, false, `[]`, `{}`, non-BMP text, error object, notification, oversized frame) runs in a Rust test against `transport::rpc` and in a root Bun test through the real `cartridge` host with a Lua and a TypeScript fixture listener. Every case decodes identically, or its applicability row names the participant and reason.
- [ ] Concurrent calls in both directions with overlapping numeric ids reach their own callers for Rust↔Lua and Rust↔TypeScript.
- [ ] A listener that closes with calls pending fails each waiter (no hang); a late reply is dropped, never delivered to a reused id. A deadline breach reports `timed_out`, distinct from a protocol error.
- [ ] The Bun test runs against every `*.ctg/src/wire.ts`; a disposable mutated copy fails the gate naming that file.

## Proof and recovery

First probe from `/Users/feb/dev/cartridge`: `just build runtime`, then a TypeScript fixture on the current host. Record revision and result; incompatibility is the baseline, not a pass. Gates: `just test runtime`; `bun test .cartridge/tests/integration/transport-conformance.test.ts` (to create; add to the `all` test step of `cartridge-development.md`). Tests and fixtures only. Fixes to a `wire.ts` copy go to its owner.

## Dependencies and review

No hard `needs`. The shipped cartridges' manifest port is out of scope: fixtures declare their own events. [Review](review.md), round 1 of 5; no inherited rounds.
