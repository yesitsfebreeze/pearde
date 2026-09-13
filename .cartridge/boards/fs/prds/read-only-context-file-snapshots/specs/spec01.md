---
complexity: medium
footprint: ["cartridge.json","src/main.rs","src/context.rs",".cartridge/tests/unit/context.rs",".cartridge/tests/integration/context.test.ts",".cartridge/docs/context.md","Cargo.toml","src/files.rs","src/service.rs"]
---

# Native exact file snapshots without tool observation

Measured baseline6a8dec3: actual SDK tool.read returns `1:first\r\n2:second\r\n` without a full source revision. It records an in-memory invocation observation but does not call sessions touch; only mutations do. Native fs.context has no handler. Preserve all existing tool behavior and schemas.

Add optional native provided key `fs.context` with `{op:"read",cwd:<trusted absolute owner root>,path:<exact normal relative path>,expected_revision?:<64 lowercase hex>,deadline_ms?:500}`. This is a trusted native operation, never a model tool input and never a capability activation request. No session/run/call is inferred and no observe/touch callback runs. Unknown fields, offset/line limits, alternate operations, invalid path or revision fail before source access. Bounds: cwd4096 bytes, path512 bytes, deadline1..2000ms. The caller resolves enabled composition owner roots; FS confines one exact path to that root and does not choose owners.

Return `{status:"available",path,revision,revision_kind:"source_bytes",text,bytes}` only for a complete <=8192-byte UTF-8 regular file. Preserve exact CRLF, BOM and trailing newline in text and hash its exact bytes. No partial body, numbered rendering, silent truncation or altered digest. A mismatching expected_revision returns `{status:"changed"}` without body/hash. Missing/nonregular/inaccessible/binary/NUL/oversized sources return bounded unavailable with static reason; no raw OS paths/errors beyond the requested relative path. Invalid input is a static error.

Canonicalize trusted root; reject absolute/parent/current/empty path components and internal symlinks. The native boundary also refuses typed `.cartridge/memos` and `.cartridge/documents` sources: reject ASCII case aliases lexically, then compare stable directory identities along the canonical target ancestry with the owner’s actual reserved directories before reading. This identity check covers filesystem case aliases that string prefix checks miss; inability to establish confinement fails unavailable. Walk at most64 path components. The trusted root itself cannot be inside a typed reserved record namespace. Pin one regular file handle, compare canonical path and file identity before/after bounded read, and refuse observed replacement/escape. Read at most8193 bytes and check metadata/caps before allocation; oversized input never returns content. Handle successful read as an observation of one open file, not a cross-file transaction. Source-byte revision identifies bytes, not historical inode/root identity: replacing a file with identical bytes keeps its source revision. Arbitrary hostile filesystem writers that deliberately race and restore all checked identities are outside this local snapshot boundary; do not claim an OS capability sandbox.

Use a blocking read worker under one native deadline with cooperative cancellation checks before opening and after I/O. Timeout returns explicit timeout; dropping await requests cancellation and never claims the blocking worker was joined. No shell, subprocess, directory walk, writes, mutation authority, stored observations or retries. The response wrapper must fit64KiB even under JSON escaping.

## Acceptance

- [x] Real native SDK preserves exact LF/CRLF/BOM/trailing-newline snapshots and SHA; source edit detects stale expected revision without replacement payload.
- [x] Missing, nonregular, symlink/escape, invalid UTF-8/NUL,8192/8193-byte boundary, replacement, typed-record case aliases (including a real case-insensitive lookup when supported) and timeout fixtures produce bounded named outcomes without writes or touch calls.
- [x] Existing FS public tests/check and new native fixtures pass; model tools have no fs.context operation.

## Verify and proof

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just test fs
just check fs
bun test ../fs.ctg/.cartridge/tests/integration/context.test.ts
```

Root owns composition grant changes and collection. The operation is an available native primitive only; caller allowlists and shared-context attribution belong to the dependent memo/Landscape leaves.
