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

- [ ] After `claim`, a hand edit of `state`, `claim` or `commit` makes `check` exit 2 with a problem that names the PRD, each changed field and its recorded and found values. The problem gives the exact command form `prd adopt <ref> --by <id> --reason "<text>" --board <board>` and says the adoption is recorded.
- [ ] `claim`, `release`, `collect`, `specced` and `refine` on that PRD exit 2 with the same reason.
- [ ] `adopt` without `--by` or `--reason` exits 2. With both flags it prints the old and new values and appends one JSON line `{at, ref, local, old, new, by, reason}` to `<board>/.state/fields/adopted.log`. After that, `check` is clean and `claim` succeeds.
- [ ] `check` exits 0 but lists, under `warnings`, an adoption whose claim moved to a different non-null holder, for as long as that adopted claim is still the live claim. The warning clears once the claim is released.
- [ ] `add` records values for the new PRD. `check` drops recorded values whose `prd.md` is gone. So add, claim, delete the dir, then re-add the same slug gives a clean `check`, and `claim` succeeds.
- [ ] Body edits, `edit()` of non-controlled keys and engine transitions raise no problem and no warning.
- [ ] `prd help` lists `adopt <id> --by <identity> --reason <text>`.
- [ ] `bun test ./.cartridge/tests/engine.test.ts` passes with these tests: "hand edits to state or claim are reported and refused until adopted", "a hand-written commit is reported", "an adopted claim that changed hands warns until it is released", "a PRD re-added at a removed path inherits no recorded values", and "body edits, untracked records and engine transitions raise no field problem".

## Steps

`attempt-2.patch` in `.state/loop/the-engine-refuses-state-and-claim-changes-it-did-not-write/` implements every step, on base 9bcdcab0.
- With the patch: engine, service, parity and event-stream tests give 52 pass, 0 fail.
- With the src hunks reverted: 4 of the 5 new tests fail.
- The re-add test only guards against false positives here. It fails against attempt-1, as review round 1 probe P1 showed.

1. `src/records.ts`, next to `edit()`:
   - `CONTROLLED = ['state', 'claim', 'commit']`.
   - The value file for a PRD is `<owner board>/.state/fields/<local>.json`. The owner board is the nearest ancestor with `settings.md`. The file holds `{state, claim, commit}` (null when absent). It is gitignored by `/boards/**/.state/`.
   - `recordFields(file)` writes the value file with `atomic()`, a single temp-file rename, so the CLI processes the daemon spawns never read a torn value file.
   - `edit()` calls `recordFields` when `changes` touches a controlled key. That covers claim, release, specced, refine, defer, retry, unblock and collect.
2. `fieldsProblem(file)`:
   - If there is no value file (fresh clone), bootstrap it by writing a temp file and linking it into place, ignoring EEXIST, so a bootstrap never clobbers a concurrent engine write.
   - Compare each field. On a mismatch, wait 50 ms and re-read once to get past the record-rename/value-rename window.
   - Return `<field> changed outside the engine (recorded X, found Y)` joined by `; `, or null.
   - `fieldsRefusal(prd, problem)` appends `; restore the recorded values or run \`prd adopt <ref> --by <id> --reason "<text>" --board <board>\` (the adoption is recorded in <board>/.state/fields/adopted.log)`.
3. `adoptFields(prd, by, reason)`:
   - Append the JSON audit line with `fs.appendFileSync` (O_APPEND, one line). The adopt op runs under the mutation lock.
   - Then `atomic()` the current values, and return `{old, new}`.
4. `dropOrphanFields(board)` deletes `*.json` under `.state/fields/` whose `prds/<local>/prd.md` does not exist.
5. `adoptionWarnings(board, graph)` reads `adopted.log`. It warns for entries whose new claim holder is non-null, differs from the old holder, and still equals the PRD's live claim. The holder is the first word of the claim.
6. `src/lifecycle.ts` `transition()`:
   - `add` calls `recordFields(file)` after its `atomic()` write (not with `--dry`).
   - After `resolve()`, `adopt` validates `--by` (the claim identity pattern) and `--reason` (non-empty, at most 1024 chars). With `--dry` it writes nothing. Otherwise it prints `Adopted <ref>: <old> -> <new>`.
   - Every other op except `brief` throws `fieldsRefusal(prd, problem)`.
7. `src/engine.ts`:
   - Add `adopt` to `mutations`.
   - `check` runs `dropOrphanFields` for the root and member boards, pushes `fieldsRefusal` problems, and returns `data.warnings`. Warnings do not change the exit code.
8. `src/cli.ts`: add the `adopt` line to the help text.
9. `.cartridge/tests/engine.test.ts`: the five named tests, on the temp-board fixture. Hand edits use `fs.writeFileSync`, never `edit()`.

## Recovery

- **Git checkout or reset of a record.** `git checkout`, `reset`, `stash` or `pull` of a prd.md with different `state`, `claim` or `commit` is reported like a hand edit, and that is intended. Restore the recorded values, or run `prd adopt <ref> --by <coordinator> --reason "restored <file> from git <rev>"`.
- **Crash during `edit()`.** A crash between the record rename and the value-file rename leaves a report whose found values are the ones the engine meant to write. Recover the same way, with an adoption reason that names the interrupted op.

## Rollout

- **Old-code window.** The daemon's prd service spawns a fresh `src/cli.ts` for each op, so it runs new code as soon as the merge lands. The risk is a process that started on old code and writes after new code is live: a `prd run` coordinator, or a `collect` (this PRD's own collect loads old code, fast-forwards, then `edit()`s `done` with no value file). A new-code `check` or op in that window bootstraps pre-write values and reports the old process's write.
- **Deploy.**
  1. Stop `prd run` loops and let in-flight collects finish.
  2. Collect this PRD with no other `prd` op running.
  3. Run `prd check --board root`. For each field problem that the engine itself wrote during the window, run `prd adopt <ref> --by <coordinator> --reason "pre-guard engine write during rollout"`, which is logged.
- **After deploy.** The first `check` writes one value file per record (574 on the live boards in review round 1, check 1.9 s → 2.3 s).

Out of scope: a foreign release routed through the engine (see Planning note). `adopt` stays out of the daemon's service OPS, so a model cannot call it via `tool.prd`. The PRD frontmatter footprint still lists `.cartridge/tests/records.test.ts`, which no step edits. Only the coordinator can drop it, because the frontmatter is engine-owned.

## Verify and Proof

```sh
bun test ./.cartridge/tests/engine.test.ts
for name in "refused until adopted" "a hand-written commit is reported" "changed hands warns" "re-added at a removed path" "raise no field problem"; do grep -q "$name" .cartridge/tests/engine.test.ts; done
bun src/cli.ts help | grep -q "adopt <id> --by"
```
