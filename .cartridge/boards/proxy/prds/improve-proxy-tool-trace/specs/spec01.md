---
complexity: medium
footprint:
- src/main.rs
- src/service.rs
- src/streaming.rs
- src/usage.rs
- src/trace.rs
- .cartridge/tests/unit/tests.rs
- .cartridge/docs/traces.md
---

# Inspect bounded internal tool traces by authenticated request identity

Add `tool_trace: false`, `trace_capacity: 128` (1–128) and `trace_ttl_secs: 300` (positive). One process-local archive holds at most capacity traces including active requests, at most 256 call records each, plus a capacity-sized diagnostic tombstone list. TTL starts at request admission and does not extend on read or completion. Expired/evicted active traces never get reinserted by later completion. Overflow marks truncation and counts omitted calls without changing execution. No durable files, payload opt-in, extra inference, retry or history reconstruction.

Reuse the trusted `Principal` established by authenticated HTTP keys or native injection. A shared key remains one principal; metadata and scope headers do not confer authority. Expose an opaque `proxy_trace_*` identity only when enabled: additive `cartridge_trace: {id}` on JSON success/errors and exactly one terminal SSE success/error; `x-cartridge-trace-id` is available from SSE headers before completion. Native errors include the lookup ID. Lookup is native `proxy {op:"trace",id}` for the native principal or authenticated HTTP GET `/v1/cartridge/traces/<id>`. Other principals/unknown IDs yield generic `trace_unavailable`; recently expired/evicted IDs yield distinct diagnostics only to their owner. Restart loses diagnostics. Disabled lookup is explicit and retains no trace records.

Each internal call attempt records request/round/call identity, bounded tool name, descriptor digest, policy decision and SHA-256 of the supplied policy revision (unknown if absent or over 64 KiB), dispatch state, monotonic policy/tool/total durations, and a fixed outcome enum. Do not retain arguments, results, caller messages, workspace paths, raw policy reasons/revisions or arbitrary error text. Caller-owned calls are not executed or recorded as internal calls. A denied/ask attempt is explicitly not dispatched. Optional memo observation behavior remains independent.

Request-owned and call-owned drop guards preserve completed attempts and label interrupted work. A dropped dispatched attempt records cancellation requested and completion unknown; it must never claim cancellation succeeded or effects were rolled back. Returned tool errors, transport failures, invalid envelopes, policy failures and provider failures retain the existing model/error flow, with generic diagnostic outcomes in the trace. Finish the tool record before awaiting best-effort outcome observations, so later cancellation does not erase known completion. Trace timing/status refers to proxy processing, not delivery acknowledgment. Missing/evicted telemetry never changes execution or recreates a record.

## Acceptance

- [x] All three native wires: mixed private/caller batches have exactly one record per internal attempt, correct round/call/descriptor/policy attribution, timings and outcomes; caller history/tool semantics and disabled JSON/SSE remain unchanged.
- [x] Distinct authenticated clients and the native principal cannot read each other's traces, including active/expired/evicted records; metadata/header spoofing fails; own active/final lookup works.
- [x] TTL, archive capacity, per-trace overflow and restart produce bounded explicit results. Secret sentinels in arguments/results/policy reasons/revisions/provider errors never appear in default traces.
- [x] Deny/ask/policy failure, reported tool error, invalid envelope, transport error, provider interruption, deadline and client disconnect retain known partial work; pending dispatch completion stays unknown, cancellation targets the same invocation, and no hidden retry occurs.

## Verify and Proof

```sh
cd /Users/feb/dev/cartridge/cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/proxy-trace" just test proxy
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/proxy-trace" just check proxy
```

Use real loopback HTTP/SSE with controlled deterministic providers and actual authenticated headers. Explicit monotonic instants test TTL without sleeping; semaphore-controlled tool calls expose active lookup and partial cancellation. Fixed terminal markers and captured dispatch requests prove no replay. Existing shared GitFS/policy consumer tests remain coordinator integration gates; prior continuation/usage receipts require revalidation because footprints overlap. Recovery is explicit client lookup or fresh caller-owned input, never automatic execution.
