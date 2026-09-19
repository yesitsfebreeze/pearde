---
complexity: medium
footprint:
  - src/evidence.rs
  - src/lib.rs
  - src/roster.rs
  - src/roster/capture.rs
  - src/roster/render.rs
  - .cartridge/tests/unit/roster_tests.rs
  - .cartridge/tests/integration/roster.test.ts
  - README.md
  - .cartridge/help.md
  - .cartridge/docs/roster.md
---

# Replace generic evidence collection with one bounded roster observation

## Inputs, dependency and landing

Requires the delivered `@harness/scoped-roster-context-contributor` receipt at
698a4dc9555a6b3ad8d46dcc5dd3a14463048e70. That receipt is historical behavior,
not proof of today's runtime. Analyzed Harness HEAD is
c8305341bb30b058c481bf023ebf977304248dab. Sessions integration source is pinned
to 499191501e7e3cbb1ac1537ea75a5f1906f97f21. Two inherited review rounds were
used; this executable spec requires fresh independent review within the three
remaining rounds.

Before implementation the coordinator must approve the two added module paths
in the PRD footprint and reconcile foreign edits in src/lib.rs, README.md and
.cartridge/help.md. Do not copy foreign assessment edits into the lane or sweep
them into collection. Rebase/review against a coherent committed owner if that
work lands first. Preserve ordinary Harness context and compaction operations;
only the obsolete discovery evidence protocol is removed. No Sessions, shared
bridge, process-test support, settings, manifest or lockfile edits are authorized.

## Implementation

1. Delete src/evidence.rs and remove `pub mod evidence` from src/lib.rs. Its
   generic Reference/Evidence/Candidate/Contribution/Task/Limits/Prepared,
   contributor scheduler, reference reader, privacy filtering and arbitrary
   contributor merging have no surviving caller besides roster. Do not copy
   those responsibilities under new names or keep a compatibility facade.
2. Keep roster::Config, host binding, Snapshot { block, info }, and the existing
   Sessions-v1 response validator in src/roster.rs. Factor only roster capture
   into src/roster/capture.rs and final block rendering into src/roster/render.rs.
   Internal records may contain validated roster rows, source metadata and a
   roster status, but cannot expose a generic provider protocol or collection
   API. Do not serialize roster rows to generic evidence and deserialize them
   again. Preserve response digest validation before allowlisting; duplicate
   IDs, inconsistent totals/source states, cross-actor unread data, oversized
   transport/fields and invalid revisions remain rejected atomically. Preserve
   allowlisted observations, unknown activity duration and null unavailable data.
3. Capture returns default Snapshot immediately when config is absent. Mismatched
   request session returns explicit unavailable info without constructing/polling
   a source request. Otherwise issue exactly one existing host.call("sessions",
   {op:"roster",access_token:host_secret,limit:config.max_rows,max_bytes:32768}).
   Use one monotonic deadline measured before that call; tokio timeout_at bounds
   waiting. Check the same deadline after validation and around bounded selection
   and rendering so a late response/CPU phase cannot be reported available.
   Drop the pending future on timeout; do not spawn retries or claim remote
   cancellation. A private helper accepting one roster-response future/closure
   is allowed for deterministic unit tests; no arbitrary contributor input.
4. Preserve fixed startup actor/credential binding and existing numeric settings:
   config defaults 200 rows, 1048576 block bytes, 10000 ms; positive cap checks;
   response transport bound32768; limits.roster_evidence_bytes remains an active
   intermediate roster-observation budget (default1048576, declared min1024).
   Do not resurrect the historical64-row/8192-byte/2000-ms configuration maxima.
   Sessions currently accepts up to100 requested rows; its rejection of the
   existing default200 is a separate pre-existing issue, not permission to
   redesign settings here. Prove supported explicit20-row configuration.
5. Render validated rows deterministically by id (the old collector's effective
   reference order). Charge the intermediate budget for serialized roster
   metadata and selected rows, and final config.max_bytes for the complete UTF-8
   escaped labeled block. Preserve whole rows; omit trailing rows until both
   budgets fit. Do not charge obsolete Reference/Candidate wrappers. Source
   omitted plus locally omitted rows determines `omitted`; unknown remaining
   counts remain explicit with source.remaining_unknown and total:null.
   `truncated` is true for producer omissions, unknown remainder, or local
   omission. Available/empty/partial/unavailable/timeout are explicit; local
   truncation need not pretend the upstream source became unavailable.
6. Retain inspection fields contributor="sessions.roster", state,
   composition_revision, deadline_exceeded, selection_reason, source,
   selected_rows, omitted and truncated. Successful/partial source keeps
   source_revision, observed_at, source_status, source_rows, source_omitted,
   remaining_unknown, total and the allowlisted named/mailbox source revisions.
   Empty successful roster is `empty`; partial stays partial even with zero rows.
   Source failures/malformed responses expose only bounded fixed reasons, never
   raw error text, credentials or rejected fields. When metadata cannot fit the
   prompt budget, preserve explicit unavailable inspection metadata, use a
   bounded fixed unavailable block if it fits, otherwise an empty block. Never
   exceed a positive max_bytes, even1. Keep source provenance in inspection if
   validation succeeded before a metadata-cap failure.
7. Define composition_revision as a SHA-256 over a deterministic roster-specific
   snapshot payload containing final selected rows, source projection metadata,
   status/reason, omissions/truncation/deadline flags and effective budgets,
   excluding the revision itself and credentials. Hash after final selection,
   so a render cap that changes selected rows changes the composition revision.
   Identical payload/budgets gives the same revision. Source revision remains
   exactly the validated Sessions digest, never rebranded as a global atomic
   state. No requirement to preserve the old protocol's hash bytes. All enabled
   outcomes, including unavailable/timeout/metadata-cap failure, have a revision.
8. Keep one captured Snapshot per resolved Request and reuse it through context,
   inspect and compaction. Append the labeled untrusted Swarm data after the
   existing instruction frame, using escape_frame after JSON serialization;
   never re-render template markers. Existing serialized request accounting and
   transcript protections remain unchanged.
9. Rewrite roster.test.ts's obsolete process-SDK harness into a disposable real
   base fixture. Its current HARNESS_BINARY/SESSIONS_BINARY/host.ts mechanism
   cannot execute current cdylibs. Build the lane's Harness module, use actual
   Sessions module code at the pinned revision, and real base process. Use
   temporary project/home/store directories, synthetic secrets with allowed
   HARNESS_ROSTER_* and SESSIONS_MAILBOX_* prefixes, explicit trust for fixture
   paths, and await bounded startup/shutdown. Never reload/stop the shared daemon.
   A fixture Lua adapter may load the real Sessions module, expose its real
   sessions/buffers operations, and count/delegate/intercept roster calls for
   fault tests; do not mock authentication, roster projection or store behavior.
   Use stock Harness init.lua/manifest. Fake only memo/router/JEV dependencies
   needed for deterministic prompts, summaries and assessment fallback. Keep all
   five existing test names and behavioral assertions, adding revisions/caps
   assertions described below. No test.skip/todo or success when artifacts are
   missing. Tear down each started process in finally/afterEach and await exit.
10. Correct roster.md's obsolete collector/cap/process claims and explain the
    local deadline, two budgets and source/composition revisions. Add a concise
    roster link/description to README/help while preserving unrelated content.

## Integration artifact preparation

The test file derives owner root from import.meta.url, never from an absolute
Harness checkout. HARNESS_MODULE optionally selects the already-built lane
module; otherwise find libharness.dylib/.so in the explicit CARGO_TARGET_DIR's
 debug directory. Fail if absent. The Verify build below creates it.

Before tests, resolve external CARTRIDGE_BIN (default
/Users/feb/dev/cartridge/cartridge.ctg/target/release/cartridge) and SESSIONS_REPO
(default /Users/feb/dev/cartridge/sessions.ctg). Record executable SHA256 and
Sessions commit. Require git cat-file of the pinned Sessions commit; git archive
that commit to a fresh temporary source directory, and build with
`cargo build --locked --lib --manifest-path <scratch>/Cargo.toml` using its own
CARGO_TARGET_DIR under the outer isolated target. Copy only that archive's
manifest/init and built Sessions module into the fixture. No dirty sibling source
or old process binary is used. These absolute external inputs do not select the
Harness-under-test. Each pass builds/tests its own cwd owner. Build fixture
preparation has a finite timeout and process cleanup; prepare once per test run.
The verifier records both owner revision/diff and external artifact hashes.

## Acceptance

- [ ] Only roster-specific capture/rendering remains: src/evidence.rs and its
      public module/wire protocol are absent; no renamed generic collector exists.
- [ ] Actual Sessions+Harness composition renders authorized20-session data once
      with outsider/transcript/inbox exclusion, fixed host credentials and
      escaped closing-frame/template-like observations; inspect makes no model call.
- [ ] Disabled and request-actor mismatch invoke no roster source; invalid digest,
      malformed identities/fields, secret-bearing upstream errors, partial/empty
      data and local deadline expiry have correct explicit metadata without leaks.
- [ ] Row cap, intermediate bytes and final escaped UTF-8 bytes are enforced with
      whole-row omissions including unknown totals and tiny metadata budgets;
      source digest is retained, and final composition revisions track selection.
- [ ] Compaction and automatic-refresh failure reuse a single captured roster;
      protected latest requests, prior summary and stored transcript survive;
      existing owner tests and checks pass without skipped behavioral proof.
- [ ] README/help/roster docs describe current roster-specific behavior/settings;
      collection contains no unrelated foreign source edits.

## Behavioral tests to add/preserve

Preserve the three existing unit names, adapting the old render unit away from
Task/Contribution/Prepared. Add these exact tests in roster_tests.rs:

- roster_capture_disabled_mismatch_and_failures_are_private: closure poll/call
  counter0 for disabled/mismatch,1 on valid/unavailable; arbitrary secret-bearing
  errors are absent from info/block; malformed accepted envelopes fail atomically.
- roster_capture_deadline_is_bounded_and_drops_pending_response: pending response
  future with Drop flag and short timeout; state timeout/deadline flag, no retry,
  drop observed, outer watchdog prevents hang; a response finishing after the
  deadline never becomes available. No wall-clock-only generous success assertion.
- roster_partial_empty_unknown_and_tiny_caps_are_explicit: valid partial/unavailable
  named/mailbox fixtures and unknown total, fully empty valid projection; measured
  UTF-8 length <= every configured block cap including1/1024, intermediate cap
  forces omissions independently of final cap; secrets/unknown fields excluded.
- roster_revisions_bind_final_selection_and_source_projection: frozen validated
  fixture and budgets hash equally; changing source content/revision, status,
  selected rows or caps changes composition hash, source digest stays unchanged
  when only local budget changes. Assert the small and full render have different
  hashes; check whole-row omission arithmetic and deterministic id ordering.

Keep integration test names below. Strengthen the first to assert explicit row
cap with a second max_rows=3 request, selected+omitted=20, private/forged exclusion,
phase update changes source/composition revisions, ack changes observed unread.
Strengthen fault test with resealed structurally malformed data and bounded local
elapsed time, deadline flag and secret-bearing error suppression. Keep corrupted
actual channel store partial behavior and exact transcript preservation in the
last two tests. Assert counters across context/inspect/compact, not just success.

## Verify and Proof

Every block runs first in lane then integrated repo, at repo-root cwd, with120s
per block. Prewarm dependencies outside collection if cold builds exceed120s;
never remove time bounds or accept a partial run. Scratch writes stay outside
footprint. Every cargo invocation, including fixture/nested builds, inherits or
sets an isolated CARGO_TARGET_DIR; never change the live module build output.

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/roster-contract-verify}"
cargo build --locked --lib
cargo fmt --all -- --check
cargo clippy --locked --workspace --all-targets -- -D warnings
test ! -e src/evidence.rs
if rg -n 'cartridge-context/v1|pub mod evidence|crate::evidence|\b(struct|enum) (Contribution|Prepared|Candidate|Reference|ContributorStatus)\b|FuturesUnordered' src/roster.rs src/roster src/lib.rs .cartridge/tests/unit/roster_tests.rs; then exit 1; fi
```

```test
run: CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/roster-contract-verify}" cargo test --locked --lib
pass: host_binding_rejects_bad_caps_and_never_accepts_request_credentials
pass: source_adapter_checks_identity_digest_revisions_bounds_and_private_inbox_fields
pass: final_render_is_escaped_after_template_and_accounts_whole_row_omissions
pass: roster_capture_disabled_mismatch_and_failures_are_private
pass: roster_capture_deadline_is_bounded_and_drops_pending_response
pass: roster_partial_empty_unknown_and_tiny_caps_are_explicit
pass: roster_revisions_bind_final_selection_and_source_projection
```

```test
run: CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/roster-contract-verify}" bun test ./.cartridge/tests/integration/roster.test.ts --reporter=junit --reporter-outfile="$PRD_TEST_REPORT"
pass: actual sessions and harness compose twenty scoped agents once with bounded escaped evidence
pass: disabled roster and copied request configuration never override host binding
pass: wrong identity malformed evidence source errors and deadline remain explicit nonfatal states
pass: partial actual channel evidence preserves phase and compaction uses the captured roster once
pass: failed automatic refresh preserves full fitting context and one captured roster
```

```test
run: CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/roster-contract-verify}" CARTRIDGE_BIN="${CARTRIDGE_BIN:-/Users/feb/dev/cartridge/cartridge.ctg/target/release/cartridge}" cargo test --locked --test process
pass: harness_projects_context_over_the_real_base
pass: harness_compacts_oversized_context_over_the_real_base
pass: harness_fails_safely_on_huge_turns_and_router_failures
pass: harness_fails_on_router_timeout_without_history_loss
```

```test
run: CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/roster-contract-verify}" CARTRIDGE_BIN="${CARTRIDGE_BIN:-/Users/feb/dev/cartridge/cartridge.ctg/target/release/cartridge}" cargo test --locked --test working
pass: rolling_memory_refreshes_below_budget_and_survives_reload_and_failure
```

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/roster-contract-verify}"
export CARTRIDGE_BIN="${CARTRIDGE_BIN:-/Users/feb/dev/cartridge/cartridge.ctg/target/release/cartridge}"
cargo test --locked --test ring --test slim
```

Independent verifier also inspects the implementation diff for renamed generic
protocol retention (a token scan cannot prove its absence), doc correctness and
foreign-change exclusion. Coordinator runs owner audit/isolation and root board
checks after source integration; leaf tests do not replace those composition gates.
