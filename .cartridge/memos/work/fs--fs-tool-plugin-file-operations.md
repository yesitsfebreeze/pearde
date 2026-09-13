---
kind: work
description: "Bounded file operations and exact edits"
status: done
needs:
  - "[[process-plugins-register-through-lua-lua-registration]]"
uses:
  - usage: "[[read-usage]]"
    when: ["Defining file read, write or exact-edit behavior, especially stale reads, concurrent changes, path escapes and partial mutation failures"]
---

# fs-tool-plugin-file-operations

Landed in the fs-operations lane: `plugins/fs/` (main.rs, service.rs, files.rs, service/tests.rs, Cargo.toml, UPSTREAM.md), `plugins/fs.lua`, workspace registration in Cargo.toml/Cargo.lock. 15 tests pass; `just check` and `just test` green.

## Do

Provide `tool.read`, `tool.write`, `tool.edit`, `tool.glob`, and `tool.grep` from one Rust process, registered by `plugins/fs.lua`. Inject `sessions`. This PRD owns the coding-tool envelope used by all tool plugins:

- `describe` returns `{name, description, input_schema}`; the name maps exactly to the provided `tool.<name>` key.
- `call` receives `{op:"call", context:{session,run,call,cwd}, input:{...}}` and returns `{content:string,error:boolean}`. The agent supplies context from the session, never from model arguments. `call` is a unique invocation ID. Unknown input fields and malformed types are rejected. Context is trusted orchestration metadata, not an authentication credential; direct local service callers are trusted operators.
- Long-running tools also implement `cancel {context:{session,run,call,cwd}}`. Cancellation is idempotent, applies only to that exact invocation, and is not advertised in the model's schema. This is an explicit extension to the earlier two-operation sketch, needed for child cleanup; it does not require a new transport frame.

Resolve paths relative to the canonical session cwd, restrict access to that workspace, reject traversal and symlink escapes, and check the nearest existing parent for a new file. Do not accept model-supplied cwd/session/run overrides. This is a path boundary, not a sandbox against concurrently malicious local processes; shell execution remains explicitly approved arbitrary code. The policy plugin owns allow/deny decisions. Successful mutations call `sessions touch`; failure to record a completed mutation must report partial success without automatic retry. Caps are bounded by plugin configuration. Default profile changes belong only to coding-profile-integration.

This memo owns only the bounded unit below; linked prerequisites own their implementations. Agent separation follows [[agent-is-a-separate-plugin]].

## Spec

Planning status: proposed specification based on source inspection. No implementation probe or code tests have run. Keep every acceptance box unchecked until verified. File footprint: `plugins/fs/`, `plugins/fs.lua`, `Cargo.toml`, `Cargo.lock`.

Create the `fs` crate using the process SDK and Lua wrapper. Implement describe and call for read/write/edit. Read input is `{path,offset?,limit?}` with one-based offset and a default limit of 2000 lines, additionally capped at 256 KiB. Reject binary/invalid UTF-8 input. Write input is `{path,text}`; create parents and replace file contents without truncating an existing file before successful preparation. Edit input is `{path,old,new,all?}`; reject empty old, require exactly one non-overlapping occurrence unless all=true, and reject zero matches even with all=true. Preserve permissions on replacement. New files use normal platform permissions. Report line numbers, truncation and filesystem errors explicitly.

Validate trusted context and workspace paths before any filesystem access. Writes to `.cartridge/memos/` are refused with guidance to tool.memo; the record is not maintained through generic writes. After a successful write/edit, record the canonical path with `sessions {op:"touch",id:context.session,file:path}`. Never claim rollback when bytes changed but touch failed. No registry, file watcher or git integration.

Port the selected tool-fs/fs-local behavior and regression cases identified in [[deepseek-plugin-port-map]], preserving source/license notices for adapted code. Track per-run canonical-path observations as unseen, confirmed absent, or present with a content-derived version. Partial reads establish a version but do not claim whole-file review. Unseen writes use atomic create-if-absent; unseen edits fail. Existing-file overwrite/edit requires a matching observed version and refreshes it after success. Serialize mutations per target within this process and compare against the observed version immediately before publication. Do not claim cross-process CAS; external writers can race replacement. Missing-file reads record confirmed absence; use no-clobber creation so a concurrent creator is preserved. Reset observations on run change or plugin reload.


Cancellation ordering: a cancel arriving before call registration must prevent that same unique invocation from subsequently executing. Retain bounded per-run cancellation tombstones until run disposal, and fail closed with capacity_exceeded rather than evicting a live-run tombstone. Test both cancel-before-registration and cancel-during-spawn; unknown cancellation never affects another invocation. The op is cancel on the existing tool key, not a new tool.cancel service.

For source or tests substantially adapted from [[deepseek-plugin-port-map]], include package-local UPSTREAM.md naming source paths/revision and UPSTREAM_LICENSE containing the full MIT notice; package/distribution checks must retain them.

## Check

- [x] Unread overwrite/edit and stale-version mutation fail without changing bytes; rereading permits the intended mutation, including same-size changes with restored mtime.
- [x] Concurrent creators preserve the winner; partial reads establish freshness only; pre-cancelled calls never mutate.

- [x] Tests verify one-based offsets, line/byte limits, binary rejection and missing-file errors.
- [x] Tests verify create/overwrite, unique edit, ambiguous edit without mutation, zero-match and empty-old rejection, and all=true replacement.
- [x] Traversal, absolute outside paths, symlinked files/parents, forged cwd fields and attempts to write the memo record fail before mutation.
- [x] A fake sessions service records only successful mutations; a touch failure returns error=true and identifies the already-changed file.
- [x] A failed preparation preserves existing file bytes and permissions; describe names and input schemas match the three provided keys.

Verification commands (future implementation gate; not run during planning):

```sh
set -eu
cargo test --manifest-path plugins/fs/Cargo.toml
cargo clippy --manifest-path plugins/fs/Cargo.toml --all-targets -- -D warnings
```
