# Read declared source edges

Trusted native consumers can call the existing `prd` capability with
`{"op":"source_declarations","board":"root","deadline_ms":500}`. `board` defaults
to the configured board and accepts a normal relative path under the configured
`.cartridge/boards`. Caller-provided root/config/cwd overrides are rejected.
`tool.prd` does not expose this operation. TypeScript consumers can import
`sourceDeclarations(boardsRoot, relativeBoard, deadlineMs)` from `src/records.ts`.

An available response contains `schema: "cartridge-source-declarations/v1"`,
`status: "available"`, the canonical selected `root`, a SHA256 `revision` over
exact settings bytes, and alias-sorted `children` with `name`, absolute normalized
`root`, and `kind: "board"`. The owner uses the same frontmatter and member
interpretation as the strict planner. It reads no record bodies and does not
require descendants to exist or have valid boards. A missing declared child is
still an edge. The strict `members()` and `scan()` APIs keep their existing
missing-board and cycle errors.

Failures contain only `schema` and `status`: `unavailable` for inaccessible
sources, `malformed` for invalid input/declarations or escapes, `capacity` for
limits, and `timeout` for deadline exhaustion. No OS diagnostics or record content
are exposed. Neither success nor failure starts a CLI subprocess, acquires a
planning lock, calls Memory, publishes a PRD event, spills an oversized response,
or writes a journal. Existing service startup recovery is separate from this
operation.

Limits are 512 UTF8 bytes/32 components for the board selector, 64 KiB for the
entire settings file, 64 edges, 64 bytes per alias, 4096 bytes per location and
absolute target, and 256 KiB for the entire response. Settings must be a regular
file, never a symlink; nonblocking open also refuses a replaced FIFO without waiting for a writer. The bounded file descriptor read detects size growth. Member iteration stops at the edge cap before expanding repeated YAML alias maps.
Existing symlink ancestors are resolved and confined both to the configured boards
scope and the selected board's parent. Invalid UTF8 is refused. BOM and CRLF bytes
are retained in the settings hash.

The 1–2000 ms deadline covers filesystem checks, reading and normalization. It
bounds the caller's wait; it does not interrupt a synchronous parser or acknowledge
cancellation of an already-issued OS operation. After an outstanding operation
settles, an expired traversal stops and closes any opened file. Native capacity retains each of its eight slots until that actual work settles. This is an observed
settings-byte result, not a transaction against concurrent directory replacement
or a record-content freshness certificate.

The maintained `source-declarations.test.ts` tests real three-level declarations,
strict scanner compatibility, missing/cyclic/repeated mounts, changed revisions,
authority/shape/cap/deadline failures, and a real composed Host call. Set
`CARTRIDGE_TEST_BIN` to a built runtime to require that last integration test;
without it, only the integration test is skipped.
