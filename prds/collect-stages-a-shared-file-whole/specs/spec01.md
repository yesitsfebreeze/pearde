---
complexity: 14
footprint:
  - resources/board/collect.py
---

# spec01 — the claim baseline records the code repo, not only the board's

`snapshot()` records one repo: `repo_root(prd["dir"])`, which is the repo the
**board** is in. On every layout this board ships — a nested `.pearde` with a
`.git` of its own, or the linked worktree this machine runs — that is not the
repo the code is in, so the baseline holds nine board paths and zero code
paths. `new_hunks` then finds nothing inherited for any code file, returns
`"all"`, and the hunk-splitter that step 3 is built around never runs once.
This unit gives the baseline both repos and keys every read by root.

**What already stands** (probe pass one, uncommitted in the tree): `snapshot()`
records `repo_of()`'s repo into `diff.repo` / `untracked.repo` / `repo`
alongside the board's, deleting a stale second side on a re-snapshot;
`baseline()` returns `sides` keyed `board` and `repo`, keeping top-level
`hunks` / `untracked` as the board side for the readers written against the
one-repo shape; `sort_paths` grows `side(root)` and `predates` / `new_hunks`
read through it. A root neither repo — one `--also` reached — has no side, and
`None` means what it always meant: whole or not at all.

**What is left**: nothing in the mechanism. Confirm the back-compat alias is
still needed rather than dropping it — `hunks-land-where-they-came-from`'s
probe reads `baseline(...)["hunks"]["src/view.js"]` directly, and its fixture
is the one layout (board not its own repo) where that path is the board side.

## Acceptance

- [x] On a board that is its own repo, a claim snapshot names a dirty code-repo path: `.claims/<prd>/repo` exists and `diff.repo` holds the path
- [x] A file whose dirt is partly older than the claim and partly newer is staged by hunk — the commit holds the newer lines and not the older ones
- [x] The older lines are still in the working tree after the collect, unstaged
- [x] On a board that is NOT its own repo, no `repo` side is written and behaviour is byte-for-byte what it was
- [x] A claim dir holding only the one-repo shape still loads, and `baseline()` returns `sides` with a `board` key only
- [x] `hunks-land-where-they-came-from`'s probe still reports every check passing and none failing — the tally is parsed, never a pinned total

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
{ bash .pearde/prds/collect-stages-a-shared-file-whole/probe/verify.sh 0 2 6 7 \
    > /tmp/s01.out 2>&1 || true; }
tail -3 /tmp/s01.out
bash .pearde/prds/the-board-runs-itself/hunks-land-where-they-came-from/probe/verify.sh \
    > /tmp/s01b.out 2>&1 || true
tail -1 /tmp/s01b.out
grep -q 'verify.sh exit 0' /tmp/s01.out
[ "$(grep -c 'FAIL ' /tmp/s01.out)" = 0 ]
# the neighbour's tally is parsed, never pinned — a passing check it gains
# must not redden this unit
{ T=$(grep -oE '[0-9]+ checks · [0-9]+ pass · [0-9]+ fail' /tmp/s01b.out | tail -1) || true; }
printf 'hunks-land-where-they-came-from: %s\n' "$T"
printf '%s\n' "$T" | awk '{ if (NF != 8 || $1 != $4 || $7 != 0) exit 1 }'
```
