---
complexity: 18
footprint:
  - resources/board/collect.py
  - resources/board/brief.py
---

# spec01 — `repo_of` defaults to the repo enclosing a nested board, and a footprint under no repo refuses loudly

`repo_of(prd, board, board_root)` in `resources/board/collect.py` now takes
three arguments. With no `repo:` key: when `board_root == board` (the board
directory itself carries a `.git` — a nested `.pearde` board, its own repo),
it returns `repo_root` of the board's own parent — the code repo the board
sits inside, never the board repo itself. When `board_root != board` (the
board has no `.git` of its own — the old layout, walked past to find the
code repo already) it is unchanged: `board_root`, exactly as before this
default existed. `sort_paths` refuses (`raise Stop`, nothing written) any
footprint path that, once filed under the resolved repo, exists neither on
disk there nor in that repo's git index (`git ls-files`) — the silent drop
the parent PRD measured, replaced by a loud one. The three other call
sites of the old two-argument `repo_of` — two in `collect.py`
(`last_child_commit`, `collect_one`) and one in `brief.py` — are updated to
the new signature; `brief.py`'s was already carrying a stray third argument
before this spec (a pre-existing call/definition mismatch, now consistent).

This already stands, uncommitted in the tree: the code change and four
fixture builders under this PRD's `probe/` (`build_fixture_nested.sh`,
`build_fixture_unnested.sh`, and the no-match/deletion cases built inline in
the verify script below), each run against the real, unmodified
`resources/board/collect.py` entry point. Nothing is left to finish; the
verify script re-proves all four cases from a clean fixture each run.

## Acceptance

- [x] a PRD with no `repo:`, a board at `.pearde/` with its own `.git`, and
      a footprint dirty in the enclosing code repo: `collect` commits that
      footprint in the code repo, not the board repo — proven on
      `probe/build_fixture_nested.sh`
- [x] a board that is not its own repo (no nested `.git`): unchanged
      behaviour — one repo, as before — proven on
      `probe/build_fixture_unnested.sh`
- [x] a footprint path under no group's root refuses loudly: `collect`
      exits non-zero, writes no commit, leaves `state:` untouched
- [x] a footprint path that is a deletion (gone from disk, still in the
      git index) is not mistaken for "under no group's root" — still
      commits

## Verify and Proof

```sh
set -e
PRD=.pearde/prds/collect-commits-the-code-repo-not-the-board-repo-twice/collect-defaults-to-the-boards-enclosing-repo
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT

# 1 — nested board defaults to the enclosing (code) repo, not itself
bash "$PRD/probe/build_fixture_nested.sh" "$T/s1" >/dev/null
python3 resources/board/collect.py fake-prd --board "$T/s1/code/.pearde" --trust --as engineer >/dev/null
test -z "$(git -C "$T/s1/code" status --porcelain -- resources/guard.py)" || { echo "FAIL: guard.py still dirty in the code repo"; exit 1; }
grep -q "guard v2" "$T/s1/code/resources/guard.py" || { echo "FAIL: wrong content committed"; exit 1; }

# 2 — board not its own repo: unchanged, single-repo behaviour
bash "$PRD/probe/build_fixture_unnested.sh" "$T/s2" >/dev/null
python3 resources/board/collect.py fake-prd --board "$T/s2/code/.pearde" --trust --as engineer >/dev/null
test -z "$(git -C "$T/s2/code" status --porcelain -- resources/guard.py)" || { echo "FAIL: guard.py still dirty (unnested)"; exit 1; }

# 3 — a footprint under no group's root refuses loudly, writes no state
bash "$PRD/probe/build_fixture_nested.sh" "$T/s3" >/dev/null
sed -i '' 's/resources\/guard.py/resources\/does-not-exist.py/' "$T/s3/code/.pearde/prds/fake-prd/specs/spec01.md"
git -C "$T/s3/code/.pearde" commit -aqm "break footprint"
if python3 resources/board/collect.py fake-prd --board "$T/s3/code/.pearde" --trust --as engineer >/dev/null 2>&1; then
  echo "FAIL: collect should have refused a footprint under no repo"; exit 1
fi
grep -q "^state: claimed" "$T/s3/code/.pearde/prds/fake-prd/prd.md" || { echo "FAIL: state moved on a refusal"; exit 1; }

# 4 — a footprint that is a deletion still commits (not mistaken for no-match)
bash "$PRD/probe/build_fixture_nested.sh" "$T/s4" >/dev/null
rm "$T/s4/code/resources/guard.py"
python3 resources/board/collect.py fake-prd --board "$T/s4/code/.pearde" --trust --as engineer >/dev/null
git -C "$T/s4/code" log --oneline -1 | grep -q "fake-prd" || { echo "FAIL: deletion footprint did not commit"; exit 1; }

echo "repo_of: all four scenarios pass"
```
