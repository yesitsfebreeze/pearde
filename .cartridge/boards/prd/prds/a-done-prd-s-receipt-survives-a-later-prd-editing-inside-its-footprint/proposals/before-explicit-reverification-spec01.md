---
complexity: 2
footprint:
  - src/lifecycle.ts
  - .cartridge/tests/receipt-drift.test.ts
---

# spec01 — a changed path in a done footprint is drift unless a later leaf collection's own lane landed the commit that changed it

## Acceptance

- [ ] A done PRD whose footprint changed after its receipt only through commits that lie inside a later collection's own lane range (`base..commit` of that collection's receipt) has no completion problem. The later PRD must own each changed path through its footprint and still pass its own `completionProblem`. This holds when that lane landed several commits and its receipt names only the last one.
- [ ] A commit inside a done PRD's footprint that no later lane range contains still reports `verified source footprint changed after collection`. This covers a hand commit made before the later lane was cut, an edit on top of a collected sibling's path, and an uncommitted edit in the working tree.
- [ ] A record that has children, or whose receipt records no `: exit 0` evidence, vouches for nothing. A container that committed a stray working-tree edit inside its own footprint while collecting does not clear an earlier receipt.
- [ ] A later PRD whose own receipt no longer verifies, for example because its spec changed after collection, vouches for nothing, and the earlier PRD reports `verified source footprint changed after collection` again.
- [ ] Every receipt `collect` writes carries `base:`, the full hash of the code HEAD the collection started from. A receipt without a `base:` vouches for nothing, and a record drifted by such a receipt is recovered by collecting it again, which the suite exercises end to end.
- [ ] A parent whose two children were collected in sequence over overlapping footprints collects with exit 0.
- [ ] `bun test ./.cartridge/tests/receipt-drift.test.ts`, `./.cartridge/tests/engine.test.ts` and `./.cartridge/tests/records.test.ts` pass.

## Design

A receipt vouches for the work of its own lane and for nothing else. `collect`
already knows that range: `initialHead` is the code HEAD the collection started
from, the candidate commit is a descendant of it, and `assertFootprint` has
checked every path between the two. Nothing durable records `initialHead`
today, so the receipt gains one line: `collect` writes `base:` with the value of
`initialHead` between `commit:` and `spec-digests:`. Nothing else in the tree
reads `collection.md`, and the field is additive, so older receipts still parse.

In `completionProblem` the drift check then attributes commits instead of
comparing bytes. The untracked-file refusal stays first and unchanged. The
changed set is still `git diff --name-only <commit> -- <footprint>`, which
compares the receipt against the working tree, so a record that is clean today
stays clean. When that set is not empty:

1. `git diff --name-only HEAD -- <footprint>` must be empty. An uncommitted edit
   sits in no lane and can never be vouched for, so it is drift at once.
2. `git log --full-history --no-renames --diff-merges=dense-combined --format=%x00%H --name-only <commit>..HEAD -- <changed>`
   is one spawn. It yields each commit since the receipt together with the files
   it touched. `--diff-merges=dense-combined` is load-bearing: without it `git
   log` prints a bare hash and no file names for a merge commit, so a merge
   would pass this check with nothing to vouch for.
3. For every pair of a commit and a changed file it touched, some record in the
   scanned graph must vouch. A record vouches when it is a different, done leaf
   that is not an ancestor in the current proof chain; its `collection.md` has a
   40-hex `base:` and a `commit:` equal to its own receipt; its body contains
   `: exit 0`; its code repository is this one; its `feet()` cover the file; the
   commit is in `git rev-list <base>..<commit>` for that receipt; and its own
   `completionProblem` is null.
4. Any pair nobody vouches for is the unchanged refusal string.

This closes both round-1 findings at their root. A hand commit made before a
later lane was cut is outside that lane's range, so the later collection cannot
excuse it (F1). A container has children and its receipt records
`container: every child done` rather than `: exit 0`, so it vouches for nothing
even when its own collection swept a stray working-tree edit into a commit (F2).
Binding a voucher to its range also removes the recursion the review sketched:
because the range test is applied to every commit between the earlier receipt
and HEAD, a commit that landed before the later lane is refused directly, with
no need to review the content at that lane's base against the earlier receipt.

Legacy receipts, written before this change and carrying no `base:`, vouch for
nothing. That is the conservative reading, and this spec adopts it, for three
reasons. It keeps the PRD's requested Acceptance exactly as written, where the
weaker reading — trusting a legacy receipt on byte equality — would be false for
a hand commit that landed before that legacy collection and still stands at its
receipt. It is monotone: no record that verifies today stops verifying, and
every receipt written from now on is bound to its lane. And it leaves a remedy
that costs no new surface: a record drifted by a legacy receipt is recovered by
collecting it again, which re-runs its own published proof against the current
tree and writes a receipt anchored at today's HEAD. That is what the refusal has
always meant, so re-verification, not a weaker rule, is the honest answer to it.

The price is that this clears nothing at all on the day it lands, and the spec
claims no more than that. Over the live root board the base and the reference
produce byte-identical verdict maps, and not one record changes verdict, this
PRD's own evidence case included. The census is a moving target because the
board is worked daily: the review counted 689 records, 381 done, 353 with a
problem and 75 reporting this refusal, and hours later the same probe counted
710 records, 388 done, 357 with a problem and 77 reporting it. The rule cannot
refuse where base passes, because `changed` is the set of paths that already
differ from the receipt and base refuses whenever that set is not empty, so the
only movement is the board's own. Two weaker readings were measured against
that. The
round-1 byte-equality rule cleared 7 records, the evidence case among them, and
is the rule this spec rejects because it launders a hand commit. A middle
reading, in which a receipt with no `base:` vouches only for its own recorded
`commit:`, clears 4 of them and still not the evidence case, because that
sibling's lane landed two commits in `web.ctg` and only the tip is recorded.
Every one of them is cleared instead by collecting the record again: `prd
defer`, `prd release <ref> open`, `prd specced`, deleting the stale
`lane/<board>-<slug>` branch that the previous collection left behind, `prd
claim` and `prd collect`. The suite pins that sequence so the remedy cannot rot.

Merges need the flag rather than an exception. `git log --name-only` says
nothing about the files a merge commit touched unless a diff-merges mode is
asked for, so without `--diff-merges=dense-combined` a merge that resolved a
file inside a done footprint to content neither parent had would be listed as a
hash with no files, the inner loop would never run, and the edit would be
excused. Dense-combined lists exactly the paths that differ from every parent,
so an ordinary merge of work each parent already carries lists nothing and costs
nothing, while such a resolution lists the file and has to be vouched for like
any other change. `collect` integrates with `merge --ff-only` and never writes a
merge commit, so no existing receipt depends on this. `--full-history` separately
keeps history simplification from hiding a commit that would otherwise need a
voucher.

A gitlink bump is one more changed path: the superproject records the submodule
path, and the collection whose footprint owns that path vouches for the commit
that moved it. Planning-record commits still only reach this check when a
footprint covers the board directory, which is unchanged.

`laneRange` memoises one `rev-list` per `base..commit` pair in a module-level
map. The history between two recorded commits cannot change, so the cache needs
no invalidation, and a sweep over a whole board pays for each receipt once.

## Steps

1. Anchor on the committed file. `git -C prd.ctg show HEAD:src/lifecycle.ts` is
   the content this spec was written against. `src/lifecycle.ts` and
   `.cartridge/tests/engine.test.ts` carry uncommitted edits from another
   session that add `test` verification blocks and submodule-seeded lanes. The
   implementer must not revert or commit them; rebase these hunks onto whatever
   is committed at claim time. Measured against the live dirty file, the two
   hunks in `completionProblem` apply with an offset of 68 lines, and the
   one-line receipt change rejects only on context: the receipt line itself is
   untouched by those edits, while the line above it became `removeLane(code,
   work.directory)`. Re-anchor that hunk on the committed text and apply it.
2. Write `base:` with the value of `initialHead` into the receipt frontmatter
   `collect` builds, between `commit:` and `spec-digests:`.
3. Replace the single drift line in `completionProblem` with the check above,
   and add the `laneRange` helper next to `childContracts`. The reference adds
   34 lines, adds no import, and changes no other function. Keep
   `--diff-merges=dense-combined` on the `git log`: dropping it reopens the
   merge hole and fails the seventh test on its own.
   `collect`'s own integration check, `source footprint changed during
   integrated verification`, stays as it is.
4. Add `.cartridge/tests/receipt-drift.test.ts` with its own fixture, built like
   the one in `engine.test.ts`: `mkdtemp`, a code repository holding `web/` and
   `lib/`, and a records repository. A parent owns `parent/search` (footprint
   `web`) and `parent/cites` (footprint `web/memos`, needs `parent/search`, two
   lane commits), both collected through `execute('claim'|'collect')`. The file
   holds the seven tests named in Verify block 1, one per case: the sibling that
   leaves the receipt verified, the uncollected commit over a collected path,
   the voucher that stopped verifying, the hand commit that predates the later
   lane (F1), the container that verified nothing of its own (F2), the
   re-collection that re-anchors a drifted receipt, and the merge that resolves
   a footprint path to content neither parent had (F5). The merge case diverges
   both sides outside the done footprint, so the merge commit itself is the only
   change inside it.
5. Both Verify blocks take their name census from the JUnit report, never from
   stdout. A passing bun test is not reliably printed when stdout is a file, so
   a `grep "(pass) <name>"` gate fails on a correct implementation; that is a
   recorded trap in this project and it beat the round-3 draft of this spec. The
   `test` block that would carry this for us, with the engine writing
   `$PRD_TEST_REPORT`, is not available: `verificationBlocks` at HEAD
   (`bdf0370c`) still matches only `sh`, `bash` and `shell`, and the `test`-block
   engine lives in the same session's uncommitted edits. The blocks therefore
   write the report themselves with `--reporter=junit --reporter-outfile`. If
   that engine is committed by claim time, convert each block to a `test` block
   naming the same tests and change nothing else.
6. Keep `--timeout 30000` on both `bun test` invocations. Under `env -i` and a
   loaded machine the fixture's own tests run 5.9 to 9.9 s against 1.4 s
   unconstrained, so bun's 5000 ms default fails three of the seven on a correct
   implementation.

## Verify and Proof

The seven fixture cases, each reported passed by name in the runner's own JUnit
report.

```sh
report="$(mktemp)"
log="$(mktemp)"
trap 'rm -f "$report" "$log"' EXIT
bun test ./.cartridge/tests/receipt-drift.test.ts --timeout 30000 --reporter=junit --reporter-outfile="$report" > "$log" 2>&1 || { cat "$log"; exit 1; }
cat "$log"
grep -Eq '<testsuites[^>]* tests="7"[^>]* failures="0"[^>]* skipped="0"' "$report" || exit 1
if grep -Eq '<(failure|error)\b' "$report"; then exit 1; fi
for named in \
  'a later collected sibling inside the footprint leaves the receipt verified and the parent collects' \
  'an uncollected commit inside a done footprint still drifts, even over a collected sibling' \
  'only a later, still-verified receipt vouches for a changed path' \
  'a hand commit made before a later lane is not vouched for by that lane' \
  'a container that verified nothing of its own never vouches for a changed path' \
  'a drifted receipt is re-anchored by re-collecting the record' \
  'an evil merge that resolves a footprint path to new content still drifts'
do
  grep -Fq "<testcase name=\"$named\"" "$report" || exit 1
done
```

The engine suite and the live-records check still pass.

```sh
report="$(mktemp)"
log="$(mktemp)"
trap 'rm -f "$report" "$log"' EXIT
bun test ./.cartridge/tests/engine.test.ts ./.cartridge/tests/records.test.ts --timeout 30000 --reporter=junit --reporter-outfile="$report" > "$log" 2>&1 || { cat "$log"; exit 1; }
cat "$log"
grep -Eq '<testsuites[^>]* failures="0"[^>]* skipped="0"' "$report" || exit 1
if grep -Eq '<(failure|error)\b' "$report"; then exit 1; fi
grep -Fq '<testcase name="real collect verifies an isolated lane and commits integration evidence"' "$report" || exit 1
grep -Fq '<testcase name="forged done state and old commit cannot substitute for collection evidence"' "$report" || exit 1
```

## Evidence from analysis (2026-09-19, rounds 2 to 4)

The reference was built in `git clone --local` copies of `prd.ctg`, with
`node_modules` copied in, under a private scratch directory. The round-4 builds
are at HEAD `bdf0370c`; `src/lifecycle.ts` and `.cartridge/tests/` are
byte-identical there and at the round-2 HEAD `4e543acc`, the file's SHA-256
being `177200f0…`, so the earlier rounds' evidence still describes this code.
Four builds were compared: `base` (the committed file plus the new test file),
`ref` (this spec), `ref-noflag` (this spec without
`--diff-merges=dense-combined`) and `r1` (the round-1 byte-equality rule
rebuilt).

- Reference: `receipt-drift` 7 pass and 0 fail; `engine` and `records` together
  26 pass and 0 fail; `tsc --noEmit` exits 0. The full suite is 88 pass and 4
  fail, all four in `statusline.test.ts`, which fails 0 of 4 on base in the same
  clone and passes 4 of 4 in the live checkout, so the clone's location causes
  them.
- Base, the committed file plus the test file only: 2 pass and 5 fail. Two tests
  pass on base because base refuses everything. The round-1 evidence claiming 1
  pass and 1 fail was wrong, and the review's correction to 1 pass and 2 fail
  described the earlier three-test file.
- Denied world, the round-1 rule — any done record whose receipt commit lies in
  `<commit>..HEAD` vouches when the file is byte-identical at that receipt: 4
  pass and 3 fail. The two failures that matter are the F1 and F2 tests, each
  with `Expected: "verified source footprint changed after collection"` and
  `Received: null`. Verify block 1 exits 1 against that rule.
- Denied world, this rule without `--diff-merges=dense-combined`: 6 pass and 1
  fail. The single failure is the merge test, with the same `Received: null`,
  which is the flag earning its place.
- Why the blocks were rewritten. The round-3 blocks grepped the runner's
  `(pass)` lines and could not pass a correct implementation. Run as `env -i
  PATH="$PATH" HOME="$HOME" sh -eu -c` against the reference, the old block 1
  exits 1 twice in a row with 4 pass and 3 fail, each failure reading `this test
  timed out after 5000ms`: three fixture cases take 5.9 to 9.9 s under a bare
  environment against 1.4 s unconstrained, over bun's 5000 ms default. The
  review separately saw six of six runs exit 1, one of them reporting 7 pass and
  0 fail with no `(pass)` line at all, which is the recorded trap that a passing
  bun test prints nothing when stdout is not a terminal. I could not reproduce
  the missing lines on this machine; the census no longer depends on them.
- The rewritten blocks, run as `env -i PATH="$PATH" HOME="$HOME" sh -eu -c`
  exactly as published: block 1 exits 0 on the reference, exits 1 on base, and
  exits 1 on the build without `--diff-merges=dense-combined`. Block 2 exits 0
  on all three, which is what a regression guard should do. Five further runs of
  block 1 on the reference all exit 0 with `tests="7" failures="0"` in the
  report, so the gate is deterministic as well as discriminating. Wall-clock
  times under load: block 1 22 to 83 s, block 2 32 to 85 s.
- Timing over the live root board, read-only, three alternating runs per build
  at 710 records and 388 done: base 24143, 38022 and 11113 ms; reference 11266,
  18745 and 17104 ms. The review, on a quieter machine, measured base 5502, 5896
  and 7104 ms against reference 11228, 8481 and 8659 ms. Taken together the
  reference costs up to about twice base over a whole board, and on a machine
  busy with other sessions that difference disappears into a spread of tens of
  seconds. Either way it is seconds, once per process, far inside the 120-second
  block limit. The round-2 claim that the two builds sit inside each other's
  spread was drawn from a quieter sample and does not reproduce; the spec's
  original claim of 20.4 s against 19.6 s does not reproduce either, and neither
  does the review's 3.6 s against 10.2 s, which measured the round-1 rule and
  its per-file `git diff --quiet` spawns.
  Steady state is not measured. No live receipt carries a `base:` yet, so every
  candidate is rejected before any Git work; once every receipt has one, the
  added cost is bounded by one memoised `rev-list` per receipt, measured at
  4.2 ms per spawn on the superproject, so under 1.6 s for a whole board once
  per process.
- Live behaviour. Two of the three round-4 probe pairs are byte-identical
  between base and reference over 388 done records, 357 problems and 77 reports
  of this refusal. In the third, one record differed, `@runtime/…/asp-is-one-file-per-responsibility`,
  clean on base and drifted on the reference, because another session collected
  it between the two probes; the following two pairs agree on it, and the rule
  cannot refuse where base passes. The PRD's evidence case,
  `…/search-returns-ranked-results-each-with-its-source-url`, still reports the
  refusal on both builds, because the sibling that changed `web.ctg` has a
  legacy receipt.
- The recovery path was probed end to end in the fixture. `prd collect` on a
  drifted done record exits 2 with the refusal; `defer`, `release … open` and
  `specced` each exit 0; `claim` first exits 2 with `pre-existing lane must be
  inspected before claim` until the stale `lane/root-search` branch is deleted,
  then exits 0; the second `collect` exits 0 and writes a receipt whose `base`
  is a 40-hex hash, and the record verifies again.

## Remaining limits

- A legacy receipt vouches for nothing, so every record that reports this
  refusal today — 77 when this spec was last measured — is cleared only by
  collecting it again, and none of them clears the moment this lands. The suite
  pins that sequence; the engine offers no single command for it.
- Verify block 1 runs seven fixture collections and block 2 runs the engine
  suite, and `verify` kills a block at 120 s. Measured under `env -i` on a
  machine shared with other sessions, block 1 took 22 to 83 s and block 2 took
  32 to 85 s. The headroom is real but it is not large, and a collection run
  while the machine is busy could hit the limit. `--timeout 30000` protects the
  individual test; nothing protects the block.
- `collect` removes a lane's worktree but leaves its branch, so re-collecting a
  record needs `git branch -D lane/<board>-<slug>` first. That is a separate
  defect, worth its own PRD, and not fixed here.
- A receipt written as an abbreviated hash, and a collection recorded on a board
  outside the scanned graph, vouch for nothing. Both stay conservative.
- A merge that resolves a file inside a done footprint to content neither parent
  had is refused, but only because `--diff-merges=dense-combined` makes `git
  log` name that file; the earlier draft of this spec claimed the refusal came
  for free, and it did not. Since such a merge sits in no lane range, nobody can
  vouch for it, and re-collecting the record is the only thing that clears it. A
  merge that only carries work its parents already had lists no paths under this
  mode and changes nothing.
