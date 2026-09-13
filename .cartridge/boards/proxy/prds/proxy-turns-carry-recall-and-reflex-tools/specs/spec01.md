---
complexity: high
footprint:
- Cargo.toml
- cartridge.json
- src/main.rs
- src/service.rs
- src/context.rs
- src/wire.rs
- src/streaming.rs
- src/usage.rs
- .cartridge/tests/unit/tests.rs
- .cartridge/tests/unit/context.rs
- .cartridge/tests/integration/recall.test.ts
- .cartridge/docs/context.md
---

# Proxy adapts one bounded sourced snapshot as untrusted context

Replace the direct memory query/system-string concatenation with the canonical
native memo context facade. Landscape owns selection/projection identities; memo
owns optional source calls. Proxy owns client wire adaptation, request budgets,
trusted profile grants and authenticated diagnostics. No second selector, memory
writer, model loop, ranking service or harness implementation belongs here.

The measured baseline at4395941 shows all three native wires elevate memory text
into system instructions, omit exact ID/source and reject a valid request before
routing when an optional memory reply is large. Native memory query/get envelopes
and the shared contributor/facade contracts have separate owner proofs.

## Preparation and authority

New profile configuration context_recall defaults true, preserving existing recall
intent; context_limits defaults deadline_ms200/max_rows5/max_bytes16384 and uses
shared Limits validation (1..2000ms,1..64rows,4096..65536bytes). The profile alone
chooses context behavior and cwd. No caller headers, metadata, supplied snapshots
or diagnostic IDs grant authority or select a different source/workspace.

After forming the first valid mandatory harness/tools envelope, obtain the latest
user text through the existing wire parser. Empty text skips preparation; more than
1024 UTF8 bytes or a NUL skips optional recall with a fixed degraded reason, without
trimming caller history or changing the query into another query. Run one bounded
native call `memo {op:context,action:prepare,cwd:<trusted profile cwd>,query,
documents:false,memory:true,limits}`. Documents stay with existing harness ownership
so this slice does not double-insert its trusted memo composition. Replace proxy's
native memory dependency with memo; the memo facade owns optional memory reachability.
The coordinator owns the shared Cargo lock dependency update and adds the exact
memory grant to memo in the shipped profile, which already declares Memory. A
valid missing-Memory composition omits both its provider and memo grant; proxy
itself no longer requires Memory. A declared provider that fails during startup
still follows existing runtime dependency activation semantics. This leaf does
not invent optional dependency loading; prove per-call failure after activation
and document the declared-provider startup limitation.

The first mandatory outgoing envelope must already meet its existing resource
budget. Reserve at least twice the chosen context byte cap plus1024 bytes for
native user-message encoding; choose a smaller validated cap from remaining room
when possible, otherwise skip optional preparation. This is a conservative
reservation, followed by exact serialized outgoing-byte validation. Failure of
optional context never rejects an otherwise valid mandatory envelope.

Bound received Prepared serialization with a capped writer before cloning or
retaining. Deserialize only the typed known contract, require the known schema,
matching requested limits, expected documents/memory source names, memory evidence
references, valid digest shapes, canonical revision recomputation and total output
within the requested cap. Unknown schema, malformed/private extension fields or
invalid digests degrade to no context. Preserve the original immutable Prepared
revision; do not trim its rows and keep a now-invalid digest.

The one Prepared value is reused through hidden model rounds, injected once into
each fresh outgoing clone, never accumulated in client history or continuation
storage. On any later round where that whole snapshot cannot fit, omit it for that
round, record the capacity degradation, and forward the valid mandatory envelope.
Source failures, timeout or malformed output likewise preserve provider/error/
streaming semantics. The caller's overall deadline still cancels the request;
optional context has its shorter bounded deadline and never retries or activates a
provider. Dropping preparation prevents later local dispatch without asserting a
remote cancellation acknowledgement.

## Native wire preservation

Encode rows with IDs, source, projection revision and selection reason as JSON data
inside a separate user-role message labelled retrieved untrusted evidence. Never
place evidence in Chat system/developer messages, Anthropic system, or Responses
instructions; hostile closing tags remain quoted data. Insert before the first
conversation message after leading Chat system/developer messages, or before the
native Anthropic/Responses conversation items. Preserve each original item and its
order, including images, reasoning items, complete tool-call/result groups and
latest user constraints. Responses string input becomes an equivalent original
user item preceded by the evidence user item. No invented tool result is used.

Existing caller tools and exact profile-granted descriptors remain unchanged and
in the same order. Preparation does not rank away required client tools, add host
capabilities, or dispatch any tool. Existing policy/invocation identity and mixed
private/caller tool behavior remain the only execution boundary.

## Bounded inspection without inference

context_diagnostics defaults false. When enabled, a separate archive retains at
most32 active/finished records (default16), with a TTL of1..300 seconds, default60 seconds
from admission that never extends, and at most the configured64KiB Prepared per
record. Profiles validate these caps. Capacity/expiry evicts whole records; handles
carry only an ID/archive reference and cannot resurrect evicted records. Archive
retention is bounded globally; per-request working data remains bounded by limits.
No transcript, raw query, caller messages, tools/arguments/results, raw errors,
authentication secret or profile config is retained. Public prepared evidence and
its original source attribution are the only retained content.

IDs are random opaque proxy_context_<32 lowercase hex>. Every record binds the
existing immutable Principal (Native, authenticated default key, or configured
named key); caller metadata cannot override it. Check ownership before exposing
state/content. Disabled, unknown, wrong-principal, expired, evicted and restarted
IDs return the same unavailable response. A shared HTTP key remains one principal.

Allocate the diagnostic handle before polling an SSE body and finalize its request
state on completion/failure/drop, including a pre-poll disconnect with no dispatch.
Prepare stores the immutable snapshot once, plus fixed status/reason and bounded
applied/omitted-round counters. Finalize before terminal SSE output. Enabled JSON
and all three native SSE formats carry one additive cartridge_context {id} terminal
metadata item, and HTTP exposes x-cartridge-context-id early. Disabled diagnostics
preserve existing JSON/SSE shapes. Fixed structured degraded observations are also
written to stderr without query/evidence/error bodies, so optional failures remain
observable with diagnostics disabled.

Native `proxy {op:context,action:read,id}` and authenticated HTTP GET
/v1/cartridge/contexts/<id> return that frozen record without any source or model
call. Native `proxy {op:context,action:prepare,query}` and authenticated HTTP POST
/v1/cartridge/context {query} explicitly prepare/retain a snapshot under configured
limits without session/tool/harness/router calls. These inspection operations require
diagnostics enabled, reject unknown fields and caller cwd/source/limit overrides,
and reuse the same preparation validator. Read never triggers re-preparation;
restart/eviction requires an explicit fresh prepare. Request-supplied diagnostic
IDs never select context or authorize an inference request.

## Acceptance

- [x] All three JSON/SSE wires receive one sourced memory snapshot as user data; exact IDs/revisions/source remain, privileged instructions exclude evidence, and hostile text cannot alter role structure.
- [x] Missing/failed/malformed/timed-out/oversized context forwards the valid mandatory envelope; exact budget checks, later-round omission and cancellation preserve existing client/provider semantics without retry or tool dispatch.
- [x] Caller history/images/reasoning/tool groups and tool definitions remain intact; fixed profile grants, policy decisions and client continuation authority still govern execution.
- [x] Exact archived snapshots and explicit prepare-only inspection make no inference call; authenticated principals cannot read each other's records, including spoofed identity metadata and expired/evicted/restart cases.
- [x] Archive and prepared byte/count/deadline limits include identity/provenance, active records and cancellation; diagnostics off preserves native response shapes while static degraded observations remain visible.
- [x] Public proxy tests/check and real composed recall fixture pass against collected facade/contributor revisions; existing usage/continuation/trace behavior remains compatible.

## Verify and Proof

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/proxy-context" just test proxy
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/proxy-context" just check proxy
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/proxy-context" just build proxy
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/proxy-context" just build memo
cd ../proxy.ctg
CARTRIDGE_WRAPPER=/Users/feb/dev/cartridge/cartridge.ctg/target/debug/cartridge MEMORY_BINARY=/Users/feb/dev/cartridge/cartridge.ctg/target/debug/memory_cartridge MEMO_BINARY=/Users/feb/dev/cartridge/cartridge.ctg/target/proxy-context/debug/memo_cartridge PROXY_BINARY=/Users/feb/dev/cartridge/cartridge.ctg/target/proxy-context/debug/proxy bun test ./.cartridge/tests/integration/recall.test.ts
```

Use instrumented native callbacks and authenticated loopback HTTP fixtures for all
three wires. Include caller tool-call/result batches, images/reasoning, private
sentinels, long optional output, tight mandatory budget, a delayed memory source,
disconnect before polling and during preparation, and principal archive boundaries.
The composed fixture uses real proxy/memo/memory SDK processes, temporary files and
local embeddings; a synthetic router echoes the actual user data projection without
an external model. Also run a real composition with no Memory provider or memo
memory grant, proving native proxy/memo startup and successful forwarding. Fingerprint existing runtime/memory executables rather than
claiming an unbuilt source revision. Source remains unchanged until the facade
receipt is current and independent round3 review passes. Coordinator refreshes
older proxy receipts whose owner footprints overlap this implementation.
