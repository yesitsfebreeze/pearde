---
complexity: moderate
footprint:
  - src/drift.rs
  - src/lib.rs
  - src/changes.rs
  - src/change_record.rs
  - src/limits.rs
  - cartridge.json
  - README.md
  - .cartridge/help.md
  - .cartridge/tests/unit/main/drift_tests.rs
  - .cartridge/tests/unit/main/tests.rs
  - .cartridge/tests/unit/main/change_records_tests.rs
  - .cartridge/tests/integration/change-records.test.ts
  - .cartridge/docs/change-records.md
---

# spec01 — Sessions retains file observations and reports later drift

This is the proposed fifth and final authorized substantive revision of
`@sessions/file-drift-awareness`. Rounds 1–4 failed at 66, 71, 74 and 88. Those
results remain authoritative history; this revision has no score yet.
Source baseline: Sessions `499191501e7e3cbb1ac1537ea75a5f1906f97f21`.

## Delivered outcome and dependent outcomes

No live end-to-end read/turn behavior is delivered by this footprint alone.
Sessions owns the observation and comparison. Its `touch` operation has no
live file-read caller and the new `drift` operation has no live turn caller.
The following owner records preserve the whole requested outcome:

| PRD acceptance | Evidence here | Required live integration |
| --- | --- | --- |
| Reading records a stamp | Executed `touch` and later mutation test | `@fs/a-read-stamps-the-file-it-returned`, which needs this leaf |
| A changed file is named next turn | Executed comparison and rendered report | `@harness/the-turn-names-the-files-that-changed-underneath-it`, which needs this leaf |
| Own writes are not drift | Executed `touch`, write, `record_changes`, comparison sequence | Harness must call `drift` to expose the rule |
| Deleted is distinct from changed | Executed comparison and text assertions | Harness delivery |
| No changes produces no report | Executed null/absent-key/no-notification assertions | Harness omits the block |
| Offline disposable-directory tests | Named tests below | No sibling runtime required |

Do not tick the original live read/next-turn acceptance merely because the
Sessions mechanism passes. The coordinator must retain these successor links
and obtain their integrated evidence before claiming that composed outcome.
The historical `just test sessions` and `just check sessions` names refer to
the owner's tests/checks; current workspace entry points are `./task test
sessions` and `./task check sessions`. The standalone Cargo gates below do not
require copying the foreign task-command migration into the lane.

## Current source and boundary

`Session.files` is a `BTreeSet<String>`. `touch` inserts an unvalidated string;
`changes::append` adds validated evidence paths only for new accepted records.
An idempotent replay adds no new path and must not refresh observations: doing
so would hide a later external edit. `change_record::normalized` already
requires an absolute lexical-normal path, including rejection of `..`, `.`
and duplicate separators through its reconstructed-path equality check.
Use that one rule for both producers. This is lexical identity, not symlink or
inode canonicalization; hard links and symlink aliases are distinct keys.

`Session` is cloned by the existing candidate-publication paths and declares
`deny_unknown_fields`. Add a cloneable, `#[serde(skip)]` stamp map. Do not add a
serialized key, another store, or a sibling dependency. `Store::install` has
four callers: `Store::load`, post-rename recovery in `publish_checked`,
`repair_empty`, and `SharedStore::refresh_mapping_target` in `src/mapping.rs`.
The last is used by live `mapping` and `connect`. Preserve resident stamps
across these installs rather than comparing against a newly sampled baseline.

Unlike earlier prose, `repair_empty` cannot replace a resident valid session:
it refuses `self.sessions.contains_key(id)`. Its legacy decoder also requires
an empty `files` list. A real repair therefore installs an absent session with
no paths; do not invent a repair fixture containing touched files. Subsequent
`touch` uses the ordinary observation path.

The live working tree has foreign edits in manifest/README/help. Implement
from the pinned committed base in an engine lane, edit only these thirteen paths,
and preserve the live foreign edits. Integration waits for source ownership
reconciliation; never include those edits merely to make collection possible.

## Observation, bounds and persistence semantics

`Stamp` is internal, cloneable and equality-comparable: `Absent`, or
`Present { mtime_ns, len }`. It need not derive Serde because it is not stored.
`observe(path)` returns `Option<Stamp>`: metadata and modified time success
produce `Present`; `NotFound` or `NotADirectory` produce `Absent`; every other
metadata/time failure produces `None`. An indeterminate observation preserves
an existing stamp and produces no report. Do not unwrap pre-epoch time
conversion or classify a permission error as disappearance. A same-length
rewrite with unchanged modification time is not detected; neither content
hashing nor filesystem watching belongs to this metadata feature.

Add `limits.stamps` to `cartridge.json`, default 4096, minimum 1, maximum
1048576, and `stamps: usize` to `src/limits.rs`. `Limits::declared` reads the
default from the document. No second Rust default and no new environment
setting. The map contains at most that many keys per session.

For live `touch` and newly accepted `record_changes` paths, refresh an already
tracked key even at capacity. Admit a new key only below capacity and only if
observation is determinate. Existing tracked keys are never evicted just to
admit another. This is first successful admission order, not a promise of
lexicographically smallest live paths. `files` continues recording all touched
paths. Above the cap, newly touched paths remain in `files` but have no drift
coverage until a later eligible observation or cold rebuild admits them.

On a genuinely absent-session install, rebuild from at most the first
`limits.stamps` entries of decoded `files` in BTreeSet order. Validate each
candidate with `normalized` before statting it; invalid legacy strings remain
in `files` for snapshot compatibility but are never observed. Invalid or
indeterminate candidates consume this cold inspection budget; do not scan an
unbounded legacy set looking for 4096 valid files. On resident install, move
its old stamp map to the incoming session, retaining only keys still in the
incoming `files`. Do not observe or fill previously untracked keys in this
branch. An empty resident map is still resident and must not trigger rebuild.
This bounds the added resident work by the capped map (membership checks in
`files`) and prevents mapping/connect from acknowledging an external edit.

The cold rebuild observes current disk, so changes made while the old store
was absent, including a host restart, are absorbed. Stamps are intentionally
not durable. Live mapping/connect and post-rename recovery do not absorb a
tracked external change because they retain resident observations. A session
removed after an unrecoverable snapshot decode has no resident knowledge to
preserve; a later successful load is cold. These limits must be in README and
help, alongside the cap's silent partial coverage. The cap bounds added stat
counts, not syscall latency or the pre-existing size of `files`/snapshots.

A sweep visits only tracked keys, observes once per key, and keeps old stamps
on indeterminate results. `Present -> Absent` is gone; every other unequal
pair is changed, including recreation after absence. Replace each determinate
stamp with the current value, never remove it on reporting. Thus each observed
transition is reported once and later transitions remain detectable. Lists
are disjoint and deterministically ordered by the map. Render a header and a
line per path explicitly saying changed or gone; paths are data, not commands.

## Frozen public reply

Changed report:
`{"id":"...","report":"<rendered string>","changed":["..."],"gone":["..."]}`.
The three report fields are flat siblings; `report` is never an object.
No change: exactly `{"id":"...","report":null}`, with no changed/gone keys.
The no-change arm returns changed-id `None`, so no snapshot publication or
session notification occurs. A changed report returns `Some(id)` through the
existing publication path, committing the refreshed in-memory observations.
The existing error/uncertainty behavior of publication remains in force.
The Harness successor must consume this exact shape; its historical failed
round incorrectly treated `report` as an object and is not a contract change.

## Implementation steps

1. Make `change_record::normalized` `pub(crate)`; keep its definition intact.
2. Declare `mod drift;` in `src/lib.rs`, add the skipped stamp field to
   `Session`, and implement observation, bounded admission, cold baseline and
   sweep responsibilities in new `src/drift.rs`. Disjoint-field borrows are
   legal Rust; no clone of `files` is needed for a helper borrowing `files`
   and `stamps`. Choose helper signatures for clarity, not the old false
   borrow-checker justification.
3. Add the declared cap and matching typed field together.
4. Validate `touch` before any mutation, add its path to `files`, and observe
   through the bounded admission helper. Refuse relative and absolute but
   unnormalized strings with a clear path-format error.
5. In `Store::install`, obtain resident stamps before replacing the session.
   Carry them forward and prune only keys absent from incoming `files`; else
   cold-baseline the incoming session. Keep existing buffer and ID handling.
   Put this decision in `install`, not only in the `Store::load` loop.
6. Add the mutating `drift` arm to `sessions_inner`, honoring the frozen reply
   and changed-id contract. Existing clone/publication machinery remains.
7. In `changes::append`, observe each newly accepted path in `added` before it
   is moved into `files`. Refresh existing keys at capacity. Do not observe
   an idempotently replayed record or a rejected batch; existing candidate
   rollback prevents failed-before-publication observations from escaping.
8. Update event description, README and help for `drift`, strict `touch`, the
   cap, cold baseline, metadata ceiling and missing live successor callers.
   Preserve unrelated command declarations from the chosen committed base.
9. Attach new `.cartridge/tests/unit/main/drift_tests.rs` to `src/lib.rs` with
   `#[cfg(test)]` and the established explicit `#[path = ...]` pattern.

## Caller and documentation migration (B9 and F17)

Strict touch is a deliberate input-contract change. Preserve legacy strings
already persisted in `files`; new calls must be absolute and normalized. There
is no temporary relative-path adapter. The complete current call-site sweep
found these owned migrations, all included in the thirteen-path footprint:

| File | Migration and preserved assertion |
| --- | --- |
| `.cartridge/tests/unit/main/tests.rs` | In `every_pre_rename_failure_preserves_all_mutations_and_notifications`, replace `changed.rs` with `dir.0.join("changed.rs")`. The target may be absent; do not create an extra store-directory file that defeats the existing one-snapshot/no-temp-leak count. Keep all three injected fault variants, the `injected` error assertion, unchanged memory/snapshot checks and absent notifications. In `unattached_buffers_remain_memory_only_and_survive_other_session_commits`, replace `x` with `dir.0.join("x")`, retaining scratch contents and restart exclusion. In `a_session_round_trips_through_its_file`, replace `a.rs` with `dir.join("a.rs")` and assert that exact absolute value in files; preserve agent, transcript, buffer, deletion and restart assertions. |
| `.cartridge/tests/unit/main/change_records_tests.rs` | In `publication_identity_deduplicates_only_same_publication_and_keeps_legacy_projection`, remove the invalid new touch. After setup, drop the Store, parse its saved snapshot, set session.files to the literal `["legacy arbitrary path"]`, write it and load a fresh Store. Assert diagnostics empty and that exact legacy entry retained before exercising new records. Retain all duplicate receipt, byte-stability, conflict, count, revision, transcript and public projection checks. Assert the invalid legacy key is absent from stamps. Do not replace the legacy string with a valid path and thereby erase compatibility coverage. |
| `.cartridge/tests/integration/change-records.test.ts` | For both legacy setup sites, await the native service's stop before editing its saved snapshot. Set files to `["legacy noncanonical path"]` or `["legacy"]`, then launch a fresh Native using the same session-data directory and continue the existing assertions through that instance. The helper may return the replacement instance; no call may use the stopped one. Retain existing native test names and every exact metadata/byte-preservation, receipt, page, restart, diagnostic and corrupt-file assertion. Assert legacy files remain visible and an unchanged drift call answers null; the Rust legacy-load test separately inspects exclusion from stamps. Leave child tracking and afterEach cleanup active for all instances. |

The native `context.test.ts` call uses `/PRIVATE-FILE`, which already meets the
new lexical rule and remains unchanged. Other read/write producers are still
the explicitly recorded FS/Harness successor work; do not weaken touch to
accommodate fixtures. Before implementation completion, repeat the touch caller
search including hidden `.cartridge` test directories and inspect any new
caller rather than assuming this inventory is permanently complete.

Add one native test in the already owned change-records integration file,
named `native touch requires normalized absolute paths and reports later drift`.
Use a separate disposable observed directory in the existing dirs cleanup
registry, create a file, touch its normalized absolute path successfully,
rewrite longer and call drift through Native; require exact changed/gone
lists and a rendered string, followed by the exact null reply. Reject a
relative string and literal absolute `/../` and `/./` strings through Native;
require a path-format error and unchanged snapshot bytes. This proves the
candidate dylib actually supplies the strict touch/drift behavior over the
real host, in addition to preserving the four migrated native fixtures.

Update `.cartridge/docs/change-records.md` in the same change. `get.files`
remains a metadata projection and conveys no authorization; touch now performs
bounded in-memory metadata observation. Evidence validation remains lexical,
not content verification or ownership proof, while accepted new record paths
also refresh those observations. `changes` page reads remain read-only. State
that metadata observation is not reading or verifying file contents. Keep the
provider-reported trust, publication uncertainty, capacity and legacy snapshot
claims that remain true; remove the broad display-only/no-file-access promises
that no longer describe touch/accepted writes.

There is one root-owned caller outside this leaf:
`.cartridge/tests/integration/jev-reliability.test.ts:28`, foreign and untracked.
The coordinator has now migrated just that argument to
`path.resolve(cwd, "jev.ctg/src/assess.ts")` using its existing import. The
before bytes, exact patch and owner handoff are retained in this report directory
as `root-jev-fixture-before.ts`, `root-jev-fixture-normalization.patch`, and
`root-jev-fixture-handoff.md`. Current file SHA-256 is
`e101e2aab73a74ebe26edec2e54b669105515868dd3813b8d9c18764321e30ec`.
The analyst re-read the changed call and handoff. The coordinator verified
TypeScript syntax and that the resolved argument is an existing normalized
absolute path; the opt-in real JEV reliability test was not run.

The existing root JEV owner must preserve that edit on its eventual landing
and run its affected gate with the identified Sessions artifact. Before Sessions
integration, recheck the actual current call site and owner reconciliation;
the untracked status and this handoff are not a committed receipt or live JEV
proof. This absolute form works with old and new Sessions, so migration happens
before strict Sessions and requires no reverse dependency on the finished JEV
product. If the relative call returns or ownership reconciliation is missing,
keep integration blocked while the lane can still be completed. Do not
edit/adopt/stage the root file in the Sessions lane, delete or skip its test,
or describe syntax/path checks as live assessment verification. Its existing
opt-in live gate remains with its root owner and is separate from this offline
Sessions gate.

## Named behavioral tests

Use two disposable directories, store and observed work, cleaned on drop.
Use the existing local `Dir`/setup shapes in `change_records_tests.rs`,
`mapping_tests.rs` and `tests.rs`; edit the two existing unit files only for the
caller migrations below. Do not edit mapping_tests.rs or import a sibling.
Every rewrite changes length as well as content. No sleep-based timestamp
assumption. Tests call the real Store/SharedStore paths, not stand-in sweeps.

- `a_read_file_is_stamped_so_a_later_change_is_named`: create a normalized
  absolute file, touch, rewrite longer, drift, assert it appears in changed.
  Refuse a relative string and separately literal absolute strings containing
  `/../`, `/./` and repeated separators. Construct the malformed strings
  without PathBuf normalization. Assert each rejection leaves files, stamps
  and snapshot bytes unchanged. A mere is_absolute guard must fail here.
- `a_changed_file_is_named_apart_from_a_deleted_one`: touch two existing
  files, rewrite one and delete the other, assert exact disjoint changed/gone
  lists and text distinguishing both. Recreate the deleted file, assert it is
  changed next time and then silent. This gates persistent absent stamps too.
- `a_file_the_session_wrote_is_not_named_as_drift`: touch w and o, rewrite
  both, accept valid fresh evidence only for w, drift names only o. Change w
  again and assert drift now names w. Replay the old evidence after another
  external rewrite and assert w is still named; duplicate receipt processing
  must not acknowledge an unrelated external edit.
- `a_reported_change_is_not_reported_twice`: touch, rewrite, report, null,
  rewrite again, report again. Removal of the stamp cannot pass.
- `nothing_changing_answers_no_report_at_all`: establish two stamped files,
  assert the exact null reply and returned changed-id None; use SharedStore
  as well to assert notification None and unchanged snapshot bytes.
- `a_reloaded_session_is_restamped_from_its_touched_files`: touch and save,
  drop the old store, load fresh, rewrite, drift names the path. Also put
  relative and absolute unnormalized legacy entries into a literal snapshot;
  fresh load must retain those files strings but create no stamps for them.
  Assert the normalized good key is tracked, so rejecting all entries fails.
- `mapping_and_connect_preserve_unreported_resident_drift`: create a real
  SharedStore and mapping using the fixtures' actual mapping/connect requests.
  Touch a file, rewrite, perform mapping lookup then reconnect, and only then
  drift: the path must be reported. Repeat in a fresh fixture for each scope
  (durable client context and connection-local context) and operation
  individually, so one path cannot hide the other's reset. After each report
  rewrite again and observe another report. Assert a successful real request,
  not merely a direct call to install. This tests live refresh, not cold load.
- `post_rename_recovery_preserves_unreported_resident_drift`: touch p,
  rewrite externally, set existing `Fault::DirectorySync`, mutate an unrelated
  buffer through Store, assert `persistence_uncertain` and the visible buffer
  update. Clear the fault and drift; p must still be named. Use the existing
  `post_rename_failure_reports_uncertainty_and_reloads_visible_state` setup
  pattern. This executes publish_checked's recovery install. Do not use touch
  of p as the fault-triggering mutation, which would acknowledge p itself.
- `repair_of_empty_legacy_session_keeps_normal_drift_behavior`: reproduce
  the existing real empty legacy repair fixture and expected-revision call;
  assert backup bytes and empty files/stamps after repair, then touch a real
  file, rewrite, drift names it. Repair of the now-valid resident session is
  refused and leaves its observations intact. This tests repair's actual
  empty-only scope, not a fabricated touched-file repair.
- `stamp_capacity_preserves_existing_observations`: run this test's scenario
  in a subprocess of the current test executable with an explicit private
  child marker and exact test filter, installing a declared Limits copy with
  stamps=2 before any Store access. The parent asserts child success and
  captures failure output. This isolates OnceLock from all other tests.
  Touch a,b,c; assert files includes all three but stamps only a,b. Rewrite all
  and record a new own-write receipt for a at capacity; drift names only b,
  not a or untracked c. Rewrite a again and assert it is named. A fresh load
  of that snapshot tracks only the first two sorted candidate keys and does
  not track c; mutate after reload and assert that same coverage. Include an
  invalid legacy first candidate in a separate cold case and assert it is
  skipped without scanning beyond two candidates. Assert lengths stay <=2.
- `stamps_are_not_written_into_the_session_snapshot`: touch, establish a
  nonempty internal stamp map, parse saved JSON and assert Session's exact
  existing key set: id,name,cwd,buffers,files,agent,created,updated,revision,
  parent,transcript, with only change_log/mailbox_lineage/mailbox_cursor
  optionally added. Fresh load has no diagnostics and contains the session.
  This is a compatibility invariant, not a test expected to fail on the old
  implementation in isolation; the nonempty-map precondition is essential.

## Acceptance and proof limits

- [ ] Strict touch and validated write evidence use one path identity, preserve
      own-write suppression, and keep later external edits observable.
- [ ] Changed and gone are distinct; repeated unchanged sweeps are silent;
      the exact frozen reply and no-change publication contract are met.
- [ ] Cold load restores bounded observation, live mapping/connect and
      post-rename recovery retain unreported resident drift, and empty-only
      repair retains its original safety restrictions.
- [ ] Admission/cold traversal obey the declared cap without preventing refresh
      of existing tracked keys, and snapshots gain no new serialized field.
- [ ] All named tests run offline, owner tests/checks pass, and manifest,
      README and help state the actual consumer boundaries and limitations.

Review history already preserves the defeated vacuous write test (B1),
unwitnessed reload scope (B6), and absolute-only validation (B8). These cases
now have concrete preconditions and distinct observable paths above. There is
no claim that named tests or mutation gates prove their own honesty. Under
review-plan.md's gate-design ceiling, independent diff reading is the backstop:
inspect real caller wiring, cap checks, preservation versus re-baselining,
replay handling, error classification and the assertions themselves. Do not
spend the remaining rounds designing self-policing tests. Permission/EIO
classification and pathological filesystem latency remain explicit diff-review
facts; no portable chmod-based test is claimed to prove them.

## Native artifact preparation and verification

Native proof uses the existing `.cartridge/tests/integration/native.ts` helper
unchanged. It copies the candidate manifest/init.lua and explicitly selected
dylib into a disposable cartridge home and project, and starts its own daemon.
It never needs the shared workspace daemon. Never rely on its newest-module
fallback or the stale sibling release binary.

The coordinator currently has a compatible committed host artifact built from
`cartridge.ctg` commit `b4345b6dc5d03d33900ff7fb793f7dd752f5757d`:
`/tmp/roster-current-host-target/debug/cartridge`, SHA-256
`b081f7d1b9aab6c1130bb61ee4ec356931b65483dcac7e88c998ca283ff6dc75`.
The analyst rechecked this hash; that is artifact identity, not a claim that
this unimplemented Sessions candidate has passed native tests. Prepare a copy
as `target/file-drift-host/cartridge` in each verification cwd (lane and target)
after checking the source artifact hash. The gate checks the copied identity.
This is ignored scratch preparation outside the footprint, not a sibling source
or fixture dependency. If the artifact disappears, export that committed host
to a separate disposable checkout, build it offline with an isolated target,
and record its provenance/hash and compatible startup evidence before using
it; an alternate artifact requires a recorded verifier-approved identity
update, never silent use of the live dirty host. If offline host preparation
cannot succeed, the native gate is blocked, not waived or replaced by Cargo.

The native build block creates this candidate's cdylib explicitly with
`cargo build --offline --locked --lib`, in the same isolated target used by
Rust verification. The current environment is macOS, matching native.ts's
existing dylib contract. The native test command names that exact module and
prepared host. A short disposable XDG_RUNTIME_DIR is created with mktemp;
trap removes it after the test and its fixture cleanup terminate. Existing
native stop/afterEach paths must reap every daemon/follow process; inspect
failures for survivors and terminate only fixture-owned processes before
ending a worker. No downloads or shared daemon restart are authorized.

## Verify

The engine runs each block from the Sessions repository root in the lane and
integrated target, with its normal timeout. This block sets an isolated target
unconditionally to avoid replacing the live dylib. A populated offline Cargo
cache is a prerequisite; no download is authorized here. Historical round-3
measurements were observations at an older source head: filtered cold build
9.97 seconds, whole suite 92.97 seconds wall; they are not promises for this
revision. Implementation must measure the named suite, and must not drop
required tests to fit a timeout.

```test
run: env -u CARTRIDGE_YOLO CARGO_TARGET_DIR=target/file-drift-verify cargo test --offline --locked --manifest-path Cargo.toml -p sessions --lib drift_tests
pass: a_read_file_is_stamped_so_a_later_change_is_named
pass: a_changed_file_is_named_apart_from_a_deleted_one
pass: a_file_the_session_wrote_is_not_named_as_drift
pass: a_reported_change_is_not_reported_twice
pass: nothing_changing_answers_no_report_at_all
pass: a_reloaded_session_is_restamped_from_its_touched_files
pass: mapping_and_connect_preserve_unreported_resident_drift
pass: post_rename_recovery_preserves_unreported_resident_drift
pass: repair_of_empty_legacy_session_keeps_normal_drift_behavior
pass: stamp_capacity_preserves_existing_observations
pass: stamps_are_not_written_into_the_session_snapshot
```

```sh
for doc in cartridge.json README.md .cartridge/help.md; do
    if grep -qn 'drift' "$doc"; then :; else
        echo "$doc does not describe the new operation"
        exit 1
    fi
done
```

Before collection, run the owner's full offline locked tests, fmt and strict
all-target clippy with an isolated CARGO_TARGET_DIR and unset CARTRIDGE_YOLO.
Run `./task audit` and `./task isolation` at workspace root and inspect the
relevant result. A pre-existing failure is reported, never quietly counted as
passing. Do not force integration over foreign manifest/document changes.


The following additional named Rust block executes the four migrated existing
tests. It is separate from the drift filter to keep the engine's per-block
budget clear; do not treat a full baseline from the old source as proof.

```test
run: env -u CARTRIDGE_YOLO CARGO_TARGET_DIR=target/file-drift-verify sh -eu -c 'for name in every_pre_rename_failure_preserves_all_mutations_and_notifications unattached_buffers_remain_memory_only_and_survive_other_session_commits a_session_round_trips_through_its_file publication_identity_deduplicates_only_same_publication_and_keeps_legacy_projection; do cargo test --offline --locked --lib "$name"; done'
pass: every_pre_rename_failure_preserves_all_mutations_and_notifications
pass: unattached_buffers_remain_memory_only_and_survive_other_session_commits
pass: a_session_round_trips_through_its_file
pass: publication_identity_deduplicates_only_same_publication_and_keeps_legacy_projection
```

The compatible host is a prepared external executable, not a thing this
Sessions source build may substitute. Check identity and build the candidate:

```sh
test -x target/file-drift-host/cartridge
host_digest=$(shasum -a 256 target/file-drift-host/cartridge | cut -d ' ' -f 1)
test "$host_digest" = b081f7d1b9aab6c1130bb61ee4ec356931b65483dcac7e88c998ca283ff6dc75
env -u CARTRIDGE_YOLO CARGO_TARGET_DIR=target/file-drift-verify cargo build --offline --locked --lib
test -f target/file-drift-verify/debug/libsessions.dylib
```

Run the actual candidate-native fixtures, with every named test required:

```test
run: env -u CARTRIDGE_YOLO sh -eu -c 'drift_runtime=$(mktemp -d /tmp/sd.XXXXXX); trap '"'"'rm -rf "$drift_runtime"'"'"' EXIT HUP INT TERM; CARTRIDGE_BIN="$PWD/target/file-drift-host/cartridge" SESSIONS_MODULE="$PWD/target/file-drift-verify/debug/libsessions.dylib" XDG_RUNTIME_DIR="$drift_runtime" bun test .cartridge/tests/integration/change-records.test.ts'
pass: native distinct direct and overlay publications persist with exact read-only pages and legacy metadata
pass: native strict DTOs, duplicate conflicts, and atomic invalid batches preserve snapshot
pass: native legacy snapshots remain readable and corrupt retained evidence is diagnosed without repair
pass: native count capacity and byte-bounded pages keep all retained publication identities
pass: native touch requires normalized absolute paths and reports later drift
```

These gates precede collection and run against the lane and integrated target.
They do not silently opt out when a host/module/Bun dependency is missing.
The root JEV fixture migration is a separate explicit pre-integration owner
gate; record it together with full owner tests/checks and audit/isolation.
