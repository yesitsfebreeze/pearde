---
state: "question"
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

## Questions

policy.ctg 03217e3 (owner, 2026-09-17) deleted every path in this PRD's footprint (`.cartridge/tests/{run,policy.rs,contract/}`, `memos/routine/policy-tests.md`) and redirected `just test policy`/`just check policy` to the composition smoke fixture (`.cartridge/tests/integration/smoke.test.ts`, policy section). Observed 2026-09-19: both gates exit 0 (6s / 4s), so Acceptance 1-2 already hold. Acceptance 3 (precedence matrix, invalid-replacement retention, explain attribution, parity, listed by `cargo test -- --list`) cannot hold: there is no crate. Two of the deleted tests covered the retired built-in `ship`/`gitfs` catalogs (help.md now says "no catalog"). MCP/proxy/native-agent parity is covered by the consumers' own tests (mcp approval.test.ts + unit tests, proxy unit tests, agent loop.rs/run_state.rs). Only the policy-internal rules (operation-over-tool precedence, whole-tool deny wins, explain `rule`/revision, invalid config keeps the prior policy) are untested now.

Where do the policy rule tests live now?

- **A (recommended): a bun rule fixture held by policy.ctg, run by the smoke gate.** Add `policy.ctg/.cartridge/tests/integration/rules.test.ts`: a table of `{config, request} -> {decision, rule}` cases through `cartridge run policy` / `policy.explain` on the built host, with a disposable `CARTRIDGE_HOME`, following `mcp.ctg/.cartridge/tests/integration/refresh.test.ts`. Also add one line to the superproject's `.cartridge/memos/routine/cartridge-smoke.md` so that `policy`/`all` also runs it, the way it already runs mcp's refresh test. This follows the owner's direction (no Rust harness, no Cargo.lock, tests run against the built host). The parity box is dropped as covered by the consumers. It touches two repos: policy.ctg (new file) and the superproject (smoke memo + pointer). Retarget the sibling `policy-refuses-unbounded-searches-...` footprint from `.cartridge/tests/policy.rs` to `.cartridge/tests/integration/rules.test.ts`.
- **B: extend the superproject smoke fixture's policy section only.** Add the precedence/explain/invalid-config cases inside `.cartridge/tests/integration/smoke.test.ts`. This touches one file and no policy.ctg change. But the tests live outside the owner, so the sibling's guard-rule cases would also have to land in the superproject, which turns that sibling into a two-repo leaf.
- **C: restore and port the Rust contract harness** (the PRD's original plan). This reverses 03217e3, brings back a 491-line crate with its own stale-prone Cargo.lock, and would test the retired catalog semantics unless those tests are cut. Not recommended without the owner's say-so.
- **D: defer this PRD as superseded by 03217e3.** Mark boxes 1-2 as met by the owner's commit. The sibling then adds its own table-driven cases (under A's or B's layout) as part of its own work, and its `needs` on this PRD is dropped.

Recommended: A. If the owner prefers the smallest board change, choose D and fold A's fixture into the sibling.
```

### Related since the question was asked (2026-09-19, coordinator cartridge-5c)

cartridge-4b's runtime analyst split `@runtime/policy-and-trust-…` so that the host absorbs policy: child 1
moves the evaluator into `cartridge.ctg/src/policy` with its own tests, child 2 removes `policy.ctg`. Its
recommendation for this board (see that PRD's `## Split`): retire this row and the deferred
`improve-policy-programme` / `improve-policy-resource-scope` as superseded by child 1's tests; retarget
`bounded-search-guard-rules` and `policy-refuses-unbounded-searches-with-a-teaching-reason` at
`cartridge.ctg/src/policy`; keep `policy-refusals-and-overrides-reach-the-caller-and-the-observation-journal`
and reconcile it with the runtime child "the agent asks through the host request…". This is a fifth
option, **E: defer this row as superseded by the host's policy move**. Nothing is deferred or retargeted
until the user answers; the runtime split has not landed.
