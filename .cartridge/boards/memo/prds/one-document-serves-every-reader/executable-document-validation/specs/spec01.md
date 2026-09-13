---
complexity: medium
footprint:
- src/document.rs
- src/validation.rs
- .cartridge/tests/unit/validation.rs
- .cartridge/tests/integration/validation.test.ts
- .cartridge/tests/fixtures/validation
- .cartridge/docs/documents.md
---

# Freeze a validated execution descriptor without starting a process

The measured native commands baseline at4b08145 extracts duplicate recipes/imports
with validated:false and no executable metadata diagnostics. Installed Just1.58.0
--dump rejects duplicate recipes and inconsistent indentation, but parses read()
and backtick expressions and reads imported source during parsing. Retain these
actual probes in baseline.json. The historical external justdown specification
URL returned404; this explicit project dialect is not a claim of full justdown or
Just compatibility.

## Native API and immutable extraction

Add native document `action:"validate"`, path/optional owner/expected_revision and
optional `argv` (default[]). Accept no directory/query or alternate projection.
Raw commands/docs/human reads remain unchanged. The model tool gains no action.
Use the existing owner/alias resolver, private guard, exact-byte Document snapshot,
frontmatter parser and fenced-command extraction. No source re-read occurs after
parse. Existing identity/CRLF fixtures remain frozen; validation gets its own corpus.

Metadata must contain existing kind/description plus `dialect: cartridge-just/v1`,
`recipe: <name>`, `invocation: run`, `execution_base: <owner-relative directory>`.
Only run is supported; sidecar/artifact/event invocation modes fail explicitly.
Execution base is exactly dot or a bounded normal relative path: no absolute path,
parent/current components, NUL or symlink. It must resolve to an existing directory
inside the selected canonical owner root, independent of caller's nested cwd.
This check is not permission to execute and does not bind mutable directory contents.

## Conservative pinned syntax

Only exact fenced just blocks participate; prose, psaido and other language fences
never become code. Unclosed fences from the shared extractor refuse with their
source lines. Concatenate exact block bodies in source order with one LF separator;
retain original line endings and a generated-line→document-line source map.

cartridge-just/v1 is a deliberately smaller profile verified against Just1.58.0.
Allow blank/comment lines, multiple bare recipes `name param ...:` with unique
ASCII names, zero to16 unique required positional parameters, and ordinary command
body lines at one consistent nonempty indentation per recipe. Require a nonempty
body for each recipe. Name grammar is [A-Za-z_][A-Za-z0-9_-]*. Permit body Just
interpolation only as a declared parameter `{{ param }}`. Reject unclosed or other
expressions. Body shell text is opaque, not checked for safety or shell validity.
No line continuations/shebang scripts or advanced recipe attributes are supported.

Reject top-level imports/includes/modules, assignments (including backticks),
settings, aliases, attributes, dependencies, optional/variadic/default parameters,
unknown declarations and inconsistent indentation. The allowlist rejects read(),
filesystem/environment functions and all other Just expressions before any external
parser/evaluator runs. No import path is opened and no external parser process is
started. This leaf adds no runner, permission decision, subscription or observation.

Bound extraction to32 blocks/64 recipes/64KiB exact generated source,64 diagnostics,
16 argv strings of at most4096 bytes each and16KiB total, no NUL. Validate argv
arity for the declared default recipe. Diagnostic codes and document line/column
identify malformed fences, missing fields/default, duplicate names, unsupported
forms, interpolation, indentation, bounds and base errors without quoting private
contents. Report omitted diagnostic count on overflow. Any error returns
validated:false and no execution descriptor/source payload.

## Descriptor boundary

Success returns source identity/revision, dialect, validated:true,
launch_authorized:false, selected recipe/parameters, invocation and execution base,
exact generated Just stdin +SHA256/source map, and command program `just` with
argv `--no-dotenv --one --justfile - --working-directory <canonical base> -- <recipe>
<supplied argv...>`. Delimiter prevents supplied option-looking values becoming
flags. Bind a validation_revision to the dialect/parser version, source revision,
extraction digest, selected recipe/argv and execution base. Read-only validation
never runs this command. Downstream runner must check the pinned Just version,
apply its own policy/lifecycle and use this frozen stdin/argv without reopening the
source; safety, exit handling, output and execution authority remain other leaves.

## Acceptance

- [x] Missing/unsupported metadata, duplicate recipes and malformed fences return located diagnostics and no execution descriptor.
- [x] Imports/includes/mods, backticks, read/functions, unknown directives/dependencies and invalid parameters/indentation cause zero process starts and no imported reads or writes.
- [x] Valid multiple-block LF/CRLF extraction preserves exact bytes/source locations, selects declared recipe/argv and remains unchanged after source mutation without re-reading.
- [x] Owner-relative bases, symlinks/escapes, parameter arity, argument flags and all caps fail explicitly; legacy raw views and frozen identity bytes remain compatible.

## Verify and proof

Freeze separate fixture manifest, including valid quoted required parameter usage,
multiple recipes/fences, CRLF, malformed fences, duplicate names, forbidden forms
and execution-base escapes. Unit tests validate the already parsed Document then
mutate/delete its source before descriptor creation to prove no reread. Actual SDK
integration uses a stub Just executable writing a sentinel; every validation case
must leave zero sentinel starts and no new paths. Compare accepted frozen stdin
against installed Just1.58.0 dump AST in the test only; never use external Just from
product validation. No recipe needs to run to prove this leaf.

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just test memo
just check memo
cd ../memo.ctg
bun test ./.cartridge/tests/integration/validation.test.ts
bun test ./.cartridge/tests/integration/context.test.ts
```

Coordinator refreshes overlapping document identity/projection receipts, then the
facade prerequisite binding as necessary. Product source remains held until prior
facade/types/initialize/board-parent collection completes and round3 review passes.
