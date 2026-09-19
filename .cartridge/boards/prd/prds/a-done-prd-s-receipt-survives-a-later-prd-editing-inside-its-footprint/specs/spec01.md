---
complexity: 4
footprint:
- src/lifecycle.ts
- src/engine.ts
- src/cli.ts
- src/collection-proof.ts
- .cartridge/tests/collection-proof.test.ts
- .cartridge/docs/collection-proof.md
- README.md
- .cartridge/help.md
---

# Explicit current-commit verification with preserved provenance

## Source baseline and ownership

Canonical owner: @prd/a-done-prd-s-receipt-survives-a-later-prd-editing-inside-its-footprint.
Checked analysis claim: codex-lifecycle-prerequisite. Source HEAD when analyzed:
c1caed63. Existing dirty lifecycle changes add named test-block validation and
seeded submodule lanes; engine.test.ts includes corresponding tests. Those are
not this implementation and must be independently reviewed, verified and
committed as a narrowly identified necessary baseline before an implementation
lane starts. No service, ASP, help, README or other dirty work enters that baseline commit.
Implementation adds only focused committed-target/reverification usage sections
to README.md and .cartridge/help.md, preserving preexisting dirty hunks byte for
byte; these exact two documentation additions are reviewed in the lane diff.
The implementation modifies only the exact eight paths above. Existing suites
are executed but not rewritten. No loaded cartridge is rebuilt or replaced.

## Design

`collect <ref> --reverify` is an explicit checked operation on a done PRD. It
retains done state and refreshes commit/evidence only after executing the same
published contract against current committed HEAD. It implies a visibly named
committed target. `collect <ref> --committed` opts a normal collection into that
same target and never silently changes default collection behavior. CLI help
and the focused contract document describe both options. Other operations
reject these options. No automatic voucher or graph-wide provenance search.

Before re-verification, validate all old receipt integrity checks except current
source drift: done state, no claim or lane, ancestry of old commit, recorded
commit equality, passing prior proof, identical published specification hashes,
closed acceptance boxes, and committed exact old PRD/spec/receipt bytes. Missing
or changed historical contracts require normal reviewed implementation work;
re-verification cannot adopt them. Validate dependencies as currently verified,
not merely marked done. For containers, current child evidence may legitimately
have refreshed since the old receipt; rerun child completion checks and record
current child-contract hashes, preserving old hashes in history.

Verification uses a temporary detached worktree at the candidate commit with
pinned submodules seeded by existing logic. Validate it is clean both before and
after proof, except generated ignored build output. Run all published executable
blocks, including required named-test pass gates. Before receipt write recheck
source HEAD, record/spec hashes, dependencies/child contracts and cancellation.
Remove only the temporary verification worktree on all outcomes. Do not remove
or force-clean a user worktree. Failed proof retains the old done receipt and
therefore remains observably stale. A retry starts fresh.

For lane collection, verify lane edits, commit only declared lane paths, confirm
candidate diff stays inside footprint, and fast-forward source using existing
guards. Verify the committed candidate independently in the detached snapshot.
Live dirty paths are never staged by committed-target collection: without a lane,
require no uncommitted intended implementation and certify HEAD only. Existing
Git merge protection refuses overlap with live dirty paths. Never stash or
rewrite a preserved README/help tail. Source HEAD must equal the candidate at
receipt publication. Existing non-committed collection remains unchanged.

New receipts explicitly record `verification-target: committed`, candidate SHA,
spec digests, child contracts, and separately observed workspace drift paths and
content hashes. Drift includes tracked/staged differences and untracked files
inside footprint; do not store file contents or secrets. The receipt body names
the detached verification cwd/commit and executable evidence. Public status adds
`verification_target`, `workspace_verified`, and `workspace_drift` while existing
`verified`/`integrated` refer explicitly to the named target. Workspace verified
is false whenever footprint differs from the verified artifact; it is not inferred
from a committed test pass. Empty footprint/container semantics follow children.
Consumers see this limitation in collection output and status, including a false
workspace flag. Final memory loaded-artifact verification remains independent.

For committed-target receipts, completion compares receipt commit to current
HEAD within the footprint; any committed drift invalidates it. Dirty workspace
changes do not invalidate committed proof but are reported independently. Legacy
receipts without the explicit target retain today's strict committed-plus-dirty
comparison. No source drift becomes trusted merely because a later PRD is done.

Before replacing collection.md, save exact prior bytes under
`collection-history/<sha256-of-bytes>.md`; reject an existing history file with
different bytes. New receipt carries previous receipt digest/path and original
integration commit. Include history and updated receipt/PRD in the same scoped
record commit. Validate referenced history recursively by digest and committed
bytes, bounded by the acyclic hash chain. No history rewrite, deletion, or migration
of existing receipts. Publication must restore prior record bytes/engine fields
if record commit fails, leaving any valid source integration available for retry;
never reset other repository changes. Existing record index guards remain.

## Recovery and migration

No automatic migration. Old strict receipts may be upgraded only by explicit
successful re-verification. Failed/cancelled verification cannot overwrite old
proof. Source races refuse before publication. Post-integration failure leaves
source integrated and the PRD uncollected, preserving evidence for checked retry.
Detached snapshot cleanup cannot delete active implementation lanes. History
integrity failures remain actionable refusals, never automatic repairs. Existing
claims, deferred automatic-voucher work and all four review rounds remain intact.

## Acceptance

- [x] `explicit reverify refreshes committed drift and preserves prior receipt` passes, while ordinary collect(done) still refuses stale proof.
- [x] `reverify refuses changed contract missing proof and active ownership` passes without mutating old receipts.
- [x] `reverify refuses unresolved dependencies and failing proof` passes; committed drift remains unverified after failure.
- [x] `committed collection preserves dirty tails and reports workspace drift` passes with byte-identical dirty README/help and no dirty paths committed.
- [x] `legacy receipts remain strict and later committed drift needs reverify` passes.
- [x] `reverification refreshes child rollups without automatic vouchers` passes after explicit child reverify, then parent reverify.
- [x] `verification races cancellation and history tampering fail closed` passes with no premature receipt update or lost changes.
- [x] `committed verification tests committed bytes rather than dirty workspace` proves a workspace-only fix cannot make broken HEAD pass.
- [x] Engine and records fixture/migration tests pass against the clean candidate; the full unchanged records suite passes independently against the identified canonical live dataset with matching code hashes; TypeScript passes and no loaded artifact was replaced.

## Verify and Proof

```sh
bun install --frozen-lockfile
```

```test
run: bun test ./.cartridge/tests/collection-proof.test.ts --timeout 30000 --reporter=junit --reporter-outfile="$PRD_TEST_REPORT"
pass: explicit reverify refreshes committed drift and preserves prior receipt
pass: reverify refuses changed contract missing proof and active ownership
pass: reverify refuses unresolved dependencies and failing proof
pass: committed collection preserves dirty tails and reports workspace drift
pass: legacy receipts remain strict and later committed drift needs reverify
pass: reverification refreshes child rollups without automatic vouchers
pass: verification races cancellation and history tampering fail closed
pass: committed verification tests committed bytes rather than dirty workspace
```

```sh
bun test ./.cartridge/tests/engine.test.ts --timeout 30000
```

```sh
bun test ./.cartridge/tests/records.test.ts --timeout 30000 -t 'the accepted-states check|migration preserves'
bun run check
```

## Canonical live-dataset gate

Before collection, an independent verifier must also run the full unchanged
records.test.ts from /Users/feb/dev/cartridge/prd.ctg against the current live
board. Prove that src/records.ts, src/planner.ts and records.test.ts hashes match
the candidate. Record the live dataset manifest digest and UTC observation time
in verification evidence. The full command is `bun test
./.cartridge/tests/records.test.ts --timeout 30000`. Failure blocks collection.
This audit proves only the identified live dataset, not the committed board
snapshot. The clean-HEAD graph test fails because an unrelated runtime declared-
settings child is untracked; preserve that limitation rather than copying or
committing unrelated records. All fixture/migration tests still run on the clean
candidate. The unpublished proposal and initial dataset manifest remain under
proposals/verification-amendment.md and verification-amendment.dataset.json.

## Limits

Only committed artifacts gain opt-in certification; live dirty or loaded artifacts
remain unverified until separately tested. No historical contract changes are
adopted, automatic voucher strategy implemented, or deferred performance work
resurrected. Test blocks remain subject to existing 120-second process limit;
split executable blocks if measured suite time threatens that limit, preserving
all named gates and obtaining review for substantive contract revisions.
