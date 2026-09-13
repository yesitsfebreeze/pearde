---
complexity: high
footprint:
  - src/ship.rs
  - src/store.rs
  - src/tool_result.rs
  - src/main.rs
  - init.lua
  - .cartridge/tests/unit/ship/tests.rs
  - .cartridge/tests/unit/store/tests.rs
  - .cartridge/tests/integration/reviewed-ship.test.ts
  - .cartridge/tests/integration/tool-result.test.ts
  - .cartridge/docs/ship.md
---

# Preview and publish one exact owned tree

Native tool.ship op=ship uses phase preview (default) or commit. Commit requires
expected_revision from preview; the old one-call commit/push path no longer runs
implicitly. Keep scan/undo shapes; remote push becomes a separate child contract.
Existing policy sees each phase's complete input and makes a separate decision.

Preview binds canonical repository/root identity, branch, HEAD, shared index digest,
exact session overlay ref, selected owned tree, author/committer identity, secrets
policy and configured required gate. Return the snapshot and its SHA-256 revision;
never touch shared index/worktree or create a branch commit during preview. Private
Git indexes/objects used to build the proposed tree are retained implementation work.
Use the existing automation identity by default; remove the invented Claude co-author.
Optional author identity comes only from validated host configuration, not model input.

Commit recomputes and compares the complete preview before gating, runs the configured
gate even with an explicit message, then revalidates under repository/session locks
and expected-HEAD CAS immediately before publication. Gate hold/error/malformed reply
or timeout refuses; bound the whole gate exchange, including body, not headers alone.
Secrets checks retain explicit reviewed force semantics; force cannot bypass a gate.
No missing-config model call is invented. Gate inputs bind the exact reviewed diff;
large diffs that cannot be fully gated refuse rather than silently truncate review.

Bound active invocation tracking; cancellation targets the trusted session/run/call/cwd
and sets a shared flag. Dropping an awaiting caller sets the same flag. Blocking commit
work checks cancellation before producing/publishing its commit; an already completed
CAS is not rolled back. Concurrent source/index/branch changes refuse with rereview
instructions; no automatic rebase or retry. Unpublished Git objects may remain after a
late CAS conflict. GitFS locks coordinate its own writers; expected refs catch external
Git updates, while arbitrary hostile filesystem writers are outside this contract.

The local result names commit/tree/parent/session/author and push=false. The source
branch and its working tree/index remain distinct: publishing a commit does not
materialize files or silently reset a user's index. Detached/unborn HEAD and unsupported
repository identity binding refuse explicitly. The supported boundary is macOS/Linux
filesystem identity; other targets must not pretend reviewed root identity is bound.

## Acceptance

- [x] The reproduced stale-preview unowned deletion fails safely; own overlay, root, branch, index, author or gate change invalidates preview and shared index/worktree remain unchanged.
- [x] Actual fixture gate hold/error/malformed/timeout refuses despite explicit message; successful gate publishes exactly the reviewed owned tree and accurate identity.
- [x] Concurrent attempts yield at most one publication; cancellation before CAS leaves history unchanged and completed publication remains explicit without retry/push.
- [x] Existing GitFS store/tool-result/consumer tests pass and native SDK fixtures prove preview/local commit without remote contact.

## Verify and Proof

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just test gitfs
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just check gitfs
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just build gitfs
GITFS_BINARY="$PWD/target/tool-result-contract/debug/gitfs" bun test ../gitfs.ctg/.cartridge/tests/integration/reviewed-ship.test.ts
```

Baseline in the parent records a real stale preview that deleted an unrelated newly
committed trunk file. Gate providers, author identities and repositories are fixtures;
no real remote push or model is used by this proof. Keep source changes owner-local.

Implementation clarification: the installed Git rejects a symbolic HEAD verification
and referent update in one transaction as duplicate HEAD updates. Instead prepare an
update of HEAD and verification of the overlay, then check the exact symbolic branch
while Git holds HEAD/referent/overlay locks, check cancellation, and commit the prepared
transaction. An actual probe confirms concurrent symbolic-ref refuses while prepared.
Shared index.lock spans this boundary. Consumer fixture receives a failing memo facade
provider to retain the prior no-recall tool-contract scenario after the proxy dependency
change. The init.lua comment now describes configured gate failure accurately.
