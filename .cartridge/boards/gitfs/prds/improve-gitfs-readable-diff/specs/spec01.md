---
complexity: medium
footprint: ["src/push.rs","src/service.rs","src/store.rs","src/tool_result.rs","src/inspection.rs",".cartridge/tests/unit/tool_result.rs",".cartridge/tests/integration/tool-result.test.ts",".cartridge/docs/inspection.md","Cargo.toml","src/provenance.rs",".cartridge/tests/unit/provenance.rs",".cartridge/tests/integration/change-provenance.test.ts",".cartridge/docs/change-provenance.md"]
---

# spec01 — Inspect base, overlay and disk without a mutation grant

`gitfs diff {path, offset?, limit?, expected_revision?}` returns pinned base and
session commit IDs, each side's content revision/mode/size, content-difference
flags and conservative three-way conflict status. Render base-to-overlay and
base-to-disk unified replacement hunks with a common prefix/suffix. Binary
content returns metadata plus an explicit binary marker. An absent side has
null revision. Symlink disk escapes and directories fail explicitly.

Default output is 16 KiB, maximum 64 KiB of UTF-8 patch text. Return next_offset
and a comparison revision; continuing requires that revision and rejects any
changed side. Cap source reads at 8 MiB per side and reject oversized sources
before generating a patch. Inspection is a read-time comparison, not a live lock
or a promise that a future materialization cannot conflict.

Read, ls and diff attach without creating a store directory or private index.
List propagates backend failures instead of claiming an empty success. Keep
write/edit/materialize/snapshot semantics and wire serialization unchanged.
The policy owner adds diff to its known gitfs operations; no default allow is
introduced. Verify through real MCP with policy allowing read/ls/diff and denying
write/edit/snapshot/materialize, retaining unrelated refs, staged bytes and disk.

## Acceptance

- [x] Native baseline probes pass: diff recognized; an untouched repo is inspected without state creation.
- [x] Real MCP with actual policy permits list/read/diff and denies every mutation; refs, real/private indexes and worktree bytes remain identical.
- [x] An external edit yields distinct base/overlay/disk revisions and conflict; large patch pages reconstruct exactly, and changed content rejects stale continuation.
- [x] Public gitfs and policy gates pass; existing GitFS and policy collection receipts are reverified against shared source changes.

## Verify and Proof

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just test gitfs
```

Also run public `just check gitfs` and `just test policy`. No remote push, repair,
materialization or destructive operation is part of the proof.
