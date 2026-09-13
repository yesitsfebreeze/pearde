---
kind: work
description: Make all fifteen cartridges measurably useful through bounded, dependency-ordered improvements
status: open
priority: P0
subwork:
  - "[[@prd/work/root--improve-tool-result-contract.md]]"
  - "[[@prd/work/root--improve-memo-programme.md]]"
  - "[[@prd/work/root--improve-memory-programme.md]]"
  - "[[@prd/work/root--improve-memory-tool-programme.md]]"
  - "[[@prd/work/root--improve-gitfs-programme.md]]"
  - "[[@prd/work/root--improve-pty-programme.md]]"
  - "[[@prd/work/root--improve-mcp-programme.md]]"
  - "[[@prd/work/root--improve-policy-programme.md]]"
  - "[[@prd/work/root--improve-sessions-programme.md]]"
  - "[[@prd/work/root--improve-harness-programme.md]]"
  - "[[@prd/work/root--improve-router-programme.md]]"
  - "[[@prd/work/root--improve-proxy-programme.md]]"
  - "[[@prd/work/root--improve-agent-programme.md]]"
  - "[[@prd/work/root--improve-fs-programme.md]]"
  - "[[@prd/work/root--improve-tools-programme.md]]"
  - "[[@prd/work/root--improve-ui-programme.md]]"
uses:
  - usage: "[[read-usage]]"
    when: [planning all cartridge improvements, choosing the next cartridge improvement, reviewing the cartridge improvement roadmap]
---

# Cartridge improvement programme

## Outcome

Turn the 2026-09-13 cartridge usefulness assessment into delivered behavior across
all 15 runnable cartridges. The scope is 45 requested improvements, three assessed
downsides per cartridge, and one shared tool-result prerequisite discovered during
planning. Each improvement has one leaf work item; each cartridge has one coordinating
parent. The runtime and landscape library participate only where those outcomes
require shared contracts, discovery or context.

The user asked for working plans. The plans are created; implementation remains open.
No usefulness score is treated as an empirical baseline or a promised result.
[[cartridge-improvement-evidence]] separates live observations, source findings,
reported tests and proposals. [[@prd/routine/plan-cartridge-work.md]] defines the reusable procedure.

## Start here

The first four work items can start independently after checking live source ownership.
They have no hard prerequisites inside this programme. Land changes to shared files
serially and revalidate against the integrated revision.

| Order | Work | Why first | Ready definition |
| --- | --- | --- | --- |
| 1 | [[@prd/work/root--improve-tool-result-contract.md]] | Real tool calls must survive the transport boundary before richer tools are useful. | Reproduce GitFS read and ship scan through a temporary real MCP host. |
| 2 | [[@prd/work/root--improve-policy-operation-rules.md]] | Read-only GitFS should be usable without a blanket mutation grant. | Establish the old/new rule precedence fixture; preserve current profiles. |
| 3 | [[@prd/work/root--improve-memory-owner-access.md]] | Recall currently fails when another process owns the configured store. | Reproduce two-client access using a disposable store and inspect the existing owner protocol. |
| 4 | [[@prd/work/root--improve-gitfs-snapshot-selection.md]] | A declared path filter should select exactly those paths. | Reproduce A/B selection in a temporary Git repo. |

Next, unlock [[@prd/work/root--improve-policy-explain.md]], [[@prd/work/root--improve-gitfs-readable-diff.md]],
[[@prd/work/root--improve-memory-readiness.md]], [[@prd/work/root--improve-memory-tool-errors.md]] and
[[@prd/work/root--improve-mcp-approval-route.md]] as their actual needs become satisfied.
Other prerequisite-free work includes compact memo discovery, type drilldown,
shell identity, session diagnosis, route explanation, capability routing, filesystem
search paging, compaction comparison and development-tool preflight.

## Delivery stages

Stages set priority and integration checkpoints. They are not artificial global barriers:
a ready child can be worked on before all unrelated tasks in an earlier stage finish.

| Stage | Outcomes | Exit evidence |
| --- | --- | --- |
| 0 — Reliable access | Shared results, operation policy/explanation, safe read discovery, memory owner access/readiness/errors, snapshot selection. | Real MCP reads/scan succeed, reads and writes have distinct policy outcomes, two-client memory recall works, selected snapshot touches only A. |
| 1 — Discovery and control | Bounded/fresh memo retrieval, individual types, fact drilldown, terminal identity/ownership/command waiting, session mapping/recovery, catalog refresh, constrained resources, reviewable shipping. | A cold caller finds and inspects a capability, sees its readiness, executes an authorized fixture operation and receives attributable results. |
| 2 — Context and diagnostics | Token/byte accounting, compaction comparisons, route explanations/capability/cost metadata, proxy usage/traces/recovery, interrupted-agent reconciliation. | Cross-round results remain attributable and accounting exposes unknowns; failed/restarted runs do not replay uncertain mutations. |
| 3 — Workflow and measured quality | Narrow memory correction, retention, direct/overlay attribution, guarded FS operations, worktree/bundle improvements, transcript/owner/readiness UI and quality evaluations. | All component acceptance checks pass; comparative evaluations report actual outcomes and retained limitations instead of architecture-based scores. |

## Dependency map

The leaf needs fields are the exact dependency graph. This diagram shows the main paths.

```mermaid
flowchart TD
    Results[Shared tool results] --> GitRead[GitFS inspection]
    Rules[Operation policy] --> Explain[Policy explanation]
    Rules --> GitRead
    Explain --> MCPAuth[MCP authorization route]
    Owner[Memory owner access] --> Ready[Memory readiness]
    Ready --> Errors[Memory tool errors]
    Results --> Errors
    Ready --> Discovery[Tool readiness discovery]
    Explain --> Discovery
    Results --> Discovery
    Results --> Refresh[MCP catalog refresh]
    Discovery --> Palette[UI availability]
    Refresh --> Palette
    Identity[Shell identity] --> Ownership[Input ownership]
    Identity --> Wait[Command-specific readback]
    Ownership --> OwnerUI[UI terminal ownership]
    GitRead --> Ship[Reviewable shipping]
    Snapshot[Selected snapshots] --> Ship
    Recovery[Session diagnosis] --> Resume[Agent restart reconciliation]
    Route[Compatible routing] --> Tokens[Harness accounting]
    Compact[Compaction comparison] --> Eval[Context quality evaluation]
```

## Component plans and coverage

Each component plan maps the assessment's three improvements to its three leaf items,
and records all three downside mitigations or retained limitations.

| Cartridge | Plan | Improvement IDs |
| --- | --- | --- |
| Memo | [[@prd/work/root--improve-memo-programme.md]] | [[@prd/work/root--improve-memo-compact-landscape.md]], [[@prd/work/root--improve-memo-stale-evidence.md]], [[@prd/work/root--improve-memo-types-drilldown.md]] |
| Memory | [[@prd/work/root--improve-memory-programme.md]] | [[@prd/work/root--improve-memory-owner-access.md]], [[@prd/work/root--improve-memory-readiness.md]], [[@prd/work/root--improve-memory-provenance.md]] |
| Memory tool adapter | [[@prd/work/root--improve-memory-tool-programme.md]] | [[@prd/work/root--improve-memory-tool-get.md]], [[@prd/work/root--improve-memory-tool-correct.md]], [[@prd/work/root--improve-memory-tool-errors.md]] |
| GitFS and ship | [[@prd/work/root--improve-gitfs-programme.md]] | [[@prd/work/root--improve-gitfs-readable-diff.md]], [[@prd/work/root--improve-gitfs-snapshot-selection.md]], [[@prd/work/root--improve-gitfs-reviewable-ship.md]] |
| PTY and shared shell | [[@prd/work/root--improve-pty-programme.md]] | [[@prd/work/root--improve-pty-shell-identity.md]], [[@prd/work/root--improve-pty-input-ownership.md]], [[@prd/work/root--improve-pty-command-wait.md]] |
| MCP bridge | [[@prd/work/root--improve-mcp-programme.md]] | [[@prd/work/root--improve-mcp-approval-route.md]], [[@prd/work/root--improve-mcp-tool-readiness.md]], [[@prd/work/root--improve-mcp-refresh-catalog.md]] |
| Policy | [[@prd/work/root--improve-policy-programme.md]] | [[@prd/work/root--improve-policy-operation-rules.md]], [[@prd/work/root--improve-policy-resource-scope.md]], [[@prd/work/root--improve-policy-explain.md]] |
| Sessions | [[@prd/work/root--improve-sessions-programme.md]] | [[@prd/work/root--improve-sessions-client-mapping.md]], [[@prd/work/root--improve-sessions-retention.md]], [[@prd/work/root--improve-sessions-recovery.md]] |
| Harness | [[@prd/work/root--improve-harness-programme.md]] | [[@prd/work/root--improve-harness-token-accounting.md]], [[@prd/work/root--improve-harness-compaction-diff.md]], [[@prd/work/root--improve-harness-quality-eval.md]] |
| Router | [[@prd/work/root--improve-router-programme.md]] | [[@prd/work/root--improve-router-route-explanation.md]], [[@prd/work/root--improve-router-capability-routing.md]], [[@prd/work/root--improve-router-cost-latency.md]] |
| Proxy | [[@prd/work/root--improve-proxy-programme.md]] | [[@prd/work/root--improve-proxy-total-usage.md]], [[@prd/work/root--improve-proxy-tool-trace.md]], [[@prd/work/root--improve-proxy-continuation-recovery.md]] |
| Agent loop | [[@prd/work/root--improve-agent-programme.md]] | [[@prd/work/root--improve-agent-task-baseline.md]], [[@prd/work/root--improve-agent-resume-boundaries.md]], [[@prd/work/root--improve-agent-decision-attribution.md]] |
| Filesystem tools | [[@prd/work/root--improve-fs-programme.md]] | [[@prd/work/root--improve-fs-change-provenance.md]], [[@prd/work/root--improve-fs-revision-guards.md]], [[@prd/work/root--improve-fs-search-pages.md]] |
| Workspace tools | [[@prd/work/root--improve-tools-programme.md]] | [[@prd/work/root--improve-tools-preflight.md]], [[@prd/work/root--improve-tools-worktree-resume.md]], [[@prd/work/root--improve-tools-bundle-provenance.md]] |
| Terminal UI | [[@prd/work/root--improve-ui-programme.md]] | [[@prd/work/root--improve-ui-run-history.md]], [[@prd/work/root--improve-ui-terminal-owner.md]], [[@prd/work/root--improve-ui-tool-availability.md]] |

## Shared footprints and coordination

- Policy, MCP, proxy and the shared tool-result work meet at dispatch/result validation.
  Settle the result envelope and policy evaluation contracts before landing adapters.
  Coordinate with [[@prd/work/root--rpc-contracts-run-across-rust-lua-and-bun.md]]; do not claim its work.
- Memory engine and adapter leaves meet at src/cartridge.rs and lifecycle errors.
  Preserve the one-writer contract. Follow memory.ctg/AGENTS.md in isolated worktrees.
- Sessions main.rs is shared by correlation, retention, recovery and filesystem evidence.
  Reconcile with [[@prd/work/root--the-board-is-channels-of-lines.md]] before changing persistence shape.
- PTY input changes overlap [[@prd/work/root--pty-encodes-input.md]]. UI changes overlap
  [[@prd/work/root--the-sidebar-slides-over-the-shell.md]] and [[@prd/work/root--the-terminal-is-drawn-from-pty.md]].
  Preserve the foreground terminal and their existing owners.
- Memo and landscape changes must preserve the existing resolver and ranking work:
  [[@prd/work/root--a-search-ranks-current-guidance-over-delivered-history.md]] and
  [[@prd/work/root--one-search-covers-the-record-and-memory.md]]. Do not create another ranking engine.
- Harness evaluation extends [[@prd/work/root--rolling-context-retains-decision-evidence.md]] and
  coordinates with [[@prd/work/root--long-horizon-recall-benchmark.md]]. Agent attribution does not
  reimplement [[@prd/work/root--agents-query-the-tool-graph.md]].
- The assessment file also proposes document execution, a central landscape query
  boundary and repository consolidation. Keep those as separately scoped architecture
  work; these improvements must neither require nor silently enact those migrations.

## Check

Before implementation, record the current result for each scenario against a fixed
fixture, source revision and profile. The following are completion targets, not claims
about today's implementation.

- [ ] Every subwork parent and [[@prd/work/root--improve-tool-result-contract.md]] is done, with all
      leaf checks and prerequisites satisfied and Result evidence recorded.
- [ ] A real MCP client lists and reads a temporary GitFS overlay, scans a harmless
      fixture, queries/gets a seeded memory fact, and reads the shared PTY state.
      These five scenarios succeed under their documented least necessary grants.
- [ ] Denied mutation, stale revision, competing store owner, interrupted operation,
      stale catalog and changed source fixtures produce explicit attributable outcomes;
      no failure is disguised as an empty successful result.
- [ ] All 45 requested improvements have their leaf evidence and all 45 downside
      entries have mitigation evidence or an explicit retained limitation.
- [ ] Default memo landscape output satisfies its proposed 16 KiB fixture target;
      retrieval fixtures report hit ranking and why matches were selected. Metadata
      does not imply verification or instruction authority.
- [ ] Quality reports separate deterministic fixture checks from opt-in model runs,
      record revisions/configurations, and count invented permission/completion as
      failures. Compare actual task completion, constraint adherence, tokens, tool
      calls and latency; do not turn subjective usefulness ratings into measurements.
- [ ] Relevant integrated module gates and real-boundary smoke tests pass on the same
      integrated revisions. Full required memory checks pass before its changes land.
- [ ] Profiles, command declarations, owner-local docs and recovery instructions match
      delivered behavior; no default tool exposure expands as an incidental side effect.

Final integrated acceptance gates (run after the scenario fixtures above are implemented):

```sh
just smoke
just check
just test
just links
```

## Verification strategy

All listed source paths in leaf items are starting points verified during planning.
A planned new fixture must be wired into the existing command shown by its leaf.
Gate commands run from `/Users/feb/dev/cartridge`; the forwarded Justfile chooses
the correct repository. Use isolated temporary profiles, repositories, remotes and
stores. Ordinary gates use fixture providers, not paid inference or private data.

At Stage 0 and after affected transport changes, use `just smoke` plus the real
tool-call scenarios added to that entry point. At each component landing, run its
scoped tests/checks. At the final integrated revision run the project's required
`just check`, `just test` and `just links`; a prior result can be reused only
when the relevant source and configuration have not changed.

Tests are future implementation obligations. This planning task verifies documents,
links, paths and dependency structure; it does not claim product behavior passed.

## Execution and completion rules

- Read current records and claim an executable leaf before implementation. New plans
  are open with no owner; no existing active claim has been reassigned.
- A size S is a local change, M a bounded cross-file contract, L a probe followed by
  smaller slices if needed. These are scope estimates, not fabricated calendar dates.
- First establish current behavior; if it already meets the outcome, record evidence
  and avoid duplicating it. Technical defaults in Approach are recommendations to
  verify, not attributed user decisions.
- Stop at a failing acceptance boundary and record the cause. Preserve store locks,
  user work and live permissions. Reconcile ambiguous external effects explicitly.
- Commit implementation inside affected submodules before updating parent pointers
  when landing is requested. A plan, commit or passing unrelated test is not done.
- If scope changes, update leaf Outcome, Check, needs and coverage together using
  revision-checked memo writes. Parents roll up completed children; they are never
  scheduled as duplicate implementation.

## Planning validation

[[cartridge-plan-validation]] records coverage, source-path checks and dependency validation.
The planning deliverable is complete; the implementation status above remains open.
