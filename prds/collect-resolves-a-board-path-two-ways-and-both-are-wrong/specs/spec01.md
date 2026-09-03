---
complexity: 14
footprint:
  - resources/board/collect.py
---

# spec01 — which repo holds a footprint is git's answer, never a string's

`foot_root` decided board membership by string prefix and resolved a footprint
against the code repo only. Both readings are wrong on a layout this repo
actually runs, and each fails in a different direction: a footprint spelled the
board's own way is refused outright, and a footprint of a code checkout nested
under the board is routed to the board, staged against an index that ignores
it, and committed as nothing at all. This unit replaces the prefix test with
`git rev-parse --show-toplevel`, tries every spelling a footprint can carry,
and makes the refusal name the places it looked.

**What already stands.** The whole change is written and green in the lane
`lane/collect-resolves-a-board-path-two-ways-and-both-are-wrong`, 123 lines in
`resources/board/collect.py`: `holder`, `same_dir`, `foot_places`, `foot_root`,
`tracked_in`, and the refusal message in `sort_paths`. The probe is 7/7 against
the lane and 3/7 against the unpatched tree; the invariant is 12/12; four
`collect` harnesses are unchanged at 101, 133, 47 and 52 pass.

**What is left.** Land it, and confirm the counts below on the tree the
implementer holds — the lane is behind whatever landed since.

## Acceptance

- [x] `holder(path)` answers with `git -C <nearest existing dir> rev-parse --show-toplevel`, caches per directory, and falls back to `planlib.repo_root` when git cannot be run
- [x] `foot_places(p, board, board_root, repo)` returns the places a footprint spelling can resolve, in order, code repo first, with no duplicates, and an absolute path as its own only place
- [x] `foot_root` returns the first place the filesystem or an index holds, spelled inside the checkout that holds it; a footprint no place holds yet resolves to the first place, as before
- [x] the root `foot_root` returns is one of the caller's own spellings of `repo`, `board_root` or `board` whenever it names the same directory, so `.pearde` does not become `pearde` mid-run
- [x] no comparison of a footprint against the board's path by `startswith` remains in `foot_root`
- [x] `sort_paths`' refusal names every place that was tried and no function that did not refuse
- [x] the probe is 7 of 7 and the invariant 12 of 12 on the tree under test
- [x] `collect-keeps-its-word` 101/101, `collect-is-a-command` 133/133, `hunks-land-where-they-came-from` 47/47 and `filing-refuses-a-file-it-does-not-hold` 52/52, run with `PEARDE_ROOT` set to the tree under test

## Verify and Proof

```sh
python3 -c "import ast; ast.parse(open('resources/board/collect.py', encoding='utf-8').read())" && echo "collect.py parses"
grep -n "def holder" resources/board/collect.py
grep -n "def foot_places" resources/board/collect.py
grep -n "rev-parse\", \"--show-toplevel" resources/board/collect.py
test -z "$(grep -n 'startswith(b + os.sep)' resources/board/collect.py)" && echo "no board prefix test left"
test -z "$(grep -n 'repo_of matched no repo' resources/board/collect.py)" && echo "no wrong refusal left"
PEARDE_ROOT="$PWD" bash .pearde/prds/collect-resolves-a-board-path-two-ways-and-both-are-wrong/probe/verify.sh
PEARDE_ROOT="$PWD" bash resources/invariants/a-board-s-own-file-commits-in-the-board-repo.sh
for h in the-tool-keeps-its-word/collect-keeps-its-word \
         the-board-runs-itself/collect-is-a-command \
         the-board-runs-itself/hunks-land-where-they-came-from \
         filing-refuses-a-file-it-does-not-hold; do
  printf '%s ' "$h"
  PEARDE_ROOT="$PWD" PEARDE_HARNESSES=1 bash ".pearde/prds/$h/probe/verify.sh" </dev/null | tail -1
done
```
