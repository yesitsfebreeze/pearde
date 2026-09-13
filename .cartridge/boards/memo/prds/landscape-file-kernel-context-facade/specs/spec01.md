---
complexity: medium
footprint:
- src/context.rs
- src/service.rs
- .cartridge/tests/integration/file-kernel-context.test.ts
- .cartridge/docs/context.md
---

# Add explicitly enabled file/kernel sources to native shared context

Baseline45d5a54 native prepare rejects files/kernel fields before callbacks. Reuse the existing prepare/read operation, canonical collector, exact reference handling, and whole-response cap. Existing documents/memory defaults and inventory API remain unchanged. This owner does not implement another file reader, selector, persistence store or cursor API.

Add trusted memo config `context_files: [{owner,path}]`, default empty, at most128 exact public declarations validated by the shared adapter. Config explicitly authorizes surfacing those file bodies. It cannot select private typed memo/document records, including case aliases: configuration rejects reserved spellings case-insensitively, and native FS checks actual reserved-directory identity under the canonical owner boundary. It cannot select arbitrary caller roots or model-supplied paths. Native prepare adds optional files/kernel booleans default false. Kernel source uses host.landscape only; file source requires already granted fs.context plus a valid allowlist. No native required injection is added: optional absent FS leaves other sources useful. Root owns the minimal optional composition grant and proves omission remains loadable.

When enabled, discovery and all owner callbacks execute inside canonical Tasks under the original shared absolute deadline. Share at most one host.landscape request per preparation between files and kernel. Resolve each configured file owner uniquely from this exact enabled composition: absolute canonical root, active state, and no ambiguous same-ID mapping. Disabled/missing owners are never opened. Pass trusted exact owner root/path to fs.context read; remaining native deadline is clamped within the parent's remaining time, and the parent timeout still covers the complete callback. Query nominations and evidence conversion use Landscape's reviewed adapter. No descriptor calls, session touches, file observation grants, tool dispatch, provider activation or inference.

Native read routes exact kind=file/kernel References through the same adapters. File read requires current explicit allowlist membership, current active owner root and granted fs.context, then sends expected source SHA for exact readback. Kernel read obtains one current host snapshot and checks the exact projected owner entry. Validate all Reference fields, including kind/owner/id/revision_kind. Current logical owner/allowlist validity, source bytes and kernel generation determine readback. Removed permission/owner or source returns unavailable; changed full file bytes or projected kernel generation returns changed. File references do not bind historical root/inode/generation: a replacement root with the same currently permitted owner/path and identical bytes returns available with the same reference. Test this explicitly. No guessed semantic search or substitution. Map errors to static bounded states and obey response max_bytes including wrapper, preserving existing read behavior for document/memory.

## Acceptance

- [x] Real SDK composition runs actual memo and FS binaries: one query yields exact configured file bytes, distinct kernel capability rows and enabled document/memory evidence, sharing canonical Prepared bounds.
- [x] Same-named files across owners, CRLF, file edit/removal, typed-record case aliases, disallowed path/config change, identical-byte owner-root replacement, inactive owner and kernel generation change preserve attribution and exact readback; unrelated references remain stable.
- [x] Omitted FS grant or disabled flags never activate providers; delayed discovery/read obeys one deadline; static partial outcomes preserve other sources and no writes/observations occur.
- [x] Native context/inventory and model surface compatibility gates pass. Source config is trusted host data, never request-supplied allowlists or roots.

## Verify and proof

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just test memo
just check memo
bun test ../memo.ctg/.cartridge/tests/integration/file-kernel-context.test.ts
bun test ../memo.ctg/.cartridge/tests/integration/context.test.ts
bun test ../memo.ctg/.cartridge/tests/integration/inventory.test.ts
cargo build -p cartridge
printf '%s  %s\n' 'b277295be8e149b5a7480236642ae52f9fff4b68508df297eba474ea33c7062a' '/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memo/prds/landscape-file-kernel-context-facade/real-host-proof.py' | shasum -a 256 -c -
python3 /Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/memo/prds/landscape-file-kernel-context-facade/real-host-proof.py
```

Root collects dependency receipts before source release and owns shared PRD/composition changes. Session, terminal and router context remain named required follow-up leaves in the parent; this leaf does not claim their implementation or scrape their broad state APIs.

Real host refinement: the preserved actual profile baseline failed when FS manifest declarations omitted fs.context. Additive owner manifest declaration d4a4239 makes the same explicit FS+grant profile pass with exact file/kernel evidence. The omission fixture removes both FS and its grant, leaving Memo loadable with files Absent and kernel Available. A missing provider while retaining its exact dependency grant is not an optional operation state. No default eager provider/profile changes are required. The pinned proof script builds on the preceding actual owner SDK binary builds and the runtime build above.
