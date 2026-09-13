---
kind: work
description: "Bounded glob and grep in the session workspace"
status: done
needs:
  - "[[process-plugins-register-through-lua-lua-registration]]"
  - "[[@prd/work/fs--fs-tool-plugin-file-operations.md]]"
uses:
  - usage: "[[read-usage]]"
    when: ["Defining glob or grep behavior, rg argument handling, ignored files, result limits or search cancellation"]
---

# fs-tool-plugin-file-search

## Do

Provide `tool.read`, `tool.write`, `tool.edit`, `tool.glob`, and `tool.grep` from one Rust process, registered by `plugins/fs.lua`. Inject `sessions`. This PRD owns the coding-tool envelope used by all tool plugins:

- `describe` returns `{name, description, input_schema}`; the name maps exactly to the provided `tool.<name>` key.
- `call` receives `{op:"call", context:{session,run,call,cwd}, input:{...}}` and returns `{content:string,error:boolean}`. The agent supplies context from the session, never from model arguments. `call` is a unique invocation ID. Unknown input fields and malformed types are rejected. Context is trusted orchestration metadata, not an authentication credential; direct local service callers are trusted operators.
- Long-running tools also implement `cancel {context:{session,run,call,cwd}}`. Cancellation is idempotent, applies only to that exact invocation, and is not advertised in the model's schema. This is an explicit extension to the earlier two-operation sketch, needed for child cleanup; it does not require a new transport frame.

Resolve paths relative to the canonical session cwd, restrict access to that workspace, reject traversal and symlink escapes, and check the nearest existing parent for a new file. Do not accept model-supplied cwd/session/run overrides. This is a path boundary, not a sandbox against concurrently malicious local processes; shell execution remains explicitly approved arbitrary code. The policy plugin owns allow/deny decisions. Successful mutations call `sessions touch`; failure to record a completed mutation must report partial success without automatic retry. Caps are bounded by plugin configuration. Default profile changes belong only to coding-profile-integration.

This memo owns only the bounded unit below; linked prerequisites own their implementations. Agent separation follows [[agent-is-a-separate-plugin]].

## Spec

User steering on 2026-09-09 supersedes the flat-search-only interface below: follow [[composable-agent-search]]. The search worker must add typed composition and reusable bounded results, update these proposed steps and acceptance checks from its implementation probe, and retain every existing backend/path/cancellation regression. The old glob/grep contract remains convenience compatibility over the same engine, not a second implementation. Do not close this memo with only independent glob and grep calls.


Planning status: proposed specification based on source inspection. No implementation probe or code tests have run. Keep every acceptance box unchecked until verified. File footprint: `plugins/fs/`.

Extend the fs plugin with glob input `{pattern}` and grep input `{pattern,path?,glob?}`. Use the existing `rg` platform tool for file enumeration and content search, with argument arrays rather than shell interpolation. Glob patterns use rg's documented glob syntax; enumerate normal non-ignored files, do not follow symlinks, sort workspace-relative paths, and cap at 1000 results/256 KiB. Grep uses rg's regex syntax and includes line numbers; cap output at 256 KiB. Restrict optional path to the workspace. Do not let a leading dash in a pattern become an option. Use concurrent draining and a 10-second configurable upper-bounded deadline; terminate and reap on deadline, cancellation or disposal. Non-matching rg exit 1 is empty success; other nonzero exits are errors with diagnostics. Missing rg is actionable, not an empty result.

Port tool-fs-search's argv and cancellation regressions listed in [[deepseek-plugin-port-map]], retaining source/license notices for adapted code. Always pass `--no-config` and explicitly keep hidden/ignored-file exclusion; do not inherit broader upstream defaults or personal RIPGREP_CONFIG_PATH. Validate structured backend output if using rg JSON rather than presenting malformed data as complete results.


Cancellation ordering: a cancel arriving before call registration must prevent that same unique invocation from subsequently executing. Retain bounded per-run cancellation tombstones until run disposal, and fail closed with capacity_exceeded rather than evicting a live-run tombstone. Test both cancel-before-registration and cancel-during-spawn; unknown cancellation never affects another invocation. The op is cancel on the existing tool key, not a new tool.cancel service.

For source or tests substantially adapted from [[deepseek-plugin-port-map]], include package-local UPSTREAM.md naming source paths/revision and UPSTREAM_LICENSE containing the full MIT notice; package/distribution checks must retain them.

## Check

- [x] Composition: chained files -> grep -> matches -> files_of returns typed items; empty input is an empty set, never a workspace sweep; incompatible stages reject before execution (`files` start, grep-from-matches requires `files_of`).

- [x] Refs: a later call reuses a prior bounded result via `ref` without resending entries; unknown refs and refs forged across the store scope (session/run/cwd) fail explicitly.

- [x] Convenience glob/grep are one-stage chains over the same engine: sorted workspace-relative results, rg ignore/hidden exclusion kept, `--no-config` argv isolation (fake rg asserts the flag), regex with line numbers, no-match exit 1 empty success.

- [x] Argument safety: literal argv arrays, no shell; patterns containing spaces, shell metacharacters and leading dashes pass through untouched (`--` separator).

- [x] Honesty and bounds: malformed structured backend output fails explicitly; oversized results report `truncated`/`complete:false` with the child terminated and reaped; missing rg is an actionable error, never an empty result.

- [x] Cancellation: a pre-cancelled invocation spawns no process; exact-call cancel is scoped to one invocation; the 10 s deadline terminates and reaps a hanging child.

Verification commands (pass gate; run on the lane):

```sh
set -eu
cargo test --manifest-path plugins/fs/Cargo.toml
cargo clippy --manifest-path plugins/fs/Cargo.toml --all-targets -- -D warnings
```

## Result

2026-09-09 — composable search with rg backend; 27 fs tests + workspace 74 green
