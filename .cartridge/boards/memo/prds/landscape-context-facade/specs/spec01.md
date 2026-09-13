---
complexity: medium
footprint:
- src/inventory.rs
- src/main.rs
- src/service.rs
- src/context.rs
- .cartridge/tests/integration/context.test.ts
- .cartridge/docs/context.md
---

# Native memo exposes the canonical context snapshot

Measured SDK baseline at76800a2 rejects native context requests in the existing
Input parser before any host calls; baseline.json retains the exact reply/probe.
Add one native operation; model tool schema and legacy record behavior stay intact.
No new selector, grants, provider configuration, source registry or cache is added.

## API and source authority

Native `memo {op:"context",cwd,action:"prepare",query,documents:true,memory:false,limits}`
returns serialized Landscape Prepared directly. Defaults enable documents and leave
memory disabled; query is required, nonempty, at most1024 UTF8 bytes and no NUL.
Only known fields are accepted. Shared Limits defaults/validation apply (deadline
1..2000ms,rows1..64,bytes4096..65536). Cwd must be absolute, bounded and no NUL;
only the trusted native caller supplies it. Owner roots come only from host.cartridges
and the existing document owner resolver; requests never inject filesystem roots.

Create exactly documents and memory Tasks and call canonical context::collect once.
No source call precedes collect: document host registry/index/read and memory
injection discovery/query/get are all inside its futures under its single absolute
deadline. Disabled sources are not polled. Missing memory injection or host is Absent;
failed discovery/calls is Unavailable; no candidates is Empty; dropped pending work
is Timeout; mixed valid/error/truncated source evidence is Partial. Missing document
directory and an empty metadata match both use the existing index's Empty result;
no second directory/owner resolver is introduced. Host SDK replies are already decoded Values: adapter caps bound inspected and retained
data, not arbitrary host/backend allocation. Errors expose status only, never
raw private metadata/backend text. Late work cannot publish a replacement snapshot;
timeout does not assert a blocking filesystem worker or remote service stopped.

Documents reuse native document index query in cwd owner's .cartridge/documents,
then inspect at most limits.max_rows existing index slots in deterministic order.
Read those exact owner/path identities with docs projection and index expected_revision.
Never scan extra rows to replace stale/invalid ones. Private documents are omitted by
index or refused by projection. Retain only public evidence text and attribution;
strip metadata, command blocks, callable descriptions and arbitrary extension fields.
No tool.* descriptors are queried. Document prose remains untrusted even if it
contains instruction-like text. References use owner from canonical document identity,
kind document, canonical identity id, projection_revision and observed_projection.
Source is canonical identity, reason is metadata match plus bounded docs projection.
Rows over8192 text bytes or invalid common-contract fields are omitted with Partial;
budget retained rows by shared max_bytes and stop with explicit truncation. Truncated
or incomplete document projections retain useful public text with Partial status.
Existing document read caps bound upstream work; shared selector owns global dedupe,
reference conflicts, final row and serialized byte budgets.

Memory uses landscape::memory::contribute(query,limits,callback), bound only to
host.call("memory",args), after host.injections confirms that exact key. Never call
meta, tools, model, reload, write or activation APIs. Memory's compact get/query
bounds and observed revision semantics remain owned by its contributor.

## Exact readback

Native `memo {op:"context",cwd,action:"read",reference,limits}` validates the exact
shared Reference and starts one deadline before source discovery. It returns
`{status:"available",evidence}` for the same observed projection, or named
`changed`, `unavailable`, `timeout`, `invalid_reference` without replacement query.
Document readback validates every Reference field, including revision_kind exactly
observed_projection, lowercase SHA256, owner/kind/id agreement and contained canonical path,
uses exact docs projection and compares derived revision; private/missing is
Unavailable, changed bytes/linked closure is Changed. Memory delegates exact get
and revision comparison to memory::read with the fixed memory callback. No semantic
query or context prepare occurs during readback. Unknown source kinds are refused.
Readback accepts no query/source-toggle fields. Prepare accepts no reference.
No retained snapshot/cache means process restart introduces no hidden stale state.
The serialized readback status/evidence wrapper must fit max_bytes. Oversized exact
evidence returns unavailable with a fixed capacity reason; never trim evidence
while retaining its old digest or leak backend error text.

## Acceptance

- [x] Actual SDK prepare joins public document and Memory evidence in one canonical snapshot and preserves exact source/reference attribution without tool/inference calls.
- [x] Disabled, absent, empty, unavailable, partial and timeout cases are named; delayed discovery and read calls share one deadline and retain useful other-source evidence.
- [x] Exact document/Memory readback succeeds unchanged, reports changed/missing/private/invalid references, and issues no semantic replacement query.
- [x] Invalid/oversized requests, private metadata and callable extras remain excluded; source/row/output budgets hold and files/provider state are unchanged.

## Verify and proof

Run actual SDK integration with an instrumented synthetic host and temporary exact
Markdown fixtures. Capture every host callback; include memory success/failure/hang,
slow cartridges discovery, delayed exact get, stale document index, private prose,
source field extras, metadata-only docs match, no matching docs and literal code.
Assert callback allowlist/counters and exact filesystem before/after hashes; no
semantic queries on readback, no retries/activation/inference/transcript mutation.
Public gates from runtime: just test memo; just check memo; just test landscape;
just check landscape, with cleared Rust wrappers and target/tool-result-contract.
Run bun test ./.cartridge/tests/integration/context.test.ts in memo. Preserve prior
baseline/review digests; coordinator refreshes overlapping existing receipts.

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just test memo
just check memo
just test landscape
just check landscape
cd ../memo.ctg
bun test ./.cartridge/tests/integration/context.test.ts
```
