# Native PRD rewrite handoff

The user confirmed on 2026-09-13 that another session is implementing the
TypeScript engine in `src/{records,planner,process}.ts` and requested coordination.
This session has paused competing engine, CLI, and service edits. No native Python
source relocation occurred: the temporary implementation remains under
`.cartridge/engine/resources`. No TypeScript files were changed by this team.

## Ownership boundary

The TypeScript owner was identified from the local session registry and matching
rewrite authorization: `Analyze plan rating`, thread
`01a097e6-4d34-7390-b55f-23792b974627`. The user asked this session to find it,
coordinate, and expressed a preference for TypeScript. A handoff was delivered
through `codex queue` as message `01a09a15-df63-7d43-b6aa-fd0ccb91aead`.
The proposed owner controls the final native engine and launchers; acknowledgment
and a division of remaining work are pending. Do not retain two production schedulers or dispatchers.
The user has chosen TypeScript as the final implementation direction. The focused
TypeScript review is in `native-typescript-review-snapshot.md`; its five concrete
reproductions and final report path were also queued to the owner. Queue submission
is confirmed; no acknowledgment has yet been received. The default local control
socket is absent, so no active-turn steering was attempted successfully.
This session supplies migrated records, behavioral evidence, and review findings.
Neither the Python prototype nor untested TypeScript files establish completion of
native integration. Coordinate removal of temporary code only after parity checks.

## Preserved records and source

- `python3 .cartridge/scripts/check-records.py --migration` passes: 182 actual
  PRDs, 385 work memos, one question, original states/claims/owners/dependencies,
  unknown frontmatter, and historical review input hashes preserved.
- All planning boards are under `.cartridge/boards`; root lists 17 member aliases.
  Each active board and PRD explicitly maps to its code repository. A missing or
  invalid mapping must refuse execution; never use the planning repository as code.
- Original PeaRDe Git history remains in this repository. Incoming source changes
  are also preserved on `refs/heads/prd-relocation-inputs`, commit
  `76c49b60c927d1c4dd688f08ba66cf2e5367493c` (includes in-progress changes).
- `.cartridge/boards/upstream-engine` is an archived, separately owned worktree;
  exclude it from default dispatch and preserve its claims.
- Source cartridges' planning records, scripts, workflows, and duplicate routines
  were cleaned. Migration manifest and verification are in `record-migration/`.
  There are 179 documented pre-existing broken links, zero newly broken links.

## Tested behavior available for porting

- `.cartridge/tests/test_engine_coordinator.py`: 16 passing Python tests, including
  real separate-code-repository worktree implementation, executable verification,
  collection, integrated commit proof, and cross-repository parent collection.
- `.cartridge/tests/test_service.py`: 16 passing native protocol tests, including
  actual pipe events, memory correlation, durable proof outbox, partial-run receipts,
  bounded output, cancellation and session ownership.
- `.cartridge/tests/test_record_serialization.py` is an additional concurrent
  root/member claim test, prepared but not yet run against the final engine.
- `.cartridge/tests/test_host_integration.py` is a prepared real-host memory/event
  fixture, not yet passing evidence. Adapt it to final native code ownership.
- Native runtime test binary is
  `/tmp/cartridge-namespace-check/cartridge.ctg/workspace/target/debug/cartridge`.

## Critical invariants

1. Recompute the complete root dependency graph after every collected result or
   refinement; direct member calls must not bypass cross-member dependencies.
2. Serialize root/member record mutations using one repository lock. Claim before
   worker launch; measure worker progress after the coordinator's own claim write.
3. Exit zero and `state: done` are insufficient. Require committed contracts,
   executable acceptance evidence, an integrated code commit, committed collection
   evidence, and no remaining active lane. Reject `--trust` and proof-free collection
   before mutating records. Parent proof recursively validates child contracts and
   each child's own code repository, including later uncommitted changes.
4. Preserve foreign claims. Cancel owned worker process groups, including detached
   descendants and descendants surviving normal leader exit; report unconfirmed
   cleanup honestly. Do not signal stale PIDs recovered from a journal.
5. Publish observed domain events through Cartridge's `prd` channel with trusted
   call/session/run context. Memory recall is evidence, not planning authority.
   Only verified integration receipts enter the durable memory outbox, including
   verified successes within a partly failed run. Only `status: committed` confirms
   ingest; ambiguous acknowledgments remain pending and retries are bounded.
6. A subprocess cannot spawn the current conversation's host sub-agents. Host
   orchestration follows `@prd/routine/run-board.md`; external execution needs an
   explicitly configured adapter. Do not start the live backlog as a migration test.

## Remaining integration work

Replace temporary launchers with the single native engine, validate behavior,
complete a real Cartridge host memory/event test, and add PRD to the MCP composition
profile. The current manifest check command refers to a not-yet-created check.py.
Retire the old dispatcher and `/Users/feb/dev/infra/pearde` temporary symlink after
updating its remaining consumers. The global `pearde` wrapper and Claude statusline
still reference that source; do not silently break them. Preserve personal ignored
state and the source snapshot when retiring temporary files.

The root workspace and member repositories have extensive unrelated staged and
unstaged edits from other sessions. Do not use broad index writes, restore unrelated
deletions, push, or claim the product backlog completed. This report is a handoff,
not final native-integration approval.
