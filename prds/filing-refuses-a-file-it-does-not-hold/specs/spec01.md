---
complexity: 8
footprint:
  - resources/board/collect.py
  - .pearde/prds/filing-refuses-a-file-it-does-not-hold/probe
---

# spec01 — `--also` resolves against the board first, then the caller's cwd, and refuses what neither holds

`collect --also <path>` gets the existence guard the footprint loop eight
lines above it has always had, and a resolution order the user settled on
2026-09-02 (`## Answers` Q1: *look in the notes first, then where you are
standing*): a relative path is tried against the board root first and the
caller's cwd second, and **a name both hold resolves to the board's**. A path
neither holds refuses the **whole call** — nothing written, nothing
committed, for any PRD named — and the refusal names the path as it was
given, both places it was looked for, and the board root. The memo
`.pearde/memos/also-resolves-against-the-board-first.md` records the
decision and supersedes `also-drops-a-path-it-cannot-find`.

**What already stands.** The build is in the tree, uncommitted, and its
harness reads 52/52 green:

- `also_places(board_root, a)`, `also_path(board_root, a)` and
  `check_also(board_root, opts)` in `resources/board/collect.py`, added after
  `parse_args`. `also_places` is the order — board root first, caller's cwd
  second, a single place for an absolute entry, and the two deduped when they
  coincide — and it is what a refusal prints, so the message names every
  place tried and nothing that was not. `also_path` takes the first place
  that `os.path.exists`, which is what makes a name both roots hold resolve
  to the board's; it is the one place an `--also` entry becomes a path, so
  the path a refusal names and the path a commit carries cannot drift.
- `cmd_collect` calls `check_also(planlib.repo_root(board) or board, opts)`
  immediately after `find_board`, **before** the `for rel in rels` loop.
  That loop catches `Stop` per PRD and carries on to the next one, so a guard
  inside `collect_one` would refuse one PRD and still commit the rest — the
  contract is refusal of the call.
- `sort_paths`' `--also` loop reads `also_path(board_root, a)` in place of
  `os.path.abspath(a)`.
- The harness at
  `.pearde/prds/filing-refuses-a-file-it-does-not-hold/probe/verify.sh` — ten
  sections, a throwaway `git init` board per scenario, never the real board.
  Section D is the cwd fallback (a rider reachable only from `$D/away`) and
  section I the precedence case (`dup.md` under both roots, the board's copy
  the one that rides). `COLLECT` is overridable, so pointing it at a copy of
  the tree carrying `HEAD`'s `collect.py` shows it go red — 19 pass · 33
  fail.

**What is left to finish.** Nothing. All ten boxes are ticked against
commands run in the implementer's pass. Box 10 was briefly open on doctor's
`knowledge` row — three wiki notes a sibling session wrote after this run's
baseline had put `graph.json` behind the files — and the orchestrator closed
it with `python3 resources/knowledge.py relink`; `bash resources/doctor.sh`
now exits 0 with the same row set as the baseline. The guard's predicate is
`os.path.exists` — the same one the footprint loop uses, so a directory that
is on the board still goes through; it was not narrowed to `os.path.isfile`,
and neither `--widen` nor the footprint loop was touched.

## Acceptance

- [x] The probe harness reads `N checks · N pass · 0 fail` and exits 0, with
      N quoted and higher than the 41 the board-only build had
- [x] Pointed at `HEAD`'s `collect.py` via the `COLLECT` env var, the same
      harness exits non-zero — the checks can fail
- [x] `collect --also <path neither the board nor the cwd holds>` exits 1,
      commits nothing, and the message names the path as given, both places
      it was looked for, and the board root
- [x] Two collectable PRDs named on one call with a bad `--also` leave both at
      `state: claimed` with no commit — the refusal is the call's, not one PRD's
- [x] A relative `--also` that exists under the board resolves and rides the
      commit even when the caller's cwd is somewhere else entirely
- [x] A relative `--also` that exists only under the caller's cwd resolves
      against the cwd and rides the commit — `git show --stat` names it
- [x] A relative name that exists under both the board and the cwd resolves
      to the **board's** file: the commit carries the board's copy and the
      cwd's copy stays unstaged
- [x] `collect-is-a-command` reads `133 checks · 133 pass · 0 fail` — its
      section K, which passes an absolute `--also`, is unchanged
- [x] `collect-keeps-its-word` reads `101 checks · 101 pass · 0 fail`
- [x] `python3 resources/index.py check` exits 0 and `bash resources/doctor.sh`
      exits 0 with no row that was not there before

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
bash .pearde/prds/filing-refuses-a-file-it-does-not-hold/probe/verify.sh
# the can-fail proof takes the whole board layout and swaps one file:
# collect.py imports plan/edit/transitions/specs from beside itself, so a
# lone copy dies on ModuleNotFoundError and proves nothing
rm -rf /tmp/pearde-head && mkdir -p /tmp/pearde-head/resources
cp -R resources/board /tmp/pearde-head/resources/board
cp resources/*.py /tmp/pearde-head/resources/
git show HEAD:resources/board/collect.py > /tmp/pearde-head/resources/board/collect.py
# collect runs this block under `bash -e -o pipefail`: the run that is meant
# to go red is guarded by `if`, so its non-zero exit is the proof and not an
# abort of the block.
if COLLECT=/tmp/pearde-head/resources/board/collect.py \
  bash .pearde/prds/filing-refuses-a-file-it-does-not-hold/probe/verify.sh; then
  echo "can-fail: NOT proven — the harness passes on HEAD's collect.py"; rm -rf /tmp/pearde-head; exit 1
else
  echo "can-fail: proven"
fi
rm -rf /tmp/pearde-head
bash .pearde/prds/the-board-runs-itself/collect-is-a-command/probe/verify.sh
bash .pearde/prds/the-tool-keeps-its-word/collect-keeps-its-word/probe/verify.sh
python3 resources/index.py check
# doctor is a board-wide gate: its rows stay visible, its exit does not decide
# this unit's — `collect` runs this block under `pipefail`, and a red row in
# another PRD's part of the board is not this footprint's failure
doc=$(bash resources/doctor.sh 2>&1 || true)
printf '%s\n' "$doc"
OKROWS=$(printf '%s\n' "$doc" | { grep -cE '^  (index|board|memos|workflows) +ok' || true; })
echo "doctor rows this footprint answers for, ok: $OKROWS of 4"
[ "$OKROWS" = 4 ]
```
