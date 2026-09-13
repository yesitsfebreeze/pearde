---
complexity: medium
footprint:
  - Cargo.toml
  - src/lib.rs
  - src/cartridge.rs
  - src/service.rs
  - src/turn.rs
  - src/observation.rs
  - .cartridge/tests/unit/observation.rs
  - .cartridge/tests/integration/tool-observations.test.ts
  - .cartridge/tests/integration/observation-fixture.ts
  - .cartridge/docs/tool-observations.md
---

# Observe native tool calls at dispatch

At src/cartridge.rs::handle's native call branch, wrap only exact bounded tool.* keys with an observation guard. The host-owned source cartridge name is provenance; it is not authenticated end-user identity. CARTRIDGE_TOOL_OBSERVATIONS=1 opts in alongside existing CARTRIDGE_DIAGNOSTICS; host-owned CARTRIDGE_TOOL_ACTORS is a bounded JSON map (<=128 sources, names <=128 bytes) assigning actor enum agent/ui/background and activity deliberate/read/poll. Invalid/unconfigured entries remain unknown. Request args/context/metadata cannot set actor or source. Operation describe is discovery; cancel is a cancellation request, never proof a dispatched effect stopped. Other operations preserve unknown activity unless the host map supplies it. Native host trust remains the existing boundary; arbitrary Lua/direct socket calls outside this branch are explicitly not covered.

Emit v1 metadata-only tool_attempt and tool_completion records through existing bounded diagnostics. Per-call observation ID uses host minted identity independent of caller call IDs. Fields: source, actor, activity, tool, bounded operation enum, provider_generation, descriptor_revision, stage, dispatched, outcome, completion_known, elapsed_ms, response_bytes. Source generation combines per-runtime identity and resolved Service version; absent resolution/version stays null. attempt is emitted before resolution/dispatch, with null completion/duration/size. Capture actual service generation inside Service::call after its existing reload read gate is held, using scoped task-local observation state. This prevents a lookup/reload race from assigning the wrong generation; unversioned invocation remains unknown. Initial attempt precedes lookup; completion carries actual dispatch revision. Report lookup failure separately. Successful tool envelope requires content string/error boolean; error envelopes differ from transport or malformed response uncertainty. Exact interrupted-outcome-unknown response preserves unknown effect completion. Successful cancel only records acknowledgement of the request. RAII drop records interrupted with completion unknown; never replay.

Hash successful describe content with existing sha2 0.10 and cache last successful observation by exact provider generation and tool key, at most128 entries; malformed/oversized (>64KiB) descriptors remain unknown. Every successful changed describe updates its SHA even within one generation. Cache misses/evictions never manufacture revisions. Record the revision actually observed for each subsequent attempt, not request-supplied metadata; projection calls it last_observed_descriptor, not necessarily current. Coordinator refreshes both shared/runtime Cargo lockfiles; this source commit does not include their unrelated changes.

Use existing diagnostic byte cap/one rotation. Observation fields contain no args/results/messages/text/error detail; response_bytes is serialized JSON size, not tokens/billing. Failures and poisoned/full sinks lose evidence explicitly without altering returned tool result. Guard allocation/cache remain bounded; no async observer RPC. Source file write latency is inherited from existing diagnostics and is not advertised as zero overhead.

## Acceptance

- [x] Real native child fixture makes mixed successful/error/describe/cancel/unknown-origin calls and metadata spoof attempts through actual runtime dispatch, proving observations and unchanged results.
- [x] Actual describe change within same generation and provider replacement/eviction give correct revision or unknown; partial/invalid response and dropped live invocation retain uncertainty.
- [x] Disabled/failed/capped diagnostic sink and secret-bearing fixtures prove no tool failure or body leakage; rotation/cache limits hold.

## Verify and Proof

```sh
cd /Users/feb/dev/cartridge/cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/sessions-mapping" just test runtime
```

```sh
cd /Users/feb/dev/cartridge/cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/sessions-mapping" cargo build --manifest-path .cartridge/workspace/Cargo.toml -p cartridge --bin cartridge
CARTRIDGE_TEST_BIN="$PWD/target/sessions-mapping/debug/cartridge" bun test ./.cartridge/tests/integration/tool-observations.test.ts
```

Also run public just check runtime. All fixtures disposable. Existing sink history is retained; deployment defaults remain disabled. No new service or transcript data is created.
