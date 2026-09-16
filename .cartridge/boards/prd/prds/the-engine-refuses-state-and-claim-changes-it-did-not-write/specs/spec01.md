---
complexity: 2
footprint:
  - src/records.ts
  - src/lifecycle.ts
  - src/engine.ts
  - .cartridge/tests/engine.test.ts
---

# spec01 — record engine-written state, claim and commit and refuse ops on a PRD whose values changed elsewhere

## Acceptance

- [ ] After `claim`, rewriting `state`/`claim` in prd.md by hand makes `check` exit 2 with a problem `<ref>: state changed outside the engine (recorded …, found …)` naming each changed field.
- [ ] `claim`, `release` and `collect` on that PRD exit 2 with the same `<ref>: state changed outside the engine` reason; `adopt <ref>` records the current values, after which `check` is clean and `claim` succeeds.
- [ ] Body text edits, `edit()` of non-controlled keys (`footprint`), engine transitions, and PRDs with no recorded digest (fresh clone, `add`) raise no problem.
- [ ] `bun test ./.cartridge/tests/engine.test.ts` passes, including the tests "hand edits to state or claim are reported and refused until adopted" and "body edits, untracked records and engine transitions raise no field problem".

## Steps

A working prototype of all steps is `attempt-1.patch` in this draft directory (base 6807f025, 18/18 engine tests pass; the new tamper test fails without the src hunks).

1. `src/records.ts`:
   - Add `CONTROLLED = ['state', 'claim', 'commit']`.
   - Add `fieldsFile(file)`: walk up from the PRD dir's parent to the nearest dir with `settings.md` (the owner board). Return `<board>/.state/fields/<path relative to board/prds>.json`, which is gitignored by `/boards/**/.state/`.
   - Add `recordFields(file)`: `atomic()` write of `{state, claim, commit}` (null when absent) parsed from the file. Temp file plus rename, so the CLI and the daemon's prd service never see a torn digest.
   - At the end of `edit()`, call `recordFields(file)` when `changes` touches a controlled key. This covers claim, release, specced, refine, defer, retry, unblock and collect, which all write through `edit()`.
   - Add `fieldsProblem(file)`: if no digest exists, bootstrap it by writing a temp file and `fs.linkSync` it into place (EEXIST ignored), so a bootstrap never overwrites a digest an engine op just wrote. Then compare each controlled field. On a mismatch, sleep 50 ms and re-read once, because the record and digest are two renames and an unlocked reader can land between them. Return `null` or `"<field> changed outside the engine (recorded X, found Y); …; run prd adopt to accept it"`.
2. `src/lifecycle.ts` `transition()`, right after `resolve()`:
   - `adopt` runs `recordFields(prd.file)` (a no-op with `--dry`) and returns `Adopted <ref> <state>`.
   - Every other op except `brief` throws `<ref>: <fieldsProblem>` when that returns a problem. `add` never reaches this and needs no digest: a missing digest bootstraps.
3. `src/engine.ts`: add `'adopt'` to `mutations`, so it runs under the mutation lock. In `check`, push `ref + ': ' + fieldsProblem(prd.file)` for every scanned PRD with a problem.
4. `.cartridge/tests/engine.test.ts`: the two tests named in Acceptance, both on temp boards (the existing `beforeEach` fixture). They hand-edit with `fs.writeFileSync`/`appendFileSync`, never `edit()`.

Out of scope: `adopt` is CLI and engine only (not added to the service OPS in `src/service.ts` or the `help.md` op list). Restoring the recorded values by hand also clears the problem. The daemon must be restarted (`daemon --replace`) to load the change.

## Verify and Proof

```sh
bun test ./.cartridge/tests/engine.test.ts
grep -q "refused until adopted" .cartridge/tests/engine.test.ts
grep -q "raise no field problem" .cartridge/tests/engine.test.ts
```
