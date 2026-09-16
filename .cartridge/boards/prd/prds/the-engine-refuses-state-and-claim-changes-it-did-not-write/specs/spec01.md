---
complexity: 3
footprint:
  - src/records.ts
  - src/lifecycle.ts
  - src/engine.ts
  - src/cli.ts
  - .cartridge/tests/engine.test.ts
---

# spec01 — record engine-written state, claim and commit, refuse ops on a PRD whose values changed elsewhere, and audit every adoption

## Acceptance

- [x] After `claim`, a hand edit of `state`, `claim` or `commit` makes `check` exit 2 with a problem that names the PRD, each changed field and its recorded and found values. The problem gives the exact command form `prd adopt <ref> --by <id> --reason "<text>" --board <board>` and says the adoption is recorded.
- [x] `claim`, `release`, `collect`, `specced` and `refine` on that PRD exit 2 with the same reason.
- [x] `adopt` without `--by` or `--reason` exits 2. With both flags it prints the old and new values and appends one JSON line `{at, ref, local, old, new, by, reason}` to `<board>/.state/fields/adopted.log`. After that, `check` is clean and `claim` succeeds.
- [x] `check` exits 0 but lists, under `warnings`, an adoption whose claim moved to a different non-null holder, for as long as that adopted claim is still the live claim. The warning clears once the claim is released.
- [x] `add` records values for the new PRD. `check` drops recorded values whose `prd.md` is gone. So add, claim, delete the dir, then re-add the same slug gives a clean `check`, and `claim` succeeds.
- [x] Dropping a record whose recorded `state` is not `open`, or whose recorded `claim` or `commit` is non-null, appends one JSON line `{at, local, dropped}` to `adopted.log` and puts one warning on that `check` naming the local and the dropped values. Dropping an idle record (`open`, no claim, no commit) is silent. So `add one` → `claim one alice` → `mv prds/one prds/two` → hand-edit `two` back to `open` with no claim → `check` exits 0 with that warning and a logged line, not `{"problems":[],"warnings":[]}`.
- [x] `check` exits 2 with a problem naming the board and the field store, not a raw `EACCES`, when `<board>/.state/fields` is not writable.
- [x] Body edits, `edit()` of non-controlled keys and engine transitions raise no problem and no warning.
- [x] `prd help` lists `adopt <id> --by <identity> --reason <text>`.
- [x] `bun test ./.cartridge/tests/engine.test.ts` passes with these tests: "hand edits to state or claim are reported and refused until adopted", "a hand-written commit is reported", "an adopted claim that changed hands warns until it is released", "a PRD re-added at a removed path inherits no recorded values", "dropping the values of a removed or rehomed record is logged and warned once", "check reports an unwritable field store instead of a raw errno", and "body edits, untracked records and engine transitions raise no field problem".

`adopt` warns rather than refusing when the found claim names a holder other than the recorded one (review round 1's B2 recommendation): `--by` is self-asserted free text, so a refusal keyed on it is bypassed by typing the recorded claimant's name, and the real control is the audit line plus the live-claim warning in box 4, which no `--by` value can suppress.

## Option chosen

Review round 2's B3 (a rename launders `state` and `claim`, and `check` deletes the evidence) is closed by the reviewer's option (a), the visible drop, not (b), the narrowed Outcome.

The store is keyed by path, so a moved record has no recorded values and is trusted on first observation. That half cannot be fixed cheaply — a content-keyed store needs a record identity the PRD format does not have — and it is named in Out of scope below. But the other half, `dropOrphanFields` deleting the last evidence of alice's claim, is three lines: read the value file before unlinking it, log it if it was not idle, and return the warning. (a) costs those lines, keeps the Outcome sentence honest (a rehome no longer passes without a trace: the recorded `analyzing` and alice's claim survive in `adopted.log` and the operator sees the drop on the `check` that performs it), and reuses the audit log and the warnings channel that `adopt` already added. (b) would buy a smaller diff by giving up the invariant the PRD exists to establish.

The warning fires once, on the `check` that performs the drop, and the permanent record is the `adopted.log` line. It is deliberately not a standing warning: the dropped record is gone, so no `prd` op can resolve a warning about it, and a standing warning on every retired PRD would never clear. The drop only happens once per removed record, so the one-shot warning cannot be missed by a later `check` — that `check` is the one that does the dropping.

## Steps

`attempt-3.patch` in `.state/loop/the-engine-refuses-state-and-claim-changes-it-did-not-write/` implements every step, on base 0f32da2e (prd.ctg HEAD at the time of review round 3). It supersedes `attempt-2.patch` and changes only `dropOrphanFields`, `check` and the tests.
- With the patch: engine, service, parity and event-stream tests give 54 pass, 0 fail.
- With the src hunks reverted: 6 of the 7 new tests fail.
- The re-add test only guards against false positives here. It fails against attempt-1, as review round 1 probe P1 showed.

1. `src/records.ts`, next to `edit()`:
   - `CONTROLLED = ['state', 'claim', 'commit']`.
   - The value file for a PRD is `<owner board>/.state/fields/<local>.json`. The owner board is the nearest ancestor with `settings.md`. The file holds `{state, claim, commit}` (null when absent). It is gitignored by `/boards/**/.state/`.
   - `recordFields(file)` writes the value file with `atomic()`, a single temp-file rename, so the CLI processes the daemon spawns never read a torn value file.
   - `edit()` calls `recordFields` when `changes` touches a controlled key. That covers claim, release, specced, refine, defer, retry, unblock and collect.
2. `fieldsProblem(file, retried = false)`:
   - If there is no value file (fresh clone), bootstrap it by writing a temp file and linking it into place, ignoring EEXIST, so a bootstrap never clobbers a concurrent engine write.
   - Compare each field. On a mismatch with `retried` false, wait 50 ms and re-read once to get past the record-rename/value-rename window. A caller that owns the pause itself passes `retried` true (see step 7).
   - Return `<field> changed outside the engine (recorded X, found Y)` joined by `; `, or null.
   - `fieldsRefusal(prd, problem)` appends `; restore the recorded values or run \`prd adopt <ref> --by <id> --reason "<text>" --board <board>\` (the adoption is recorded in <board>/.state/fields/adopted.log)`.
3. `adoptFields(prd, by, reason)`:
   - Append the JSON audit line with `fs.appendFileSync` (O_APPEND, one line). The adopt op runs under the mutation lock.
   - Then `atomic()` the current values, and return `{old, new}`.
4. `dropOrphanFields(board)` walks `.state/fields/`, and for each `*.json` whose `prds/<local>/prd.md` does not exist: read the recorded values, delete the file, and — unless the record was idle (`state` `open`, `claim` and `commit` null) — append `{at, local, dropped}` to `adopted.log` and collect one warning naming the local, the dropped values, the log path and the rehome case. It returns the collected warnings. The drop is the last moment the engine can see what it is losing, so it is the only place the loss can be recorded.
5. `adoptionWarnings(board, graph)` reads `adopted.log`. It warns for `adopt` entries whose new claim holder is non-null, differs from the old holder, and still equals the PRD's live claim. The holder is the first word of the claim. Drop entries carry no `new`, so they are skipped here; their warning is emitted once by step 4.
6. `src/lifecycle.ts` `transition()`:
   - `add` calls `recordFields(file)` after its `atomic()` write (not with `--dry`).
   - After `resolve()`, `adopt` validates `--by` (the claim identity pattern) and `--reason` (non-empty, at most 1024 chars). With `--dry` it writes nothing. Otherwise it prints `Adopted <ref>: <old> -> <new>`.
   - Every other op except `brief` throws `fieldsRefusal(prd, problem)`. A single-record op keeps the self-retry of step 2.
7. `src/engine.ts`:
   - Add `adopt` to `mutations`.
   - `check` runs `dropOrphanFields` for the root and member boards and keeps its warnings, then makes one pass of `fieldsProblem(file, true)` over the graph with no sleep, sleeps 50 ms once if that pass found anything, re-checks only those records, and pushes `fieldsRefusal` problems for the ones that still mismatch. One pause per `check`, not one per record: measured on a temp board with 20 tampered records, `check` takes 342 ms instead of 1318 ms, and the cost no longer grows with the number of tampered records inside an unlocked op.
   - Then `adoptionWarnings` for the same boards, and `data.warnings`. Warnings do not change the exit code.
   - The whole field section is wrapped so an unusable store (read-only `.state/fields`, a corrupt value file) becomes one problem naming the board and what `check` needs, instead of a raw errno escaping the op. `check` is no longer read-only: it writes bootstrap value files, deletes orphans and appends drop lines under `<board>/.state/fields/`.
8. `src/cli.ts`: add the `adopt` line to the help text.
9. `.cartridge/tests/engine.test.ts`: the seven named tests, on the temp-board fixture. Hand edits use `fs.writeFileSync`, never `edit()`.

## Recovery

- **Git checkout or reset of a record.** `git checkout`, `reset`, `stash` or `pull` of a prd.md with different `state`, `claim` or `commit` is reported like a hand edit, and that is intended. Restore the recorded values, or run `prd adopt <ref> --by <coordinator> --reason "restored <file> from git <rev>"`.
- **Crash during `edit()`.** A crash between the record rename and the value-file rename leaves a report whose found values are the ones the engine meant to write. Recover the same way, with an adoption reason that names the interrupted op.
- **A rehomed or retired record.** The `check` that notices the removal warns and logs `{at, local, dropped}`. Compare the dropped values with the record at its new path: if they survived the move, nothing to do; if they did not, restore them or `prd adopt <new-ref> --by <coordinator> --reason "rehomed from <local>"`, which links the two in the same log.
- **An unwritable board.** `check` exits 2 with `the engine field store is unavailable (<code>)`. Restore write access to `<board>/.state/fields` — `check` maintains the store, so a read-only board cannot be checked.

## Rollout

- **Old-code window.** The daemon's prd service spawns a fresh `src/cli.ts` for each op, so it runs new code as soon as the merge lands. The risk is a process that started on old code and writes after new code is live: a `prd run` coordinator, or a `collect` (this PRD's own collect loads old code, fast-forwards, then `edit()`s `done` with no value file). A new-code `check` or op in that window bootstraps pre-write values and reports the old process's write.
- **Deploy.**
  1. Stop `prd run` loops and let in-flight collects finish.
  2. Collect this PRD with no other `prd` op running.
  3. Run `prd check --board root`. For each field problem that the engine itself wrote during the window, run `prd adopt <ref> --by <coordinator> --reason "pre-guard engine write during rollout"`, which is logged.
- **After deploy.** The first `check` writes one value file per record. Measured on a copy of the live boards (574 records, this machine): `check --board root --json` exits 0 with 0 problems and 0 warnings unpatched (2.09 s, 2.24 s) and patched (2.46 s, 2.23 s, 2.15 s), leaving 574 value files and no `adopted.log`. The difference is inside run-to-run noise; there is no measurable slowdown. Review round 2 measured the same shape on a 569-record board (1.53–1.75 s patched vs 2.00–2.77 s unpatched).

Out of scope, and named here because the Outcome does not cover them:

- A foreign release routed through the engine (see the PRD's Planning note).
- **A record moved to another path is re-trusted at the new path.** The store is keyed by path, so after `mv prds/one prds/two` the record at `two` has no recorded values and its current `state`, `claim` and `commit` are trusted on first observation; `claim two <other>` then succeeds. What the guard does deliver for a rehome is that the values it is losing are logged to `adopted.log` and warned about, so the move leaves a trace an operator can reconcile (see Recovery). Closing the other half needs a record identity independent of the path, which the PRD format does not have.
- `adopt` stays out of the daemon's service OPS, so a model cannot call it through `tool.prd`. That is the intended boundary, not an omission: accepting a value the engine did not write is a coordinator decision made at a CLI by a named identity, and an agent that hits a refusal is meant to stop and report it, not to clear it.

## Verify and Proof

```sh
bun test ./.cartridge/tests/engine.test.ts
for name in "refused until adopted" "a hand-written commit is reported" "changed hands warns" "re-added at a removed path" "rehomed record is logged and warned once" "unwritable field store instead of a raw errno" "raise no field problem"; do grep -q "$name" .cartridge/tests/engine.test.ts; done
bun src/cli.ts help | grep -q "adopt <id> --by"
```
