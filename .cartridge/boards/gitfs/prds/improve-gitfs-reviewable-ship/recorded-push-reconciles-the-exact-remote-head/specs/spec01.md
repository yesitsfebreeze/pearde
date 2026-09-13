---
complexity: high
footprint:
  - src/main.rs
  - src/ship.rs
  - src/store.rs
  - src/push.rs
  - src/tool_result.rs
  - .cartridge/tests/unit/push/tests.rs
  - .cartridge/tests/integration/recorded-push.test.ts
  - .cartridge/docs/push.md
---

# Record one ordinary push against the exact advertised remote head

Extend native tool.ship with op=push and phases preview, commit and reconcile.
Preview/commit name a configured remote, exact refs/heads/* ref, full local commit
OID and expected_remote_head (full OID or null for a new ref). Commit additionally
requires the preview's expected_revision and a caller-chosen operation_id. Reconcile
accepts only operation_id and reads its recorded binding; it never sends a push.
Use trusted session/run/call/cwd from the existing tool boundary and cancellation
registry. No router, inference, fetch, rebase, reset, force flag or automatic retry.

Resolve one configured push URL and bind its SHA-256 identity (never persist or
return raw URLs), exact repository filesystem identity, session, remote name/ref,
local commit and expected remote OID plus configured deadline in the preview hash.
Remote names are bounded safe names, refs are bounded validated branch refs and OIDs
are complete SHA-1/SHA-256 hex. The named local commit must be a commit carrying
exact Shipped-by, Gitfs-Session and Gitfs-Review trailers from local reviewed ship.
Expected remote objects must already exist locally and be ancestors of the target;
an absent expected ref uses Git's all-zero advertisement. A remote already at the
target needs no push and is reported explicitly. Preview uses bounded ls-remote to
verify the exact expected ref. Refuse multiple push URLs, mirrored remotes, configured
URL rewrite rules, malformed/oversized output or unsupported platforms. Refusing
URL rewrite rules avoids ambiguous double rewriting when a resolved URL is used.
Host Git configuration/credentials remain trusted transport configuration; arbitrary
hostile filesystem writers or helpers that deliberately escape their process group
are outside the supported macOS/Linux boundary.

Commit rebuilds the preview binding and refuses changes. It then reserves the
operation and destination in a private durable store under the repository's GitFS
store. Atomic fsynced record publication precedes spawning git push. At most 128
records, each at most 4096 bytes, are retained with no automatic eviction: capacity
refuses new attempts rather than forgetting replay protection. A record contains
only bounded binding fields, revision, operation identity and fixed status/reason;
no URL, credentials, diff, transcript or raw transport stderr. Corrupt/oversized
records fail closed. A repository-wide lock serializes reservations and updates.
Repeated operation IDs return the same attempt without redispatch; conflicting
reuse fails. An unresolved attempt blocks a new ID for the same URL/ref destination.
Records and their guards survive cartridge restart; an interrupted attempt remains
unknown and is never replayed. Local commit objects and history remain available.

Use ordinary git push of the exact commit:ref and a private operation-owned pre-push
hook, overriding the store's usual disabled hooks only for this command. Disable
follow-tags, mirror and recursive submodule pushes. The hook accepts exactly one
update and checks its local OID, destination ref and advertised old OID against the
record. Extra/missing updates or mismatches refuse before Git can publish. The hook
writes a bounded durable result; only its explicit refusal proves no update was
sent. After it permits the update, ordinary Git's server CAS binds that same
advertisement. A separate ls-remote check alone is never the publication guard.
All helpers run within the command's process group, terminated/reaped on timeout,
cancellation, output overflow or caller drop. Read stdout/stderr under fixed 64 KiB
caps and one absolute configured push_timeout_ms deadline (default 10000, valid
100..60000), including local checks, hook and remote reads. No interactive prompts.

An attempt is durable unknown before dispatch; cancellation before spawn may record
refused, but any crash or unacknowledged post-dispatch outcome remains unknown. Hook
refusal is definite refusal. Otherwise completion requires exact recorded remote
readback equal to the attempted commit, either after the push or during later
read-only reconciliation. Old/different OIDs or unavailable readback alone cannot
prove refusal: the remote may still apply the update or may already have advanced.
Reconciliation revalidates the stored repository and configured URL identity, retains
unknown on configuration drift, and never accepts a caller-supplied replacement
binding. Fixed statuses confirmed/refused/unknown and explicit reasons tell callers
whether the observed target is confirmed or the attempt needs reconciliation.
Positive confirmation stays historical evidence even if a later read sees advance.

## Acceptance

- [x] A real bare remote accepts only the exact reviewed local commit and expected advertised old OID; old/different OIDs and non-ancestor targets refuse, including a remote advance inside the pre-push boundary, without force, history rewrite or changes to unrelated refs.
- [x] Durable attempt publication precedes dispatch; duplicate IDs and unresolved destinations never resend, including fresh process instances. Capacity/corrupt records and changed repository/remote/commit/ref bindings fail closed.
- [x] Lost replies, timeout, cancellation and process cleanup preserve unknown after dispatch; exact remote readback alone confirms later completion. Old/different/unavailable readback cannot invent refusal; reconcile sends no mutation.
- [x] Public GitFS tests/check and actual native SDK fixtures prove the phases, reviewed commit requirement, secret-free records, bounded output/time and helper cleanup with disposable repositories and no external network.

## Verify and Proof

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just test gitfs
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just check gitfs
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just build gitfs
GITFS_BINARY="$PWD/target/tool-result-contract/debug/gitfs" bun test ../gitfs.ctg/.cartridge/tests/integration/recorded-push.test.ts
```

The native baseline proves this operation was absent at local-publication source
67ef4ac. The recorded disposable Git2.50.1 probe proves hook rejection and actual
server CAS refusal when a remote advances after advertisement. New fixtures will
use owned local helpers for lost-response/hang/overflow cases; no real remote or
credentials are used. Root collection and overlapping receipt refresh stay with
the coordinator. Inherited review rounds1–2 remain counted.
