---
complexity: medium
footprint: ["src/context.rs","src/inventory.rs","src/main.rs","src/service.rs","src/board.rs",".cartridge/templates/board",".cartridge/tests/unit/board.rs",".cartridge/docs/board.md","src/source_search.rs","src/document.rs",".cartridge/tests/unit/source_search.rs"]
---

# spec01 — Preview and safely install the owner-shipped board

The native memo service accepts `op: board`, trusted absolute existing `cwd`,
`action: preview|install` (preview by default), and optional single-segment `name`
(default root). It targets only `.cartridge/boards/<name>` and ships a versioned,
fixed manifest of relative settings, grammar, document templates and workflow
files. Settings use paths relative to the board; no developer-home paths,
engine implementation, profile changes or memory-store writes are installed.
The separate board-engine-integration leaf owns pinned engine execution proof.

Preview returns each declared path, exact proposed bytes and SHA-256, plus
missing/identical/conflict status, without creating a directory or memo seeds.
Existing bytes larger than the bounded template limit, symlinks, special files,
and invalid ancestor paths are conflicts. Unknown files remain untouched.

Install rechecks the filesystem: any initial collision prevents all writes.
Identical files remain byte-identical. Missing files publish complete bytes
atomically with no replacement; a racing creator is preserved and classified.
Late errors or cancellation report completed file paths and incomplete status,
without rollback or automatic replay. An explicit retry fills only missing
files. Aborting a native request asks its blocking worker to stop at the next
file boundary; already-published files remain inspectable in a later preview.
A process crash can leave temporary staging files, which retries do not delete.
The host owns the workspace and its directory ancestors; adversarial concurrent
ancestor renames are outside this boundary. Model tool calls cannot invoke board
installation or provide a trusted cwd.

## Acceptance

- [x] Native preview creates nothing; empty install exactly matches its versioned manifest and relative path substitutions.
- [x] Repeated install writes no bytes; authored settings, profile, decision and memory-store sentinels survive conflicts unchanged.
- [x] Initial collisions cause zero writes; racing file creation never overwrites bytes; injected interruption after one publication reports partial effects and retry completes missing files.
- [x] Invalid names, relative cwd, symlinks and oversized collision files fail closed; aborted native installation stops at a boundary and remains resumable; legacy memo tests pass.

## Verify and Proof

```sh
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= cargo test --manifest-path Cargo.toml -p memo_cartridge
```

Run public `just test memo` and `just check memo` from the runtime checkout.
Fixtures use disposable directories, exact byte snapshots and deterministic
publication hooks rather than timing to prove partial recovery and races.
