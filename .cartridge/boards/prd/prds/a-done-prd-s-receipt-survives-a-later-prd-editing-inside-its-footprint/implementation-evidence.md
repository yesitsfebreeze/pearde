# Lifecycle prerequisite implementation evidence

Status: implemented in isolated claimed lane; independent source verification and
proposed verification amendment remain pending. This is not a collection receipt.

The existing named-test and pinned-submodule lane baseline is commit ad71d3eb,
limited to src/lifecycle.ts and .cartridge/tests/engine.test.ts, independently
approved by /root. Both prerequisite named tests and TypeScript passed before
that commit. The first full baseline engine run had 24 passes and one two-second
worker-deadline timeout under load; the unchanged test subsequently passed in
333 milliseconds. The implementation engine suite later passed all 25 tests.

New executable regression suite: eight named tests passed, initially with
79 assertions in 18.84 seconds; stronger lane and rollback coverage passed
84 assertions in 30.36 seconds. A later parent target refusal check was added
within the same named rollup test. Final verifier must rerun the current bytes.
The suite covers committed artifact refresh and immutable receipt history,
contract/provenance/ownership refusals, dependencies and failure, actual lane
integration while dirty README/help tails remain byte-for-byte present, strict
legacy semantics, parent rollups, HEAD races, cancellation, history tampering,
record commit failure rollback and refusal to certify a workspace-only fix.

Negative baseline reproduction: clean ad71d3eb at /tmp/prd-lifecycle-before,
with only the new regression file copied in and frozen dependencies installed,
reported zero passes and eight failures in 6.24 seconds. Baseline lacks explicit
flags; the refresh test also first demonstrates normal collection's stale-source
refusal. This negative run is not claimed to reproduce each new guard failure.

Clean implementation checkout engine suite: 25 passes. Records fixture and
migration checks: two passes. TypeScript: passes. Diff whitespace check: passes.
The full clean-HEAD records suite fails its live-board graph check because the
committed runtime parent references an unrelated untracked declared-settings
child. No unrelated board work was copied or committed. The same unchanged
full records suite on the canonical live board passes three tests and 6630
assertions in 18.25 seconds. Code identity and live dataset manifest are in
proposals/verification-amendment.md and its adjacent dataset JSON. The proposed
amendment is unpublished pending independent authorization/review; no claim is
made that committed board data passes the live graph audit.

No cartridge build or loaded artifact was replaced. Only the eight declared
source/documentation paths differ in the implementation lane. Preserved source
README/help edits may require explicit coordinator reconciliation before lane
integration; the engine intentionally retains Git's overlap refusal.

## Independent verification completed

Reviewer/verifier: /root. Round 6 passes at 92/100. Current named suite:
eight passes, 87 assertions, 34.60 seconds. Full unchanged canonical live records:
three passes, 6630 assertions, 28.48 seconds. TypeScript passes. Source hash
identity for records.ts, planner.ts and records.test.ts was independently checked.
Pinned dataset observation is evidence/independent-board-manifest.json, SHA-256
`d235e46fe6b03782287f11d0898d4523c49557718122fc0cdd5e600368a0da40`;
its UTC timestamp identifies the observed dataset. Logs are retained alongside.
The committed global board-data limitation remains explicit. Acceptance boxes
are closed after this independent evidence; executable contract bytes are unchanged.

The coordinator authorized checked collection followed, if Git refuses the known
doc overlap, by scoped integration recovery. This preserves original dirty bytes
and all unrelated paths, integrates only the independently verified candidate,
and retries full checked snapshot verification before publishing any receipt.

## Post-integration owner gates

/root independently ran `./task audit prd`: hard checks pass. Existing dirty,
untracked and stray prd launcher findings remain soft findings; no unrelated
cleanup occurred. `/root` also ran `./task isolation`: all 21 cartridges pass.
The full collection retry is still responsible for its executable committed
snapshot proof; owner gate results do not substitute for that receipt.

## Checked collection completed

The full checked retry passed every published executable block in both lane and
clean committed snapshot and transitioned claimed to done. Integration source:
`7a44c88fba2322e6c4fa990da24407b3f02b6123`. The receipt reports verified and
integrated true for `verification_target: committed`, with `workspace_verified:
false` and exactly README.md and .cartridge/help.md as preserved dirty paths.
The lane was removed. evidence/checked-collection.json retains the full API
result. The scoped reconciliation proof confirms all 214 unrelated dirty paths
and statuses remained unchanged, with external backup paths and file hashes.
