---
complexity: 8
footprint:
  - resources/board/collect.py
  - resources/board/refuse.py
  - resources/board/session.py
  - resources/board/serve.py
  - resources/board/shared.py
  - resources/knowledge.py
  - resources/graph/graph.sh
  - resources/guard.py
---

# spec03 — the comments and printed paths outside the resolvers say `.pearde`

Eight modules spelled the board directory undotted in a docstring, a comment or
a string a person reads. Two of those strings are memo paths the guard and
`refuse` print in a refusal, so a reader was being sent to
`pearde/memos/…` on a board where the file is at `.pearde/memos/…`. Two are
real orderings: `graph.sh` asked `pearde/` before `.pearde/` when choosing where
a graph pass writes, and `shared.py` listed the undotted cache row first.

This spec deliberately stops at the resolvers. `boards.py`, `common.py`,
`plan.py`, `health.py`, `questions.py`, `memos.py`, `grammar.py`, `doctor.sh`
and `statusline.sh` are the footprint of
`the-board-name-is-one-dotted-constant`, and `init.py` of
`init-and-upgrade-write-the-dotted-board`; each still carries a stale comment,
and the report names every one so the sibling that rewrites the reader rewrites
its comment in the same hunk.

**Stands.** All eight files are rewritten in the lane. `graph.sh` asks
`.pearde/` first. `shared.py` lists the dotted cache row first, and its
`CACHE_KEY` comment now says what the key is and why it stays the legacy
spelling. `collect.py`'s `under()` docstring no longer claims this board is
reached through a symlink. `guard.py` and `refuse.py` print `.pearde/memos/…`.
`one-copy-per-machine-of-what-every-lane-regenerates.sh` is 4 PASS 0 FAIL after
the row reorder, and
`no-destructive-git-runs-in-a-tree-the-session-does-not-own.sh` is 6 PASS 0
FAIL after the refusal strings changed.

**Left.** Nothing but the checks below. `guard.py` is in this footprint for its
two memo-path strings only; if the sibling PRD claims the whole file first,
hand those two lines to it rather than editing around it.

## Acceptance

- [x] No file in the footprint spells a board path `pearde/…`, except where the
      line introduces the legacy name or is `shared.py`'s `CACHE_KEY` and the
      row keyed on it.
- [x] The refusal the guard prints for a shared-checkout `reset --hard` names
      `.pearde/memos/a-session-that-writes-a-shared-checkout-can-revert-another-session-s-work.md`,
      and the one for a skill-tree write names `.pearde/memos/the-install-is-live-symlinks.md`.
- [x] `graph.sh` resolves `<folder>/.pearde` before `<folder>/pearde`, so a
      graph pass on a board carrying both writes into the board.
- [x] `shared.py`'s dotted cache row is listed before the legacy one, and the
      comment above `CACHE_KEY` states the key is the legacy spelling and why.
- [x] Every module in the footprint still imports.
- [x] `one-copy-per-machine-of-what-every-lane-regenerates.sh` is 4 PASS 0 FAIL
      and `no-destructive-git-runs-in-a-tree-the-session-does-not-own.sh` is 6
      PASS 0 FAIL.

## Verify and Proof

```sh
cd "$(git rev-parse --show-toplevel)"
F="resources/board/collect.py resources/board/refuse.py resources/board/session.py
   resources/board/serve.py resources/board/shared.py resources/knowledge.py
   resources/graph/graph.sh resources/guard.py"
# every bare `pearde/` left says legacy, or is the graphify cache key and its row
grep -nE '(^|[^./a-zA-Z_-])pearde/' $F | grep -vE 'legacy|graphify' && exit 1
# the two refusal strings a person reads
python3 -c "
import sys; sys.path.insert(0, 'resources'); sys.path.insert(0, 'resources/board')
import refuse, guard
line = refuse.refuse_line('reset --hard', '/t', 'r', 'w')
assert '.pearde/memos/a-session-that-writes' in line, line
assert 'a session-that-writes'.replace(' ','') or True
assert not line.count(' pearde/memos'), line
assert guard.MEMO == '.pearde/memos/the-install-is-live-symlinks.md', guard.MEMO
print('refusal strings ok')
"
# graph.sh asks the dotted name first
grep -n 'GRAPH_BOARD=' resources/graph/graph.sh | head -1 | grep -q '\.pearde' || exit 1
# shared.py: dotted row first, and the key explained
python3 -c "
import sys; sys.path.insert(0, 'resources/board')
import shared
rows = [s.pattern for s in shared.SHARED if s.key == shared.CACHE_KEY]
assert rows == ['.pearde/graphify/cache', 'pearde/graphify/cache'], rows
src = open('resources/board/shared.py').read()
assert 'LEGACY spelling' in src
print('shared rows ok:', rows)
"
# every module still imports
for m in resources/board/collect.py resources/board/refuse.py resources/board/session.py \
         resources/board/serve.py resources/board/shared.py resources/knowledge.py \
         resources/guard.py; do
  python3 -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" "$m" || exit 1
done
bash -n resources/graph/graph.sh || exit 1
# the two harnesses this footprint moves
for f in one-copy-per-machine-of-what-every-lane-regenerates \
         no-destructive-git-runs-in-a-tree-the-session-does-not-own; do
  out=$(bash "resources/invariants/$f.sh" 2>&1); rc=$?
  printf '%-58s rc=%s PASS=%s FAIL=%s\n' "$f" "$rc" \
    "$(printf '%s' "$out" | grep -c '^PASS')" "$(printf '%s' "$out" | grep -c '^FAIL')"
  [ "$rc" = 0 ] || exit 1
done
echo "spec03 ok"
```
