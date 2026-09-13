---
state: open
origin: requested
priority: 85
blast-radius: high
workflow: develop-one-cartridge
needs:
  - memory-document-works-end-to-end
  - @landscape/context-quality-is-measured
footprint:
  - /Users/feb/dev/cartridge/harness.ctg/main.rs
  - /Users/feb/dev/cartridge/harness.ctg/inspection.rs
  - /Users/feb/dev/cartridge/harness.ctg/working.rs
  - /Users/feb/dev/cartridge/harness.ctg/eval
  - /Users/feb/dev/cartridge/proxy.ctg/service.rs
  - /Users/feb/dev/cartridge/harness.ctg/tests
---

# Harness builds model context from the shared landscape result

Context gathering is currently split between harness, proxy recall, memo, terminal inspection, and memory. Harness should adapt one sourced context to a model conversation.

## Ownership and scope

Owner: `harness`. Participating repositories: `harness.ctg`, `proxy.ctg`, `agent.ctg`. Coordinate from the root master board. Footprints are preliminary checkout-absolute paths so Pearde can detect cross-board overlaps; narrow and rebase them during analysis before claiming in another checkout.

## Implementation plan

1. Capture current context and compaction fixtures as the baseline. Separate contributor gathering from conversation projection and summary storage.
2. Consume landscape's selected context and completeness metadata for both native turns and proxy injection. Keep canonical transcript and caller-owned proxy history unchanged.
3. Preserve explicit system-memo authority, source labels, latest user request, complete tool exchanges, and existing hard byte budgets.
4. Remove proxy's private recall assembly once equivalent memory facts arrive through landscape. Extend inspection to show chosen/omitted sources and the exact sent context revision.

## Acceptance contract

- Native and proxy paths receive equivalent relevant system facts under the same source snapshot, without double-inserting memory recall.
- Inspection names selection reasons and unavailable sources and can run without a model call.
- Existing compaction fault cases preserve the previous summary/transcript; latest user constraints and complete tool exchanges survive.
- Offline context-quality corpus passes with no regression in critical facts; optional live-model evaluation records model/prompt revision separately.

## Verification to turn into specs

Run from the composed repository root. These are proposed gates, not results. The analyst must probe commands and write executable `specs/specNN.md` gates with source revisions and expected outcomes before implementation.

```sh
just test harness
just test proxy
just test agent
python3 harness.ctg/eval/eval_compaction.py --check
```

## Failure and recovery

Retrieved prose gains system authority or budgets discard the latest user constraint. Assert authority and retention separately from ranking.

Rollback: Retain a comparison path during rollout. Revert context assembly without rewriting canonical transcripts or persisted summaries.

## Prior context

Related existing runtime memo leaf names: `rolling-context-retains-decision-evidence`, `the-context-inspector-opens-from-the-chat-editor`. Resolve them under `cartridge.ctg/.cartridge/memos/` and inspect older `.pearde` work before changing scope; link superseded work explicitly. This PRD is the authoritative state for this new slice, not a copy of an older ticket.

## Evidence

No implementation evidence yet. The assessment provides the baseline. All new PRDs begin `open`; Pearde transition commands govern later states. Do not manufacture specifications, approvals, timings, claims, or passing results.
