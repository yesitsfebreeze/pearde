---
complexity: 3
footprint:
  - .pearde/prds/the-board-runs-itself/readme-in-three-rings/probe/verify.sh
---

# spec04 — the README harness reads the round table at the header it now has

`readme-in-three-rings` section D proves the README's seven round rows are
`references/parts/loop.md`'s, byte for byte. It pulls both tables with an awk
anchored on `^| step | command`. The `pearde next` work (`9a7ce2c`) re-aimed
loop.md's table to `| step | the orchestrator decides |` and the README's
mirror edit followed it, so the anchor matched nothing: awk read zero rows out
of a table that was sitting right there, and the byte-for-byte check compared
two empty files and passed. One red row, and one row that had quietly stopped
proving anything.

Both anchors now read `^| step |`, which matches the header whatever its second
column is called, and the rows are selected as before by `^| [1-7] `.

## What the probe already established

The retired anchor reads 0 rows from the current README; the re-aimed one reads
7, and diffing them against loop.md's 7 is empty — so the check is back to
proving what it was written to prove, and it fails again the moment either file
drifts. The harness went from 71 to 72 of its 74 checks.

What is left is not this contract's. The two rows still red in that harness are
`H quickstart.sh exits 0` and `H …and every check passed`, which need a fresh
`init --example` board to pass doctor — the contract of
`init-seeds-a-board-doctor-calls-green`. A third, `G index.py check is silent`,
is red for a reason outside every PRD on this board: see the report's findings.
`workflows-on-the-board/workflow-skill` pins this harness at
`74 checks · 74 pass · 0 fail` and therefore stays red until that sibling lands;
that cascade is expected, not a regression from this spec.

## Acceptance

- [x] `bash .pearde/prds/the-board-runs-itself/readme-in-three-rings/probe/verify.sh 2>&1 | grep -c '^FAIL: D'` reports 0 — section D was 1 failure before
- [x] `grep -c '| step | command' .pearde/prds/the-board-runs-itself/readme-in-three-rings/probe/verify.sh` reports 0 — the retired anchor is gone from both awk programs
- [x] section D of this PRD's harness passes: the retired anchor reads 0 rows from the README, the re-aimed one reads 7, and they diff empty against loop.md's 7
- [x] every remaining failure in that harness is an `H` or `G` row — `grep -c '^FAIL: [^HG]'` reports 0 — so nothing outside the quickstart and the index rows is left
- [x] `grep -c '^| step | the orchestrator decides |'` reports 1 in both `README.md` and `references/parts/loop.md` — the fixture moved to meet the tree, and the tree was not moved to meet the fixture

## Verify and Proof

```sh
bash .pearde/prds/the-board-runs-itself/readme-in-three-rings/probe/verify.sh 2>&1 | grep -E '^FAIL|^[0-9]+ checks'
grep -c '| step | command' .pearde/prds/the-board-runs-itself/readme-in-three-rings/probe/verify.sh
grep -c '^| step | the orchestrator decides |' README.md references/parts/loop.md
bash .pearde/prds/seven-closed-probes-drifted-red/the-fixtures-meet-the-tool/probe/verify.sh
```
