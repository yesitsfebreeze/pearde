---
repo: /Users/feb/dev/cartridge/memo.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memo
work-kind: leaf
description: "Resolve native memos and repository files by declared usage and situation"
---

# Implement memo usage resolution

## Outcome

A caller can ask the native memo service for files appropriate to a usage and
situation, receive bounded results with an explanation, and inspect undeclared
repository files. This is the first stage of [[memo-resolver-design]], grounded in
[[resolver-source-findings]]. It precedes the work planner.

Scope expanded with the user's integration request: scope/routine declarations,
harness guidance, observations, reports, and conditional writes are included.
Automatic lesson application, execution adapters, and cold-file review remain
outside this implementation.

## Acceptance
- [x] Usage and resource are declared through native type memos. The initial
  read/edit/run/compose usages are discoverable through `types` and `list`.
- [x] Shared `uses` metadata rejects unknown usages, duplicate entries, wrong
  field shapes, and empty situation lists. Existing memos without it remain readable.
- [x] Exact lookup distinguishes missing references, unsupported usages, and
  conflicting resource targets; it never guesses a basename.
- [x] Query lookup filters by usage and returns deterministic ranked candidates
  with matched fields, caveats, and revision digests, bounded to the requested limit.
- [x] A linked but lexically unrelated file does not match; repeated trigger text
  does not boost rank. A common word in `not_when` alone does not veto a candidate.
- [x] Scope-limited file inventory reports undeclared files, exclusions, missing
  targets, and conflicts without reading ignored runtime files or the old record.
- [x] An external-file resource cannot escape the workspace through absolute paths,
  traversal, or symlinks. Its source remains in place and unmodified.
- [x] Source edits are visible on the next lookup. `resolve` and `coverage` write
  no records, execute nothing, and do not count an access as useful.
- [x] Both the host service and model tool expose the new operations with strict
  request validation, cancellation, bounded output, and actionable errors.
- [x] Real declarations demonstrate: “record a settled choice” finds the decision
  type's compose usage; “change system prompt placeholder handling” finds the
  harness prompt resource's edit usage; an unrelated situation returns no hits.
- [x] Focused memo tests and the repository gate pass; documentation accurately
  distinguishes shipped retrieval and explicit feedback from deferred automation.

## Approach

Use `builtin/memo/src/record.rs` as the current record boundary and preserve its
one YAML parser. Keep ranking/resource inventory in focused sibling modules if
needed; expose operations through `builtin/memo/src/service.rs`. Update
`builtin/memo/tests/tests.rs`, `builtin/memo/README.md`, and the seed registration
only for behavior delivered in this stage. Bootstrap tests must cover new records
and preservation of existing ones; no automatic merge into an existing record.

Write the active declarations through the memo service. Extend `Input` and the
model descriptor together. Add regression fixtures that distinguish lexical
matching from link popularity, demonstrate exclusion behavior, and exercise
actual filesystem boundaries. Run focused checks, then `just all`.

## Result

Native integration implemented in `builtin/memo`, with resolver guidance composed
by the existing harness and operation-specific memo policy. Active declarations
were installed through validated writes; old reflex names were renamed to resolver
at the user's request. The old kern record remains untouched.

Verification on 2026-09-10: 16 focused memo tests passed; real cartridge/memo/harness
process smoke composed resolver guidance and preserved the user message without
a model request. Live resolution found decision instructions for “record a settled
choice” and the harness source for “change system prompt placeholder handling”.
The final `NEXTEST_TEST_THREADS=2 just all` gate passed formatting, Clippy, the
workspace tests, doctests and six Python lane tests. Initial default-parallel gate
hit the pre-existing search timeout. Enlarging the compaction fixture budget for
the expanded tool descriptor preserved and passed its compaction assertions.

Coverage is intentionally incremental: undeclared files are reported, not silently
classified. Observations are explicit caller reports, not independently verified
usefulness. Changes remain in the working tree; no commit or push was requested.
