---
complexity: 14
footprint:
  - resources/board/collect.py
  - references/parts/commits.md
---

# spec01 — the board's spelling inside its own repo is the empty string

`sort_paths` computed `board_rel = os.path.relpath(board, board_root)`, which
answers `"."` when the board IS its git repo — the layout this repo has run
since 2026-09-02. `"."` is a prefix of no path git ever prints, so
`inside(path, ["."])` was False for every one of them: `scratch` swallowed no
machine-local dotfile and the rider sweep fired on nothing. Measured on this
board, 543 dirty board paths, 0 recognised as under the board — a worker's
memo or workflow edit written beside its build was committed nowhere, and 6
`.state/` files were reported as if a person had to decide about them. This
unit gives the prefix one honest answer on both layouts and one reader,
`under_board`, so no caller repeats the arithmetic that broke.

**What already stands.** The whole change is written and green in the lane
`lane/board-rel-is-a-third-wrong-board-path-resolution`, 51 added and 6 removed
lines in `resources/board/collect.py`: `board_prefix`, `under_board`, `scratch`
rewritten on it, `board_rel`'s one assignment, the rider sweep's test, and the
claim guard on the `scratch` skip. The PRD's probe is 24 of 24 against the lane
and 4 red against the module as it stood before; every one of the 14 committed
harnesses that read `collect.py` prints the count it printed before the first
edit.

**What is left.** Land it. The counts below were re-taken on the second pass
against the merged tree — the lane's diff applied onto the checkout at
`1880990`, where the sibling `collect-resolves-a-board-path-two-ways-and-both-are-wrong`
has since landed in the same file and in different functions. The two sets of
hunks do not touch: `git apply --3way` of the lane's diff onto that commit
reported both files clean, so the rebase `lanes.merge` runs before its
`--ff-only` merge has nothing to resolve. `a-board-s-own-file-commits-in-the-board-repo`
grew from 12 checks to 20 in that sibling's commit, which is why the count in
the last box moved; every other count is unchanged. `references/parts/commits.md`
is in the footprint above because the first pass wrote the rule's prose there
and named it nowhere — a footprint that does not name it leaves the paragraph
stranded in the lane.

## Acceptance

- [x] `board_prefix(board, board_root)` answers `""` when the two name one directory and the board's directory name when they do not, comparing absolute paths and never a string prefix
- [x] `under_board(path, board_rel)` returns the path respelled relative to the board, or `None` when it is not under the board — and returns the whole name unchanged under an empty prefix, rather than chopping its first character
- [x] `scratch` is written on `under_board` and no longer computes `path[len(board_rel) + 1:]` itself
- [x] `sort_paths` sets `board_rel` from `board_prefix` and the rider sweep tests `under_board(path, board_rel) is not None`, not `inside(path, [board_rel])`
- [x] the `scratch` skip in `sort_paths` fires only on a path no claim names — not one in `--widen`, not one in the union of footprints, not one under the PRD's own folder — so a `footprint:` naming `pearde/.gitignore` is still committed
- [x] the PRD's probe is 24 of 24 on the tree under test, and red on the module without this change
- [x] `a-board-s-own-file-commits-in-the-board-repo` is 20 PASS, `collect-keeps-its-word` 101/101, `collect-is-a-command` 133/133, `hunks-land-where-they-came-from` 47/47, `filing-refuses-a-file-it-does-not-hold` 52/52 and `collect-must-not-reset-the-checkout-it-did-not-write` 31/31, each run with `PEARDE_ROOT` set to the tree under test

## Verify and Proof

```sh
set -e
python3 -c "import ast; ast.parse(open('resources/board/collect.py', encoding='utf-8').read())" && echo "collect.py parses"
grep -n "def board_prefix" resources/board/collect.py
grep -n "def under_board" resources/board/collect.py
grep -n "board_rel = board_prefix(board, board_root)" resources/board/collect.py
grep -n "and under_board(path, board_rel) is not None" resources/board/collect.py
grep -n "and full not in widen and not inside(path, union)" resources/board/collect.py
# the two resolutions this replaces, asserted gone as a check that FAILS on a
# regression — `test -z "$(grep …)" && echo` cannot: under `-e` a failing
# left side of `&&` is not the last command in the list, so bash walks on and
# the line only ever decorates the output
if grep -q 'board_rel = os.path.relpath' resources/board/collect.py; then
  echo "the relpath board_rel is back"; exit 1
fi
echo "no relpath board_rel left"
# only in code — the docstring of `under_board` quotes the old expression on
# purpose, to say what it replaced
if grep -nE '^[[:space:]]*(if|elif|and|return|.*=)[^#]*inside\(path, \[board_rel\]\)' \
   resources/board/collect.py; then
  echo "inside() is deciding the board prefix again"; exit 1
fi
echo "no inside() on the board prefix left"
python3 - <<'PY'
import sys
sys.path.insert(0, "resources/board")
import collect as c
assert c.board_prefix("/r/pearde", "/r/pearde") == ""
assert c.board_prefix("/r/pearde", "/r") == "pearde"
assert c.under_board("memos/m1.md", "") == "memos/m1.md"
assert c.under_board("pearde/memos/m1.md", "pearde") == "memos/m1.md"
assert c.under_board("resources/x.py", "pearde") is None
assert c.scratch(".state/history.jsonl", "") is True
assert c.scratch("memos/m1.md", "") is False
print("the prefix arithmetic is right on both layouts")
PY
PEARDE_ROOT="$PWD" bash pearde/prds/board-rel-is-a-third-wrong-board-path-resolution/probe/verify.sh
PEARDE_ROOT="$PWD" bash resources/invariants/a-board-s-own-file-commits-in-the-board-repo.sh
for h in the-tool-keeps-its-word/collect-keeps-its-word \
         the-board-runs-itself/collect-is-a-command \
         the-board-runs-itself/hunks-land-where-they-came-from \
         filing-refuses-a-file-it-does-not-hold \
         collect-must-not-reset-the-checkout-it-did-not-write; do
  printf '%s ' "$h"
  PEARDE_ROOT="$PWD" PEARDE_HARNESSES=1 bash "pearde/prds/$h/probe/verify.sh" </dev/null | tail -1
done
```
