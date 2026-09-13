# Native PRD rewrite: independent review handoff

Status: **handoff, not final approval**. The user confirmed that another session
owns the concurrent TypeScript rewrite. This review stops source work and broad
execution so that session can become the single implementation owner. The
Python results below are acceptance evidence and regression requirements for
the rewrite; they do not verify the TypeScript files.

See [the coordinator's ownership and provenance handoff](native-rewrite-coordination.md)
for source snapshots, pending session identification, preserved personal state,
remaining launcher consumers and the final integration boundary.

## Scope and independently observed evidence

Reviewed the centralized record migration, native engine API, repository mapping,
dependency gates, claims, collection, continuous dispatch, process cancellation,
runtime event transport, memory recall and the verified-outcome outbox.
The reviewer made no live claims, dispatched no product PRDs and edited no source.
Behavioral tests used disposable records, Git repositories and stand-in workers.

Independent commands and results on 2026-09-13:

```sh
python3 prd.ctg/.cartridge/scripts/check-records.py --migration
# PASS: 182 central PRDs; 386 native work/question states preserved;
# historical review-input hashes unchanged; dependency DAG valid.

PYTHONWARNINGS=ignore::ResourceWarning python3 -m unittest discover \
  -s prd.ctg/.cartridge/tests -p test_engine_coordinator.py -q
# PASS: 16 tests, 3.877 seconds.

python3 -m unittest discover \
  -s prd.ctg/.cartridge/tests -p test_service.py -q
# PASS: 16 tests, 1.193 seconds.
```

An earlier unsuppressed engine run also passed; inherited `open(...).read()`
code emitted ResourceWarnings. These warnings were not test failures.

The engine suite included an actual claim, isolated code worktree, code edit,
executable verification, collection and committed receipt with separate code
and record repositories. It also included actual child collection followed by
parent collection across different code repositories. Changing a child's spec
afterward invalidated the parent's verification.

The service suite exercised the real JSON-lines subprocess protocol and actual
engine event pipe. Its memory provider was a controlled fixture. **This reviewer
did not verify the final live Cartridge host, real memory provider or final MCP
discovery.** The coordinator still owns those checks.

A scoped executable search outside `prd.ctg` found no remaining PeaRDe,
`legacy-sys`, external PeaRDe-path or `board-plan` references in Python, shell,
Lua and Justfile sources, excluding Git, build, dependency and state directories.
This was not an exhaustive claim about every historical document.

## Acceptance and regression cases to preserve in TypeScript

1. **One owner and one engine.** Planning records, workflows, templates, PRDs,
   sub-PRDs, scheduling and orchestration belong to `prd.ctg`. Other cartridges
   expose generic runtime, memory and event capabilities. Remove the superseded
   active implementation after parity, rather than leaving competing schedulers.
   CLI and MCP must call the same native domain operations.

2. **Record and code repositories are separate.** Every central PRD has an
   explicit valid code-repository mapping. Invalid or missing required mappings
   refuse before changes. Resolve footprints and worktrees in the code repository;
   commit PRD/spec/collection evidence in the record repository. Run source-code
   gates in the mapped code repository. Preserve all original record identities,
   dependencies, claims and lifecycle state during migration.

3. **Master and member dependency context.** A member PRD depending on an open
   PRD in another member must not be claimable through a member-only command.
   Unresolved external dependencies fail closed. Root-context claims can proceed
   after their cross-member prerequisite is satisfied. Qualified aliases must
   resolve to the owning record without losing the complete dependency graph.
   Every actionable address returned by a plan must round-trip through read/claim.

4. **Atomic claims and mutations.** Serialize snapshot → gate → mutation →
   readback across processes and master/member aliases. Two concurrent claims
   of the same PRD must have exactly one winner. A command must not attribute
   another command's changes to its own events or receipts. Do not hold the
   mutation lock across an entire run while its workers need to claim/collect.
   The Python record guard was inspected; a concurrent-claim regression still
   needs explicit final execution and must be ported to the rewrite.

5. **Correct sub-PRD identity.** Adding under `@member/parent` creates
   `parent/child` in that member, retains its code owner and records the transition
   under the owning member and full local path. The earlier implementation
   created the correct file but wrote a root-board journal entry for bare `child`.

6. **Collection establishes evidence before done.** Exit zero and worker prose
   are insufficient. Reject proof-free collection before any lane merge or record
   change. Require passing executable verification, closed acceptance boxes,
   released claims, integrated commit receipts, committed PRD and spec bytes,
   committed collection evidence and no outstanding unmerged owned lane.
   The earlier dispatcher accepted `done` plus an unrelated old ancestor SHA;
   preserve the regression that rejects this forged completion.

7. **Parents verify children.** Validate every child's receipt and current
   contract recursively. A completed container is identified structurally:
   the old collection predicate accepted only `open`, so applying it to `done`
   skipped child validation. A parent may inherit a verified child's commit from
   a different code repository. Commit the parent's collection evidence as well
   as its PRD. A changed child spec must invalidate its parent's proof.

8. **Continuous dispatch is accountable.** Recompute the ready frontier after
   analysis, specification, child completion and collection. Respect slot limits,
   per-board limits, existing claims and real-path footprint clashes. A worker
   exiting zero without persisted progress is failed, not retried indefinitely.
   Validate pre-existing `done` records before announcing whole-board completion;
   print and checkpoint their actual verification failures. Preserve blocked,
   failed and uncertain work separately from completed work.

9. **Process ownership survives cancellation and normal exit.** Signal only
   groups started by the current service, never PIDs recovered from old journals.
   Stop groups in parallel with a shared finite deadline. The service's grace
   period must exceed the engine's complete cleanup budget: the earlier 3-second
   service grace killed the engine before its 5-second worker grace could finish,
   leaving detached workers alive. Test TERM-ignoring workers and descendants
   whose leader has already exited. Drain finished-worker groups before allowing
   the next conflicting footprint. Retain claims/lanes when cleanup is uncertain.

10. **Native events and memory are observable.** Emit actual planning, worker,
    transition and verification events through the Cartridge event system with
    host-owned invocation context. Drain the event pipe during process shutdown;
    bound event size/count and report loss or unavailable publication. Recall
    memory as context, never as lifecycle authority. Queue only independently
    verified per-PRD outcomes in a durable outbox, including successes from a run
    that is incomplete overall. Require a committed memory acknowledgment, bound
    retries and expose pending writes without repeating code collection.

11. **The service boundary remains bounded.** Reject model-supplied executable,
    adapter, cwd and board escape overrides. Keep trusted adapter configuration
    separate. Preserve session-owned asynchronous job journals and exact-call
    cancellation/replay protection. Bound serialized responses, including large
    `changed` arrays and Unicode; retain full verification evidence in durable
    storage rather than losing it merely to fit a public status response.

## Remaining release evidence

Port and run the cases above against the TypeScript implementation, including
the actual cross-repository collection cycle and subprocess tests. Re-run record
migration checks after final ownership cleanup. Exercise real host discovery,
read/plan, mutation events and memory query/verified ingestion using disposable
fixture boards through the actual runtime. Verify the installed CLI and worker
entry point, the continuous board routine, and the absence of a second active
engine. Record the exact final revision and results. No final score or release
approval is granted by this handoff.
