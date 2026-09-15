---
repo: /Users/feb/dev/cartridge/policy.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: policy
work-kind: leaf
needs:
- "@root/process-plugins-register-through-lua-lua-registration"
---

# Declarative fail-closed policy without Lua waiting

## Do

`plugins/policy.lua` provides policy and performs no waiting. `policy {tool,input,context}` returns `{decision:"allow"|"deny"|"ask",reason?}` immediately. Lua callbacks are synchronous; coroutine yield is not an approval mechanism. The agent owns correlation, timeout, cancellation and answering; the terminal only displays and submits decisions.

Defaults allow read/glob/grep and memo list/read; memo write and write/edit/bash ask. Unknown tools default to ask. Invalid configuration, invalid memo operation or malformed policy result fails closed. Exact per-tool rules in config may deliberately override defaults. Do not ship allow_if command patterns: substring matching cannot safely authorize compound shell commands. No stored approvals or sandbox claims. Profile config and client changes are owned by their respective integration PRDs.

This memo owns only the bounded unit below; linked prerequisites own their implementations. Agent separation follows [[agent-is-a-separate-plugin]].

## Spec

Planning status: proposed specification based on source inspection. No implementation probe or code tests have run. Keep every acceptance box unchecked until verified. File footprint: `plugins/policy.lua`, `core/tests/`.

Implement a Lua component providing policy with configurable `tools` exact-name overrides and a default decision. Validate allowed decision strings once on apply and reject unusable config rather than granting access. Inspect tool.memo input.op so a read allow does not authorize a write. Use the tool's declared name consistently without ambiguous aliases. Return a short reason for denials and asks. Do not emit ask events or subscribe to answer events in Lua.

Add a Rust/mlua test in the existing glue test module loading the real Lua file; no new Lua test runner is needed. Assert that a call returns synchronously and has no event subscription side effects.


Agent injection of policy is mandatory. Missing/unloaded/failed policy blocks execution; it cannot broaden permissions during hot reload. File freshness enforcement remains in fs; Lua policy decides permission, not filesystem atomicity.

## Acceptance
- [x] Default read/glob/grep and memo list/read return allow; write/edit/bash/memo write return ask.
- [x] An unknown tool uses configured default; unknown memo operation and malformed input do not receive allow.
- [x] Exact allow/deny/ask overrides work; invalid decision/config fails closed.
- [x] The real Lua plugin returns immediately without awaiting an event or exposing a coroutine-based approval path.

Verification commands (future implementation gate; not run during planning):

```sh
set -eu
cargo test -p glue policy
test -f plugins/policy.lua
cargo clippy -p glue --all-targets -- -D warnings
```

Implemented synchronous policy and four real-Lua tests; exact Spec block and `just check` passed. Combined `just all`: 32/32 tests plus fmt, Clippy, and docs passed after rebase and before landing. Empty JSON array validation was seen failing before repair. Landed `work/policy` into `snapshot/plugin-workspace`; lane closed after owner release and generated Cargo output cleanup. Final profile must provide `config = {}`; explicit JSON null is invalid config.
