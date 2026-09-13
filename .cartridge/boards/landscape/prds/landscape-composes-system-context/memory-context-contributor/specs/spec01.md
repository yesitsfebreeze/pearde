---
complexity: medium
footprint:
- src/lib.rs
- src/memory.rs
- .cartridge/tests/unit/src/memory/tests.rs
- .cartridge/docs/memory-context.md
---

# Memory contributes exact observed evidence to the shared context

This leaf implements the memory producer for the canonical context-contributor
contract. It adds no second context selector, memory store, facade operation,
profile grant, tool execution or inference loop. The memo-owned facade leaf will
bind its host callback to the existing memory service; the proxy adapter consumes
that facade after its prerequisites complete.

The measured baseline is the existing Landscape library at `408de6c`: a query
finds the two fixture memo/tool candidates but no memory-only fact, and no memory
availability observation exists. See baseline.json and baseline-log.txt. The
memory wire inspected at `09bfaae` supports ranked query and exact-ID compact
readback, with source objects and visible truncation, but no engine revision.

## Contract

Use the shared context types and absolute-deadline collector. The producer accepts
a validated bounded query, shared limits and a callback bound to memory; the
callback receives operation arguments only, never a capability key. A disabled or
absent source is represented by the collector without polling this producer.

The API is `memory::contribute(query, limits, call) -> Contribution`; the callback
returns a future of `Result<Value, String>`. Shared Limits are deadline_ms 1..2000,
max_rows 1..64, max_bytes 4096..65536; the outer canonical collector owns timeout.

Perform exactly one semantic `query` with `k` bounded by the configured row count
and the shared hard maximum. Inspect only that many ranked candidate slots, dedupe
exact IDs, require active status and bounded source metadata, and discard query
preview text and edges. Never scan arbitrary extra rows to replace invalid ones.
Hydrate at most that many nominated IDs, using only
`get {id:<exact returned ID>,compact:true,edge_limit:1}`. A returned different ID,
source mismatch, missing/deleted entity, explicitly expired entity or malformed
reply is named partial/unavailable evidence, never a replacement semantic query.
The current engine accepts prefixes; equality of the returned full ID is mandatory.

Normalize source provenance as a canonical JSON string from the existing object
fields scheme/object_id/section/url. IDs are at most 256 bytes; each source field
is at most 1024 bytes and the serialized source at most 4096 bytes. Compact text
is at most 4096 bytes, preserving the engine truncation marker. Explicit private
query/get rows are discarded before public validation or evidence retention. Bound IDs and every provenance
field before cloning them, and bound the complete serialized evidence row before
retention. Share the configured total byte allowance across all retained memory
rows. Stop hydration when count or byte allowance is exhausted; mark truncation
rather than silently implying complete selection. Do not retain raw backend
errors, edges, confidence internals, arbitrary extension fields or preview bodies.

Each row uses owner `memory`, kind `memory`, the exact entity ID, source provenance,
and compact readback text as untrusted data. Revision kind is
`observed_projection`: SHA-256 of the canonical normalized ID/source/text projection
including whether text was truncated. This identifies the exact observed evidence;
it is not an engine transaction, freshness guarantee or digest of unseen full text.
Selection reason states ranked memory selection and compact/truncated hydration.
Identical replies produce identical references and prepared snapshot digest.

Expose exact reference readback through the same callback: only a get for the
reference ID, followed by ID/source/projection-digest checks. Missing/changed
references return a typed unavailable/changed result with no semantic fallback.
Evidence content is never interpreted as instructions, authority or callable tool
metadata. The collector owns overall deadline/cancellation and global selection;
a timeout drops in-flight read work and returns its named partial status without
claiming the memory server acknowledged cancellation.

## Boundaries retained honestly

The current ranked memory transport includes 500-character text and bounded edge
previews. This leaf discards those previews before context selection; it does not
claim the transport is metadata-only. The separate one-search acceptance still
requires a memory-owned metadata projection. Native compact get exposes at most
500 characters plus text_truncated; full-text hydration is not claimed. Limits
bound inspected/retained context after the host has decoded a reply, not arbitrary
backend allocation. Query and get are separate observations, not an atomic engine
snapshot; active status comes from the query and explicit expiry from get.

## Acceptance

- [x] A memory-only fact joins memo/tool evidence through one canonical prepared result, carries exact ID/source/projection revision, and exact readback never semantically requeries.
- [x] Disabled/absent/empty/unavailable/malformed/timeout and missing or changed exact evidence are distinguishable; optional memory failure leaves useful other contributors and returns within the one deadline.
- [x] Configured candidate count and total retained bytes bound hydration; oversized IDs/source/text, duplicate IDs, source mismatch, returned prefix matches, and visible compact truncation have explicit fixture evidence.
- [x] No model/tool/write callback is issued; private candidates remain subject to shared filtering; repeated identical snapshots and source reads give the same prepared digest.
- [x] Complete Landscape tests and public check pass at the integrated shared-contract revision; memo consumer tests remain compatible.

## Verify and Proof

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/landscape-memory" just test landscape
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/landscape-memory" just check landscape
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/landscape-memory" just test memo
```

Fixtures use an instrumented fixed-capability callback with realistic memory
query/get envelopes. They compare calls and returned snapshots, including one
successful contributor alongside hanging/failed memory; exact callback counters
must prove no hidden query retry, inference or write. Product source is unchanged
until the prerequisite contract is collected, this spec receives independent
review, and shared-file registration ownership is coordinated.
