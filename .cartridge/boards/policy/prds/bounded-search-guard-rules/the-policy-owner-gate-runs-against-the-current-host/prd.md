---
state: open
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge/policy.ctg"
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: policy
work-kind: leaf
footprint:
- ".cartridge/tests/run"
- ".cartridge/tests/policy.rs"
- ".cartridge/tests/contract/Cargo.toml"
- ".cartridge/tests/contract/Cargo.lock"
- ".cartridge/memos/routine/policy-tests.md"
---
# The policy owner gate runs against the current host

`just test policy` and `just check policy` fail at e478864 before any test runs, so no policy rule can be proven offline. `.cartridge/tests/run` at HEAD builds a manifest that no longer exists (`cartridge.ctg/.cartridge/workspace/Cargo.toml`); `.cartridge/tests/contract/Cargo.lock` is stale under `--locked`; and `.cartridge/tests/policy.rs` imports `cartridge::runtime`, `cartridge::cartridge` and `lua::Host`, and writes fixtures in the retired `return {provide=…, apply=function(ctx) ctx:on/ctx:provide}` shape, none of which the current host crate exports. Port the fixture to the current host and node (`cartridge.listen`) API without dropping coverage.

## Acceptance

- [ ] `just test policy` from /Users/feb/dev/cartridge exits 0.
- [ ] `just check policy` from /Users/feb/dev/cartridge exits 0.
- [ ] The rule-precedence matrix, invalid-replacement retention, explain attribution and MCP/proxy/native-agent allow-and-deny parity tests still exist and run (test names listed by `cargo test -- --list`).

## Proof and recovery

Footprint: `.cartridge/tests/run` (an uncommitted foreign edit already points it at `mcp.ctg`/`proxy.ctg` manifests — reconcile with its author before absorbing it), `.cartridge/tests/policy.rs`, `.cartridge/tests/contract/Cargo.{toml,lock}`, `.cartridge/memos/routine/policy-tests.md`. Reference fixtures on the current API: `agent.ctg/.cartridge/tests/integration/loop.rs` (policy fixture via `cartridge.listen`). Baseline observed 2026-09-16: both gates exit 1 (`cannot update the lock file … --locked`), test ~9.5s, check ~1.5s.

Split from `@policy/bounded-search-guard-rules` on 2026-09-16 (analyst-1). No review rounds used before the split.
