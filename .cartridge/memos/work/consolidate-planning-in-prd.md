---
kind: work
description: Consolidate PeaRDe planning, records and orchestration into one independent PRD cartridge
status: active
owner: /root/prd-consolidation
---

# Planning belongs to PRD

## Outcome

One `prd.ctg` cartridge owns the existing PeaRDe implementation from
`~/dev/infra/pearde`, all planning records for this composed project, specifications,
sub-PRDs, reviews, workflows, dependency scheduling, Gantt rendering and worker
orchestration. Other cartridges contain their domain implementation and have no
PeaRDe board, planning scripts or planning dependency. PRD knows their code locations.

The user explicitly corrected an earlier distributed-board proposal: consolidate
everything into this plugin and retain one implementation. Existing source changes,
PRD state, claims, dependencies and review history must survive the move.

## Approach

1. Preserve the original PeaRDe Git history and existing edits while integrating
   its planning core into native src/engine modules. Relocation under
   .cartridge/engine was an initial migration step, superseded by the user's
   explicit native-integration correction. Retire the old dispatcher and old-path
   compatibility alias from the finished system; keep one implementation.
2. Move current root/member planning records into .cartridge/boards with their
   existing member aliases. Record absolute source repository mappings and refuse
   missing/invalid mappings instead of treating the planning repository as code.
3. Consolidate planning memos, workflows, templates and review records. Retain
   historical review attribution and hashes; relocation is not fresh plan approval.
   Delete redundant planning artifacts and declarations from other cartridges.
4. Reuse the existing engine for scan, specs, refinement, claims, plan, Gantt,
   transitions and collection. Correct explicit central-board dispatch, root/member
   dependency gates, fresh frontier rescans, persisted completion checks and owned
   worker cancellation. Do not create a second scheduler.
5. Expose a `prd` CLI and `prd`/`tool.prd` services over one native planning API,
   using the standard Cartridge protocol. Publish observed state changes and worker
   lifecycle events on the runtime's prd channel. Recall planning context through
   the injected memory service and persist verified outcome evidence with explicit
   committed/pending status; memory does not replace authoritative PRD state.
   The MCP tool supplies planning and checked operations. Its contributed
   run-board routine coordinates this host's sub-agents. Standalone execution uses
   an explicitly configured external agent adapter; a subprocess cannot invoke the
   current conversation's collaboration API.
6. Verify against temporary boards and separate code repositories; prove component
   and host protocol behavior, inventory preservation, plan/Gantt output and cleanup.
   Do not dispatch the live backlog as a migration test.

## Review and delegation

User delegates ratings to agents. Engine analyst review:93/100; record migration
review:94/100. Both identify source-repository ownership, preserved history and real
continuous completion as required checks. Root coordinates publication and integration.
Workers: /root/prd_engine_analysis owns engine edits/tests; /root/prd_record_analysis
owns record migration; /root/prd_service owns service/protocol tests. Root owns CLI,
composition, integration and final verification. Each initial implementation has a
20-minute budget, extendable once by10 minutes for observed progress.

## Check

- [ ] Original engine history and pre-existing changes are preserved in one location.
- [ ] All182 current PRDs preserve identity, hierarchy, dependencies, state and unknown metadata; source repositories are explicit. The reviewed inventory contained180; two concurrently added records were found and included in the actual pre-move census.
- [ ] Other cartridges retain no PeaRDe implementation or planning board; central links and provenance are checked.
- [ ] CLI scan, plan, Gantt, specs/transition paths and mapped code ownership work.
- [ ] Continuous dispatch rescans dependencies and children, respects footprints and claims, and never infers done from process exit alone.
- [ ] Tool protocol rejects forged context/path escapes, bounds operations and owns cancellation; actual Cartridge composition discovers tool.prd and its guidance.
- [ ] Native host tests demonstrate runtime event publication and memory recall/outcome calls; no legacy CLI dispatcher is on the production execution path.
- [ ] Independent review and targeted tests pass, final results distinguish observed behavior from remaining limits.

Run `python3 -m unittest discover -s .cartridge/tests -p 'test_*.py'`,
`python3 .cartridge/scripts/check.py`, `./prd scan`, `./prd plan --json`,
`./prd gantt`, and fixture-based host protocol checks from prd.ctg.

## Failure

Preserve migration manifests and original state. Do not restore another session's
deleted files, overwrite concurrent edits, clear foreign claims, or replay uncertain
dispatch. A failing check remains visible. Keep the live backlog unlaunched until
an execution request selects it.
