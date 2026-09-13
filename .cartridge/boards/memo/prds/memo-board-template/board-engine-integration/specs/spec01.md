---
complexity: medium
footprint:
  - src/board.rs
  - .cartridge/templates/board
  - .cartridge/tests/unit/board.rs
  - .cartridge/tests/integration/board-engine.test.ts
  - .cartridge/docs/board.md
---

# spec01 — The generated board calls its pinned maintained planner

Current authority is `prd.ctg/src`, the maintained Bun implementation of the
Pearde board contract; its docs explicitly replace the retired external CLI.
Keep this engine external to memo. Extend the owner template to version 2 with
`engine.json` and a thin `prd.ts` entry. A source revision and SHA-256 manifest
bind the current engine's eight source files plus package/lock inputs. No engine
implementation, network download, installation or command-shell string is copied.

Invoke `bun <board>/prd.ts --engine <checkout> <operation> [arguments]`.
The engine location is explicit and may be anywhere; the board path always comes
from the generated entry's own directory. Refuse board override arguments,
unknown entry options, missing/malformed/symlinked pin inputs, or source mismatch
before launching. Use argument arrays and forward the engine's stdout, stderr,
exit status and process signals. A read command does not change work records.
The full engine planner remains available, including paging and its ready
frontier. The adapter owns no lifecycle or dependency algorithm.

Use the actual memo SDK process to generate root and member boards in disposable
Git projects. Demonstrate qualified cross-board prerequisites, a dependency-held
item, a ready item, invalid transition refusal, overlapping claim refusal and
failed collection remaining unfinished. Repeat from a separately located second
project and engine checkout, with an unrelated legacy `.pearde` sentinel present.
Validate generated workflow/grammar libraries through the same pinned entry.
Show that stale engine content and attempted board overrides execute nothing.

Template upgrades preserve the installer's collision contract: a version-1 board
with edited or different declared files is reported rather than rewritten.
Existing source and planning records remain the compatible fallback. On engine
failure retain its actual exit/error and partial effects; never automatically
retry a transition or reinterpret worker success as collection.

## Acceptance

- [x] A generated root/member fixture resolves qualified dependencies and exposes the complete ready frontier through the pinned adapter.
- [x] Actual engine calls refuse invalid transitions and overlapping claims; failed verification remains unfinished and preserves source HEAD.
- [x] Equivalent fixtures work at two checkout paths, preserve a legacy board, validate workflow/grammar, and never embed developer-home paths.
- [x] Missing/tampered engine and board override attempts fail before execution; existing installation collision, cancellation and owner gates pass.

## Verify and Proof

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just test memo
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just check memo
bun test ../memo.ctg/.cartridge/tests/integration/board-engine.test.ts
```

The integration fixture builds the actual memo SDK binary and launches the pinned
engine with subprocess argument arrays. Pin mismatch is a real failure, not a
skip. Reverify the overlapping initialize-board collection after this change.
