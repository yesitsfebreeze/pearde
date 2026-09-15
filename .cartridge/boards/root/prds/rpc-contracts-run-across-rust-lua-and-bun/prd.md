---
repo: /Users/feb/dev/cartridge
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
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

## From the retired work memo

Folded 2026-09-15 from `work/rpc-contracts-run-across-rust-lua-and-bun.md` (status active, owner codex-work-2026-09-12/rpc-contracts, estimate 2d). The PRD state above is authoritative.

> The language boundaries share executable RPC contract cases

### Outcome

Rust SDK processes, Lua services and the Bun UI obey one documented host protocol, verified through shared behavioral cases. Keep transport and lifecycle infrastructure in the core; reuse existing fixtures instead of creating another runtime.

### Check

- [ ] A real-host suite exercises Rust-to-Lua and host-to-Bun round-trips for null, false, empty arrays/objects, Unicode, errors and concurrent bidirectional calls with overlapping numeric IDs.
- [ ] Cases cover apply failure, reload/dispose, EOF with pending calls and late replies; each participant has an explicit applicability matrix.
- [ ] Tests distinguish a supported timeout/cancellation difference from a protocol violation and run under the normal gate.

### Approach

Observed 2026-09-12: `core/tests/process.rs` already checks Rust/Lua ID namespaces, EOF, metadata and dropped waiters. `builtin/ui/tests/wire.test.ts` has one test for out-of-order replies and disconnect. Extend that foundation; the missing result is shared coverage, not a claim that no integration tests exist.

Audit: [[runtime-audit-2026-09-12]].
