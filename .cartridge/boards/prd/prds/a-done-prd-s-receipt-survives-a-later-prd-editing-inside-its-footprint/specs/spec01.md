---
complexity: 2
footprint:
  - src/lifecycle.ts
  - .cartridge/tests/receipt-drift.test.ts
---

# spec01 — a changed path in a done footprint is drift unless a later collected, still-verified PRD that owns it landed exactly that content

## Acceptance

- [ ] A done PRD whose footprint was changed after its receipt only by later collections of other done PRDs has no completion problem. Each of those PRDs must own the changed paths through its footprint and still pass its own `completionProblem`, and the paths must be byte-identical at HEAD to that PRD's receipt. This holds when the later PRD's lane landed several commits and its receipt names only the last one.
- [ ] A commit inside a done PRD's footprint that no later collection landed still reports `verified source footprint changed after collection`. This covers an edit on top of a collected sibling's path and a deletion of a path that an earlier collection never had.
- [ ] A later PRD whose own receipt no longer verifies, for example because its spec changed after collection, vouches for nothing. The earlier PRD then reports `verified source footprint changed after collection` again.
- [ ] A parent whose two children were collected in sequence over overlapping footprints collects with exit 0.
- [ ] `bun test ./.cartridge/tests/receipt-drift.test.ts`, `./.cartridge/tests/engine.test.ts` and `./.cartridge/tests/records.test.ts` pass.

## Design

In `completionProblem` (`src/lifecycle.ts`), the drift check keeps the untracked-file refusal as it is. It then lists the changed paths with `git diff --name-only <commit> -- <footprint>`, which compares against the working tree, so uncommitted edits still count. When that list is not empty, it builds one candidate list for each call:

1. `git rev-list <commit>..HEAD` is one spawn. Its hashes form a set.
2. Candidates are the done records in the scanned graph whose `commit:` is in that set, which means they were collected after this receipt. Each candidate's owned paths are `feet(other)` relative to the code repo. The filter is a set lookup before any `feet()` call, so a drift check over 600+ records spawns no extra git process per record.
3. A changed file counts as reviewed when some candidate owns it (equal to, or under, one of its feet) and `git diff --quiet <candidate commit> -- <file>` exits 0, meaning the tree matches what that collection verified. The candidate must also pass its own `completionProblem(other, graph, seen)`, memoised once per candidate. The `seen` set is the existing cycle guard.
4. If any changed file is not reviewed, the refusal is the unchanged string.

Byte equality at the receipt replaces reconstructing the lane's range. `collection.md` records only the final `commit:`, and no durable record keeps the lane base (`initialHead`), so the range base..commit cannot be recovered from the records. It does not need to be. Every lane commit that `collect` fast-forwards is an ancestor of the receipt, and whatever those commits wrote is the content at the receipt. The fixture's second child lands two lane commits (compare the live `b08cd13` and `12a1646`, both from one PRD) and is covered.

Superproject pointer bumps take the same path. A gitlink shows in `git diff --name-only` as the submodule path, and a candidate whose footprint owns that path vouches for it only if the pointer at HEAD equals the pointer in its receipt. Planning-record commits never reach this check unless a footprint covers the board directory; that pre-existing behaviour is unchanged.

## Steps

1. Replace the single drift line in `completionProblem` with the check above. The reference hunk is about 20 lines, adds no import and changes no other function. `collect`'s integration check (`source footprint changed during integrated verification`) stays as it is.
2. Add `.cartridge/tests/receipt-drift.test.ts` with its own fixture (`mkdtemp`, a code repo and a records repo). Children `parent/search` (footprint `web`) and `parent/cites` (footprint `web/memos`, needs search, two lane commits) are collected through `execute('claim'|'collect')`. The file contains the three tests named in Verify.
3. `src/lifecycle.ts` also has uncommitted edits from another session (the `test` Verify block). Apply this hunk on top of them rather than over them. The hunk touches only the drift block in `completionProblem`, which those edits do not change.

## Verify and Proof

The new fixture cases, reported passed by name.

```sh
log="$(mktemp)"
trap 'rm -f "$log"' EXIT
bun test ./.cartridge/tests/receipt-drift.test.ts > "$log" 2>&1 || { cat "$log"; exit 1; }
cat "$log"
for named in \
  'a later collected sibling inside the footprint leaves the receipt verified and the parent collects' \
  'an uncollected commit inside a done footprint still drifts, even over a collected sibling' \
  'only a later, still-verified receipt vouches for a changed path'
do
  grep -Fq "(pass) $named" "$log" || { echo "not reported passed: $named"; exit 1; }
done
grep -Eq '^ 0 fail$' "$log"
```

The engine suite and the live-records check still pass.

```sh
log="$(mktemp)"
trap 'rm -f "$log"' EXIT
bun test ./.cartridge/tests/engine.test.ts ./.cartridge/tests/records.test.ts > "$log" 2>&1 || { cat "$log"; exit 1; }
cat "$log"
grep -Fq '(pass) real collect verifies an isolated lane and commits integration evidence' "$log"
grep -Fq '(pass) forged done state and old commit cannot substitute for collection evidence' "$log"
grep -Eq '^ 0 fail$' "$log"
```

## Evidence from analysis (2026-09-19)

The reference was built in a scratch clone at `ee4d910f`.

- Base with only the new test file: `receipt-drift` 1 pass, 1 fail. The first test fails at `expect(problem('parent/search')).toBeNull()` with `Received: "verified source footprint changed after collection"`.
- Reference: `receipt-drift` 3 pass, 0 fail. `engine` 23 pass, 0 fail. `records` 3 pass, 0 fail. `tsc --noEmit` exits 0. The full suite has 85 pass and 4 fail; all 4 are `statusline.test.ts`, which also fails 0/4 on base in the scratch clone and passes 4/4 in the live checkout, so the failures come from the clone's location.
- Denied worlds, each run separately: letting any done record vouch instead of only records in `<commit>..HEAD`, and replacing the candidate's `completionProblem` with `true`. Both fail the third test (2 pass, 1 fail). With the first, Verify block 1 exits 1.
- Verify blocks, run as `env -i PATH="$PATH" HOME="$HOME" sh -eu -c`. Reference: block 1 exits 0 in 8 s and block 2 exits 0 in 15 s. Base with only the new test file: block 1 exits 1 and block 2 exits 0.
- Read-only run over the live `root` board (645 records, 374 done) with the reference source: `completionProblem` time is unchanged, 20.4 s against 19.6 s on base. Problems fall from 341 to 334. The records that clear include this PRD's evidence case, `…/search-returns-ranked-results-each-with-its-source-url`, and its sibling `…/web-ctg-exists-as-a-cartridge-and-fetches-a-page-as-readable-text`, plus `@gitfs/gitfs-is-back-in-the-composition`, whose `.cartridge/init.lua` was later landed by web-ctg-exists. The first draft looped over every done record with a `merge-base` spawn and took 92 s, which is why the design uses the rev-list set.

## Remaining limits

- A receipt written as an abbreviated hash matches nothing in the `rev-list` set, so it vouches for nothing and the check stays conservative. `collect` always writes the full hash.
- Only records in the scanned graph (the board and its members) can vouch. A collection recorded on an unrelated board that targets the same repository still reads as drift.
