---
state: open
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge"
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: policy
work-kind: leaf
footprint:
- "agent.ctg"
- "agent.ctg/src/lib.rs"
- "agent.ctg/.cartridge/tests"
- "mcp.ctg"
- "mcp.ctg/src/service.rs"
- "mcp.ctg/.cartridge/tests/unit/tests.rs"
needs:
- "@policy/bounded-search-guard-rules/policy-refuses-unbounded-searches-with-a-teaching-reason"
---
# Policy refusals and overrides reach the caller and the observation journal

A policy reason is useless if the caller never sees it: `agent.ctg/src/lib.rs` `prepare_tool` turns every `deny` into the bare text `permission denied`, and `mcp.ctg/src/service.rs` does the same unless `policy_explanations` is on. Neither journals a refusal; only granted dispatches are observed (`observe_tool` / `observe`, stage `used`, via `memo` op `observe`). Forward the policy `reason` into the refused tool result, and observe refusals and overrides with the caller context and the policy `rule`.

## Acceptance

- [ ] A denied call through the native agent returns a tool result whose content contains the policy `reason`; same for MCP with explanations off.
- [ ] A denied call is observed through `memo` op `observe` with stage `refused`, the caller `{session, run, call}`, the tool and the policy `rule`; readable afterwards with the journal's existing query.
- [ ] An allowed call whose policy response carries `override` is observed as an override naming the bypassed rule.
- [ ] A failed observe never changes the decision or the result (fixture with a failing `memo`).
- [ ] `just test agent`, `just test mcp`, `just check agent`, `just check mcp` exit 0.

## Proof and recovery

Footprint: `agent.ctg/src/lib.rs`, `agent.ctg/.cartridge/tests/`, `mcp.ctg/src/service.rs`, `mcp.ctg/.cartridge/tests/unit/tests.rs`, and the two submodule pointers. Shared contract with child 2: the `policy` response's `reason`, `rule`, `override` fields.

Split from `@policy/bounded-search-guard-rules` on 2026-09-16 (analyst-1). No review rounds used before the split.
