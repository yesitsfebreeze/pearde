---
complexity: medium
footprint: ["src/context.rs","src/main.rs","src/service.rs","src/inventory.rs",".cartridge/tests/integration/inventory.test.ts",".cartridge/docs/inventory.md","src/source_search.rs","src/document.rs",".cartridge/tests/unit/source_search.rs"]
---

# Native memo adapter for the shared bounded inventory

Baseline 3251566: actual memo SDK request op=landscape, version=2, action=summary rejects unknown action before any host callback. Retained baseline probe/JSON precede this spec. Implement only after the reviewed Landscape inventory child is collected. Existing model tool schema and unversioned native op=landscape continue unchanged; do not create another collector or path selector.

Native request `{op:"landscape",version:2,action:"summary",cwd:<trusted absolute dir>,timeout_ms?:2000}` captures and publishes one shared-library Snapshot, returning its default <=16-KiB summary. Native `{op:"landscape",version:2,action:"inventory",cwd,snapshot:<token>,owner?:<exact id>,cursor?:<opaque>,limit?:100}` reads that snapshot only. Unknown fields/actions/versions and invalid cwd, timeout 1..5000, limit 1..256 or oversize token/filter/cursor reject before host work. Version 2 is additive and the default action within version 2 is summary. No caller roots, tool grants or presentation text are accepted.

One Service cache holds one immutable Snapshot, bounded by the library's 128-owner/100,000-path/16-MiB retained path limits. Use the existing trusted native host; summary calls host.landscape exactly once and passes the raw composition to canonical inventory::capture. One absolute deadline starts before discovery and includes host response and all library scans. Missing host/discovery failure/timeout yields static unavailable/timeout, with no raw backend errors and no replacement of last usable snapshot. Host decoding may allocate before the adapter can enforce library limits; document that boundary. No tool descriptors, injections, record survey, inference, document content reads, provider activation or persistence.

Each summary obtains a monotonic request ticket before awaiting discovery. Only the newest started capture may publish; an older capture completing later returns superseded and cannot replace cache. A failed newer request preserves the previously published snapshot, but an older in-flight capture may not publish afterward. Publishing happens under a short cache mutex after capture; never hold it across await. Inventory clones the frozen Arc under that mutex, verifies requested token, then library pages it without any fresh host/FS calls. Successful new publication invalidates earlier tokens/cursors explicitly, including an identical recapture. A service restart has a different capture token and empty cache. Concurrent inventory already holding an old immutable snapshot may finish consistently on its own token; it never combines generations. Clients requesting after replacement receive stale_snapshot and must explicitly refresh. Snapshot tokens are not authorization credentials; exposure is limited to this native service instance's configured host composition.

All successes serialize <=16 KiB including wrapper fields; return library response directly to avoid unbudgeted envelopes. All static failure responses are bounded. Source revision is distinct from capture token. Omitted and unavailable counts stay honest; partial inventory does not become a successful complete inventory. No source/config/history writes and no automatic retries.

## Acceptance

- [x] Real SDK fixture with 10,000 tracked paths: native v2 default summary <=16 KiB with omissions; pages reconstruct exact owner/path pairs and <=16 KiB each. One host snapshot call, none while paging, no tool/record callbacks or writes.
- [x] Refresh/generation change, identical refresh, changed filter, malformed/stale cursor, missing cache and restarted process refuse explicitly. Concurrent slow-old/fast-new capture cannot overwrite newest; failed refresh preserves published snapshot.
- [x] Missing/failed host, common deadline, failed owner plus usable owner, and bounded request failures produce named outcomes. Disabled contributors never scanned. Unversioned native and model landscape contracts remain accepted.

## Verify and proof

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just test memo
just check memo
bun test ../memo.ctg/.cartridge/tests/integration/inventory.test.ts
bun test ../memo.ctg/.cartridge/tests/integration/context.test.ts
```

Proof binds exact memo and Landscape source revisions and reports real native assertions. Coordinator collects and refreshes affected memo facade/types/template receipts. Source footprint excludes document identity, projection and validation modules. No runtime composition edits.
