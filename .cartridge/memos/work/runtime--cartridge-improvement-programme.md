---
kind: work
description: Make all fifteen cartridges measurably useful through bounded, dependency-ordered improvements
status: open
priority: P0
subwork:
  - "[[improve-tool-result-contract]]"
  - "[[improve-memo-programme]]"
  - "[[improve-memory-programme]]"
  - "[[improve-memory-tool-programme]]"
  - "[[improve-gitfs-programme]]"
  - "[[improve-pty-programme]]"
  - "[[improve-mcp-programme]]"
  - "[[improve-policy-programme]]"
  - "[[improve-sessions-programme]]"
  - "[[improve-harness-programme]]"
  - "[[improve-router-programme]]"
  - "[[improve-proxy-programme]]"
  - "[[improve-agent-programme]]"
  - "[[improve-fs-programme]]"
  - "[[improve-tools-programme]]"
  - "[[improve-ui-programme]]"
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
| 1 | [[improve-tool-result-contract]] | Real tool calls must survive the transport boundary before richer tools are useful. | Reproduce GitFS read and ship scan through a temporary real MCP host. |
| 2 | [[improve-policy-operation-rules]] | Read-only GitFS should be usable without a blanket mutation grant. | Establish the old/new rule precedence fixture; preserve current profiles. |
| 3 | [[improve-memory-owner-access]] | Recall currently fails when another process owns the configured store. | Reproduce two-client access using a disposable store and inspect the existing owner protocol. |
| 4 | [[improve-gitfs-snapshot-selection]] | A declared path filter should select exactly those paths. | Reproduce A/B selection in a temporary Git repo. |

Next, unlock [[improve-policy-explain]], [[improve-gitfs-readable-diff]],
[[improve-memory-readiness]], [[improve-memory-tool-errors]] and
[[improve-mcp-approval-route]] as their actual needs become satisfied.
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
| Memo | [[improve-memo-programme]] | [[improve-memo-compact-landscape]], [[improve-memo-stale-evidence]], [[improve-memo-types-drilldown]] |
| Memory | [[improve-memory-programme]] | [[improve-memory-owner-access]], [[improve-memory-readiness]], [[improve-memory-provenance]] |
| Memory tool adapter | [[improve-memory-tool-programme]] | [[improve-memory-tool-get]], [[improve-memory-tool-correct]], [[improve-memory-tool-errors]] |
| GitFS and ship | [[improve-gitfs-programme]] | [[improve-gitfs-readable-diff]], [[improve-gitfs-snapshot-selection]], [[improve-gitfs-reviewable-ship]] |
| PTY and shared shell | [[improve-pty-programme]] | [[improve-pty-shell-identity]], [[improve-pty-input-ownership]], [[improve-pty-command-wait]] |
| MCP bridge | [[improve-mcp-programme]] | [[improve-mcp-approval-route]], [[improve-mcp-tool-readiness]], [[improve-mcp-refresh-catalog]] |
| Policy | [[improve-policy-programme]] | [[improve-policy-operation-rules]], [[improve-policy-resource-scope]], [[improve-policy-explain]] |
| Sessions | [[improve-sessions-programme]] | [[improve-sessions-client-mapping]], [[improve-sessions-retention]], [[improve-sessions-recovery]] |
| Harness | [[improve-harness-programme]] | [[improve-harness-token-accounting]], [[improve-harness-compaction-diff]], [[improve-harness-quality-eval]] |
| Router | [[improve-router-programme]] | [[improve-router-route-explanation]], [[improve-router-capability-routing]], [[improve-router-cost-latency]] |
| Proxy | [[improve-proxy-programme]] | [[improve-proxy-total-usage]], [[improve-proxy-tool-trace]], [[improve-proxy-continuation-recovery]] |
| Agent loop | [[improve-agent-programme]] | [[improve-agent-task-baseline]], [[improve-agent-resume-boundaries]], [[improve-agent-decision-attribution]] |
| Filesystem tools | [[improve-fs-programme]] | [[improve-fs-change-provenance]], [[improve-fs-revision-guards]], [[improve-fs-search-pages]] |
| Workspace tools | [[improve-tools-programme]] | [[improve-tools-preflight]], [[improve-tools-worktree-resume]], [[improve-tools-bundle-provenance]] |
| Terminal UI | [[improve-ui-programme]] | [[improve-ui-run-history]], [[improve-ui-terminal-owner]], [[improve-ui-tool-availability]] |

## Shared footprints and coordination

- Policy, MCP, proxy and the shared tool-result work meet at dispatch/result validation.
  Settle the result envelope and policy evaluation contracts before landing adapters.
  Coordinate with [[rpc-contracts-run-across-rust-lua-and-bun]]; do not claim its work.
- Memory engine and adapter leaves meet at src/cartridge.rs and lifecycle errors.
  Preserve the one-writer contract. Follow memory.ctg/AGENTS.md in isolated worktrees.
- Sessions main.rs is shared by correlation, retention, recovery and filesystem evidence.
  Reconcile with [[the-board-is-channels-of-lines]] before changing persistence shape.
- PTY input changes overlap [[pty-encodes-input]]. UI changes overlap
  [[the-sidebar-slides-over-the-shell]] and [[the-terminal-is-drawn-from-pty]].
  Preserve the foreground terminal and their existing owners.
- Memo and landscape changes must preserve the existing resolver and ranking work:
  [[a-search-ranks-current-guidance-over-delivered-history]] and
  [[one-search-covers-the-record-and-memory]]. Do not create another ranking engine.
- Harness evaluation extends [[rolling-context-retains-decision-evidence]] and
  coordinates with [[long-horizon-recall-benchmark]]. Agent attribution does not
  reimplement [[agents-query-the-tool-graph]].
- The assessment file also proposes document execution, a central landscape query
  boundary and repository consolidation. Keep those as separately scoped architecture
  work; these improvements must neither require nor silently enact those migrations.

## Check

Before implementation, record the current result for each scenario against a fixed
fixture, source revision and profile. The following are completion targets, not claims
about today's implementation.

- [ ] Every subwork parent and [[improve-tool-result-contract]] is done, with all
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
