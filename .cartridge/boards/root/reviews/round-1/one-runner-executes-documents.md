---
state: open
origin: requested
priority: 92
blast-radius: high
workflow: develop-one-cartridge
needs:
  - @gitfs/tool-results-interoperate
  - @memo/one-document-serves-every-reader
footprint:
  - /Users/feb/dev/cartridge/cartridge.ctg/src/process.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/sdk.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/main.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/tests
  - /Users/feb/dev/cartridge/policy.ctg/init.lua
---

# A shared execution path runs a selected just recipe

A new executable document should work without a handwritten Rust tool handler or a new process cartridge. The executor must preserve existing policy, identity, limits, and cancellation behavior.

## Ownership and scope

Owner: `runtime`. Participating repositories: `cartridge.ctg`, `policy.ctg`, `memo.ctg`. Coordinate from the root master board. Footprints are preliminary checkout-absolute paths so Pearde can detect cross-board overlaps; narrow and rebase them during analysis before claiming in another checkout.

## Implementation plan

1. Probe just's actual argument parsing with spaces, newlines, Unicode, leading dashes, and shell metacharacters. Define an argv-based invocation; do not copy a documentation command shape without testing it.
2. Use one reusable executor module over existing process/lifecycle machinery. Bind owner/path/revision, recipe, trusted cwd/session/run/call, and policy decision before spawning.
3. Implement run and artifact modes first, with separate stdout/stderr, exit status, deadlines, cancellation, and output caps. Recipes delegate persistent operations to existing services using the current host route, rather than accidentally booting a second profile.
4. Expose a generic command entry usable from shell, agent, MCP, and proxy. Keep transport formatting outside the executor and keep domain operations outside the kernel.
5. Use current launch-authority/sandbox contracts as dependencies; never claim a sandbox property that the runtime does not enforce.

## Acceptance contract

- A fixture document executes with literal argument boundaries; metacharacter input is data, not an extra shell command introduced by the launcher.
- Unknown recipe, stale revision, denied policy, and invalid cwd spawn nothing; policy ask retains each client's existing approval behavior.
- Nonzero exit remains a failure even if stdout contains success-looking JSON or an ARTIFACT marker.
- Cancellation targets one invocation and terminates its owned process tree; completed mutations are not reported as rolled back.
- An artifact result returns a verified path only after success; output truncation is explicit and bounded.

## Verification to turn into specs

Run from the composed repository root. These are proposed gates, not results. The analyst must probe commands and write executable `specs/specNN.md` gates with source revisions and expected outcomes before implementation.

```sh
just test runtime
just check runtime
just smoke policy
```

## Failure and recovery

A recipe calls a fresh temporary host and duplicates a memory writer or listener. Carry the existing host route through execution and test process counts.

Rollback: Keep legacy adapters selectable while the generic route stabilizes. Do not replay failed or interrupted mutations automatically.

## Prior context

Related existing runtime memo leaf names: `every-tool-is-one-command`, `the-tool-contract-is-a-memo`. Resolve them under `cartridge.ctg/.cartridge/memos/` and inspect older `.pearde` work before changing scope; link superseded work explicitly. This PRD is the authoritative state for this new slice, not a copy of an older ticket.

## Evidence

No implementation evidence yet. The assessment provides the baseline. All new PRDs begin `open`; Pearde transition commands govern later states. Do not manufacture specifications, approvals, timings, claims, or passing results.
